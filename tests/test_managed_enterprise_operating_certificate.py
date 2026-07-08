from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_operating_certificate import (
    REQUIRED_CERTIFICATE_SECTIONS,
    REQUIRED_SIGNOFFS,
    build_managed_enterprise_operating_certificate,
    validate_managed_enterprise_operating_certificate,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_operating_certificate_warns_without_blocking_shape() -> None:
    certificate = build_managed_enterprise_operating_certificate(evidence_mode="sample")

    result = validate_managed_enterprise_operating_certificate(certificate)

    assert result["ready_for_managed_enterprise_operating_certificate"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["section_count"] == len(REQUIRED_CERTIFICATE_SECTIONS)
    assert result["signoff_count"] == len(REQUIRED_SIGNOFFS)


def test_live_operating_certificate_is_ready() -> None:
    certificate = build_managed_enterprise_operating_certificate(evidence_mode="live")

    result = validate_managed_enterprise_operating_certificate(certificate, require_live=True)

    assert result["ready_for_managed_enterprise_operating_certificate"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["section_count"] == result["required_section_count"]
    assert result["signoff_count"] == result["required_signoff_count"]


def test_require_live_rejects_sample_operating_certificate() -> None:
    certificate = build_managed_enterprise_operating_certificate(evidence_mode="sample")

    result = validate_managed_enterprise_operating_certificate(certificate, require_live=True)

    assert result["ready_for_managed_enterprise_operating_certificate"] is False
    assert result["blocker_count"] == 1


def test_missing_certificate_section_blocks_readiness() -> None:
    certificate = build_managed_enterprise_operating_certificate(evidence_mode="live")
    certificate["certificate_sections"] = [
        section
        for section in certificate["certificate_sections"]
        if section["section_id"] != "trust_controls"
    ]

    result = validate_managed_enterprise_operating_certificate(certificate, require_live=True)

    assert result["ready_for_managed_enterprise_operating_certificate"] is False
    assert result["blocker_count"] == 1
    section_check = next(check for check in result["checks"] if check["name"] == "certificate_sections")
    assert "trust_controls" in section_check["message"]


def test_missing_certificate_signoff_blocks_readiness() -> None:
    certificate = build_managed_enterprise_operating_certificate(evidence_mode="live")
    certificate["signoffs"] = [
        signoff
        for signoff in certificate["signoffs"]
        if signoff["signoff_id"] != "security_owner"
    ]

    result = validate_managed_enterprise_operating_certificate(certificate, require_live=True)

    assert result["ready_for_managed_enterprise_operating_certificate"] is False
    assert result["blocker_count"] == 1
    signoff_check = next(check for check in result["checks"] if check["name"] == "signoffs")
    assert "security_owner" in signoff_check["message"]


def test_unsafe_operating_certificate_reference_blocks_readiness() -> None:
    certificate = build_managed_enterprise_operating_certificate(evidence_mode="live")
    certificate["certificate_outcome"]["public_safe_claims_ref"] = "https://example.com/raw-claims"

    result = validate_managed_enterprise_operating_certificate(certificate, require_live=True)

    assert result["ready_for_managed_enterprise_operating_certificate"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_operating_certificate_readiness() -> None:
    certificate = build_managed_enterprise_operating_certificate(evidence_mode="live")
    certificate["tenant_name"] = "do-not-commit"

    result = validate_managed_enterprise_operating_certificate(certificate, require_live=True)

    assert result["ready_for_managed_enterprise_operating_certificate"] is False
    assert result["blocker_count"] == 1


def test_operating_certificate_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-certificate"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_certificate.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_certificate = export_dir / "managed-enterprise-operating-certificate.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_certificate.py",
            "--certificate",
            str(live_certificate),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_operating_certificate_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-certificate"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-certificate",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_certificate = export_dir / "managed-enterprise-operating-certificate.live.sanitized.example.json"
    assert live_certificate.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-certificate",
            "--certificate",
            str(live_certificate),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_operating_certificate": true' in validate_result.output


def test_operating_certificate_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_certificate = tmp_path / "sample-certificate.json"
    sample_certificate.write_text(
        json.dumps(build_managed_enterprise_operating_certificate(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-certificate",
            "--certificate",
            str(sample_certificate),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
