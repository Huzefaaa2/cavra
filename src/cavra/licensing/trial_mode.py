from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from cavra.licensing.license_types import License, LicenseEdition, LicenseStatus


@dataclass(frozen=True)
class TrialMode:
    """Local placeholder for future trial validation."""

    license: License

    @property
    def active(self) -> bool:
        return self.license.edition == LicenseEdition.TRIAL and self.license.normalized_status() == LicenseStatus.VALID

    def days_remaining(self, *, now: datetime | None = None) -> int | None:
        if not self.license.expires_at:
            return None
        current = now or datetime.now(timezone.utc)
        try:
            expires = datetime.fromisoformat(self.license.expires_at.replace("Z", "+00:00"))
        except ValueError:
            return 0
        return max(0, (expires - current).days)

    def validation_note(self) -> str:
        return (
            "Local trial checks are placeholders. Real trial entitlement, "
            "signature, and revocation validation must be delegated to the "
            "private CAVRA license service."
        )
