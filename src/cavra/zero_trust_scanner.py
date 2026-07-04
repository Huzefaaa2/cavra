from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


ZERO_TRUST_SCANNER_RESULT_SCHEMA = "cavra.zero-trust-scanner.result.v1"
ZERO_TRUST_SCANNER_EVIDENCE_SCHEMA = "cavra.zero-trust-scanner.evidence.v1"
ZERO_TRUST_SCANNER_READINESS_SCHEMA = "cavra.zero-trust-scanner.readiness.v1"

ALLOWED_SCAN_ENVIRONMENTS = {
    "customer_vpc",
    "on_prem",
    "private_subnet",
    "air_gapped",
    "container",
    "kubernetes",
}
REQUIRED_SCAN_RESULT_FIELDS = {
    "scanner_id",
    "environment",
    "asset_ref",
    "asset_type",
    "artifact_digest",
    "risk_score",
    "risk_tier",
    "findings",
    "evidence_ref",
}
FORBIDDEN_EGRESS_FIELDS = {
    "raw_model",
    "model_bytes",
    "model_weights",
    "training_data",
    "dataset_rows",
    "prompt_samples",
    "source_code",
    "secret",
    "private_key",
    "credential",
    "raw_artifact",
    "file_contents",
}
REQUIRED_SCANNER_ARTIFACTS = {
    "scanner_result_contract",
    "egress_sanitizer",
    "reference_scan_sample",
    "negative_egress_fixture",
    "deployment_topology",
}


def build_zero_trust_scan_result(payload: dict[str, Any]) -> dict[str, Any]:
    validation = validate_zero_trust_scan_result(payload)
    if not validation["valid"]:
        blockers = [
            check["message"]
            for check in validation["checks"]
            if check["status"] == "blocker"
        ]
        raise ValueError("; ".join(blockers))
    return {
        "schema_version": ZERO_TRUST_SCANNER_RESULT_SCHEMA,
        "product": "CAVRA",
        "scanner_id": payload["scanner_id"],
        "environment": payload["environment"],
        "asset_ref": payload["asset_ref"],
        "asset_type": payload["asset_type"],
        "artifact_digest": payload["artifact_digest"],
        "risk_score": int(payload["risk_score"]),
        "risk_tier": payload["risk_tier"],
        "findings": [_sanitize_finding(finding) for finding in payload["findings"]],
        "evidence_ref": payload["evidence_ref"],
        "metadata": sanitize_scanner_payload(payload.get("metadata", {})),
    }


def build_zero_trust_scan_result_from_file(path: Path) -> dict[str, Any]:
    payload = {
        "scanner_id": "cavra-local-reference-scanner",
        "environment": "container",
        "asset_ref": f"file://{path.name}",
        "asset_type": "artifact",
        "artifact_digest": f"sha256:{_sha256_file(path)}",
        "risk_score": 0,
        "risk_tier": "low",
        "findings": [],
        "evidence_ref": f"evidence://zero-trust-scanner/local/{path.name}",
        "metadata": {
            "file_name": path.name,
            "file_size_bytes": path.stat().st_size,
        },
    }
    return build_zero_trust_scan_result(payload)


def validate_zero_trust_scan_result(payload: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    missing = sorted(field for field in REQUIRED_SCAN_RESULT_FIELDS if field not in payload or payload.get(field) in (None, ""))
    forbidden = sorted(find_forbidden_egress_fields(payload))
    environment = str(payload.get("environment", ""))
    digest = str(payload.get("artifact_digest", ""))
    findings = payload.get("findings", [])
    score_valid = _risk_score_valid(payload.get("risk_score"))
    _add_check(
        checks,
        "required_fields",
        "pass" if not missing else "blocker",
        "Required scanner result fields are present." if not missing else f"Missing scanner fields: {', '.join(missing)}.",
    )
    _add_check(
        checks,
        "environment",
        "pass" if environment in ALLOWED_SCAN_ENVIRONMENTS else "blocker",
        "Scanner environment is an approved customer-side execution mode." if environment in ALLOWED_SCAN_ENVIRONMENTS else "Scanner environment must be customer_vpc, on_prem, private_subnet, air_gapped, container, or kubernetes.",
    )
    _add_check(
        checks,
        "artifact_digest",
        "pass" if digest.startswith("sha256:") and len(digest) > 20 else "blocker",
        "Artifact digest is hash-based." if digest.startswith("sha256:") and len(digest) > 20 else "Artifact digest must be a sha256 reference.",
    )
    _add_check(
        checks,
        "risk_score",
        "pass" if score_valid else "blocker",
        "Risk score is within 0-100." if score_valid else "Risk score must be an integer from 0 to 100.",
    )
    _add_check(
        checks,
        "findings",
        "pass" if isinstance(findings, list) else "blocker",
        "Findings are structured metadata records." if isinstance(findings, list) else "Findings must be a list.",
    )
    _add_check(
        checks,
        "no_raw_egress",
        "pass" if not forbidden else "blocker",
        "Scanner result contains only metadata, hashes, scores, and evidence references." if not forbidden else f"Forbidden raw egress fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.zero-trust-scanner.result-validation.v1",
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "checks": checks,
    }


def sanitize_scanner_payload(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {
            key: sanitize_scanner_payload(value)
            for key, value in payload.items()
            if key not in FORBIDDEN_EGRESS_FIELDS
        }
    if isinstance(payload, list):
        return [sanitize_scanner_payload(item) for item in payload]
    return payload


def find_forbidden_egress_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key in FORBIDDEN_EGRESS_FIELDS:
                found.add(path)
            found.update(find_forbidden_egress_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_egress_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def validate_zero_trust_scanner_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_deployment(packet.get("deployment", {}), checks)
    _check_artifacts(packet.get("scanner_artifacts", {}), checks)
    _check_egress_controls(packet.get("egress_controls", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": ZERO_TRUST_SCANNER_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_zero_trust_scanner_contract": contract_ready,
        "ready_for_live_zero_trust_scanner": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _sanitize_finding(finding: Any) -> dict[str, Any]:
    if not isinstance(finding, dict):
        return {"finding_id": "unstructured", "risk_score": 0, "metadata": sanitize_scanner_payload(finding)}
    allowed = {
        "finding_id",
        "title",
        "category",
        "severity",
        "risk_score",
        "asset_ref",
        "evidence_ref",
        "metadata",
    }
    return {
        key: sanitize_scanner_payload(value)
        for key, value in finding.items()
        if key in allowed and key not in FORBIDDEN_EGRESS_FIELDS
    }


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _risk_score_valid(value: Any) -> bool:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return False
    return 0 <= score <= 100


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == ZERO_TRUST_SCANNER_EVIDENCE_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Zero-trust scanner evidence packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.zero-trust-scanner.evidence.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    if mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live zero-trust scanner evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample zero-trust scanner packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live scanner validation requires evidence_mode=live.")


def _check_deployment(deployment: dict[str, Any], checks: list[dict[str, str]]) -> None:
    modes = set(deployment.get("supported_modes", []))
    required = {"customer_vpc", "on_prem", "container"}
    missing = sorted(required - modes)
    flags = {
        "customer_side_execution": deployment.get("customer_side_execution") is True,
        "outbound_only": deployment.get("outbound_only") is True,
        "private_network_supported": deployment.get("private_network_supported") is True,
    }
    if not missing and all(flags.values()):
        _add_check(checks, "deployment", "pass", "Scanner deployment topology supports customer-side execution.")
        return
    problems = [name for name, ok in flags.items() if not ok]
    if missing:
        problems.append(f"supported_modes: {', '.join(missing)}")
    _add_check(checks, "deployment", "blocker", f"Scanner deployment evidence is missing: {', '.join(problems)}.")


def _check_artifacts(artifacts: dict[str, Any], checks: list[dict[str, str]]) -> None:
    artifact_ids = set(artifacts.get("artifact_ids", []))
    missing = sorted(REQUIRED_SCANNER_ARTIFACTS - artifact_ids)
    flags = {
        "versioned": artifacts.get("versioned") is True,
        "docs_published": artifacts.get("docs_published") is True,
        "reference_result_validated": artifacts.get("reference_result_validated") is True,
    }
    if not missing and all(flags.values()):
        _add_check(checks, "scanner_artifacts", "pass", "Scanner contract artifacts are versioned and validated.")
        return
    problems = [name for name, ok in flags.items() if not ok]
    if missing:
        problems.append(f"artifact_ids: {', '.join(missing)}")
    _add_check(checks, "scanner_artifacts", "blocker", f"Scanner artifacts are missing: {', '.join(problems)}.")


def _check_egress_controls(controls: dict[str, Any], checks: list[dict[str, str]]) -> None:
    flags = {
        "metadata_only": controls.get("metadata_only") is True,
        "hashes_only_for_artifacts": controls.get("hashes_only_for_artifacts") is True,
        "raw_model_blocked": controls.get("raw_model_blocked") is True,
        "training_data_blocked": controls.get("training_data_blocked") is True,
        "secret_redaction_tested": controls.get("secret_redaction_tested") is True,
        "negative_egress_tests_passed": controls.get("negative_egress_tests_passed") is True,
    }
    if all(flags.values()):
        _add_check(checks, "egress_controls", "pass", "Scanner egress controls are enforced and tested.")
    else:
        missing = [name for name, ok in flags.items() if not ok]
        _add_check(checks, "egress_controls", "blocker", f"Scanner egress controls are missing: {', '.join(missing)}.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = [
        "scanner_owner",
        "reference_scan_result_ref",
        "negative_egress_test_ref",
        "deployment_validation_ref",
        "customer_network_boundary_ref",
    ]
    missing = [field for field in required if not evidence.get(field)]
    if not missing:
        _add_check(checks, "operating_evidence", "pass", "Zero-trust scanner operating evidence references are present.")
    else:
        _add_check(checks, "operating_evidence", "blocker", f"Operating evidence is missing: {', '.join(missing)}.")
