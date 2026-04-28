# secure-app

A minimal Python web service with a GitHub Actions DevSecOps pipeline built to demonstrate advanced artifact readiness.

## What this pipeline does

- Runs SAST with Semgrep
- Performs dependency scanning with pip-audit
- Executes secret scanning with Gitleaks
- Builds the container image only after security scans pass
- Generates a CycloneDX SBOM for the built image
- Runs Trivy container vulnerability scanning against the local image
- Uploads all scan results and SBOM as GitHub Actions artifacts
- Marks the image as a trusted build only after checks are successful

## Produced artifacts

- `semgrep.json` — code-level static analysis results for auditing
- `pip-audit.json` — dependency vulnerability findings
- `gitleaks.json` — repository secret scan output
- `sbom-<COMMIT_SHA>.json` — CycloneDX Software Bill of Materials for the built image
- `vulnerability-summary-<COMMIT_SHA>.json` — container vulnerability report from Trivy
- `image-id-<COMMIT_SHA>.txt` — exact image identifier tied to the commit SHA
- `trusted-build-<COMMIT_SHA>.txt` — trusted build promotion marker published only after all checks pass

## Local run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```
