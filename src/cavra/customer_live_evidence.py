from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CUSTOMER_LIVE_EVIDENCE_SCHEMA = "cavra.customer-live-evidence.packet.v1"
CUSTOMER_LIVE_EVIDENCE_RESULT_SCHEMA = "cavra.customer-live-evidence.result.v1"

REQUIRED_EVIDENCE_SECTIONS = {
    "platform_readiness": [
        "tenant_isolation_ref",
        "identity_validation_ref",
        "data_residency_ref",
        "private_network_ref",
    ],
    "evidence_audit": [
        "kms_hsm_custody_ref",
        "immutable_audit_ref",
        "retention_policy_ref",
        "independent_verifier_ref",
    ],
    "connectors_scanners": [
        "connector_live_delivery_ref",
        "model_registry_sandbox_ref",
        "zero_trust_scanner_ref",
        "no_raw_egress_test_ref",
    ],
    "policy_monitoring": [
        "opa_runtime_ref",
        "policy_lifecycle_ref",
        "continuous_monitoring_ref",
        "event_bus_health_ref",
    ],
    "phase6_ecosystem": [
        "phase6_rollup_ref",
        "benchmark_run_ref",
        "generic_adapter_ref",
        "ai_red_team_ref",
        "zero_trust_deployment_ref",
    ],
    "aispm_production": [
        "production_readiness_packet_ref",
        "report_delivery_ref",
        "runtime_workflow_ref",
        "closeout_approval_ref",
    ],
}

REQUIRED_CUSTOMER_PROFILE_FIELDS = {
    "customer_ref",
    "deployment_ref",
    "environment_ref",
    "owner_group_ref",
    "evidence_room_ref",
}

FORBIDDEN_LIVE_EVIDENCE_FIELDS = {
    "secret",
    "password",
    "token",
    "api_key",
    "private_key",
    "connection_string",
    "raw_model",
    "model_bytes",
    "model_weights",
    "training_data",
    "dataset_rows",
    "prompt_samples",
    "source_code",
    "customer_data",
    "tenant_name",
    "email",
    "smtp_password",
}

ALLOWED_REF_PREFIXES = (
    "evidence://",
    "ticket://",
    "audit://",
    "runbook://",
    "git://",
    "workflow://",
    "vault://",
    "share://",
    "sample://",
)


def build_customer_live_evidence_template(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    return {
        "schema_version": CUSTOMER_LIVE_EVIDENCE_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "customer_profile": {
            "customer_ref": f"{prefix}://customer/redacted",
            "deployment_ref": f"{prefix}://deployment/managed-enterprise",
            "environment_ref": f"{prefix}://environment/production",
            "owner_group_ref": f"{prefix}://owner/security-platform",
            "evidence_room_ref": f"{prefix}://evidence-room/cavra-live-closeout",
        },
        "evidence_sections": {
            section: {
                field: f"{prefix}://customer-live/{section}/{field}"
                for field in fields
            }
            for section, fields in sorted(REQUIRED_EVIDENCE_SECTIONS.items())
        },
        "redaction_controls": {
            "contains_no_secrets": True,
            "contains_no_raw_model_data": True,
            "contains_no_training_data": True,
            "contains_no_prompt_samples": True,
            "contains_no_source_code": True,
            "contains_no_customer_pii": True,
        },
        "attestation": {
            "prepared_by_ref": f"{prefix}://operator/customer-success-security",
            "reviewer_ref": f"{prefix}://approver/cavra-release-authority",
            "approval_ref": f"{prefix}://approval/customer-live-closeout",
        },
    }


def validate_customer_live_evidence_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == CUSTOMER_LIVE_EVIDENCE_SCHEMA else "blocker",
        "Customer-live evidence schema is valid."
        if packet.get("schema_version") == CUSTOMER_LIVE_EVIDENCE_SCHEMA
        else f"Packet must use {CUSTOMER_LIVE_EVIDENCE_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_profile(packet.get("customer_profile", {}), checks)
    _check_evidence_sections(packet.get("evidence_sections", {}), checks)
    _check_redaction_controls(packet.get("redaction_controls", {}), checks)
    _check_attestation(packet.get("attestation", {}), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(packet))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Packet contains only sanitized references and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    live_ready = blocker_count == 0 and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIVE_EVIDENCE_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_customer_live_evidence_intake": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def find_forbidden_live_evidence_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            normalized = str(key).lower()
            if normalized in FORBIDDEN_LIVE_EVIDENCE_FIELDS:
                found.add(path)
            found.update(find_forbidden_live_evidence_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_live_evidence_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def write_customer_live_evidence_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_customer_live_evidence_template(evidence_mode="sample")
    live = build_customer_live_evidence_template(evidence_mode="live")
    sample_result = validate_customer_live_evidence_packet(sample)
    live_result = validate_customer_live_evidence_packet(live, require_live=True)
    written = {
        "sample": output_dir / "customer-live-evidence.sample.json",
        "live_sanitized_example": output_dir / "customer-live-evidence.live.sanitized.example.json",
        "sample_result": output_dir / "customer-live-evidence.sample.result.json",
        "live_result": output_dir / "customer-live-evidence.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.customer-live-evidence.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_live_evidence_intake": live_result["ready_for_customer_live_evidence_intake"],
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    sanitized = packet.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized customer evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample packet validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Customer-live intake requires evidence_mode=live and sanitized=true.")


def _check_profile(profile: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(profile, dict):
        _add_check(checks, "customer_profile", "blocker", "customer_profile must be an object.")
        return
    missing = sorted(field for field in REQUIRED_CUSTOMER_PROFILE_FIELDS if not profile.get(field))
    bad_refs = sorted(field for field in REQUIRED_CUSTOMER_PROFILE_FIELDS if field in profile and not _is_safe_ref(profile[field]))
    if not missing and not bad_refs:
        _add_check(checks, "customer_profile", "pass", "Customer profile uses sanitized references.")
    else:
        problems = []
        if missing:
            problems.append(f"missing: {', '.join(missing)}")
        if bad_refs:
            problems.append(f"unsafe refs: {', '.join(bad_refs)}")
        _add_check(checks, "customer_profile", "blocker", f"Customer profile is invalid: {'; '.join(problems)}.")


def _check_evidence_sections(sections: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(sections, dict):
        _add_check(checks, "evidence_sections", "blocker", "evidence_sections must be an object.")
        return
    missing_sections = sorted(section for section in REQUIRED_EVIDENCE_SECTIONS if section not in sections)
    missing_fields: list[str] = []
    bad_refs: list[str] = []
    for section, fields in REQUIRED_EVIDENCE_SECTIONS.items():
        section_payload = sections.get(section, {})
        if not isinstance(section_payload, dict):
            missing_fields.extend(f"{section}.{field}" for field in fields)
            continue
        for field in fields:
            value = section_payload.get(field)
            if not value:
                missing_fields.append(f"{section}.{field}")
            elif not _is_safe_ref(value):
                bad_refs.append(f"{section}.{field}")
    if not missing_sections and not missing_fields and not bad_refs:
        _add_check(checks, "evidence_sections", "pass", "All customer-live evidence references are present and sanitized.")
    else:
        problems = []
        if missing_sections:
            problems.append(f"missing sections: {', '.join(missing_sections)}")
        if missing_fields:
            problems.append(f"missing fields: {', '.join(missing_fields)}")
        if bad_refs:
            problems.append(f"unsafe refs: {', '.join(bad_refs)}")
        _add_check(checks, "evidence_sections", "blocker", f"Evidence sections are invalid: {'; '.join(problems)}.")


def _check_redaction_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    required = [
        "contains_no_secrets",
        "contains_no_raw_model_data",
        "contains_no_training_data",
        "contains_no_prompt_samples",
        "contains_no_source_code",
        "contains_no_customer_pii",
    ]
    if not isinstance(controls, dict):
        _add_check(checks, "redaction_controls", "blocker", "redaction_controls must be an object.")
        return
    missing = sorted(control for control in required if controls.get(control) is not True)
    _add_check(
        checks,
        "redaction_controls",
        "pass" if not missing else "blocker",
        "Redaction controls are explicitly affirmed."
        if not missing
        else f"Redaction controls missing or false: {', '.join(missing)}.",
    )


def _check_attestation(attestation: Any, checks: list[dict[str, str]]) -> None:
    required = ["prepared_by_ref", "reviewer_ref", "approval_ref"]
    if not isinstance(attestation, dict):
        _add_check(checks, "attestation", "blocker", "attestation must be an object.")
        return
    missing = sorted(field for field in required if not attestation.get(field))
    bad_refs = sorted(field for field in required if field in attestation and not _is_safe_ref(attestation[field]))
    if not missing and not bad_refs:
        _add_check(checks, "attestation", "pass", "Prepared-by, reviewer, and approval refs are present.")
    else:
        problems = []
        if missing:
            problems.append(f"missing: {', '.join(missing)}")
        if bad_refs:
            problems.append(f"unsafe refs: {', '.join(bad_refs)}")
        _add_check(checks, "attestation", "blocker", f"Attestation is invalid: {'; '.join(problems)}.")


def _is_safe_ref(value: Any) -> bool:
    text = str(value)
    return any(text.startswith(prefix) for prefix in ALLOWED_REF_PREFIXES)


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
