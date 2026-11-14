"""Thin, dependency-free LLM client.

Why raw HTTP (urllib) instead of vendor SDKs?
  * One interface for every provider -> the pipeline never knows which model it talks to.
  * Zero install friction for reviewers (no SDK version conflicts).
  * Easy to swap the *generator* and the *judge* to different models, which reduces
    "self-grading" bias (a model tends to like its own writing).

Supported providers (pick with LF_GEN_PROVIDER / LF_JUDGE_PROVIDER or auto-detect):
  anthropic | openai | gemini | openai_compat (Groq, OpenRouter, Together, Ollama...) | mock
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


class LLMError(RuntimeError):
    pass


@dataclass
class LLMConfig:
    provider: str
    model: str
    temperature: float = 0.4
    max_tokens: int = 8192


DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4.1-mini",
    "gemini": "gemini-2.5-flash",
    "openai_compat": "llama-3.3-70b-versatile",  # Groq default; override with LF_*_MODEL
    "mock": "mock",
}


def autodetect_provider() -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        return "gemini"
    if os.getenv("OPENAI_COMPAT_API_KEY"):
        return "openai_compat"
    return "mock"


def _post(url: str, payload: dict, headers: dict, retries: int = 3) -> dict:
    data = json.dumps(payload).encode()
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="ignore")[:500]
            last = LLMError(f"HTTP {e.code} from {url}: {body}")
            if e.code in (429, 500, 502, 503, 529):  # transient -> back off and retry
                time.sleep(2 ** attempt * 3)
                continue
            raise last
        except urllib.error.URLError as e:
            last = LLMError(f"Network error calling {url}: {e}")
            time.sleep(2 ** attempt)
    raise last  # type: ignore[misc]


class LLM:
    """call(system, user) -> str. Same signature for every provider."""

    def __init__(self, cfg: LLMConfig, mock_responder=None):
        self.cfg = cfg
        self.mock_responder = mock_responder
        self.calls = 0

    def call(self, system: str, user: str, *, temperature: float | None = None, tag: str = "") -> str:
        self.calls += 1
        t = self.cfg.temperature if temperature is None else temperature
        p = self.cfg.provider
        if p == "mock":
            if not self.mock_responder:
                raise LLMError("mock provider needs a responder")
            return self.mock_responder(system, user, tag)
        if p == "anthropic":
            out = _post(
                "https://api.anthropic.com/v1/messages",
                {"model": self.cfg.model, "max_tokens": self.cfg.max_tokens, "temperature": t,
                 "system": system, "messages": [{"role": "user", "content": user}]},
                {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
            )
            return "".join(b.get("text", "") for b in out.get("content", []))
        if p in ("openai", "openai_compat"):
            if p == "openai":
                base, key = "https://api.openai.com/v1", os.environ["OPENAI_API_KEY"]
            else:
                base = os.getenv("OPENAI_COMPAT_BASE_URL", "https://api.groq.com/openai/v1")
                key = os.environ.get("OPENAI_COMPAT_API_KEY", "none")
            out = _post(
                f"{base.rstrip('/')}/chat/completions",
                {"model": self.cfg.model, "temperature": t, "max_tokens": self.cfg.max_tokens,
                 "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
                {"Authorization": f"Bearer {key}"},
            )
            return out["choices"][0]["message"]["content"]
        if p == "gemini":
            key = os.getenv("GEMINI_API_KEY") or os.environ["GOOGLE_API_KEY"]
            out = _post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.cfg.model}:generateContent",
                {"systemInstruction": {"parts": [{"text": system}]},
                 "contents": [{"role": "user", "parts": [{"text": user}]}],
                 "generationConfig": {"temperature": t, "maxOutputTokens": self.cfg.max_tokens}},
                {"x-goog-api-key": key},  # header works for both classic "AIza..." and newer "AQ..." keys
            )
            parts = out.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
            if not text:
                raise LLMError(f"Gemini returned no text: {json.dumps(out)[:300]}")
            return text
        raise LLMError(f"Unknown provider {p}")

    def call_json(self, system: str, user: str, *, tag: str = "") -> dict:
        """Ask for JSON, parse robustly, retry once with a repair nudge if parsing fails."""
        raw = self.call(system, user, temperature=0.0, tag=tag)
        try:
            return extract_json(raw)
        except ValueError:
            raw = self.call(system, user + "\n\nYour previous reply was not valid JSON. Reply with ONLY the JSON object.",
                            temperature=0.0, tag=tag)
            return extract_json(raw)


def extract_json(text: str) -> dict:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    else:
        s, e = text.find("{"), text.rfind("}")
        if s == -1 or e == -1:
            raise ValueError("no JSON object found")
        text = text[s : e + 1]
    return json.loads(text)


def build_llm(role: str, mock_responder=None) -> LLM:
    """role = 'gen' or 'judge'. Env: LF_GEN_PROVIDER, LF_GEN_MODEL, LF_JUDGE_PROVIDER, LF_JUDGE_MODEL."""
    prov = os.getenv(f"LF_{role.upper()}_PROVIDER") or autodetect_provider()
    model = os.getenv(f"LF_{role.upper()}_MODEL") or DEFAULT_MODELS[prov]
    temp = 0.7 if role == "gen" else 0.0
    return LLM(LLMConfig(provider=prov, model=model, temperature=temp), mock_responder)
