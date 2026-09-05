from __future__ import annotations

import subprocess
import time
from pathlib import Path

from .config import CommandCheckConfig
from .models import CheckResult, CheckStatus
from .util import sha256_bytes


def run_check(spec: CommandCheckConfig, repo: Path, *, include_output: bool = False) -> CheckResult:
    started = time.monotonic()
    try:
        proc = subprocess.run(
            list(spec.command), cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=spec.timeout_seconds, shell=False, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        duration = int((time.monotonic() - started) * 1000)
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        return CheckResult(
            check_id=spec.check_id, status=CheckStatus.UNKNOWN, mandatory=spec.mandatory,
            reason=f"timed out after {spec.timeout_seconds}s", duration_ms=duration,
            command=list(spec.command), stdout_sha256=sha256_bytes(stdout), stderr_sha256=sha256_bytes(stderr),
            stdout_bytes=len(stdout), stderr_bytes=len(stderr),
            stdout=stdout.decode("utf-8", "replace") if include_output else None,
            stderr=stderr.decode("utf-8", "replace") if include_output else None,
        )
    except OSError as exc:
        duration = int((time.monotonic() - started) * 1000)
        return CheckResult(
            check_id=spec.check_id, status=CheckStatus.UNKNOWN, mandatory=spec.mandatory,
            reason=f"could not execute command: {exc}", duration_ms=duration, command=list(spec.command),
        )

    duration = int((time.monotonic() - started) * 1000)
    status = CheckStatus.PASS if proc.returncode == 0 else CheckStatus.FAIL
    return CheckResult(
        check_id=spec.check_id, status=status, mandatory=spec.mandatory,
        reason="command exited 0" if proc.returncode == 0 else f"command exited {proc.returncode}",
        duration_ms=duration, command=list(spec.command), return_code=proc.returncode,
        stdout_sha256=sha256_bytes(proc.stdout), stderr_sha256=sha256_bytes(proc.stderr),
        stdout_bytes=len(proc.stdout), stderr_bytes=len(proc.stderr),
        stdout=proc.stdout.decode("utf-8", "replace") if include_output else None,
        stderr=proc.stderr.decode("utf-8", "replace") if include_output else None,
    )
