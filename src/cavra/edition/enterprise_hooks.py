from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any

ENTERPRISE_PACKAGE = "cavra_enterprise"
ENTERPRISE_MESSAGE = (
    "This capability requires a CAVRA Enterprise Subscription, CAVRA Managed, "
    "or a private commercial package that is not shipped in the public repository."
)


@dataclass(frozen=True)
class EnterpriseFeatureUnavailable(Exception):
    """Raised when a private commercial package is requested from public code."""

    feature_name: str
    message: str = ENTERPRISE_MESSAGE

    def __str__(self) -> str:
        return self.message


def is_enterprise_available(package_name: str = ENTERPRISE_PACKAGE) -> bool:
    """Return true only when the private commercial compatibility package is installed."""

    try:
        importlib.import_module(package_name)
    except ImportError:
        return False
    return True


def load_enterprise_feature(name: str, package_name: str = ENTERPRISE_PACKAGE) -> Any:
    """Dynamically load a private commercial package without shipping it publicly."""

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
