from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from cavra.licensing.license_types import License, LicenseEdition, LicenseStatus


class LocalLicenseClient:
    """Public-safe license reader with local mock validation only.

    Real online validation, signing-key verification, revocation checks, billing
    state, and tenant entitlement lookup must be implemented in the private
    Enterprise/SaaS repository.
    """

    def load(self, path: Path | None) -> License:
        if path is None or not path.exists():
            return License(
                license_id="community",
                edition=LicenseEdition.COMMUNITY,
                customer_name="Community User",
                features=(),
                status=LicenseStatus.VALID,
            )
        payload = json.loads(path.read_text(encoding="utf-8"))
        return self.from_payload(payload)

    def from_payload(self, payload: dict[str, Any]) -> License:
        edition = LicenseEdition(str(payload.get("edition", "community")).lower())
        features = tuple(str(item) for item in payload.get("features", []) if item)
        license_obj = License(
            license_id=str(payload.get("license_id", "")),
            edition=edition,
            customer_name=str(payload.get("customer_name", "")),
            expires_at=payload.get("expires_at"),
            features=features,
            signature=payload.get("signature"),
            status=LicenseStatus(str(payload.get("status", "valid")).lower()),
        )
        # Public repo intentionally does not verify cryptographic signatures.
        # TODO(private): delegate signature, revocation, and entitlement checks
        # to the private license service/client.
        if license_obj.signature and edition == LicenseEdition.COMMUNITY:
            return replace(license_obj, status=LicenseStatus.UNSUPPORTED)
        return license_obj

    def validate(self, license_obj: License) -> LicenseStatus:
        return license_obj.normalized_status()
