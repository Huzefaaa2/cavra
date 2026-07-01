from __future__ import annotations

from dataclasses import dataclass

from cavra.licensing.license_types import License, LicenseEdition, LicenseStatus
from cavra.product_model import (
    COMMERCIAL_ENTITLEMENT_CAPABILITIES,
    CONFIGURABLE_CAPABILITIES,
    CORE_CAPABILITIES,
    MANAGED_SERVICE_CAPABILITIES,
    CapabilityExplanation,
    CapabilityStatus,
    CommercialEntitlement,
    DeploymentMode,
    ProductModelConfig,
    ProviderProfile,
    explain_capability_status,
    normalize_capability,
)


COMMUNITY_FEATURES = CORE_CAPABILITIES | CONFIGURABLE_CAPABILITIES
ENTERPRISE_FEATURES = COMMERCIAL_ENTITLEMENT_CAPABILITIES | MANAGED_SERVICE_CAPABILITIES


@dataclass(frozen=True)
class FeatureExplanation:
    feature: str
    enabled: bool
    reason: str
    status: str = CapabilityStatus.AVAILABLE.value
    required_configuration: tuple[str, ...] = ()


def is_feature_enabled(feature_name: str, edition: str, license_obj: License | None = None) -> bool:
    """Return whether the product supports a feature for compatibility callers.

    This legacy API no longer treats CAVRA Community as a crippled edition.
    Core and self-hostable capabilities return True. Provider-backed
    capabilities also return True because they are available once configured.
    Managed-service and commercial-pack capabilities require the corresponding
    entitlement.
    """

    if license_obj is not None and license_obj.normalized_status() != LicenseStatus.VALID:
        return False
    config = _legacy_config_from_edition(edition, license_obj)
    explanation = explain_capability_status(feature_name, config)
    if explanation.status in {CapabilityStatus.AVAILABLE, CapabilityStatus.REQUIRES_CONFIGURATION}:
        return True
    return False


def list_available_features(edition: str) -> dict[str, list[str]]:
    config = _legacy_config_from_edition(edition, None)
    registry = sorted(COMMUNITY_FEATURES | ENTERPRISE_FEATURES)
    buckets: dict[str, list[str]] = {
        "enabled": [],
        "requires_configuration": [],
        "requires_managed_service": [],
        "requires_commercial_entitlement": [],
        "unsupported": [],
        # Deprecated key kept for callers that still expect a locked bucket.
        "locked": [],
    }
    for capability in registry:
        explanation = explain_capability_status(capability, config)
        if explanation.status == CapabilityStatus.AVAILABLE:
            buckets["enabled"].append(capability)
        elif explanation.status == CapabilityStatus.REQUIRES_CONFIGURATION:
            buckets["requires_configuration"].append(capability)
        elif explanation.status == CapabilityStatus.REQUIRES_MANAGED_SERVICE:
            buckets["requires_managed_service"].append(capability)
        elif explanation.status == CapabilityStatus.REQUIRES_COMMERCIAL_ENTITLEMENT:
            buckets["requires_commercial_entitlement"].append(capability)
        else:
            buckets["unsupported"].append(capability)
    buckets["locked"] = sorted(
        buckets["requires_managed_service"] + buckets["requires_commercial_entitlement"]
    )
    return buckets


def explain_locked_feature(feature_name: str) -> FeatureExplanation:
    explanation = explain_capability_status(feature_name, ProductModelConfig())
    return FeatureExplanation(
        feature=explanation.capability,
        enabled=explanation.enabled,
        reason=explanation.reason,
        status=explanation.status.value,
        required_configuration=explanation.required_configuration,
    )


def _legacy_config_from_edition(edition: str, license_obj: License | None) -> ProductModelConfig:
    normalized = (edition or LicenseEdition.COMMUNITY.value).lower().strip()
    if license_obj is not None:
        normalized = license_obj.edition.value
        if license_obj.normalized_status() != LicenseStatus.VALID:
            return ProductModelConfig(
                deployment_mode=DeploymentMode.COMMUNITY,
                commercial_entitlement=CommercialEntitlement.NONE,
                provider_profile=ProviderProfile.LOCAL,
                legacy_edition=normalized,
            )
    if normalized == LicenseEdition.SAAS.value:
        return ProductModelConfig(
            deployment_mode=DeploymentMode.MANAGED,
            commercial_entitlement=CommercialEntitlement.MANAGED,
            provider_profile=ProviderProfile.MANAGED,
            legacy_edition=normalized,
        )
    if normalized in {
        LicenseEdition.TRIAL.value,
        LicenseEdition.BUSINESS.value,
        LicenseEdition.ENTERPRISE.value,
    }:
        return ProductModelConfig(
            deployment_mode=DeploymentMode.TRIAL_ACCESS
            if normalized == LicenseEdition.TRIAL.value
            else DeploymentMode.COMMUNITY,
            commercial_entitlement=CommercialEntitlement.ENTERPRISE_SUBSCRIPTION,
            provider_profile=ProviderProfile.SELF_HOSTED,
            legacy_edition=normalized,
        )
    return ProductModelConfig(legacy_edition=normalized if normalized != "community" else None)


__all__ = [
    "COMMERCIAL_ENTITLEMENT_CAPABILITIES",
    "CONFIGURABLE_CAPABILITIES",
    "CORE_CAPABILITIES",
    "COMMUNITY_FEATURES",
    "ENTERPRISE_FEATURES",
    "FeatureExplanation",
    "is_feature_enabled",
    "list_available_features",
    "explain_locked_feature",
    "explain_capability_status",
    "normalize_capability",
]
