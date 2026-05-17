from pathlib import Path

from cavra.evidence import create_evidence_bundle, verify_evidence_bundle
from cavra.runtime import RuntimeGuard


def _decisions() -> list[dict[str, object]]:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    return [
        guard.evaluate_file_access(Path(".env"), "read").to_dict(),
        guard.evaluate_command("terraform plan").to_dict(),
        guard.evaluate_command("terraform apply -auto-approve").to_dict(),
    ]


def test_create_and_verify_evidence_bundle(tmp_path: Path) -> None:
    result = create_evidence_bundle(_decisions(), tmp_path, session_id="pytest", signer="pytest", key="secret")
    assert result.manifest_path.exists()
    assert (tmp_path / "evidence.json").exists()
    assert (tmp_path / "pr-attestation.md").exists()
    assert (tmp_path / "compliance-mapping.md").exists()
    assert (tmp_path / "siem-event.json").exists()
    ok, errors = verify_evidence_bundle(tmp_path, key="secret")
    assert ok, errors


def test_verify_evidence_bundle_detects_tampering(tmp_path: Path) -> None:
    create_evidence_bundle(_decisions(), tmp_path, session_id="pytest")
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_text(evidence_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    ok, errors = verify_evidence_bundle(tmp_path)
    assert not ok
    assert any("checksum mismatch" in error for error in errors)
