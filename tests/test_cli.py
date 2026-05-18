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
