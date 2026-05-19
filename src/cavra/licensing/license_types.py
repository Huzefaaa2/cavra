from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class LicenseEdition(str, Enum):
    COMMUNITY = "community"
    TRIAL = "trial"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"
    SAAS = "saas"


class LicenseStatus(str, Enum):
    VALID = "valid"
    EXPIRED = "expired"
    INVALID = "invalid"
    MISSING = "missing"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class License:
    license_id: str
    edition: LicenseEdition
    customer_name: str = ""
    expires_at: str | None = None
    features: tuple[str, ...] = field(default_factory=tuple)
    signature: str | None = None
    status: LicenseStatus = LicenseStatus.VALID

    def is_expired(self, *, now: datetime | None = None) -> bool:
        if not self.expires_at:
            return False
        current = now or datetime.now(timezone.utc)
        expires = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
        return expires < current

    def normalized_status(self, *, now: datetime | None = None) -> LicenseStatus:
        if self.status != LicenseStatus.VALID:
            return self.status
        return LicenseStatus.EXPIRED if self.is_expired(now=now) else LicenseStatus.VALID

    def to_dict(self) -> dict[str, object]:
        return {
            "license_id": self.license_id,
            "edition": self.edition.value,
            "customer_name": self.customer_name,
            "expires_at": self.expires_at,
            "features": list(self.features),
            "signature": self.signature,
            "status": self.status.value,
        }
