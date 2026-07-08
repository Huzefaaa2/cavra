from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_certificate_publication_index import (
    REQUIRED_PUBLIC_SAFE_CLAIMS,
    REQUIRED_PUBLICATION_CHANNELS,
    build_managed_enterprise_certificate_publication_index,
    validate_managed_enterprise_certificate_publication_index,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_certificate_publication_index_warns_without_blocking_shape() -> None:
    index = build_managed_enterprise_certificate_publication_index(evidence_mode="sample")

    result = validate_managed_enterprise_certificate_publication_index(index)

    assert result["ready_for_managed_enterprise_certificate_publication"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["channel_count"] == len(REQUIRED_PUBLICATION_CHANNELS)
    assert result["claim_count"] == len(REQUIRED_PUBLIC_SAFE_CLAIMS)


def test_live_certificate_publication_index_is_ready() -> None:
    index = build_managed_enterprise_certificate_publication_index(evidence_mode="live")

    result = validate_managed_enterprise_certificate_publication_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_certificate_publication"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["channel_count"] == result["required_channel_count"]
    assert result["claim_count"] == result["required_claim_count"]


def test_require_live_rejects_sample_certificate_publication_index() -> None:
    index = build_managed_enterprise_certificate_publication_index(evidence_mode="sample")

    result = validate_managed_enterprise_certificate_publication_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_certificate_publication"] is False
    assert result["blocker_count"] == 1


def test_missing_publication_channel_blocks_readiness() -> None:
    index = build_managed_enterprise_certificate_publication_index(evidence_mode="live")
    index["publication_channels"] = [
        channel
        for channel in index["publication_channels"]
        if channel["channel_id"] != "github_wiki"
    ]

    result = validate_managed_enterprise_certificate_publication_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_certificate_publication"] is False
    assert result["blocker_count"] == 1
    channel_check = next(check for check in result["checks"] if check["name"] == "publication_channels")
    assert "github_wiki" in channel_check["message"]


def test_missing_public_safe_claim_blocks_readiness() -> None:
    index = build_managed_enterprise_certificate_publication_index(evidence_mode="live")
    index["public_safe_claims"] = [
        claim
        for claim in index["public_safe_claims"]
        if claim["claim_id"] != "support_path_active"
    ]

    result = validate_managed_enterprise_certificate_publication_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_certificate_publication"] is False
    assert result["blocker_count"] == 1
    claim_check = next(check for check in result["checks"] if check["name"] == "public_safe_claims")
    assert "support_path_active" in claim_check["message"]


def test_unsafe_publication_reference_blocks_readiness() -> None:
    index = build_managed_enterprise_certificate_publication_index(evidence_mode="live")
    index["publication_outcome"]["support_contact_ref"] = "https://example.com/raw-contact"

    result = validate_managed_enterprise_certificate_publication_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_certificate_publication"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_certificate_publication_readiness() -> None:
    index = build_managed_enterprise_certificate_publication_index(evidence_mode="live")
    index["raw_contracts"] = ["do-not-commit"]

    result = validate_managed_enterprise_certificate_publication_index(index, require_live=True)

    assert result["ready_for_managed_enterprise_certificate_publication"] is False
    assert result["blocker_count"] == 1


def test_certificate_publication_index_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-certificate-publication-index"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_certificate_publication_index.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_index = export_dir / "managed-enterprise-certificate-publication-index.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_certificate_publication_index.py",
            "--index",
            str(live_index),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_certificate_publication_index_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-certificate-publication-index"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-certificate-publication-index",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_index = export_dir / "managed-enterprise-certificate-publication-index.live.sanitized.example.json"
    assert live_index.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-certificate-publication-index",
            "--index",
            str(live_index),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_certificate_publication": true' in validate_result.output


def test_certificate_publication_index_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_index = tmp_path / "sample-index.json"
    sample_index.write_text(
        json.dumps(
            build_managed_enterprise_certificate_publication_index(evidence_mode="sample"),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-certificate-publication-index",
            "--index",
            str(sample_index),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"blocker_count": 1' in result.output
