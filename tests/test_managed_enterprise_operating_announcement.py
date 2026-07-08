from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_operating_announcement import (
    REQUIRED_ANNOUNCEMENT_SECTIONS,
    REQUIRED_CHANNELS,
    build_managed_enterprise_operating_announcement,
    validate_managed_enterprise_operating_announcement,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_operating_announcement_warns_without_blocking_shape() -> None:
    announcement = build_managed_enterprise_operating_announcement(evidence_mode="sample")

    result = validate_managed_enterprise_operating_announcement(announcement)

    assert result["ready_for_managed_enterprise_operating_announcement"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["section_count"] == len(REQUIRED_ANNOUNCEMENT_SECTIONS)
    assert result["channel_count"] == len(REQUIRED_CHANNELS)


def test_live_operating_announcement_is_ready() -> None:
    announcement = build_managed_enterprise_operating_announcement(evidence_mode="live")

    result = validate_managed_enterprise_operating_announcement(announcement, require_live=True)

    assert result["ready_for_managed_enterprise_operating_announcement"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["section_count"] == result["required_section_count"]
    assert result["channel_count"] == result["required_channel_count"]


def test_require_live_rejects_sample_operating_announcement() -> None:
    announcement = build_managed_enterprise_operating_announcement(evidence_mode="sample")

    result = validate_managed_enterprise_operating_announcement(announcement, require_live=True)

    assert result["ready_for_managed_enterprise_operating_announcement"] is False
    assert result["blocker_count"] == 1


def test_missing_announcement_section_blocks_readiness() -> None:
    announcement = build_managed_enterprise_operating_announcement(evidence_mode="live")
    announcement["announcement_sections"] = [
        section
        for section in announcement["announcement_sections"]
        if section["section_id"] != "security_and_trust"
    ]

    result = validate_managed_enterprise_operating_announcement(announcement, require_live=True)

    assert result["ready_for_managed_enterprise_operating_announcement"] is False
    assert result["blocker_count"] == 1
    section_check = next(check for check in result["checks"] if check["name"] == "announcement_sections")
    assert "security_and_trust" in section_check["message"]


def test_missing_publication_channel_blocks_readiness() -> None:
    announcement = build_managed_enterprise_operating_announcement(evidence_mode="live")
    announcement["publication_channels"] = [
        channel
        for channel in announcement["publication_channels"]
        if channel["channel_id"] != "github_wiki"
    ]

    result = validate_managed_enterprise_operating_announcement(announcement, require_live=True)

    assert result["ready_for_managed_enterprise_operating_announcement"] is False
    assert result["blocker_count"] == 1
    channel_check = next(check for check in result["checks"] if check["name"] == "publication_channels")
    assert "github_wiki" in channel_check["message"]


def test_unsafe_operating_announcement_reference_blocks_readiness() -> None:
    announcement = build_managed_enterprise_operating_announcement(evidence_mode="live")
    announcement["announcement_outcome"]["support_contact_ref"] = "https://example.com/raw-contact"

    result = validate_managed_enterprise_operating_announcement(announcement, require_live=True)

    assert result["ready_for_managed_enterprise_operating_announcement"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_operating_announcement_readiness() -> None:
    announcement = build_managed_enterprise_operating_announcement(evidence_mode="live")
    announcement["raw_contracts"] = ["do-not-commit"]

    result = validate_managed_enterprise_operating_announcement(announcement, require_live=True)

    assert result["ready_for_managed_enterprise_operating_announcement"] is False
    assert result["blocker_count"] == 1


def test_operating_announcement_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-announcement"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_announcement.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_announcement = export_dir / "managed-enterprise-operating-announcement.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_announcement.py",
            "--announcement",
            str(live_announcement),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_operating_announcement_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-announcement"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-announcement",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_announcement = export_dir / "managed-enterprise-operating-announcement.live.sanitized.example.json"
    assert live_announcement.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-announcement",
            "--announcement",
            str(live_announcement),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_operating_announcement": true' in validate_result.output


def test_operating_announcement_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_announcement = tmp_path / "sample-announcement.json"
    sample_announcement.write_text(
        json.dumps(build_managed_enterprise_operating_announcement(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-announcement",
            "--announcement",
            str(sample_announcement),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
