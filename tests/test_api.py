import json
import time
from base64 import urlsafe_b64encode

from fastapi.testclient import TestClient

from cavra.api import create_app
from cavra.evidence import create_evidence_bundle, generate_ed25519_keypair, sha256_file
from cavra.runtime import RuntimeGuard


def _b64url(data: bytes) -> str:
    return urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _signed_rs256_token(claims: dict[str, object], *, kid: str = "api-test-key") -> tuple[str, dict[str, object]]:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding, rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_numbers = private_key.public_key().public_numbers()
    jwk = {
        "kty": "RSA",
        "kid": kid,
        "alg": "RS256",
        "use": "sig",
        "n": _b64url(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, "big")),
        "e": _b64url(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, "big")),
    }
    signing_input = ".".join(
        [
            _b64url(json.dumps({"alg": "RS256", "kid": kid, "typ": "JWT"}, separators=(",", ":")).encode("utf-8")),
            _b64url(json.dumps(claims, separators=(",", ":")).encode("utf-8")),
        ]
    ).encode("ascii")
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{signing_input.decode('ascii')}.{_b64url(signature)}", {"keys": [jwk]}


def test_api_persists_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())

    response = client.post("/evidence", json={"session_id": "api-session", "decision_count": 2})

    assert response.status_code == 200
    assert response.json()["session_id"] == "api-session"
    assert client.get("/evidence").json()["items"][0]["session_id"] == "api-session"
    assert client.get("/evidence/api-session").json()["decision_count"] == 2


def test_api_filters_json_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())
    client.post("/evidence", json={"session_id": "blocked-session", "signer": "security", "blocked_count": 2})
    client.post("/evidence", json={"session_id": "clean-session", "signer": "docs", "blocked_count": 0})

    response = client.get("/evidence", params={"signer": "security", "min_blocked": 1, "limit": 10})

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["session_id"] == "blocked-session"


def test_api_filters_json_rollout_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())
    client.post(
        "/evidence",
        json={
            "session_id": "rollout-1",
            "signer": "release-agent",
            "metadata_kind": "managed-endpoint-rollout",
            "rollout_status": "staged",
            "environment": "production",
            "deployment_targets": ["github-actions-linux-amd64-runner"],
        },
    )
    client.post("/evidence", json={"session_id": "regular-session", "signer": "security"})

    response = client.get(
        "/evidence",
        params={
            "metadata_kind": "managed-endpoint-rollout",
            "rollout_status": "staged",
            "environment": "production",
            "deployment_target": "github-actions-linux-amd64-runner",
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["session_id"] == "rollout-1"


def test_api_searches_sqlite_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_DB", str(tmp_path / "metadata.db"))
    client = TestClient(create_app())
    client.post("/evidence", json={"session_id": "blocked-session", "signer": "security", "blocked_count": 2})
    client.post("/evidence", json={"session_id": "clean-session", "signer": "docs", "blocked_count": 0})

    response = client.get("/evidence", params={"signer": "security", "min_blocked": 1, "limit": 10})

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["session_id"] == "blocked-session"


def test_api_filters_sqlite_rollout_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_DB", str(tmp_path / "metadata.db"))
    client = TestClient(create_app())
    client.post(
        "/evidence",
        json={
            "session_id": "rollout-1",
            "signer": "release-agent",
            "metadata_kind": "managed-endpoint-rollout",
            "rollout_status": "succeeded",
            "environment": "production",
            "deployment_targets": ["windows-intune-amd64-workstation"],
        },
    )
    client.post("/evidence", json={"session_id": "regular-session", "signer": "security"})

    response = client.get(
        "/evidence",
        params={
            "metadata_kind": "managed-endpoint-rollout",
            "rollout_status": "succeeded",
            "deployment_target": "windows-intune-amd64-workstation",
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["session_id"] == "rollout-1"


def test_api_serves_configured_evidence_artifacts(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    monkeypatch.setenv("CAVRA_EVIDENCE_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    create_evidence_bundle(
        [guard.evaluate_command("terraform plan").to_dict()],
        tmp_path / "artifacts" / "api-session",
        session_id="api-session",
        signer="platform-security",
    )
    client = TestClient(create_app())
    client.post("/evidence", json={"session_id": "api-session", "decision_count": 1, "signer": "platform-security"})

    listing = client.get("/evidence/api-session/artifacts")
    attestation = client.get("/evidence/api-session/artifacts/pr-attestation.md")
    bundle = client.get("/evidence/api-session/artifact-bundle")
    rejected = client.get("/evidence/api-session/artifacts/../../etc/passwd")
    config = client.get("/console/config").json()

    assert listing.status_code == 200
    assert listing.json()["artifact_count"] == 7
    assert any(item["artifact"] == "pr-attestation.md" for item in listing.json()["artifacts"])
    assert attestation.status_code == 200
    assert attestation.headers["content-type"].startswith("text/markdown")
    assert "CAVRA PR Attestation" in attestation.text
    assert bundle.status_code == 200
    assert bundle.content.startswith(b"PK")
    assert rejected.status_code in {400, 404}
    assert config["evidence_artifacts"] == "configured"
    assert config["endpoints"]["evidence_artifact_bundle"] == "/evidence/{session_id}/artifact-bundle"


def test_api_serves_configured_rollout_evidence_artifacts(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    artifact_root = tmp_path / "artifacts"
    rollout_dir = artifact_root / "rollout-1"
    rollout_dir.mkdir(parents=True)
    evidence_path = rollout_dir / "managed-endpoint-rollout-evidence.json"
    summary_path = rollout_dir / "managed-endpoint-rollout-evidence.md"
    evidence_path.write_text(
        json.dumps({"schema_version": "cavra.go-runtime.endpoint-rollout-evidence.v1", "rollout_id": "rollout-1"}),
        encoding="utf-8",
    )
    summary_path.write_text("# Rollout\n", encoding="utf-8")
    (rollout_dir / "checksums.txt").write_text(
        "\n".join(
            [
                f"{sha256_file(evidence_path)}  managed-endpoint-rollout-evidence.json",
                f"{sha256_file(summary_path)}  managed-endpoint-rollout-evidence.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_EVIDENCE_ARTIFACT_ROOT", str(artifact_root))
    client = TestClient(create_app())
    client.post(
        "/evidence",
        json={
            "session_id": "rollout-1",
            "metadata_kind": "managed-endpoint-rollout",
            "bundle_dir": str(rollout_dir),
            "rollout_status": "staged",
            "environment": "production",
        },
    )

    listing = client.get("/evidence/rollout-1/artifacts")
    evidence = client.get("/evidence/rollout-1/artifacts/managed-endpoint-rollout-evidence.json")
    bundle = client.get("/evidence/rollout-1/artifact-bundle")
    rejected = client.get("/evidence/rollout-1/artifacts/evidence.json")

    assert listing.status_code == 200
    assert listing.json()["metadata_kind"] == "managed-endpoint-rollout"
    assert listing.json()["artifact_count"] == 3
    assert listing.json()["rollout_artifact_integrity"]["status"] == "verified"
    assert listing.json()["promotion_readiness"]["status"] == "ready"
    assert listing.json()["artifacts"][0]["artifact"] == "managed-endpoint-rollout-evidence.json"
    assert evidence.status_code == 200
    assert evidence.headers["content-type"].startswith("application/json")
    assert evidence.json()["rollout_id"] == "rollout-1"
    assert bundle.status_code == 200
    assert bundle.content.startswith(b"PK")
    assert rejected.status_code == 400


def test_api_creates_signed_rollout_promotion_approval(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    connector_config = tmp_path / "connectors.json"
    connector_config.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra?token=secret"}}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_CONNECTOR_CONFIG", str(connector_config))
    private_key = tmp_path / "keys" / "private.pem"
    public_key = tmp_path / "keys" / "public.pem"
    generate_ed25519_keypair(private_key, public_key)
    monkeypatch.setenv("CAVRA_ROLLOUT_PROMOTION_SIGNING_KEY", private_key.read_text(encoding="utf-8"))
    artifact_root = tmp_path / "artifacts"
    rollout_dir = artifact_root / "rollout-1"
    rollout_dir.mkdir(parents=True)
    evidence_path = rollout_dir / "managed-endpoint-rollout-evidence.json"
    summary_path = rollout_dir / "managed-endpoint-rollout-evidence.md"
    evidence_path.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-runtime.endpoint-rollout-evidence.v1",
                "rollout_id": "rollout-1",
                "status": "staged",
                "change_record": "CHG-123",
                "environment": "production",
                "rollout_ring": "pilot",
                "release": {"version": "v0.1.0", "repository": "Huzefaaa2/cavra"},
                "deployment_targets": [
                    {
                        "id": "github-actions-linux-amd64-runner",
                        "rollback_steps": ["Restore previous signed runtime package."],
                    }
                ],
                "controls": ["rollout-evidence-checksummed"],
            }
        ),
        encoding="utf-8",
    )
    summary_path.write_text("# Rollout\n", encoding="utf-8")
    (rollout_dir / "checksums.txt").write_text(
        "\n".join(
            [
                f"{sha256_file(evidence_path)}  managed-endpoint-rollout-evidence.json",
                f"{sha256_file(summary_path)}  managed-endpoint-rollout-evidence.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_EVIDENCE_ARTIFACT_ROOT", str(artifact_root))
    client = TestClient(create_app())
    client.post(
        "/evidence",
        json={
            "session_id": "rollout-1",
            "metadata_kind": "managed-endpoint-rollout",
            "bundle_dir": str(rollout_dir),
            "rollout_status": "staged",
        },
    )

    response = client.post(
        "/evidence/rollout-1/promotion-request",
        json={
            "target_ring": "production",
            "requested_by": "release-manager",
            "require_package_verification": False,
            "require_signatures": False,
            "require_provenance": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["valid"] is True
    assert response.json()["request"]["signature"]["algorithm"] == "Ed25519"
    approval = response.json()["approval"]
    assert approval["state"] == "pending"
    assert client.get("/approvals", params={"state": "pending"}).json()["items"][0]["approval_id"] == approval["approval_id"]
    assert client.get("/console/config").json()["endpoints"]["evidence_rollout_promotion_request"] == "/evidence/{session_id}/promotion-request"
    assert client.get("/console/config").json()["endpoints"]["evidence_rollout_promotion_execution"] == "/evidence/{session_id}/promotion-execution"
    assert client.get("/console/config").json()["endpoints"]["release_connector_deliveries"] == "/release-connector-deliveries"

    pending_execution = client.post(
        "/evidence/rollout-1/promotion-execution",
        json={"request": response.json()["request"], "approval_id": approval["approval_id"], "executed_by": "release-manager"},
    )
    assert pending_execution.status_code == 400

    approved = client.post(
        f"/approvals/{approval['approval_id']}/approve",
        json={"actor": "cab@example.com", "reason": "Approved production ring promotion."},
    )
    execution = client.post(
        "/evidence/rollout-1/promotion-execution",
        json={"request": response.json()["request"], "approval_id": approval["approval_id"], "executed_by": "release-manager"},
    )
    assert approved.status_code == 200
    assert execution.status_code == 200
    assert execution.json()["valid"] is True
    assert execution.json()["execution"]["ring_advancement"]["to"] == "production"
    assert execution.json()["execution"]["approval"]["state"] == "approved"
    assert execution.json()["metadata"]["metadata_kind"] == "rollout-promotion-execution"
    assert execution.json()["metadata"]["rollback_evidence_refs"] == execution.json()["execution"]["rollback_evidence_refs"]
    searched = client.get(
        "/promotion-executions",
        params={
            "rollout_id": "rollout-1",
            "target_ring": "production",
            "approval_state": "approved",
            "promotion_execution_status": "executed",
            "deployment_target": "github-actions-linux-amd64-runner",
        },
    )
    detail = client.get(f"/promotion-executions/{execution.json()['execution']['execution_id']}")
    evidence_search = client.get(
        "/evidence",
        params={
            "metadata_kind": "rollout-promotion-execution",
            "rollout_status": "promoted",
            "target_ring": "production",
            "approval_state": "approved",
        },
    )
    assert searched.status_code == 200
    assert searched.json()["total"] == 1
    assert detail.status_code == 200
    assert detail.json()["audit_links"]["approval"] == f"approval://{approval['approval_id']}"
    assert evidence_search.status_code == 200
    assert evidence_search.json()["items"][0]["session_id"] == execution.json()["execution"]["execution_id"]
    audit_export = client.get(f"/promotion-executions/{execution.json()['execution']['execution_id']}/audit-export")
    assert audit_export.status_code == 200
    assert audit_export.json()["event"]["event_type"] == "cavra.rollout_promotion_execution"
    audit_delivery = client.post(
        f"/promotion-executions/{execution.json()['execution']['execution_id']}/audit-export/deliver",
        json={"provider": "webhook", "retries": 1, "timeout_seconds": 0.1},
    )
    assert audit_delivery.status_code == 200
    assert audit_delivery.json()["event_id"] == execution.json()["execution"]["execution_id"]
    assert audit_delivery.json()["deliveries"][0]["attempt_count"] == 2
    assert audit_delivery.json()["deliveries"][0]["request"]["url"].endswith("?REDACTED")
    assert audit_delivery.json()["metadata"]["metadata_kind"] == "release-connector-delivery"
    rollback_approval = client.post(
        "/approvals",
        json={
            "decision": {
                "decision_id": "rollback-decision",
                "session_id": "rollout-1",
                "correlation_id": execution.json()["execution"]["execution_id"],
                "action_type": "release_rollback_endpoint_rollout",
                "target": "rollout-1",
                "decision": "require_approval",
                "severity": "high",
                "rule_id": "release.rollout.rollback.require_approval",
                "reason": "Rollback requires approved change control.",
                "metadata": {
                    "promotion_execution_id": execution.json()["execution"]["execution_id"],
                    "target_ring": "production",
                },
            },
            "approver_group": "Change Advisory Board",
            "requested_by": "release-manager",
        },
    )
    rollback_approval_id = rollback_approval.json()["approval_id"]
    approved_rollback = client.post(
        f"/approvals/{rollback_approval_id}/approve",
        json={"actor": "cab@example.com", "reason": "Approved rollback."},
    )
    rollback = client.post(
        f"/promotion-executions/{execution.json()['execution']['execution_id']}/rollback-execution",
        json={
            "approval_id": rollback_approval_id,
            "executed_by": "release-manager",
            "rollback_reason": "Production validation failed.",
        },
    )
    assert approved_rollback.status_code == 200
    assert rollback.status_code == 200
    assert rollback.json()["valid"] is True
    assert rollback.json()["metadata"]["metadata_kind"] == "rollout-rollback-execution"
    assert rollback.json()["rollback"]["ring_rollback"]["to"] == "pilot"
    rollback_detail = client.get(f"/rollback-executions/{rollback.json()['rollback']['rollback_id']}")
    rollback_search = client.get(
        "/evidence",
        params={
            "metadata_kind": "rollout-rollback-execution",
            "rollback_execution_status": "executed",
            "approval_state": "approved",
        },
    )
    assert rollback_detail.status_code == 200
    assert rollback_search.status_code == 200
    assert rollback_search.json()["items"][0]["session_id"] == rollback.json()["rollback"]["rollback_id"]
    rollback_delivery = client.post(
        f"/rollback-executions/{rollback.json()['rollback']['rollback_id']}/deliver",
        json={"provider": "webhook", "retries": 1, "timeout_seconds": 0.1},
    )
    assert rollback_delivery.status_code == 200
    assert rollback_delivery.json()["event_id"] == rollback.json()["rollback"]["rollback_id"]
    assert rollback_delivery.json()["deliveries"][0]["attempt_count"] == 2
    delivery_history = client.get("/release-connector-deliveries", params={"provider": "webhook", "success": False})
    delivery_dashboard = client.get("/release-connector-deliveries/dashboard")
    assert delivery_history.status_code == 200
    assert delivery_history.json()["total"] == 2
    assert delivery_dashboard.status_code == 200
    assert delivery_dashboard.json()["alert_level"] == "critical"
    assert delivery_dashboard.json()["failed_deliveries"] == 2

    rejected = client.post(
        "/evidence/rollout-1/promotion-request",
        json={
            "package_dir": str(tmp_path / "outside-package"),
            "require_package_verification": False,
            "require_signatures": False,
            "require_provenance": False,
        },
    )
    assert rejected.status_code == 400


def test_api_evidence_artifacts_require_configured_root(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.delenv("CAVRA_EVIDENCE_ARTIFACT_ROOT", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())
    client.post("/evidence", json={"session_id": "api-session", "decision_count": 1})

    response = client.get("/evidence/api-session/artifacts")
    config = client.get("/console/config").json()

    assert response.status_code == 400
    assert response.json()["detail"] == "evidence artifact root is not configured"
    assert config["evidence_artifacts"] == "disabled"


def test_api_release_channel_and_endpoint_export_history(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())
    promotion_metadata = {
        "session_id": "rcp_stable_1",
        "created_at": "2026-05-19T00:00:00+00:00",
        "signer": "release-manager",
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 1,
        "metadata_kind": "release-channel-promotion-request",
        "request_id": "rcp_stable_1",
        "channel": "stable",
        "target_ring": "enterprise",
        "approval_id": "apr_channel",
        "approval_state": "pending",
        "deployment_targets": ["linux-systemd-amd64-workstation"],
        "endpoint_management_tools": ["linux"],
        "request": {"request_id": "rcp_stable_1", "channel": "stable"},
    }
    export_metadata = {
        "session_id": "eme_stable_1",
        "created_at": "2026-05-19T00:05:00+00:00",
        "signer": "release-manager",
        "decision_count": 0,
        "blocked_count": 0,
        "approval_required_count": 1,
        "metadata_kind": "endpoint-management-export",
        "export_id": "eme_stable_1",
        "channel": "stable",
        "provider": "all",
        "providers": ["jamf", "linux"],
        "approval_id": "apr_channel",
        "approval_state": "pending",
        "request_id": "rcp_stable_1",
        "files": ["jamf-policy.json", "linux-fleet-manifest.json"],
        "manifest": {"channel": "stable", "providers": ["jamf", "linux"]},
    }
    client.post("/evidence", json=promotion_metadata)
    client.post("/evidence", json=export_metadata)

    config = client.get("/console/config").json()
    promotions = client.get(
        "/release-channel-promotions",
        params={"channel": "stable", "target_ring": "enterprise", "approval_state": "pending"},
    )
    promotion_detail = client.get("/release-channel-promotions/rcp_stable_1")
    exports = client.get("/endpoint-management-exports", params={"channel": "stable", "provider": "jamf"})
    export_detail = client.get("/endpoint-management-exports/eme_stable_1")
    dashboard = client.get("/endpoint-management-exports/dashboard")

    assert config["endpoints"]["release_channel_promotions"] == "/release-channel-promotions"
    assert config["endpoints"]["endpoint_management_export_dashboard"] == "/endpoint-management-exports/dashboard"
    assert promotions.status_code == 200
    assert promotions.json()["total"] == 1
    assert promotion_detail.status_code == 200
    assert promotion_detail.json()["approval_id"] == "apr_channel"
    assert exports.status_code == 200
    assert exports.json()["items"][0]["export_id"] == "eme_stable_1"
    assert export_detail.status_code == 200
    assert export_detail.json()["providers"] == ["jamf", "linux"]
    assert dashboard.status_code == 200
    assert dashboard.json()["total_exports"] == 1
    assert dashboard.json()["providers"]["jamf"] == 1
    assert dashboard.json()["pending_approval_exports"] == 1


def test_api_reconciles_managed_endpoint_deployment_drift(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    connector_config = tmp_path / "connectors.json"
    connector_config.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra?token=secret"}}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_CONNECTOR_CONFIG", str(connector_config))
    client = TestClient(create_app())
    desired_manifest = {
        "schema_version": "cavra.go-runtime.endpoint-deployment.v1",
        "version": "v0.2.0-rc.1",
        "commit": "abc123",
        "repository": "Huzefaaa2/cavra",
        "deployment_targets": [
            {
                "id": "linux-systemd-amd64-workstation",
                "binary_sha256": "good",
                "management_tool": "Linux endpoint management",
            }
        ],
    }
    linux_inventory = {
        "schema_version": "linux.fleet.inventory.v1",
        "observed_at": "2026-05-19T00:00:00+00:00",
        "hosts": [
            {
                "endpoint_id": "workstation-1",
                "deployment_target": "linux-systemd-amd64-workstation",
                "installed_version": "v0.1.0",
                "binary_sha256": "old",
                "last_seen_at": "2026-05-19T00:00:00+00:00",
            }
        ],
    }

    inventory_response = client.post(
        "/endpoint-inventory/ingest",
        json={"provider": "linux", "inventory": linux_inventory, "channel": "stable"},
    )
    response = client.post(
        "/endpoint-deployment/reconcile",
        json={
            "desired_manifest": desired_manifest,
            "observed_inventory": inventory_response.json()["inventory"],
            "stale_after_hours": 24,
        },
    )
    inventory_history = client.get("/endpoint-inventory-ingestions", params={"provider": "linux"})
    inventory_dashboard = client.get("/endpoint-inventory-ingestions/dashboard")
    freshness_report = client.post(
        "/endpoint-inventory/freshness-report",
        json={"provider": "linux", "channel": "stable", "max_age_hours": 1, "critical_age_hours": 1},
    )
    freshness_history = client.get("/endpoint-inventory-freshness", params={"provider": "linux"})
    freshness_dashboard = client.get("/endpoint-inventory-freshness/dashboard")
    history = client.get("/endpoint-reconciliations", params={"drift_status": "drift_detected"})
    dashboard = client.get("/endpoint-reconciliations/dashboard")
    remediation_request = client.post(
        f"/endpoint-reconciliations/{response.json()['reconciliation_id']}/remediation-request",
        json={"strategy": "rollback", "requested_by": "release-agent"},
    )
    approval_id = remediation_request.json()["approval"]["approval_id"]
    approval = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "endpoint-cab", "reason": "Reviewed endpoint drift remediation"},
    )
    remediation_execution = client.post(
        f"/endpoint-remediations/{remediation_request.json()['request']['request_id']}/execute",
        json={"approval_id": approval_id, "executed_by": "release-agent"},
    )
    remediation_handoff = client.post(
        f"/endpoint-remediations/{remediation_request.json()['request']['request_id']}/handoff",
        json={"providers": ["jira", "private_queue"], "requested_by": "release-agent"},
    )
    handoff_status = client.post(
        f"/endpoint-remediation-handoffs/{remediation_handoff.json()['handoff']['handoff_id']}/status",
        json={
            "provider": "private_queue",
            "status": "completed",
            "external_ref": "queue-job-789",
            "callback_payload": {"result": "ok", "secret": "hidden"},
            "recorded_by": "release-agent",
        },
    )
    remediation_history = client.get("/endpoint-remediations")
    remediation_dashboard = client.get("/endpoint-remediations/dashboard")
    handoff_history = client.get("/endpoint-remediation-handoffs", params={"provider": "private_queue"})
    handoff_dashboard = client.get("/endpoint-remediation-handoffs/dashboard")
    handoff_status_history = client.get("/endpoint-remediation-handoff-statuses", params={"provider": "private_queue"})
    handoff_status_dashboard = client.get("/endpoint-remediation-handoff-statuses/dashboard")
    sla_report = client.post(
        "/endpoint-remediation-sla/report",
        json={"warning_hours": 1, "critical_hours": 1, "generated_by": "release-agent"},
    )
    sla_delivery = client.post(
        f"/endpoint-remediation-sla-reports/{sla_report.json()['report_id']}/deliver",
        json={
            "provider": "webhook",
            "retries": 0,
            "generated_by": "release-agent",
            "routing_policy": {
                "rules": [
                    {
                        "rule_id": "webhook-release-owner",
                        "alert_levels": ["healthy", "warning", "critical"],
                        "providers": ["webhook"],
                        "owner": "release-governance",
                        "acknowledgement_required": True,
                    }
                ]
            },
        },
    )
    sla_delivery_suppressed = client.post(
        f"/endpoint-remediation-sla-reports/{sla_report.json()['report_id']}/deliver",
        json={
            "provider": "webhook",
            "retries": 0,
            "generated_by": "release-agent",
            "routing_policy": {
                "rules": [
                    {
                        "rule_id": "webhook-release-owner",
                        "alert_levels": ["healthy", "warning", "critical"],
                        "providers": ["webhook"],
                        "owner": "release-governance",
                        "acknowledgement_required": True,
                    }
                ]
            },
        },
    )
    sla_ack = client.post(
        f"/endpoint-remediation-sla-reports/{sla_report.json()['report_id']}/acknowledgements",
        json={"provider": "webhook", "acknowledged_by": "release-manager"},
    )
    sla_notification_history = client.get("/endpoint-remediation-sla-notifications")
    sla_notification_dashboard = client.get("/endpoint-remediation-sla-notifications/dashboard")
    sla_escalation_plan = client.post(
        "/endpoint-remediation-sla-notifications/escalation-plan",
        json={
            "generated_by": "release-agent",
            "slo_policy": {
                "default_slo": {"acknowledgement_minutes": 1, "resolution_minutes": 1},
                "ladders": [
                    {
                        "level": "release-governance",
                        "after_minutes": 0,
                        "providers": ["webhook"],
                        "action": "Escalate unresolved SLA notification to release governance.",
                    }
                ],
            },
        },
    )
    sla_escalation_delivery = client.post(
        f"/endpoint-remediation-sla-escalations/{sla_escalation_plan.json()['plan']['plan_id']}/deliver",
        json={"provider": "webhook", "retries": 0, "generated_by": "release-agent"},
    )
    sla_escalation_review = client.post(
        f"/endpoint-remediation-sla-escalations/{sla_escalation_plan.json()['plan']['plan_id']}/reviews",
        json={
            "report_id": sla_report.json()["report_id"],
            "provider": "webhook",
            "owner": "release-governance",
            "reviewed_by": "release-manager",
            "review_state": "escalated",
        },
    )
    sla_escalation_action_history = client.get("/endpoint-remediation-sla-escalation-actions")
    sla_escalation_action_dashboard = client.get("/endpoint-remediation-sla-escalation-actions/dashboard")
    sla_escalation_recurrence_plan = client.post(
        "/endpoint-remediation-sla-escalations/recurrence-plan",
        json={
            "generated_by": "release-agent",
            "recurrence_policy": {
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
            },
        },
    )
    sla_escalation_recurrence_delivery = client.post(
        f"/endpoint-remediation-sla-escalation-recurrences/{sla_escalation_recurrence_plan.json()['plan']['recurrence_plan_id']}/deliver",
        json={"provider": "webhook", "retries": 0, "generated_by": "release-agent"},
    )
    sla_escalation_suppression_audit = client.get(
        f"/endpoint-remediation-sla-escalation-recurrences/{sla_escalation_recurrence_plan.json()['plan']['recurrence_plan_id']}/suppression-audit"
    )
    sla_escalation_recurrence_retry_plan = client.post(
        "/endpoint-remediation-sla-escalation-recurrences/retry-plan",
        json={
            "generated_by": "release-agent",
            "retry_policy": {"max_retry_attempts": 3, "retry_delay_minutes": 1, "backoff_multiplier": 1},
        },
    )
    sla_escalation_owner_digest = client.post(
        f"/endpoint-remediation-sla-escalation-recurrences/{sla_escalation_recurrence_plan.json()['plan']['recurrence_plan_id']}/owner-digest",
        json={
            "retry_plan_id": sla_escalation_recurrence_retry_plan.json()["plan"]["retry_plan_id"],
            "provider": "webhook",
            "retries": 0,
            "generated_by": "release-agent",
        },
    )
    sla_escalation_suppression_trends = client.get(
        "/endpoint-remediation-sla-escalation-recurrences/suppression-trends"
    )
    sla_escalation_recurrence_automation = client.post(
        "/endpoint-remediation-sla-escalation-recurrences/automation-run",
        json={
            "generated_by": "release-agent",
            "dry_run": True,
            "schedule": {"interval_minutes": 30},
            "retry_policy": {"max_retry_attempts": 3, "retry_delay_minutes": 1, "backoff_multiplier": 1},
        },
    )
    sla_escalation_recurrence_automation_history = client.get(
        "/endpoint-remediation-sla-escalation-recurrence-automations"
    )
    sla_escalation_recurrence_automation_dashboard = client.get(
        "/endpoint-remediation-sla-escalation-recurrence-automations/dashboard"
    )
    sla_escalation_recurrence_automation_health = client.get(
        "/endpoint-remediation-sla-escalation-recurrence-automations/health",
        params={"expected_interval_minutes": 30, "stale_metadata_minutes": 120},
    )
    sla_escalation_recurrence_automation_health_alert_delivery = client.post(
        "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/deliver",
        json={
            "provider": "webhook",
            "retries": 0,
            "generated_by": "release-agent",
            "routing_policy": {
                "rules": [
                    {
                        "rule_id": "webhook-recurrence-health",
                        "alert_levels": ["warning", "critical"],
                        "providers": ["webhook"],
                        "owner": "release-governance",
                        "acknowledgement_required": True,
                    }
                ]
            },
        },
    )
    health_alert_plan = sla_escalation_recurrence_automation_health_alert_delivery.json().get("plan", {})
    sla_escalation_recurrence_automation_health_alert_ack = client.post(
        (
            "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/"
            f"{health_alert_plan.get('health_id', 'erslah-missing')}/acknowledgements"
        ),
        json={
            "provider": "webhook",
            "acknowledged_by": "release-manager",
            "plan_id": health_alert_plan.get("plan_id"),
        },
    )
    sla_escalation_recurrence_automation_health_alert_history = client.get(
        "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts"
    )
    sla_escalation_recurrence_automation_health_alert_dashboard = client.get(
        "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/dashboard"
    )
    sla_escalation_recurrence_history = client.get("/endpoint-remediation-sla-escalation-recurrences")
    sla_escalation_recurrence_dashboard = client.get("/endpoint-remediation-sla-escalation-recurrences/dashboard")
    sla_escalation_history = client.get("/endpoint-remediation-sla-escalations", params={"active_only": True})
    sla_escalation_dashboard = client.get("/endpoint-remediation-sla-escalations/dashboard")
    sla_history = client.get("/endpoint-remediation-sla-reports")
    sla_dashboard = client.get("/endpoint-remediation-sla-reports/dashboard")
    automation = client.post(
        f"/endpoint-inventory-ingestions/{inventory_response.json()['inventory_id']}/reconcile",
        json={
            "desired_manifest": desired_manifest,
            "remediation_strategy": "rollback",
            "requested_by": "release-agent",
        },
    )
    automation_history = client.get("/endpoint-reconciliation-automations")
    automation_dashboard = client.get("/endpoint-reconciliation-automations/dashboard")
    config = client.get("/console/config").json()

    assert response.status_code == 200
    assert inventory_response.status_code == 200
    assert inventory_response.json()["metadata"]["metadata_kind"] == "endpoint-inventory-ingestion"
    assert inventory_history.status_code == 200
    assert inventory_history.json()["total"] == 1
    assert inventory_dashboard.status_code == 200
    assert inventory_dashboard.json()["providers"][0]["provider"] == "linux"
    assert freshness_report.status_code == 200
    assert freshness_report.json()["metadata"]["metadata_kind"] == "endpoint-inventory-freshness-report"
    assert freshness_history.status_code == 200
    assert freshness_history.json()["total"] == 1
    assert freshness_dashboard.status_code == 200
    assert freshness_dashboard.json()["report_count"] == 1
    assert response.json()["drift_status"] == "drift_detected"
    assert response.json()["metadata"]["metadata_kind"] == "managed-endpoint-reconciliation"
    assert history.status_code == 200
    assert history.json()["total"] == 1
    assert dashboard.status_code == 200
    assert dashboard.json()["alert_level"] == "critical"
    assert remediation_request.status_code == 200
    assert remediation_request.json()["metadata"]["metadata_kind"] == "endpoint-drift-remediation-request"
    assert remediation_request.json()["request"]["actions"][0]["action_type"] == "rollback_runtime"
    assert approval.status_code == 200
    assert remediation_execution.status_code == 200
    assert remediation_execution.json()["metadata"]["metadata_kind"] == "endpoint-drift-remediation-execution"
    assert remediation_handoff.status_code == 200
    assert remediation_handoff.json()["metadata"]["metadata_kind"] == "endpoint-remediation-handoff"
    assert remediation_handoff.json()["handoff"]["payloads"]["private_queue"]["queue_event"]["status"] == "ready_for_private_connector"
    assert handoff_status.status_code == 200
    assert handoff_status.json()["metadata"]["metadata_kind"] == "endpoint-remediation-handoff-status"
    assert handoff_status.json()["status"]["callback_payload"]["secret"] == "[redacted]"
    assert remediation_history.status_code == 200
    assert remediation_history.json()["total"] == 2
    assert remediation_dashboard.status_code == 200
    assert remediation_dashboard.json()["execution_count"] == 1
    assert handoff_history.status_code == 200
    assert handoff_history.json()["total"] == 1
    assert handoff_dashboard.status_code == 200
    assert handoff_dashboard.json()["provider_count"] == 2
    assert handoff_status_history.status_code == 200
    assert handoff_status_history.json()["total"] == 1
    assert handoff_status_dashboard.status_code == 200
    assert handoff_status_dashboard.json()["completed_count"] == 1
    assert sla_report.status_code == 200
    assert sla_report.json()["metadata"]["metadata_kind"] == "endpoint-remediation-sla-report"
    assert sla_report.json()["report"]["executive_summary"]["tracked_work_item_count"] == 2
    assert sla_delivery.status_code == 200
    assert sla_delivery.json()["metadata"]["connector_delivery_source"] == "endpoint_remediation_sla_notification"
    assert sla_delivery.json()["delivery"]["event_type"] == "cavra.endpoint_remediation_sla.notification"
    assert sla_delivery.json()["plan_metadata"]["metadata_kind"] == "endpoint-remediation-sla-notification-plan"
    assert sla_delivery_suppressed.status_code == 200
    assert sla_delivery_suppressed.json()["delivery"] is None
    assert sla_delivery_suppressed.json()["plan"]["suppressed_providers"][0]["provider"] == "webhook"
    assert sla_ack.status_code == 200
    assert sla_ack.json()["metadata"]["metadata_kind"] == "endpoint-remediation-sla-notification-ack"
    assert sla_notification_history.status_code == 200
    assert sla_notification_history.json()["total"] >= 4
    assert sla_notification_dashboard.status_code == 200
    assert sla_notification_dashboard.json()["suppressed_provider_count"] >= 1
    assert sla_escalation_plan.status_code == 200
    assert sla_escalation_plan.json()["metadata"]["metadata_kind"] == "endpoint-remediation-sla-escalation-plan"
    assert sla_escalation_delivery.status_code == 200
    assert sla_escalation_delivery.json()["metadata"]["connector_delivery_source"] == "endpoint_remediation_sla_escalation_delivery"
    assert sla_escalation_delivery.json()["event"]["event_type"] == "cavra.endpoint_remediation_sla.escalation_delivery"
    assert sla_escalation_review.status_code == 200
    assert sla_escalation_review.json()["metadata"]["metadata_kind"] == "endpoint-remediation-sla-escalation-review"
    assert sla_escalation_action_history.status_code == 200
    assert sla_escalation_action_history.json()["total"] >= 3
    assert sla_escalation_action_dashboard.status_code == 200
    assert sla_escalation_action_dashboard.json()["delivery_count"] >= 1
    assert sla_escalation_recurrence_plan.status_code == 200
    assert (
        sla_escalation_recurrence_plan.json()["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-recurrence-plan"
    )
    assert sla_escalation_recurrence_delivery.status_code == 200
    assert (
        sla_escalation_recurrence_delivery.json()["event"]["event_type"]
        == "cavra.endpoint_remediation_sla.escalation_recurrence_delivery"
    )
    assert sla_escalation_suppression_audit.status_code == 200
    assert (
        sla_escalation_suppression_audit.json()["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-suppression-audit"
    )
    assert sla_escalation_recurrence_retry_plan.status_code == 200
    assert (
        sla_escalation_recurrence_retry_plan.json()["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-recurrence-retry-plan"
    )
    assert sla_escalation_owner_digest.status_code == 200
    assert (
        sla_escalation_owner_digest.json()["digest_metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-owner-digest"
    )
    assert sla_escalation_suppression_trends.status_code == 200
    assert (
        sla_escalation_suppression_trends.json()["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-suppression-trend"
    )
    assert sla_escalation_recurrence_automation.status_code == 200
    assert (
        sla_escalation_recurrence_automation.json()["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-recurrence-automation-run"
    )
    assert sla_escalation_recurrence_automation.json()["run"]["dry_run"] is True
    assert sla_escalation_recurrence_automation_history.status_code == 200
    assert sla_escalation_recurrence_automation_history.json()["total"] >= 1
    assert sla_escalation_recurrence_automation_dashboard.status_code == 200
    assert sla_escalation_recurrence_automation_dashboard.json()["run_count"] >= 1
    assert sla_escalation_recurrence_automation_health.status_code == 200
    assert "missed_run_count" in sla_escalation_recurrence_automation_health.json()
    assert sla_escalation_recurrence_automation_health_alert_delivery.status_code == 200
    assert (
        sla_escalation_recurrence_automation_health_alert_delivery.json()["plan_metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan"
    )
    assert sla_escalation_recurrence_automation_health_alert_ack.status_code == 200
    assert (
        sla_escalation_recurrence_automation_health_alert_ack.json()["metadata"]["metadata_kind"]
        == "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack"
    )
    assert sla_escalation_recurrence_automation_health_alert_history.status_code == 200
    assert sla_escalation_recurrence_automation_health_alert_history.json()["total"] >= 2
    assert sla_escalation_recurrence_automation_health_alert_dashboard.status_code == 200
    assert "outstanding_acknowledgement_count" in sla_escalation_recurrence_automation_health_alert_dashboard.json()
    assert sla_escalation_recurrence_history.status_code == 200
    assert sla_escalation_recurrence_history.json()["total"] >= 1
    assert sla_escalation_recurrence_dashboard.status_code == 200
    assert sla_escalation_recurrence_dashboard.json()["route_count"] >= 1
    assert sla_escalation_history.status_code == 200
    assert sla_escalation_history.json()["total"] >= 1
    assert sla_escalation_dashboard.status_code == 200
    assert sla_escalation_dashboard.json()["active_escalation_count"] >= 1
    assert sla_history.status_code == 200
    assert sla_history.json()["total"] == 1
    assert sla_dashboard.status_code == 200
    assert sla_dashboard.json()["report_count"] == 1
    assert automation.status_code == 200
    assert automation.json()["metadata"]["metadata_kind"] == "endpoint-reconciliation-automation"
    assert automation.json()["approval"]["state"] == "pending"
    assert automation_history.status_code == 200
    assert automation_history.json()["total"] == 1
    assert automation_dashboard.status_code == 200
    assert automation_dashboard.json()["pending_approval_count"] == 1
    assert config["endpoints"]["endpoint_inventory_dashboard"] == "/endpoint-inventory-ingestions/dashboard"
    assert config["endpoints"]["endpoint_inventory_freshness_dashboard"] == "/endpoint-inventory-freshness/dashboard"
    assert config["endpoints"]["endpoint_reconciliation_dashboard"] == "/endpoint-reconciliations/dashboard"
    assert config["endpoints"]["endpoint_reconciliation_automation_dashboard"] == "/endpoint-reconciliation-automations/dashboard"
    assert config["endpoints"]["endpoint_remediation_dashboard"] == "/endpoint-remediations/dashboard"
    assert config["endpoints"]["endpoint_remediation_handoff_dashboard"] == "/endpoint-remediation-handoffs/dashboard"
    assert (
        config["endpoints"]["endpoint_remediation_handoff_status_dashboard"]
        == "/endpoint-remediation-handoff-statuses/dashboard"
    )
    assert config["endpoints"]["endpoint_remediation_sla_dashboard"] == "/endpoint-remediation-sla-reports/dashboard"
    assert config["endpoints"]["endpoint_remediation_sla_deliver"] == "/endpoint-remediation-sla-reports/{report_id}/deliver"
    assert (
        config["endpoints"]["endpoint_remediation_sla_acknowledge"]
        == "/endpoint-remediation-sla-reports/{report_id}/acknowledgements"
    )
    assert config["endpoints"]["endpoint_remediation_sla_notifications"] == "/endpoint-remediation-sla-notifications"
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_plan"]
        == "/endpoint-remediation-sla-notifications/escalation-plan"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_deliver"]
        == "/endpoint-remediation-sla-escalations/{plan_id}/deliver"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_review"]
        == "/endpoint-remediation-sla-escalations/{plan_id}/reviews"
    )
    assert config["endpoints"]["endpoint_remediation_sla_escalations"] == "/endpoint-remediation-sla-escalations"
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_dashboard"]
        == "/endpoint-remediation-sla-escalations/dashboard"
    )
    assert config["endpoints"]["endpoint_remediation_sla_escalation_actions"] == "/endpoint-remediation-sla-escalation-actions"
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_action_dashboard"]
        == "/endpoint-remediation-sla-escalation-actions/dashboard"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_plan"]
        == "/endpoint-remediation-sla-escalations/recurrence-plan"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_deliver"]
        == "/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/deliver"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_suppression_audit"]
        == "/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/suppression-audit"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_retry_plan"]
        == "/endpoint-remediation-sla-escalation-recurrences/retry-plan"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_owner_digest"]
        == "/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/owner-digest"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_suppression_trends"]
        == "/endpoint-remediation-sla-escalation-recurrences/suppression-trends"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_automation"]
        == "/endpoint-remediation-sla-escalation-recurrences/automation-run"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_automations"]
        == "/endpoint-remediation-sla-escalation-recurrence-automations"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_automation_health"]
        == "/endpoint-remediation-sla-escalation-recurrence-automations/health"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_automation_health_alert_deliver"]
        == "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/deliver"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_automation_health_alerts"]
        == "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard"]
        == "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/dashboard"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrences"]
        == "/endpoint-remediation-sla-escalation-recurrences"
    )
    assert (
        config["endpoints"]["endpoint_remediation_sla_escalation_recurrence_dashboard"]
        == "/endpoint-remediation-sla-escalation-recurrences/dashboard"
    )


def test_api_serves_endpoint_management_export_artifacts_with_integrity(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    artifact_root = tmp_path / "artifacts"
    export_dir = artifact_root / "eme_stable_1"
    export_dir.mkdir(parents=True)
    manifest_path = export_dir / "endpoint-management-export-manifest.json"
    summary_path = export_dir / "endpoint-management-export-manifest.md"
    jamf_path = export_dir / "jamf-policy.json"
    linux_path = export_dir / "linux-fleet-manifest.json"
    manifest_payload = {
        "schema_version": "cavra.endpoint-management-export.v1",
        "channel": "stable",
        "providers": ["jamf", "linux"],
        "release": {"version": "v0.2.0-rc.1"},
        "approval": {"approval_id": "apr_channel"},
    }
    manifest_path.write_text(json.dumps(manifest_payload), encoding="utf-8")
    summary_path.write_text("# Endpoint Export\n", encoding="utf-8")
    jamf_path.write_text(json.dumps({"schema_version": "cavra.endpoint-management.jamf.v1"}), encoding="utf-8")
    linux_path.write_text(json.dumps({"schema_version": "cavra.endpoint-management.linux.v1"}), encoding="utf-8")
    (export_dir / "checksums.txt").write_text(
        "\n".join(
            [
                f"{sha256_file(manifest_path)}  endpoint-management-export-manifest.json",
                f"{sha256_file(summary_path)}  endpoint-management-export-manifest.md",
                f"{sha256_file(jamf_path)}  jamf-policy.json",
                f"{sha256_file(linux_path)}  linux-fleet-manifest.json",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_EVIDENCE_ARTIFACT_ROOT", str(artifact_root))
    connector_config = tmp_path / "connectors.json"
    connector_config.write_text(
        json.dumps({"connectors": {"jamf": {"url": "http://127.0.0.1:9/jamf?token=secret"}}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_CONNECTOR_CONFIG", str(connector_config))
    client = TestClient(create_app())
    client.post(
        "/evidence",
        json={
            "session_id": "eme_stable_1",
            "metadata_kind": "endpoint-management-export",
            "export_id": "eme_stable_1",
            "bundle_dir": str(export_dir),
            "channel": "stable",
            "providers": ["jamf", "linux"],
            "files": [
                "endpoint-management-export-manifest.json",
                "endpoint-management-export-manifest.md",
                "jamf-policy.json",
                "linux-fleet-manifest.json",
                "checksums.txt",
            ],
            "manifest": manifest_payload,
        },
    )

    listing = client.get("/endpoint-management-exports/eme_stable_1/artifacts")
    artifact = client.get("/endpoint-management-exports/eme_stable_1/artifacts/jamf-policy.json")
    bundle = client.get("/endpoint-management-exports/eme_stable_1/artifact-bundle")
    rejected = client.get("/endpoint-management-exports/eme_stable_1/artifacts/intune-win32-app.json")
    publish = client.post(
        "/endpoint-management-exports/eme_stable_1/publish",
        json={"provider": "jamf", "retries": 0, "timeout_seconds": 0.1},
    )
    publications = client.get("/endpoint-management-publications", params={"provider": "jamf", "success": "false"})
    publication_dashboard = client.get("/endpoint-management-publications/dashboard")
    jamf_sha256 = sha256_file(jamf_path)
    jamf_path.write_text(json.dumps({"tampered": True}), encoding="utf-8")
    tampered_listing = client.get("/endpoint-management-exports/eme_stable_1/artifacts")
    tampered_download = client.get("/endpoint-management-exports/eme_stable_1/artifacts/jamf-policy.json")

    assert listing.status_code == 200
    assert listing.json()["metadata_kind"] == "endpoint-management-export"
    assert listing.json()["artifact_count"] == 5
    assert listing.json()["endpoint_management_export_integrity"]["status"] == "verified"
    assert listing.json()["download_readiness"]["status"] == "ready"
    assert artifact.status_code == 200
    assert artifact.headers["content-type"].startswith("application/json")
    assert artifact.headers["x-cavra-artifact-kind"] == "jamf-policy"
    assert artifact.headers["x-cavra-artifact-sha256"] == jamf_sha256
    assert artifact.json()["schema_version"] == "cavra.endpoint-management.jamf.v1"
    assert bundle.status_code == 200
    assert bundle.content.startswith(b"PK")
    assert bundle.headers["x-cavra-artifact-count"] == "5"
    assert rejected.status_code == 400
    assert publish.status_code == 200
    assert publish.json()["providers"] == ["jamf"]
    assert publish.json()["delivery"]["deliveries"][0]["request"]["url"].endswith("?REDACTED")
    assert publish.json()["metadata"]["metadata_kind"] == "endpoint-management-publication-delivery"
    assert publications.status_code == 200
    assert publications.json()["total"] == 1
    assert publication_dashboard.status_code == 200
    assert publication_dashboard.json()["providers"][0]["failed"] == 1
    assert tampered_listing.status_code == 200
    assert tampered_listing.json()["endpoint_management_export_integrity"]["status"] == "failed"
    assert tampered_download.status_code == 400
    assert "checksum verification failed" in tampered_download.json()["detail"]


def test_api_console_config_and_cors(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.delenv("CAVRA_ACTIVITY_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    monkeypatch.setenv("CAVRA_ACTIVITY_STORE", str(tmp_path / "activity.json"))
    monkeypatch.setenv("CAVRA_CORS_ORIGINS", "http://127.0.0.1:5173")
    monkeypatch.setenv("CAVRA_PUBLIC_API_BASE_URL", "https://cavra.example")
    client = TestClient(create_app())

    config = client.get("/console/config").json()
    cors = client.options(
        "/evidence",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert config["api_base_url"] == "https://cavra.example"
    assert config["metadata_mode"] == "json"
    assert config["activity_mode"] == "json"
    assert config["endpoints"]["sandbox_metrics"] == "/api/sandbox/metrics"
    assert config["endpoints"]["sandbox_run"] == "/api/sandbox/run"
    assert cors.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


def test_api_sandbox_run_uses_backend_policy_and_persists_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.delenv("CAVRA_ACTIVITY_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    monkeypatch.setenv("CAVRA_ACTIVITY_STORE", str(tmp_path / "activity.json"))
    client = TestClient(create_app())

    scenarios = client.get("/api/sandbox/scenarios")
    response = client.post(
        "/api/sandbox/run",
        json={"scenario": "before-the-agent-acts", "persona": "Auditor", "policy_mode": "Strict regulated repository"},
    )
    payload = response.json()
    run_id = payload["run_id"]
    evidence = client.get(f"/api/sandbox/runs/{run_id}/evidence")
    attestation = client.get(f"/api/sandbox/runs/{run_id}/attestation")
    metadata = client.get(f"/evidence/{run_id}")
    sessions = client.get("/sessions", params={"repository": "sandbox/before-the-agent-acts"})
    decisions = client.get("/decisions", params={"session_id": run_id})
    metrics = client.get("/api/sandbox/metrics")
    replay = client.post(f"/api/sandbox/runs/{run_id}/replay")
    replay_metrics = client.get("/api/sandbox/metrics")
    missing = client.get("/api/sandbox/runs/missing")

    assert scenarios.status_code == 200
    assert scenarios.json()[0]["id"] == "before-the-agent-acts"
    assert response.status_code == 200
    assert payload["source"] == "cavra-api"
    assert payload["policy_mode"] == "strict"
    assert payload["decision_count"] == 7
    assert payload["blocked_count"] >= 3
    assert any(item["download_url"].endswith("/evidence") for item in payload["artifacts"])
    assert evidence.status_code == 200
    assert evidence.json()["run"]["run_id"] == run_id
    assert attestation.status_code == 200
    assert "CAVRA PR Attestation" in attestation.text
    assert metadata.status_code == 200
    assert metadata.json()["session_id"] == run_id
    assert sessions.json()["total"] == 1
    assert decisions.json()["total"] == 7
    assert metrics.status_code == 200
    assert metrics.json()["tracking"] == "none"
    assert metrics.json()["telemetry"] == "disabled"
    assert metrics.json()["total_runs"] == 1
    assert metrics.json()["total_decisions"] == 7
    assert replay.status_code == 200
    assert replay.json()["run_id"] != run_id
    assert replay_metrics.json()["total_runs"] == 2
    assert replay_metrics.json()["total_decisions"] == 14
    assert missing.status_code == 404


def test_api_persists_json_decisions_and_sessions(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_ACTIVITY_DB", raising=False)
    monkeypatch.setenv("CAVRA_ACTIVITY_STORE", str(tmp_path / "activity.json"))
    client = TestClient(create_app())

    decision = client.post(
        "/decisions",
        json={
            "session_id": "api-session",
            "agent_id": "codex-agent",
            "actor": "codex-agent",
            "repository": "payments/api",
            "action_type": "execute_command",
            "target": "terraform apply -auto-approve",
        },
    )
    sessions = client.get("/sessions", params={"repository": "payments/api"})
    blocked = client.get("/decisions", params={"session_id": "api-session", "decision": "block"})
    fetched = client.get(f"/decisions/{decision.json()['decision_id']}")

    assert decision.status_code == 200
    assert decision.json()["decision"] == "block"
    assert sessions.json()["total"] == 1
    assert sessions.json()["items"][0]["blocked_count"] == 1
    assert blocked.json()["total"] == 1
    assert fetched.json()["repository"] == "payments/api"


def test_api_sqlite_activity_store(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_ACTIVITY_STORE", raising=False)
    monkeypatch.setenv("CAVRA_ACTIVITY_DB", str(tmp_path / "activity.db"))
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())

    decision = client.post(
        "/decisions",
        json={
            "session_id": "sqlite-session",
            "agent_id": "claude-code",
            "repository": "platform/repo",
            "action_type": "write_file",
            "target": "iam/admin-role.tf",
        },
    )
    session = client.get("/sessions/sqlite-session")
    listed = client.get("/decisions", params={"agent_id": "claude-code", "severity": "high"})
    config = client.get("/console/config").json()
    sandbox_run = client.post("/api/sandbox/run", json={"scenario": "before-the-agent-acts"})
    sandbox_metrics = client.get("/api/sandbox/metrics").json()

    assert decision.status_code == 200
    assert decision.json()["decision"] == "require_approval"
    assert session.json()["approval_required_count"] == 1
    assert listed.json()["total"] == 1
    assert config["activity_mode"] == "sqlite"
    assert sandbox_run.status_code == 200
    assert sandbox_metrics["total_runs"] == 1
    assert sandbox_metrics["total_decisions"] == 7


def test_api_operations_store_status_and_retention_plan(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_ACTIVITY_STORE", str(tmp_path / "activity.json"))
    client = TestClient(create_app())

    stores = client.get("/operations/stores").json()
    retention = client.get("/operations/retention-plan", params={"retention_days": 365, "legal_hold": True}).json()

    assert stores["total"] == 6
    assert any(item["name"] == "activity" for item in stores["items"])
    assert retention["retention_days"] == 365
    assert retention["legal_hold"] is True


def test_api_repository_inventory_and_policy_rollouts(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_INVENTORY_DB", raising=False)
    monkeypatch.setenv("CAVRA_INVENTORY_STORE", str(tmp_path / "inventory.json"))
    client = TestClient(create_app())

    repository = client.post(
        "/repositories",
        json={
            "repository": "payments/api",
            "owner": "Payments Platform",
            "policy_pack": "cavra-banking",
            "risk_tier": "high",
            "required_checks": ["cavra", "CodeQL"],
        },
    )
    rollout = client.post(
        "/policy-rollouts",
        json={
            "rollout_id": "payments-api-banking",
            "repository": "payments/api",
            "policy_pack": "cavra-banking",
            "state": "active",
            "mode": "strict",
            "coverage_percent": 90,
        },
    )

    assert repository.status_code == 200
    assert rollout.status_code == 200
    assert client.get("/repositories", params={"risk_tier": "high"}).json()["total"] == 1
    assert client.get("/repositories/payments%2Fapi").json()["policy_pack"] == "cavra-banking"
    assert client.get("/policy-rollouts", params={"repository": "payments/api"}).json()["total"] == 1
    assert client.get("/policy-rollouts/payments-api-banking").json()["mode"] == "strict"


def test_api_policy_rollout_detail_includes_context(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_INVENTORY_DB", raising=False)
    monkeypatch.delenv("CAVRA_ACTIVITY_DB", raising=False)
    monkeypatch.delenv("CAVRA_INTEGRATION_DB", raising=False)
    monkeypatch.setenv("CAVRA_INVENTORY_STORE", str(tmp_path / "inventory.json"))
    monkeypatch.setenv("CAVRA_ACTIVITY_STORE", str(tmp_path / "activity.json"))
    monkeypatch.setenv("CAVRA_INTEGRATION_STORE", str(tmp_path / "integrations.json"))
    client = TestClient(create_app())

    client.post("/repositories", json={"repository": "payments/api", "policy_pack": "cavra-ai-agent-baseline"})
    client.post(
        "/policy-rollouts",
        json={
            "rollout_id": "payments-api-baseline",
            "repository": "payments/api",
            "policy_pack": "cavra-ai-agent-baseline",
            "state": "active",
            "mode": "enforce",
            "coverage_percent": 90,
        },
    )
    client.post(
        "/integrations",
        json={"integration_id": "github", "provider": "github", "category": "source_control", "status": "active"},
    )
    client.post(
        "/decisions",
        json={"session_id": "rollout-session", "repository": "payments/api", "policy_pack": "cavra-ai-agent-baseline", "action_type": "execute_command", "target": "terraform plan"},
    )

    detail = client.get("/policy-rollout-details/payments-api-baseline")

    assert detail.status_code == 200
    payload = detail.json()
    assert payload["rollout"]["rollout_id"] == "payments-api-baseline"
    assert payload["repository"]["repository"] == "payments/api"
    assert payload["policy_pack"]["id"] == "cavra-ai-agent-baseline"
    assert payload["activity_summary"]["total"] == 1
    assert payload["integration_summary"]["by_category"]["source_control"] == 1


def test_api_policy_pack_draft_catalog_and_rollout_change(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_INVENTORY_DB", raising=False)
    monkeypatch.setenv("CAVRA_INVENTORY_STORE", str(tmp_path / "inventory.json"))
    client = TestClient(create_app())

    catalog = client.get("/policy-pack-catalog")
    draft = client.post(
        "/policy-packs/draft",
        json={
            "id": "cavra-platform-baseline",
            "title": "Platform Baseline",
            "description": "Platform engineering controls.",
            "version": "2026.05",
            "inherits": "cavra-ai-agent-baseline",
            "commands": {"block": ["terraform apply -auto-approve"]},
        },
    )
    plan = client.post(
        "/policy-rollouts/change-plan",
        json={
            "rollout_id": "payments-platform",
            "repository": "payments/api",
            "policy_pack": "cavra-platform-baseline",
            "mode": "strict",
            "state": "active",
            "coverage_percent": 95,
        },
    )
    applied = client.post(
        "/policy-rollouts/apply-change",
        json={
            "rollout_id": "payments-platform",
            "repository": "payments/api",
            "policy_pack": "cavra-platform-baseline",
            "mode": "strict",
            "state": "active",
            "coverage_percent": 95,
        },
    )

    assert catalog.status_code == 200
    assert catalog.json()["total"] > 0
    assert draft.status_code == 200
    assert draft.json()["valid"] is True
    assert plan.status_code == 200
    assert plan.json()["approval_required"] is True
    assert applied.status_code == 200
    assert applied.json()["rollout"]["rollout_id"] == "payments-platform"
    assert client.get("/policy-rollouts/payments-platform").json()["mode"] == "strict"
    assert client.get("/console/config").json()["endpoints"]["policy_pack_draft"] == "/policy-packs/draft"


def test_api_policy_pack_publish_requires_approved_digest_bound_approval(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_POLICY_DIR", str(tmp_path / "policies"))
    monkeypatch.setenv("CAVRA_POLICY_SIGNING_KEY", "secret")
    client = TestClient(create_app())
    draft = {
        "id": "cavra-platform-baseline",
        "title": "Platform Baseline",
        "description": "Platform engineering controls.",
        "version": "2026.05",
        "commands": {"block": ["terraform apply -auto-approve"]},
    }

    plan = client.post("/policy-packs/publish-plan", json=draft)
    request = client.post("/policy-packs/publish-request", json={"draft": draft, "requested_by": "platform@example.com"})
    approval_id = request.json()["approval"]["approval_id"]
    pending_publish = client.post("/policy-packs/publish", json={"draft": draft, "approval_id": approval_id})
    approved = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "security@example.com", "reason": "approved policy write-back"},
    )
    published = client.post("/policy-packs/publish", json={"draft": draft, "approval_id": approval_id})
    mutated = {**draft, "commands": {"block": ["terraform apply -auto-approve", "kubectl delete namespace"]}}
    rejected = client.post("/policy-packs/publish", json={"draft": mutated, "approval_id": approval_id})
    config = client.get("/console/config").json()

    assert plan.status_code == 200
    assert plan.json()["approval_required"] is True
    assert request.status_code == 200
    assert request.json()["approval"]["state"] == "pending"
    assert pending_publish.status_code == 400
    assert approved.status_code == 200
    assert published.status_code == 200
    assert published.json()["status"] == "published"
    assert (tmp_path / "policies" / "cavra-platform-baseline" / "policy.yaml").exists()
    assert (tmp_path / "policies" / "cavra-platform-baseline" / "policy.yaml.sig.json").exists()
    assert rejected.status_code == 400
    assert "approval does not match policy draft digest" in rejected.json()["detail"]
    assert config["endpoints"]["policy_pack_publish"] == "/policy-packs/publish"


def test_api_deployment_production_readiness(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_CORS_ORIGINS", "https://console.example")
    monkeypatch.setenv("CAVRA_EVIDENCE_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    client = TestClient(create_app())

    response = client.get("/deployment/production-readiness")
    config = client.get("/console/config").json()

    assert response.status_code == 200
    assert response.json()["schema_version"] == "cavra.deployment.production_readiness.v1"
    assert any(item["id"] == "cors_restricted" for item in response.json()["checks"])
    assert response.json()["go_backend_pilot"]["status"] == "disabled"
    assert response.json()["go_backend_deployment"]["status"] == "not_configured"
    assert response.json()["go_backend_promotion"]["status"] == "not_requested"
    assert response.json()["go_backend_rollback"]["status"] == "not_requested"
    assert response.json()["go_backend_rollback_rehearsal"]["status"] == "not_requested"
    assert response.json()["go_backend_rollback_drill_history"]["status"] == "not_requested"
    assert response.json()["go_backend_rollback_drill_schedule"]["status"] == "not_requested"
    assert config["endpoints"]["deployment_readiness"] == "/deployment/production-readiness"
    assert config["endpoints"]["go_backend_readiness"] == "/runtime/go-pilot/readiness"
    assert config["endpoints"]["go_deployment_readiness"] == "/runtime/go-pilot/deployment-readiness"
    assert config["endpoints"]["go_promotion_readiness"] == "/runtime/go-pilot/promotion-readiness"
    assert config["endpoints"]["go_rollback_readiness"] == "/runtime/go-pilot/rollback-readiness"
    assert config["endpoints"]["go_rollback_rehearsal"] == "/runtime/go-pilot/rollback-rehearsal"
    assert config["endpoints"]["go_rollback_drills"] == "/runtime/go-pilot/rollback-drills"
    assert config["endpoints"]["go_rollback_drill_schedule"] == "/runtime/go-pilot/rollback-drill-schedule"
    assert config["endpoints"]["go_rollback_drill_notifications"] == "/runtime/go-pilot/rollback-drill-notifications/deliver"
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledge"]
        == "/runtime/go-pilot/rollback-drill-notifications/{schedule_id}/acknowledgements"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_bulk_acknowledge"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_retry_plan"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_worker"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_workers"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-runs"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_worker_dashboard"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-dashboard"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_deliver"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alerts"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_dashboard"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alert-dashboard"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_retry_acknowledge"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plans/{retry_plan_id}/acknowledgements"
    )
    assert (
        config["endpoints"][
            "go_rollback_drill_notification_acknowledgement_audit_delivery_retry_execution_approval_plan"
        ]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan"
    )
    assert (
        config["endpoints"][
            "go_rollback_drill_notification_acknowledgement_audit_delivery_retry_execution_approval_decide"
        ]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plans/{approval_plan_id}/decisions"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_connector_recovery_playbook"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_connector_recovery_close"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbooks/{playbook_id}/closures"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_retry_recovery_report"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_plan"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_deliver"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/deliver"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report"]
        == "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report"
    )
    assert config["endpoints"]["go_rollback_drill_notification_history"] == "/runtime/go-pilot/rollback-drill-notifications"
    assert (
        config["endpoints"]["go_rollback_drill_notification_dashboard"]
        == "/runtime/go-pilot/rollback-drill-notifications/dashboard"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_escalation_plan"]
        == "/runtime/go-pilot/rollback-drill-notifications/escalation-plan"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_routes"]
        == "/runtime/go-pilot/rollback-drill-notifications/routes"
    )
    assert (
        config["endpoints"]["go_rollback_drill_notification_suppression_trends"]
        == "/runtime/go-pilot/rollback-drill-notifications/suppression-trends"
    )


def test_api_go_backend_pilot_readiness_and_evaluation(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "shadow")
    monkeypatch.setenv("CAVRA_GO_RUNTIME_PATH", str(tmp_path / "missing-runtime"))
    monkeypatch.setenv("CAVRA_GO_RUNTIME_POLICY", str(tmp_path / "missing-policy.json"))
    client = TestClient(create_app())

    readiness = client.get("/runtime/go-pilot/readiness")
    evaluation = client.post(
        "/runtime/go-pilot/evaluate",
        json={"action_type": "execute_command", "target": "terraform plan"},
    )

    assert readiness.status_code == 200
    assert readiness.json()["status"] == "needs_attention"
    assert evaluation.status_code == 200
    assert evaluation.json()["selected_backend"] == "python"
    assert evaluation.json()["fallback_used"] is True
    assert evaluation.json()["effective_decision"]["decision"] == "allow"


def test_api_go_backend_deployment_readiness(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "shadow")
    monkeypatch.setenv("CAVRA_GO_RUNTIME_PACKAGE_DIR", str(tmp_path / "missing-package"))
    client = TestClient(create_app())

    readiness = client.get("/runtime/go-pilot/deployment-readiness")
    production = client.get("/deployment/production-readiness")

    assert readiness.status_code == 200
    assert readiness.json()["schema_version"] == "cavra.go-backend-pilot.deployment-readiness.v1"
    assert readiness.json()["status"] == "needs_attention"
    assert production.json()["go_backend_deployment"]["status"] == "needs_attention"
    assert any(item["id"] == "go_backend_deployment_paths" for item in production.json()["checks"])


def test_api_go_backend_promotion_readiness(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "promoted")
    monkeypatch.setenv("CAVRA_GO_PROMOTION_EVIDENCE", str(tmp_path / "missing-promotion.json"))
    client = TestClient(create_app())

    readiness = client.get("/runtime/go-pilot/promotion-readiness")

    assert readiness.status_code == 200
    assert readiness.json()["schema_version"] == "cavra.go-backend-pilot.promotion-readiness.v1"
    assert readiness.json()["status"] == "needs_attention"


def test_api_go_backend_rollback_readiness(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "promoted")
    monkeypatch.setenv("CAVRA_GO_ROLLBACK_PLAN", str(tmp_path / "missing-rollback.json"))
    client = TestClient(create_app())

    readiness = client.get("/runtime/go-pilot/rollback-readiness")

    assert readiness.status_code == 200
    assert readiness.json()["schema_version"] == "cavra.go-backend-pilot.rollback-readiness.v1"
    assert readiness.json()["status"] == "needs_attention"


def test_api_go_backend_rollback_rehearsal(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "promoted")
    monkeypatch.setenv("CAVRA_GO_ROLLBACK_REHEARSAL_EVIDENCE", str(tmp_path / "missing-rehearsal.json"))
    client = TestClient(create_app())

    rehearsal = client.get("/runtime/go-pilot/rollback-rehearsal")

    assert rehearsal.status_code == 200
    assert rehearsal.json()["schema_version"] == "cavra.go-backend-pilot.rollback-rehearsal.v1"
    assert rehearsal.json()["status"] == "needs_attention"


def test_api_go_backend_rollback_drills(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "promoted")
    monkeypatch.setenv("CAVRA_GO_ROLLBACK_DRILL_HISTORY", str(tmp_path / "missing-drills.json"))
    client = TestClient(create_app())

    drills = client.get("/runtime/go-pilot/rollback-drills")

    assert drills.status_code == 200
    assert drills.json()["schema_version"] == "cavra.go-backend-pilot.rollback-drill-history.v1"
    assert drills.json()["status"] == "needs_attention"


def test_api_go_backend_rollback_drill_schedule(monkeypatch, tmp_path) -> None:
    history = tmp_path / "drills.json"
    history.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-rollback-drill-history.v1",
                "drills": [
                    {
                        "drill_id": "drill_api",
                        "executed_at": "2099-01-01T00:00:00+00:00",
                        "target_mode": "disabled",
                        "status": "pass",
                        "fallback_verified": True,
                        "recovery_minutes": 5,
                        "max_recovery_minutes": 15,
                        "runbook_ref": "docs/go-backend-rollback-drill-scheduling.md",
                        "evidence_refs": ["go-rollback-drill://api"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    schedule = tmp_path / "schedule.json"
    schedule.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-rollback-drill-schedule.v1",
                "schedule_id": "go_backend_api_schedule",
                "status": "active",
                "interval_days": 30,
                "next_due_at": "2099-02-01T00:00:00+00:00",
                "owners": ["release-governance"],
                "notification_providers": ["webhook"],
                "runbook_ref": "docs/go-backend-rollback-drill-scheduling.md",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "promoted")
    monkeypatch.setenv("CAVRA_GO_ROLLBACK_DRILL_HISTORY", str(history))
    monkeypatch.setenv("CAVRA_GO_ROLLBACK_DRILL_SCHEDULE", str(schedule))
    client = TestClient(create_app())

    response = client.get("/runtime/go-pilot/rollback-drill-schedule")

    assert response.status_code == 200
    assert response.json()["schema_version"] == "cavra.go-backend-pilot.rollback-drill-schedule.v1"
    assert response.json()["status"] == "ready"
    assert response.json()["schedule"]["notification_providers"] == ["webhook"]


def test_api_go_backend_rollback_drill_notification_delivery(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "evidence.json"))
    connector_config = tmp_path / "connectors.json"
    connector_config.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra"}}}),
        encoding="utf-8",
    )
    schedule = tmp_path / "schedule.json"
    schedule.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-rollback-drill-schedule.v1",
                "schedule_id": "go_backend_stale_schedule",
                "status": "active",
                "interval_days": 30,
                "next_due_at": "2000-01-01T00:00:00+00:00",
                "owners": ["release-governance"],
                "notification_providers": ["webhook"],
                "runbook_ref": "docs/go-backend-rollback-drill-scheduling.md",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_CONNECTOR_CONFIG", str(connector_config))
    monkeypatch.setenv("CAVRA_GO_BACKEND_MODE", "promoted")
    monkeypatch.setenv("CAVRA_GO_ROLLBACK_DRILL_SCHEDULE", str(schedule))
    client = TestClient(create_app())

    response = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/deliver",
        json={
            "provider": "webhook",
            "retries": 0,
            "timeout_seconds": 0.1,
            "routing_policy": {
                "owner_routes": {
                    "release-governance": {
                        "providers": ["webhook"],
                        "acknowledgement_minutes": 30,
                    }
                }
            },
        },
    )
    dashboard_before = client.get("/runtime/go-pilot/rollback-drill-notifications/dashboard")
    escalation = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/escalation-plan",
        json={"policy": {"acknowledgement_minutes": 60}, "generated_by": "test"},
    )
    acknowledgement = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/go_backend_stale_schedule/acknowledgements",
        json={
            "provider": "webhook",
            "acknowledged_by": "release-manager",
            "plan_id": response.json()["plan"]["plan_id"],
        },
    )
    bulk_acknowledgement = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk",
        json={
            "acknowledgement_state": "resolved",
            "acknowledged_by": "release-manager",
            "external_ref": "CHG-456",
            "routes": [
                {
                    "schedule_id": "go_backend_stale_schedule",
                    "provider": "webhook",
                    "plan_id": response.json()["plan"]["plan_id"],
                }
            ],
        },
    )
    acknowledgement_audit = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package",
        json={"owner": "release-governance", "provider": "webhook", "generated_by": "release-manager"},
    )
    acknowledgement_audit_delivery = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery",
        json={
            "owner": "release-governance",
            "provider": "webhook",
            "delivery_provider": "webhook",
            "generated_by": "release-manager",
            "cadence": "hourly",
            "schedule_ref": "release-governance-hourly",
            "retries": 0,
            "timeout_seconds": 0.1,
        },
    )
    audit_delivery_retry_plan = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan",
        json={
            "generated_by": "release-manager",
            "retry_policy": {"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
        },
    )
    audit_delivery_worker = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run",
        json={
            "generated_by": "release-manager",
            "dry_run": True,
            "max_retry_deliveries": 2,
            "retry_policy": {"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            "schedule": {"interval_minutes": 30, "cadence": "every_30_minutes"},
        },
    )
    audit_delivery_worker_history = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-runs",
        params={"dry_run": True},
    )
    audit_delivery_worker_dashboard = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-dashboard"
    )
    audit_delivery_worker_health = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health",
        params={"expected_interval_minutes": 30, "stale_metadata_minutes": 120},
    )
    audit_delivery_worker_health_alert_delivery = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver",
        json={
            "generated_by": "release-manager",
            "provider": "webhook",
            "force": True,
            "retries": 0,
            "timeout_seconds": 0.1,
            "expected_interval_minutes": 30,
            "stale_metadata_minutes": 120,
        },
    )
    health_alert_plan = audit_delivery_worker_health_alert_delivery.json().get("plan", {})
    audit_delivery_worker_health_alert_ack = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/"
        f"worker-health-alerts/{health_alert_plan.get('health_id', 'gordackhealth-missing')}/acknowledgements",
        json={
            "provider": "webhook",
            "acknowledged_by": "release-manager",
            "acknowledgement_state": "acknowledged",
            "plan_id": health_alert_plan.get("plan_id"),
        },
    )
    audit_delivery_worker_health_alert_history = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts"
    )
    audit_delivery_worker_health_alert_dashboard = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alert-dashboard"
    )
    first_retry_decision = audit_delivery_retry_plan.json()["plan"]["retry_decisions"][0]
    audit_delivery_retry_ack = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/"
        f"retry-plans/{audit_delivery_retry_plan.json()['plan']['retry_plan_id']}/acknowledgements",
        json={
            "provider": first_retry_decision["provider"],
            "acknowledged_by": "release-manager",
            "acknowledgement_state": "accepted",
            "delivery_id": first_retry_decision["delivery_id"],
            "audit_id": first_retry_decision["audit_id"],
        },
    )
    audit_delivery_retry_execution_approval_plan = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan",
        json={"generated_by": "release-manager", "approval_policy": {"require_retry_ack": True}},
    )
    first_approval_decision = audit_delivery_retry_execution_approval_plan.json()["plan"]["approval_decisions"][0]
    audit_delivery_retry_execution_approval_decision = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/"
        f"retry-execution-approval-plans/{audit_delivery_retry_execution_approval_plan.json()['plan']['approval_plan_id']}/decisions",
        json={
            "provider": first_approval_decision["provider"],
            "decided_by": "release-manager",
            "approval_state": "approved",
            "retry_plan_id": first_approval_decision["retry_plan_id"],
            "delivery_id": first_approval_decision["delivery_id"],
            "audit_id": first_approval_decision["audit_id"],
            "external_ref": "CHG-789",
        },
    )
    audit_delivery_live_retry_worker = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run",
        json={
            "generated_by": "release-manager",
            "execute": True,
            "max_retry_deliveries": 2,
            "retry_policy": {"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            "schedule": {"interval_minutes": 30, "cadence": "manual_retry"},
            "retries": 0,
            "timeout_seconds": 0.1,
        },
    )
    audit_delivery_connector_recovery_playbook = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook",
        json={"generated_by": "release-manager", "min_failure_count": 1, "lookback_hours": 24},
    )
    audit_delivery_connector_recovery_closure = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/"
        f"connector-recovery-playbooks/{audit_delivery_connector_recovery_playbook.json()['playbook']['playbook_id']}/closures",
        json={
            "provider": "webhook",
            "closed_by": "release-manager",
            "closure_state": "resolved",
            "external_ref": "INC-123",
            "verification_refs": [
                audit_delivery_live_retry_worker.json()["retry_results"][0]["execution_record"]["execution_id"]
            ],
        },
    )
    audit_delivery_retry_recovery_report = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report",
        params={"recovery_slo_minutes": 120, "generated_by": "release-manager"},
    )
    audit_delivery_recovery_escalation_plan = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan",
        json={"recovery_slo_minutes": 120, "generated_by": "release-manager"},
    )
    audit_delivery_recovery_escalation_delivery = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/"
        f"recovery-escalations/{audit_delivery_recovery_escalation_plan.json()['plan']['plan_id']}/deliver",
        json={
            "generated_by": "release-manager",
            "provider": "webhook",
            "retries": 0,
            "timeout_seconds": 0.1,
        },
    )
    audit_delivery_recovery_executive_report = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report",
        params={"recovery_slo_minutes": 120, "generated_by": "release-manager"},
    )
    history = client.get("/runtime/go-pilot/rollback-drill-notifications")
    audit_delivery_history = client.get(
        "/runtime/go-pilot/rollback-drill-notifications",
        params={"connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit"},
    )
    failed_audit_delivery_history = client.get(
        "/runtime/go-pilot/rollback-drill-notifications",
        params={
            "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit",
            "delivery_success": False,
        },
    )
    cadence_history = client.get(
        "/runtime/go-pilot/rollback-drill-notifications",
        params={"cadence": "hourly"},
    )
    audit_id_history = client.get(
        "/runtime/go-pilot/rollback-drill-notifications",
        params={"audit_id": acknowledgement_audit_delivery.json()["audit_package"]["audit_id"]},
    )
    routes = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/routes",
        params={"owner": "release-governance", "provider": "webhook"},
    )
    suppression_trend = client.get(
        "/runtime/go-pilot/rollback-drill-notifications/suppression-trends",
        params={"owner": "release-governance"},
    )
    dashboard_after = client.get("/runtime/go-pilot/rollback-drill-notifications/dashboard")

    assert response.status_code == 200
    assert response.json()["plan"]["alert_level"] == "critical"
    assert response.json()["plan"]["selected_providers"] == ["webhook"]
    assert response.json()["plan"]["route_decisions"][0]["acknowledgement_minutes"] == 30
    assert response.json()["metadata"]["connector_delivery_source"] == "go_backend_rollback_drill_notification"
    assert response.json()["plan_metadata"]["metadata_kind"] == "go-backend-rollback-drill-notification-plan"
    assert dashboard_before.status_code == 200
    assert dashboard_before.json()["outstanding_acknowledgement_count"] == 1
    assert escalation.status_code == 200
    assert escalation.json()["metadata"]["metadata_kind"] == "go-backend-rollback-drill-notification-escalation-plan"
    assert acknowledgement.status_code == 200
    assert acknowledgement.json()["metadata"]["metadata_kind"] == "go-backend-rollback-drill-notification-ack"
    assert bulk_acknowledgement.status_code == 200
    assert bulk_acknowledgement.json()["acknowledgement_count"] == 1
    assert bulk_acknowledgement.json()["acknowledgements"][0]["acknowledgement_state"] == "resolved"
    assert acknowledgement_audit.status_code == 200
    assert (
        acknowledgement_audit.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-package"
    )
    assert acknowledgement_audit.json()["audit_package"]["route_count"] == 1
    assert acknowledgement_audit.json()["audit_package"]["resolved_count"] == 1
    assert acknowledgement_audit_delivery.status_code == 200
    assert acknowledgement_audit_delivery.json()["audit_package"]["route_count"] == 1
    assert acknowledgement_audit_delivery.json()["delivery_plan"]["selected_providers"] == ["webhook"]
    assert acknowledgement_audit_delivery.json()["delivery_plan"]["cadence"] == "hourly"
    assert (
        acknowledgement_audit_delivery.json()["plan_metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-plan"
    )
    assert (
        acknowledgement_audit_delivery.json()["metadata"]["connector_delivery_source"]
        == "go_backend_rollback_drill_acknowledgement_audit"
    )
    assert audit_delivery_retry_plan.status_code == 200
    assert (
        audit_delivery_retry_plan.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan"
    )
    assert audit_delivery_retry_plan.json()["plan"]["decision_count"] == 1
    assert audit_delivery_worker.status_code == 200
    assert (
        audit_delivery_worker.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run"
    )
    assert audit_delivery_worker.json()["run"]["dry_run"] is True
    assert audit_delivery_worker_history.status_code == 200
    assert audit_delivery_worker_history.json()["total"] == 1
    assert audit_delivery_worker_dashboard.status_code == 200
    assert audit_delivery_worker_dashboard.json()["run_count"] == 1
    assert audit_delivery_worker_dashboard.json()["dry_run_count"] == 1
    assert audit_delivery_worker_health.status_code == 200
    assert audit_delivery_worker_health.json()["connector_delivery_failure_count"] == 1
    assert audit_delivery_worker_health_alert_delivery.status_code == 200
    assert (
        audit_delivery_worker_health_alert_delivery.json()["plan_metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan"
    )
    assert audit_delivery_worker_health_alert_ack.status_code == 200
    assert (
        audit_delivery_worker_health_alert_ack.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-ack"
    )
    assert audit_delivery_worker_health_alert_history.status_code == 200
    assert audit_delivery_worker_health_alert_history.json()["total"] >= 2
    assert audit_delivery_worker_health_alert_dashboard.status_code == 200
    assert audit_delivery_worker_health_alert_dashboard.json()["acknowledgement_count"] == 1
    assert audit_delivery_retry_ack.status_code == 200
    assert (
        audit_delivery_retry_ack.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-ack"
    )
    assert audit_delivery_retry_execution_approval_plan.status_code == 200
    assert (
        audit_delivery_retry_execution_approval_plan.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-plan"
    )
    assert audit_delivery_retry_execution_approval_plan.json()["plan"]["approval_required_count"] == 1
    assert audit_delivery_retry_execution_approval_decision.status_code == 200
    assert (
        audit_delivery_retry_execution_approval_decision.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision"
    )
    assert audit_delivery_live_retry_worker.status_code == 200
    assert audit_delivery_live_retry_worker.json()["run"]["dry_run"] is False
    assert (
        audit_delivery_live_retry_worker.json()["retry_results"][0]["execution_metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record"
    )
    assert audit_delivery_connector_recovery_playbook.status_code == 200
    assert (
        audit_delivery_connector_recovery_playbook.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook"
    )
    assert audit_delivery_connector_recovery_playbook.json()["playbook"]["provider_count"] == 1
    assert audit_delivery_connector_recovery_closure.status_code == 200
    assert (
        audit_delivery_connector_recovery_closure.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-closure"
    )
    assert audit_delivery_connector_recovery_closure.json()["closure"]["closure_state"] == "resolved"
    assert audit_delivery_retry_recovery_report.status_code == 200
    assert (
        audit_delivery_retry_recovery_report.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-recovery-report"
    )
    assert audit_delivery_retry_recovery_report.json()["report"]["execution_count"] == 1
    assert audit_delivery_retry_recovery_report.json()["report"]["execution_failed_count"] == 1
    assert audit_delivery_retry_recovery_report.json()["report"]["recovery_closed_count"] == 1
    assert audit_delivery_retry_recovery_report.json()["report"]["recovery_slo_breached_count"] == 0
    assert audit_delivery_retry_recovery_report.json()["report"]["closure_trends"][0]["resolved_count"] == 1
    assert audit_delivery_recovery_escalation_plan.status_code == 200
    assert (
        audit_delivery_recovery_escalation_plan.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan"
    )
    assert audit_delivery_recovery_escalation_plan.json()["plan"]["failed_execution_count"] == 1
    assert audit_delivery_recovery_escalation_plan.json()["plan"]["escalation_count"] == 1
    assert audit_delivery_recovery_escalation_delivery.status_code == 200
    assert (
        audit_delivery_recovery_escalation_delivery.json()["metadata"]["connector_delivery_source"]
        == "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation"
    )
    assert audit_delivery_recovery_executive_report.status_code == 200
    assert (
        audit_delivery_recovery_executive_report.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report"
    )
    assert audit_delivery_recovery_executive_report.json()["report"]["executive_summary"]["failed_execution_count"] == 1
    assert history.status_code == 200
    assert history.json()["total"] >= 21
    assert audit_delivery_history.status_code == 200
    assert audit_delivery_history.json()["total"] >= 3
    assert failed_audit_delivery_history.status_code == 200
    assert failed_audit_delivery_history.json()["total"] >= 2
    assert cadence_history.status_code == 200
    assert cadence_history.json()["total"] == 1
    assert cadence_history.json()["items"][0]["metadata_kind"] == "go-backend-rollback-drill-acknowledgement-audit-delivery-plan"
    assert audit_id_history.status_code == 200
    assert audit_id_history.json()["total"] >= 3
    assert routes.status_code == 200
    assert routes.json()["total"] == 1
    assert routes.json()["items"][0]["action"] == "deliver"
    assert suppression_trend.status_code == 200
    assert (
        suppression_trend.json()["metadata"]["metadata_kind"]
        == "go-backend-rollback-drill-routing-suppression-trend"
    )
    assert dashboard_after.status_code == 200
    assert dashboard_after.json()["outstanding_acknowledgement_count"] == 0
    assert dashboard_after.json()["acknowledgement_audit_delivery_plan_count"] >= 3
    assert dashboard_after.json()["acknowledgement_audit_delivery_count"] >= 2
    assert dashboard_after.json()["failed_acknowledgement_audit_delivery_count"] >= 2
    assert dashboard_after.json()["acknowledgement_audit_delivery_health"] == "critical"
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_plan_count"] >= 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_ack_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_execution_approval_plan_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_execution_approval_decision_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_execution_approved_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_execution_record_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_execution_failed_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_connector_recovery_playbook_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_connector_recovery_closure_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_connector_recovery_closed_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_retry_recovery_report_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_recovery_escalation_plan_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_recovery_escalation_route_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_recovery_executive_report_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_worker_run_count"] == 2
    assert dashboard_after.json()["acknowledgement_audit_delivery_worker_health_alert_count"] == 1
    assert dashboard_after.json()["acknowledgement_audit_delivery_worker_health_alert_ack_count"] == 1


def test_api_integration_delivery_uses_connector_config(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_INTEGRATION_DB", raising=False)
    monkeypatch.setenv("CAVRA_INTEGRATION_STORE", str(tmp_path / "integrations.json"))
    config_path = tmp_path / "connectors.json"
    config_path.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra?token=secret"}}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_CONNECTOR_CONFIG", str(config_path))
    client = TestClient(create_app())
    client.post(
        "/integrations",
        json={
            "integration_id": "webhook",
            "provider": "webhook",
            "category": "siem",
            "status": "active",
            "health_status": "healthy",
        },
    )

    response = client.post(
        "/integrations/webhook/deliver",
        json={
            "event": {
                "event_type": "cavra.evidence_bundle",
                "session_id": "api-session",
                "decision_count": 1,
                "blocked_count": 1,
                "approval_required_count": 0,
                "max_severity": "high",
            },
            "retries": 0,
            "timeout_seconds": 0.1,
        },
    )
    config = client.get("/console/config").json()

    assert response.status_code == 200
    assert response.json()["schema_version"] == "cavra.connector.delivery.v1"
    assert response.json()["deliveries"][0]["provider"] == "webhook"
    assert response.json()["deliveries"][0]["request"]["url"].endswith("?REDACTED")
    assert config["connector_delivery"] == "configured"
    assert config["endpoints"]["integration_deliver"] == "/integrations/{integration_id}/deliver"


def test_api_sqlite_inventory_store(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_INVENTORY_STORE", raising=False)
    monkeypatch.setenv("CAVRA_INVENTORY_DB", str(tmp_path / "inventory.db"))
    client = TestClient(create_app())

    created = client.post(
        "/repositories",
        json={"repository": "platform/repo", "owner": "Platform", "policy_pack": "cavra-ai-agent-baseline"},
    )
    rollout = client.post(
        "/policy-rollouts",
        json={"repository": "platform/repo", "policy_pack": "cavra-ai-agent-baseline", "state": "planned", "mode": "enforce"},
    )
    config = client.get("/console/config").json()

    assert created.status_code == 200
    assert rollout.status_code == 200
    assert client.get("/repositories", params={"owner": "Platform"}).json()["total"] == 1
    assert client.get("/policy-rollouts", params={"state": "planned"}).json()["total"] == 1
    assert config["inventory_mode"] == "sqlite"


def test_api_integrations_inventory(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_INTEGRATION_DB", raising=False)
    monkeypatch.setenv("CAVRA_INTEGRATION_STORE", str(tmp_path / "integrations.json"))
    client = TestClient(create_app())

    created = client.post(
        "/integrations",
        json={
            "integration_id": "github-enterprise",
            "provider": "github",
            "name": "GitHub Enterprise",
            "category": "source_control",
            "status": "active",
            "health_status": "healthy",
            "owner": "Developer Platform",
            "environment": "production",
            "capabilities": ["required_check", "pull_request"],
        },
    )

    assert created.status_code == 200
    assert client.get("/integrations", params={"category": "source_control"}).json()["total"] == 1
    assert client.get("/integrations/github-enterprise").json()["provider"] == "github"


def test_api_sqlite_integrations_inventory(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_INTEGRATION_STORE", raising=False)
    monkeypatch.setenv("CAVRA_INTEGRATION_DB", str(tmp_path / "integrations.db"))
    client = TestClient(create_app())

    created = client.post(
        "/integrations",
        json={
            "integration_id": "splunk-soc",
            "provider": "splunk",
            "category": "siem",
            "status": "configured",
            "health_status": "not_checked",
            "owner": "SOC",
        },
    )
    config = client.get("/console/config").json()

    assert created.status_code == 200
    assert client.get("/integrations", params={"owner": "SOC"}).json()["total"] == 1
    assert config["integration_mode"] == "sqlite"


def test_api_console_security_boundary_reports_oidc_rbac(monkeypatch, tmp_path) -> None:
    oidc = tmp_path / "oidc.json"
    rbac = tmp_path / "rbac.json"
    oidc.write_text('{"issuer":"https://issuer.example","audience":"cavra","jwks":{"keys":[]}}', encoding="utf-8")
    rbac.write_text('{"approval_rbac":{"group_mappings":{"platform":"Platform Security"}}}', encoding="utf-8")
    monkeypatch.setenv("CAVRA_APPROVAL_OIDC_CONFIG", str(oidc))
    monkeypatch.setenv("CAVRA_APPROVAL_RBAC_FILE", str(rbac))
    monkeypatch.setenv("CAVRA_CORS_ORIGINS", "https://console.example")
    client = TestClient(create_app())

    boundary = client.get("/console/security-boundary").json()
    config = client.get("/console/config").json()

    assert boundary["mode"] == "oidc_rbac_ready"
    assert boundary["oidc"]["configured"] is True
    assert boundary["rbac"]["configured"] is True
    assert boundary["cors"]["origins"] == ["https://console.example"]
    assert config["endpoints"]["console_security_boundary"] == "/console/security-boundary"


def test_api_registry_agents_and_mcp_trust(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_REGISTRY_DB", raising=False)
    monkeypatch.setenv("CAVRA_REGISTRY_STORE", str(tmp_path / "registry.json"))
    client = TestClient(create_app())

    agent = client.post(
        "/agents",
        json={"agent_id": "codex-agent", "vendor": "OpenAI", "capabilities": ["code_edit"], "owner": "Platform AI"},
    )
    mcp = client.post(
        "/mcp/servers",
        json={
            "server_id": "github-mcp",
            "trust_tier": "approved",
            "approval_state": "approved",
            "capabilities": ["repository"],
            "allowed_tools": ["create_pull_request"],
        },
    )
    trust = client.get("/mcp/trust", params={"server": "github-mcp", "tool": "create_pull_request", "capability": "repository"})
    decision = client.post(
        "/decisions",
        json={"action_type": "mcp_tool_call", "server": "github-mcp", "tool": "create_pull_request", "capability": "repository"},
    )
    config = client.get("/console/config").json()

    assert agent.status_code == 200
    assert client.get("/agents").json()["total"] == 1
    assert mcp.status_code == 200
    assert client.get("/mcp/servers").json()["total"] == 1
    assert trust.json()["decision"] == "allow"
    assert decision.json()["rule_id"] == "mcp.registry.allow"
    assert config["registry_store"].endswith("registry.json")


def test_api_sqlite_registry_and_catalogs(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_REGISTRY_STORE", raising=False)
    monkeypatch.setenv("CAVRA_REGISTRY_DB", str(tmp_path / "registry.db"))
    client = TestClient(create_app())

    agent = client.post(
        "/agents",
        json={"agent_id": "claude-code", "vendor": "Anthropic", "capabilities": ["mcp_tool_call"], "owner": "AI Platform"},
    )
    mcp = client.post(
        "/mcp/servers",
        json={
            "server_id": "filesystem-mcp",
            "trust_tier": "approved",
            "approval_state": "approved",
            "capabilities": ["filesystem"],
            "allowed_tools": ["read_file"],
        },
    )
    profiles = client.get("/agents/profiles")
    classification = client.get("/mcp/tool-classifications", params={"capability": "filesystem"})
    config = client.get("/console/config").json()

    assert agent.status_code == 200
    assert mcp.status_code == 200
    assert client.get("/agents", params={"owner": "AI Platform"}).json()["total"] == 1
    assert client.get("/mcp/servers", params={"capability": "filesystem"}).json()["total"] == 1
    assert {item["profile_id"] for item in profiles.json()["items"]} >= {"claude-code", "codex"}
    assert classification.json()["risk_tier"] == "high"
    assert config["registry_mode"] == "sqlite"


def test_api_approval_lifecycle(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post(
        "/approvals",
        json={"decision": decision, "requested_by": "developer"},
    )
    approval_id = created.json()["approval_id"]
    approved = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "platform-security", "reason": "Scoped IAM change reviewed.", "external_ref": "CHG-22"},
    )
    listed = client.get("/approvals", params={"state": "approved"})

    assert created.status_code == 200
    assert created.json()["state"] == "pending"
    assert approved.status_code == 200
    assert approved.json()["state"] == "approved"
    assert listed.json()["total"] == 1


def test_api_approval_sqlite_store(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_APPROVAL_STORE", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_DB", str(tmp_path / "approvals.db"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post("/approvals", json={"decision": decision, "requested_by": "developer"})
    config = client.get("/console/config").json()

    assert created.status_code == 200
    assert created.json()["state"] == "pending"
    assert client.get("/approvals", params={"state": "pending"}).json()["total"] == 1
    assert config["approval_mode"] == "sqlite"


def test_api_approval_uses_repository_routing_file(monkeypatch, tmp_path) -> None:
    routing = tmp_path / "routing.json"
    routing.write_text(
        '{"approval_routing":[{"rule_id_prefix":"filesystem.write","target_contains":"iam/","approver_group":"Cloud IAM Owners"}]}',
        encoding="utf-8",
    )
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_ROUTING_FILE", str(routing))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post("/approvals", json={"decision": decision, "requested_by": "developer"})

    assert created.status_code == 200
    assert created.json()["approver_group"] == "Cloud IAM Owners"


def test_api_approval_actor_claims_enforce_group(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    rejected = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "dev@example.com", "reason": "Not authorized.", "actor_claims": {"email": "dev@example.com", "groups": ["Developers"]}},
    )
    accepted = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "iam@example.com", "reason": "Authorized.", "actor_claims": {"email": "iam@example.com", "groups": ["IAM"]}},
    )

    assert rejected.status_code == 400
    assert accepted.status_code == 200
    assert accepted.json()["state"] == "approved"


def test_api_approval_actor_token_enforces_oidc_and_repository_rbac(monkeypatch, tmp_path) -> None:
    token, jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-approvals",
            "sub": "user-123",
            "email": "owner@example.com",
            "groups": ["github-team:payments-owners"],
            "repository": "payments/api",
            "exp": int(time.time()) + 300,
        }
    )
    oidc_config = tmp_path / "oidc.json"
    rbac_file = tmp_path / "rbac.json"
    oidc_config.write_text(
        json.dumps({"issuer": "https://issuer.example", "audience": "cavra-approvals", "jwks": jwks}),
        encoding="utf-8",
    )
    rbac_file.write_text(
        json.dumps(
            {
                "approval_rbac": {
                    "group_mappings": {"github-team:payments-owners": "Payments Owners"},
                    "repository_permissions": [
                        {
                            "repository": "payments/api",
                            "approver_group": "IAM",
                            "groups": ["Payments Owners"],
                            "actions": ["approved"],
                        }
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_OIDC_CONFIG", str(oidc_config))
    monkeypatch.setenv("CAVRA_APPROVAL_RBAC_FILE", str(rbac_file))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    decision["repository"] = "payments/api"
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    accepted = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "owner@example.com", "reason": "OIDC repository owner.", "actor_token": token},
    )
    config = client.get("/console/config").json()

    assert accepted.status_code == 200
    assert accepted.json()["state"] == "approved"
    assert config["approval_oidc"] == "configured"
    assert config["approval_rbac"] == "configured"


def test_api_console_session_and_authorization_header_enforce_rbac(monkeypatch, tmp_path) -> None:
    token, jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-console",
            "sub": "user-123",
            "email": "owner@example.com",
            "groups": ["github-team:payments-owners"],
            "repository": "payments/api",
            "exp": int(time.time()) + 300,
        }
    )
    oidc_config = tmp_path / "oidc.json"
    rbac_file = tmp_path / "rbac.json"
    oidc_config.write_text(
        json.dumps({"issuer": "https://issuer.example", "audience": "cavra-console", "jwks": jwks}),
        encoding="utf-8",
    )
    rbac_file.write_text(
        json.dumps(
            {
                "approval_rbac": {
                    "group_mappings": {"github-team:payments-owners": "Payments Owners"},
                    "repository_permissions": [
                        {
                            "repository": "payments/api",
                            "approver_group": "IAM",
                            "groups": ["Payments Owners"],
                            "actions": ["approved", "denied"],
                        }
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_OIDC_CONFIG", str(oidc_config))
    monkeypatch.setenv("CAVRA_APPROVAL_RBAC_FILE", str(rbac_file))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    decision["repository"] = "payments/api"
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    unauthenticated = client.get("/console/session")
    authenticated = client.get("/console/session", headers={"authorization": f"Bearer {token}"})
    rejected = client.post(f"/approvals/{approval_id}/approve", json={"reason": "Missing actor context."})
    accepted = client.post(
        f"/approvals/{approval_id}/approve",
        headers={"authorization": f"Bearer {token}"},
        json={"reason": "Repository owner via console session."},
    )

    assert unauthenticated.status_code == 200
    assert unauthenticated.json()["mode"] == "auth_required"
    assert authenticated.status_code == 200
    assert authenticated.json()["authenticated"] is True
    assert authenticated.json()["actor"]["actor"] == "owner@example.com"
    assert authenticated.json()["repository_permissions"][0]["repository"] == "payments/api"
    assert rejected.status_code == 401
    assert accepted.status_code == 200
    assert accepted.json()["decided_by"] == "owner@example.com"


def test_api_go_drill_acknowledgement_requires_authenticated_console_actor(monkeypatch, tmp_path) -> None:
    token, jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-console",
            "sub": "release-user",
            "email": "release@example.com",
            "groups": ["Release Governance"],
            "exp": int(time.time()) + 300,
        }
    )
    oidc_config = tmp_path / "oidc.json"
    oidc_config.write_text(
        json.dumps({"issuer": "https://issuer.example", "audience": "cavra-console", "jwks": jwks}),
        encoding="utf-8",
    )
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_OIDC_CONFIG", str(oidc_config))
    client = TestClient(create_app())

    unauthenticated = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/go_backend_stale_schedule/acknowledgements",
        json={"provider": "slack", "acknowledged_by": "spoofed-user"},
    )
    authenticated = client.post(
        "/runtime/go-pilot/rollback-drill-notifications/go_backend_stale_schedule/acknowledgements",
        headers={"authorization": f"Bearer {token}"},
        json={"provider": "slack", "acknowledgement_state": "resolved"},
    )
    session = client.get("/console/session", headers={"authorization": f"Bearer {token}"})

    assert unauthenticated.status_code == 401
    assert authenticated.status_code == 200
    assert authenticated.json()["acknowledgement"]["acknowledged_by"] == "release@example.com"
    assert authenticated.json()["acknowledgement"]["acknowledgement_state"] == "resolved"
    assert authenticated.json()["actor"]["actor"] == "release@example.com"
    assert session.json()["permissions"]["acknowledge_drill_notifications"] is True


def test_api_console_break_glass_requires_authorized_oidc_actor(monkeypatch, tmp_path) -> None:
    cab_token, jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-console",
            "sub": "cab-user",
            "email": "cab@example.com",
            "groups": ["Change Advisory Board"],
            "exp": int(time.time()) + 300,
        }
    )
    dev_token, _unused_jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-console",
            "sub": "dev-user",
            "email": "dev@example.com",
            "groups": ["Developers"],
            "exp": int(time.time()) + 300,
        }
    )
    oidc_config = tmp_path / "oidc.json"
    rbac_file = tmp_path / "rbac.json"
    oidc_config.write_text(
        json.dumps({"issuer": "https://issuer.example", "audience": "cavra-console", "jwks": jwks}),
        encoding="utf-8",
    )
    rbac_file.write_text('{"approval_rbac":{"group_mappings":{}}}', encoding="utf-8")
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_OIDC_CONFIG", str(oidc_config))
    monkeypatch.setenv("CAVRA_APPROVAL_RBAC_FILE", str(rbac_file))
    client = TestClient(create_app())
    payload = {
        "decision": {
            "decision_id": "dec_break_glass",
            "session_id": "console-session",
            "action_type": "execute_command",
            "target": "terraform apply",
            "rule_id": "commands.block",
            "decision": "block",
            "severity": "critical",
        },
        "reason": "Emergency production recovery.",
    }

    missing = client.post("/approvals/break-glass", json=payload)
    forbidden = client.post("/approvals/break-glass", headers={"authorization": f"Bearer {dev_token}"}, json=payload)
    accepted = client.post("/approvals/break-glass", headers={"authorization": f"Bearer {cab_token}"}, json=payload)

    assert missing.status_code == 401
    assert forbidden.status_code == 401
    assert accepted.status_code == 200
    assert accepted.json()["requested_by"] == "cab@example.com"
    assert accepted.json()["state"] == "break_glass"


def test_api_approval_actor_token_rejects_without_oidc_config(monkeypatch, tmp_path) -> None:
    token, _jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-approvals",
            "sub": "user-123",
            "groups": ["IAM"],
            "exp": int(time.time()) + 300,
        }
    )
    monkeypatch.delenv("CAVRA_APPROVAL_OIDC_CONFIG", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    rejected = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "owner@example.com", "reason": "Needs OIDC config.", "actor_token": token},
    )

    assert rejected.status_code == 400


def test_api_approval_delivers_with_configured_provider(monkeypatch, tmp_path) -> None:
    provider_config = tmp_path / "providers.json"
    provider_config.write_text(
        '{"approval_providers":{"webhook":{"url":"https://approval.example/hook"}}}',
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_PROVIDER_CONFIG", str(provider_config))
    calls = []

    def fake_deliver(approval, config, *, provider, retries, timeout_seconds):
        calls.append((approval, config, provider, retries, timeout_seconds))
        return {
            "schema_version": "cavra.approval.delivery.v1",
            "approval_id": approval["approval_id"],
            "success": True,
            "deliveries": [{"provider": provider, "success": True}],
        }

    monkeypatch.setattr("cavra.api.deliver_provider_requests", fake_deliver)
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    delivered = client.post(f"/approvals/{approval_id}/deliver", json={"provider": "webhook", "retries": 1, "timeout_seconds": 3})
    config = client.get("/console/config").json()

    assert delivered.status_code == 200
    assert delivered.json()["success"] is True
    assert calls[0][2:] == ("webhook", 1, 3.0)
    assert config["approval_provider_delivery"] == "configured"


def test_api_approval_delivery_requires_provider_config(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_APPROVAL_PROVIDER_CONFIG", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    delivered = client.post(f"/approvals/{approval_id}/deliver", json={"provider": "webhook"})

    assert delivered.status_code == 400


def test_api_approval_accepts_raw_decision_payload(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post("/approvals", json=decision)

    assert created.status_code == 200
    assert created.json()["decision_id"] == decision["decision_id"]


def test_api_break_glass_requires_reason(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    rejected = client.post("/approvals/break-glass", json={"decision": decision, "actor": "incident-commander"})
    accepted = client.post(
        "/approvals/break-glass",
        json={
            "decision": decision,
            "actor": "incident-commander",
            "reason": "Production recovery for active incident.",
            "external_ref": "INC-9",
        },
    )

    assert rejected.status_code == 400
    assert accepted.status_code == 200
    assert accepted.json()["state"] == "break_glass"
    assert accepted.json()["external_ref"] == "INC-9"
