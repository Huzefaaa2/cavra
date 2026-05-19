from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any

ENTERPRISE_PACKAGE = "cavra_enterprise"
ENTERPRISE_MESSAGE = "This feature is available in CAVRA Enterprise. See docs/enterprise/features.md for details."


@dataclass(frozen=True)
class EnterpriseFeatureUnavailable(Exception):
    """Raised when a private Enterprise feature is requested from Community code."""

    feature_name: str
    message: str = ENTERPRISE_MESSAGE

    def __str__(self) -> str:
        return self.message


def is_enterprise_available(package_name: str = ENTERPRISE_PACKAGE) -> bool:
    """Return true only when the private Enterprise package is installed."""

    try:
        importlib.import_module(package_name)
    except ImportError:
        return False
    return True


def load_enterprise_feature(name: str, package_name: str = ENTERPRISE_PACKAGE) -> Any:
    """Dynamically load a private Enterprise feature without shipping it publicly."""

    try:
        package = importlib.import_module(package_name)
    except ImportError as exc:
        raise EnterpriseFeatureUnavailable(name) from exc
    try:
        return getattr(package, name)
    except AttributeError as exc:
        raise EnterpriseFeatureUnavailable(name) from exc


def enterprise_unavailable_response(feature_name: str) -> dict[str, Any]:
    return {
        "available": False,
        "feature": feature_name,
        "reason": ENTERPRISE_MESSAGE,
    }
