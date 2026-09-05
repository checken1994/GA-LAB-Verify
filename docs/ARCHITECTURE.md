# GA LAB Architecture

GA LAB v1 is a local/CI verification gate.

```text
Repository / PR checkout
→ Git identity + optional base diff
→ Policy checks
→ Configured verification commands
→ Evidence normalization + hashes
→ Verdict authority
→ JSON evidence report + Markdown projection
```

## Authority rules

1. Any mandatory `FAIL` ⇒ `BLOCKED`.
2. Otherwise any mandatory `UNKNOWN` ⇒ `UNKNOWN`.
3. Otherwise all mandatory checks passed ⇒ `SAFE_TO_MERGE`.

Every report carries `tested_sha`. `ga-lab validate-report` rejects a report if its SHA differs from current HEAD or its evidence hash no longer matches its contents.

Commands are argument arrays with `shell=False`. This prevents shell metacharacter interpretation but does not make an untrusted repository safe.

## Explicit non-goals

GA LAB v1 does not claim OS/container sandbox isolation, autonomous repair, universal proof of program correctness, hosted SaaS operation, or completeness of the broader SCP architecture.
