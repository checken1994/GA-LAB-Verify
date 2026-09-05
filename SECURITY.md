# Security Policy

GA LAB executes verification commands declared in `.ga-lab-verify.toml`. A repository that can modify this configuration can request arbitrary local processes under the permissions of the user running GA LAB.

**Do not run GA LAB against an untrusted repository or untrusted configuration outside an appropriate sandbox.**

GA LAB v1 deliberately does not claim OS-level sandbox isolation. Commands run with `shell=False`; raw stdout/stderr is hashed and omitted from reports by default unless `--include-output` is explicitly used.

Report vulnerabilities privately to **checken1994@gmail.com** with affected version/SHA, reproduction steps and impact.
