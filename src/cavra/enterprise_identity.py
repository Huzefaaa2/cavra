from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_ENTERPRISE_ROLES = {
    "ciso",
    "security_operator",
    "platform_security",
    "model_owner",
    "auditor",
    "break_glass_approver",
}

REQUIRED_ABAC_ATTRIBUTES = {
    "tenant_id",
    "workspace_id",
    "environment",
    "repository",
    "model_owner_ref",
    "data_classification",
}

REQUIRED_CLAIMS = {
    "sub",
    "email",
    "groups",
    "roles",
    "tenant_id",
    "workspace_id",
}

ENTERPRISE_LIVE_IDENTITY_SCHEMA_VERSION = "cavra.enterprise.identity_live_validation.v1"

REQUIRED_LIVE_IDENTITY_CHECKS = {
    "oidc_token_validation",
    "rbac_group_mapping",
    "abac_runtime_scope",
    "scim_group_sync",
    "scim_deprovisioning",
    "break_glass_audit",
    "audit_evidence_retention",
}

SECRET_FIELD_MARKERS = {
    "access_token",
    "api_key",
    "bearer",
    "client_secret",
    "password",
    "private_key",
    "saml_certificate",
    "saml_private_key",
    "scim_token",
    "secret",
    "token",
}


def default_enterprise_identity_policy() -> dict[str, Any]:
    return {
        "schema_version": "cavra.enterprise.identity_policy.v1",
        "product": "CAVRA",
        "identity_providers": {
            "oidc": {
                "status": "supported",
                "config_env": "CAVRA_APPROVAL_OIDC_CONFIG",
                "required_claims": sorted(REQUIRED_CLAIMS),
                "supported_providers": ["Microsoft Entra ID", "Okta", "OIDC-compliant IdP"],
            },
            "saml": {
                "status": "bridge_required",
                "pattern": "SAML assertion is normalized by the IdP, gateway, or private Enterprise bridge into the CAVRA OIDC claim contract.",
                "required_bridge_outputs": sorted(REQUIRED_CLAIMS),
            },
            "scim": {
                "status": "private_enterprise_sync_contract",
                "required_controls": [
                    "group-to-role synchronization",
                    "deprovisioning within 60 minutes",
                    "tenant and workspace membership synchronization",
                    "audit record for create, update, disable, and delete events",
                ],
            },
        },
        "rbac": {
            "config_env": "CAVRA_APPROVAL_RBAC_FILE",
            "required_roles": sorted(REQUIRED_ENTERPRISE_ROLES),
            "role_groups": {
                "ciso": ["CAVRA-CISO"],
                "security_operator": ["CAVRA-Security-Operations"],
                "platform_security": ["CAVRA-Platform-Security"],
                "model_owner": ["CAVRA-Model-Owners"],
                "auditor": ["CAVRA-Auditors"],
                "break_glass_approver": ["Change Advisory Board"],
            },
        },
        "abac": {
            "required_attributes": sorted(REQUIRED_ABAC_ATTRIBUTES),
            "resource_boundaries": [
                "tenant_id",
                "workspace_id",
                "repository",
                "environment",
                "model_owner_ref",
                "data_classification",
            ],
        },
        "break_glass": {
            "required_role": "break_glass_approver",
            "required_group": "Change Advisory Board",
            "reason_required": True,
            "external_reference_required": True,
            "max_ttl_hours": 4,
            "audit_event_required": True,
        },
        "console": {
            "mutation_endpoints_require_verified_actor": True,
            "session_endpoint": "/console/session",
            "security_boundary_endpoint": "/console/security-boundary",
        },
    }


def load_enterprise_identity_policy(path: Path | None) -> dict[str, Any]:
    if path is None:
        return default_enterprise_identity_policy()
    if not path.exists():
        raise FileNotFoundError(f"enterprise identity policy file not found: {path}")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install PyYAML to load YAML enterprise identity policies.") from exc
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("enterprise identity policy file must contain an object")
    return merge_enterprise_identity_policy(payload)


def merge_enterprise_identity_policy(policy: dict[str, Any]) -> dict[str, Any]:
    merged = default_enterprise_identity_policy()
    _deep_merge(merged, policy)
    return merged


def build_enterprise_identity_contract(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    identity_policy = merge_enterprise_identity_policy(policy or {})
    return {
        "schema_version": "cavra.enterprise.identity_contract.v1",
        "product": "CAVRA",
        "purpose": "Public-safe Enterprise identity, RBAC, ABAC, SCIM, SAML bridge, and break-glass contract.",
        "policy": identity_policy,
        "public_boundaries": [
            "Public CAVRA validates the policy contract, OIDC/JWKS token shape, RBAC mappings, and console mutation boundaries.",
            "Private Managed or Enterprise services own SAML bridge adapters, SCIM sync workers, tenant directory storage, and IdP-specific automation.",
            "Customer secrets, directory exports, user records, SAML certificates, SCIM bearer tokens, and tenant membership payloads must not be committed to this repository.",
        ],
    }


def build_enterprise_identity_readiness(
    *,
    oidc_configured: bool,
    rbac_configured: bool,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity_policy = merge_enterprise_identity_policy(policy or {})
    checks = _identity_policy_checks(identity_policy, oidc_configured=oidc_configured, rbac_configured=rbac_configured)
    blockers = [check for check in checks if check["status"] == "blocker"]
    warnings = [check for check in checks if check["status"] == "warn"]
    status = "blocked" if blockers else "contract_ready" if warnings else "ready"
    return {
        "schema_version": "cavra.enterprise.identity_readiness.v1",
        "product": "CAVRA",
        "status": status,
        "ready_for_enterprise_identity": not blockers,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
        "next_controls": [
            "Run console session tests with a signed IdP token.",
            "Verify SCIM deprovisioning evidence in the private Enterprise tenant directory.",
            "Run break-glass audit tests with a Change Advisory Board actor.",
            "Bind R2.2 tenant isolation to the same tenant_id and workspace_id claims.",
        ],
    }


def enterprise_actor_claims_context(claims: dict[str, Any], *, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    identity_policy = merge_enterprise_identity_policy(policy or {})
    roles = _string_list(claims.get("roles"))
    groups = _string_list(claims.get("groups"))
    role_groups = identity_policy.get("rbac", {}).get("role_groups", {})
    mapped_roles = set(roles)
    for role, role_group_names in role_groups.items():
        if set(groups) & set(_string_list(role_group_names)):
            mapped_roles.add(str(role))
    return {
        "actor": claims.get("email") or claims.get("preferred_username") or claims.get("sub") or "unknown",
        "subject": claims.get("sub"),
        "tenant_id": claims.get("tenant_id") or claims.get("tid"),
        "workspace_id": claims.get("workspace_id") or claims.get("workspace"),
        "groups": sorted(groups),
        "roles": sorted(mapped_roles),
        "repository": claims.get("repository") or claims.get("repo"),
        "environment": claims.get("environment"),
        "model_owner_ref": claims.get("model_owner_ref"),
        "data_classification": claims.get("data_classification"),
    }


def actor_has_enterprise_scope(
    actor_context: dict[str, Any],
    *,
    action: str,
    resource: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> bool:
    identity_policy = merge_enterprise_identity_policy(policy or {})
    action_roles = {
        "approve_runtime_action": {"security_operator", "platform_security"},
        "approve_model_artifact": {"model_owner", "ciso"},
        "read_audit": {"auditor", "ciso", "security_operator"},
        "break_glass": {"break_glass_approver"},
    }.get(action, set())
    roles = set(_string_list(actor_context.get("roles")))
    if action_roles and not roles & action_roles:
        return False
    for boundary in identity_policy.get("abac", {}).get("resource_boundaries", []):
        if boundary in {"tenant_id", "workspace_id"} and resource.get(boundary):
            if str(actor_context.get(boundary) or "") != str(resource.get(boundary)):
                return False
    return True


def validate_enterprise_live_identity_packet(packet: dict[str, Any]) -> dict[str, Any]:
    checks = _live_identity_packet_checks(packet)
    blockers = [check for check in checks if check["status"] == "blocker"]
    warnings = [check for check in checks if check["status"] == "warn"]
    return {
        "schema_version": "cavra.enterprise.identity_live_validation_result.v1",
        "product": "CAVRA",
        "packet_schema_version": packet.get("schema_version") if isinstance(packet, dict) else None,
        "packet_id": packet.get("packet_id") if isinstance(packet, dict) else None,
        "ready_for_live_enterprise_identity": not blockers,
        "status": "blocked" if blockers else "ready" if not warnings else "ready_with_warnings",
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
        "next_controls": [
            "Attach this packet to the R2.1 identity evidence room.",
            "Rerun after every IdP claim, SCIM worker, RBAC, ABAC, or break-glass control change.",
            "Use the same tenant_id and workspace_id evidence as input to R2.2 tenant isolation validation.",
        ],
    }


def load_enterprise_live_identity_packet(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"enterprise live identity packet not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("enterprise live identity packet must contain a JSON object")
    return payload


def _live_identity_packet_checks(packet: dict[str, Any]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    if not isinstance(packet, dict):
        return [_check("packet_shape", "blocker", "Packet must be a JSON object.")]
    schema_version = packet.get("schema_version")
    checks.append(
        _check(
            "packet_schema",
            "pass" if schema_version == ENTERPRISE_LIVE_IDENTITY_SCHEMA_VERSION else "blocker",
            "Live identity packet schema version is correct."
            if schema_version == ENTERPRISE_LIVE_IDENTITY_SCHEMA_VERSION
            else f"Live identity packet schema must be {ENTERPRISE_LIVE_IDENTITY_SCHEMA_VERSION}.",
        )
    )
    checks.extend(_packet_required_field_checks(packet))
    checks.extend(_packet_secret_redaction_checks(packet))
    checks.extend(_packet_environment_checks(packet))
    checks.extend(_packet_evidence_checks(packet))
    checks.extend(_packet_control_checks(packet))
    return checks


def _packet_required_field_checks(packet: dict[str, Any]) -> list[dict[str, str]]:
    required_fields = ["packet_id", "generated_at", "environment", "evidence", "checks"]
    missing = [field for field in required_fields if field not in packet]
    return [
        _check(
            "packet_required_fields",
            "pass" if not missing else "blocker",
            "Packet includes required identity validation fields."
            if not missing
            else f"Packet missing required fields: {', '.join(missing)}.",
        )
    ]


def _packet_secret_redaction_checks(packet: dict[str, Any]) -> list[dict[str, str]]:
    secret_paths = _find_secret_like_paths(packet)
    return [
        _check(
            "secret_redaction",
            "pass" if not secret_paths else "blocker",
            "Packet does not include token, password, certificate, private key, or secret fields."
            if not secret_paths
            else f"Packet contains secret-like fields: {', '.join(secret_paths[:5])}.",
        )
    ]


def _packet_environment_checks(packet: dict[str, Any]) -> list[dict[str, str]]:
    environment = packet.get("environment", {})
    if not isinstance(environment, dict):
        return [_check("environment_shape", "blocker", "Packet environment must be an object.")]
    required = ["validation_mode", "identity_provider", "tenant_id", "workspace_id", "issuer", "repository"]
    missing = [field for field in required if not environment.get(field)]
    checks = [
        _check(
            "environment_contract",
            "pass" if not missing else "blocker",
            "Environment includes provider, issuer, tenant, workspace, and repository context."
            if not missing
            else f"Environment missing: {', '.join(missing)}.",
        )
    ]
    checks.append(
        _check(
            "live_validation_mode",
            "pass" if environment.get("validation_mode") == "live" else "blocker",
            "Packet was produced from a live IdP and SCIM validation run."
            if environment.get("validation_mode") == "live"
            else "Packet validation_mode must be live before R2.1 can close.",
        )
    )
    return checks


def _packet_evidence_checks(packet: dict[str, Any]) -> list[dict[str, str]]:
    evidence = packet.get("evidence", {})
    if not isinstance(evidence, dict):
        return [_check("evidence_shape", "blocker", "Packet evidence must be an object.")]
    evidence_refs = _string_list(evidence.get("evidence_refs"))
    redaction_status = str(evidence.get("redaction_status", "")).lower()
    return [
        _check(
            "evidence_refs",
            "pass" if evidence_refs else "blocker",
            "Packet includes public-safe evidence references."
            if evidence_refs
            else "Packet must include at least one public-safe evidence reference.",
        ),
        _check(
            "evidence_redaction",
            "pass" if redaction_status in {"public_safe", "redacted"} else "blocker",
            "Packet evidence is marked public-safe or redacted."
            if redaction_status in {"public_safe", "redacted"}
            else "Packet evidence must be marked public_safe or redacted.",
        ),
    ]


def _packet_control_checks(packet: dict[str, Any]) -> list[dict[str, str]]:
    control_checks = packet.get("checks", [])
    if not isinstance(control_checks, list):
        return [_check("control_checks_shape", "blocker", "Packet checks must be a list.")]
    check_by_id = {str(item.get("check_id")): item for item in control_checks if isinstance(item, dict)}
    missing = sorted(REQUIRED_LIVE_IDENTITY_CHECKS - set(check_by_id))
    checks = [
        _check(
            "required_live_identity_checks",
            "pass" if not missing else "blocker",
            "Packet includes all required live identity checks."
            if not missing
            else f"Packet missing live identity checks: {', '.join(missing)}.",
        )
    ]
    for check_id in sorted(REQUIRED_LIVE_IDENTITY_CHECKS & set(check_by_id)):
        item = check_by_id[check_id]
        status = str(item.get("status", "")).lower()
        evidence_ref = item.get("evidence_ref")
        checks.append(
            _check(
                f"live_identity_{check_id}",
                "pass" if status == "pass" and evidence_ref else "blocker",
                f"{check_id} passed with evidence reference."
                if status == "pass" and evidence_ref
                else f"{check_id} must pass and include evidence_ref.",
            )
        )
    scim_deprovisioning = check_by_id.get("scim_deprovisioning", {})
    metrics = scim_deprovisioning.get("metrics", {}) if isinstance(scim_deprovisioning, dict) else {}
    sla_minutes = metrics.get("deprovisioning_sla_minutes") if isinstance(metrics, dict) else None
    checks.append(
        _check(
            "scim_deprovisioning_sla",
            "pass" if isinstance(sla_minutes, int) and sla_minutes <= 60 else "blocker",
            "SCIM deprovisioning evidence meets the 60 minute SLA."
            if isinstance(sla_minutes, int) and sla_minutes <= 60
            else "SCIM deprovisioning must include deprovisioning_sla_minutes <= 60.",
        )
    )
    return checks


def _find_secret_like_paths(value: Any, *, prefix: str = "$") -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{prefix}.{key}"
            normalized_key = str(key).lower()
            if any(marker in normalized_key for marker in SECRET_FIELD_MARKERS):
                paths.append(child_path)
            paths.extend(_find_secret_like_paths(child, prefix=child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            paths.extend(_find_secret_like_paths(child, prefix=f"{prefix}[{index}]"))
    return paths


def _identity_policy_checks(
    policy: dict[str, Any],
    *,
    oidc_configured: bool,
    rbac_configured: bool,
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    checks.append(
        _check(
            "oidc_runtime_config",
            "pass" if oidc_configured else "warn",
            "OIDC/JWKS runtime config is available." if oidc_configured else "OIDC/JWKS runtime config is not set in this process.",
        )
    )
    checks.append(
        _check(
            "rbac_runtime_config",
            "pass" if rbac_configured else "warn",
            "RBAC runtime config is available." if rbac_configured else "RBAC runtime config is not set in this process.",
        )
    )
    oidc_claims = set(_string_list(policy.get("identity_providers", {}).get("oidc", {}).get("required_claims")))
    missing_claims = REQUIRED_CLAIMS - oidc_claims
    checks.append(
        _check(
            "oidc_claim_contract",
            "pass" if not missing_claims else "blocker",
            "OIDC claim contract covers enterprise identity claims."
            if not missing_claims
            else f"OIDC claim contract missing: {', '.join(sorted(missing_claims))}",
        )
    )
    saml_outputs = set(
        _string_list(policy.get("identity_providers", {}).get("saml", {}).get("required_bridge_outputs"))
    )
    missing_saml_outputs = REQUIRED_CLAIMS - saml_outputs
    checks.append(
        _check(
            "saml_bridge_contract",
            "pass" if not missing_saml_outputs else "blocker",
            "SAML bridge contract normalizes SAML assertions into the CAVRA claim contract."
            if not missing_saml_outputs
            else f"SAML bridge contract missing: {', '.join(sorted(missing_saml_outputs))}",
        )
    )
    scim_controls = set(_string_list(policy.get("identity_providers", {}).get("scim", {}).get("required_controls")))
    checks.append(
        _check(
            "scim_lifecycle_contract",
            "pass" if len(scim_controls) >= 4 else "blocker",
            "SCIM lifecycle contract covers group sync, deprovisioning, tenant/workspace membership, and audit events."
            if len(scim_controls) >= 4
            else "SCIM lifecycle contract is incomplete.",
        )
    )
    roles = set(_string_list(policy.get("rbac", {}).get("required_roles")))
    missing_roles = REQUIRED_ENTERPRISE_ROLES - roles
    checks.append(
        _check(
            "rbac_roles",
            "pass" if not missing_roles else "blocker",
            "RBAC roles cover security, CISO, model owner, auditor, and break-glass personas."
            if not missing_roles
            else f"RBAC roles missing: {', '.join(sorted(missing_roles))}",
        )
    )
    abac_attributes = set(_string_list(policy.get("abac", {}).get("required_attributes")))
    missing_attributes = REQUIRED_ABAC_ATTRIBUTES - abac_attributes
    checks.append(
        _check(
            "abac_attributes",
            "pass" if not missing_attributes else "blocker",
            "ABAC attributes cover tenant, workspace, environment, repository, model owner, and data classification."
            if not missing_attributes
            else f"ABAC attributes missing: {', '.join(sorted(missing_attributes))}",
        )
    )
    break_glass = policy.get("break_glass", {})
    break_glass_ok = (
        break_glass.get("required_role") == "break_glass_approver"
        and break_glass.get("reason_required") is True
        and break_glass.get("external_reference_required") is True
        and int(break_glass.get("max_ttl_hours", 0)) <= 4
        and break_glass.get("audit_event_required") is True
    )
    checks.append(
        _check(
            "break_glass_controls",
            "pass" if break_glass_ok else "blocker",
            "Break-glass requires CAB role, reason, external reference, short TTL, and audit evidence."
            if break_glass_ok
            else "Break-glass control contract is incomplete.",
        )
    )
    return checks


def _check(check_id: str, status: str, message: str) -> dict[str, str]:
    return {"check_id": check_id, "status": status, "message": message}


def _deep_merge(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_merge(target[key], value)
        else:
            target[key] = value


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value]
    return [str(value)]
