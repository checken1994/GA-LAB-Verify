# Release Procedure

1. Freeze the intended commit on `main`.
2. Run CI on that exact SHA.
3. Run `ga-lab verify --repo .` on a clean checkout of the same SHA.
4. Preserve the JSON report outside the source tree or as a CI artifact.
5. Validate it with `ga-lab validate-report REPORT.json --repo .`.
6. Tag only the SHA whose mandatory gates passed.
7. Never reuse evidence from SHA X to certify SHA Y.
