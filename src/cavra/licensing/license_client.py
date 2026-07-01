from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from cavra.licensing.license_types import License, LicenseEdition, LicenseStatus, LicenseValidationReport


class LocalLicenseClient:
    """Public-safe license reader with local mock validation only.

    Real online validation, signing-key verification, revocation checks, billing
    state, and tenant entitlement lookup must be implemented in the private
    CAVRA Managed or commercial entitlement service.
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
        try:
            edition = LicenseEdition(str(payload.get("edition", "community")).lower())
        except ValueError:
            return License(
                license_id=str(payload.get("license_id", "")),
                edition=LicenseEdition.COMMUNITY,
                customer_name=str(payload.get("customer_name", "")),
                status=LicenseStatus.INVALID,
            )
        features = tuple(str(item) for item in payload.get("features", []) if item)
        try:
            status = LicenseStatus(str(payload.get("status", "valid")).lower())
        except ValueError:
            status = LicenseStatus.INVALID
        license_obj = License(
            license_id=str(payload.get("license_id", "")),
            edition=edition,
            customer_name=str(payload.get("customer_name", "")),
            expires_at=payload.get("expires_at"),
            features=features,
            signature=payload.get("signature"),
            status=status,
        )
        # Public repo intentionally does not verify cryptographic signatures.
        # TODO(private): delegate signature, revocation, and entitlement checks
        # to the private license service/client.
        if license_obj.signature and edition == LicenseEdition.COMMUNITY:
            return replace(license_obj, status=LicenseStatus.UNSUPPORTED)
        return license_obj

    def validate(self, license_obj: License) -> LicenseStatus:
        return license_obj.normalized_status()

    def validation_report(self, license_obj: License) -> LicenseValidationReport:
        status = self.validate(license_obj)
        private_required = license_obj.edition != LicenseEdition.COMMUNITY
        if status == LicenseStatus.VALID and private_required:
            message = (
                "Local validation accepted the public entitlement shape. Real commercial entitlement, "
                "signature, revocation, managed service, billing, and tenant checks require the private CAVRA Managed or entitlement service."
            )
        elif status == LicenseStatus.VALID:
            message = "CAVRA Community is valid and does not require a license key for local or self-hosted use."
        elif status == LicenseStatus.EXPIRED:
            message = "License is expired."
        elif status == LicenseStatus.UNSUPPORTED:
            message = "License payload is unsupported by the public CAVRA Community client."
        elif status in {LicenseStatus.REVOKED, LicenseStatus.SUSPENDED}:
            message = f"License is {status.value}; private validation is required before use."
        else:
            message = "License payload is invalid."
        return LicenseValidationReport(
            status=status,
            edition=license_obj.edition,
            license_id=license_obj.license_id,
            valid=status == LicenseStatus.VALID,
            message=message,
            private_validation_required=private_required,
            enabled_features=license_obj.features if status == LicenseStatus.VALID else (),
            locked_features=() if status == LicenseStatus.VALID else license_obj.features,
        )
