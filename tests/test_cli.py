import json
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.evidence import create_evidence_bundle, export_key_trust_root, generate_ed25519_keypair
from cavra.runtime import RuntimeGuard


runner = CliRunner()


def _decisions() -> list[dict[str, object]]:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    return [
        guard.evaluate_file_access(Path(".env"), "read").to_dict(),
        guard.evaluate_command("terraform plan").to_dict(),
    ]


def test_verify_attestation_cli_fails_invalid_report(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    create_evidence_bundle(_decisions(), bundle, session_id="cli-test")
    (bundle / "pr-attestation.md").unlink()

    result = runner.invoke(
        app,
        [
            "evidence",
            "verify-attestation",
            str(bundle),
            "--output",
            str(tmp_path / "attestation"),
        ],
    )

    assert result.exit_code == 1
    assert "PR attestation verification failed" in result.output
    assert "missing pr-attestation.md" in result.output


def test_verify_attestation_cli_exports_valid_report(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    create_evidence_bundle(_decisions(), bundle, session_id="cli-test")

    result = runner.invoke(
        app,
        [
            "evidence",
            "verify-attestation",
            str(bundle),
            "--output",
            str(tmp_path / "attestation"),
        ],
    )

    assert result.exit_code == 0
    assert "PR attestation verification exported" in result.output


def test_runtime_go_pilot_readiness_cli_reports_disabled() -> None:
    result = runner.invoke(app, ["runtime", "go-pilot-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.readiness.v1"
    assert payload["status"] == "disabled"


def test_runtime_go_deployment_readiness_cli_reports_not_configured() -> None:
    result = runner.invoke(app, ["runtime", "go-deployment-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.deployment-readiness.v1"
    assert payload["status"] == "not_configured"


def test_runtime_go_promotion_readiness_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-promotion-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.promotion-readiness.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_readiness_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-readiness.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_rehearsal_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-rehearsal", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-rehearsal.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_drills_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-drills", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-drill-history.v1"
    assert payload["status"] == "not_requested"


def test_integration_deliver_cli_accepts_config_option(tmp_path: Path) -> None:
    event = tmp_path / "event.json"
    config = tmp_path / "connectors.json"
    output = tmp_path / "delivery"
    event.write_text(
        json.dumps(
            {
                "event_type": "cavra.evidence_bundle",
                "session_id": "cli-connector-test",
                "decision_count": 1,
                "blocked_count": 1,
                "approval_required_count": 0,
                "max_severity": "high",
            }
        ),
        encoding="utf-8",
    )
    config.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra?token=secret"}}}),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "integration",
            "deliver",
            str(event),
            "--config",
            str(config),
            "--provider",
            "webhook",
            "--retries",
            "0",
            "--timeout-seconds",
            "0.1",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert "connector delivery evidence exported" in result.output
    assert list(output.glob("*.json"))


def test_trust_distribution_cli_exports_offline_package(tmp_path: Path) -> None:
    private_key = tmp_path / "private.pem"
    public_key = tmp_path / "public.pem"
    trust_root = tmp_path / "trust-root.json"
    output = tmp_path / "trust-distribution"
    generate_ed25519_keypair(private_key, public_key)
    export_key_trust_root(public_key, trust_root, key_id="cli-prod")

    result = runner.invoke(
        app,
        [
            "evidence",
            "trust-distribution",
            str(trust_root),
            "--output",
            str(output),
            "--environment",
            "prod",
            "--distribution-id",
            "cli-dist",
            "--channel",
            "source-control",
            "--channel",
            "offline-media",
        ],
    )

    assert result.exit_code == 0
    assert "trust-root distribution exported" in result.output
    manifest = json.loads((output / "trust-root-distribution-manifest.json").read_text(encoding="utf-8"))
    assert manifest["distribution_id"] == "cli-dist"
    assert manifest["channels"] == ["source-control", "offline-media"]
