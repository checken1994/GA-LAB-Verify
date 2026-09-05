from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


DEFAULT_CONFIG = """schema_version = 1

[policy]
require_clean_worktree = true
protected_paths = []
forbid_test_weakening = true

[[checks]]
id = \"tests\"
command = [\"python\", \"-m\", \"unittest\", \"discover\", \"-s\", \"tests\", \"-v\"]
mandatory = true
timeout_seconds = 120
"""


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class PolicyConfig:
    require_clean_worktree: bool = True
    protected_paths: tuple[str, ...] = ()
    forbid_test_weakening: bool = True


@dataclass(frozen=True)
class CommandCheckConfig:
    check_id: str
    command: tuple[str, ...]
    mandatory: bool = True
    timeout_seconds: int = 120


@dataclass(frozen=True)
class VerifyConfig:
    schema_version: int
    policy: PolicyConfig
    checks: tuple[CommandCheckConfig, ...]


def load_config(path: Path) -> tuple[VerifyConfig, bytes]:
    raw = path.read_bytes()
    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise ConfigError(f"invalid TOML: {exc}") from exc

    if data.get("schema_version") != 1:
        raise ConfigError("schema_version must equal 1")

    policy_raw = data.get("policy", {})
    protected = policy_raw.get("protected_paths", [])
    if not isinstance(protected, list) or not all(isinstance(x, str) and x for x in protected):
        raise ConfigError("policy.protected_paths must be a list of non-empty strings")

    policy = PolicyConfig(
        require_clean_worktree=bool(policy_raw.get("require_clean_worktree", True)),
        protected_paths=tuple(protected),
        forbid_test_weakening=bool(policy_raw.get("forbid_test_weakening", True)),
    )

    checks_raw = data.get("checks", [])
    if not isinstance(checks_raw, list) or not checks_raw:
        raise ConfigError("at least one [[checks]] entry is required")

    checks: list[CommandCheckConfig] = []
    seen: set[str] = set()
    for item in checks_raw:
        check_id = item.get("id")
        command = item.get("command")
        if not isinstance(check_id, str) or not check_id.strip():
            raise ConfigError("each check requires a non-empty id")
        if check_id in seen:
            raise ConfigError(f"duplicate check id: {check_id}")
        seen.add(check_id)
        if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
            raise ConfigError(f"check {check_id!r} command must be a non-empty string array")
        timeout = item.get("timeout_seconds", 120)
        if not isinstance(timeout, int) or timeout <= 0 or timeout > 3600:
            raise ConfigError(f"check {check_id!r} timeout_seconds must be 1..3600")
        checks.append(CommandCheckConfig(
            check_id=check_id,
            command=tuple(command),
            mandatory=bool(item.get("mandatory", True)),
            timeout_seconds=timeout,
        ))

    return VerifyConfig(schema_version=1, policy=policy, checks=tuple(checks)), raw
