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
