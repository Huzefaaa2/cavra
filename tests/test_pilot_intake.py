import json

from fastapi.testclient import TestClient

from cavra.api import create_app
from cavra.pilot_intake import PilotIntakeStore, build_pilot_readiness, normalize_pilot_intake


def _pilot_payload() -> dict:
    return {
        "schema_version": "cavra.final_closeout_pilot_intake.v1",
        "intake_id": "pilot-demo",
        "generated_for": "customer-owned-private-record",
        "pilot_objective": "Scope a production pilot after final closeout trial.",
        "repositories": [
            {
                "repository": "example/release-service",
                "owner": "release-platform",
                "protected_branches": ["main"],
                "required_checks": ["cavra-required-check"],
            }
        ],
        "agents": [{"agent": "codex", "identity": "transparent-ai-agent"}],
        "ci_cd": {"platform": "github-actions", "required_check": "cavra-required-check", "failure_behavior": "block"},
        "connectors": [{"provider": "webhook", "status": "tested"}],
        "identity_and_rbac": {
            "identity_provider": "entra-id",
            "release_manager_group": "release-managers",
            "security_reviewer_group": "security-reviewers",
        },
        "retention": {"retention_days": 365, "archive_destination": "customer-owned-archive"},
        "enterprise_or_saas_handoff": {
            "preferred_deployment": "saas",
            "commercial_owner": "account-owner",
            "target_pilot_start": "2026-06-15",
        },
        "success_criteria": ["CAVRA required check runs on pilot repository."],
    }


def test_normalize_pilot_intake_builds_readiness() -> None:
    record = normalize_pilot_intake(_pilot_payload())

    assert record["schema_version"] == "cavra.pilot_intake.record.v1"
    assert record["intake_id"] == "pilot-demo"
    assert record["readiness"]["overall_status"] == "ready"
    assert record["readiness"]["ready_count"] == 6
    assert record["storage_boundary"]["sensitive_material_rejected"] is True


def test_pilot_readiness_flags_missing_handoff() -> None:
    payload = _pilot_payload()
    payload["enterprise_or_saas_handoff"]["commercial_owner"] = "to-be-confirmed"

    readiness = build_pilot_readiness(normalize_pilot_intake(payload))

    assert readiness["overall_status"] == "needs_input"
    assert any(
        item["area"] == "enterprise_saas_handoff" and item["status"] == "needs_input"
        for item in readiness["areas"]
    )


def test_pilot_intake_rejects_sensitive_material() -> None:
    payload = _pilot_payload()
    payload["connectors"][0]["token"] = "ghp_123456789012345678901234567890123456"

    try:
        normalize_pilot_intake(payload)
    except ValueError as exc:
        assert "sensitive field" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected sensitive pilot intake payload to be rejected")


def test_pilot_intake_store_persists_records(tmp_path) -> None:
    store = PilotIntakeStore(tmp_path / "pilot-intakes.json")

    record = store.upsert(_pilot_payload())
    listing = store.list(repository="example/release-service")
    saved = json.loads((tmp_path / "pilot-intakes.json").read_text(encoding="utf-8"))

    assert record["intake_id"] == "pilot-demo"
    assert listing["total"] == 1
    assert store.get("pilot-demo")["readiness"]["overall_status"] == "ready"
    assert saved["schema_version"] == "cavra.pilot_intake.store.v1"


def test_api_persists_pilot_intake(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_PILOT_INTAKE_STORE", str(tmp_path / "pilot-intakes.json"))
    client = TestClient(create_app())

    created = client.post("/pilot-intakes", json=_pilot_payload())
    listing = client.get("/pilot-intakes", params={"overall_status": "ready"})
    readiness = client.get("/pilot-intakes/pilot-demo/readiness")
    config = client.get("/console/config")

    assert created.status_code == 200
    assert created.json()["readiness"]["overall_status"] == "ready"
    assert listing.json()["total"] == 1
    assert readiness.json()["ready_count"] == 6
    assert config.json()["endpoints"]["pilot_intakes"] == "/pilot-intakes"
