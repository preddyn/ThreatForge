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

**Defaults:** Python + pytest  
**Supported:** JavaScript/Jest, Java/JUnit, Go/testing, etc.

---
## 📦 Installation

```bash
git clone https://github.com/preddyn/ThreatForge.git
cd ThreatForge
pip install -r requirements.txt
## 🚀 Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Set your API key
export OPENAI_API_KEY="sk-..."

# 3. Run
python threatforge.py examples/sampleTM.yml M-Auth-001 --output tests/test_auth_security.py

## 📖 Usage

```bash
python threatforge.py <threat_model.yaml> <mitigation_id> [options]

### Options

| Flag         | Description                              | Default       |
|--------------|------------------------------------------|---------------|
| `--language` | Target programming language              | `python`      |
| `--framework`| Testing framework                        | `pytest`      |
| `--model`    | OpenAI model (e.g. `gpt-4o-mini`)        | `gpt-4o`      |
| `--output`   | Save generated tests to file             | (stdout only) |

## 🛠 Example Commands

```bash
# Python + pytest (default)
python threatforge.py examples/sampleTM.yml M-Auth-001 --output tests/test_jwt_security.py

# JavaScript + Jest
python threatforge.py examples/sampleTM.yml M-Auth-001 --language=javascript --framework=jest

# Java + JUnit with cheaper model
python threatforge.py examples/sampleTM.yml M-Auth-001 --language=java --framework=junit --model=gpt-4o-mini