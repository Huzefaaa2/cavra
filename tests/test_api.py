from pathlib import Path

from fastapi.testclient import TestClient

from cavra.api import create_app
from cavra.evidence import create_evidence_bundle
from cavra.runtime import RuntimeGuard


def _decisions() -> list[dict[str, object]]:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    return [
        guard.evaluate_file_access(Path(".env"), "read").to_dict(),
        guard.evaluate_command("terraform plan").to_dict(),
    ]


def test_api_persists_evidence_metadata(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())

    response = client.post("/evidence", json={"session_id": "api-session", "decision_count": 2})

    assert response.status_code == 200
    assert response.json()["session_id"] == "api-session"
    assert client.get("/evidence").json()[0]["session_id"] == "api-session"
    assert client.get("/evidence/api-session").json()["decision_count"] == 2


def test_api_indexes_evidence_bundle(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    bundle_dir = tmp_path / "bundle"
    create_evidence_bundle(_decisions(), bundle_dir, session_id="api-bundle")
    client = TestClient(create_app())

    response = client.post("/evidence/index-bundle", json={"bundle_dir": str(bundle_dir)})

    assert response.status_code == 200
    assert response.json()["session_id"] == "api-bundle"
    assert client.get("/evidence/api-bundle").json()["decision_count"] == 2
