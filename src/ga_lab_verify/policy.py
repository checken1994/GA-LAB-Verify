from __future__ import annotations

import re

from .config import PolicyConfig
from .models import CheckResult, CheckStatus


_WEAKENING_PATTERNS = (
    ("pytest skip", re.compile(r"^\+.*(?:pytest\.skip|pytest\.mark\.skip)")),
    ("pytest xfail", re.compile(r"^\+.*(?:pytest\.xfail|pytest\.mark\.xfail)")),
    ("unittest skip", re.compile(r"^\+.*@unittest\.skip")),
    ("placeholder assert", re.compile(r"^\+\s*assert\s+True(?:\s|$)")),
)


def evaluate_repository_policy(policy: PolicyConfig, *, clean: bool, changed: list[str], diff_text: str) -> list[CheckResult]:
    results: list[CheckResult] = []

    if policy.require_clean_worktree:
        results.append(CheckResult(
            check_id="policy.clean_worktree",
            status=CheckStatus.PASS if clean else CheckStatus.FAIL,
            mandatory=True,
            reason="worktree is clean" if clean else "worktree contains uncommitted or untracked changes",
        ))

    protected_hits = sorted({
        path
        for path in changed
        for prefix in policy.protected_paths
        if path == prefix.rstrip("/") or path.startswith(prefix)
    })
    results.append(CheckResult(
        check_id="policy.protected_paths",
        status=CheckStatus.FAIL if protected_hits else CheckStatus.PASS,
        mandatory=True,
        reason=("protected paths changed: " + ", ".join(protected_hits) if protected_hits else "no protected path changes detected"),
    ))

    if policy.forbid_test_weakening:
        hits: list[str] = []
        for line in diff_text.splitlines():
            for label, pattern in _WEAKENING_PATTERNS:
                if pattern.search(line):
                    hits.append(label)
        results.append(CheckResult(
            check_id="policy.test_integrity",
            status=CheckStatus.FAIL if hits else CheckStatus.PASS,
            mandatory=True,
            reason=("new test-weakening patterns detected: " + ", ".join(sorted(set(hits))) if hits else "no configured test-weakening patterns detected"),
        ))

    return results
