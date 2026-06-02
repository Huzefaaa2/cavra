import json
from pathlib import Path

from fastapi.testclient import TestClient

from cavra.api import create_app
from cavra.pilot_intake import (
    PilotIntakeStore,
    build_pilot_readiness,
    build_private_persistence_handoff_plan,
    normalize_pilot_intake,
)


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


def test_normalize_trial_to_pilot_template_builds_readiness() -> None:
    payload = json.loads(
        Path("examples/demos/trial-to-pilot-intake/trial-to-pilot-intake-template.json").read_text(encoding="utf-8")
    )

    record = normalize_pilot_intake(payload)

    assert record["schema_version"] == "cavra.pilot_intake.record.v1"
    assert record["source_schema_version"] == "cavra.trial_to_pilot_intake.v1"
    assert record["intake_id"] == "trial-to-pilot-demo"
    assert record["readiness"]["area_count"] == 6
    assert record["storage_boundary"]["private_records"] == "store customer pilot responses in self-hosted Enterprise or SaaS storage"


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


def test_private_persistence_handoff_plan_is_public_safe() -> None:
    record = normalize_pilot_intake(_pilot_payload())

    plan = build_private_persistence_handoff_plan(
        record,
        tenant_id="tenant-demo",
        providers=["saas_tenant", "security_review", "itsm"],
        requested_by="sales-engineering",
    )

    assert plan["schema_version"] == "cavra.pilot_intake.private_handoff_plan.v1"
    assert plan["tenant_id"] == "tenant-demo"
    assert plan["private_implementation_required"] is True
    assert plan["community_boundary"]["contains_connector_credentials"] is False
    assert plan["tenant_persistence_contract"]["tenant_scope_required"] is True
    assert plan["authorization_contract"]["authenticated_updates_required"] is True
    assert plan["encrypted_storage_contract"]["required"] is True
    assert {item["provider"] for item in plan["handoff_tasks"]} == {"itsm", "saas_tenant", "security_review"}
    assert all(item["mutation_allowed_in_community"] is False for item in plan["handoff_tasks"])


def test_api_persists_pilot_intake(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_PILOT_INTAKE_STORE", str(tmp_path / "pilot-intakes.json"))
    client = TestClient(create_app())

    created = client.post("/pilot-intakes", json=_pilot_payload())
    listing = client.get("/pilot-intakes", params={"overall_status": "ready"})
    readiness = client.get("/pilot-intakes/pilot-demo/readiness")
    handoff = client.post(
        "/pilot-intakes/pilot-demo/private-handoff-plan",
        json={"tenant_id": "tenant-demo", "providers": ["saas_tenant", "customer_success"]},
    )
    config = client.get("/console/config")

    assert created.status_code == 200
    assert created.json()["readiness"]["overall_status"] == "ready"
    assert listing.json()["total"] == 1
    assert readiness.json()["ready_count"] == 6
    assert handoff.status_code == 200
    assert handoff.json()["tenant_id"] == "tenant-demo"
    assert handoff.json()["handoff_tasks"][0]["private_connector_required"] is True
    assert config.json()["endpoints"]["pilot_intakes"] == "/pilot-intakes"
    assert (
        config.json()["endpoints"]["pilot_intake_private_handoff_plan"]
        == "/pilot-intakes/{intake_id}/private-handoff-plan"
    )


def test_api_rejects_invalid_private_handoff_provider(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_PILOT_INTAKE_STORE", str(tmp_path / "pilot-intakes.json"))
    client = TestClient(create_app())
    client.post("/pilot-intakes", json=_pilot_payload())

    response = client.post(
        "/pilot-intakes/pilot-demo/private-handoff-plan",
        json={"tenant_id": "tenant-demo", "providers": ["unknown"]},
    )

    assert response.status_code == 400
    assert "unsupported handoff task provider" in response.json()["detail"]
