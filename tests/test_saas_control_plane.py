from __future__ import annotations

from cavra.licensing.license_client import LocalLicenseClient
from cavra.saas_control_plane import (
    CustomerOperatingDashboardSummary,
    EntitlementStatusSummary,
    PolicyRegistryReadinessSummary,
    SAAS_CONTROL_PLANE_CONTRACT_VERSION,
    SAAS_CONTROL_PLANE_REQUEST_VERSION,
    SaaSOperatingAutomationSummary,
    SaaSContractError,
    SaaSOperation,
    SaaSResponseStatus,
    SupportHandoffReadinessSummary,
    TenantAuditStoreOperatingSummary,
    build_customer_operating_dashboard_request,
    build_customer_operating_dashboard_response,
    build_entitlement_status_request,
    build_entitlement_status_response,
    build_evidence_export_request,
    build_license_validation_request,
    build_policy_registry_readiness_request,
    build_policy_registry_readiness_response,
    build_policy_registry_lookup_request,
    build_saas_operating_automation_request,
    build_saas_operating_automation_response,
    build_support_handoff_readiness_request,
    build_support_handoff_readiness_response,
    build_tenant_audit_store_operating_request,
    build_tenant_audit_store_operating_response,
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
    assert SaaSOperation.TENANT_AUDIT_STORE_OPERATING.value in {item["name"] for item in contract["operations"]}
    assert SaaSOperation.CUSTOMER_OPERATING_DASHBOARD.value in {item["name"] for item in contract["operations"]}
    assert SaaSOperation.SUPPORT_HANDOFF_READINESS.value in {item["name"] for item in contract["operations"]}
    assert SaaSOperation.SAAS_OPERATING_AUTOMATION.value in {item["name"] for item in contract["operations"]}
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


def test_tenant_audit_store_operating_request_is_public_safe() -> None:
    request = build_tenant_audit_store_operating_request(
        "tenant-demo",
        requested_by="console",
        retention_profile="standard-365",
        evidence_window="last-24h",
    )
    payload = request.to_dict()

    assert payload["operation"] == "tenant_audit_store_operating"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["retention_profile"] == "standard-365"
    assert payload["payload"]["evidence_window"] == "last-24h"
    assert payload["payload"]["required_checks"] == [
        "store_health",
        "retention_posture",
        "evidence_freshness",
        "export_readiness",
        "immutable_storage",
        "dashboard_visibility",
    ]


def test_tenant_audit_store_operating_request_rejects_empty_checks() -> None:
    try:
        build_tenant_audit_store_operating_request("tenant-demo", required_checks=())
    except SaaSContractError as exc:
        assert "required_checks" in str(exc)
    else:
        raise AssertionError("expected empty audit-store checks to be rejected")


def test_tenant_audit_store_operating_request_rejects_sensitive_values() -> None:
    try:
        build_tenant_audit_store_operating_request(
            "tenant-demo",
            retention_profile="ghp_123456789012345678901234567890",
        )
    except SaaSContractError as exc:
        assert "sensitive value" in str(exc)
    else:
        raise AssertionError("expected sensitive retention profile to be rejected")


def test_tenant_audit_store_operating_response_serializes_summary() -> None:
    request = build_tenant_audit_store_operating_request("tenant-demo", requested_by="console")
    summary = TenantAuditStoreOperatingSummary(
        tenant_id="tenant-demo",
        health_status="ready",
        retention_status="degraded",
        evidence_freshness_status="ready",
        export_status="blocked",
        latest_evidence_at="2026-06-02T00:00:00Z",
        retention_profile="standard-365",
        supported_export_formats=("json", "zip"),
        blockers=("export connector approval pending",),
    )

    response = build_tenant_audit_store_operating_response(request, summary).to_dict()

    assert response["operation"] == "tenant_audit_store_operating"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["payload"]["summary"]["health_status"] == "ready"
    assert response["payload"]["summary"]["retention_status"] == "degraded"
    assert response["payload"]["summary"]["evidence_freshness_status"] == "ready"
    assert response["payload"]["summary"]["export_status"] == "blocked"
    assert response["payload"]["summary"]["supported_export_formats"] == ["json", "zip"]
    assert response["payload"]["summary"]["blockers"] == ["export connector approval pending"]
    assert response["payload"]["private_modules_required"] == [
        "tenant audit store",
        "retention enforcement",
        "evidence freshness monitor",
        "export connector service",
        "operating dashboard",
    ]


def test_tenant_audit_store_operating_summary_rejects_invalid_state() -> None:
    summary = TenantAuditStoreOperatingSummary(
        tenant_id="tenant-demo",
        health_status="healthy",
        retention_status="ready",
        evidence_freshness_status="ready",
        export_status="ready",
    )

    try:
        summary.to_dict()
    except SaaSContractError as exc:
        assert "health_status" in str(exc)
    else:
        raise AssertionError("expected unknown audit-store state to be rejected")


def test_tenant_audit_store_operating_response_requires_matching_request() -> None:
    request = build_policy_registry_readiness_request("tenant-demo")
    summary = TenantAuditStoreOperatingSummary(
        tenant_id="tenant-demo",
        health_status="ready",
        retention_status="ready",
        evidence_freshness_status="ready",
        export_status="ready",
    )

    try:
        build_tenant_audit_store_operating_response(request, summary)
    except SaaSContractError as exc:
        assert "tenant_audit_store_operating" in str(exc)
    else:
        raise AssertionError("expected mismatched request to be rejected")


def test_customer_operating_dashboard_request_is_public_safe() -> None:
    request = build_customer_operating_dashboard_request(
        "tenant-demo",
        requested_by="console",
        dashboard_scope="hosted-saas-operations",
        evidence_window="last-7d",
    )
    payload = request.to_dict()

    assert payload["operation"] == "customer_operating_dashboard"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["dashboard_scope"] == "hosted-saas-operations"
    assert payload["payload"]["evidence_window"] == "last-7d"
    assert payload["payload"]["required_checks"] == [
        "dashboard_visibility",
        "billing_observability",
        "license_service_telemetry",
        "support_handoff",
        "customer_success_health",
        "escalation_readiness",
        "release_acceptance",
    ]


def test_customer_operating_dashboard_request_rejects_empty_checks() -> None:
    try:
        build_customer_operating_dashboard_request("tenant-demo", required_checks=())
    except SaaSContractError as exc:
        assert "required_checks" in str(exc)
    else:
        raise AssertionError("expected empty dashboard checks to be rejected")


def test_customer_operating_dashboard_request_rejects_sensitive_values() -> None:
    try:
        build_customer_operating_dashboard_request(
            "tenant-demo",
            dashboard_scope="ghp_123456789012345678901234567890",
        )
    except SaaSContractError as exc:
        assert "sensitive value" in str(exc)
    else:
        raise AssertionError("expected sensitive dashboard scope to be rejected")


def test_customer_operating_dashboard_response_serializes_summary() -> None:
    request = build_customer_operating_dashboard_request("tenant-demo", requested_by="console")
    summary = CustomerOperatingDashboardSummary(
        tenant_id="tenant-demo",
        dashboard_status="ready",
        billing_status="ready",
        license_service_status="degraded",
        support_handoff_status="ready",
        customer_success_status="ready",
        escalation_status="blocked",
        release_closeout_status="ready",
        latest_dashboard_at="2026-06-02T00:00:00Z",
        dashboard_scope="hosted-saas-operations",
        blockers=("escalation route approval pending",),
    )

    response = build_customer_operating_dashboard_response(request, summary).to_dict()

    assert response["operation"] == "customer_operating_dashboard"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["payload"]["summary"]["dashboard_status"] == "ready"
    assert response["payload"]["summary"]["license_service_status"] == "degraded"
    assert response["payload"]["summary"]["escalation_status"] == "blocked"
    assert response["payload"]["summary"]["blockers"] == ["escalation route approval pending"]
    assert response["payload"]["private_modules_required"] == [
        "billing observability",
        "license-service telemetry",
        "support handoff",
        "customer-success health",
        "escalation routing",
        "release closeout",
        "operating dashboard",
    ]


def test_customer_operating_dashboard_summary_rejects_invalid_state() -> None:
    summary = CustomerOperatingDashboardSummary(
        tenant_id="tenant-demo",
        dashboard_status="visible",
        billing_status="ready",
        license_service_status="ready",
        support_handoff_status="ready",
        customer_success_status="ready",
        escalation_status="ready",
        release_closeout_status="ready",
    )

    try:
        summary.to_dict()
    except SaaSContractError as exc:
        assert "dashboard_status" in str(exc)
    else:
        raise AssertionError("expected unknown dashboard state to be rejected")


def test_customer_operating_dashboard_response_requires_matching_request() -> None:
    request = build_tenant_audit_store_operating_request("tenant-demo")
    summary = CustomerOperatingDashboardSummary(
        tenant_id="tenant-demo",
        dashboard_status="ready",
        billing_status="ready",
        license_service_status="ready",
        support_handoff_status="ready",
        customer_success_status="ready",
        escalation_status="ready",
        release_closeout_status="ready",
    )

    try:
        build_customer_operating_dashboard_response(request, summary)
    except SaaSContractError as exc:
        assert "customer_operating_dashboard" in str(exc)
    else:
        raise AssertionError("expected mismatched request to be rejected")


def test_support_handoff_readiness_request_is_public_safe() -> None:
    request = build_support_handoff_readiness_request(
        "tenant-demo",
        requested_by="console",
        handoff_scope="hosted-saas-support",
        support_tier="enterprise",
    )
    payload = request.to_dict()

    assert payload["operation"] == "support_handoff_readiness"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["handoff_scope"] == "hosted-saas-support"
    assert payload["payload"]["support_tier"] == "enterprise"
    assert payload["payload"]["required_checks"] == [
        "support_owner_assignment",
        "customer_success_owner_assignment",
        "escalation_routing",
        "customer_health_review",
        "handoff_dashboard",
        "release_owner_acceptance",
    ]


def test_support_handoff_readiness_request_rejects_empty_checks() -> None:
    try:
        build_support_handoff_readiness_request("tenant-demo", required_checks=())
    except SaaSContractError as exc:
        assert "required_checks" in str(exc)
    else:
        raise AssertionError("expected empty support handoff checks to be rejected")


def test_support_handoff_readiness_request_rejects_sensitive_values() -> None:
    try:
        build_support_handoff_readiness_request(
            "tenant-demo",
            handoff_scope="xoxb-12345678901234567890",
        )
    except SaaSContractError as exc:
        assert "sensitive value" in str(exc)
    else:
        raise AssertionError("expected sensitive handoff scope to be rejected")


def test_support_handoff_readiness_response_serializes_summary() -> None:
    request = build_support_handoff_readiness_request("tenant-demo", requested_by="console")
    summary = SupportHandoffReadinessSummary(
        tenant_id="tenant-demo",
        support_status="ready",
        customer_success_status="ready",
        escalation_status="degraded",
        health_review_status="ready",
        dashboard_status="blocked",
        support_tier="enterprise",
        handoff_scope="hosted-saas-support",
        blockers=("handoff dashboard approval pending",),
    )

    response = build_support_handoff_readiness_response(request, summary).to_dict()

    assert response["operation"] == "support_handoff_readiness"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["payload"]["summary"]["support_status"] == "ready"
    assert response["payload"]["summary"]["escalation_status"] == "degraded"
    assert response["payload"]["summary"]["dashboard_status"] == "blocked"
    assert response["payload"]["summary"]["blockers"] == ["handoff dashboard approval pending"]
    assert response["payload"]["private_modules_required"] == [
        "support ownership",
        "customer-success ownership",
        "escalation routing",
        "customer health review",
        "handoff dashboard",
        "release owner acceptance",
    ]


def test_support_handoff_readiness_summary_rejects_invalid_state() -> None:
    summary = SupportHandoffReadinessSummary(
        tenant_id="tenant-demo",
        support_status="assigned",
        customer_success_status="ready",
        escalation_status="ready",
        health_review_status="ready",
        dashboard_status="ready",
    )

    try:
        summary.to_dict()
    except SaaSContractError as exc:
        assert "support_status" in str(exc)
    else:
        raise AssertionError("expected unknown support handoff state to be rejected")


def test_support_handoff_readiness_response_requires_matching_request() -> None:
    request = build_tenant_audit_store_operating_request("tenant-demo")
    summary = SupportHandoffReadinessSummary(
        tenant_id="tenant-demo",
        support_status="ready",
        customer_success_status="ready",
        escalation_status="ready",
        health_review_status="ready",
        dashboard_status="ready",
    )

    try:
        build_support_handoff_readiness_response(request, summary)
    except SaaSContractError as exc:
        assert "support_handoff_readiness" in str(exc)
    else:
        raise AssertionError("expected mismatched request to be rejected")


def test_saas_operating_automation_request_is_public_safe() -> None:
    request = build_saas_operating_automation_request(
        "tenant-demo",
        requested_by="console",
        automation_scope="trial-to-paid-customer-scale",
        automation_cadence="daily",
    )
    payload = request.to_dict()

    assert payload["operation"] == "saas_operating_automation"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["automation_scope"] == "trial-to-paid-customer-scale"
    assert payload["payload"]["automation_cadence"] == "daily"
    assert payload["payload"]["required_checks"] == [
        "billing_monitoring",
        "license_telemetry_sync",
        "support_followup",
        "customer_success_review",
        "dashboard_refresh",
        "escalation_drill",
        "closeout_retry",
    ]


def test_saas_operating_automation_request_rejects_empty_checks() -> None:
    try:
        build_saas_operating_automation_request("tenant-demo", required_checks=())
    except SaaSContractError as exc:
        assert "required_checks" in str(exc)
    else:
        raise AssertionError("expected empty SaaS operating automation checks to be rejected")


def test_saas_operating_automation_request_rejects_sensitive_values() -> None:
    try:
        build_saas_operating_automation_request(
            "tenant-demo",
            automation_cadence="ghp_123456789012345678901234567890",
        )
    except SaaSContractError as exc:
        assert "sensitive value" in str(exc)
    else:
        raise AssertionError("expected sensitive automation cadence to be rejected")


def test_saas_operating_automation_response_serializes_summary() -> None:
    request = build_saas_operating_automation_request("tenant-demo", requested_by="console")
    summary = SaaSOperatingAutomationSummary(
        tenant_id="tenant-demo",
        automation_status="scheduled",
        billing_monitoring_status="enabled",
        license_telemetry_status="automated",
        support_followup_status="ready",
        customer_success_review_status="scheduled",
        dashboard_refresh_status="automated",
        escalation_drill_status="blocked",
        closeout_retry_status="enabled",
        automation_scope="trial-to-paid-customer-scale",
        automation_cadence="daily",
        blockers=("escalation drill owner pending",),
    )

    response = build_saas_operating_automation_response(request, summary).to_dict()

    assert response["operation"] == "saas_operating_automation"
    assert response["status"] == SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE.value
    assert response["payload"]["summary"]["automation_status"] == "scheduled"
    assert response["payload"]["summary"]["license_telemetry_status"] == "automated"
    assert response["payload"]["summary"]["escalation_drill_status"] == "blocked"
    assert response["payload"]["summary"]["blockers"] == ["escalation drill owner pending"]
    assert response["payload"]["private_modules_required"] == [
        "billing monitoring",
        "license telemetry sync",
        "support follow-up",
        "customer-success review",
        "dashboard refresh automation",
        "escalation drill scheduler",
        "closeout retry automation",
    ]


def test_saas_operating_automation_summary_rejects_invalid_state() -> None:
    summary = SaaSOperatingAutomationSummary(
        tenant_id="tenant-demo",
        automation_status="running",
        billing_monitoring_status="ready",
        license_telemetry_status="ready",
        support_followup_status="ready",
        customer_success_review_status="ready",
        dashboard_refresh_status="ready",
        escalation_drill_status="ready",
        closeout_retry_status="ready",
    )

    try:
        summary.to_dict()
    except SaaSContractError as exc:
        assert "automation_status" in str(exc)
    else:
        raise AssertionError("expected unknown SaaS operating automation state to be rejected")


def test_saas_operating_automation_response_requires_matching_request() -> None:
    request = build_customer_operating_dashboard_request("tenant-demo")
    summary = SaaSOperatingAutomationSummary(
        tenant_id="tenant-demo",
        automation_status="ready",
        billing_monitoring_status="ready",
        license_telemetry_status="ready",
        support_followup_status="ready",
        customer_success_review_status="ready",
        dashboard_refresh_status="ready",
        escalation_drill_status="ready",
        closeout_retry_status="ready",
    )

    try:
        build_saas_operating_automation_response(request, summary)
    except SaaSContractError as exc:
        assert "saas_operating_automation" in str(exc)
    else:
        raise AssertionError("expected mismatched request to be rejected")


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
