from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .config import VerifyConfig
from .git_repo import GitError, changed_files, resolve_ref, snapshot, unified_diff
from .models import CheckResult, CheckStatus, VerificationReport, Verdict
from .policy import evaluate_repository_policy
from .runner import run_check
from .util import sha256_bytes


def derive_verdict(checks: list[CheckResult]) -> tuple[Verdict, list[str]]:
    mandatory = [c for c in checks if c.mandatory]
    failed = [c for c in mandatory if c.status is CheckStatus.FAIL]
    unknown = [c for c in mandatory if c.status is CheckStatus.UNKNOWN]
    if failed:
        return Verdict.BLOCKED, [f"{c.check_id}: {c.reason}" for c in failed]
    if unknown:
        return Verdict.UNKNOWN, [f"{c.check_id}: {c.reason}" for c in unknown]
    return Verdict.SAFE_TO_MERGE, ["all mandatory checks passed for the tested SHA"]


def verify(repo: Path, config: VerifyConfig, config_raw: bytes, *, base_ref: str | None = None, include_output: bool = False) -> VerificationReport:
    repo = repo.resolve()
    checks: list[CheckResult] = []
    tested_sha: str | None = None
    base_sha: str | None = None

    try:
        snap = snapshot(repo)
        tested_sha = snap.head_sha
        changed: list[str] = []
        diff_text = ""
        if base_ref:
            base_sha = resolve_ref(repo, base_ref)
            changed = changed_files(repo, base_sha, tested_sha)
            diff_text = unified_diff(repo, base_sha, tested_sha)
        checks.extend(evaluate_repository_policy(config.policy, clean=snap.clean, changed=changed, diff_text=diff_text))
    except GitError as exc:
        checks.append(CheckResult(check_id="git.identity", status=CheckStatus.UNKNOWN, mandatory=True, reason=str(exc)))

    for spec in config.checks:
        checks.append(run_check(spec, repo, include_output=include_output))

    verdict, reasons = derive_verdict(checks)
    return VerificationReport(
        schema_version=1, tool_version=__version__,
        created_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        repository=str(repo), tested_sha=tested_sha, base_sha=base_sha,
        config_sha256=sha256_bytes(config_raw), verdict=verdict, reasons=reasons, checks=checks,
    )
