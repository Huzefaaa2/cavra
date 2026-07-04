from __future__ import annotations

from typing import Any

from cavra.connector_sdk import (
    CONNECTOR_MANIFEST_SCHEMA,
    REQUIRED_TEST_SUITES,
    build_connector_certification_packet,
    build_connector_compatibility_matrix,
    validate_connector_manifest,
)


CERTIFIED_CONNECTORS_EVIDENCE_SCHEMA = "cavra.certified-connectors.evidence.v1"
CERTIFIED_CONNECTORS_READINESS_SCHEMA = "cavra.certified-connectors.readiness.v1"

PRIORITY_CONNECTOR_SPECS: dict[str, dict[str, Any]] = {
    "github": {
        "display_name": "GitHub Connector",
        "category": "scm",
        "auth_modes": ["bearer_token", "oidc_workload_identity"],
        "events": ["cavra.runtime.decision", "cavra.evidence_bundle", "cavra.pr.attestation"],
        "capabilities": ["required_check", "repository_dispatch", "pull_request_comment", "audit_metadata"],
    },
    "gitlab": {
        "display_name": "GitLab Connector",
        "category": "scm",
        "auth_modes": ["bearer_token", "api_key"],
        "events": ["cavra.runtime.decision", "cavra.evidence_bundle", "cavra.merge_request.attestation"],
        "capabilities": ["commit_status", "pipeline_trigger", "merge_request_note", "audit_metadata"],
    },
    "azure_repos": {
        "display_name": "Azure Repos Connector",
        "category": "scm",
        "auth_modes": ["bearer_token", "oidc_workload_identity"],
        "events": ["cavra.runtime.decision", "cavra.evidence_bundle", "cavra.pull_request.attestation"],
        "capabilities": ["pull_request_status", "service_hook", "policy_evaluation", "audit_metadata"],
    },
    "github_actions": {
        "display_name": "GitHub Actions Connector",
        "category": "ci_cd",
        "auth_modes": ["bearer_token", "oidc_workload_identity"],
        "events": ["cavra.release.gate", "cavra.runtime.decision", "cavra.evidence_bundle"],
        "capabilities": ["workflow_dispatch", "deployment_protection", "required_check", "audit_metadata"],
    },
    "jenkins": {
        "display_name": "Jenkins Connector",
        "category": "ci_cd",
        "auth_modes": ["api_key", "bearer_token"],
        "events": ["cavra.release.gate", "cavra.runtime.decision", "cavra.evidence_bundle"],
        "capabilities": ["job_parameter_trigger", "build_status", "evidence_upload", "audit_metadata"],
    },
    "splunk": {
        "display_name": "Splunk HEC Connector",
        "category": "siem",
        "auth_modes": ["bearer_token"],
        "events": ["cavra.evidence_bundle", "cavra.runtime.decision", "cavra.aispm.finding"],
        "capabilities": ["hec_event_delivery", "index_routing", "redacted_headers", "audit_metadata"],
    },
    "sentinel": {
        "display_name": "Microsoft Sentinel Connector",
        "category": "siem",
        "auth_modes": ["bearer_token", "oauth2_client_credentials"],
        "events": ["cavra.evidence_bundle", "cavra.runtime.decision", "cavra.aispm.finding"],
        "capabilities": ["log_ingestion", "workspace_routing", "redacted_headers", "audit_metadata"],
    },
    "servicenow": {
        "display_name": "ServiceNow Connector",
        "category": "itsm",
        "auth_modes": ["bearer_token", "api_key"],
        "events": ["cavra.approval.required", "cavra.runtime.decision", "cavra.aispm.finding"],
        "capabilities": ["change_request", "incident_creation", "correlation_id", "audit_metadata"],
    },
    "jira": {
        "display_name": "Jira Connector",
        "category": "itsm",
        "auth_modes": ["bearer_token", "api_key"],
        "events": ["cavra.approval.required", "cavra.runtime.decision", "cavra.aispm.finding"],
        "capabilities": ["issue_creation", "labels", "structured_description", "audit_metadata"],
    },
    "slack": {
        "display_name": "Slack Connector",
        "category": "chatops",
        "auth_modes": ["webhook_secret", "bearer_token"],
        "events": ["cavra.approval.required", "cavra.runtime.decision", "cavra.aispm.finding"],
        "capabilities": ["block_message", "channel_routing", "approval_notification", "audit_metadata"],
    },
    "teams": {
        "display_name": "Microsoft Teams Connector",
        "category": "chatops",
        "auth_modes": ["webhook_secret", "bearer_token"],
        "events": ["cavra.approval.required", "cavra.runtime.decision", "cavra.aispm.finding"],
        "capabilities": ["message_card", "channel_routing", "approval_notification", "audit_metadata"],
    },
}

REQUIRED_PRIORITY_CONNECTORS = set(PRIORITY_CONNECTOR_SPECS)
REQUIRED_CONNECTOR_GROUPS = {"scm", "ci_cd", "siem", "itsm", "chatops"}


def build_priority_connector_manifest(provider: str) -> dict[str, Any]:
    spec = PRIORITY_CONNECTOR_SPECS[provider]
    return {
        "schema_version": CONNECTOR_MANIFEST_SCHEMA,
        "connector_id": f"cavra-certified-{provider.replace('_', '-')}",
        "display_name": spec["display_name"],
        "provider": provider,
        "category": spec["category"],
        "version": "2026.07",
        "sdk_version": "1.0",
        "entrypoint": f"cavra.connectors.{provider}:CertifiedConnector",
        "certification_tier": "certified",
        "supported_events": spec["events"],
        "capabilities": spec["capabilities"],
        "auth": {
            "modes": spec["auth_modes"],
            "secret_fields": ["authorization", "token", "api_key", "webhook_url", "client_secret"],
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
            "tenant_scope_required": True,
        },
        "tests": {
            "suites": sorted(REQUIRED_TEST_SUITES),
            "fixtures": [f"examples/connectors/priority-certified/{provider}.json"],
        },
        "compatibility": {
            "cavra_versions": ["1.0.0"],
            "api_contract": "openapi/cavra-api.openapi.json",
            "connector_sdk": "1.0",
        },
    }


def build_priority_connector_registry() -> dict[str, Any]:
    manifests = [build_priority_connector_manifest(provider) for provider in sorted(PRIORITY_CONNECTOR_SPECS)]
    return {
        "schema_version": "cavra.certified-connectors.registry.v1",
        "product": "CAVRA",
        "connector_count": len(manifests),
        "providers": sorted(PRIORITY_CONNECTOR_SPECS),
        "groups": sorted({manifest["category"] for manifest in manifests}),
        "manifests": manifests,
        "compatibility_matrix": build_connector_compatibility_matrix(manifests),
        "certification_packets": [
            build_connector_certification_packet(manifest) for manifest in manifests
        ],
    }


def validate_priority_connector_registry(manifests: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    manifests = manifests or [build_priority_connector_manifest(provider) for provider in sorted(PRIORITY_CONNECTOR_SPECS)]
    checks: list[dict[str, str]] = []
    providers = {str(manifest.get("provider")) for manifest in manifests}
    missing = sorted(REQUIRED_PRIORITY_CONNECTORS - providers)
    invalid = [
        str(manifest.get("provider") or manifest.get("connector_id"))
        for manifest in manifests
        if not validate_connector_manifest(manifest)["valid"]
    ]
    groups = {str(manifest.get("category")) for manifest in manifests}
    missing_groups = sorted(REQUIRED_CONNECTOR_GROUPS - groups)
    _add_check(
        checks,
        "priority_providers",
        "pass" if not missing else "blocker",
        "Every priority provider has a certified manifest." if not missing else f"Missing priority providers: {', '.join(missing)}.",
    )
    _add_check(
        checks,
        "manifest_validation",
        "pass" if not invalid else "blocker",
        "Every certified connector manifest validates." if not invalid else f"Invalid manifests: {', '.join(invalid)}.",
    )
    _add_check(
        checks,
        "connector_groups",
        "pass" if not missing_groups else "blocker",
        "SCM, CI/CD, SIEM, ITSM, and ChatOps groups are covered." if not missing_groups else f"Missing connector groups: {', '.join(missing_groups)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.certified-connectors.registry-validation.v1",
        "product": "CAVRA",
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "provider_count": len(providers),
        "providers": sorted(providers),
        "checks": checks,
    }


def validate_certified_connectors_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_provider_registry(packet.get("provider_registry", {}), checks)
    _check_provider_groups(packet.get("provider_groups", {}), checks)
    _check_delivery_contracts(packet.get("delivery_contracts", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CERTIFIED_CONNECTORS_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_priority_connector_contract": contract_ready,
        "ready_for_live_priority_connectors": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == CERTIFIED_CONNECTORS_EVIDENCE_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Certified connector evidence packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.certified-connectors.evidence.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    if mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live priority connector evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample priority connector packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live priority connector validation requires evidence_mode=live.")


def _check_provider_registry(registry: dict[str, Any], checks: list[dict[str, str]]) -> None:
    provider_ids = set(registry.get("provider_ids", []))
    missing = sorted(REQUIRED_PRIORITY_CONNECTORS - provider_ids)
    required_flags = {
        "manifests_published": registry.get("manifests_published") is True,
        "certification_packets_generated": registry.get("certification_packets_generated") is True,
        "compatibility_matrix_generated": registry.get("compatibility_matrix_generated") is True,
    }
    if not missing and all(required_flags.values()):
        _add_check(checks, "provider_registry", "pass", "Priority connector registry is complete.")
        return
    missing_fields = [name for name, ok in required_flags.items() if not ok]
    if missing:
        missing_fields.append(f"provider_ids: {', '.join(missing)}")
    _add_check(checks, "provider_registry", "blocker", f"Priority connector registry is missing: {', '.join(missing_fields)}.")


def _check_provider_groups(groups: dict[str, Any], checks: list[dict[str, str]]) -> None:
    missing = sorted(group for group in REQUIRED_CONNECTOR_GROUPS if not groups.get(group))
    if not missing:
        _add_check(checks, "provider_groups", "pass", "Required connector groups are covered.")
    else:
        _add_check(checks, "provider_groups", "blocker", f"Connector groups are missing: {', '.join(missing)}.")


def _check_delivery_contracts(contracts: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = {
        "request_specs_tested": contracts.get("request_specs_tested") is True,
        "redaction_tested": contracts.get("redaction_tested") is True,
        "auth_modes_documented": contracts.get("auth_modes_documented") is True,
        "provider_payloads_supported": contracts.get("provider_payloads_supported") is True,
    }
    if all(required.values()):
        _add_check(checks, "delivery_contracts", "pass", "Priority connector delivery contracts are tested.")
    else:
        missing = [name for name, ok in required.items() if not ok]
        _add_check(checks, "delivery_contracts", "blocker", f"Delivery contracts are missing: {', '.join(missing)}.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = [
        "connector_owner",
        "registry_review_ref",
        "live_sandbox_validation_ref",
        "compatibility_matrix_ref",
        "credential_custody_ref",
    ]
    missing = [field for field in required if not evidence.get(field)]
    if not missing:
        _add_check(checks, "operating_evidence", "pass", "Priority connector operating evidence references are present.")
    else:
        _add_check(checks, "operating_evidence", "blocker", f"Operating evidence is missing: {', '.join(missing)}.")
