from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


class GitError(RuntimeError):
    pass


@dataclass(frozen=True)
class GitSnapshot:
    head_sha: str
    clean: bool


def _git(repo: Path, *args: str, timeout: int = 30) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitError(f"unable to execute git: {exc}") from exc
    if proc.returncode != 0:
        raise GitError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def snapshot(repo: Path) -> GitSnapshot:
    head = _git(repo, "rev-parse", "HEAD").strip()
    if len(head) != 40:
        raise GitError("HEAD did not resolve to a full commit SHA")
    status = _git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    return GitSnapshot(head_sha=head, clean=(status.strip() == ""))


def resolve_ref(repo: Path, ref: str) -> str:
    sha = _git(repo, "rev-parse", f"{ref}^{{commit}}").strip()
    if len(sha) != 40:
        raise GitError(f"ref {ref!r} did not resolve to a full commit SHA")
    return sha


def changed_files(repo: Path, base_sha: str, head_sha: str) -> list[str]:
    out = _git(repo, "diff", "--name-only", f"{base_sha}..{head_sha}")
    return [line.strip() for line in out.splitlines() if line.strip()]


def unified_diff(repo: Path, base_sha: str, head_sha: str) -> str:
    return _git(repo, "diff", "--no-ext-diff", "--unified=0", f"{base_sha}..{head_sha}", timeout=60)
