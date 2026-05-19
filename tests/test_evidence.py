import json
from pathlib import Path

from cavra.evidence import (
    EvidenceArtifactError,
    EvidenceMetadataStore,
    SQLiteEvidenceMetadataStore,
    apply_sqlite_migrations,
    build_evidence_artifact_archive,
    build_trust_root_bundle,
    create_evidence_bundle,
    export_attestation_verification,
    export_immutable_storage_plan,
    export_key_trust_root,
    export_retention_policy,
    export_siem_payloads,
    export_trust_root_distribution,
    export_trust_root_bundle,
    generate_ed25519_keypair,
    list_evidence_artifacts,
    load_evidence_artifact,
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
    assert (tmp_path / "retention-policy.json").exists()
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
    assert "examples/immutable-storage/aws-s3-object-lock" in plan_path.read_text(encoding="utf-8")
    assert "examples/immutable-storage/azure-blob-immutability" in plan_path.read_text(encoding="utf-8")


def test_ed25519_signed_evidence_bundle_verifies(tmp_path: Path) -> None:
    private_key = tmp_path / "private.pem"
    public_key = tmp_path / "public.pem"
    generate_ed25519_keypair(private_key, public_key)

    create_evidence_bundle(
        _decisions(),
        tmp_path / "bundle",
        session_id="pytest",
        signer="pytest",
        private_key=private_key,
    )

    ok, errors = verify_evidence_bundle(tmp_path / "bundle", public_key=public_key)
    assert ok, errors


def test_trust_root_verifies_key_id(tmp_path: Path) -> None:
    private_key = tmp_path / "private.pem"
    public_key = tmp_path / "public.pem"
    trust_root = tmp_path / "trust-root.json"
    generate_ed25519_keypair(private_key, public_key)
    export_key_trust_root(public_key, trust_root, key_id="prod-signing", owner="security")
    create_evidence_bundle(
        _decisions(),
        tmp_path / "bundle",
        session_id="pytest",
        signer="security",
        private_key=private_key,
        key_id="prod-signing",
    )

    ok, errors = verify_evidence_bundle(tmp_path / "bundle", trust_root=trust_root, key_id="prod-signing")

    assert ok, errors


def test_trust_root_bundle_verifies_matching_key(tmp_path: Path) -> None:
    private_key = tmp_path / "private.pem"
    public_key = tmp_path / "public.pem"
    trust_root = tmp_path / "trust-root.json"
    trust_bundle = tmp_path / "trust-roots.json"
    generate_ed25519_keypair(private_key, public_key)
    export_key_trust_root(public_key, trust_root, key_id="prod-signing", owner="security")
    export_trust_root_bundle([trust_root], trust_bundle)
    create_evidence_bundle(
        _decisions(),
        tmp_path / "bundle",
        session_id="pytest",
        signer="security",
        private_key=private_key,
        key_id="prod-signing",
    )

    ok, errors = verify_evidence_bundle(tmp_path / "bundle", trust_root=trust_bundle, key_id="prod-signing")

    assert ok, errors


def test_trust_root_bundle_rejects_duplicate_key_ids(tmp_path: Path) -> None:
    first_private = tmp_path / "first-private.pem"
    first_public = tmp_path / "first-public.pem"
    second_private = tmp_path / "second-private.pem"
    second_public = tmp_path / "second-public.pem"
    first_root = tmp_path / "first-root.json"
    second_root = tmp_path / "second-root.json"
    generate_ed25519_keypair(first_private, first_public)
    generate_ed25519_keypair(second_private, second_public)
    export_key_trust_root(first_public, first_root, key_id="duplicate")
    export_key_trust_root(second_public, second_root, key_id="duplicate")

    try:
        build_trust_root_bundle([first_root, second_root])
    except ValueError as exc:
        assert "duplicate trust-root key IDs" in str(exc)
    else:
        raise AssertionError("expected duplicate key IDs to fail")


def test_export_trust_root_distribution_creates_offline_artifacts(tmp_path: Path) -> None:
    private_key = tmp_path / "private.pem"
    public_key = tmp_path / "public.pem"
    trust_root = tmp_path / "trust-root.json"
    output = tmp_path / "distribution"
    generate_ed25519_keypair(private_key, public_key)
    export_key_trust_root(public_key, trust_root, key_id="prod-signing", owner="security")

    result = export_trust_root_distribution(
        [trust_root],
        output,
        environment="regulated-prod",
        distribution_id="dist-2026-q2",
        channels=["source-control", "offline-media"],
    )

    assert result.output_dir == output
    bundle = json.loads((output / "evidence-trust-roots.json").read_text(encoding="utf-8"))
    manifest = json.loads((output / "trust-root-distribution-manifest.json").read_text(encoding="utf-8"))
    checksums = (output / "checksums.txt").read_text(encoding="utf-8")
    readme = (output / "trust-root-distribution.md").read_text(encoding="utf-8")
    assert bundle["schema_version"] == "cavra.evidence.trust-root-bundle.v1"
    assert manifest["schema_version"] == "cavra.evidence.trust-root-distribution.v1"
    assert manifest["distribution_id"] == "dist-2026-q2"
    assert manifest["environment"] == "regulated-prod"
    assert manifest["bundle"]["active_key_ids"] == ["prod-signing"]
    assert "offline-media" in manifest["channels"]
    assert "evidence-trust-roots.json" in checksums
    assert "trust-root-distribution-manifest.json" in checksums
    assert "cavra evidence verify" in readme


def test_retention_policy_minimum_is_enforced(tmp_path: Path) -> None:
    create_evidence_bundle(_decisions(), tmp_path, session_id="pytest", retention_days=30)

    ok, errors = verify_evidence_bundle(tmp_path, minimum_retention_days=365)

    assert not ok
    assert "retention policy below minimum" in errors


def test_export_retention_policy_for_existing_bundle(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    output_dir = tmp_path / "retention"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="pytest")

    result = export_retention_policy(
        bundle_dir,
        output_dir,
        retention_days=365,
        classification="audit",
        legal_hold=True,
    )

    assert result.output_dir == output_dir
    policy = (output_dir / "retention-policy.json").read_text(encoding="utf-8")
    assert "audit" in policy
    assert "365" in policy
    assert (output_dir / "retention-policy.md").exists()


def test_evidence_metadata_store_indexes_bundle(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="pytest")
    store = EvidenceMetadataStore(tmp_path / "metadata.json")

    metadata = store.index_bundle(bundle_dir)

    assert metadata["session_id"] == "pytest"
    assert metadata["decision_count"] == 3
    assert store.get("pytest")["blocked_count"] == 2


def test_evidence_artifact_root_lists_and_loads_allowed_files(tmp_path: Path) -> None:
    root = tmp_path / "artifacts"
    bundle_dir = root / "pytest"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="pytest")

    listing = list_evidence_artifacts(
        root,
        "pytest",
        base_path="/evidence/pytest/artifacts",
        bundle_path="/evidence/pytest/artifact-bundle",
    )
    metadata, payload = load_evidence_artifact(root, "pytest", "pr-attestation.md")
    archive_metadata, archive_payload = build_evidence_artifact_archive(root, "pytest")

    assert listing["artifact_count"] == 7
    assert listing["bundle_download_url"] == "/evidence/pytest/artifact-bundle"
    assert any(item["artifact"] == "pr-attestation.md" for item in listing["artifacts"])
    assert metadata["media_type"] == "text/markdown"
    assert b"CAVRA PR Attestation" in payload
    assert archive_metadata["media_type"] == "application/zip"
    assert archive_payload.startswith(b"PK")


def test_evidence_artifact_root_rejects_unsafe_paths(tmp_path: Path) -> None:
    root = tmp_path / "artifacts"
    create_evidence_bundle(_decisions(), root / "pytest", session_id="pytest")

    for session_id, artifact_name in [("../outside", "manifest.json"), ("pytest", "../manifest.json")]:
        try:
            load_evidence_artifact(root, session_id, artifact_name)
        except EvidenceArtifactError:
            pass
        else:
            raise AssertionError("expected unsafe artifact path to fail")


def test_sqlite_evidence_metadata_store_searches_with_pagination(tmp_path: Path) -> None:
    first_bundle = tmp_path / "first"
    second_bundle = tmp_path / "second"
    create_evidence_bundle(_decisions(), first_bundle, session_id="first", signer="security")
    create_evidence_bundle(_decisions()[:1], second_bundle, session_id="second", signer="docs")
    store = SQLiteEvidenceMetadataStore(tmp_path / "metadata.db")
    store.index_bundle(first_bundle)
    store.index_bundle(second_bundle)

    blocked = store.search(min_blocked=2, limit=10, offset=0)
    signed_by_docs = store.search(signer="docs", limit=10, offset=0)
    first_page = store.search(limit=1, offset=0)

    assert blocked["total"] == 1
    assert blocked["items"][0]["session_id"] == "first"
    assert signed_by_docs["items"][0]["session_id"] == "second"
    assert first_page["limit"] == 1
    assert len(first_page["items"]) == 1


def test_sqlite_evidence_metadata_store_filters_rollout_metadata(tmp_path: Path) -> None:
    store = SQLiteEvidenceMetadataStore(tmp_path / "metadata.db")
    store.upsert(
        {
            "session_id": "rollout-1",
            "created_at": "2026-05-19T00:00:00Z",
            "signer": "release-agent",
            "decision_count": 0,
            "blocked_count": 0,
            "approval_required_count": 0,
            "metadata_kind": "managed-endpoint-rollout",
            "rollout_status": "staged",
            "environment": "production",
            "deployment_targets": ["github-actions-linux-amd64-runner"],
        }
    )
    store.upsert(
        {
            "session_id": "session-1",
            "created_at": "2026-05-19T00:01:00Z",
            "signer": "security",
            "decision_count": 1,
            "blocked_count": 0,
            "approval_required_count": 0,
        }
    )

    result = store.search(
        metadata_kind="managed-endpoint-rollout",
        rollout_status="staged",
        environment="production",
        deployment_target="github-actions-linux-amd64-runner",
    )

    assert result["total"] == 1
    assert result["items"][0]["session_id"] == "rollout-1"


def test_export_attestation_verification(tmp_path: Path) -> None:
    bundle_dir = tmp_path / "bundle"
    output_dir = tmp_path / "attestation"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="pytest")

    result = export_attestation_verification(bundle_dir, output_dir)

    assert (output_dir / "pr-attestation-verification.json").exists()
    assert (output_dir / "pr-attestation-verification.md").exists()
    assert result.output_dir == output_dir


def test_apply_sqlite_migrations_is_idempotent(tmp_path: Path) -> None:
    database = tmp_path / "metadata.db"
    migrations_dir = Path("migrations/sqlite")

    first = apply_sqlite_migrations(database, migrations_dir)
    second = apply_sqlite_migrations(database, migrations_dir)

    assert first["applied"] == [
        "001_evidence_metadata.sql",
        "002_approval_router.sql",
        "003_agent_mcp_registry.sql",
        "004_activity_sessions_decisions.sql",
        "005_repository_policy_rollout.sql",
        "006_integrations_inventory.sql",
    ]
    assert second["applied"] == []
    assert second["skipped"] == [
        "001_evidence_metadata.sql",
        "002_approval_router.sql",
        "003_agent_mcp_registry.sql",
        "004_activity_sessions_decisions.sql",
        "005_repository_policy_rollout.sql",
        "006_integrations_inventory.sql",
    ]
