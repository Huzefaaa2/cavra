from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.managed_enterprise_operating_chain import (
    REQUIRED_CHAIN_ARTIFACTS,
    build_managed_enterprise_operating_chain_manifest,
    validate_managed_enterprise_operating_chain,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


def test_sample_operating_chain_warns_without_blocking_shape() -> None:
    manifest = build_managed_enterprise_operating_chain_manifest(evidence_mode="sample")

    result = validate_managed_enterprise_operating_chain(manifest, base_dir=REPO_ROOT)

    assert result["ready_for_managed_enterprise_operating_chain"] is False
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 1
    assert result["artifact_count"] == len(REQUIRED_CHAIN_ARTIFACTS)


def test_live_operating_chain_is_ready() -> None:
    manifest = build_managed_enterprise_operating_chain_manifest(evidence_mode="live")

    result = validate_managed_enterprise_operating_chain(manifest, base_dir=REPO_ROOT, require_live=True)

    assert result["ready_for_managed_enterprise_operating_chain"] is True
    assert result["blocker_count"] == 0
    assert result["warning_count"] == 0
    assert result["artifact_count"] == result["required_artifact_count"]
    assert all(artifact["ready"] is True for artifact in result["artifact_results"].values())


def test_require_live_rejects_sample_operating_chain() -> None:
    manifest = build_managed_enterprise_operating_chain_manifest(evidence_mode="sample")

    result = validate_managed_enterprise_operating_chain(manifest, base_dir=REPO_ROOT, require_live=True)

    assert result["ready_for_managed_enterprise_operating_chain"] is False
    assert result["blocker_count"] >= 1


def test_missing_chain_artifact_blocks_readiness() -> None:
    manifest = build_managed_enterprise_operating_chain_manifest(evidence_mode="live")
    manifest["artifact_paths"]["operating_announcement_path"] = "examples/missing/announcement.json"

    result = validate_managed_enterprise_operating_chain(manifest, base_dir=REPO_ROOT, require_live=True)

    assert result["ready_for_managed_enterprise_operating_chain"] is False
    assert result["blocker_count"] == 1
    assert result["artifact_results"]["operating_announcement"]["ready"] is False


def test_unsafe_chain_artifact_path_blocks_readiness() -> None:
    manifest = build_managed_enterprise_operating_chain_manifest(evidence_mode="live")
    manifest["artifact_paths"]["cutover_runbook_path"] = "../private/cutover.json"

    result = validate_managed_enterprise_operating_chain(manifest, base_dir=REPO_ROOT, require_live=True)

    assert result["ready_for_managed_enterprise_operating_chain"] is False
    assert result["blocker_count"] == 1


def test_forbidden_private_material_blocks_operating_chain_readiness() -> None:
    manifest = build_managed_enterprise_operating_chain_manifest(evidence_mode="live")
    manifest["tenant_name"] = "do-not-commit"

    result = validate_managed_enterprise_operating_chain(manifest, base_dir=REPO_ROOT, require_live=True)

    assert result["ready_for_managed_enterprise_operating_chain"] is False
    assert result["blocker_count"] == 1


def test_operating_chain_script_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-chain"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_chain.py",
            "--export-dir",
            str(export_dir),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    live_manifest = export_dir / "managed-enterprise-operating-chain.live.sanitized.example.json"
    subprocess.run(
        [
            "python3",
            "scripts/validate_managed_enterprise_operating_chain.py",
            "--manifest",
            str(live_manifest),
            "--repo-root",
            str(REPO_ROOT),
            "--require-live",
        ],
        cwd=REPO_ROOT,
        check=True,
    )


def test_operating_chain_cli_exports_and_validates(tmp_path: Path) -> None:
    export_dir = tmp_path / "managed-enterprise-operating-chain"
    export_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-chain",
            "--export-dir",
            str(export_dir),
        ],
    )

    assert export_result.exit_code == 0, export_result.output
    live_manifest = export_dir / "managed-enterprise-operating-chain.live.sanitized.example.json"
    assert live_manifest.exists()

    validate_result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-chain",
            "--manifest",
            str(live_manifest),
            "--repo-root",
            str(REPO_ROOT),
            "--require-live",
        ],
    )

    assert validate_result.exit_code == 0, validate_result.output
    assert '"ready_for_managed_enterprise_operating_chain": true' in validate_result.output


def test_operating_chain_cli_rejects_sample_when_live_required(tmp_path: Path) -> None:
    sample_manifest = tmp_path / "sample-manifest.json"
    sample_manifest.write_text(
        json.dumps(build_managed_enterprise_operating_chain_manifest(evidence_mode="sample"), indent=2) + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "release",
            "managed-enterprise-operating-chain",
            "--manifest",
            str(sample_manifest),
            "--repo-root",
            str(REPO_ROOT),
            "--require-live",
        ],
    )

    assert result.exit_code == 1
    assert '"ready_for_managed_enterprise_operating_chain": false' in result.output
