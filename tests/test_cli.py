import json
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.evidence import create_evidence_bundle
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
