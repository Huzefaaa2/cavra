from pathlib import Path

from cavra.evidence import (
    create_evidence_bundle,
    export_immutable_storage_plan,
    export_siem_payloads,
    verify_evidence_bundle,
)
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


def test_export_siem_payloads_for_supported_providers(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    output_dir = tmp_path / "exports"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="pytest")

    result = export_siem_payloads(bundle_dir, output_dir)

    assert result.output_dir == output_dir
    assert (output_dir / "splunk-hec-events.json").exists()
    assert (output_dir / "sentinel-log-analytics.json").exists()
    assert (output_dir / "datadog-events.json").exists()
    assert (output_dir / "webhook-payload.json").exists()


def test_export_siem_payloads_rejects_unknown_provider(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="pytest")

    try:
        export_siem_payloads(bundle_dir, tmp_path / "exports", provider="unknown")
    except ValueError as exc:
        assert "unknown SIEM provider" in str(exc)
    else:
        raise AssertionError("expected unknown provider to fail")


def test_export_immutable_storage_plan(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    output_dir = tmp_path / "storage"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="pytest", key="secret")

    result = export_immutable_storage_plan(
        bundle_dir,
        output_dir,
        retention_days=365,
        s3_bucket="enterprise-cavra-evidence",
        azure_account="enterpriseevidence",
    )

    plan_path = output_dir / "immutable-storage-plan.json"
    assert result.output_dir == output_dir
    assert plan_path.exists()
    assert (output_dir / "immutable-storage-plan.md").exists()
    assert "enterprise-cavra-evidence" in plan_path.read_text(encoding="utf-8")
    assert "enterpriseevidence" in plan_path.read_text(encoding="utf-8")
