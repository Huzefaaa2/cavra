from __future__ import annotations

from dataclasses import dataclass

from cavra.edition.community import ENTERPRISE_MESSAGE
from cavra.licensing.license_types import License, LicenseEdition, LicenseStatus


COMMUNITY_FEATURES = {
    "local_scan",
    "basic_policy_evaluation",
    "cli_execution",
    "starter_policies",
    "github_action_support",
}

ENTERPRISE_FEATURES = {
    "sso",
    "rbac",
    "central_dashboard",
    "audit_export",
    "policy_approval_workflow",
    "compliance_evidence_reports",
    "private_policy_packs",
    "organization_wide_enforcement",
    "drift_monitoring",
    "ai_remediation_recommendations",
    "saas_api_integration",
}


@dataclass(frozen=True)
class FeatureExplanation:
    feature: str
    enabled: bool
    reason: str


def is_feature_enabled(feature_name: str, edition: str, license_obj: License | None = None) -> bool:
    normalized = feature_name.strip().lower()
    if normalized in COMMUNITY_FEATURES:
        return True
    if normalized not in ENTERPRISE_FEATURES:
        return False
    if edition == LicenseEdition.COMMUNITY.value:
        return False
    if license_obj is None:
        return False
    if license_obj.normalized_status() != LicenseStatus.VALID:
        return False
    return license_obj.edition in {
        LicenseEdition.TRIAL,
        LicenseEdition.BUSINESS,
        LicenseEdition.ENTERPRISE,
        LicenseEdition.SAAS,
    } and (normalized in license_obj.features or "*" in license_obj.features)


def list_available_features(edition: str) -> dict[str, list[str]]:
    community = sorted(COMMUNITY_FEATURES)
    enterprise = [] if edition == LicenseEdition.COMMUNITY.value else sorted(ENTERPRISE_FEATURES)
    locked = sorted(ENTERPRISE_FEATURES) if edition == LicenseEdition.COMMUNITY.value else []
    return {"enabled": community + enterprise, "locked": locked}


def explain_locked_feature(feature_name: str) -> FeatureExplanation:
    normalized = feature_name.strip().lower()
    if normalized in COMMUNITY_FEATURES:
        return FeatureExplanation(normalized, True, "Community feature is available.")
    if normalized in ENTERPRISE_FEATURES:
        return FeatureExplanation(normalized, False, ENTERPRISE_MESSAGE)
    return FeatureExplanation(normalized, False, "Unknown feature.")
