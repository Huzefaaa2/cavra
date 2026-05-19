from __future__ import annotations

import json
import subprocess
import zipfile
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.evidence import generate_ed25519_keypair
from cavra.release import (
    capture_managed_endpoint_rollout_evidence,
    smoke_test_go_installers,
    validate_go_release_upgrade,
    verify_go_airgap_bundle,
    verify_go_release_package,
)

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
    provenance = json.loads((dist / "cavra-runtime.provenance.intoto.json").read_text(encoding="utf-8"))
    bootstrap = json.loads((dist / "offline-trust-root-bootstrap.json").read_text(encoding="utf-8"))
    installers = json.loads((dist / "cavra-runtime.installers.json").read_text(encoding="utf-8"))
    endpoint_deployment = json.loads((dist / "cavra-runtime.endpoint-deployment.json").read_text(encoding="utf-8"))
    summary = (dist / "release-evidence.md").read_text(encoding="utf-8")

    assert "bin/cavra-runtime_test_linux_amd64" in checksums
    assert "cavra-runtime.endpoint-deployment.json" in checksums
    assert "cavra-runtime.installers.json" in checksums
    assert "cavra-runtime.provenance.intoto.json" in checksums
    assert "offline-trust-root-bootstrap.json" in checksums
    assert sbom["spdxVersion"] == "SPDX-2.3"
    assert {package["name"] for package in sbom["packages"]} >= {"cavra-runtime", "example.com/dependency"}
    assert provenance["_type"] == "https://in-toto.io/Statement/v1"
    assert provenance["predicateType"] == "https://slsa.dev/provenance/v1"
    assert provenance["predicate"]["buildDefinition"]["externalParameters"]["version"] == "v0.1.0-test"
    assert bootstrap["schema_version"] == "cavra.offline-trust-bootstrap.v1"
    assert bootstrap["mode"] == "air_gapped"
    assert "cavra-runtime.endpoint-deployment.json" in bootstrap["required_files"]
    assert "cavra-runtime.installers.json" in bootstrap["required_files"]
    assert "cavra release verify-airgap-bundle cavra-go-runtime-v0.1.0-test.zip" in bootstrap["verification_commands"]
    assert installers["schema_version"] == "cavra.go-runtime.installers.v1"
    assert installers["targets"][0]["target"] == "linux/amd64"
    assert installers["targets"][0]["binary"] == "bin/cavra-runtime_test_linux_amd64"
    assert installers["targets"][0]["verification_command"] == "sha256sum -c checksums.txt"
    assert endpoint_deployment["schema_version"] == "cavra.go-runtime.endpoint-deployment.v1"
    assert endpoint_deployment["source_metadata"] == "cavra-runtime.installers.json"
    assert endpoint_deployment["deployment_targets"][0]["binary"] == "bin/cavra-runtime_test_linux_amd64"
    assert any(
        "cavra release smoke-installers" in command
        for command in endpoint_deployment["deployment_targets"][0]["verification_commands"]
    )
    assert evidence["schema_version"] == "cavra.go-release.evidence.v1"
    assert evidence["dry_run"] is True
    assert evidence["signature_count"] == 0
    assert {artifact["kind"] for artifact in evidence["artifacts"]} >= {
        "go-binary",
        "managed-endpoint-deployment",
        "installer-metadata",
        "sbom",
        "offline-trust-bootstrap",
        "slsa-provenance",
        "checksums",
    }
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
    assert "bin/cavra-runtime_test_linux_amd64" in valid_result.verified_provenance
    assert "bin/cavra-runtime_test_linux_amd64" in valid_result.verified_signatures
    assert "cavra-runtime.endpoint-deployment.json" in valid_result.verified_artifacts
    assert "cavra-runtime.endpoint-deployment.json" in valid_result.verified_provenance
    assert "cavra-runtime.endpoint-deployment.json" in valid_result.verified_signatures
    assert "cavra-runtime.installers.json" in valid_result.verified_artifacts
    assert "cavra-runtime.installers.json" in valid_result.verified_provenance
    assert "cavra-runtime.installers.json" in valid_result.verified_signatures
    assert "cavra-runtime.provenance.intoto.json" in valid_result.verified_signatures
    assert "offline-trust-root-bootstrap.json" in valid_result.verified_signatures
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


def test_go_release_verifier_rejects_missing_installer_metadata(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")

    (dist / "cavra-runtime.installers.json").unlink()

    invalid_result = verify_go_release_package(dist)
    assert not invalid_result.valid
    assert any("missing cavra-runtime.installers.json" in error for error in invalid_result.errors)


def test_go_release_verifier_rejects_missing_endpoint_deployment_metadata(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")

    (dist / "cavra-runtime.endpoint-deployment.json").unlink()

    invalid_result = verify_go_release_package(dist)
    assert not invalid_result.valid
    assert any("missing cavra-runtime.endpoint-deployment.json" in error for error in invalid_result.errors)


def test_go_installer_smoke_validation_accepts_signed_metadata(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")

    valid_result = smoke_test_go_installers(dist, execute_native=False)

    assert valid_result.valid
    assert valid_result.verified_targets == ["linux/amd64", "linux/arm64"]
    cli_result = runner.invoke(app, ["release", "smoke-installers", str(dist), "--skip-execution", "--json"])
    assert cli_result.exit_code == 0
    assert json.loads(cli_result.output)["valid"] is True


def test_managed_endpoint_rollout_evidence_captures_selected_targets(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")
    output = tmp_path / "rollout"

    result = capture_managed_endpoint_rollout_evidence(
        dist,
        output,
        deployment_ids=["github-actions-linux-amd64-runner"],
        rollout_id="chg-123-v0.1.0-test",
        rollout_ring="pilot",
        status="staged",
        actor="release-agent",
        change_record="CHG-123",
    )

    assert result.valid
    assert result.rollout_id == "chg-123-v0.1.0-test"
    assert result.deployment_targets == ["github-actions-linux-amd64-runner"]
    assert set(result.files) == {
        "managed-endpoint-rollout-evidence.json",
        "managed-endpoint-rollout-evidence.md",
        "checksums.txt",
    }
    evidence = json.loads((output / "managed-endpoint-rollout-evidence.json").read_text(encoding="utf-8"))
    assert evidence["schema_version"] == "cavra.go-runtime.endpoint-rollout-evidence.v1"
    assert evidence["status"] == "staged"
    assert evidence["change_record"] == "CHG-123"
    assert evidence["deployment_targets"][0]["id"] == "github-actions-linux-amd64-runner"
    assert "release-evidence.json" in evidence["source_artifacts"]["release_evidence"]["path"]
    assert "managed-endpoint-rollout-evidence.json" in (output / "checksums.txt").read_text(encoding="utf-8")
    cli_result = runner.invoke(
        app,
        [
            "release",
            "capture-rollout",
            str(dist),
            "--output",
            str(tmp_path / "cli-rollout"),
            "--deployment-id",
            "github-actions-linux-amd64-runner",
            "--rollout-id",
            "chg-456-v0.1.0-test",
            "--change-record",
            "CHG-456",
            "--json",
        ],
    )
    assert cli_result.exit_code == 0
    assert json.loads(cli_result.output)["valid"] is True


def test_managed_endpoint_rollout_evidence_rejects_unknown_target(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")

    result = capture_managed_endpoint_rollout_evidence(
        dist,
        tmp_path / "rollout",
        deployment_ids=["unknown-target"],
    )

    assert not result.valid
    assert any("unknown endpoint deployment target: unknown-target" in error for error in result.errors)


def test_airgap_bundle_verifier_accepts_signed_zip_and_rejects_missing_bootstrap(tmp_path: Path, monkeypatch) -> None:
    dist = tmp_path / "go-runtime-v0.1.0-test"
    bin_dir = dist / "bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "cavra-runtime_test_linux_amd64").write_bytes(b"test-binary")
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

    bundle = tmp_path / "cavra-go-runtime-v0.1.0-test.zip"
    _zip_package(dist, bundle)
    valid_result = verify_go_airgap_bundle(bundle)
    assert valid_result.valid
    assert "go-runtime-v0.1.0-test/offline-trust-root-bootstrap.json" in valid_result.verified_members
    assert "offline-trust-root-bootstrap.json" in valid_result.verified_bootstrap
    cli_result = runner.invoke(app, ["release", "verify-airgap-bundle", str(bundle), "--json"])
    assert cli_result.exit_code == 0
    assert json.loads(cli_result.output)["valid"] is True

    (dist / "offline-trust-root-bootstrap.json").unlink()
    missing_bootstrap_bundle = tmp_path / "missing-bootstrap.zip"
    _zip_package(dist, missing_bootstrap_bundle)
    invalid_result = verify_go_airgap_bundle(missing_bootstrap_bundle)
    assert not invalid_result.valid
    assert any("offline-trust-root-bootstrap" in error for error in invalid_result.errors)


def test_airgap_bundle_verifier_rejects_unsafe_zip_members(tmp_path: Path) -> None:
    bundle = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr("../escape.txt", "bad")

    result = verify_go_airgap_bundle(bundle, require_signatures=False, require_provenance=False)

    assert not result.valid
    assert any("unsafe archive member path" in error for error in result.errors)


def test_release_candidate_upgrade_validation_rejects_regressions(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))

    previous = _package_go_runtime(tmp_path, "v0.1.0", "abc123")
    candidate = _package_go_runtime(tmp_path, "v0.2.0-rc.1", "def456")

    valid_result = validate_go_release_upgrade(previous, candidate)
    assert valid_result.valid
    assert valid_result.previous_version == "v0.1.0"
    assert valid_result.candidate_version == "v0.2.0-rc.1"
    assert not valid_result.artifact_changes["removed_binaries"]
    cli_result = runner.invoke(app, ["release", "validate-upgrade", str(previous), str(candidate), "--json"])
    assert cli_result.exit_code == 0
    assert json.loads(cli_result.output)["valid"] is True

    rollback = _package_go_runtime(tmp_path, "v0.0.9", "ghi789")
    invalid_result = validate_go_release_upgrade(previous, rollback)
    assert not invalid_result.valid
    assert any("older than previous version" in error for error in invalid_result.errors)

    reduced_candidate = _package_go_runtime(tmp_path, "v0.2.0-rc.2", "jkl012", targets=("linux_amd64",))
    candidate_regression = validate_go_release_upgrade(previous, reduced_candidate)
    assert not candidate_regression.valid
    assert any("removed Go runtime binary target: linux_arm64" in error for error in candidate_regression.errors)


def test_go_release_workflow_requires_signed_release_artifacts() -> None:
    text = Path(".github/workflows/go-release.yml").read_text(encoding="utf-8")

    assert "Go Runtime Release Package" in text
    assert "contents: write" in text
    assert "go-version-file: go/cavra-runtime/go.mod" in text
    assert "GOOS=" in text
    assert "checksums" in text
    assert "provenance" in text
    assert "scripts/package_go_release.py" in text
    assert "CAVRA_GO_RELEASE_SIGNING_KEY" in text
    assert "--signing-required" in text
    assert "gh release upload" in text
    assert "actions/upload-artifact@v4" in text


def _package_go_runtime(root: Path, version: str, commit: str, *, targets: tuple[str, ...] = ("linux_amd64", "linux_arm64")) -> Path:
    dist = root / f"go-runtime-{version}"
    bin_dir = dist / "bin"
    bin_dir.mkdir(parents=True)
    for target in targets:
        (bin_dir / f"cavra-runtime_{version}_{target}").write_bytes(f"{version}-{target}".encode("utf-8"))
    (dist / "go-modules.json").write_text(
        json.dumps({"Path": "github.com/Huzefaaa2/cavra/go/cavra-runtime", "Version": "main"}) + "\n",
        encoding="utf-8",
    )
    subprocess.run(
        [
            "python3",
            "scripts/package_go_release.py",
            "--dist",
            str(dist),
            "--version",
            version,
            "--commit",
            commit,
            "--ref",
            f"refs/tags/{version}",
            "--event",
            "release",
            "--signing-required",
        ],
        check=True,
    )
    return dist


def _zip_package(package_dir: Path, bundle: Path) -> None:
    with zipfile.ZipFile(bundle, "w") as archive:
        for path in sorted(package_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(package_dir.parent))
