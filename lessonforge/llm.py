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
    "gemini": "gemini-3.6-flash",
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


def _post(url: str, payload: dict, headers: dict, retries: int = 6) -> dict:
    """POST JSON. Free tiers rate-limit hard (HTTP 429), so back off patiently:
    honor Retry-After when given, else wait 5s, 10s, 20s, 40s, 60s."""
    data = json.dumps(payload).encode()
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "Accept": "application/json",
                                                       # Some APIs sit behind Cloudflare, which blocks the default
                                                       # "Python-urllib" user agent (HTTP 403, error code 1010).
                                                       "User-Agent": "lessonforge/1.0 (+https://github.com)", **headers})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="ignore")[:500]
            last = LLMError(f"HTTP {e.code} from {url.split('?')[0]}: {body}")
            low = body.lower()
            if e.code == 429 and ("per day" in low or "tpd" in low or "rpd" in low or "quota" in low):
                # A DAILY quota will not recover in seconds - fail fast instead of waiting for hours.
                raise LLMError(f"daily quota exhausted for this model: {body[:200]}")
            if e.code in (429, 500, 502, 503, 504, 529) and attempt < retries - 1:
                wait = min(60, 5 * 2 ** attempt)
                ra = e.headers.get("Retry-After") if e.headers else None
                if ra and ra.strip().isdigit():
                    wait = min(90, int(ra) + 1)
                print(f"           (rate limited / busy: HTTP {e.code}; waiting {wait}s and retrying)")
                time.sleep(wait)
                continue
            raise last
        except urllib.error.URLError as e:
            last = LLMError(f"Network error calling {url.split('?')[0]}: {e}")
            time.sleep(2 ** attempt)
    raise last  # type: ignore[misc]


class LLM:
    """call(system, user) -> str. Same signature for every provider."""

    def __init__(self, cfg: LLMConfig, mock_responder=None):
        self.cfg = cfg
        self.mock_responder = mock_responder
        self.calls = 0

    def call(self, system: str, user: str, *, temperature: float | None = None, tag: str = "",
             json_mode: bool = False) -> str:
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
            url, hdr = f"{base.rstrip('/')}/chat/completions", {"Authorization": f"Bearer {key}"}
            payload = {"model": self.cfg.model, "temperature": t, "max_tokens": self.cfg.max_tokens,
                       "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
            extras = {}
            if json_mode:
                extras["response_format"] = {"type": "json_object"}  # provider-enforced JSON
            if "qwen" in self.cfg.model.lower():
                extras["reasoning_format"] = "hidden"  # Groq: drop <think> text from the reply
            if "gpt-oss" in self.cfg.model or self.cfg.model.startswith(("o1", "o3", "o4")):
                # Reasoning models spend output tokens "thinking" first. With a small token cap they
                # can run out before writing the answer (empty reply). Low effort keeps room for it.
                extras["reasoning_effort"] = "low"
            try:
                out = _post(url, {**payload, **extras}, hdr)
            except LLMError as e:
                if extras and "HTTP 400" in str(e):  # provider rejected an optional param -> plain request
                    out = _post(url, payload, hdr)
                else:
                    raise
            choice = out["choices"][0]
            text = (choice.get("message") or {}).get("content") or ""
            if not text.strip():
                raise LLMError(f"empty reply (finish_reason={choice.get('finish_reason')}); "
                               f"raise LF_{'JUDGE' if t == 0 else 'GEN'}_MAX_TOKENS if this repeats")
            return text
        if p == "gemini":
            key = os.getenv("GEMINI_API_KEY") or os.environ["GOOGLE_API_KEY"]
            out = _post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.cfg.model}:generateContent",
                {"systemInstruction": {"parts": [{"text": system}]},
                 "contents": [{"role": "user", "parts": [{"text": user}]}],
                 # Gemini 3.5+ models reject sampling params (temperature/top_p/top_k), so none are sent.
                 "generationConfig": {"maxOutputTokens": self.cfg.max_tokens,
                                      **({"responseMimeType": "application/json"} if json_mode else {})}},
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
        raw = self.call(system, user, temperature=0.0, tag=tag, json_mode=True)
        try:
            return extract_json(raw)
        except ValueError:
            raw = self.call(system, user + "\n\nYour previous reply was not valid JSON. Reply with ONLY the JSON object.",
                            temperature=0.0, tag=tag, json_mode=True)
            return extract_json(raw)


def extract_json(text: str) -> dict:
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()  # reasoning models
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
    # Judges only return a short JSON verdict; a smaller cap keeps each request under
    # free-tier tokens-per-minute limits (e.g. Groq counts max_tokens toward TPM).
    max_tok = int(os.getenv(f"LF_{role.upper()}_MAX_TOKENS") or (8192 if role == "gen" else 3000))
    return LLM(LLMConfig(provider=prov, model=model, temperature=temp, max_tokens=max_tok), mock_responder)
