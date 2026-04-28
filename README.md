# DevSecOps Demonstration Repository

This repository contains two parallel implementations of a simple Python Flask application to demonstrate **secure DevSecOps practices** versus **common security pitfalls**.

## 📁 Repository Structure

```
alecks_DevSecOps/
├── good-app/                      # ✅ Secure implementation
│   ├── app/
│   │   └── main.py               # Clean, secure Flask API
│   ├── tests/
│   │   └── test_main.py          # All tests pass
│   ├── Dockerfile                # Secure, minimal base image
│   └── requirements.txt           # Secure dependency versions
│
├── bad-app/                       # ❌ Intentionally vulnerable implementation
│   ├── app/
│   │   └── main.py               # Contains validation bug
│   ├── tests/
│   │   └── test_main.py          # Test fails due to bug
│   ├── Dockerfile                # Outdated base image with CVEs
│   └── requirements.txt           # Includes vulnerable versions
│
└── .github/
    └── workflows/
        ├── good-app-pipeline.yml  # ✅ Demonstrates PASSING pipeline
        └── bad-app-pipeline.yml   # ❌ Demonstrates FAILING pipeline
```

## 🔍 Key Differences

### Application Code

#### Good App (`good-app/app/main.py`)
```python
@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        raise BadRequest("JSON body must contain 'message'")
    message = data["message"].strip()
    return jsonify(message=message), 200
```
✅ **Proper input validation and error handling**

#### Bad App (`bad-app/app/main.py`)
```python
def is_strong_password(password: str) -> bool:
    # BUG: Accepts any password with a digit, even if < 8 chars
    return len(password) >= 8 or any(char.isdigit() for char in password)
```
❌ **Flawed validation logic: "1" would be accepted as a strong password**

---

### Dependencies

| Aspect | Good App | Bad App | Issue |
|--------|----------|---------|-------|
| **Flask** | 2.3.4 | 2.2.0 | Flask 2.2.0 has known CVEs |
| **pytest** | 7.4.3 | 6.2.5 | pytest 6.2.5 is outdated |
| **Python** | 3.12 | 3.8 | Python 3.8 is EOL (end-of-life) |

---

### Docker Images

| Aspect | Good App | Bad App | Issue |
|--------|----------|---------|-------|
| **Base Image** | `python:3.12-slim` | `python:3.8-buster` | Buster is outdated, includes OS vulns |
| **Security** | Non-root user | Runs as root | ❌ Privilege escalation risk |
| **Size** | Minimal (~150MB) | Larger (~900MB+) | Larger attack surface |

---

### Pipeline Stages

#### Good App Pipeline ✅

```
dependency-scan → unit-tests → build-image → container-scan → deploy ✅
  (No vulns)       (All pass)     (Clean)      (No issues)     (Ready)
```

**What passes:**
- ✅ No vulnerable dependencies detected
- ✅ All unit tests pass
- ✅ Container image builds successfully
- ✅ Minimal security findings (only expected base image info)
- ✅ Deployment stage completes

#### Bad App Pipeline ❌

```
dependency-scan → unit-tests → build-image → container-scan → report ❌
  (Vulns found)   (Test fails)    (Succeeds)   (Many issues)   (Fails)
```

**What fails:**
- ❌ CVEs detected in Flask 2.2.0 and pytest 6.2.5
- ❌ Unit test fails: `test_register_rejects_weak_password`
  - Password "12345" incorrectly accepted (has digit but < 8 chars)
- ⚠️ Container scan finds HIGH/CRITICAL vulnerabilities
  - Outdated Python 3.8-buster base image
  - OS-level CVEs in Debian buster
- ❌ Pipeline halts at security validation

---

## 🚀 Running Locally

### Good App
```bash
cd good-app

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run application
python app/main.py

# Build container
docker build -t good-app:latest .
docker run -p 5000:5000 good-app:latest
```

### Bad App
```bash
cd bad-app

# Install dependencies (will show CVE warnings)
pip install -r requirements.txt

# Run tests (will fail)
pytest -v
# FAILED test_register_rejects_weak_password: AssertionError

# Run application (despite bug)
python app/main.py

# Build container (will build but scan will show vulns)
docker build -t bad-app:latest .
```

---

## 📊 Vulnerability Examples

### CVEs in Bad App Dependencies

**Flask 2.2.0** has known vulnerabilities:
- Request data validation bypass
- Potential for denial of service attacks

**pytest 6.2.5** is severely outdated with multiple security issues.

**Python 3.8-buster** includes:
- OpenSSL vulnerabilities (CVE-2023-XXXXX)
- glibc issues
- systemd vulnerabilities

Run Trivy locally to see:
```bash
trivy image python:3.8-buster  # Shows 100+ vulnerabilities
trivy image python:3.12-slim   # Shows minimal vulns
```

---

## 🔐 DevSecOps Lessons

### Good Practices Demonstrated in `good-app/`

1. **Dependency Management**
   - ✅ Use latest secure versions
   - ✅ Pin exact versions in requirements.txt
   - ✅ Regular audits with `pip-audit`

2. **Code Quality**
   - ✅ Proper input validation
   - ✅ Explicit error handling
   - ✅ 100% test coverage

3. **Container Security**
   - ✅ Use minimal base images (`-slim`, `-alpine`)
   - ✅ Modern Python LTS versions
   - ✅ Run as non-root user
   - ✅ Explicit EXPOSE and CMD

4. **Pipeline Security**
   - ✅ Dependency scanning (pip-audit)
   - ✅ Unit test validation
   - ✅ Container image scanning (Trivy)
   - ✅ Gating deployment on security checks

### Anti-Patterns in `bad-app/`

1. ❌ Outdated dependencies with known CVEs
2. ❌ Flawed business logic (validation bug)
3. ❌ Outdated base images (EOL Python, old Debian)
4. ❌ Running as root in container
5. ❌ No security scanning in development
6. ❌ Allowing failed security checks

---

## 🔗 GitHub Actions Workflows

### Good App Pipeline (`good-app-pipeline.yml`)

**Triggers:** Push to `main` or PR with changes to `good-app/**`

**Stages:**
1. **Dependency Scan** - Audit Python packages for CVEs
2. **Unit Tests** - Run pytest suite (must all pass)
3. **Build Image** - Docker build and tag
4. **Container Scan** - Trivy scan for vulnerabilities
5. **Deploy** - Only runs if all previous stages pass

### Bad App Pipeline (`bad-app-pipeline.yml`)

**Triggers:** Push to `main` or PR with changes to `bad-app/**`

**Stages:**
1. **Dependency Scan** - Continues despite vulnerabilities
2. **Unit Tests** - Fails due to validation bug
3. **Build Image** - Builds despite failures
4. **Container Scan** - Shows hundreds of vulnerabilities
5. **Report Status** - Documents all failures

---

## 📈 Training Use Cases

### For Security Teams
- Audit your pipelines for these patterns
- Implement policy-as-code to block bad-app patterns
- Train teams on secure defaults

### For Developers
- Compare secure vs insecure code side-by-side
- Understand impact of dependency vulnerabilities
- Learn proper validation patterns

### For DevOps/Platform Teams
- Implement Trivy scanning in your CI/CD
- Enforce non-root container users
- Mandate current Python/base image versions
- Block deployment if security gates fail

### For Compliance/Governance
- Document security controls in place
- Show audit trail of vulnerability scanning
- Demonstrate gated deployment pipeline

---

## 🛠️ Local Testing

### Run Container Scans Locally

```bash
# Install Trivy
brew install aquasecurity/trivy/trivy

# Scan good app
cd good-app
docker build -t good-app:latest .
trivy image good-app:latest

# Scan bad app
cd ../bad-app
docker build -t bad-app:latest .
trivy image bad-app:latest  # Shows HIGH/CRITICAL vulns
```

### Run Dependency Audits

```bash
pip install pip-audit

# Good app
cd good-app
pip-audit  # ✅ No vulnerabilities found

# Bad app
cd ../bad-app
pip-audit  # ❌ Shows CVEs in Flask and pytest
```

### Run Unit Tests

```bash
# Good app
cd good-app
pip install -r requirements.txt
pytest -v  # ✅ All pass

# Bad app
cd ../bad-app
pip install -r requirements.txt
pytest -v  # ❌ test_register_rejects_weak_password FAILED
```

---

## 📝 API Endpoints

### Good App: `/echo` endpoint
```bash
# Request
curl -X POST http://localhost:5000/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}'

# Response
{"message":"Hello World"}
```

### Bad App: `/register` endpoint
```bash
# Request (weak password)
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "1"}'

# Response (INCORRECTLY ACCEPTED due to bug)
{"username":"alice","status":"registered"}
```

---

## 📚 References

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE: Improper Input Validation (CWE-20)](https://cwe.mitre.org/data/definitions/20.html)
- [Aqua Security Trivy](https://github.com/aquasecurity/trivy)
- [pip-audit Documentation](https://github.com/pypa/pip-audit)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_considerations.html)
- [NIST: Secure Software Development Framework](https://csrc.nist.gov/publications/detail/sp/800-218/final)

---

## 📜 License

MIT License - Feel free to use this for training and demonstration purposes.

---

## 🤝 Contributing

This repository is designed for educational purposes. Improvements and additional scenarios welcome!

**Suggested additions:**
- OWASP dependency check integration
- SonarQube for code quality scanning
- SAST (Static Application Security Testing) scanning
- Additional bad patterns (SQL injection, hardcoded secrets, etc.)

