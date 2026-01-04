# ThreatForge 🔒⚔️

**Automated Adversarial Security Test Generator** powered by OpenAI's LLM.

Generate high-quality, self-contained adversarial unit tests directly from structured threat models — perfect for security engineers, red teams, and secure development lifecycle (SDLC) integration.

Given a YAML threat model with risks and mitigations, ThreatForge extracts a specific mitigation and uses `gpt-4o` (or your chosen model) to generate targeted security tests: edge cases, bypass attempts, abuse cases, and negative tests.

---

## ✨ Features

- Parses structured YAML threat models
- Generates **adversarial** (not just happy-path) tests
- Supports multiple languages & frameworks
- Self-contained tests with mocks/stubs
- Clean CLI with file output option
- Secure: no hardcoded keys

Defaults: **Python + pytest**  
Supported: JavaScript/Jest, Java/JUnit, Go/testing, etc.

---

## 🚀 Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Set your API key
export OPENAI_API_KEY="sk-..."

# 3. Run
python threatforge.py examples/sampleTM.yml M-Auth-001 --output tests/test_auth_security.py
Generated tests are printed and saved to file.

📦 Installation
Bashgit clone https://github.com/yourusername/ThreatForge.git
cd ThreatForge
pip install -r requirements.txt

📖 Usage
Bashpython threatforge.py <threat_model.yaml> <mitigation_id> [options]
Options






























FlagDescriptionDefault--languageTarget programming languagepython--frameworkTesting frameworkpytest--modelOpenAI model (e.g. gpt-4o-mini)gpt-4o--outputSave generated tests to file(stdout only)
Example Threat Model (examples/sampleTM.yml)
YAMLmitigations:
  - id: M-Auth-001
    description: "JWT tokens must use RS256 algorithm and be validated against a strict allowlist."
    related_risks: ["R-Auth-001", "R-Auth-002"]

  - id: M-Input-001
    description: "All user inputs must be validated against a strict schema and sanitized."
    related_risks: ["R-Injection-001"]

risks:
  - id: R-Auth-001
    description: "Algorithm confusion attack (none/HS256 bypass)"
    mechanism: "Attacker switches alg header to unsupported value"
    impact: "Unauthorized access"

  - id: R-Auth-002
    description: "Token forgery with weak keys"
    mechanism: "Craft token with invalid signature"
    impact: "Privilege escalation"
Example Commands
Bash# Python + pytest (default)
python threatforge.py examples/sampleTM.yml M-Auth-001 --output tests/test_jwt_security.py

# JavaScript + Jest
python threatforge.py examples/sampleTM.yml M-Auth-001 --language=javascript --framework=jest

# Java + JUnit with cheaper model
python threatforge.py examples/sampleTM.yml M-Auth-001 --language=java --framework=junit --model=gpt-4o-mini