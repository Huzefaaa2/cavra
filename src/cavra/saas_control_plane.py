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
    ENTITLEMENT_STATUS = "entitlement_status"
    TENANT_ONBOARDING = "tenant_onboarding"
    TENANT_STATUS = "tenant_status"
    LICENSE_VALIDATION = "license_validation"
    POLICY_REGISTRY_READINESS = "policy_registry_readiness"
    POLICY_REGISTRY_LOOKUP = "policy_registry_lookup"
    TENANT_AUDIT_STORE_OPERATING = "tenant_audit_store_operating"
    CUSTOMER_OPERATING_DASHBOARD = "customer_operating_dashboard"
    SUPPORT_HANDOFF_READINESS = "support_handoff_readiness"
    SAAS_OPERATING_AUTOMATION = "saas_operating_automation"
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
TENANT_DEPLOYMENT_MODELS = frozenset({"hosted_saas", "self_hosted_enterprise", "hybrid"})
TENANT_ONBOARDING_REQUIREMENTS = (
    "identity_provider",
    "license_validation",
    "policy_registry",
    "audit_store",
    "support_owner",
)
ENTITLEMENT_STATUSES = frozenset({"active", "trial", "suspended", "expired", "missing", "unknown"})
POLICY_REGISTRY_READINESS_CHECKS = (
    "service_availability",
    "catalog_freshness",
    "policy_pack_versions",
    "artifact_integrity",
    "entitlement_scope",
    "approval_state",
)
POLICY_REGISTRY_READINESS_STATUSES = frozenset({"ready", "degraded", "blocked", "unknown"})
TENANT_AUDIT_STORE_OPERATING_CHECKS = (
    "store_health",
    "retention_posture",
    "evidence_freshness",
    "export_readiness",
    "immutable_storage",
    "dashboard_visibility",
)
TENANT_AUDIT_STORE_OPERATING_STATUSES = frozenset({"ready", "degraded", "blocked", "unknown"})
CUSTOMER_OPERATING_DASHBOARD_CHECKS = (
    "dashboard_visibility",
    "billing_observability",
    "license_service_telemetry",
    "support_handoff",
    "customer_success_health",
    "escalation_readiness",
    "release_acceptance",
)
CUSTOMER_OPERATING_DASHBOARD_STATUSES = frozenset({"ready", "degraded", "blocked", "unknown"})
SUPPORT_HANDOFF_READINESS_CHECKS = (
    "support_owner_assignment",
    "customer_success_owner_assignment",
    "escalation_routing",
    "customer_health_review",
    "handoff_dashboard",
    "release_owner_acceptance",
)
SUPPORT_HANDOFF_READINESS_STATUSES = frozenset({"ready", "degraded", "blocked", "unknown"})
SAAS_OPERATING_AUTOMATION_CHECKS = (
    "billing_monitoring",
    "license_telemetry_sync",
    "support_followup",
    "customer_success_review",
    "dashboard_refresh",
    "escalation_drill",
    "closeout_retry",
)
SAAS_OPERATING_AUTOMATION_STATUSES = frozenset(
    {"ready", "scheduled", "enabled", "automated", "blocked", "unknown"}
)


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


@dataclass(frozen=True)
class EntitlementStatusSummary:
    tenant_id: str
    entitlement_status: str
    subscription_plan: str
    license_status: str
    enabled_features: tuple[str, ...] = field(default_factory=tuple)
    locked_features: tuple[str, ...] = field(default_factory=tuple)
    expires_at: str | None = None
    private_validation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        _validate_entitlement_status(self.entitlement_status)
        _reject_sensitive_material(
            {
                "subscription_plan": self.subscription_plan,
                "license_status": self.license_status,
                "enabled_features": list(self.enabled_features),
                "locked_features": list(self.locked_features),
                "expires_at": self.expires_at,
            }
        )
        return {
            "tenant_id": _safe_identifier(self.tenant_id, field_name="tenant_id"),
            "entitlement_status": self.entitlement_status,
            "subscription_plan": self.subscription_plan,
            "license_status": self.license_status,
            "enabled_features": list(self.enabled_features),
            "locked_features": list(self.locked_features),
            "expires_at": self.expires_at,
            "private_validation_required": self.private_validation_required,
            "billing_boundary": "billing and subscription verification are private service responsibilities",
        }


@dataclass(frozen=True)
class PolicyRegistryReadinessSummary:
    tenant_id: str
    readiness_status: str
    catalog_status: str
    latest_catalog_version: str | None = None
    policy_pack_count: int = 0
    checked_at: str | None = None
    blockers: tuple[str, ...] = field(default_factory=tuple)
    private_validation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        _validate_policy_registry_readiness_status(self.readiness_status, field_name="readiness_status")
        _validate_policy_registry_readiness_status(self.catalog_status, field_name="catalog_status")
        if self.policy_pack_count < 0:
            raise SaaSContractError("policy_pack_count must be greater than or equal to 0")
        _reject_sensitive_material(
            {
                "latest_catalog_version": self.latest_catalog_version,
                "checked_at": self.checked_at,
                "blockers": list(self.blockers),
            }
        )
        return {
            "tenant_id": _safe_identifier(self.tenant_id, field_name="tenant_id"),
            "readiness_status": self.readiness_status,
            "catalog_status": self.catalog_status,
            "latest_catalog_version": self.latest_catalog_version,
            "policy_pack_count": self.policy_pack_count,
            "checked_at": self.checked_at,
            "blockers": list(self.blockers),
            "private_validation_required": self.private_validation_required,
            "registry_boundary": "hosted registry availability, artifact delivery, and tenant catalog validation are private service responsibilities",
        }


@dataclass(frozen=True)
class TenantAuditStoreOperatingSummary:
    tenant_id: str
    health_status: str
    retention_status: str
    evidence_freshness_status: str
    export_status: str
    latest_evidence_at: str | None = None
    retention_profile: str = "tenant-default"
    supported_export_formats: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    private_validation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        _validate_audit_store_operating_status(self.health_status, field_name="health_status")
        _validate_audit_store_operating_status(self.retention_status, field_name="retention_status")
        _validate_audit_store_operating_status(
            self.evidence_freshness_status,
            field_name="evidence_freshness_status",
        )
        _validate_audit_store_operating_status(self.export_status, field_name="export_status")
        _reject_sensitive_material(
            {
                "latest_evidence_at": self.latest_evidence_at,
                "retention_profile": self.retention_profile,
                "supported_export_formats": list(self.supported_export_formats),
                "blockers": list(self.blockers),
            }
        )
        return {
            "tenant_id": _safe_identifier(self.tenant_id, field_name="tenant_id"),
            "health_status": self.health_status,
            "retention_status": self.retention_status,
            "evidence_freshness_status": self.evidence_freshness_status,
            "export_status": self.export_status,
            "latest_evidence_at": self.latest_evidence_at,
            "retention_profile": self.retention_profile,
            "supported_export_formats": list(self.supported_export_formats),
            "blockers": list(self.blockers),
            "private_validation_required": self.private_validation_required,
            "audit_store_boundary": "tenant archive storage, retention enforcement, export connectors, and customer evidence remain private service responsibilities",
        }


@dataclass(frozen=True)
class CustomerOperatingDashboardSummary:
    tenant_id: str
    dashboard_status: str
    billing_status: str
    license_service_status: str
    support_handoff_status: str
    customer_success_status: str
    escalation_status: str
    release_closeout_status: str
    latest_dashboard_at: str | None = None
    dashboard_scope: str = "tenant-operating"
    blockers: tuple[str, ...] = field(default_factory=tuple)
    private_validation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        _validate_customer_operating_dashboard_status(self.dashboard_status, field_name="dashboard_status")
        _validate_customer_operating_dashboard_status(self.billing_status, field_name="billing_status")
        _validate_customer_operating_dashboard_status(
            self.license_service_status,
            field_name="license_service_status",
        )
        _validate_customer_operating_dashboard_status(
            self.support_handoff_status,
            field_name="support_handoff_status",
        )
        _validate_customer_operating_dashboard_status(
            self.customer_success_status,
            field_name="customer_success_status",
        )
        _validate_customer_operating_dashboard_status(self.escalation_status, field_name="escalation_status")
        _validate_customer_operating_dashboard_status(
            self.release_closeout_status,
            field_name="release_closeout_status",
        )
        _reject_sensitive_material(
            {
                "latest_dashboard_at": self.latest_dashboard_at,
                "dashboard_scope": self.dashboard_scope,
                "blockers": list(self.blockers),
            }
        )
        return {
            "tenant_id": _safe_identifier(self.tenant_id, field_name="tenant_id"),
            "dashboard_status": self.dashboard_status,
            "billing_status": self.billing_status,
            "license_service_status": self.license_service_status,
            "support_handoff_status": self.support_handoff_status,
            "customer_success_status": self.customer_success_status,
            "escalation_status": self.escalation_status,
            "release_closeout_status": self.release_closeout_status,
            "latest_dashboard_at": self.latest_dashboard_at,
            "dashboard_scope": self.dashboard_scope,
            "blockers": list(self.blockers),
            "private_validation_required": self.private_validation_required,
            "dashboard_boundary": (
                "customer operating dashboards, provider telemetry, support systems, "
                "and customer records remain private service responsibilities"
            ),
        }


@dataclass(frozen=True)
class SupportHandoffReadinessSummary:
    tenant_id: str
    support_status: str
    customer_success_status: str
    escalation_status: str
    health_review_status: str
    dashboard_status: str
    support_tier: str = "enterprise"
    handoff_scope: str = "hosted-saas-support"
    blockers: tuple[str, ...] = field(default_factory=tuple)
    private_validation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        _validate_support_handoff_readiness_status(self.support_status, field_name="support_status")
        _validate_support_handoff_readiness_status(
            self.customer_success_status,
            field_name="customer_success_status",
        )
        _validate_support_handoff_readiness_status(self.escalation_status, field_name="escalation_status")
        _validate_support_handoff_readiness_status(self.health_review_status, field_name="health_review_status")
        _validate_support_handoff_readiness_status(self.dashboard_status, field_name="dashboard_status")
        _reject_sensitive_material(
            {
                "support_tier": self.support_tier,
                "handoff_scope": self.handoff_scope,
                "blockers": list(self.blockers),
            }
        )
        return {
            "tenant_id": _safe_identifier(self.tenant_id, field_name="tenant_id"),
            "support_status": self.support_status,
            "customer_success_status": self.customer_success_status,
            "escalation_status": self.escalation_status,
            "health_review_status": self.health_review_status,
            "dashboard_status": self.dashboard_status,
            "support_tier": self.support_tier,
            "handoff_scope": self.handoff_scope,
            "blockers": list(self.blockers),
            "private_validation_required": self.private_validation_required,
            "handoff_boundary": (
                "support queues, customer-success notes, customer health records, "
                "escalation connectors, and dashboard systems remain private service responsibilities"
            ),
        }


@dataclass(frozen=True)
class SaaSOperatingAutomationSummary:
    tenant_id: str
    automation_status: str
    billing_monitoring_status: str
    license_telemetry_status: str
    support_followup_status: str
    customer_success_review_status: str
    dashboard_refresh_status: str
    escalation_drill_status: str
    closeout_retry_status: str
    automation_scope: str = "trial-to-paid-customer-scale"
    automation_cadence: str = "daily"
    blockers: tuple[str, ...] = field(default_factory=tuple)
    private_validation_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        _validate_saas_operating_automation_status(self.automation_status, field_name="automation_status")
        _validate_saas_operating_automation_status(
            self.billing_monitoring_status,
            field_name="billing_monitoring_status",
        )
        _validate_saas_operating_automation_status(
            self.license_telemetry_status,
            field_name="license_telemetry_status",
        )
        _validate_saas_operating_automation_status(
            self.support_followup_status,
            field_name="support_followup_status",
        )
        _validate_saas_operating_automation_status(
            self.customer_success_review_status,
            field_name="customer_success_review_status",
        )
        _validate_saas_operating_automation_status(
            self.dashboard_refresh_status,
            field_name="dashboard_refresh_status",
        )
        _validate_saas_operating_automation_status(
            self.escalation_drill_status,
            field_name="escalation_drill_status",
        )
        _validate_saas_operating_automation_status(
            self.closeout_retry_status,
            field_name="closeout_retry_status",
        )
        _reject_sensitive_material(
            {
                "automation_scope": self.automation_scope,
                "automation_cadence": self.automation_cadence,
                "blockers": list(self.blockers),
            }
        )
        return {
            "tenant_id": _safe_identifier(self.tenant_id, field_name="tenant_id"),
            "automation_status": self.automation_status,
            "billing_monitoring_status": self.billing_monitoring_status,
            "license_telemetry_status": self.license_telemetry_status,
            "support_followup_status": self.support_followup_status,
            "customer_success_review_status": self.customer_success_review_status,
            "dashboard_refresh_status": self.dashboard_refresh_status,
            "escalation_drill_status": self.escalation_drill_status,
            "closeout_retry_status": self.closeout_retry_status,
            "automation_scope": self.automation_scope,
            "automation_cadence": self.automation_cadence,
            "blockers": list(self.blockers),
            "private_validation_required": self.private_validation_required,
            "automation_boundary": (
                "billing systems, license telemetry, support workflows, customer-success records, "
                "dashboard refresh jobs, escalation drills, closeout retries, and scheduler execution "
                "remain private service responsibilities"
            ),
        }


def build_entitlement_status_request(
    tenant_id: str,
    *,
    requested_by: str = "community",
    feature_names: tuple[str, ...] = (),
) -> SaaSControlPlaneRequest:
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.ENTITLEMENT_STATUS,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "feature_names": list(feature_names),
            "requested_checks": ["subscription_status", "license_status", "feature_grants"],
            "entitlement_boundary": "public request shape only; billing and license validation are private",
        },
    )


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


def build_tenant_onboarding_request(
    tenant_id: str,
    *,
    organization_name: str,
    requested_by: str = "community",
    deployment_model: str = "hosted_saas",
    region: str = "tenant-selected",
    requirements: tuple[str, ...] = TENANT_ONBOARDING_REQUIREMENTS,
    contacts: dict[str, str] | None = None,
) -> SaaSControlPlaneRequest:
    if deployment_model not in TENANT_DEPLOYMENT_MODELS:
        supported = ", ".join(sorted(TENANT_DEPLOYMENT_MODELS))
        raise SaaSContractError(f"deployment_model must be one of: {supported}")
    if not organization_name.strip():
        raise SaaSContractError("organization_name must not be empty")
    if not requirements:
        raise SaaSContractError("requirements must include at least one onboarding requirement")
    contact_payload = contacts or {}
    _reject_sensitive_material(contact_payload)
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.TENANT_ONBOARDING,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "organization_name": organization_name.strip(),
            "deployment_model": deployment_model,
            "region": region.strip(),
            "requirements": list(requirements),
            "contacts": contact_payload,
            "activation_boundary": "public request shape only; tenant provisioning implementation is private",
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


def build_policy_registry_readiness_request(
    tenant_id: str,
    *,
    requested_by: str = "community",
    policy_pack_refs: tuple[str, ...] = (),
    catalog_scope: str = "tenant-default",
    required_checks: tuple[str, ...] = POLICY_REGISTRY_READINESS_CHECKS,
) -> SaaSControlPlaneRequest:
    if not required_checks:
        raise SaaSContractError("required_checks must include at least one policy registry readiness check")
    _reject_sensitive_material({"policy_pack_refs": list(policy_pack_refs), "catalog_scope": catalog_scope})
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.POLICY_REGISTRY_READINESS,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "policy_pack_refs": list(policy_pack_refs),
            "catalog_scope": catalog_scope,
            "required_checks": list(required_checks),
            "readiness_boundary": "public request shape only; hosted policy registry operation is private",
        },
    )


def build_tenant_audit_store_operating_request(
    tenant_id: str,
    *,
    requested_by: str = "community",
    retention_profile: str = "tenant-default",
    evidence_window: str = "last-24h",
    required_checks: tuple[str, ...] = TENANT_AUDIT_STORE_OPERATING_CHECKS,
) -> SaaSControlPlaneRequest:
    if not required_checks:
        raise SaaSContractError("required_checks must include at least one tenant audit-store operating check")
    _reject_sensitive_material({"retention_profile": retention_profile, "evidence_window": evidence_window})
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.TENANT_AUDIT_STORE_OPERATING,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "retention_profile": retention_profile,
            "evidence_window": evidence_window,
            "required_checks": list(required_checks),
            "operating_boundary": "public request shape only; tenant audit-store operation is private",
        },
    )


def build_customer_operating_dashboard_request(
    tenant_id: str,
    *,
    requested_by: str = "community",
    dashboard_scope: str = "tenant-operating",
    evidence_window: str = "last-24h",
    required_checks: tuple[str, ...] = CUSTOMER_OPERATING_DASHBOARD_CHECKS,
) -> SaaSControlPlaneRequest:
    if not required_checks:
        raise SaaSContractError("required_checks must include at least one customer operating dashboard check")
    _reject_sensitive_material({"dashboard_scope": dashboard_scope, "evidence_window": evidence_window})
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.CUSTOMER_OPERATING_DASHBOARD,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "dashboard_scope": dashboard_scope,
            "evidence_window": evidence_window,
            "required_checks": list(required_checks),
            "dashboard_boundary": "public request shape only; customer operating dashboards are private",
        },
    )


def build_support_handoff_readiness_request(
    tenant_id: str,
    *,
    requested_by: str = "community",
    handoff_scope: str = "hosted-saas-support",
    support_tier: str = "enterprise",
    required_checks: tuple[str, ...] = SUPPORT_HANDOFF_READINESS_CHECKS,
) -> SaaSControlPlaneRequest:
    if not required_checks:
        raise SaaSContractError("required_checks must include at least one support handoff readiness check")
    _reject_sensitive_material({"handoff_scope": handoff_scope, "support_tier": support_tier})
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.SUPPORT_HANDOFF_READINESS,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "handoff_scope": handoff_scope,
            "support_tier": support_tier,
            "required_checks": list(required_checks),
            "handoff_boundary": "public request shape only; support and customer-success handoff is private",
        },
    )


def build_saas_operating_automation_request(
    tenant_id: str,
    *,
    requested_by: str = "community",
    automation_scope: str = "trial-to-paid-customer-scale",
    automation_cadence: str = "daily",
    required_checks: tuple[str, ...] = SAAS_OPERATING_AUTOMATION_CHECKS,
) -> SaaSControlPlaneRequest:
    if not required_checks:
        raise SaaSContractError("required_checks must include at least one SaaS operating automation check")
    _reject_sensitive_material({"automation_scope": automation_scope, "automation_cadence": automation_cadence})
    return SaaSControlPlaneRequest(
        operation=SaaSOperation.SAAS_OPERATING_AUTOMATION,
        tenant_id=_safe_identifier(tenant_id, field_name="tenant_id"),
        requested_by=_safe_identifier(requested_by, field_name="requested_by"),
        payload={
            "automation_scope": automation_scope,
            "automation_cadence": automation_cadence,
            "required_checks": list(required_checks),
            "automation_boundary": "public request shape only; SaaS operating automation execution is private",
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


def build_tenant_audit_store_operating_response(
    request: SaaSControlPlaneRequest,
    summary: TenantAuditStoreOperatingSummary,
    *,
    status: SaaSResponseStatus = SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
) -> SaaSControlPlaneResponse:
    if request.operation != SaaSOperation.TENANT_AUDIT_STORE_OPERATING:
        raise SaaSContractError("tenant audit-store operating response requires a tenant_audit_store_operating request")
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=status,
        message="Tenant audit-store operating status requires private archive, retention, evidence, export, and dashboard validation.",
        correlation_id=request.correlation_id,
        payload={
            "summary": summary.to_dict(),
            "private_modules_required": [
                "tenant audit store",
                "retention enforcement",
                "evidence freshness monitor",
                "export connector service",
                "operating dashboard",
            ],
            "next_step": "See docs/architecture/tenant-audit-store-operating-contract.md",
        },
    )


def build_customer_operating_dashboard_response(
    request: SaaSControlPlaneRequest,
    summary: CustomerOperatingDashboardSummary,
    *,
    status: SaaSResponseStatus = SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
) -> SaaSControlPlaneResponse:
    if request.operation != SaaSOperation.CUSTOMER_OPERATING_DASHBOARD:
        raise SaaSContractError("customer operating dashboard response requires a customer_operating_dashboard request")
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=status,
        message=(
            "Customer operating dashboard status requires private billing, license-service, "
            "support, customer-success, escalation, and release closeout validation."
        ),
        correlation_id=request.correlation_id,
        payload={
            "summary": summary.to_dict(),
            "private_modules_required": [
                "billing observability",
                "license-service telemetry",
                "support handoff",
                "customer-success health",
                "escalation routing",
                "release closeout",
                "operating dashboard",
            ],
            "next_step": "See docs/architecture/customer-operating-dashboard-support-handoff-contract.md",
        },
    )


def build_support_handoff_readiness_response(
    request: SaaSControlPlaneRequest,
    summary: SupportHandoffReadinessSummary,
    *,
    status: SaaSResponseStatus = SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
) -> SaaSControlPlaneResponse:
    if request.operation != SaaSOperation.SUPPORT_HANDOFF_READINESS:
        raise SaaSContractError("support handoff readiness response requires a support_handoff_readiness request")
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=status,
        message=(
            "Support handoff readiness requires private support, customer-success, "
            "escalation, health-review, and dashboard validation."
        ),
        correlation_id=request.correlation_id,
        payload={
            "summary": summary.to_dict(),
            "private_modules_required": [
                "support ownership",
                "customer-success ownership",
                "escalation routing",
                "customer health review",
                "handoff dashboard",
                "release owner acceptance",
            ],
            "next_step": "See docs/architecture/customer-operating-dashboard-support-handoff-contract.md",
        },
    )


def build_saas_operating_automation_response(
    request: SaaSControlPlaneRequest,
    summary: SaaSOperatingAutomationSummary,
    *,
    status: SaaSResponseStatus = SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
) -> SaaSControlPlaneResponse:
    if request.operation != SaaSOperation.SAAS_OPERATING_AUTOMATION:
        raise SaaSContractError("SaaS operating automation response requires a saas_operating_automation request")
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=status,
        message=(
            "SaaS operating automation requires private billing monitoring, license telemetry, "
            "support, customer-success, dashboard, escalation, closeout retry, and scheduler validation."
        ),
        correlation_id=request.correlation_id,
        payload={
            "summary": summary.to_dict(),
            "private_modules_required": [
                "billing monitoring",
                "license telemetry sync",
                "support follow-up",
                "customer-success review",
                "dashboard refresh automation",
                "escalation drill scheduler",
                "closeout retry automation",
            ],
            "next_step": "See docs/architecture/saas-operating-automation-contract.md",
        },
    )


def build_policy_registry_readiness_response(
    request: SaaSControlPlaneRequest,
    summary: PolicyRegistryReadinessSummary,
    *,
    status: SaaSResponseStatus = SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
) -> SaaSControlPlaneResponse:
    if request.operation != SaaSOperation.POLICY_REGISTRY_READINESS:
        raise SaaSContractError("policy registry readiness response requires a policy_registry_readiness request")
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=status,
        message="Hosted policy registry readiness requires private registry, artifact, entitlement, and rollout validation.",
        correlation_id=request.correlation_id,
        payload={
            "summary": summary.to_dict(),
            "private_modules_required": [
                "hosted policy registry service",
                "policy-pack artifact store",
                "feature entitlement registry",
                "approval workflow",
                "rollout telemetry",
            ],
            "next_step": "See docs/architecture/hosted-policy-registry-readiness-contract.md",
        },
    )


def build_entitlement_status_response(
    request: SaaSControlPlaneRequest,
    summary: EntitlementStatusSummary,
    *,
    status: SaaSResponseStatus = SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
) -> SaaSControlPlaneResponse:
    if request.operation != SaaSOperation.ENTITLEMENT_STATUS:
        raise SaaSContractError("entitlement status response requires an entitlement_status request")
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=status,
        message="Entitlement status requires private billing, subscription, and license-service validation.",
        correlation_id=request.correlation_id,
        payload={
            "summary": summary.to_dict(),
            "private_modules_required": [
                "billing integration",
                "license service",
                "subscription status",
                "feature entitlement registry",
            ],
            "next_step": "See docs/architecture/entitlement-status-contract.md",
        },
    )


def build_tenant_onboarding_unavailable_response(request: SaaSControlPlaneRequest) -> SaaSControlPlaneResponse:
    if request.operation != SaaSOperation.TENANT_ONBOARDING:
        raise SaaSContractError("tenant onboarding response requires a tenant_onboarding request")
    return SaaSControlPlaneResponse(
        operation=request.operation,
        status=SaaSResponseStatus.REQUIRES_PRIVATE_SERVICE,
        message="Tenant onboarding requires the private CAVRA SaaS Control Plane or Enterprise service.",
        correlation_id=request.correlation_id,
        payload={
            "tenant_id": request.tenant_id,
            "private_modules_required": [
                "identity onboarding",
                "license service",
                "policy registry",
                "audit store",
                "support ownership",
            ],
            "next_step": "See docs/architecture/tenant-onboarding-contract.md",
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
                "name": SaaSOperation.ENTITLEMENT_STATUS.value,
                "request": "tenant identifier and optional feature names",
                "response": "subscription, license, and feature entitlement summary",
            },
            {
                "name": SaaSOperation.TENANT_ONBOARDING.value,
                "request": "tenant activation metadata, deployment model, contacts, and readiness requirements",
                "response": "tenant activation state, blockers, and private service handoff status",
            },
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
                "name": SaaSOperation.POLICY_REGISTRY_READINESS.value,
                "request": "tenant identifier, catalog scope, policy-pack references, and readiness checks",
                "response": "hosted registry availability, catalog freshness, version state, blockers, and private service handoff status",
            },
            {
                "name": SaaSOperation.POLICY_REGISTRY_LOOKUP.value,
                "request": "policy references and public labels",
                "response": "policy metadata and downloadable artifact references",
            },
            {
                "name": SaaSOperation.TENANT_AUDIT_STORE_OPERATING.value,
                "request": "tenant identifier, retention profile, evidence window, and operating checks",
                "response": "audit-store health, retention posture, evidence freshness, export readiness, blockers, and private service handoff status",
            },
            {
                "name": SaaSOperation.CUSTOMER_OPERATING_DASHBOARD.value,
                "request": "tenant identifier, dashboard scope, evidence window, and operating dashboard checks",
                "response": "customer operating dashboard readiness across billing, license service, support, customer success, escalation, and release closeout",
            },
            {
                "name": SaaSOperation.SUPPORT_HANDOFF_READINESS.value,
                "request": "tenant identifier, handoff scope, support tier, and support handoff checks",
                "response": "support, customer-success, escalation, health review, dashboard, and release owner readiness",
            },
            {
                "name": SaaSOperation.SAAS_OPERATING_AUTOMATION.value,
                "request": "tenant identifier, automation scope, automation cadence, and operating automation checks",
                "response": "billing monitoring, license telemetry, support follow-up, customer-success review, dashboard refresh, escalation drill, and closeout retry readiness",
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


def _validate_entitlement_status(status: str) -> None:
    if status not in ENTITLEMENT_STATUSES:
        supported = ", ".join(sorted(ENTITLEMENT_STATUSES))
        raise SaaSContractError(f"entitlement_status must be one of: {supported}")


def _validate_policy_registry_readiness_status(status: str, *, field_name: str) -> None:
    if status not in POLICY_REGISTRY_READINESS_STATUSES:
        supported = ", ".join(sorted(POLICY_REGISTRY_READINESS_STATUSES))
        raise SaaSContractError(f"{field_name} must be one of: {supported}")


def _validate_audit_store_operating_status(status: str, *, field_name: str) -> None:
    if status not in TENANT_AUDIT_STORE_OPERATING_STATUSES:
        supported = ", ".join(sorted(TENANT_AUDIT_STORE_OPERATING_STATUSES))
        raise SaaSContractError(f"{field_name} must be one of: {supported}")


def _validate_customer_operating_dashboard_status(status: str, *, field_name: str) -> None:
    if status not in CUSTOMER_OPERATING_DASHBOARD_STATUSES:
        supported = ", ".join(sorted(CUSTOMER_OPERATING_DASHBOARD_STATUSES))
        raise SaaSContractError(f"{field_name} must be one of: {supported}")


def _validate_support_handoff_readiness_status(status: str, *, field_name: str) -> None:
    if status not in SUPPORT_HANDOFF_READINESS_STATUSES:
        supported = ", ".join(sorted(SUPPORT_HANDOFF_READINESS_STATUSES))
        raise SaaSContractError(f"{field_name} must be one of: {supported}")


def _validate_saas_operating_automation_status(status: str, *, field_name: str) -> None:
    if status not in SAAS_OPERATING_AUTOMATION_STATUSES:
        supported = ", ".join(sorted(SAAS_OPERATING_AUTOMATION_STATUSES))
        raise SaaSContractError(f"{field_name} must be one of: {supported}")


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
    "CUSTOMER_OPERATING_DASHBOARD_CHECKS",
    "CUSTOMER_OPERATING_DASHBOARD_STATUSES",
    "ENTITLEMENT_STATUSES",
    "EVIDENCE_EXPORT_FORMATS",
    "POLICY_REGISTRY_READINESS_CHECKS",
    "POLICY_REGISTRY_READINESS_STATUSES",
    "SAAS_CONTROL_PLANE_CONTRACT_VERSION",
    "SAAS_CONTROL_PLANE_REQUEST_VERSION",
    "SAAS_CONTROL_PLANE_RESPONSE_VERSION",
    "SAAS_OPERATING_AUTOMATION_CHECKS",
    "SAAS_OPERATING_AUTOMATION_STATUSES",
    "SUPPORT_HANDOFF_READINESS_CHECKS",
    "SUPPORT_HANDOFF_READINESS_STATUSES",
    "TENANT_DEPLOYMENT_MODELS",
    "TENANT_AUDIT_STORE_OPERATING_CHECKS",
    "TENANT_AUDIT_STORE_OPERATING_STATUSES",
    "TENANT_ONBOARDING_REQUIREMENTS",
    "CustomerOperatingDashboardSummary",
    "EntitlementStatusSummary",
    "PolicyRegistryReadinessSummary",
    "SaaSOperatingAutomationSummary",
    "SupportHandoffReadinessSummary",
    "TenantAuditStoreOperatingSummary",
    "SaaSContractError",
    "SaaSControlPlaneRequest",
    "SaaSControlPlaneResponse",
    "SaaSOperation",
    "SaaSResponseStatus",
    "build_entitlement_status_request",
    "build_entitlement_status_response",
    "build_customer_operating_dashboard_request",
    "build_customer_operating_dashboard_response",
    "build_evidence_export_request",
    "build_license_validation_request",
    "build_saas_operating_automation_request",
    "build_saas_operating_automation_response",
    "build_support_handoff_readiness_request",
    "build_support_handoff_readiness_response",
    "build_tenant_audit_store_operating_request",
    "build_tenant_audit_store_operating_response",
    "build_policy_registry_readiness_request",
    "build_policy_registry_readiness_response",
    "build_policy_registry_lookup_request",
    "build_tenant_onboarding_request",
    "build_tenant_onboarding_unavailable_response",
    "build_tenant_status_request",
    "build_unavailable_response",
    "describe_public_contract",
    "validate_public_payload",
]
