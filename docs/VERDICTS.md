# Verdict Semantics

- `SAFE_TO_MERGE`: every mandatory declared check passed for the exact tested SHA. Scoped evidence, not proof of zero defects.
- `BLOCKED`: a mandatory check failed or policy violation was observed.
- `UNKNOWN`: a mandatory fact could not be established safely.

`UNKNOWN` and `BLOCKED` both prevent automated merge, but they preserve different epistemic meanings.
