from fastapi.testclient import TestClient

from cavra.api import create_app


def test_api_persists_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())

    response = client.post("/evidence", json={"session_id": "api-session", "decision_count": 2})

    assert response.status_code == 200
    assert response.json()["session_id"] == "api-session"
    assert client.get("/evidence").json()[0]["session_id"] == "api-session"
    assert client.get("/evidence/api-session").json()["decision_count"] == 2
