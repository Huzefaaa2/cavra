from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from cavra.product_model import ProductModelConfig, explain_capability_status

COMMUNITY_EDITION = "community"
ENTERPRISE_MESSAGE = (
    "CAVRA Community includes the public capability surface. This capability may "
    "require provider configuration, CAVRA Managed, or a CAVRA Enterprise Subscription."
)


@dataclass(frozen=True)
class CommunityEdition:
    """Runtime descriptor for CAVRA Community, the public self-hosted product."""

    name: str = COMMUNITY_EDITION
    license_required: bool = False

    def allows_enterprise_feature(self, feature_name: str) -> bool:
        return False

    def locked_message(self, feature_name: str) -> str:
        return ENTERPRISE_MESSAGE


def current_edition(env: dict[str, str] | None = None) -> str:
    """Return the requested edition, defaulting safely to community."""

    source = env if env is not None else os.environ
    requested = source.get("CAVRA_EDITION", COMMUNITY_EDITION).strip().lower()
    if requested in {"", "ce", "community"}:
        return COMMUNITY_EDITION
    return requested


def current_product_model(env: dict[str, str] | None = None) -> ProductModelConfig:
    """Return the canonical product model while preserving old env parsing."""

    source = env if env is not None else os.environ
    return ProductModelConfig.from_env(source)


def is_community_mode(env: dict[str, str] | None = None) -> bool:
    return current_edition(env) == COMMUNITY_EDITION


def require_enterprise(feature_name: str, *, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Deprecated compatibility wrapper for old Enterprise-only checks."""

    explanation = explain_capability_status(feature_name)
    return {
        "allowed": False,
        "feature": feature_name,
        "edition": COMMUNITY_EDITION,
        "reason": explanation.reason,
        "capability_status": explanation.status.value,
        "required_configuration": list(explanation.required_configuration),
        "commercial_entitlement_required": explanation.commercial_entitlement_required,
        "managed_service_available": explanation.managed_service_available,
        "deprecated": True,
        "context": context or {},
    }
