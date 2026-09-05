from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import VerificationReport
from .util import canonical_json, sha256_text


def evidence_hash(report: VerificationReport | dict[str, Any]) -> str:
    if isinstance(report, VerificationReport):
        data = report.to_dict(include_evidence_hash=False)
    else:
        data = dict(report)
        data.pop("evidence_sha256", None)
    return sha256_text(canonical_json(data))


def attach_evidence_hash(report: VerificationReport) -> None:
    report.evidence_sha256 = evidence_hash(report)


def write_report(report: VerificationReport, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    short = (report.tested_sha or "unknown")[:12]
    stamp = report.created_at.replace(":", "").replace("-", "").replace("+00:00", "Z")
    json_path = output_dir / f"{short}-{stamp}.json"
    md_path = output_dir / f"{short}-{stamp}.md"
    json_path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    return json_path, md_path


def render_markdown(report: VerificationReport) -> str:
    lines = [
        "# GA LAB Verification Report", "", f"- Verdict: **{report.verdict.value}**",
        f"- Tested SHA: `{report.tested_sha or 'UNKNOWN'}`", f"- Base SHA: `{report.base_sha or 'not supplied'}`",
        f"- Evidence SHA-256: `{report.evidence_sha256 or 'UNKNOWN'}`", f"- Created: `{report.created_at}`",
        "", "## Checks", "", "| Check | Mandatory | Status | Reason |", "|---|---:|---|---|",
    ]
    for check in report.checks:
        reason = check.reason.replace("|", "\\|")
        lines.append(f"| `{check.check_id}` | {'yes' if check.mandatory else 'no'} | **{check.status.value}** | {reason} |")
    if report.reasons:
        lines += ["", "## Verdict reasons", ""] + [f"- {r}" for r in report.reasons]
    lines += ["", "> This verdict is scoped to the checks and exact SHA recorded above.\n"]
    return "\n".join(lines)


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
