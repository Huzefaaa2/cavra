#!/usr/bin/env python3
"""Validate hosted sandbox post-deploy evidence wiring."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(read(path))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_file(path: str, failures: list[str]) -> None:
    require((ROOT / path).is_file(), f"missing required file: {path}", failures)


def require_text(path: str, needle: str, label: str, failures: list[str]) -> None:
    require(needle in read(path), f"{label} missing {needle}", failures)


def main() -> int:
    failures: list[str] = []
    required_files = [
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json",
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.md",
        "scripts/generate-hosted-sandbox-deploy-evidence.py",
        "scripts/validate-hosted-sandbox-deploy-evidence.py",
        "scripts/validate-hosted-sandbox-pages.mjs",
        ".github/workflows/deploy-sandbox.yml",
        "README.md",
        "docs/hosted-sandbox-deployment.md",
        "docs/wiki/Hosted-Sandbox-Deployment.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
    ]
    for path in required_files:
        require_file(path, failures)
    if failures:
        for failure in failures:
            print(failure)
        return 1

    contract = load_json("docs/release-verifications/hosted-sandbox-post-deploy-evidence.json")
    require(
        contract.get("schema_version") == "cavra.hosted_sandbox.post_deploy_evidence_contract.v1",
        f"{CONTRACT_PATH}: invalid schema_version",
        failures,
    )
    require(contract.get("generator") == "scripts/generate-hosted-sandbox-deploy-evidence.py", f"{CONTRACT_PATH}: generator mismatch", failures)
    require(contract.get("validator") == "scripts/validate-hosted-sandbox-deploy-evidence.py", f"{CONTRACT_PATH}: validator mismatch", failures)
    require(contract.get("workflow") == ".github/workflows/deploy-sandbox.yml", f"{CONTRACT_PATH}: workflow mismatch", failures)
    require(contract.get("artifact_name") == "cavra-hosted-sandbox-post-deploy-evidence", f"{CONTRACT_PATH}: artifact name mismatch", failures)

    workflow = read(".github/workflows/deploy-sandbox.yml")
    for needle in [
        "npm run validate:sandbox:hosted",
        "python scripts/generate-hosted-sandbox-deploy-evidence.py",
        "actions/upload-artifact@v4",
        "cavra-hosted-sandbox-post-deploy-evidence",
        ".cavra/deploy-evidence/*",
        "CAVRA_HOSTED_SMOKE_STATUS: pass",
    ]:
        require(needle in workflow, f"deploy workflow missing {needle}", failures)

    generator = read("scripts/generate-hosted-sandbox-deploy-evidence.py")
    for needle in [
        "cavra.hosted_sandbox.post_deploy_evidence.v1",
        "GITHUB_RUN_ID",
        "GITHUB_SHA",
        "CAVRA_SANDBOX_URL",
        "workflow_run_url",
        "scripts/validate-hosted-sandbox-pages.mjs",
    ]:
        require(needle in generator, f"post-deploy evidence generator missing {needle}", failures)

    doc_needles = [
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.md",
        "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json",
        "scripts/generate-hosted-sandbox-deploy-evidence.py",
        "scripts/validate-hosted-sandbox-deploy-evidence.py",
        "cavra-hosted-sandbox-post-deploy-evidence",
    ]
    for doc_path in [
        "README.md",
        "docs/hosted-sandbox-deployment.md",
        "docs/wiki/Hosted-Sandbox-Deployment.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
    ]:
        for needle in doc_needles:
            require_text(doc_path, needle, doc_path, failures)

    forbidden = [
        "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
        "license_private_key",
        "private_registry_token",
        "customer_identity_payload",
        "raw_prompt_payload",
    ]
    combined = "\n".join(
        [
            read("docs/release-verifications/hosted-sandbox-post-deploy-evidence.json"),
            read("docs/release-verifications/hosted-sandbox-post-deploy-evidence.md"),
        ]
    )
    for term in forbidden:
        require(term not in combined, f"post-deploy evidence contract must not expose {term}", failures)

    if failures:
        print("Hosted sandbox post-deploy evidence validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Hosted sandbox post-deploy evidence validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
