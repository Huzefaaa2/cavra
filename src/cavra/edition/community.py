from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

COMMUNITY_EDITION = "community"
ENTERPRISE_MESSAGE = "This feature is available in CAVRA Enterprise. See docs/enterprise/features.md for details."


@dataclass(frozen=True)
class CommunityEdition:
    """Runtime edition descriptor for the public Community Edition."""

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


def is_community_mode(env: dict[str, str] | None = None) -> bool:
    return current_edition(env) == COMMUNITY_EDITION


def require_enterprise(feature_name: str, *, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a public-safe blocked response for enterprise-only features."""

    return {
        "allowed": False,
        "feature": feature_name,
        "edition": COMMUNITY_EDITION,
        "reason": ENTERPRISE_MESSAGE,
        "context": context or {},
    }
