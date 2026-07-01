from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class CapabilityStatus(str, Enum):
    AVAILABLE = "available"
    REQUIRES_CONFIGURATION = "requires_configuration"
    REQUIRES_MANAGED_SERVICE = "requires_managed_service"
    REQUIRES_COMMERCIAL_ENTITLEMENT = "requires_commercial_entitlement"
    UNSUPPORTED = "unsupported"
    DEPRECATED = "deprecated"


class DeploymentMode(str, Enum):
    COMMUNITY = "community"
    MANAGED = "managed"
    TRIAL_ACCESS = "trial_access"


class CommercialEntitlement(str, Enum):
    NONE = "none"
    ENTERPRISE_SUBSCRIPTION = "enterprise_subscription"
    MANAGED = "managed"


class ProviderProfile(str, Enum):
    LOCAL = "local"
    SELF_HOSTED = "self_hosted"
    MANAGED = "managed"


CORE_CAPABILITIES = frozenset(
    {
        "runtime_decisions",
        "policy_evaluation",
        "approvals",
        "evidence_bundles",
        "aispm",
        "report_center",
        "local_dashboard",
        "ci_cd_enforcement",
        "self_hosted_tenant_model",
        "connector_framework",
        "reference_connectors",
        "public_policy_packs",
        "public_contracts",
        # Legacy feature names kept as first-class aliases for CLI/API callers.
        "local_scan",
        "basic_policy_evaluation",
        "cli_execution",
        "starter_policies",
        "github_action_support",
        "central_dashboard",
        "organization_wide_enforcement",
        "drift_monitoring",
        "ai_remediation_recommendations",
    }
)

CONFIGURABLE_CAPABILITIES = frozenset(
    {
        "sso_rbac",
        "sso",
        "rbac",
        "audit_export",
        "report_delivery",
        "policy_registry",
        "connector_credentials",
        "compliance_evidence_reports",
        "policy_approval_workflow",
    }
)

MANAGED_SERVICE_CAPABILITIES = frozenset(
    {
        "managed_tenant_operations",
        "billing",
        "support_handoff",
        "customer_success_operations",
        "managed_policy_registry",
        "managed_report_delivery",
        "managed_audit_storage",
        "managed_dashboard_operations",
        # Legacy name. The public contract exists; hosted execution is Managed.
        "saas_api_integration",
    }
)

COMMERCIAL_ENTITLEMENT_CAPABILITIES = frozenset(
    {
        "certified_connectors",
        "commercial_policy_packs",
        "private_policy_packs",
        "compliance_packs",
        "custom_integrations",
        "implementation_help",
        "sla_support",
        "procurement_security_review",
    }
)

CAPABILITY_ALIASES = {
    "enterprise_sso": "sso_rbac",
    "enterprise_rbac": "sso_rbac",
    "tenant_isolation": "self_hosted_tenant_model",
    "live_connectors": "certified_connectors",
    "private_connectors": "certified_connectors",
    "production_report_delivery": "report_delivery",
}


@dataclass(frozen=True)
class ProductModelConfig:
    deployment_mode: DeploymentMode = DeploymentMode.COMMUNITY
    commercial_entitlement: CommercialEntitlement = CommercialEntitlement.NONE
    provider_profile: ProviderProfile = ProviderProfile.LOCAL
    legacy_edition: str | None = None
    deprecation_warnings: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "ProductModelConfig":
        data = env or {}
        warnings: list[str] = []

        deployment_mode = _enum_value(
            DeploymentMode,
            data.get("CAVRA_DEPLOYMENT_MODE"),
            DeploymentMode.COMMUNITY,
        )
        commercial_entitlement = _enum_value(
            CommercialEntitlement,
            data.get("CAVRA_COMMERCIAL_ENTITLEMENT"),
            CommercialEntitlement.NONE,
        )
        provider_profile = _enum_value(
            ProviderProfile,
            data.get("CAVRA_PROVIDER_PROFILE"),
            ProviderProfile.LOCAL,
        )

        legacy_edition = data.get("CAVRA_EDITION")
        if legacy_edition:
            legacy = legacy_edition.lower().strip()
            warnings.append(
                "CAVRA_EDITION is deprecated; use CAVRA_DEPLOYMENT_MODE, "
                "CAVRA_COMMERCIAL_ENTITLEMENT, and CAVRA_PROVIDER_PROFILE."
            )
            if legacy == "community":
                deployment_mode = DeploymentMode.COMMUNITY
                commercial_entitlement = CommercialEntitlement.NONE
            elif legacy in {"enterprise", "business"}:
                deployment_mode = DeploymentMode.COMMUNITY
                commercial_entitlement = CommercialEntitlement.ENTERPRISE_SUBSCRIPTION
                provider_profile = ProviderProfile.SELF_HOSTED
            elif legacy == "saas":
                deployment_mode = DeploymentMode.MANAGED
                commercial_entitlement = CommercialEntitlement.MANAGED
                provider_profile = ProviderProfile.MANAGED
            elif legacy == "trial":
                deployment_mode = DeploymentMode.TRIAL_ACCESS
                commercial_entitlement = CommercialEntitlement.ENTERPRISE_SUBSCRIPTION
                provider_profile = ProviderProfile.SELF_HOSTED
            else:
                warnings.append(f"Unknown legacy CAVRA_EDITION value ignored: {legacy_edition}")

        return cls(
            deployment_mode=deployment_mode,
            commercial_entitlement=commercial_entitlement,
            provider_profile=provider_profile,
            legacy_edition=legacy_edition,
            deprecation_warnings=tuple(warnings),
        )


@dataclass(frozen=True)
class CapabilityExplanation:
    capability: str
    status: CapabilityStatus
    reason: str
    required_configuration: tuple[str, ...] = field(default_factory=tuple)
    managed_service_available: bool = False
    commercial_entitlement_required: bool = False

    @property
    def enabled(self) -> bool:
        return self.status in {
            CapabilityStatus.AVAILABLE,
            CapabilityStatus.REQUIRES_CONFIGURATION,
        }


def normalize_capability(capability: str) -> str:
    normalized = capability.lower().strip().replace("-", "_")
    return CAPABILITY_ALIASES.get(normalized, normalized)


def explain_capability_status(
    capability: str,
    config: ProductModelConfig | None = None,
    *,
    configured_providers: tuple[str, ...] = (),
) -> CapabilityExplanation:
    cfg = config or ProductModelConfig()
    normalized = normalize_capability(capability)
    configured = {item.lower().strip().replace("-", "_") for item in configured_providers}

    if normalized in CORE_CAPABILITIES:
        return CapabilityExplanation(
            normalized,
            CapabilityStatus.AVAILABLE,
            "Available in CAVRA Community for local or self-hosted use.",
        )

    if normalized in CONFIGURABLE_CAPABILITIES:
        if (
            normalized in configured
            or cfg.provider_profile == ProviderProfile.MANAGED
            or cfg.deployment_mode == DeploymentMode.MANAGED
        ):
            return CapabilityExplanation(
                normalized,
                CapabilityStatus.AVAILABLE,
                "Available because the required provider is configured.",
            )
        return CapabilityExplanation(
            normalized,
            CapabilityStatus.REQUIRES_CONFIGURATION,
            "Available in CAVRA Community, but it requires backing provider configuration.",
            required_configuration=_required_configuration(normalized),
        )

    if normalized in MANAGED_SERVICE_CAPABILITIES:
        if cfg.deployment_mode == DeploymentMode.MANAGED or cfg.commercial_entitlement == CommercialEntitlement.MANAGED:
            return CapabilityExplanation(
                normalized,
                CapabilityStatus.AVAILABLE,
                "Available through CAVRA Managed.",
                managed_service_available=True,
            )
        return CapabilityExplanation(
            normalized,
            CapabilityStatus.REQUIRES_MANAGED_SERVICE,
            "This is an operated-service capability available through CAVRA Managed.",
            managed_service_available=True,
        )

    if normalized in COMMERCIAL_ENTITLEMENT_CAPABILITIES:
        if cfg.commercial_entitlement in {
            CommercialEntitlement.ENTERPRISE_SUBSCRIPTION,
            CommercialEntitlement.MANAGED,
        }:
            return CapabilityExplanation(
                normalized,
                CapabilityStatus.AVAILABLE,
                "Available with a CAVRA Enterprise Subscription or CAVRA Managed entitlement.",
                commercial_entitlement_required=True,
            )
        return CapabilityExplanation(
            normalized,
            CapabilityStatus.REQUIRES_COMMERCIAL_ENTITLEMENT,
            "This requires a CAVRA Enterprise Subscription, commercial pack, or certified connector package.",
            commercial_entitlement_required=True,
        )

    return CapabilityExplanation(
        normalized,
        CapabilityStatus.UNSUPPORTED,
        "Unknown capability. Check the public capability registry or provider interface.",
    )


def resolve_capability_status(
    capability: str,
    config: ProductModelConfig | None = None,
    *,
    configured_providers: tuple[str, ...] = (),
) -> CapabilityStatus:
    return explain_capability_status(
        capability,
        config,
        configured_providers=configured_providers,
    ).status


def _enum_value(enum_type: type[Enum], raw: str | None, default: Enum) -> Enum:
    if not raw:
        return default
    candidate = raw.lower().strip()
    for item in enum_type:
        if item.value == candidate:
            return item
    return default


def _required_configuration(capability: str) -> tuple[str, ...]:
    return {
        "sso_rbac": ("identity_provider", "rbac_mapping"),
        "sso": ("identity_provider",),
        "rbac": ("rbac_mapping",),
        "audit_export": ("audit_store", "export_destination"),
        "report_delivery": ("smtp_or_report_provider", "recipient_policy", "delivery_audit_store"),
        "policy_registry": ("database_or_object_store",),
        "connector_credentials": ("secret_store", "connector_credentials"),
        "compliance_evidence_reports": ("evidence_store", "report_template"),
        "policy_approval_workflow": ("approval_provider", "reviewer_mapping"),
    }.get(capability, ("provider_configuration",))


__all__ = [
    "CAPABILITY_ALIASES",
    "COMMERCIAL_ENTITLEMENT_CAPABILITIES",
    "CONFIGURABLE_CAPABILITIES",
    "CORE_CAPABILITIES",
    "MANAGED_SERVICE_CAPABILITIES",
    "CapabilityExplanation",
    "CapabilityStatus",
    "CommercialEntitlement",
    "DeploymentMode",
    "ProductModelConfig",
    "ProviderProfile",
    "explain_capability_status",
    "normalize_capability",
    "resolve_capability_status",
]
