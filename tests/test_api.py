from fastapi.testclient import TestClient

from cavra.api import create_app


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


def test_api_searches_sqlite_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_DB", str(tmp_path / "metadata.db"))
    client = TestClient(create_app())
    client.post("/evidence", json={"session_id": "blocked-session", "signer": "security", "blocked_count": 2})
    client.post("/evidence", json={"session_id": "clean-session", "signer": "docs", "blocked_count": 0})

    response = client.get("/evidence", params={"signer": "security", "min_blocked": 1, "limit": 10})

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["session_id"] == "blocked-session"


def test_api_console_config_and_cors(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
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
    assert cors.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


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
