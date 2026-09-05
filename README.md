# GA LAB

**Evidence-first verification for AI-generated code changes.**

> GA LAB verifies what coding agents actually changed before a human trusts or merges it.

GA LAB is a focused software product built from verification principles developed in **SCP (Self-Correcting Platform)**. SCP remains the broader research and systems-engineering foundation; GA LAB turns its strongest ideas into a narrow workflow for repositories, branches and pull requests.

```text
AI-generated change
        ↓
GA LAB verification
        ↓
actual repository state + tests + policy + evidence
        ↓
SAFE_TO_MERGE | BLOCKED | UNKNOWN
```

GA LAB does **not** trust a model's self-report, a green-looking log line, or a stale artifact as proof. Verification evidence is bound to the exact Git commit SHA being evaluated.

## What GA LAB verifies

- exact Git SHA and clean/dirty repository state;
- configured build, test and security commands;
- changed-file policy and protected-path rules;
- suspicious test weakening patterns such as new `skip`, `xfail`, or placeholder assertions;
- deterministic evidence hashes for configuration, command results and generated reports;
- fail-closed verdicts when a mandatory check cannot be established.

## Verdicts

| Verdict | Meaning |
|---|---|
| `SAFE_TO_MERGE` | Every mandatory verification check passed for the exact tested SHA. |
| `BLOCKED` | At least one mandatory check failed or a protected policy was violated. |
| `UNKNOWN` | GA LAB cannot establish a required fact safely; it refuses to upgrade uncertainty to success. |

## Quick start

Requires Python 3.11+ and Git.

```bash
git clone https://github.com/checken1994/GA-LAB-Verify.git
cd GA-LAB-Verify
python -m pip install -e .
ga-lab init
ga-lab verify --repo .
```

Reports are written under `.ga-lab/reports/` as JSON and Markdown. The JSON report is the machine-readable authority; the Markdown file is a human-readable projection of the same run.

## Design principles inherited from SCP

1. **Reality over model** — claims must be supported by observed state or executable checks.
2. **PASS is not truth** — a successful command proves only its declared scope.
3. **Evidence is SHA-bound** — evidence from commit `X` cannot silently certify commit `Y`.
4. **UNKNOWN fails closed** — uncertainty is preserved instead of being rewritten as success.
5. **Small, reversible authority** — verification observes and reports; it does not silently rewrite protected project policy.
6. **Test integrity matters** — green results created by weakening the harness are not treated as trustworthy success.

See [`docs/SCP_ORIGIN.md`](docs/SCP_ORIGIN.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), and [`SECURITY.md`](SECURITY.md).

## Project status

This repository is the standalone public product repository for GA LAB. Release readiness is determined by repository CI and verification evidence generated for the exact release SHA; documentation never overrides a failing or missing gate.

## Contact

**Minh Nguyen Van**  
Phone: **0974061824**  
Email: **checken1994@gmail.com**  
GitHub: **[@checken1994](https://github.com/checken1994)**

## Copyright

Copyright © 2026 Minh Nguyen Van. All rights reserved. See [`LICENSE.md`](LICENSE.md).
