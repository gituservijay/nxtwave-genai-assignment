from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class CheckResult:
    id: str
    passed: bool
    reason: str
    evidence: str = ""
    fix: str = ""
    dimension: str = ""
    kind: str = "code"  # code | llm

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Evaluation:
    results: list[CheckResult]

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def failed(self) -> list[CheckResult]:
        return [r for r in self.results if not r.passed]

    @property
    def score(self) -> int:
        return sum(r.passed for r in self.results)

    def to_dict(self) -> dict:
        return {"passed": self.passed, "score": f"{self.score}/{len(self.results)}",
                "results": [r.to_dict() for r in self.results]}


@dataclass
class Attempt:
    number: int
    lesson: str
    evaluation: Evaluation
    changes_requested: list[str] = field(default_factory=list)  # feedback that produced THIS draft
    injected_error: str | None = None
    regressions: list[str] = field(default_factory=list)
