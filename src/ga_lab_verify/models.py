from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class CheckStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class Verdict(StrEnum):
    SAFE_TO_MERGE = "SAFE_TO_MERGE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    status: CheckStatus
    mandatory: bool
    reason: str
    duration_ms: int = 0
    command: list[str] | None = None
    return_code: int | None = None
    stdout_sha256: str | None = None
    stderr_sha256: str | None = None
    stdout_bytes: int = 0
    stderr_bytes: int = 0
    stdout: str | None = None
    stderr: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class VerificationReport:
    schema_version: int
    tool_version: str
    created_at: str
    repository: str
    tested_sha: str | None
    base_sha: str | None
    config_sha256: str
    verdict: Verdict
    reasons: list[str] = field(default_factory=list)
    checks: list[CheckResult] = field(default_factory=list)
    evidence_sha256: str | None = None

    def to_dict(self, include_evidence_hash: bool = True) -> dict[str, Any]:
        data: dict[str, Any] = {
            "schema_version": self.schema_version,
            "tool_version": self.tool_version,
            "created_at": self.created_at,
            "repository": self.repository,
            "tested_sha": self.tested_sha,
            "base_sha": self.base_sha,
            "config_sha256": self.config_sha256,
            "verdict": self.verdict.value,
            "reasons": list(self.reasons),
            "checks": [c.to_dict() for c in self.checks],
        }
        if include_evidence_hash:
            data["evidence_sha256"] = self.evidence_sha256
        return data
