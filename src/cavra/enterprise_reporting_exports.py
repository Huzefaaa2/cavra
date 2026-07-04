from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ENTERPRISE_REPORT_EXPORT_READINESS_SCHEMA = "cavra.enterprise.report-exports.readiness.v1"
ENTERPRISE_REPORT_EXPORT_EVIDENCE_SCHEMA = "cavra.enterprise.report-exports.evidence.v1"
ENTERPRISE_REPORT_EXPORT_MANIFEST_SCHEMA = "cavra.enterprise.report-exports.manifest.v1"

REQUIRED_EXPORTS = {"auditor_markdown", "bi_csv", "executive_json", "board_pdf_manifest"}
REQUIRED_LIVE_FORMATS = {"pdf", "csv", "json", "markdown"}
REQUIRED_DISTRIBUTION_CHANNELS = {"portal", "email", "grc_upload"}
REQUIRED_CONTROLS = {
    "rbac_scoped",
    "recipient_policy_enforced",
    "watermarking_enabled",
    "immutable_store_enabled",
    "redaction_enabled",
    "export_approval_supported",
}


def build_sample_reporting_source() -> dict[str, Any]:
    return {
        "reporting_period": {
            "starts_at": "2026-07-01T00:00:00Z",
            "ends_at": "2026-07-31T23:59:59Z",
        },
        "executive_summary": {
            "headline": "CAVRA runtime authority reduced high-risk unmanaged agent actions.",
            "posture_status": "attention_required",
            "readiness_score": 91,
            "material_risk": "Residual approval latency and compliance exceptions require governance review.",
            "recommended_action": "Clear overdue approvals and close compliance exceptions before the next board cycle.",
        },
        "metrics": [
            {"metric": "runtime_decisions", "value": 1284, "unit": "count", "audience": "bi"},
            {"metric": "blocked_actions", "value": 73, "unit": "count", "audience": "bi"},
            {"metric": "approval_required", "value": 119, "unit": "count", "audience": "bi"},
            {"metric": "audit_readiness_score", "value": 91, "unit": "percent", "audience": "board"},
            {"metric": "mapped_compliance_findings", "value": 48, "unit": "count", "audience": "audit"},
        ],
        "audit_findings": [
            {
                "finding_id": "audit-001",
                "title": "Immutable audit log validated for reporting window.",
                "severity": "low",
                "status": "closed",
                "evidence_ref": "evidence://sample/reporting/audit-log",
            },
            {
                "finding_id": "audit-002",
                "title": "Two approval exceptions need CISO review.",
                "severity": "medium",
                "status": "open",
                "evidence_ref": "evidence://sample/reporting/approval-exceptions",
            },
        ],
        "board_talking_points": [
            "Coverage improved across governed repositories and runtime workflows.",
            "AISPM findings are now mapped to clause-level compliance controls.",
            "Evidence custody, immutable audit, and reporting exports have live validation gates.",
        ],
    }


def export_enterprise_reporting_package(
    output_dir: Path,
    *,
    source: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    source = source or build_sample_reporting_source()
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()

    artifacts = [
        _write_executive_json(output_dir, source, generated_at),
        _write_bi_csv(output_dir, source),
        _write_auditor_markdown(output_dir, source, generated_at),
        _write_board_pdf_manifest(output_dir, source, generated_at),
    ]
    manifest = {
        "schema_version": ENTERPRISE_REPORT_EXPORT_MANIFEST_SCHEMA,
        "product": "CAVRA",
        "generated_at": generated_at,
        "export_ids": sorted(REQUIRED_EXPORTS),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "public_safety_boundary": (
            "Artifacts are public-safe samples. Enterprise renderers attach real tenant-scoped PDF, "
            "workbook, delivery, and evidence-room outputs in private deployments."
        ),
    }
    manifest_path = output_dir / "enterprise-report-export-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["manifest_sha256"] = _sha256(manifest_path)
    return manifest


def build_enterprise_report_export_readiness(
    packet: dict[str, Any] | None = None,
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    if packet is None:
        return {
            "schema_version": ENTERPRISE_REPORT_EXPORT_READINESS_SCHEMA,
            "product": "CAVRA",
            "evidence_mode": "contract",
            "ready_for_enterprise_report_export_contract": True,
            "ready_for_enterprise_live_report_exports": False,
            "status": "ready_with_warnings",
            "blocker_count": 0,
            "warning_count": 1,
            "checks": [
                {
                    "name": "evidence_packet",
                    "status": "warn",
                    "message": "Enterprise report export contract is available, but no sample or live packet was supplied.",
                }
            ],
        }
    return validate_enterprise_report_export_packet(packet, require_live=require_live)


def validate_enterprise_report_export_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_export_catalog(packet.get("export_catalog", {}), checks)
    _check_artifacts(packet.get("artifacts", {}), checks)
    _check_distribution(packet.get("distribution", {}), checks)
    _check_controls(packet.get("controls", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)

    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": ENTERPRISE_REPORT_EXPORT_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_enterprise_report_export_contract": contract_ready,
        "ready_for_enterprise_live_report_exports": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _write_executive_json(output_dir: Path, source: dict[str, Any], generated_at: str) -> dict[str, Any]:
    path = output_dir / "executive-summary.json"
    payload = {
        "schema_version": "cavra.enterprise.executive-summary.v1",
        "generated_at": generated_at,
        "reporting_period": source["reporting_period"],
        "executive_summary": source["executive_summary"],
        "board_talking_points": source["board_talking_points"],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return _artifact("executive_json", path, "application/json")


def _write_bi_csv(output_dir: Path, source: dict[str, Any]) -> dict[str, Any]:
    path = output_dir / "bi-metrics.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "unit", "audience"])
        writer.writeheader()
        writer.writerows(source["metrics"])
    return _artifact("bi_csv", path, "text/csv")


def _write_auditor_markdown(output_dir: Path, source: dict[str, Any], generated_at: str) -> dict[str, Any]:
    path = output_dir / "auditor-narrative.md"
    lines = [
        "# CAVRA Auditor Narrative",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "## Summary",
        "",
        source["executive_summary"]["headline"],
        "",
        "## Findings",
        "",
    ]
    for finding in source["audit_findings"]:
        lines.extend(
            [
                f"- `{finding['finding_id']}` {finding['title']}",
                f"  - Severity: `{finding['severity']}`",
                f"  - Status: `{finding['status']}`",
                f"  - Evidence: `{finding['evidence_ref']}`",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return _artifact("auditor_markdown", path, "text/markdown")


def _write_board_pdf_manifest(output_dir: Path, source: dict[str, Any], generated_at: str) -> dict[str, Any]:
    path = output_dir / "board-pack-pdf-manifest.json"
    payload = {
        "schema_version": "cavra.enterprise.board-pdf-manifest.v1",
        "generated_at": generated_at,
        "title": "CAVRA Board Pack",
        "format": "pdf",
        "renderer": "requires_cavra_enterprise",
        "source_sections": ["executive_summary", "metrics", "audit_findings", "board_talking_points"],
        "page_plan": [
            "Executive posture summary",
            "AISPM and runtime control metrics",
            "Audit readiness and evidence status",
            "Board talking points and decisions requested",
        ],
        "readiness_score": source["executive_summary"]["readiness_score"],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return _artifact("board_pdf_manifest", path, "application/json")


def _artifact(export_id: str, path: Path, media_type: str) -> dict[str, Any]:
    return {
        "export_id": export_id,
        "path": str(path),
        "filename": path.name,
        "media_type": media_type,
        "sha256": _sha256(path),
        "size_bytes": path.stat().st_size,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == ENTERPRISE_REPORT_EXPORT_EVIDENCE_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Report export evidence packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.enterprise.report-exports.evidence.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    evidence_mode = packet.get("evidence_mode")
    if evidence_mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live report export evidence packet supplied.")
    elif evidence_mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample report export packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live report export validation requires evidence_mode=live.")


def _check_export_catalog(catalog: dict[str, Any], checks: list[dict[str, str]]) -> None:
    export_ids = set(catalog.get("export_ids", []))
    formats = set(catalog.get("formats", []))
    audiences = set(catalog.get("audiences", []))
    missing_exports = sorted(REQUIRED_EXPORTS - export_ids)
    missing_formats = sorted(REQUIRED_LIVE_FORMATS - formats)
    required_flags = {
        "versioned": catalog.get("versioned") is True,
        "approved": catalog.get("approved") is True,
        "owner": bool(catalog.get("owner")),
        "catalog_ref": bool(catalog.get("catalog_ref")),
    }
    required_audiences = {"auditor", "bi", "executive", "board"}
    missing_audiences = sorted(required_audiences - audiences)
    if not missing_exports and not missing_formats and not missing_audiences and all(required_flags.values()):
        _add_check(checks, "export_catalog", "pass", "Approved export catalog covers auditor, BI, executive, and board outputs.")
        return
    missing = [name for name, ok in required_flags.items() if not ok]
    if missing_exports:
        missing.append(f"exports: {', '.join(missing_exports)}")
    if missing_formats:
        missing.append(f"formats: {', '.join(missing_formats)}")
    if missing_audiences:
        missing.append(f"audiences: {', '.join(missing_audiences)}")
    _add_check(checks, "export_catalog", "blocker", f"Export catalog is missing: {', '.join(missing)}.")


def _check_artifacts(artifacts: dict[str, Any], checks: list[dict[str, str]]) -> None:
    generated = set(artifacts.get("generated_exports", []))
    missing_exports = sorted(REQUIRED_EXPORTS - generated)
    required_flags = {
        "checksums_verified": artifacts.get("checksums_verified") is True,
        "sample_package_validated": artifacts.get("sample_package_validated") is True,
        "pdf_render_validated": artifacts.get("pdf_render_validated") is True,
        "csv_schema_validated": artifacts.get("csv_schema_validated") is True,
        "json_schema_validated": artifacts.get("json_schema_validated") is True,
        "markdown_render_validated": artifacts.get("markdown_render_validated") is True,
        "manifest_ref": bool(artifacts.get("manifest_ref")),
    }
    if not missing_exports and all(required_flags.values()):
        _add_check(checks, "artifacts", "pass", "Report export artifacts and checksums are validated.")
        return
    missing = [name for name, ok in required_flags.items() if not ok]
    if missing_exports:
        missing.append(f"generated_exports: {', '.join(missing_exports)}")
    _add_check(checks, "artifacts", "blocker", f"Report artifacts are missing: {', '.join(missing)}.")


def _check_distribution(distribution: dict[str, Any], checks: list[dict[str, str]]) -> None:
    channels = set(distribution.get("channels", []))
    missing_channels = sorted(REQUIRED_DISTRIBUTION_CHANNELS - channels)
    required_flags = {
        "delivery_tested": distribution.get("delivery_tested") is True,
        "evidence_room_published": distribution.get("evidence_room_published") is True,
        "recipient_approval_tested": distribution.get("recipient_approval_tested") is True,
        "latest_delivery_ref": bool(distribution.get("latest_delivery_ref")),
    }
    if not missing_channels and all(required_flags.values()):
        _add_check(checks, "distribution", "pass", "Portal, email, and GRC upload distribution paths are validated.")
        return
    missing = [name for name, ok in required_flags.items() if not ok]
    if missing_channels:
        missing.append(f"channels: {', '.join(missing_channels)}")
    _add_check(checks, "distribution", "blocker", f"Distribution path is missing: {', '.join(missing)}.")


def _check_controls(controls: dict[str, Any], checks: list[dict[str, str]]) -> None:
    missing = sorted(control for control in REQUIRED_CONTROLS if controls.get(control) is not True)
    if not missing:
        _add_check(checks, "controls", "pass", "Export security controls are enabled.")
    else:
        _add_check(checks, "controls", "blocker", f"Export controls are missing: {', '.join(missing)}.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = [
        "report_owner",
        "approval_policy_ref",
        "export_validation_ref",
        "evidence_room_ref",
        "auditor_handoff_ref",
        "board_pack_review_ref",
    ]
    missing = [field for field in required if not evidence.get(field)]
    if not missing:
        _add_check(checks, "operating_evidence", "pass", "Report export operating evidence references are present.")
    else:
        _add_check(checks, "operating_evidence", "blocker", f"Operating evidence is missing: {', '.join(missing)}.")
