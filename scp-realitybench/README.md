# SCP RealityBench v0.1

Independent benchmark for testing frontier LLMs on falsification, runtime verification, repair, epistemic calibration, policy compliance, and cross-system reasoning.

## Repository boundary

This public repository contains only the benchmark runner, schemas/contracts, public challenges, scoring/replay specifications, adapters, documentation, and public exports.

It MUST NOT contain:
- hidden challenges
- hidden oracle implementations
- mutation manifests for active hidden instances
- canaries
- provider secrets

The benchmark must not be imported by SCP production core. Benchmark and remediation are separate authorities.

## Canonical implementation authority

See `MASTER_IMPLEMENTATION_CONTRACT.md` (RB-00 through RB-62). No release may be called complete unless RB-61 and RB-62 pass from a clean clone.

## Canonical topology

- `scp-realitybench/` — public code and public suite
- `scp-realitybench-private/` — hidden challenges/oracles/mutations/private CI
- `scp-realitybench-results/` — publishable evidence/result bundles only

## Target suite

- 8 tracks
- 48 canonical templates
- 16 public
- 32 hidden
- official hidden tournament: 5 independent mutated runs/template = 160 runs/model

## Truth authority

Behavioral truth must come from Independent Oracle + observable Reality state. Model self-report, confidence, return code, or "no exception" is never sufficient by itself.
