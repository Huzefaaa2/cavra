from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from cavra.licensing.license_types import LicenseValidationReport


SAAS_CONTROL_PLANE_CONTRACT_VERSION = "cavra.saas_control_plane.contract.v1"
SAAS_CONTROL_PLANE_REQUEST_VERSION = "cavra.saas_control_plane.request.v1"
SAAS_CONTROL_PLANE_RESPONSE_VERSION = "cavra.saas_control_plane.response.v1"


class SaaSContractError(ValueError):
    pass


class SaaSOperation(str, Enum):
    TENANT_STATUS = "tenant_status"
    LICENSE_VALIDATION = "license_validation"
    POLICY_REGISTRY_LOOKUP = "policy_registry_lookup"
    EVIDENCE_EXPORT = "evidence_export"


class SaaSResponseStatus(str, Enum):
    ACCEPTED = "accepted"
    UNAVAILABLE = "unavailable"
    REQUIRES_PRIVATE_SERVICE = "requires_private_service"


SENSITIVE_KEY_PARTS = {
    "api_key",
    "authorization",
    "client_secret",
    "password",
    "private_key",
    "secret",
    "signing_key",
    "token",
    "webhook_secret",
}
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)
EVIDENCE_EXPORT_FORMATS = frozenset({"json", "jsonl", "markdown", "zip"})


@dataclass(frozen=True)
class SaaSControlPlaneRequest:
    operation: SaaSOperation
    tenant_id: str
    requested_by: str
    payload: dict[str, Any]
    correlation_id: str = field(default_factory=lambda: f"saas-{uuid.uuid4().hex[:12]}")
    schema_version: str = SAAS_CONTROL_PLANE_REQUEST_VERSION
    private_implementation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "operation": self.operation.value,
            "tenant_id": self.tenant_id,
            "requested_by": self.requested_by,
            "correlation_id": self.correlation_id,
            "private_implementation_required": self.private_implementation_required,
            "payload": _public_payload(self.payload),
        }


@dataclass(frozen=True)
class SaaSControlPlaneResponse:
    operation: SaaSOperation
    status: SaaSResponseStatus
    message: str
    correlation_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    schema_version: str = SAAS_CONTROL_PLANE_RESPONSE_VERSION
    private_implementation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "operation": self.operation.value,
            "status": self.status.value,
            "message": self.message,
            "correlation_id": self.correlation_id,
            "private_implementation_required": self.private_implementation_required,
            "payload": _public_payload(self.payload),
        }


def build_tenant_status_request(
    tenant_id: str,
    *,
    requested_by: str = "community",
    capabilities: tuple[str, ...] = ("license", "policy_registry", "evidence_export"),
) -> SaaSControlPlaneRequest:
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.TENANT_STATUS,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "requested_capabilities": list(capabilities),
            "public_client_boundary": "status lookup contract only",
        },
    )


def build_license_validation_request(
    tenant_id: str,
    report: LicenseValidationReport,
    *,
    requested_by: str = "community",
) -> SaaSControlPlaneRequest:
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.LICENSE_VALIDATION,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "local_validation_report": report.to_dict(),
            "requested_checks": ["signature", "revocation", "subscription_status"],
            "server_boundary": "real validation is performed by private SaaS or Enterprise services",
        },
    )


def build_policy_registry_lookup_request(
    tenant_id: str,
    policy_refs: tuple[str, ...],
    *,
    requested_by: str = "community",
    labels: dict[str, str] | None = None,
) -> SaaSControlPlaneRequest:
    if not policy_refs:
        raise SaaSContractError("policy_refs must include at least one policy reference")
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.POLICY_REGISTRY_LOOKUP,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "policy_refs": list(policy_refs),
            "labels": labels or {},
            "resolution_boundary": "public request shape only; hosted registry implementation is private",
        },
    )


def build_evidence_export_request(
    tenant_id: str,
    evidence_refs: tuple[str, ...],
    *,
    export_format: str = "json",
    requested_by: str = "community",
    retention_profile: str = "tenant-default",
) -> SaaSControlPlaneRequest:
    if export_format not in EVIDENCE_EXPORT_FORMATS:
        supported = ", ".join(sorted(EVIDENCE_EXPORT_FORMATS))
        raise SaaSContractError(f"export_format must be one of: {supported}")
    if not evidence_refs:
        raise SaaSContractError("evidence_refs must include at least one evidence reference")
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.EVIDENCE_EXPORT,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "evidence_refs": list(evidence_refs),
            "export_format": export_format,
            "retention_profile": retention_profile,
            "export_boundary": "public request shape only; storage and delivery implementation is private",
        },
    )


def build_unavailable_response(request: SaaSControlPlaneRequest) -> SaaSControlPlaneResponse:
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
        message="This operation requires the private CAVRA SaaS Control Plane or Enterprise service.",
        correlation_id=request.correlation_id,
        payload={
            "tenant_id": request.tenant_id,
            "next_step": "See docs/architecture/saas-control-plane-contract.md",
        },
    )


def describe_public_contract() -> dict[str, Any]:
    return {
        "schema_version": SAAS_CONTROL_PLANE_CONTRACT_VERSION,
        "product": "CAVRA",
        "public_repository_boundary": {
            "contains_saas_backend": False,
            "contains_license_service": False,
            "contains_customer_records": False,
            "purpose": "Public-safe client request and response contracts for future private services.",
        },
        "operations": [
            {
                "name": SaaSOperation.TENANT_STATUS.value,
                "request": "tenant identifier and requested capabilities",
                "response": "tenant entitlement and service availability summary",
            },
            {
                "name": SaaSOperation.LICENSE_VALIDATION.value,
                "request": "local validation report and requested server checks",
                "response": "validated entitlement and feature grant summary",
            },
            {
                "name": SaaSOperation.POLICY_REGISTRY_LOOKUP.value,
                "request": "policy references and public labels",
                "response": "policy metadata and downloadable artifact references",
            },
            {
                "name": SaaSOperation.EVIDENCE_EXPORT.value,
                "request": "evidence references, format, and retention profile",
                "response": "export job status and governed artifact references",
            },
        ],
    }


def validate_public_payload(payload: dict[str, Any]) -> None:
    _reject_sensitive_material(payload)


def _public_payload(payload: dict[str, Any]) -> dict[str, Any]:
    _reject_sensitive_material(payload)
    return payload


def _safe_identifier(value: str, *, field_name: str) -> str:
    candidate = str(value).strip()
    if not candidate:
        raise SaaSContractError(f"{field_name} must not be empty")
    _reject_sensitive_material({field_name: candidate})
    return candidate


def _reject_sensitive_material(value: Any, *, path: str = "payload") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            normalized = key_text.lower()
            if any(part in normalized for part in SENSITIVE_KEY_PARTS):
                raise SaaSContractError(f"sensitive field is not allowed in public SaaS contract payload: {path}.{key_text}")
            _reject_sensitive_material(item, path=f"{path}.{key_text}")
    elif isinstance(value, (list, tuple, set)):
        for index, item in enumerate(value):
            _reject_sensitive_material(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        for pattern in SENSITIVE_VALUE_PATTERNS:
            if pattern.search(value):
                raise SaaSContractError(f"sensitive value is not allowed in public SaaS contract payload: {path}")


__all__ = [
    "EVIDENCE_EXPORT_FORMATS",
    "SAAS_CONTROL_PLANE_CONTRACT_VERSION",
    "SAAS_CONTROL_PLANE_REQUEST_VERSION",
    "SAAS_CONTROL_PLANE_RESPONSE_VERSION",
    "SaaSContractError",
    "SaaSControlPlaneRequest",
    "SaaSControlPlaneResponse",
    "SaaSOperation",
    "SaaSResponseStatus",
    "build_evidence_export_request",
    "build_license_validation_request",
    "build_policy_registry_lookup_request",
    "build_tenant_status_request",
    "build_unavailable_response",
    "describe_public_contract",
    "validate_public_payload",
]
