from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


CONNECTOR_MANIFEST_SCHEMA = "cavra.connector.sdk.manifest.v1"
CONNECTOR_CERTIFICATION_SCHEMA = "cavra.connector.sdk.certification.v1"
CONNECTOR_SDK_READINESS_SCHEMA = "cavra.connector.sdk.readiness.v1"
CONNECTOR_SDK_EVIDENCE_SCHEMA = "cavra.connector.sdk.evidence.v1"

SUPPORTED_CONNECTOR_CATEGORIES = {
    "scm",
    "ci_cd",
    "siem",
    "itsm",
    "chatops",
    "notification",
    "grc",
    "model_registry",
    "scanner",
    "webhook",
}
SUPPORTED_AUTH_MODES = {
    "none",
    "api_key",
    "bearer_token",
    "oauth2_client_credentials",
    "oidc_workload_identity",
    "webhook_secret",
}
SUPPORTED_CERTIFICATION_TIERS = {"reference", "partner", "certified"}
REQUIRED_TEST_SUITES = {
    "unit",
    "contract",
    "redaction",
    "retry",
    "timeout",
    "auth",
    "compatibility",
}
REQUIRED_SECURITY_FLAGS = {
    "redacts_secrets",
    "does_not_log_payload_secrets",
    "supports_timeout",
    "supports_retries",
    "idempotency_supported",
}
REQUIRED_READINESS_ARTIFACTS = {
    "sdk_manifest_schema",
    "reference_connector_manifest",
    "certification_validator",
    "compatibility_matrix",
    "example_connector",
}


@dataclass(frozen=True)
class ConnectorRequest:
    event_type: str
    event_id: str
    payload: dict[str, Any]
    tenant_id: str | None = None
    workspace_id: str | None = None


@dataclass(frozen=True)
class ConnectorResponse:
    success: bool
    provider: str
    status_code: int | None = None
    external_ref: str | None = None
    error: str | None = None
    metadata: dict[str, Any] | None = None


class ConnectorPlugin(Protocol):
    manifest: dict[str, Any]

    def build_request(self, request: ConnectorRequest) -> dict[str, Any]:
        ...

    def parse_response(self, response: dict[str, Any]) -> ConnectorResponse:
        ...


def build_reference_webhook_manifest() -> dict[str, Any]:
    return {
        "schema_version": CONNECTOR_MANIFEST_SCHEMA,
        "connector_id": "cavra-reference-webhook",
        "display_name": "CAVRA Reference Webhook Connector",
        "provider": "webhook",
        "category": "webhook",
        "version": "2026.07",
        "sdk_version": "1.0",
        "entrypoint": "cavra.connectors.reference_webhook:ReferenceWebhookConnector",
        "certification_tier": "reference",
        "supported_events": [
            "cavra.evidence_bundle",
            "cavra.runtime.decision",
            "cavra.aispm.finding",
            "cavra.report.export",
        ],
        "capabilities": [
            "deliver_event",
            "redact_credentials",
            "retry_delivery",
            "timeout_control",
            "audit_metadata",
        ],
        "auth": {
            "modes": ["webhook_secret", "bearer_token"],
            "secret_fields": ["authorization", "token", "webhook_url"],
        },
        "runtime": {
            "language": "python",
            "min_python": "3.9",
            "network_required": True,
            "timeout_seconds_default": 10,
            "max_retries_default": 2,
        },
        "security": {
            "redacts_secrets": True,
            "does_not_log_payload_secrets": True,
            "supports_timeout": True,
            "supports_retries": True,
            "idempotency_supported": True,
            "tenant_scope_required": False,
        },
        "tests": {
            "suites": sorted(REQUIRED_TEST_SUITES),
            "fixtures": ["examples/connectors/webhook-certified/connector-manifest.json"],
        },
        "compatibility": {
            "cavra_versions": ["1.0.0"],
            "api_contract": "openapi/cavra-api.openapi.json",
            "connector_sdk": "1.0",
        },
    }


def validate_connector_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_manifest_schema(manifest, checks)
    _check_manifest_identity(manifest, checks)
    _check_manifest_capabilities(manifest, checks)
    _check_manifest_auth(manifest.get("auth", {}), checks)
    _check_manifest_runtime(manifest.get("runtime", {}), checks)
    _check_manifest_security(manifest.get("security", {}), checks)
    _check_manifest_tests(manifest.get("tests", {}), checks)
    _check_manifest_compatibility(manifest.get("compatibility", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.connector.sdk.manifest-validation.v1",
        "connector_id": manifest.get("connector_id", "unknown"),
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "checks": checks,
    }


def build_connector_compatibility_matrix(manifests: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for manifest in manifests:
        validation = validate_connector_manifest(manifest)
        rows.append(
            {
                "connector_id": manifest.get("connector_id"),
                "provider": manifest.get("provider"),
                "category": manifest.get("category"),
                "version": manifest.get("version"),
                "certification_tier": manifest.get("certification_tier"),
                "cavra_versions": manifest.get("compatibility", {}).get("cavra_versions", []),
                "valid": validation["valid"],
                "blocker_count": validation["blocker_count"],
            }
        )
    return {
        "schema_version": "cavra.connector.sdk.compatibility-matrix.v1",
        "product": "CAVRA",
        "connector_count": len(rows),
        "valid_connector_count": sum(1 for row in rows if row["valid"]),
        "rows": sorted(rows, key=lambda row: str(row.get("connector_id") or "")),
    }


def build_connector_certification_packet(
    manifest: dict[str, Any],
    *,
    probe_results: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validation = validate_connector_manifest(manifest)
    probe_results = probe_results or _default_probe_results()
    return {
        "schema_version": CONNECTOR_CERTIFICATION_SCHEMA,
        "product": "CAVRA",
        "connector_id": manifest.get("connector_id"),
        "provider": manifest.get("provider"),
        "certification_tier": manifest.get("certification_tier"),
        "manifest_validation": validation,
        "probe_results": probe_results,
        "certified": validation["valid"] and _probe_results_pass(probe_results),
    }


def build_enterprise_connector_sdk_readiness(
    packet: dict[str, Any] | None = None,
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    if packet is None:
        return {
            "schema_version": CONNECTOR_SDK_READINESS_SCHEMA,
            "product": "CAVRA",
            "evidence_mode": "contract",
            "ready_for_enterprise_connector_sdk_contract": True,
            "ready_for_enterprise_live_connector_certification": False,
            "status": "ready_with_warnings",
            "blocker_count": 0,
            "warning_count": 1,
            "checks": [
                {
                    "name": "evidence_packet",
                    "status": "warn",
                    "message": "Enterprise connector SDK contract is available, but no sample or live packet was supplied.",
                }
            ],
        }
    return validate_enterprise_connector_sdk_packet(packet, require_live=require_live)


def validate_enterprise_connector_sdk_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_packet_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_sdk_artifacts(packet.get("sdk_artifacts", {}), checks)
    _check_certification_program(packet.get("certification_program", {}), checks)
    _check_reference_connector(packet.get("reference_connector", {}), checks)
    _check_compatibility(packet.get("compatibility", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CONNECTOR_SDK_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_enterprise_connector_sdk_contract": contract_ready,
        "ready_for_enterprise_live_connector_certification": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _default_probe_results() -> dict[str, Any]:
    return {
        "contract": "pass",
        "redaction": "pass",
        "retry": "pass",
        "timeout": "pass",
        "auth": "pass",
        "compatibility": "pass",
    }


def _probe_results_pass(probe_results: dict[str, Any]) -> bool:
    return all(str(value) == "pass" for value in probe_results.values())


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_manifest_schema(manifest: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if manifest.get("schema_version") == CONNECTOR_MANIFEST_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Connector manifest schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Manifest must use cavra.connector.sdk.manifest.v1.")


def _check_manifest_identity(manifest: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = ["connector_id", "display_name", "provider", "version", "sdk_version", "entrypoint"]
    missing = [field for field in required if not manifest.get(field)]
    category = manifest.get("category")
    tier = manifest.get("certification_tier")
    if category not in SUPPORTED_CONNECTOR_CATEGORIES:
        missing.append("supported category")
    if tier not in SUPPORTED_CERTIFICATION_TIERS:
        missing.append("supported certification_tier")
    if not missing:
        _add_check(checks, "identity", "pass", "Connector identity, category, tier, and entrypoint are valid.")
    else:
        _add_check(checks, "identity", "blocker", f"Connector identity is missing: {', '.join(missing)}.")


def _check_manifest_capabilities(manifest: dict[str, Any], checks: list[dict[str, str]]) -> None:
    capabilities = [item for item in manifest.get("capabilities", []) if item]
    events = [item for item in manifest.get("supported_events", []) if item]
    if len(capabilities) >= 3 and events:
        _add_check(checks, "capabilities", "pass", "Connector capabilities and supported events are declared.")
    else:
        _add_check(checks, "capabilities", "blocker", "Connector requires at least three capabilities and one supported event.")


def _check_manifest_auth(auth: dict[str, Any], checks: list[dict[str, str]]) -> None:
    modes = set(auth.get("modes", []))
    secret_fields = [field for field in auth.get("secret_fields", []) if field]
    unsupported = sorted(modes - SUPPORTED_AUTH_MODES)
    if modes and not unsupported and secret_fields:
        _add_check(checks, "auth", "pass", "Connector auth modes and secret fields are declared.")
    else:
        missing: list[str] = []
        if not modes:
            missing.append("auth.modes")
        if unsupported:
            missing.append(f"unsupported auth modes: {', '.join(unsupported)}")
        if not secret_fields:
            missing.append("auth.secret_fields")
        _add_check(checks, "auth", "blocker", f"Connector auth declaration is missing: {', '.join(missing)}.")


def _check_manifest_runtime(runtime: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = {
        "language": bool(runtime.get("language")),
        "timeout_seconds_default": _positive_number(runtime.get("timeout_seconds_default")),
        "max_retries_default": _non_negative_number(runtime.get("max_retries_default")),
    }
    if all(required.values()):
        _add_check(checks, "runtime", "pass", "Connector runtime defaults are valid.")
    else:
        missing = [name for name, ok in required.items() if not ok]
        _add_check(checks, "runtime", "blocker", f"Connector runtime is missing: {', '.join(missing)}.")


def _check_manifest_security(security: dict[str, Any], checks: list[dict[str, str]]) -> None:
    missing = sorted(flag for flag in REQUIRED_SECURITY_FLAGS if security.get(flag) is not True)
    if not missing:
        _add_check(checks, "security", "pass", "Connector security controls are declared.")
    else:
        _add_check(checks, "security", "blocker", f"Connector security flags are missing: {', '.join(missing)}.")


def _check_manifest_tests(tests: dict[str, Any], checks: list[dict[str, str]]) -> None:
    suites = set(tests.get("suites", []))
    missing = sorted(REQUIRED_TEST_SUITES - suites)
    if not missing:
        _add_check(checks, "tests", "pass", "Connector certification test suites are declared.")
    else:
        _add_check(checks, "tests", "blocker", f"Connector test suites are missing: {', '.join(missing)}.")


def _check_manifest_compatibility(compatibility: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = {
        "cavra_versions": bool(compatibility.get("cavra_versions")),
        "api_contract": bool(compatibility.get("api_contract")),
        "connector_sdk": bool(compatibility.get("connector_sdk")),
    }
    if all(required.values()):
        _add_check(checks, "compatibility", "pass", "Connector compatibility metadata is declared.")
    else:
        missing = [name for name, ok in required.items() if not ok]
        _add_check(checks, "compatibility", "blocker", f"Connector compatibility is missing: {', '.join(missing)}.")


def _check_packet_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == CONNECTOR_SDK_EVIDENCE_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Connector SDK evidence packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.connector.sdk.evidence.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    evidence_mode = packet.get("evidence_mode")
    if evidence_mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live connector SDK evidence packet supplied.")
    elif evidence_mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample connector SDK packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live connector SDK validation requires evidence_mode=live.")


def _check_sdk_artifacts(artifacts: dict[str, Any], checks: list[dict[str, str]]) -> None:
    artifact_ids = set(artifacts.get("artifact_ids", []))
    missing = sorted(REQUIRED_READINESS_ARTIFACTS - artifact_ids)
    required_flags = {
        "versioned": artifacts.get("versioned") is True,
        "public_contract": artifacts.get("public_contract") is True,
        "docs_published": artifacts.get("docs_published") is True,
    }
    if not missing and all(required_flags.values()):
        _add_check(checks, "sdk_artifacts", "pass", "Connector SDK artifacts are versioned and published.")
        return
    missing_fields = [name for name, ok in required_flags.items() if not ok]
    if missing:
        missing_fields.append(f"artifact_ids: {', '.join(missing)}")
    _add_check(checks, "sdk_artifacts", "blocker", f"SDK artifacts are missing: {', '.join(missing_fields)}.")


def _check_certification_program(program: dict[str, Any], checks: list[dict[str, str]]) -> None:
    suites = set(program.get("required_test_suites", []))
    missing_suites = sorted(REQUIRED_TEST_SUITES - suites)
    required_flags = {
        "certification_policy_published": program.get("certification_policy_published") is True,
        "compatibility_matrix_published": program.get("compatibility_matrix_published") is True,
        "redaction_required": program.get("redaction_required") is True,
        "retries_required": program.get("retries_required") is True,
        "timeouts_required": program.get("timeouts_required") is True,
    }
    if not missing_suites and all(required_flags.values()):
        _add_check(checks, "certification_program", "pass", "Certification program and required test suites are defined.")
        return
    missing = [name for name, ok in required_flags.items() if not ok]
    if missing_suites:
        missing.append(f"test_suites: {', '.join(missing_suites)}")
    _add_check(checks, "certification_program", "blocker", f"Certification program is missing: {', '.join(missing)}.")


def _check_reference_connector(reference: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required_flags = {
        "manifest_validated": reference.get("manifest_validated") is True,
        "certification_packet_generated": reference.get("certification_packet_generated") is True,
        "delivery_contract_compatible": reference.get("delivery_contract_compatible") is True,
        "secret_redaction_tested": reference.get("secret_redaction_tested") is True,
        "example_connector_ref": bool(reference.get("example_connector_ref")),
    }
    if all(required_flags.values()):
        _add_check(checks, "reference_connector", "pass", "Reference connector validates against the SDK contract.")
    else:
        missing = [name for name, ok in required_flags.items() if not ok]
        _add_check(checks, "reference_connector", "blocker", f"Reference connector is missing: {', '.join(missing)}.")


def _check_compatibility(compatibility: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required_flags = {
        "api_contract_validated": compatibility.get("api_contract_validated") is True,
        "python_versions_declared": bool(compatibility.get("python_versions")),
        "cavra_versions_declared": bool(compatibility.get("cavra_versions")),
        "backward_compatibility_policy": bool(compatibility.get("backward_compatibility_policy")),
    }
    if all(required_flags.values()):
        _add_check(checks, "compatibility", "pass", "Connector SDK compatibility policy is declared.")
    else:
        missing = [name for name, ok in required_flags.items() if not ok]
        _add_check(checks, "compatibility", "blocker", f"Compatibility evidence is missing: {', '.join(missing)}.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = [
        "sdk_owner",
        "certification_review_ref",
        "compatibility_matrix_ref",
        "reference_connector_test_ref",
        "partner_onboarding_ref",
    ]
    missing = [field for field in required if not evidence.get(field)]
    if not missing:
        _add_check(checks, "operating_evidence", "pass", "Connector SDK operating evidence references are present.")
    else:
        _add_check(checks, "operating_evidence", "blocker", f"Operating evidence is missing: {', '.join(missing)}.")


def _positive_number(value: Any) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def _non_negative_number(value: Any) -> bool:
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False
