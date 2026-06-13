#!/usr/bin/env python3
"""Validate AISPM Enterprise Trial lab notebook wiki publication readiness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = Path(
    "examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json"
)
DEFAULT_SCHEMA = Path(
    "src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json"
)
DEFAULT_SUMMARY_JSON = Path(
    "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json"
)
DEFAULT_SUMMARY_MARKDOWN = Path(
    "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md"
)
DEFAULT_ENTERPRISE_READINESS_JSON = Path(
    "docs/release-verifications/aispm-enterprise-trial-readiness-public-summary.json"
)
WIKI_HOME = Path("docs/wiki/Home.md")

REQUIRED_PUBLIC_SAFE_SECTIONS = (
    "## Public Safety Rules",
    "## Related Pages",
)
FORBIDDEN_PUBLIC_NOTEBOOK_MARKERS = (
    "CAVRA_TRIAL_LICENSE_PRIVATE_KEY",
    "CAVRA_TRIAL_OPERATOR_SESSION_SECRET",
    "CAVRA_TRIAL_PORTAL_OPERATOR_TOKEN",
    "CAVRA_TRIAL_LICENSE_PRIVATE_KEY_PEM_B64",
    "CAVRA_TRIAL_LICENSE_PUBLIC_KEY_PEM_B64",
    "LICENSE_SIGNING_KEY",
    "STRIPE_SECRET",
    "CUSTOMER_SECRET",
    "PRIVATE_POLICY_PACK",
    "INTERNAL_ONLY",
)
REQUIRED_ENTERPRISE_READINESS_GATES = (
    "runtime-binding",
    "alert-transport",
    "release-dashboard-publication",
    "trial-lab-notebook",
    "operator-audit-archive",
    "trial-package-readiness-validator",
)


def _read_text(root: Path, relative: Path) -> str:
    return (root / relative).read_text(encoding="utf-8")


def _read_json(root: Path, relative: Path) -> dict[str, Any]:
    return json.loads(_read_text(root, relative))


def _validate_packet(root: Path, packet_path: Path, schema_path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    failures: list[str] = []
    packet_file = root / packet_path
    schema_file = root / schema_path

    if not packet_file.is_file():
        return None, [f"missing readiness packet: {packet_path}"]
    if not schema_file.is_file():
        return None, [f"missing readiness schema: {schema_path}"]

    packet = _read_json(root, packet_path)
    schema = _read_json(root, schema_path)
    try:
        jsonschema.validate(packet, schema=schema)
    except jsonschema.ValidationError as exc:
        failures.append(f"readiness packet schema validation failed: {exc.message}")
    return packet, failures


def build_summary(
    root: Path,
    packet_path: Path = DEFAULT_PACKET,
    schema_path: Path = DEFAULT_SCHEMA,
) -> dict[str, Any]:
    """Return a deterministic publication readiness summary."""

    root = root.resolve()
    blockers: list[str] = []
    packet, packet_failures = _validate_packet(root, packet_path, schema_path)
    blockers.extend(packet_failures)
    summary: dict[str, Any] = {
        "schema_version": "cavra.aispm.trial_lab_notebook_publication_summary.v1",
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "generated_at": None,
        "source_packet": str(packet_path),
        "source_schema": str(schema_path),
        "wiki_home": str(WIKI_HOME),
        "overall_status": "blocked",
        "counts": {
            "wiki_pages": 0,
            "pages_ready": 0,
            "visual_assets": 0,
            "visual_assets_ready": 0,
            "acceptance_criteria": 0,
            "acceptance_criteria_ready": 0,
            "blockers": 0,
        },
        "pages": [],
        "visual_assets": [],
        "navigation_checks": [],
        "acceptance_criteria": [],
        "enterprise_readiness_sync": {
            "source_ref": str(DEFAULT_ENTERPRISE_READINESS_JSON),
            "status": "blocked",
            "ready_gates": 0,
            "required_gates": list(REQUIRED_ENTERPRISE_READINESS_GATES),
            "gates": [],
            "blockers": [],
        },
        "public_safety": {
            "required_sections": list(REQUIRED_PUBLIC_SAFE_SECTIONS),
            "forbidden_markers_checked": list(FORBIDDEN_PUBLIC_NOTEBOOK_MARKERS),
        },
        "blockers": [],
    }
    if packet is None:
        summary["blockers"] = blockers
        summary["counts"]["blockers"] = len(blockers)
        return summary

    summary["generated_at"] = packet.get("generated_at")

    wiki_home_path = root / WIKI_HOME
    if not wiki_home_path.is_file():
        blockers.append(f"missing wiki home: {WIKI_HOME}")
        summary["blockers"] = blockers
        summary["counts"]["blockers"] = len(blockers)
        return summary
    wiki_home = _read_text(root, WIKI_HOME)

    page_ids = {page["page_id"] for page in packet.get("wiki_pages", [])}
    required_nav_ids: set[str] = set()
    for nav_check in packet.get("navigation_checks", []):
        required_nav_ids.update(nav_check.get("required_page_ids", []))
        required_pages = nav_check.get("required_page_ids", [])
        summary["navigation_checks"].append(
            {
                "nav_id": nav_check.get("nav_id"),
                "location": nav_check.get("location"),
                "required_page_ids": required_pages,
                "status": "ready"
                if all(page_id in page_ids for page_id in required_pages)
                else "blocked",
            }
        )
    missing_nav_ids = required_nav_ids - page_ids
    if missing_nav_ids:
        blockers.append(
            "navigation checks reference unknown page ids: "
            + ", ".join(sorted(missing_nav_ids))
        )

    for page in packet.get("wiki_pages", []):
        page_id = page["page_id"]
        source_ref = Path(page["source_ref"])
        page_path = root / source_ref
        page_blockers: list[str] = []
        page_summary: dict[str, Any] = {
            "page_id": page_id,
            "title": page["title"],
            "source_ref": str(source_ref),
            "exists": page_path.is_file(),
            "listed_in_home": False,
            "title_present": False,
            "public_safety_sections_present": [],
            "checkpoint_refs": page.get("checkpoint_refs", []),
            "status": "blocked",
            "blockers": page_blockers,
        }
        if not page_path.is_file():
            page_blockers.append(f"missing wiki source file: {source_ref}")
            blockers.append(f"{page_id}: missing wiki source file: {source_ref}")
            summary["pages"].append(page_summary)
            continue

        page_text = _read_text(root, source_ref)
        page_summary["listed_in_home"] = source_ref.name in wiki_home
        page_summary["title_present"] = page["title"] in page_text
        page_summary["public_safety_sections_present"] = [
            section for section in REQUIRED_PUBLIC_SAFE_SECTIONS if section in page_text
        ]
        if not page_summary["listed_in_home"]:
            page_blockers.append(f"{source_ref.name} is not linked from {WIKI_HOME}")
            blockers.append(f"{page_id}: {source_ref.name} is not linked from {WIKI_HOME}")
        if not page.get("nav_entry_required"):
            page_blockers.append("nav_entry_required must be true")
            blockers.append(f"{page_id}: nav_entry_required must be true")
        if not page.get("link_health_required"):
            page_blockers.append("link_health_required must be true")
            blockers.append(f"{page_id}: link_health_required must be true")
        if not page_summary["title_present"]:
            page_blockers.append("page title does not match readiness packet title")
            blockers.append(f"{page_id}: page title does not match readiness packet title")

        for section in REQUIRED_PUBLIC_SAFE_SECTIONS:
            if section not in page_text:
                page_blockers.append(f"missing required section {section}")
                blockers.append(f"{page_id}: missing required section {section}")

        for marker in FORBIDDEN_PUBLIC_NOTEBOOK_MARKERS:
            if marker in page_text:
                page_blockers.append(f"forbidden public notebook marker found: {marker}")
                blockers.append(f"{page_id}: forbidden public notebook marker found: {marker}")

        for checkpoint_ref in page.get("checkpoint_refs", []):
            if checkpoint_ref not in page_text and "Checkpoint" not in page_text:
                page_blockers.append(f"missing checkpoint coverage for {checkpoint_ref}")
                blockers.append(f"{page_id}: missing checkpoint coverage for {checkpoint_ref}")

        if not page_blockers:
            page_summary["status"] = "ready"
        summary["pages"].append(page_summary)

    for asset in packet.get("visual_assets", []):
        asset_blockers: list[str] = []
        if asset.get("redaction_status") != "public_safe":
            asset_blockers.append("visual asset is not marked public_safe")
            blockers.append(f"{asset['asset_id']}: visual asset is not marked public_safe")
        if not asset.get("alt_text_required"):
            asset_blockers.append("alt text must be required")
            blockers.append(f"{asset['asset_id']}: alt text must be required")
        if not asset.get("required"):
            asset_blockers.append("asset must be required")
            blockers.append(f"{asset['asset_id']}: asset must be required")
        summary["visual_assets"].append(
            {
                "asset_id": asset["asset_id"],
                "asset_type": asset["asset_type"],
                "source_route": asset["source_route"],
                "redaction_status": asset["redaction_status"],
                "alt_text_required": asset["alt_text_required"],
                "required": asset["required"],
                "status": "ready" if not asset_blockers else "blocked",
                "blockers": asset_blockers,
            }
        )

    for criterion in packet.get("acceptance_criteria", []):
        criterion_blockers: list[str] = []
        if not criterion.get("required"):
            criterion_blockers.append("acceptance criterion must be required")
            blockers.append(f"{criterion['criterion_id']}: acceptance criterion must be required")
        summary["acceptance_criteria"].append(
            {
                "criterion_id": criterion["criterion_id"],
                "description": criterion["description"],
                "required": criterion["required"],
                "status": "ready" if not criterion_blockers else "blocked",
                "blockers": criterion_blockers,
            }
        )

    enterprise_sync = _enterprise_readiness_sync(root)
    summary["enterprise_readiness_sync"] = enterprise_sync
    blockers.extend(enterprise_sync["blockers"])

    summary["blockers"] = blockers
    summary["counts"] = {
        "wiki_pages": len(summary["pages"]),
        "pages_ready": sum(1 for page in summary["pages"] if page["status"] == "ready"),
        "visual_assets": len(summary["visual_assets"]),
        "visual_assets_ready": sum(
            1 for asset in summary["visual_assets"] if asset["status"] == "ready"
        ),
        "acceptance_criteria": len(summary["acceptance_criteria"]),
        "acceptance_criteria_ready": sum(
            1
            for criterion in summary["acceptance_criteria"]
            if criterion["status"] == "ready"
        ),
        "enterprise_readiness_gates": len(summary["enterprise_readiness_sync"]["gates"]),
        "enterprise_readiness_gates_ready": summary["enterprise_readiness_sync"]["ready_gates"],
        "blockers": len(blockers),
    }
    summary["overall_status"] = "ready" if not blockers else "blocked"
    return summary


def _enterprise_readiness_sync(root: Path) -> dict[str, Any]:
    blockers: list[str] = []
    path = root / DEFAULT_ENTERPRISE_READINESS_JSON
    sync: dict[str, Any] = {
        "source_ref": str(DEFAULT_ENTERPRISE_READINESS_JSON),
        "status": "blocked",
        "generated_at": None,
        "ready_gates": 0,
        "required_gates": list(REQUIRED_ENTERPRISE_READINESS_GATES),
        "gates": [],
        "blockers": blockers,
    }
    if not path.is_file():
        blockers.append(f"missing Enterprise readiness public summary: {DEFAULT_ENTERPRISE_READINESS_JSON}")
        return sync
    payload = json.loads(path.read_text(encoding="utf-8"))
    sync["generated_at"] = payload.get("generated_at")
    if payload.get("mode") != "public_safe_summary":
        blockers.append("Enterprise readiness summary mode must be public_safe_summary")
    if payload.get("edition") != "enterprise_trial":
        blockers.append("Enterprise readiness summary edition must be enterprise_trial")
    boundary = str(payload.get("public_safety_boundary") or "")
    if not boundary:
        blockers.append("Enterprise readiness summary must include public_safety_boundary")
    for marker in FORBIDDEN_PUBLIC_NOTEBOOK_MARKERS:
        if marker in json.dumps(payload):
            blockers.append(f"forbidden public notebook marker found in Enterprise readiness summary: {marker}")

    gates = payload.get("readiness_gates")
    if not isinstance(gates, list):
        blockers.append("Enterprise readiness summary readiness_gates must be a list")
        gates = []
    gate_ids = {str(gate.get("gate_id")) for gate in gates if isinstance(gate, dict)}
    for gate_id in REQUIRED_ENTERPRISE_READINESS_GATES:
        if gate_id not in gate_ids:
            blockers.append(f"Enterprise readiness gate missing from public summary: {gate_id}")
    for gate in gates:
        if not isinstance(gate, dict):
            blockers.append("Enterprise readiness gate entry must be an object")
            continue
        gate_blockers: list[str] = []
        if gate.get("status") != "ready":
            gate_blockers.append("status must be ready")
        if gate.get("public_safe") is not True:
            gate_blockers.append("public_safe must be true")
        if not gate.get("public_summary"):
            gate_blockers.append("public_summary is required")
        sync["gates"].append(
            {
                "gate_id": gate.get("gate_id"),
                "label": gate.get("label"),
                "status": "ready" if not gate_blockers else "blocked",
                "blockers": gate_blockers,
            }
        )
        blockers.extend(f"{gate.get('gate_id')}: {blocker}" for blocker in gate_blockers)
    sync["ready_gates"] = sum(1 for gate in sync["gates"] if gate["status"] == "ready")
    sync["status"] = "ready" if not blockers else "blocked"
    return sync


def validate(root: Path, packet_path: Path = DEFAULT_PACKET, schema_path: Path = DEFAULT_SCHEMA) -> list[str]:
    """Return validation failures for AISPM trial lab notebook publication readiness."""

    return list(build_summary(root, packet_path, schema_path)["blockers"])


def render_markdown(summary: dict[str, Any]) -> str:
    """Render a reviewer-facing Markdown readiness summary."""

    lines = [
        "# AISPM Trial Lab Notebook Publication Readiness Summary",
        "",
        f"Status: `{summary['overall_status']}`",
        f"Generated At: `{summary['generated_at']}`",
        f"Source Packet: `{summary['source_packet']}`",
        f"Source Schema: `{summary['source_schema']}`",
        "",
        "## Rollup",
        "",
        "| Area | Ready | Total |",
        "| --- | ---: | ---: |",
        f"| Wiki pages | {summary['counts']['pages_ready']} | {summary['counts']['wiki_pages']} |",
        f"| Visual assets | {summary['counts']['visual_assets_ready']} | {summary['counts']['visual_assets']} |",
        (
            f"| Acceptance criteria | {summary['counts']['acceptance_criteria_ready']} | "
            f"{summary['counts']['acceptance_criteria']} |"
        ),
        (
            f"| Enterprise readiness gates | {summary['counts']['enterprise_readiness_gates_ready']} | "
            f"{summary['counts']['enterprise_readiness_gates']} |"
        ),
        f"| Blockers | 0 | {summary['counts']['blockers']} |",
        "",
        "## Wiki Pages",
        "",
        "| Page | Source | Home Nav | Public Safety | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for page in summary["pages"]:
        public_safety = ", ".join(page["public_safety_sections_present"]) or "missing"
        lines.append(
            f"| {page['title']} | `{page['source_ref']}` | "
            f"{'yes' if page['listed_in_home'] else 'no'} | {public_safety} | "
            f"`{page['status']}` |"
        )

    lines.extend(
        [
            "",
            "## Visual Assets",
            "",
            "| Asset | Type | Redaction | Alt Text | Status |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for asset in summary["visual_assets"]:
        lines.append(
            f"| {asset['asset_id']} | {asset['asset_type']} | "
            f"{asset['redaction_status']} | {'yes' if asset['alt_text_required'] else 'no'} | "
            f"`{asset['status']}` |"
        )

    lines.extend(
        [
            "",
            "## Enterprise Trial Readiness Sync",
            "",
            f"Source: `{summary['enterprise_readiness_sync']['source_ref']}`",
            "",
            "| Gate | Label | Status |",
            "| --- | --- | --- |",
        ]
    )
    for gate in summary["enterprise_readiness_sync"]["gates"]:
        lines.append(f"| {gate['gate_id']} | {gate['label']} | `{gate['status']}` |")

    lines.extend(["", "## Blockers", ""])
    if summary["blockers"]:
        lines.extend(f"- {blocker}" for blocker in summary["blockers"])
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "## Public Safety",
            "",
            "The summary is generated from public-safe metadata only. It does not include "
            "Enterprise source code, license keys, package tokens, evaluator identities, "
            "operator identities, customer data, raw prompts, model reasoning, raw tool "
            "output, provider responses, private remediation details, or secrets.",
            "",
        ]
    )
    return "\n".join(lines)


def write_summary(summary: dict[str, Any], json_path: Path | None, markdown_path: Path | None) -> None:
    """Write optional JSON and Markdown readiness summaries."""

    if json_path is not None:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if markdown_path is not None:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_markdown(summary), encoding="utf-8")


def check_summary(summary: dict[str, Any], json_path: Path, markdown_path: Path) -> list[str]:
    """Return freshness failures for committed summary artifacts."""

    failures: list[str] = []
    expected_json = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    expected_markdown = render_markdown(summary)
    if not json_path.is_file():
        failures.append(f"missing summary JSON: {json_path}")
    elif json_path.read_text(encoding="utf-8") != expected_json:
        failures.append(f"summary JSON is stale: {json_path}")
    if not markdown_path.is_file():
        failures.append(f"missing summary Markdown: {markdown_path}")
    elif markdown_path.read_text(encoding="utf-8") != expected_markdown:
        failures.append(f"summary Markdown is stale: {markdown_path}")
    return failures

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument(
        "--packet",
        type=Path,
        default=DEFAULT_PACKET,
        help="Readiness packet path relative to repository root.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Readiness schema path relative to repository root.",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=None,
        help="Optional JSON summary output path.",
    )
    parser.add_argument(
        "--summary-markdown",
        type=Path,
        default=None,
        help="Optional Markdown summary output path.",
    )
    parser.add_argument(
        "--check-summary",
        action="store_true",
        help="Check committed summary artifacts for freshness.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    summary = build_summary(root, args.packet, args.schema)
    if args.summary_json or args.summary_markdown:
        write_summary(
            summary,
            root / args.summary_json if args.summary_json else None,
            root / args.summary_markdown if args.summary_markdown else None,
        )

    failures = list(summary["blockers"])
    if args.check_summary:
        failures.extend(
            check_summary(
                summary,
                root / DEFAULT_SUMMARY_JSON,
                root / DEFAULT_SUMMARY_MARKDOWN,
            )
        )
    if failures:
        print("CAVRA AISPM trial lab notebook publication validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA AISPM trial lab notebook publication validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
