from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cavra.config.features import explain_locked_feature, is_feature_enabled, list_available_features
from cavra.edition.community import ENTERPRISE_MESSAGE, current_edition, require_enterprise
from cavra.edition.enterprise_hooks import EnterpriseFeatureUnavailable, is_enterprise_available, load_enterprise_feature
from cavra.licensing.license_client import LocalLicenseClient
from cavra.licensing.license_types import LicenseEdition, LicenseStatus
from cavra.licensing.trial_mode import TrialMode
from cavra.plugin_runtime.loader import PluginLoadError, load_plugin, read_manifest


def test_community_mode_is_default_and_requires_no_license() -> None:
    license_obj = LocalLicenseClient().load(None)

    assert current_edition({}) == "community"
    assert license_obj.edition == LicenseEdition.COMMUNITY
    assert LocalLicenseClient().validate(license_obj) == LicenseStatus.VALID


def test_enterprise_feature_returns_friendly_community_message() -> None:
    response = require_enterprise("sso")

    assert response["allowed"] is False
    assert response["reason"] == ENTERPRISE_MESSAGE
    assert is_enterprise_available("cavra_enterprise_missing_for_test") is False
    try:
        load_enterprise_feature("sso", package_name="cavra_enterprise_missing_for_test")
    except EnterpriseFeatureUnavailable as exc:
        assert str(exc) == ENTERPRISE_MESSAGE
    else:
        raise AssertionError("expected unavailable enterprise feature")


def test_feature_registry_separates_community_and_enterprise_features() -> None:
    assert is_feature_enabled("local_scan", "community") is True
    assert is_feature_enabled("sso", "community") is False
    available = list_available_features("community")
    assert "local_scan" in available["enabled"]
    assert "sso" in available["locked"]
    assert explain_locked_feature("sso").reason == ENTERPRISE_MESSAGE


def test_plugin_loader_rejects_enterprise_plugin_in_community(tmp_path: Path) -> None:
    manifest_path = tmp_path / "plugin.json"
    manifest_path.write_text(
        json.dumps(
            {
                "name": "private-rbac",
                "version": "1.0.0",
                "edition_required": "enterprise",
                "entrypoint": "cavra_enterprise.rbac:Plugin",
                "permissions": ["rbac:read"],
            }
        ),
        encoding="utf-8",
    )
    manifest = read_manifest(manifest_path)

    try:
        load_plugin(manifest, edition="community")
    except PluginLoadError as exc:
        assert str(exc) == ENTERPRISE_MESSAGE
    else:
        raise AssertionError("expected enterprise plugin to be blocked")


def test_trial_license_mock_loads_safely(tmp_path: Path) -> None:
    expires_at = (datetime.now(timezone.utc) + timedelta(days=14)).isoformat()
    license_path = tmp_path / "trial.json"
    license_path.write_text(
        json.dumps(
            {
                "license_id": "trial-local-placeholder",
                "edition": "trial",
                "customer_name": "Example Trial",
                "expires_at": expires_at,
                "features": ["sso"],
                "status": "valid",
            }
        ),
        encoding="utf-8",
    )
    license_obj = LocalLicenseClient().load(license_path)
    trial = TrialMode(license_obj)

    assert trial.active is True
    assert trial.days_remaining() >= 13
    assert "private CAVRA license service" in trial.validation_note()
    assert is_feature_enabled("sso", "trial", license_obj) is True


def test_boundary_validation_script_detects_risky_terms(tmp_path: Path) -> None:
    risky = tmp_path / "src"
    risky.mkdir()
    (risky / "bad.py").write_text("ENTERPRISE_PRIVATE_KEY = 'do-not-commit'\n", encoding="utf-8")

    result = subprocess.run(
        ["bash", "scripts/validate-boundaries.sh", str(tmp_path)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "public boundary validation failed" in result.stderr
