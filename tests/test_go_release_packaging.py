from __future__ import annotations

import json
import subprocess
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from typer.testing import CliRunner

from cavra.approvals import ApprovalStore, create_approval_request
from cavra.cli import app
from cavra.evidence import EvidenceMetadataStore, generate_ed25519_keypair
from cavra.release import (
    automate_endpoint_reconciliation_from_ingestion,
    build_endpoint_drift_remediation_dashboard,
    build_endpoint_drift_remediation_execution_metadata,
    build_endpoint_drift_remediation_request_metadata,
    build_endpoint_remediation_handoff,
    build_endpoint_remediation_handoff_dashboard,
    build_endpoint_remediation_handoff_metadata,
    build_endpoint_remediation_handoff_status_dashboard,
    build_endpoint_remediation_handoff_status_metadata,
    build_endpoint_remediation_sla_dashboard,
    build_endpoint_remediation_sla_escalation_action_dashboard,
    build_endpoint_remediation_sla_escalation_delivery_event,
    build_endpoint_remediation_sla_escalation_dashboard,
    build_endpoint_remediation_sla_escalation_plan,
    build_endpoint_remediation_sla_escalation_plan_metadata,
    build_endpoint_remediation_sla_escalation_owner_digest_event,
    build_endpoint_remediation_sla_escalation_owner_digest_metadata,
    build_endpoint_remediation_sla_escalation_recurrence_dashboard,
    build_endpoint_remediation_sla_escalation_recurrence_delivery_event,
    build_endpoint_remediation_sla_escalation_recurrence_plan,
    build_endpoint_remediation_sla_escalation_recurrence_plan_metadata,
    build_endpoint_remediation_sla_escalation_recurrence_retry_plan,
    build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata,
    build_endpoint_remediation_sla_escalation_review_metadata,
    build_endpoint_remediation_sla_escalation_suppression_audit,
    build_endpoint_remediation_sla_escalation_suppression_audit_metadata,
    build_endpoint_remediation_sla_escalation_suppression_trends,
    build_endpoint_remediation_sla_escalation_suppression_trend_metadata,
    build_endpoint_remediation_sla_notification_dashboard,
    build_endpoint_remediation_sla_notification_event,
    build_endpoint_remediation_sla_notification_ack_metadata,
    build_endpoint_remediation_sla_notification_plan,
    build_endpoint_remediation_sla_notification_plan_metadata,
    build_endpoint_remediation_sla_report,
    build_endpoint_remediation_sla_report_metadata,
    build_endpoint_inventory_freshness_dashboard,
    build_endpoint_inventory_freshness_metadata,
    build_endpoint_inventory_ingestion_dashboard,
    build_endpoint_inventory_ingestion_metadata,
    build_endpoint_reconciliation_automation_dashboard,
    build_endpoint_reconciliation_automation_metadata,
    build_managed_endpoint_reconciliation_dashboard,
    build_managed_endpoint_reconciliation_metadata,
    build_managed_endpoint_rollout_rollback_execution_metadata,
    capture_managed_endpoint_rollout_evidence,
    create_managed_endpoint_rollout_rollback_execution,
    create_managed_endpoint_rollout_promotion_execution,
    create_managed_endpoint_rollout_promotion_request,
    create_endpoint_drift_remediation_request,
    acknowledge_endpoint_remediation_sla_notification,
    create_release_channel_promotion_request,
    execute_endpoint_drift_remediation,
    export_endpoint_remediation_sla_escalation_suppression_audit,
    export_endpoint_management_bundles,
    export_rollout_promotion_execution_audit,
    filter_endpoint_inventory_freshness_history,
    filter_managed_endpoint_reconciliation_history,
    filter_endpoint_drift_remediation_history,
    filter_endpoint_remediation_handoff_history,
    filter_endpoint_remediation_handoff_status_history,
    filter_endpoint_remediation_sla_escalation_history,
    filter_endpoint_remediation_sla_escalation_action_history,
    filter_endpoint_remediation_sla_escalation_recurrence_history,
    filter_endpoint_remediation_sla_notification_history,
    filter_endpoint_remediation_sla_report_history,
    filter_endpoint_inventory_ingestion_history,
    filter_endpoint_reconciliation_automation_history,
    evaluate_endpoint_inventory_freshness,
    ingest_endpoint_inventory,
    reconcile_managed_endpoint_deployment,
    review_endpoint_remediation_sla_escalation,
    record_endpoint_remediation_handoff_status,
    smoke_test_go_installers,
    validate_go_release_upgrade,
    verify_managed_endpoint_rollout_evidence,
    verify_go_airgap_bundle,
    verify_go_release_package,
    verify_release_channel_promotion_request_signature,
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
    channels = json.loads((dist / "cavra-runtime.channels.json").read_text(encoding="utf-8"))
    updater_policy = json.loads((dist / "cavra-runtime.updater-policy.json").read_text(encoding="utf-8"))
    summary = (dist / "release-evidence.md").read_text(encoding="utf-8")

    assert "bin/cavra-runtime_test_linux_amd64" in checksums
    assert "cavra-runtime.endpoint-deployment.json" in checksums
    assert "cavra-runtime.installers.json" in checksums
    assert "cavra-runtime.channels.json" in checksums
    assert "cavra-runtime.updater-policy.json" in checksums
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
    assert "cavra-runtime.channels.json" in bootstrap["required_files"]
    assert "cavra-runtime.updater-policy.json" in bootstrap["required_files"]
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
    assert channels["schema_version"] == "cavra.go-runtime.channels.v1"
    assert channels["updater_policy"] == "cavra-runtime.updater-policy.json"
    assert channels["channels"][0]["auto_update"] is False
    assert channels["channels"][0]["approval_required"] is True
    assert channels["channels"][0]["workstation_targets"][0]["binary"] == "bin/cavra-runtime_test_linux_amd64"
    assert updater_policy["schema_version"] == "cavra.go-runtime.updater-policy.v1"
    assert updater_policy["default_auto_update"] is False
    assert updater_policy["policies"][0]["rollback"]["required"] is True
    assert evidence["schema_version"] == "cavra.go-release.evidence.v1"
    assert evidence["dry_run"] is True
    assert evidence["signature_count"] == 0
    assert {artifact["kind"] for artifact in evidence["artifacts"]} >= {
        "go-binary",
        "managed-endpoint-deployment",
        "installer-metadata",
        "release-channel-manifest",
        "updater-policy",
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
    assert "cavra-runtime.channels.json" in valid_result.verified_artifacts
    assert "cavra-runtime.channels.json" in valid_result.verified_provenance
    assert "cavra-runtime.channels.json" in valid_result.verified_signatures
    assert "cavra-runtime.updater-policy.json" in valid_result.verified_artifacts
    assert "cavra-runtime.updater-policy.json" in valid_result.verified_provenance
    assert "cavra-runtime.updater-policy.json" in valid_result.verified_signatures
    assert "cavra-runtime.provenance.intoto.json" in valid_result.verified_signatures
    assert "offline-trust-root-bootstrap.json" in valid_result.verified_signatures
    assert "release-evidence.json" in valid_result.verified_signatures
    cli_result = runner.invoke(app, ["release", "verify-go-package", str(dist), "--json"])
    assert cli_result.exit_code == 0
    assert json.loads(cli_result.output)["valid"] is True
    channel_cli = runner.invoke(app, ["release", "channel-manifest", str(dist), "--channel", "stable", "--json"])
    policy_cli = runner.invoke(app, ["release", "updater-policy", str(dist), "--json"])
    assert channel_cli.exit_code == 0
    assert json.loads(channel_cli.output)["channels"][0]["channel"] == "stable"
    assert policy_cli.exit_code == 0
    assert json.loads(policy_cli.output)["default_auto_update"] is False

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


def test_go_release_verifier_rejects_missing_channel_and_updater_policy(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.1.0-test", "abc123")

    (dist / "cavra-runtime.channels.json").unlink()
    (dist / "cavra-runtime.updater-policy.json").unlink()

    invalid_result = verify_go_release_package(dist)
    assert not invalid_result.valid
    assert any("missing cavra-runtime.channels.json" in error for error in invalid_result.errors)
    assert any("missing cavra-runtime.updater-policy.json" in error for error in invalid_result.errors)


def test_release_channel_promotion_request_and_endpoint_exports(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(
        tmp_path,
        "v0.1.0-test",
        "abc123",
        targets=("linux_amd64", "darwin_arm64", "windows_amd64"),
    )

    request = create_release_channel_promotion_request(
        dist,
        output_dir=tmp_path / "channel-promotion",
        channel="stable",
        target_ring="enterprise",
        requested_by="release-manager",
        signing_key_pem=private_key.read_text(encoding="utf-8"),
    )

    assert request.valid
    assert request.channel == "stable"
    assert request.approval["state"] == "pending"
    assert request.approval["decision"]["action_type"] == "release_promote_channel_manifest"
    assert request.request["channel_manifest"]["channel"]["channel"] == "stable"
    assert request.request["updater_policy"]["policy"]["channel"] == "stable"
    assert {target["management_tool"] for target in request.request["workstation_targets"]} >= {
        "Jamf Pro",
        "Microsoft Intune",
        "Linux endpoint management",
    }
    verify_release_channel_promotion_request_signature(request.request)
    assert set(request.files) == {"release-channel-promotion-request.json", "release-channel-promotion-request.md"}

    export = export_endpoint_management_bundles(
        dist,
        tmp_path / "endpoint-export",
        channel="stable",
        provider="all",
        promotion_request=request.request,
    )

    assert export.valid
    assert export.providers == ["intune", "jamf", "linux"]
    assert set(export.files) >= {
        "endpoint-management-export-manifest.json",
        "endpoint-management-export-manifest.md",
        "checksums.txt",
        "jamf-policy.json",
        "intune-win32-app.json",
        "linux-fleet-manifest.json",
        "linux-install-cavra-runtime.sh",
    }
    assert export.manifest["approval"]["approval_id"] == request.approval["approval_id"]
    jamf = json.loads((tmp_path / "endpoint-export" / "jamf-policy.json").read_text(encoding="utf-8"))
    intune = json.loads((tmp_path / "endpoint-export" / "intune-win32-app.json").read_text(encoding="utf-8"))
    linux = json.loads((tmp_path / "endpoint-export" / "linux-fleet-manifest.json").read_text(encoding="utf-8"))
    assert jamf["schema_version"] == "cavra.endpoint-management.jamf.v1"
    assert intune["schema_version"] == "cavra.endpoint-management.intune.v1"
    assert linux["schema_version"] == "cavra.endpoint-management.linux.v1"

    approval_json = tmp_path / "channel-approvals.json"
    metadata_json = tmp_path / "release-metadata.json"
    cli_request = runner.invoke(
        app,
        [
            "release",
            "request-channel-promotion",
            str(dist),
            "--output",
            str(tmp_path / "cli-channel-promotion"),
            "--channel",
            "stable",
            "--approval-store",
            str(approval_json),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    assert cli_request.exit_code == 0
    request_payload = json.loads(cli_request.output)
    assert request_payload["valid"] is True
    assert request_payload["metadata"]["metadata_kind"] == "release-channel-promotion-request"
    assert request_payload["indexed_metadata_stores"] == [str(metadata_json)]
    assert json.loads(approval_json.read_text(encoding="utf-8"))["items"][0]["state"] == "pending"

    cli_export = runner.invoke(
        app,
        [
            "release",
            "export-endpoint-management",
            str(dist),
            "--output",
            str(tmp_path / "cli-endpoint-export"),
            "--channel",
            "stable",
            "--provider",
            "jamf",
            "--promotion-request",
            str(tmp_path / "cli-channel-promotion" / "release-channel-promotion-request.json"),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    assert cli_export.exit_code == 0
    export_payload = json.loads(cli_export.output)
    assert export_payload["valid"] is True
    assert export_payload["providers"] == ["jamf"]
    assert "jamf-policy.json" in export_payload["files"]
    assert export_payload["metadata"]["metadata_kind"] == "endpoint-management-export"
    indexed_metadata = EvidenceMetadataStore(metadata_json).list()
    assert {item["metadata_kind"] for item in indexed_metadata} == {
        "release-channel-promotion-request",
        "endpoint-management-export",
    }

    connector_config = tmp_path / "endpoint-connectors.json"
    connector_config.write_text(
        json.dumps({"connectors": {"jamf": {"url": "http://127.0.0.1:9/jamf?token=secret"}}}),
        encoding="utf-8",
    )
    publication_metadata = tmp_path / "endpoint-publications.json"
    publication_delivery = runner.invoke(
        app,
        [
            "release",
            "deliver-endpoint-export",
            str(tmp_path / "cli-endpoint-export" / "endpoint-management-export-manifest.json"),
            "--config",
            str(connector_config),
            "--provider",
            "jamf",
            "--retries",
            "0",
            "--timeout-seconds",
            "0.1",
            "--metadata-json",
            str(publication_metadata),
            "--json",
        ],
    )
    assert publication_delivery.exit_code == 0
    publication_payload = json.loads(publication_delivery.output)
    assert publication_payload["valid"] is True
    assert publication_payload["providers"] == ["jamf"]
    assert publication_payload["delivery"]["deliveries"][0]["request"]["url"].endswith("?REDACTED")
    assert publication_payload["metadata"]["metadata_kind"] == "endpoint-management-publication-delivery"
    assert publication_payload["metadata"]["failed_providers"] == ["jamf"]
    history = runner.invoke(
        app,
        [
            "release",
            "endpoint-publication-history",
            "--metadata-json",
            str(publication_metadata),
            "--provider",
            "jamf",
            "--no-success",
        ],
    )
    dashboard = runner.invoke(
        app,
        [
            "release",
            "endpoint-publication-dashboard",
            "--metadata-json",
            str(publication_metadata),
        ],
    )
    assert history.exit_code == 0
    assert json.loads(history.output)["total"] == 1
    assert dashboard.exit_code == 0
    assert json.loads(dashboard.output)["providers"][0]["failed"] == 1


def test_managed_endpoint_reconciliation_detects_drift_and_indexes_metadata(tmp_path: Path, monkeypatch) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.2.0-rc.1", "abc123", targets=("linux_amd64",))
    desired_manifest = json.loads((dist / "cavra-runtime.endpoint-deployment.json").read_text(encoding="utf-8"))
    target = desired_manifest["deployment_targets"][0]
    observed_at = datetime.now(timezone.utc).isoformat()
    observed = {
        "schema_version": "cavra.endpoint-observations.v1",
        "observed_at": observed_at,
        "channel": "stable",
        "endpoints": [
            {
                "endpoint_id": "runner-1",
                "deployment_target": target["id"],
                "installed_version": "v0.2.0-rc.1",
                "binary_sha256": target["binary_sha256"],
                "last_seen_at": observed_at,
            },
            {
                "endpoint_id": "runner-2",
                "deployment_target": target["id"],
                "installed_version": "v0.1.0",
                "binary_sha256": "bad",
                "last_seen_at": observed_at,
            },
        ],
    }

    result = reconcile_managed_endpoint_deployment(
        desired_manifest,
        observed,
        package_dir=dist,
        output_dir=tmp_path / "reconciliation",
        stale_after_hours=24,
    )

    assert result.valid
    assert result.drift_status == "drift_detected"
    assert result.report["summary"]["compliant_endpoint_count"] == 1
    assert result.report["summary"]["drifted_endpoint_count"] == 1
    assert "managed-endpoint-reconciliation.json" in result.files
    metadata = build_managed_endpoint_reconciliation_metadata(result.report, bundle_dir=tmp_path / "reconciliation")
    history = filter_managed_endpoint_reconciliation_history(
        [metadata],
        drift_status="drift_detected",
        deployment_target=target["id"],
    )
    dashboard = build_managed_endpoint_reconciliation_dashboard([metadata])
    assert metadata["metadata_kind"] == "managed-endpoint-reconciliation"
    assert history["total"] == 1
    assert dashboard["alert_level"] == "critical"

    observed_path = tmp_path / "observed-endpoints.json"
    observed_path.write_text(json.dumps(observed), encoding="utf-8")
    metadata_json = tmp_path / "reconciliation-metadata.json"
    cli_result = runner.invoke(
        app,
        [
            "release",
            "reconcile-endpoint-deployment",
            str(dist),
            str(observed_path),
            "--output",
            str(tmp_path / "cli-reconciliation"),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    assert cli_result.exit_code == 0
    cli_payload = json.loads(cli_result.output)
    assert cli_payload["metadata"]["metadata_kind"] == "managed-endpoint-reconciliation"
    assert cli_payload["report"]["summary"]["drifted_endpoint_count"] == 1
    history_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-reconciliation-history",
            "--metadata-json",
            str(metadata_json),
            "--drift-status",
            "drift_detected",
        ],
    )
    dashboard_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-reconciliation-dashboard",
            "--metadata-json",
            str(metadata_json),
        ],
    )
    assert history_cli.exit_code == 0
    assert json.loads(history_cli.output)["total"] == 1
    assert dashboard_cli.exit_code == 0
    assert json.loads(dashboard_cli.output)["drifted_endpoint_count"] == 1


def test_endpoint_inventory_ingestion_normalizes_provider_exports_and_indexes_metadata(tmp_path: Path) -> None:
    jamf_export = {
        "schema_version": "jamf.computer-inventory.export.v1",
        "channel": "stable",
        "computers": [
            {
                "id": "jamf-1",
                "name": "macbook-1",
                "serialNumber": "JAMF123",
                "policy_name": "macos-jamf-arm64-workstation",
                "cavra": {
                    "runtime_version": "v0.2.0-rc.1",
                    "runtime_sha256": "good",
                    "last_seen_at": "2026-05-19T00:00:00+00:00",
                },
            }
        ],
    }
    result = ingest_endpoint_inventory(
        "jamf",
        jamf_export,
        output_dir=tmp_path / "inventory",
        channel="stable",
    )
    metadata = build_endpoint_inventory_ingestion_metadata(result.ingestion or {}, bundle_dir=tmp_path / "inventory")
    history = filter_endpoint_inventory_ingestion_history(
        [metadata],
        provider="jamf",
        deployment_target="macos-jamf-arm64-workstation",
    )
    dashboard = build_endpoint_inventory_ingestion_dashboard([metadata])

    assert result.valid
    assert result.inventory_id
    assert result.inventory is not None
    assert result.inventory["schema_version"] == "cavra.endpoint-observations.v1"
    assert result.inventory["endpoints"][0]["endpoint_id"] == "jamf-1"
    assert result.inventory["endpoints"][0]["deployment_target"] == "macos-jamf-arm64-workstation"
    assert result.inventory["endpoints"][0]["installed_version"] == "v0.2.0-rc.1"
    assert "endpoint-inventory.json" in result.files
    assert metadata["metadata_kind"] == "endpoint-inventory-ingestion"
    assert history["total"] == 1
    assert dashboard["providers"][0]["provider"] == "jamf"

    source = tmp_path / "jamf-export.json"
    source.write_text(json.dumps(jamf_export), encoding="utf-8")
    metadata_json = tmp_path / "inventory-metadata.json"
    cli_result = runner.invoke(
        app,
        [
            "release",
            "ingest-endpoint-inventory",
            str(source),
            "--provider",
            "jamf",
            "--channel",
            "stable",
            "--output",
            str(tmp_path / "cli-inventory"),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    history_cli = runner.invoke(
        app,
        ["release", "endpoint-inventory-history", "--metadata-json", str(metadata_json), "--provider", "jamf"],
    )
    dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-inventory-dashboard", "--metadata-json", str(metadata_json)],
    )
    assert cli_result.exit_code == 0
    cli_payload = json.loads(cli_result.output)
    assert cli_payload["metadata"]["metadata_kind"] == "endpoint-inventory-ingestion"
    assert cli_payload["inventory"]["endpoints"][0]["binary_sha256"] == "good"
    assert history_cli.exit_code == 0
    assert json.loads(history_cli.output)["total"] == 1
    assert dashboard_cli.exit_code == 0
    assert json.loads(dashboard_cli.output)["endpoint_count"] == 1


def test_endpoint_inventory_freshness_and_automation_open_remediation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.2.0-rc.1", "abc123", targets=("linux_amd64",))
    desired_manifest = json.loads((dist / "cavra-runtime.endpoint-deployment.json").read_text(encoding="utf-8"))
    target = desired_manifest["deployment_targets"][0]
    linux_export = {
        "schema_version": "linux.fleet.inventory.v1",
        "observed_at": "2026-05-19T00:00:00+00:00",
        "hosts": [
            {
                "endpoint_id": "runner-2",
                "deployment_target": target["id"],
                "installed_version": "v0.1.0",
                "binary_sha256": "bad",
                "last_seen_at": "2026-05-19T00:00:00+00:00",
            }
        ],
    }
    ingestion = ingest_endpoint_inventory("linux", linux_export, output_dir=tmp_path / "inventory", channel="stable")
    ingestion_metadata = build_endpoint_inventory_ingestion_metadata(ingestion.ingestion or {})
    freshness = evaluate_endpoint_inventory_freshness(
        [ingestion_metadata],
        output_dir=tmp_path / "freshness",
        max_age_hours=24,
        critical_age_hours=48,
        now=datetime(2026, 5, 21, 12, 0, tzinfo=timezone.utc),
    )
    freshness_metadata = build_endpoint_inventory_freshness_metadata(freshness.report or {})
    freshness_history = filter_endpoint_inventory_freshness_history(
        [freshness_metadata],
        alert_level="critical",
        provider="linux",
    )
    freshness_dashboard = build_endpoint_inventory_freshness_dashboard([freshness_metadata])

    assert freshness.valid
    assert freshness.alert_level == "critical"
    assert "endpoint-inventory-freshness.json" in freshness.files
    assert freshness_metadata["metadata_kind"] == "endpoint-inventory-freshness-report"
    assert freshness_history["total"] == 1
    assert freshness_dashboard["critical_count"] == 1

    automation = automate_endpoint_reconciliation_from_ingestion(
        desired_manifest,
        ingestion_metadata,
        package_dir=dist,
        output_dir=tmp_path / "automation",
        remediation_strategy="rollback",
        requested_by="release-agent",
    )
    automation_metadata = build_endpoint_reconciliation_automation_metadata(automation.automation or {})
    automation_history = filter_endpoint_reconciliation_automation_history(
        [automation_metadata],
        drift_status="drift_detected",
        approval_state="pending",
    )
    automation_dashboard = build_endpoint_reconciliation_automation_dashboard([automation_metadata])

    assert automation.valid
    assert automation.reconciliation is not None
    assert automation.remediation_request is not None
    assert automation.approval is not None
    assert automation.approval["state"] == "pending"
    assert automation.remediation_request["strategy"] == "rollback"
    assert automation_metadata["metadata_kind"] == "endpoint-reconciliation-automation"
    assert automation_history["total"] == 1
    assert automation_dashboard["pending_approval_count"] == 1

    metadata_json = tmp_path / "metadata.json"
    approval_json = tmp_path / "approvals.json"
    EvidenceMetadataStore(metadata_json).upsert(ingestion_metadata)
    cli_freshness = runner.invoke(
        app,
        [
            "release",
            "endpoint-inventory-freshness",
            "--metadata-json",
            str(metadata_json),
            "--output",
            str(tmp_path / "cli-freshness"),
            "--max-age-hours",
            "1",
            "--critical-age-hours",
            "1",
            "--json",
        ],
    )
    ingestion_path = tmp_path / "inventory" / "endpoint-inventory-ingestion.json"
    cli_automation = runner.invoke(
        app,
        [
            "release",
            "automate-endpoint-reconciliation",
            str(dist),
            str(ingestion_path),
            "--output",
            str(tmp_path / "cli-automation"),
            "--approval-store",
            str(approval_json),
            "--metadata-json",
            str(metadata_json),
            "--remediation-strategy",
            "rollback",
            "--json",
        ],
    )
    automation_history_cli = runner.invoke(
        app,
        ["release", "endpoint-reconciliation-automation-history", "--metadata-json", str(metadata_json)],
    )
    automation_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-reconciliation-automation-dashboard", "--metadata-json", str(metadata_json)],
    )
    assert cli_freshness.exit_code == 0
    assert json.loads(cli_freshness.output)["metadata"]["metadata_kind"] == "endpoint-inventory-freshness-report"
    assert cli_automation.exit_code == 0
    automation_payload = json.loads(cli_automation.output)
    assert automation_payload["metadata"]["metadata_kind"] == "endpoint-reconciliation-automation"
    assert ApprovalStore(approval_json).get(automation_payload["approval"]["approval_id"]) is not None
    assert automation_history_cli.exit_code == 0
    assert json.loads(automation_history_cli.output)["total"] == 1
    assert automation_dashboard_cli.exit_code == 0
    assert json.loads(automation_dashboard_cli.output)["pending_approval_count"] == 1


def test_endpoint_drift_remediation_requires_approval_and_indexes_execution(
    tmp_path: Path,
    monkeypatch,
) -> None:
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_GO_RELEASE_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    dist = _package_go_runtime(tmp_path, "v0.2.0-rc.1", "abc123", targets=("linux_amd64",))
    desired_manifest = json.loads((dist / "cavra-runtime.endpoint-deployment.json").read_text(encoding="utf-8"))
    target = desired_manifest["deployment_targets"][0]
    observed = {
        "schema_version": "cavra.endpoint-observations.v1",
        "observed_at": "2026-05-19T00:00:00+00:00",
        "channel": "stable",
        "endpoints": [
            {
                "endpoint_id": "runner-2",
                "deployment_target": target["id"],
                "installed_version": "v0.1.0",
                "binary_sha256": "bad",
                "last_seen_at": "2026-05-19T00:00:00+00:00",
            }
        ],
    }
    reconciliation = reconcile_managed_endpoint_deployment(
        desired_manifest,
        observed,
        package_dir=dist,
        output_dir=tmp_path / "reconciliation",
        stale_after_hours=24,
    )
    request_result = create_endpoint_drift_remediation_request(
        reconciliation.report or {},
        output_dir=tmp_path / "remediation-request",
        strategy="rollback",
    )

    assert request_result.valid
    assert request_result.approval is not None
    assert request_result.request is not None
    assert request_result.approval["state"] == "pending"
    assert request_result.approval["decision"]["action_type"] == "endpoint_drift_remediation"
    assert any(action["action_type"] == "rollback_runtime" for action in request_result.request["actions"])
    assert "endpoint-remediation-request.json" in request_result.files

    pending_execution = execute_endpoint_drift_remediation(request_result.request, request_result.approval)
    assert not pending_execution.valid
    assert "endpoint drift remediation requires an approved approval record" in pending_execution.errors

    approval_store = ApprovalStore(tmp_path / "approvals.json")
    approval_store.upsert(request_result.approval)
    approved = approval_store.decide(
        request_result.approval["approval_id"],
        state="approved",
        actor="endpoint-cab",
        reason="Drift remediation reviewed",
    )
    execution_result = execute_endpoint_drift_remediation(
        request_result.request,
        approved,
        output_dir=tmp_path / "remediation-execution",
    )
    request_metadata = build_endpoint_drift_remediation_request_metadata(request_result.request)
    handoff_result = build_endpoint_remediation_handoff(
        request_result.request,
        output_dir=tmp_path / "remediation-handoff",
        providers=["jira", "servicenow", "slack", "teams", "private_queue"],
    )
    handoff_metadata = build_endpoint_remediation_handoff_metadata(handoff_result.handoff or {})
    handoff_status_result = record_endpoint_remediation_handoff_status(
        handoff_result.handoff or {},
        provider="private_queue",
        status="completed",
        external_ref="queue-job-123",
        callback_payload={"job": {"id": "queue-job-123", "token": "sensitive"}},
        output_dir=tmp_path / "remediation-handoff-status",
    )
    handoff_status_metadata = build_endpoint_remediation_handoff_status_metadata(handoff_status_result.status or {})
    handoff_failed_status = record_endpoint_remediation_handoff_status(
        handoff_result.handoff or {},
        provider="jira",
        status="failed",
        external_ref="CAVRA-123",
    )
    handoff_failed_status_metadata = build_endpoint_remediation_handoff_status_metadata(handoff_failed_status.status or {})
    sla_result = build_endpoint_remediation_sla_report(
        [handoff_metadata],
        [handoff_failed_status_metadata],
        warning_hours=1,
        critical_hours=2,
        output_dir=tmp_path / "remediation-sla",
    )
    sla_metadata = build_endpoint_remediation_sla_report_metadata(sla_result.report or {})
    sla_event = build_endpoint_remediation_sla_notification_event(sla_result.report or {})
    notification_policy = {
        "default_providers": ["slack"],
        "suppression_window_minutes": 120,
        "rules": [
            {
                "rule_id": "critical-release-governance",
                "alert_levels": ["critical"],
                "providers": ["jira", "slack"],
                "min_breached": 1,
                "owner": "release-cab",
                "acknowledgement_required": True,
            }
        ],
    }
    notification_plan = build_endpoint_remediation_sla_notification_plan(
        sla_result.report or {},
        policy=notification_policy,
        available_providers=["jira", "slack", "webhook"],
    )
    notification_plan_metadata = build_endpoint_remediation_sla_notification_plan_metadata(notification_plan)
    acknowledgement = acknowledge_endpoint_remediation_sla_notification(
        sla_result.report["report_id"],
        provider="slack",
        acknowledged_by="release-manager",
        plan_id=notification_plan["plan_id"],
    )
    acknowledgement_metadata = build_endpoint_remediation_sla_notification_ack_metadata(acknowledgement)
    suppressed_plan = build_endpoint_remediation_sla_notification_plan(
        sla_result.report or {},
        policy=notification_policy,
        delivery_items=[
            {
                "metadata_kind": "release-connector-delivery",
                "connector_delivery_source": "endpoint_remediation_sla_notification",
                "event_id": sla_result.report["report_id"],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "delivery_success": True,
                "providers": ["slack"],
                "session_id": "rcd-slack-existing",
            }
        ],
        available_providers=["jira", "slack", "webhook"],
    )
    notification_history = filter_endpoint_remediation_sla_notification_history(
        [notification_plan_metadata, acknowledgement_metadata],
        report_id=sla_result.report["report_id"],
    )
    notification_dashboard = build_endpoint_remediation_sla_notification_dashboard(
        [notification_plan_metadata, acknowledgement_metadata]
    )
    escalation_policy = {
        "default_slo": {"acknowledgement_minutes": 30, "resolution_minutes": 180},
        "owner_slos": {"release-cab": {"acknowledgement_minutes": 15, "resolution_minutes": 60}},
        "ladders": [
            {
                "level": "owner",
                "after_minutes": 20,
                "providers": ["slack"],
                "action": "Escalate to endpoint remediation owner.",
            },
            {
                "level": "release-governance",
                "after_minutes": 60,
                "providers": ["jira"],
                "action": "Escalate to release governance.",
            },
        ],
    }
    escalation_plan = build_endpoint_remediation_sla_escalation_plan(
        [notification_plan_metadata, acknowledgement_metadata],
        policy=escalation_policy,
        now=datetime.fromisoformat(notification_plan["generated_at"]) + timedelta(minutes=75),
    )
    escalation_plan_metadata = build_endpoint_remediation_sla_escalation_plan_metadata(escalation_plan)
    escalation_history = filter_endpoint_remediation_sla_escalation_history(
        [escalation_plan_metadata],
        owner="release-cab",
        active_only=True,
    )
    escalation_dashboard = build_endpoint_remediation_sla_escalation_dashboard([escalation_plan_metadata])
    escalation_event = build_endpoint_remediation_sla_escalation_delivery_event(escalation_plan)
    escalation_delivery_metadata = {
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "endpoint_remediation_sla_escalation_delivery",
        "session_id": "rcd-escalation-existing",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "event_id": escalation_plan["plan_id"],
        "event_type": "cavra.endpoint_remediation_sla.escalation_delivery",
        "delivery_success": True,
        "providers": ["jira"],
        "failed_providers": [],
    }
    escalation_review = review_endpoint_remediation_sla_escalation(
        escalation_plan["plan_id"],
        report_id=sla_result.report["report_id"],
        provider="jira",
        owner="release-cab",
        reviewed_by="release-manager",
        review_state="escalated",
    )
    escalation_review_metadata = build_endpoint_remediation_sla_escalation_review_metadata(escalation_review)
    escalation_action_history = filter_endpoint_remediation_sla_escalation_action_history(
        [escalation_plan_metadata, escalation_delivery_metadata, escalation_review_metadata],
        owner="release-cab",
    )
    escalation_action_dashboard = build_endpoint_remediation_sla_escalation_action_dashboard(
        [escalation_plan_metadata, escalation_delivery_metadata, escalation_review_metadata]
    )
    recurrence_policy = {
        "recurrence_interval_minutes": 30,
        "max_recurrences_per_route": 3,
        "maintenance_windows": [
            {
                "window_id": "jira-maintenance",
                "owners": ["release-cab"],
                "providers": ["jira"],
                "start_at": (
                    datetime.fromisoformat(escalation_plan["generated_at"]) - timedelta(minutes=5)
                ).isoformat(),
                "end_at": (
                    datetime.fromisoformat(escalation_plan["generated_at"]) + timedelta(minutes=30)
                ).isoformat(),
                "reason": "provider maintenance",
            }
        ],
        "owner_calendars": {
            "release-cab": {
                "business_hours": [{"days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"], "start": "00:00", "end": "23:59"}]
            }
        },
    }
    recurrence_plan = build_endpoint_remediation_sla_escalation_recurrence_plan(
        [escalation_plan_metadata, escalation_delivery_metadata, escalation_review_metadata],
        policy=recurrence_policy,
        now=datetime.fromisoformat(escalation_plan["generated_at"]) + timedelta(minutes=10),
    )
    recurrence_metadata = build_endpoint_remediation_sla_escalation_recurrence_plan_metadata(recurrence_plan)
    recurrence_history = filter_endpoint_remediation_sla_escalation_recurrence_history(
        [recurrence_metadata],
        action="suppress",
    )
    recurrence_dashboard = build_endpoint_remediation_sla_escalation_recurrence_dashboard([recurrence_metadata])
    recurrence_event = build_endpoint_remediation_sla_escalation_recurrence_delivery_event(recurrence_plan)
    failed_recurrence_delivery_metadata = {
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "endpoint_remediation_sla_escalation_recurrence_delivery",
        "session_id": "rcd-recurrence-existing",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "event_id": recurrence_plan["recurrence_plan_id"],
        "event_type": "cavra.endpoint_remediation_sla.escalation_recurrence_delivery",
        "delivery_success": False,
        "providers": [recurrence_event["routes"][0]["provider"]],
        "failed_providers": [recurrence_event["routes"][0]["provider"]],
        "status_codes": [503],
        "attempt_count": 1,
        "max_attempt_count": 1,
    }
    recurrence_retry_plan = build_endpoint_remediation_sla_escalation_recurrence_retry_plan(
        [recurrence_metadata, failed_recurrence_delivery_metadata],
        policy={"max_retry_attempts": 3, "retry_delay_minutes": 1, "backoff_multiplier": 1},
        now=datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    recurrence_retry_metadata = build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata(
        recurrence_retry_plan
    )
    owner_digest_event = build_endpoint_remediation_sla_escalation_owner_digest_event(
        recurrence_plan,
        retry_plan=recurrence_retry_plan,
    )
    owner_digest_metadata = build_endpoint_remediation_sla_escalation_owner_digest_metadata(owner_digest_event)
    suppression_audit = build_endpoint_remediation_sla_escalation_suppression_audit(recurrence_plan)
    suppression_audit_metadata = build_endpoint_remediation_sla_escalation_suppression_audit_metadata(
        suppression_audit,
        bundle_dir=tmp_path / "recurrence-suppression-audit",
    )
    suppression_export = export_endpoint_remediation_sla_escalation_suppression_audit(
        recurrence_plan,
        tmp_path / "recurrence-suppression-audit",
    )
    suppression_trend = build_endpoint_remediation_sla_escalation_suppression_trends(
        [recurrence_metadata, suppression_audit_metadata]
    )
    suppression_trend_metadata = build_endpoint_remediation_sla_escalation_suppression_trend_metadata(suppression_trend)
    execution_metadata = build_endpoint_drift_remediation_execution_metadata(execution_result.execution or {})
    history = filter_endpoint_drift_remediation_history(
        [request_metadata, execution_metadata],
        reconciliation_id=reconciliation.reconciliation_id,
    )
    handoff_history = filter_endpoint_remediation_handoff_history([handoff_metadata], provider="private_queue")
    handoff_dashboard = build_endpoint_remediation_handoff_dashboard([handoff_metadata])
    handoff_status_history = filter_endpoint_remediation_handoff_status_history(
        [handoff_status_metadata],
        handoff_status="completed",
    )
    handoff_status_dashboard = build_endpoint_remediation_handoff_status_dashboard([handoff_status_metadata])
    sla_history = filter_endpoint_remediation_sla_report_history([sla_metadata], alert_level="critical")
    sla_dashboard = build_endpoint_remediation_sla_dashboard([sla_metadata])
    dashboard = build_endpoint_drift_remediation_dashboard([request_metadata, execution_metadata])

    assert execution_result.valid
    assert execution_result.execution is not None
    assert execution_result.execution["approval"]["state"] == "approved"
    assert execution_result.execution["action_results"][0]["status"] == "queued_for_private_connector_or_manual_execution"
    assert handoff_result.valid
    assert handoff_result.handoff["payloads"]["jira"]["issue"]["summary"].startswith("CAVRA endpoint remediation")
    assert handoff_result.handoff["payloads"]["private_queue"]["queue_event"]["status"] == "ready_for_private_connector"
    assert "private-queue-handoff.json" in handoff_result.files
    assert handoff_metadata["metadata_kind"] == "endpoint-remediation-handoff"
    assert handoff_history["total"] == 1
    assert handoff_dashboard["provider_count"] == 5
    assert handoff_status_result.valid
    assert handoff_status_result.status["callback_payload"]["job"]["token"] == "[redacted]"
    assert "endpoint-remediation-handoff-status.json" in handoff_status_result.files
    assert handoff_status_metadata["metadata_kind"] == "endpoint-remediation-handoff-status"
    assert handoff_status_history["total"] == 1
    assert handoff_status_dashboard["completed_count"] == 1
    assert sla_result.valid
    assert sla_result.report["executive_summary"]["breached_count"] == 1
    assert sla_result.report["escalation_payloads"]["executive_summary"]["critical_count"] == 1
    assert sla_event["event_type"] == "cavra.endpoint_remediation_sla.notification"
    assert sla_event["provider_payloads"]["slack"]["blocks"][0]["type"] == "header"
    assert sla_event["provider_payloads"]["servicenow"]["correlation_id"] == sla_result.report["report_id"]
    assert notification_plan["selected_providers"] == ["jira", "slack"]
    assert notification_plan["acknowledgement_required_providers"] == ["jira", "slack"]
    assert suppressed_plan["selected_providers"] == ["jira"]
    assert suppressed_plan["suppressed_providers"][0]["provider"] == "slack"
    assert acknowledgement_metadata["metadata_kind"] == "endpoint-remediation-sla-notification-ack"
    assert notification_history["total"] == 2
    assert notification_dashboard["outstanding_acknowledgement_count"] == 1
    assert escalation_plan["active_escalation_count"] == 2
    assert escalation_plan["owners"][0]["owner"] == "release-cab"
    assert escalation_plan_metadata["metadata_kind"] == "endpoint-remediation-sla-escalation-plan"
    assert escalation_history["total"] == 1
    assert escalation_dashboard["active_escalation_count"] == 2
    assert escalation_event["event_type"] == "cavra.endpoint_remediation_sla.escalation_delivery"
    assert escalation_event["provider_payloads"]["slack"]["blocks"][0]["type"] == "header"
    assert escalation_review_metadata["metadata_kind"] == "endpoint-remediation-sla-escalation-review"
    assert escalation_review_metadata["review_state"] == "escalated"
    assert escalation_action_history["total"] == 2
    assert escalation_action_dashboard["delivery_count"] == 1
    assert escalation_action_dashboard["owner_review_count"] == 1
    assert recurrence_metadata["metadata_kind"] == "endpoint-remediation-sla-escalation-recurrence-plan"
    assert recurrence_plan["suppressed_route_count"] >= 1
    assert recurrence_plan["maintenance_suppressed_count"] >= 1
    assert recurrence_history["total"] == 1
    assert recurrence_dashboard["suppressed_route_count"] >= 1
    assert recurrence_event["event_type"] == "cavra.endpoint_remediation_sla.escalation_recurrence_delivery"
    assert recurrence_event["summary"]["deliverable_route_count"] >= 1
    assert all(route["action"] == "deliver" for route in recurrence_event["routes"])
    assert suppression_audit_metadata["metadata_kind"] == "endpoint-remediation-sla-escalation-suppression-audit"
    assert suppression_audit["summary"]["suppressed_route_count"] >= 1
    assert any(path.name == "endpoint-remediation-sla-escalation-suppression-audit.md" for path in suppression_export.files)
    assert recurrence_retry_metadata["metadata_kind"] == "endpoint-remediation-sla-escalation-recurrence-retry-plan"
    assert recurrence_retry_plan["retryable_count"] >= 1
    assert owner_digest_metadata["metadata_kind"] == "endpoint-remediation-sla-escalation-owner-digest"
    assert owner_digest_event["event_type"] == "cavra.endpoint_remediation_sla.escalation_owner_digest"
    assert owner_digest_event["summary"]["owner_count"] >= 1
    assert suppression_trend_metadata["metadata_kind"] == "endpoint-remediation-sla-escalation-suppression-trend"
    assert suppression_trend["suppression_event_count"] >= 1
    assert "endpoint-remediation-sla-report.json" in sla_result.files
    assert sla_metadata["metadata_kind"] == "endpoint-remediation-sla-report"
    assert sla_history["total"] == 1
    assert sla_dashboard["breached_count"] == 1
    assert execution_metadata["metadata_kind"] == "endpoint-drift-remediation-execution"
    assert history["total"] == 2
    assert dashboard["execution_count"] == 1

    report_path = tmp_path / "reconciliation" / "managed-endpoint-reconciliation.json"
    metadata_json = tmp_path / "metadata.json"
    approval_json = tmp_path / "cli-approvals.json"
    connector_config = tmp_path / "connectors.json"
    connector_config.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra?token=secret"}}}),
        encoding="utf-8",
    )
    routing_policy = tmp_path / "sla-notification-routing-policy.json"
    routing_policy.write_text(
        json.dumps(
            {
                "rules": [
                    {
                        "rule_id": "webhook-release-owner",
                        "alert_levels": ["healthy", "warning", "critical"],
                        "providers": ["webhook"],
                        "owner": "release-governance",
                        "acknowledgement_required": True,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    slo_policy = tmp_path / "sla-escalation-policy.json"
    slo_policy.write_text(
        json.dumps(
            {
                "default_slo": {"acknowledgement_minutes": 1, "resolution_minutes": 1},
                "ladders": [
                    {
                        "level": "release-governance",
                        "after_minutes": 0,
                        "providers": ["webhook"],
                        "action": "Escalate unresolved SLA notification to release governance.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    recurrence_policy = tmp_path / "sla-escalation-recurrence-policy.json"
    recurrence_policy.write_text(
        json.dumps(
            {
                "recurrence_interval_minutes": 30,
                "max_recurrences_per_route": 3,
                "owner_calendars": {
                    "release-governance": {
                        "business_hours": [
                            {
                                "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                                "start": "00:00",
                                "end": "23:59",
                            }
                        ]
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    request_cli = runner.invoke(
        app,
        [
            "release",
            "request-endpoint-remediation",
            str(report_path),
            "--output",
            str(tmp_path / "cli-remediation-request"),
            "--approval-store",
            str(approval_json),
            "--metadata-json",
            str(metadata_json),
            "--strategy",
            "republish",
            "--json",
        ],
    )
    assert request_cli.exit_code == 0
    request_payload = json.loads(request_cli.output)
    cli_approval = ApprovalStore(approval_json).decide(
        request_payload["approval"]["approval_id"],
        state="approved",
        actor="endpoint-cab",
        reason="Approved republish remediation",
    )
    assert cli_approval["state"] == "approved"
    execution_cli = runner.invoke(
        app,
        [
            "release",
            "execute-endpoint-remediation",
            str(tmp_path / "cli-remediation-request" / "endpoint-remediation-request.json"),
            "--approval-store",
            str(approval_json),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    handoff_cli = runner.invoke(
        app,
        [
            "release",
            "export-endpoint-remediation-handoff",
            str(tmp_path / "cli-remediation-request" / "endpoint-remediation-request.json"),
            "--output",
            str(tmp_path / "endpoint-remediation-handoff"),
            "--provider",
            "jira",
            "--provider",
            "private_queue",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    handoff_payload = json.loads(handoff_cli.output) if handoff_cli.exit_code == 0 else {}
    handoff_status_cli = runner.invoke(
        app,
        [
            "release",
            "record-endpoint-remediation-handoff-status",
            str(tmp_path / "endpoint-remediation-handoff" / "endpoint-remediation-handoff.json"),
            "--provider",
            "private_queue",
            "--status",
            "delivered",
            "--external-ref",
            "queue-job-456",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    history_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-history", "--metadata-json", str(metadata_json)],
    )
    handoff_history_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-handoff-history", "--metadata-json", str(metadata_json)],
    )
    handoff_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-handoff-dashboard", "--metadata-json", str(metadata_json)],
    )
    handoff_status_history_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-handoff-status-history", "--metadata-json", str(metadata_json)],
    )
    handoff_status_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-handoff-status-dashboard", "--metadata-json", str(metadata_json)],
    )
    sla_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-remediation-sla-report",
            "--output",
            str(tmp_path / "cli-remediation-sla"),
            "--metadata-json",
            str(metadata_json),
            "--index-metadata-json",
            str(metadata_json),
            "--warning-hours",
            "1",
            "--critical-hours",
            "1",
            "--json",
        ],
    )
    sla_delivery_cli = runner.invoke(
        app,
        [
            "release",
            "deliver-endpoint-remediation-sla",
            str(tmp_path / "cli-remediation-sla" / "endpoint-remediation-sla-report.json"),
            "--config",
            str(connector_config),
            "--provider",
            "webhook",
            "--routing-policy",
            str(routing_policy),
            "--retries",
            "0",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_delivery_suppressed_cli = runner.invoke(
        app,
        [
            "release",
            "deliver-endpoint-remediation-sla",
            str(tmp_path / "cli-remediation-sla" / "endpoint-remediation-sla-report.json"),
            "--config",
            str(connector_config),
            "--provider",
            "webhook",
            "--routing-policy",
            str(routing_policy),
            "--retries",
            "0",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_notification_ack_cli = runner.invoke(
        app,
        [
            "release",
            "ack-endpoint-remediation-sla",
            json.loads(sla_cli.output)["report_id"],
            "--provider",
            "webhook",
            "--acknowledged-by",
            "release-manager",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_notification_history_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-notification-history", "--metadata-json", str(metadata_json)],
    )
    sla_notification_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-notification-dashboard", "--metadata-json", str(metadata_json)],
    )
    sla_escalation_plan_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-remediation-sla-escalation-plan",
            "--slo-policy",
            str(slo_policy),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_plan_path = tmp_path / "endpoint-remediation-sla-escalation-plan.json"
    if sla_escalation_plan_cli.exit_code == 0:
        sla_escalation_plan_path.write_text(sla_escalation_plan_cli.output, encoding="utf-8")
    sla_escalation_delivery_cli = runner.invoke(
        app,
        [
            "release",
            "deliver-endpoint-remediation-sla-escalation",
            str(sla_escalation_plan_path),
            "--config",
            str(connector_config),
            "--provider",
            "webhook",
            "--retries",
            "0",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_review_cli = runner.invoke(
        app,
        [
            "release",
            "review-endpoint-remediation-sla-escalation",
            json.loads(sla_escalation_plan_cli.output)["plan"]["plan_id"] if sla_escalation_plan_cli.exit_code == 0 else "plan",
            "--report-id",
            json.loads(sla_cli.output)["report_id"],
            "--provider",
            "webhook",
            "--owner",
            "release-governance",
            "--reviewed-by",
            "release-manager",
            "--review-state",
            "escalated",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_action_history_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-escalation-action-history", "--metadata-json", str(metadata_json)],
    )
    sla_escalation_action_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-escalation-action-dashboard", "--metadata-json", str(metadata_json)],
    )
    sla_escalation_recurrence_plan_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-remediation-sla-escalation-recurrence-plan",
            "--recurrence-policy",
            str(recurrence_policy),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_recurrence_plan_path = tmp_path / "endpoint-remediation-sla-escalation-recurrence-plan.json"
    if sla_escalation_recurrence_plan_cli.exit_code == 0:
        sla_escalation_recurrence_plan_path.write_text(sla_escalation_recurrence_plan_cli.output, encoding="utf-8")
    sla_escalation_recurrence_delivery_cli = runner.invoke(
        app,
        [
            "release",
            "deliver-endpoint-remediation-sla-escalation-recurrence",
            str(sla_escalation_recurrence_plan_path),
            "--config",
            str(connector_config),
            "--provider",
            "webhook",
            "--retries",
            "0",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_suppression_audit_cli = runner.invoke(
        app,
        [
            "release",
            "export-endpoint-remediation-sla-escalation-suppression-audit",
            str(sla_escalation_recurrence_plan_path),
            "--output",
            str(tmp_path / "cli-escalation-suppression-audit"),
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_recurrence_retry_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-remediation-sla-escalation-recurrence-retry-plan",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_recurrence_retry_path = tmp_path / "endpoint-remediation-sla-escalation-recurrence-retry-plan.json"
    if sla_escalation_recurrence_retry_cli.exit_code == 0:
        sla_escalation_recurrence_retry_path.write_text(sla_escalation_recurrence_retry_cli.output, encoding="utf-8")
    sla_escalation_owner_digest_cli = runner.invoke(
        app,
        [
            "release",
            "deliver-endpoint-remediation-sla-escalation-owner-digest",
            str(sla_escalation_recurrence_plan_path),
            "--retry-plan",
            str(sla_escalation_recurrence_retry_path),
            "--config",
            str(connector_config),
            "--provider",
            "webhook",
            "--retries",
            "0",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_suppression_trends_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-remediation-sla-escalation-suppression-trends",
            "--metadata-json",
            str(metadata_json),
            "--json",
        ],
    )
    sla_escalation_recurrence_history_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-escalation-recurrence-history", "--metadata-json", str(metadata_json)],
    )
    sla_escalation_recurrence_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-escalation-recurrence-dashboard", "--metadata-json", str(metadata_json)],
    )
    sla_escalation_history_cli = runner.invoke(
        app,
        [
            "release",
            "endpoint-remediation-sla-escalation-history",
            "--metadata-json",
            str(metadata_json),
            "--active-only",
        ],
    )
    sla_escalation_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-escalation-dashboard", "--metadata-json", str(metadata_json)],
    )
    sla_history_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-history", "--metadata-json", str(metadata_json)],
    )
    sla_dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-sla-dashboard", "--metadata-json", str(metadata_json)],
    )
    dashboard_cli = runner.invoke(
        app,
        ["release", "endpoint-remediation-dashboard", "--metadata-json", str(metadata_json)],
    )
    assert execution_cli.exit_code == 0
    assert json.loads(execution_cli.output)["execution"]["execution_status"] == "recorded"
    assert handoff_cli.exit_code == 0
    assert handoff_payload["metadata"]["metadata_kind"] == "endpoint-remediation-handoff"
    assert handoff_status_cli.exit_code == 0
    assert json.loads(handoff_status_cli.output)["metadata"]["metadata_kind"] == "endpoint-remediation-handoff-status"
    assert history_cli.exit_code == 0
    assert json.loads(history_cli.output)["total"] == 2
    assert handoff_history_cli.exit_code == 0
    assert json.loads(handoff_history_cli.output)["total"] == 1
    assert handoff_dashboard_cli.exit_code == 0
    assert json.loads(handoff_dashboard_cli.output)["provider_count"] == 2
    assert handoff_status_history_cli.exit_code == 0
    assert json.loads(handoff_status_history_cli.output)["total"] == 1
    assert handoff_status_dashboard_cli.exit_code == 0
    assert json.loads(handoff_status_dashboard_cli.output)["in_progress_count"] == 1
    assert sla_cli.exit_code == 0
    assert json.loads(sla_cli.output)["metadata"]["metadata_kind"] == "endpoint-remediation-sla-report"
    assert sla_delivery_cli.exit_code == 0
    sla_delivery_payload = json.loads(sla_delivery_cli.output)
    assert sla_delivery_payload["metadata"]["connector_delivery_source"] == "endpoint_remediation_sla_notification"
    assert sla_delivery_payload["delivery"]["event_type"] == "cavra.endpoint_remediation_sla.notification"
    assert sla_delivery_payload["plan_metadata"]["metadata_kind"] == "endpoint-remediation-sla-notification-plan"
    assert sla_delivery_suppressed_cli.exit_code == 0
    assert json.loads(sla_delivery_suppressed_cli.output)["delivery"] is None
    assert json.loads(sla_delivery_suppressed_cli.output)["plan"]["suppressed_providers"][0]["provider"] == "webhook"
    assert sla_notification_ack_cli.exit_code == 0
    assert json.loads(sla_notification_ack_cli.output)["metadata"]["metadata_kind"] == "endpoint-remediation-sla-notification-ack"
    assert sla_notification_history_cli.exit_code == 0
    assert json.loads(sla_notification_history_cli.output)["total"] >= 4
    assert sla_notification_dashboard_cli.exit_code == 0
    assert json.loads(sla_notification_dashboard_cli.output)["suppressed_provider_count"] >= 1
    assert sla_escalation_plan_cli.exit_code == 0
    assert json.loads(sla_escalation_plan_cli.output)["metadata"]["metadata_kind"] == "endpoint-remediation-sla-escalation-plan"
    assert sla_escalation_delivery_cli.exit_code == 0
    assert json.loads(sla_escalation_delivery_cli.output)["metadata"]["connector_delivery_source"] == "endpoint_remediation_sla_escalation_delivery"
    assert json.loads(sla_escalation_delivery_cli.output)["event"]["event_type"] == "cavra.endpoint_remediation_sla.escalation_delivery"
    assert sla_escalation_review_cli.exit_code == 0
    assert json.loads(sla_escalation_review_cli.output)["metadata"]["metadata_kind"] == "endpoint-remediation-sla-escalation-review"
    assert sla_escalation_action_history_cli.exit_code == 0
    assert json.loads(sla_escalation_action_history_cli.output)["total"] >= 3
    assert sla_escalation_action_dashboard_cli.exit_code == 0
    assert json.loads(sla_escalation_action_dashboard_cli.output)["delivery_count"] >= 1
    assert sla_escalation_recurrence_plan_cli.exit_code == 0
    assert (
        json.loads(sla_escalation_recurrence_plan_cli.output)["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-recurrence-plan"
    )
    assert sla_escalation_recurrence_delivery_cli.exit_code == 0
    assert (
        json.loads(sla_escalation_recurrence_delivery_cli.output)["event"]["event_type"]
        == "cavra.endpoint_remediation_sla.escalation_recurrence_delivery"
    )
    assert sla_escalation_suppression_audit_cli.exit_code == 0
    assert (
        json.loads(sla_escalation_suppression_audit_cli.output)["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-suppression-audit"
    )
    assert sla_escalation_recurrence_retry_cli.exit_code == 0
    assert (
        json.loads(sla_escalation_recurrence_retry_cli.output)["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-recurrence-retry-plan"
    )
    assert sla_escalation_owner_digest_cli.exit_code == 0
    assert (
        json.loads(sla_escalation_owner_digest_cli.output)["digest_metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-owner-digest"
    )
    assert sla_escalation_suppression_trends_cli.exit_code == 0
    assert (
        json.loads(sla_escalation_suppression_trends_cli.output)["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-suppression-trend"
    )
    assert sla_escalation_recurrence_history_cli.exit_code == 0
    assert json.loads(sla_escalation_recurrence_history_cli.output)["total"] >= 1
    assert sla_escalation_recurrence_dashboard_cli.exit_code == 0
    assert json.loads(sla_escalation_recurrence_dashboard_cli.output)["route_count"] >= 1
    assert sla_escalation_history_cli.exit_code == 0
    assert json.loads(sla_escalation_history_cli.output)["total"] >= 1
    assert sla_escalation_dashboard_cli.exit_code == 0
    assert json.loads(sla_escalation_dashboard_cli.output)["active_escalation_count"] >= 1
    assert sla_history_cli.exit_code == 0
    assert json.loads(sla_history_cli.output)["total"] == 1
    assert sla_dashboard_cli.exit_code == 0
    assert json.loads(sla_dashboard_cli.output)["report_count"] == 1
    assert dashboard_cli.exit_code == 0
    assert json.loads(dashboard_cli.output)["request_count"] == 1


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

    connector_config = tmp_path / "connectors.json"
    connector_config.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra?token=secret"}}}),
        encoding="utf-8",
    )
    delivery_metadata = tmp_path / "delivery-metadata.json"
    promotion_delivery = runner.invoke(
        app,
        [
            "release",
            "deliver-promotion-audit",
            str(tmp_path / "promotion-execution" / "rollout-promotion-execution.json"),
            "--config",
            str(connector_config),
            "--provider",
            "webhook",
            "--retries",
            "1",
            "--timeout-seconds",
            "0.1",
            "--output",
            str(tmp_path / "promotion-delivery"),
            "--metadata-json",
            str(delivery_metadata),
            "--json",
        ],
    )
    rollback_delivery = runner.invoke(
        app,
        [
            "release",
            "deliver-rollback-execution",
            str(tmp_path / "rollback-execution" / "rollout-rollback-execution.json"),
            "--config",
            str(connector_config),
            "--provider",
            "webhook",
            "--retries",
            "1",
            "--timeout-seconds",
            "0.1",
            "--output",
            str(tmp_path / "rollback-delivery"),
            "--metadata-json",
            str(delivery_metadata),
            "--json",
        ],
    )
    assert promotion_delivery.exit_code == 0
    promotion_delivery_payload = json.loads(promotion_delivery.output)
    assert promotion_delivery_payload["event_id"] == promotion.execution["execution_id"]
    assert promotion_delivery_payload["deliveries"][0]["attempt_count"] == 2
    assert promotion_delivery_payload["deliveries"][0]["request"]["url"].endswith("?REDACTED")
    assert promotion_delivery_payload["metadata"]["metadata_kind"] == "release-connector-delivery"
    assert str(delivery_metadata) in promotion_delivery_payload["indexed_metadata_stores"]
    assert rollback_delivery.exit_code == 0
    rollback_delivery_payload = json.loads(rollback_delivery.output)
    assert rollback_delivery_payload["event_id"] == result.rollback["rollback_id"]
    assert rollback_delivery_payload["deliveries"][0]["attempt_count"] == 2
    history = runner.invoke(
        app,
        [
            "release",
            "connector-delivery-history",
            "--metadata-json",
            str(delivery_metadata),
            "--provider",
            "webhook",
            "--no-success",
        ],
    )
    dashboard = runner.invoke(
        app,
        [
            "release",
            "connector-delivery-dashboard",
            "--metadata-json",
            str(delivery_metadata),
        ],
    )
    assert history.exit_code == 0
    assert json.loads(history.output)["total"] == 2
    assert dashboard.exit_code == 0
    assert json.loads(dashboard.output)["alert_level"] == "critical"


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
