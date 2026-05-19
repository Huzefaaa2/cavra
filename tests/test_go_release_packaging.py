from __future__ import annotations

import json
import subprocess
import zipfile
from pathlib import Path

from typer.testing import CliRunner

from cavra.approvals import ApprovalStore, create_approval_request
from cavra.cli import app
from cavra.evidence import generate_ed25519_keypair
from cavra.release import (
    build_managed_endpoint_rollout_rollback_execution_metadata,
    capture_managed_endpoint_rollout_evidence,
    create_managed_endpoint_rollout_rollback_execution,
    create_managed_endpoint_rollout_promotion_execution,
    create_managed_endpoint_rollout_promotion_request,
    export_rollout_promotion_execution_audit,
    smoke_test_go_installers,
    validate_go_release_upgrade,
    verify_managed_endpoint_rollout_evidence,
    verify_go_airgap_bundle,
    verify_go_release_package,
    verify_rollout_promotion_request_signature,
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


def test_managed_endpoint_rollout_evidence_verifies_and_indexes_metadata(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")
    rollout_dir = tmp_path / "rollout"
    capture_managed_endpoint_rollout_evidence(
        dist,
        rollout_dir,
        deployment_ids=["github-actions-linux-amd64-runner"],
        rollout_id="chg-123-v0.1.0-test",
        rollout_ring="pilot",
        status="staged",
        actor="release-agent",
        change_record="CHG-123",
    )

    result = verify_managed_endpoint_rollout_evidence(rollout_dir)

    assert result.valid
    assert result.rollout_id == "chg-123-v0.1.0-test"
    assert result.verified_artifacts == [
        "managed-endpoint-rollout-evidence.json",
        "managed-endpoint-rollout-evidence.md",
    ]
    assert result.metadata["metadata_kind"] == "managed-endpoint-rollout"
    assert result.metadata["session_id"] == "chg-123-v0.1.0-test"
    assert result.metadata["deployment_targets"] == ["github-actions-linux-amd64-runner"]

    metadata_json = tmp_path / "metadata.json"
    sqlite = tmp_path / "metadata.db"
    cli_result = runner.invoke(
        app,
        [
            "release",
            "verify-rollout",
            str(rollout_dir),
            "--metadata-json",
            str(metadata_json),
            "--sqlite",
            str(sqlite),
            "--json",
        ],
    )

    assert cli_result.exit_code == 0
    payload = json.loads(cli_result.output)
    assert payload["valid"] is True
    assert str(metadata_json) in payload["indexed_metadata_stores"]
    assert json.loads(metadata_json.read_text(encoding="utf-8"))["items"][0]["session_id"] == "chg-123-v0.1.0-test"


def test_managed_endpoint_rollout_evidence_rejects_checksum_tampering(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")
    rollout_dir = tmp_path / "rollout"
    capture_managed_endpoint_rollout_evidence(
        dist,
        rollout_dir,
        deployment_ids=["github-actions-linux-amd64-runner"],
        rollout_id="chg-123-v0.1.0-test",
    )

    evidence_path = rollout_dir / "managed-endpoint-rollout-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["status"] = "succeeded"
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    result = verify_managed_endpoint_rollout_evidence(rollout_dir)

    assert not result.valid
    assert any("rollout checksum mismatch" in error for error in result.errors)


def test_managed_endpoint_rollout_promotion_request_is_signed_and_persisted(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")
    rollout_dir = tmp_path / "rollout"
    capture_managed_endpoint_rollout_evidence(
        dist,
        rollout_dir,
        deployment_ids=["github-actions-linux-amd64-runner"],
        rollout_id="chg-123-v0.1.0-test",
        rollout_ring="pilot",
        status="staged",
        actor="release-agent",
        change_record="CHG-123",
    )

    result = create_managed_endpoint_rollout_promotion_request(
        rollout_dir,
        output_dir=tmp_path / "promotion",
        target_ring="production",
        requested_by="release-manager",
        signing_key_pem=private_key.read_text(encoding="utf-8"),
    )

    assert result.valid
    assert result.approval["state"] == "pending"
    assert result.approval["approver_group"] == "Change Advisory Board"
    assert result.request["target_ring"] == "production"
    assert result.request["signature"]["algorithm"] == "Ed25519"
    verify_rollout_promotion_request_signature(result.request)
    assert set(result.files) == {
        "rollout-promotion-approval-request.json",
        "rollout-promotion-approval-request.md",
    }

    approval_json = tmp_path / "approvals.json"
    cli_result = runner.invoke(
        app,
        [
            "release",
            "request-rollout-promotion",
            str(rollout_dir),
            "--output",
            str(tmp_path / "cli-promotion"),
            "--target-ring",
            "production",
            "--approval-store",
            str(approval_json),
            "--json",
        ],
    )

    assert cli_result.exit_code == 0
    payload = json.loads(cli_result.output)
    assert payload["valid"] is True
    assert payload["request"]["signature"]["algorithm"] == "Ed25519"
    assert json.loads(approval_json.read_text(encoding="utf-8"))["items"][0]["state"] == "pending"


def test_managed_endpoint_rollout_promotion_execution_requires_approved_request(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")
    rollout_dir = tmp_path / "rollout"
    capture_managed_endpoint_rollout_evidence(
        dist,
        rollout_dir,
        deployment_ids=["github-actions-linux-amd64-runner"],
        rollout_id="chg-123-v0.1.0-test",
        rollout_ring="pilot",
        status="staged",
        change_record="CHG-123",
    )
    request_result = create_managed_endpoint_rollout_promotion_request(
        rollout_dir,
        output_dir=tmp_path / "promotion-request",
        target_ring="production",
        signing_key_pem=private_key.read_text(encoding="utf-8"),
    )
    pending_result = create_managed_endpoint_rollout_promotion_execution(
        request_result.request,
        request_result.approval,
        output_dir=tmp_path / "pending-execution",
    )
    assert not pending_result.valid
    assert "rollout promotion execution requires an approved approval record" in pending_result.errors

    approval_store = ApprovalStore(tmp_path / "approvals.json")
    approval_store.upsert(request_result.approval)
    approved = approval_store.decide(
        request_result.approval["approval_id"],
        state="approved",
        actor="cab@example.com",
        reason="Validated staged rollout evidence.",
    )
    result = create_managed_endpoint_rollout_promotion_execution(
        request_result.request,
        approved,
        output_dir=tmp_path / "promotion-execution",
        executed_by="release-manager",
    )

    assert result.valid
    assert result.execution["schema_version"] == "cavra.go-runtime.endpoint-rollout-promotion-execution.v1"
    assert result.execution["ring_advancement"] == {
        "from": "pilot",
        "to": "production",
        "previous_rollout_status": "staged",
        "new_rollout_status": "promoted",
    }
    assert "promotion-request-signature-verified" in result.execution["controls"]
    assert result.execution["rollback_evidence_refs"]
    assert set(result.files) == {"rollout-promotion-execution.json", "rollout-promotion-execution.md"}

    metadata_json = tmp_path / "execution-metadata.json"
    cli_result = runner.invoke(
        app,
        [
            "release",
            "execute-rollout-promotion",
            str(tmp_path / "promotion-request" / "rollout-promotion-approval-request.json"),
            "--approval-store",
            str(tmp_path / "approvals.json"),
            "--output",
            str(tmp_path / "cli-promotion-execution"),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )

    assert cli_result.exit_code == 0
    payload = json.loads(cli_result.output)
    assert payload["valid"] is True
    assert payload["execution"]["approval"]["state"] == "approved"
    assert str(metadata_json) in payload["indexed_metadata_stores"]
    metadata = json.loads(metadata_json.read_text(encoding="utf-8"))["items"][0]
    assert metadata["metadata_kind"] == "rollout-promotion-execution"
    assert metadata["rollout_status"] == "promoted"
    assert metadata["target_ring"] == "production"
    assert metadata["rollback_evidence_refs"]


def test_managed_endpoint_rollout_rollback_execution_and_audit_exports(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")
    rollout_dir = tmp_path / "rollout"
    capture_managed_endpoint_rollout_evidence(
        dist,
        rollout_dir,
        deployment_ids=["github-actions-linux-amd64-runner"],
        rollout_id="chg-123-v0.1.0-test",
        rollout_ring="pilot",
        status="staged",
        change_record="CHG-123",
    )
    request_result = create_managed_endpoint_rollout_promotion_request(
        rollout_dir,
        output_dir=tmp_path / "promotion-request",
        target_ring="production",
        signing_key_pem=private_key.read_text(encoding="utf-8"),
    )
    approval_store = ApprovalStore(tmp_path / "approvals.json")
    approval_store.upsert(request_result.approval)
    approved_promotion = approval_store.decide(
        request_result.approval["approval_id"],
        state="approved",
        actor="cab@example.com",
        reason="Validated staged rollout evidence.",
    )
    promotion = create_managed_endpoint_rollout_promotion_execution(
        request_result.request,
        approved_promotion,
        output_dir=tmp_path / "promotion-execution",
        executed_by="release-manager",
    )
    rollback_decision = {
        "decision_id": "rollback-decision",
        "session_id": promotion.execution["rollout_id"],
        "correlation_id": promotion.execution["execution_id"],
        "action_type": "release_rollback_endpoint_rollout",
        "target": promotion.execution["rollout_id"],
        "decision": "require_approval",
        "severity": "high",
        "rule_id": "release.rollout.rollback.require_approval",
        "reason": "Rollback requires approved change control.",
        "actor": "release-manager",
        "metadata": {
            "promotion_execution_id": promotion.execution["execution_id"],
            "target_ring": "production",
        },
    }
    rollback_approval = create_approval_request(rollback_decision, approver_group="Change Advisory Board")
    approval_store.upsert(rollback_approval)
    approved_rollback = approval_store.decide(
        rollback_approval["approval_id"],
        state="approved",
        actor="cab@example.com",
        reason="Rollback approved.",
    )

    result = create_managed_endpoint_rollout_rollback_execution(
        promotion.execution,
        approved_rollback,
        output_dir=tmp_path / "rollback-execution",
        executed_by="release-manager",
        rollback_reason="Production validation failed.",
    )

    assert result.valid
    assert result.rollback["schema_version"] == "cavra.go-runtime.endpoint-rollout-rollback-execution.v1"
    assert result.rollback["ring_rollback"] == {
        "from": "production",
        "to": "pilot",
        "previous_rollout_status": "promoted",
        "new_rollout_status": "rolled_back",
    }
    assert result.rollback["rollback_evidence_refs"] == promotion.execution["rollback_evidence_refs"]
    assert set(result.files) == {"rollout-rollback-execution.json", "rollout-rollback-execution.md"}
    metadata = build_managed_endpoint_rollout_rollback_execution_metadata(result.rollback)
    assert metadata["metadata_kind"] == "rollout-rollback-execution"
    assert metadata["rollback_execution_status"] == "executed"
    assert metadata["promotion_execution_id"] == promotion.execution["execution_id"]

    export_result = export_rollout_promotion_execution_audit(
        promotion.execution,
        tmp_path / "audit-export",
        provider="all",
        itsm_project_key="CAVRA",
    )
    exported_names = {path.name for path in export_result.files}
    assert "promotion-execution-audit-event.json" in exported_names
    assert "splunk-hec-events.json" in exported_names
    assert "jira-issue.json" in exported_names
    audit_event = json.loads((tmp_path / "audit-export" / "promotion-execution-audit-event.json").read_text(encoding="utf-8"))
    assert audit_event["event_type"] == "cavra.rollout_promotion_execution"
    assert audit_event["rollback_reference_count"] > 0

    metadata_json = tmp_path / "rollback-metadata.json"
    cli_result = runner.invoke(
        app,
        [
            "release",
            "execute-rollout-rollback",
            str(tmp_path / "promotion-execution" / "rollout-promotion-execution.json"),
            "--approval-store",
            str(tmp_path / "approvals.json"),
            "--approval-id",
            approved_rollback["approval_id"],
            "--output",
            str(tmp_path / "cli-rollback-execution"),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    assert cli_result.exit_code == 0
    payload = json.loads(cli_result.output)
    assert payload["valid"] is True
    assert payload["rollback"]["approval"]["state"] == "approved"
    assert str(metadata_json) in payload["indexed_metadata_stores"]

    export_cli = runner.invoke(
        app,
        [
            "release",
            "export-promotion-audit",
            str(tmp_path / "promotion-execution" / "rollout-promotion-execution.json"),
            "--output",
            str(tmp_path / "cli-audit-export"),
            "--provider",
            "jira",
            "--json",
        ],
    )
    assert export_cli.exit_code == 0
    assert "jira-issue.json" in export_cli.output


def test_managed_endpoint_rollout_promotion_request_requires_ready_rollout(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")
    rollout_dir = tmp_path / "rollout"
    capture_managed_endpoint_rollout_evidence(
        dist,
        rollout_dir,
        deployment_ids=["github-actions-linux-amd64-runner"],
        rollout_id="chg-123-v0.1.0-test",
        status="planned",
    )

    result = create_managed_endpoint_rollout_promotion_request(
        rollout_dir,
        target_ring="production",
        signing_key_pem=private_key.read_text(encoding="utf-8"),
    )

    assert not result.valid
    assert "rollout promotion requires staged or succeeded rollout evidence" in result.errors


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
