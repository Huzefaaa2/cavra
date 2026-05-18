from __future__ import annotations

import json
import subprocess
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.evidence import generate_ed25519_keypair
from cavra.release import verify_go_release_package

runner = CliRunner()


def test_go_release_packaging_creates_sbom_checksums_and_evidence(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    bin_dir = dist / "bin"
    bin_dir.mkdir(parents=True)
    binary = bin_dir / "cavra-runtime_test_linux_amd64"
    binary.write_bytes(b"test-binary")
    (dist / "go-modules.json").write_text(
        "\n".join(
            [
                json.dumps({"Path": "github.com/Huzefaaa2/cavra/go/cavra-runtime", "Version": "main"}),
                json.dumps({"Path": "example.com/dependency", "Version": "v1.2.3"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            "python3",
            "scripts/package_go_release.py",
            "--dist",
            str(dist),
            "--version",
            "v0.1.0-test",
            "--commit",
            "abc123",
            "--ref",
            "refs/tags/v0.1.0-test",
            "--event",
            "workflow_dispatch",
            "--dry-run",
        ],
        check=True,
    )

    checksums = (dist / "checksums.txt").read_text(encoding="utf-8")
    sbom = json.loads((dist / "cavra-runtime.sbom.spdx.json").read_text(encoding="utf-8"))
    evidence = json.loads((dist / "release-evidence.json").read_text(encoding="utf-8"))
    summary = (dist / "release-evidence.md").read_text(encoding="utf-8")

    assert "bin/cavra-runtime_test_linux_amd64" in checksums
    assert sbom["spdxVersion"] == "SPDX-2.3"
    assert {package["name"] for package in sbom["packages"]} >= {"cavra-runtime", "example.com/dependency"}
    assert evidence["schema_version"] == "cavra.go-release.evidence.v1"
    assert evidence["dry_run"] is True
    assert evidence["signature_count"] == 0
    assert {artifact["kind"] for artifact in evidence["artifacts"]} >= {"go-binary", "sbom", "checksums"}
    assert "No signing key was provided" in summary


def test_go_release_verifier_accepts_signed_package_and_rejects_tampering(tmp_path: Path, monkeypatch) -> None:
    dist = tmp_path / "dist"
    bin_dir = dist / "bin"
    bin_dir.mkdir(parents=True)
    binary = bin_dir / "cavra-runtime_test_linux_amd64"
    binary.write_bytes(b"test-binary")
    (dist / "go-modules.json").write_text(
        json.dumps({"Path": "github.com/Huzefaaa2/cavra/go/cavra-runtime", "Version": "main"}) + "\n",
        encoding="utf-8",
    )
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))

    subprocess.run(
        [
            "python3",
            "scripts/package_go_release.py",
            "--dist",
            str(dist),
            "--version",
            "v0.1.0-test",
            "--commit",
            "abc123",
            "--ref",
            "refs/tags/v0.1.0-test",
            "--event",
            "release",
            "--signing-required",
        ],
        check=True,
    )

    valid_result = verify_go_release_package(dist)
    assert valid_result.valid
    assert "bin/cavra-runtime_test_linux_amd64" in valid_result.verified_artifacts
    assert "bin/cavra-runtime_test_linux_amd64" in valid_result.verified_signatures
    assert "release-evidence.json" in valid_result.verified_signatures
    cli_result = runner.invoke(app, ["release", "verify-go-package", str(dist), "--json"])
    assert cli_result.exit_code == 0
    assert json.loads(cli_result.output)["valid"] is True

    binary.write_bytes(b"tampered-binary")

    invalid_result = verify_go_release_package(dist)
    assert not invalid_result.valid
    assert any("checksum mismatch" in error for error in invalid_result.errors)
    cli_invalid_result = runner.invoke(app, ["release", "verify-go-package", str(dist)])
    assert cli_invalid_result.exit_code == 1


def test_go_release_workflow_requires_signed_release_artifacts() -> None:
    text = Path(".github/workflows/go-release.yml").read_text(encoding="utf-8")

    assert "Go Runtime Release Package" in text
    assert "contents: write" in text
    assert "go-version-file: go/cavra-runtime/go.mod" in text
    assert "GOOS=" in text
    assert "checksums" in text
    assert "scripts/package_go_release.py" in text
    assert "CAVRA_GO_RELEASE_SIGNING_KEY" in text
    assert "--signing-required" in text
    assert "gh release upload" in text
    assert "actions/upload-artifact@v4" in text
