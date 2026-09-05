# Release Procedure

GA LAB publishes two synchronized distribution surfaces:

1. a GitHub **Release** tagged `v<project.version>` with Python build artifacts and SHA-bound verification evidence;
2. a GitHub Container Registry **Package** at `ghcr.io/checken1994/ga-lab-verify` with version and `latest` tags.

## Authority and ordering

The publish workflow runs only from `main` and uses the version declared in `pyproject.toml`.

Before anything is published it must:

1. check out the exact candidate SHA with full Git history;
2. install GA LAB;
3. compile the production package;
4. run the complete unit-test suite;
5. run `ga-lab verify --repo .` on that exact SHA;
6. build the Python wheel/source distribution;
7. build and push the versioned GHCR image;
8. create the GitHub Release last, attaching the build artifacts and GA LAB evidence.

Publishing the container before creating the Release makes the job safely retryable: if Release creation fails, a rerun may push the same immutable version tag again and then finish the Release. A Release is therefore the final publication boundary.

## Evidence binding

Release notes record the exact Git SHA and evidence SHA-256. Evidence generated for SHA X must never certify SHA Y. The JSON verification report attached to a Release is the machine-readable authority for the GA LAB verification run performed by the publish workflow.

## Versioning

To publish a new version:

1. update `project.version` in `pyproject.toml`;
2. update `CHANGELOG.md`;
3. merge/push the release candidate to `main`;
4. CI and the publish workflow verify the candidate;
5. if `v<version>` does not already exist, the workflow publishes the GHCR package and creates the GitHub Release.

If the tag/Release already exists, the workflow does not silently replace it. Bump the version instead.

## Package tags

For version `1.0.0`, the workflow publishes:

```text
ghcr.io/checken1994/ga-lab-verify:1.0.0
ghcr.io/checken1994/ga-lab-verify:v1.0.0
ghcr.io/checken1994/ga-lab-verify:latest
```

Package visibility/access is controlled by GitHub package settings. The image carries OCI source, revision, version and license labels linking it back to this repository and exact commit.
