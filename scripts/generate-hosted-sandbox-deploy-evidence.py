#!/usr/bin/env python3
"""Generate public-safe post-deploy evidence for the hosted sandbox."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / ".cavra" / "deploy-evidence"


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def workflow_run_url(server_url: str, repository: str, run_id: str) -> str:
    if not run_id or run_id == "local":
        return "local-validation"
    return f"{server_url.rstrip('/')}/{repository}/actions/runs/{run_id}"


def build_packet(args: argparse.Namespace) -> dict[str, Any]:
    repository = args.repository or env("GITHUB_REPOSITORY", "Huzefaaa2/cavra")
    server_url = args.server_url or env("GITHUB_SERVER_URL", "https://github.com")
    run_id = args.run_id or env("GITHUB_RUN_ID", "local")
    run_attempt = args.run_attempt or env("GITHUB_RUN_ATTEMPT", "local")
    page_url = args.page_url or env("CAVRA_SANDBOX_URL", "https://huzefaaa2.github.io/cavra/")
    hosted_smoke_status = args.hosted_smoke_status or env("CAVRA_HOSTED_SMOKE_STATUS", "pass")
    commit_sha = args.commit_sha or env("GITHUB_SHA", "local-validation")
    ref_name = args.ref_name or env("GITHUB_REF_NAME", "local")
    workflow = args.workflow or env("GITHUB_WORKFLOW", "Deploy Sandbox")

    return {
        "schema_version": "cavra.hosted_sandbox.post_deploy_evidence.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "github_pages_post_deploy_evidence",
        "generated_at": args.generated_at or utc_now(),
        "status": "pass" if hosted_smoke_status == "pass" else "failed",
        "page_url": page_url,
        "repository": repository,
        "commit_sha": commit_sha,
        "ref_name": ref_name,
        "workflow": workflow,
        "workflow_run_id": run_id,
        "workflow_run_attempt": run_attempt,
        "workflow_run_url": workflow_run_url(server_url, repository, run_id),
        "hosted_smoke": {
            "status": hosted_smoke_status,
            "command": "npm run validate:sandbox:hosted",
            "validator": "scripts/validate-hosted-sandbox-pages.mjs",
            "record": "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json",
        },
        "verification_sources": [
            "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json",
            "docs/release-verifications/aispm-launch-readiness-rollup.json",
            ".github/workflows/deploy-sandbox.yml",
        ],
        "artifact_name": "cavra-hosted-sandbox-post-deploy-evidence",
        "public_safety_boundary": (
            "This packet records public GitHub Pages deployment metadata and hosted smoke "
            "status only. It must not include customer records, private trial package "
            "tokens, license signing keys, private registry credentials, or Enterprise "
            "source code."
        ),
    }


def write_markdown(packet: dict[str, Any], path: Path) -> None:
    lines = [
        "# Hosted Sandbox Post-Deploy Evidence",
        "",
        f"Generated: {packet['generated_at']}",
        "",
        f"Status: {packet['status']}",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Page URL | `{packet['page_url']}` |",
        f"| Repository | `{packet['repository']}` |",
        f"| Commit SHA | `{packet['commit_sha']}` |",
        f"| Ref | `{packet['ref_name']}` |",
        f"| Workflow | `{packet['workflow']}` |",
        f"| Workflow run | `{packet['workflow_run_url']}` |",
        f"| Hosted smoke | `{packet['hosted_smoke']['status']}` |",
        "",
        "## Verification Sources",
        "",
    ]
    lines.extend(f"- `{source}`" for source in packet["verification_sources"])
    lines.extend(
        [
            "",
            "## Public Safety Boundary",
            "",
            packet["public_safety_boundary"],
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_packet(packet: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    required = [
        "schema_version",
        "generated_at",
        "status",
        "page_url",
        "repository",
        "commit_sha",
        "workflow_run_url",
        "hosted_smoke",
        "public_safety_boundary",
    ]
    for key in required:
        if not packet.get(key):
            failures.append(f"missing required packet field: {key}")
    if packet.get("schema_version") != "cavra.hosted_sandbox.post_deploy_evidence.v1":
        failures.append("invalid schema_version")
    if packet.get("status") not in {"pass", "failed"}:
        failures.append("status must be pass or failed")
    if packet.get("hosted_smoke", {}).get("validator") != "scripts/validate-hosted-sandbox-pages.mjs":
        failures.append("hosted smoke validator mismatch")
    forbidden = [
        "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
        "license_private_key",
        "private_registry_token",
        "customer_identity_payload",
        "raw_prompt_payload",
    ]
    packet_text = json.dumps(packet, sort_keys=True)
    for term in forbidden:
        if term in packet_text:
            failures.append(f"packet must not expose {term}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--page-url", default="")
    parser.add_argument("--hosted-smoke-status", default="")
    parser.add_argument("--commit-sha", default="")
    parser.add_argument("--repository", default="")
    parser.add_argument("--server-url", default="")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--run-attempt", default="")
    parser.add_argument("--workflow", default="")
    parser.add_argument("--ref-name", default="")
    parser.add_argument("--generated-at", default="")
    args = parser.parse_args()

    packet = build_packet(args)
    failures = validate_packet(packet)
    if failures:
        print("Hosted sandbox post-deploy evidence generation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "hosted-sandbox-post-deploy-evidence.json"
    markdown_path = output_dir / "hosted-sandbox-post-deploy-evidence.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(packet, markdown_path)
    print("Hosted sandbox post-deploy evidence generated.")
    print(f"- {json_path}")
    print(f"- {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
