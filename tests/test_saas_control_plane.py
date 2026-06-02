from __future__ import annotations

from cavra.licensing.license_client import LocalLicenseClient
from cavra.saas_control_plane import (
    SAAS_CONTROL_PLANE_CONTRACT_VERSION,
    SAAS_CONTROL_PLANE_REQUEST_VERSION,
    SaaSContractError,
    SaaSOperation,
    SaaSResponseStatus,
    build_evidence_export_request,
    build_license_validation_request,
    build_policy_registry_lookup_request,
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
    assert SaaSOperation.EVIDENCE_EXPORT.value in {item["name"] for item in contract["operations"]}


def test_build_tenant_status_request_is_public_safe() -> None:
    request = build_tenant_status_request("tenant-demo", requested_by="console")
    payload = request.to_dict()

    assert payload["schema_version"] == SAAS_CONTROL_PLANE_REQUEST_VERSION
    assert payload["operation"] == "tenant_status"
    assert payload["private_implementation_required"] is True
    assert payload["payload"]["requested_capabilities"] == ["license", "policy_registry", "evidence_export"]


def test_build_license_validation_request_embeds_local_report() -> None:
    license_obj = LocalLicenseClient().load(None)
    report = LocalLicenseClient().validation_report(license_obj)
    request = build_license_validation_request("tenant-demo", report, requested_by="cli")

    payload = request.to_dict()["payload"]

    assert payload["local_validation_report"]["edition"] == "community"
    assert payload["local_validation_report"]["valid"] is True
    assert payload["requested_checks"] == ["signature", "revocation", "subscription_status"]


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
