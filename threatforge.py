#!/usr/bin/env python3
"""
ThreatForge - Adversarial Security Test Generator
Version: 1.0 (Jan 2026 compatible with openai-python v2.14+)
"""

import os
import sys
import argparse
import yaml
from typing import Dict, Any, List
from openai import OpenAI

def load_yaml(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Error: YAML file not found: {path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed parsing YAML: {e}")
        sys.exit(1)

def extract_mitigation_and_risks(data: Dict[str, Any], mitigation_id: str) -> Dict[str, Any]:
    mitigations = data.get("mitigations", []) or []
    risks = data.get("risks", []) or []
    mitigation = next((m for m in mitigations if isinstance(m, dict) and m.get("id") == mitigation_id), None)
    if not mitigation:
        return {}
    related_ids = set(mitigation.get("related_risks", []) or [])
    related_risks = [
        {
            "id": r.get("id", "Unknown"),
            "description": r.get("description", "N/A"),
            "mechanism": r.get("mechanism", "N/A"),
            "impact": r.get("impact", "N/A"),
        }
        for r in risks if isinstance(r, dict) and r.get("id") in related_ids
    ]
    return {
        "mitigation": {
            "id": mitigation.get("id", mitigation_id),
            "description": mitigation.get("description", "No description provided."),
        },
        "related_risks": related_risks,
    }

def format_risks(risks: List[Dict[str, Any]]) -> str:
    if not risks:
        return "None"
    return "\n".join([
        f"- Risk ID: {r['id']}\n  Desc: {r['description']}\n  Mechanism: {r['mechanism']}"
        for r in risks
    ])

def build_prompt(mitigation_desc: str, risks_block: str, language: str, framework: str) -> str:
    return f"""
You are an expert security engineer specializing in adversarial testing.
Generate adversarial unit tests to stress-test the following mitigation.

Mitigation: {mitigation_desc}

Associated Risks:
{risks_block}

Requirements:
- Language: {language}
- Framework: {framework}
- Focus on edge cases, bypass attempts, negative tests
- Self-contained with mocks/stubs/fixtures
- Output ONLY the clean {language} code block (no explanations, no markdown fences)
""".strip()

def generate_tests(args) -> int:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return 2

    client = OpenAI(api_key=api_key)
    data = load_yaml(args.yaml_file)
    info = extract_mitigation_and_risks(data, args.mitigation_id)

    if not info.get("mitigation"):
        print(f"Error: Mitigation ID '{args.mitigation_id}' not found in {args.yaml_file}")
        return 1

    prompt = build_prompt(
        info["mitigation"]["description"],
        format_risks(info["related_risks"]),
        args.language,
        args.framework
    )

    try:
        resp = client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": "You are ThreatForge, a security test generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        raw_output = resp.choices[0].message.content.strip()

        # Clean up common LLM artifacts
        if raw_output.startswith("```") and raw_output.endswith("```"):
            raw_output = raw_output.split("\n", 1)[1].rsplit("\n", 1)[0].strip()

        print(raw_output)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(raw_output)
            print(f"\nTests saved to: {args.output}")

        return 0

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return 3

def main():
    parser = argparse.ArgumentParser(
        description="ThreatForge - Generate adversarial security unit tests from threat models",
        epilog="Example: python threatforge.py sampleTM.yml M-Auth-001 --language=javascript --framework=jest"
    )
    parser.add_argument("yaml_file", help="Path to the YAML threat model file")
    parser.add_argument("mitigation_id", help="ID of the mitigation to test (e.g. M-Auth-001)")
    parser.add_argument("--language", default="python", help="Target language (default: python)")
    parser.add_argument("--framework", default="pytest", help="Testing framework (default: pytest)")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    parser.add_argument("--output", help="Save generated tests to this file (optional)")

    args = parser.parse_args()
    sys.exit(generate_tests(args))

if __name__ == "__main__":
    main()