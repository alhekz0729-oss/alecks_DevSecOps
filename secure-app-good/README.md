# secure-app

A minimal Flask-based sample application designed to demonstrate an advanced GitHub-based DevSecOps pipeline.

## Repository structure

- `app/main.py` - application entrypoint and HTTP routes
- `requirements.txt` - pinned runtime dependencies
- `Dockerfile` - secure container image build instructions
- `.github/workflows/devsecops-pipeline.yml` - GitHub Actions pipeline
- `.semgrep.yml` - custom SAST rules for the repository
- `README.md` - this document

## DevSecOps pipeline capabilities

The GitHub Actions workflow is built around multiple dependent jobs and enforces security gates before image certification:

1. Dependency scan using `pip-audit`
2. Static application security test (SAST) using `semgrep`
3. Secret scanning using `gitleaks`
4. Docker image build only after all scans succeed
5. Container vulnerability scanning using `Trivy`
6. SBOM generation using `Syft`
7. Artifact upload for auditing and promotion

## Artifacts produced by the pipeline

- `dependency-scan-report` - `pip-audit` output for dependency review
- `sast-report` - `semgrep` results in SARIF and text formats
- `secret-scan-report` - `gitleaks` JSON report for exposed secrets
- `build-artifacts`:
  - `sbom/cyclonedx-sbom.json` - CycloneDX SBOM for the built image
  - `scan-results/trivy-report.json` - container vulnerability scan summary
  - `scan-results/image-identifier.txt` - image metadata tied to commit SHA
  - `scan-results/image-digest.txt` - local image digest for traceability

## Security posture enhancements

- No hardcoded secrets are present in source code
- Runtime dependency versions are pinned
- Dockerfile uses a non-root user and installs dependencies without cache
- Image certification and trust metadata are only produced after all security checks pass

## Running locally

Install dependencies and run the app:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app/main.py
```

Run tests:

```bash
python -m pip install pytest
pytest -q
```
