from __future__ import annotations

from cavra.licensing.license_client import LocalLicenseClient
from cavra.saas_control_plane import (
    EntitlementStatusSummary,
    PolicyRegistryReadinessSummary,
    SAAS_CONTROL_PLANE_CONTRACT_VERSION,
    SAAS_CONTROL_PLANE_REQUEST_VERSION,
    SaaSContractError,
    SaaSOperation,
    SaaSResponseStatus,
    build_entitlement_status_request,
    build_entitlement_status_response,
    build_evidence_export_request,
    build_license_validation_request,
    build_policy_registry_readiness_request,
    build_policy_registry_readiness_response,
    build_policy_registry_lookup_request,
    build_tenant_onboarding_request,
    build_tenant_onboarding_unavailable_response,
    build_tenant_status_request,
    build_unavailable_response,
    describe_public_contract,
    validate_public_payload,
)


def test_describe_public_contract_marks_private_boundaries() -> None:
    contract = describe_public_contract()

    assert contract["schema_version"] == SAAS_CONTROL_PLANE_CONTRACT_VERSION
    boundary = contract["public_repository_boundary"]
    assert boundary["contains_saas_backend"] is False
    assert boundary["contains_license_service"] is False
    assert SaaSOperation.ENTITLEMENT_STATUS.value in {item["name"] for item in contract["operations"]}
    assert SaaSOperation.TENANT_ONBOARDING.value in {item["name"] for item in contract["operations"]}
    assert SaaSOperation.POLICY_REGISTRY_READINESS.value in {item["name"] for item in contract["operations"]}
    assert SaaSOperation.EVIDENCE_EXPORT.value in {item["name"] for item in contract["operations"]}


def test_build_tenant_status_request_is_public_safe() -> None:
    request = build_tenant_status_request("tenant-demo", requested_by="console")
    payload = request.to_dict()

    assert payload["schema_version"] == SAAS_CONTROL_PLANE_REQUEST_VERSION
    assert payload["operation"] == "tenant_status"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["requested_capabilities"] == ["license", "policy_registry", "evidence_export"]


def test_build_entitlement_status_request_is_public_safe() -> None:
    request = build_entitlement_status_request(
        "tenant-demo",
        requested_by="console",
        feature_names=("sso", "audit_export"),
    )
    payload = request.to_dict()

    assert payload["operation"] == "entitlement_status"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["feature_names"] == ["sso", "audit_export"]
    assert payload["payload"]["requested_checks"] == ["subscription_status", "license_status", "feature_grants"]


def test_build_entitlement_status_response_serializes_summary() -> None:
    request = build_entitlement_status_request("tenant-demo", requested_by="console", feature_names=("sso",))
    summary = EntitlementStatusSummary(
        tenant_id="tenant-demo",
        entitlement_status="trial",
        subscription_plan="enterprise-trial",
        license_status="valid",
        enabled_features=("sso",),
        locked_features=("ai_remediation",),
        expires_at="2026-07-02T00:00:00Z",
    )

    response = build_entitlement_status_response(request, summary).to_dict()

    assert response["operation"] == "entitlement_status"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["payload"]["summary"]["entitlement_status"] == "trial"
    assert response["payload"]["summary"]["enabled_features"] == ["sso"]
    assert response["payload"]["summary"]["locked_features"] == ["ai_remediation"]
    assert response["payload"]["private_modules_required"] == [
        "billing integration",
        "license service",
        "subscription status",
        "feature entitlement registry",
    ]


def test_entitlement_status_summary_rejects_unknown_status() -> None:
    summary = EntitlementStatusSummary(
        tenant_id="tenant-demo",
        entitlement_status="granted",
        subscription_plan="enterprise",
        license_status="valid",
    )

    try:
        summary.to_dict()
    except SaaSContractError as exc:
        assert "entitlement_status" in str(exc)
    else:
        raise AssertionError("expected unknown entitlement status to be rejected")


def test_build_tenant_onboarding_request_is_public_safe() -> None:
    request = build_tenant_onboarding_request(
        "tenant-demo",
        organization_name="Demo Organization",
        requested_by="sales-engineering",
        contacts={"commercial_owner": "owner@example.invalid"},
    )
    payload = request.to_dict()

    assert payload["operation"] == "tenant_onboarding"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["organization_name"] == "Demo Organization"
    assert payload["payload"]["deployment_model"] == "hosted_saas"
    assert payload["payload"]["requirements"] == [
        "identity_provider",
        "license_validation",
        "policy_registry",
        "audit_store",
        "support_owner",
    ]


def test_build_tenant_onboarding_request_rejects_invalid_deployment_model() -> None:
    try:
        build_tenant_onboarding_request(
            "tenant-demo",
            organization_name="Demo Organization",
            deployment_model="public_demo",
        )
    except SaaSContractError as exc:
        assert "deployment_model" in str(exc)
    else:
        raise AssertionError("expected invalid deployment model to be rejected")


def test_build_tenant_onboarding_request_rejects_sensitive_contact_fields() -> None:
    try:
        build_tenant_onboarding_request(
            "tenant-demo",
            organization_name="Demo Organization",
            contacts={"api_token": "placeholder"},
        )
    except SaaSContractError as exc:
        assert "sensitive field" in str(exc)
    else:
        raise AssertionError("expected sensitive contact field to be rejected")


def test_build_license_validation_request_embeds_local_report() -> None:
    license_obj = LocalLicenseClient().load(None)
    report = LocalLicenseClient().validation_report(license_obj)
    request = build_license_validation_request("tenant-demo", report, requested_by="cli")

    payload = request.to_dict()["payload"]

    assert payload["local_validation_report"]["edition"] == "community"
    assert payload["local_validation_report"]["valid"] is True
    assert payload["requested_checks"] == ["signature", "revocation", "subscription_status"]


def test_policy_registry_readiness_request_is_public_safe() -> None:
    request = build_policy_registry_readiness_request(
        "tenant-demo",
        requested_by="console",
        policy_pack_refs=("starter-policy-1", "starter-policy-2"),
        catalog_scope="tenant-default",
    )
    payload = request.to_dict()

    assert payload["operation"] == "policy_registry_readiness"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["policy_pack_refs"] == ["starter-policy-1", "starter-policy-2"]
    assert payload["payload"]["catalog_scope"] == "tenant-default"
    assert payload["payload"]["required_checks"] == [
        "service_availability",
        "catalog_freshness",
        "policy_pack_versions",
        "artifact_integrity",
        "entitlement_scope",
        "approval_state",
    ]


def test_policy_registry_readiness_request_rejects_empty_checks() -> None:
    try:
        build_policy_registry_readiness_request("tenant-demo", required_checks=())
    except SaaSContractError as exc:
        assert "required_checks" in str(exc)
    else:
        raise AssertionError("expected empty readiness checks to be rejected")


def test_policy_registry_readiness_request_rejects_sensitive_labels() -> None:
    try:
        build_policy_registry_readiness_request("tenant-demo", catalog_scope="ghp_123456789012345678901234567890")
    except SaaSContractError as exc:
        assert "sensitive value" in str(exc)
    else:
        raise AssertionError("expected sensitive catalog scope to be rejected")


def test_policy_registry_readiness_response_serializes_summary() -> None:
    request = build_policy_registry_readiness_request(
        "tenant-demo",
        requested_by="console",
        policy_pack_refs=("starter-policy-1",),
    )
    summary = PolicyRegistryReadinessSummary(
        tenant_id="tenant-demo",
        readiness_status="degraded",
        catalog_status="ready",
        latest_catalog_version="catalog-2026.06.02",
        policy_pack_count=12,
        checked_at="2026-06-02T00:00:00Z",
        blockers=("approval workflow pending",),
    )

    response = build_policy_registry_readiness_response(request, summary).to_dict()

    assert response["operation"] == "policy_registry_readiness"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["payload"]["summary"]["readiness_status"] == "degraded"
    assert response["payload"]["summary"]["catalog_status"] == "ready"
    assert response["payload"]["summary"]["policy_pack_count"] == 12
    assert response["payload"]["summary"]["blockers"] == ["approval workflow pending"]
    assert response["payload"]["private_modules_required"] == [
        "hosted policy registry service",
        "policy-pack artifact store",
        "feature entitlement registry",
        "approval workflow",
        "rollout telemetry",
    ]


def test_policy_registry_readiness_summary_rejects_invalid_state() -> None:
    summary = PolicyRegistryReadinessSummary(
        tenant_id="tenant-demo",
        readiness_status="published",
        catalog_status="ready",
    )

    try:
        summary.to_dict()
    except SaaSContractError as exc:
        assert "readiness_status" in str(exc)
    else:
        raise AssertionError("expected unknown readiness status to be rejected")


def test_policy_registry_readiness_summary_rejects_negative_policy_pack_count() -> None:
    summary = PolicyRegistryReadinessSummary(
        tenant_id="tenant-demo",
        readiness_status="ready",
        catalog_status="ready",
        policy_pack_count=-1,
    )

    try:
        summary.to_dict()
    except SaaSContractError as exc:
        assert "policy_pack_count" in str(exc)
    else:
        raise AssertionError("expected negative policy pack count to be rejected")


def test_policy_registry_lookup_rejects_empty_policy_refs() -> None:
    try:
        build_policy_registry_lookup_request("tenant-demo", ())
    except SaaSContractError as exc:
        assert "policy_refs" in str(exc)
    else:
        raise AssertionError("expected empty policy refs to be rejected")


def test_evidence_export_request_rejects_unknown_format() -> None:
    try:
        build_evidence_export_request("tenant-demo", ("session-123",), export_format="pdf")
    except SaaSContractError as exc:
        assert "export_format" in str(exc)
    else:
        raise AssertionError("expected unsupported export format to be rejected")


def test_public_contract_rejects_sensitive_keys_and_values() -> None:
    for payload in (
        {"client_secret": "placeholder"},
        {"nested": {"token": "placeholder"}},
        {"value": "ghp_123456789012345678901234567890"},
    ):
        try:
            validate_public_payload(payload)
        except SaaSContractError:
            pass
        else:
            raise AssertionError("expected sensitive payload to be rejected")


def test_unavailable_response_points_to_private_service() -> None:
    request = build_evidence_export_request("tenant-demo", ("session-123",), requested_by="console")
    response = build_unavailable_response(request).to_dict()

    assert response["operation"] == "evidence_export"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["correlation_id"] == request.correlation_id
    assert response["private_implementation_required"] is True


def test_tenant_onboarding_unavailable_response_lists_private_modules() -> None:
    request = build_tenant_onboarding_request("tenant-demo", organization_name="Demo Organization")
    response = build_tenant_onboarding_unavailable_response(request).to_dict()

    assert response["operation"] == "tenant_onboarding"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["payload"]["private_modules_required"] == [
        "identity onboarding",
        "license service",
        "policy registry",
        "audit store",
        "support ownership",
    ]
