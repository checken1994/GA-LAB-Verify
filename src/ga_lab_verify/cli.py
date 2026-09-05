from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .config import ConfigError, DEFAULT_CONFIG, load_config
from .git_repo import GitError, snapshot
from .models import Verdict
from .report import attach_evidence_hash, evidence_hash, load_report, write_report
from .verifier import verify


def _exit_code(verdict: Verdict) -> int:
    if verdict is Verdict.SAFE_TO_MERGE:
        return 0
    if verdict is Verdict.BLOCKED:
        return 2
    return 3


def _cmd_init(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if path.exists() and not args.force:
        print(f"refusing to overwrite existing {path}; use --force", file=sys.stderr)
        return 2
    path.write_text(DEFAULT_CONFIG, encoding="utf-8")
    print(f"wrote {path}")
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = repo / config_path
    try:
        config, raw = load_config(config_path)
    except (OSError, ConfigError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 3

    report = verify(repo, config, raw, base_ref=args.base, include_output=args.include_output)
    attach_evidence_hash(report)
    json_path, md_path = write_report(report, Path(args.output_dir))
    print(f"verdict={report.verdict.value}")
    print(f"tested_sha={report.tested_sha or 'UNKNOWN'}")
    print(f"evidence_sha256={report.evidence_sha256}")
    print(f"json_report={json_path}")
    print(f"markdown_report={md_path}")
    return _exit_code(report.verdict)


def _cmd_validate(args: argparse.Namespace) -> int:
    try:
        data = load_report(Path(args.report))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"invalid report: {exc}", file=sys.stderr)
        return 2
    expected_hash = evidence_hash(data)
    if data.get("evidence_sha256") != expected_hash:
        print("invalid report: evidence SHA-256 mismatch", file=sys.stderr)
        return 2
    try:
        current = snapshot(Path(args.repo)).head_sha
    except GitError as exc:
        print(f"cannot validate repository SHA: {exc}", file=sys.stderr)
        return 2
    if data.get("tested_sha") != current:
        print(f"stale report: tested_sha={data.get('tested_sha')} current_head={current}", file=sys.stderr)
        return 2
    print(f"VALID evidence_sha256={expected_hash} tested_sha={current}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ga-lab", description="Evidence-first verification for AI-generated code changes")
    parser.add_argument("--version", action="version", version=f"GA LAB {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="write a starter .ga-lab-verify.toml")
    p_init.add_argument("--path", default=".ga-lab-verify.toml")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=_cmd_init)

    p_verify = sub.add_parser("verify", help="verify a repository checkout")
    p_verify.add_argument("--repo", default=".")
    p_verify.add_argument("--config", default=".ga-lab-verify.toml")
    p_verify.add_argument("--base", help="optional base ref/SHA for changed-file policy checks")
    p_verify.add_argument("--output-dir", default=".ga-lab/reports")
    p_verify.add_argument("--include-output", action="store_true", help="embed raw stdout/stderr in evidence (may expose secrets)")
    p_verify.set_defaults(func=_cmd_verify)

    p_validate = sub.add_parser("validate-report", help="validate report integrity and current-SHA binding")
    p_validate.add_argument("report")
    p_validate.add_argument("--repo", default=".")
    p_validate.set_defaults(func=_cmd_validate)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    raise SystemExit(args.func(args))
