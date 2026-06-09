from pathlib import Path
import json

import jsonschema

from cavra.activity import ActivityStore
from cavra.aispm import (
    build_aispm_dashboard_contract,
    build_aispm_posture,
    build_aispm_trace_replay_packet,
    build_sample_aispm_dashboard,
)


def _decision(
    *,
    decision_id: str,
    session_id: str,
    agent_id: str,
    decision: str,
    severity: str,
    action_type: str = "execute_command",
    target: str = "terraform apply",
    rule_id: str = "iac.production-change",
) -> dict[str, object]:
    return {
        "decision_id": decision_id,
        "session_id": session_id,
        "agent_id": agent_id,
        "actor": agent_id,
        "repository": "payments/api",
        "action_type": action_type,
        "target": target,
        "requested_operation": target,
        "policy_pack": "cloud-iam-prod",
        "policy_id": "cloud-iam-prod",
        "rule_id": rule_id,
        "decision": decision,
        "severity": severity,
        "reason": "test decision",
        "evidence_refs": [f"signed://evidence/{decision_id}"],
        "timestamp": "2026-06-09T00:00:00+00:00",
    }


def test_aispm_contract_keeps_enterprise_controls_locked() -> None:
    contract = build_aispm_dashboard_contract()

    assert contract["schema_version"] == "cavra.aispm.contract.v1"
    assert contract["community_boundary"]["status"] == "available"
    assert contract["enterprise_boundary"]["status"] == "requires_cavra_enterprise"
    assert "kill switch and runtime overrides" in contract["enterprise_boundary"]["capabilities"]


def test_aispm_posture_rolls_up_activity_store_decisions(tmp_path: Path) -> None:
    store = ActivityStore(tmp_path / "activity.json")
    store.upsert_decision(
        _decision(
            decision_id="dec-block-secret",
            session_id="session-1",
            agent_id="codex-agent",
            decision="block",
            severity="critical",
            action_type="read_file",
            target=".env.production",
            rule_id="secrets.block-sensitive-read",
        )
    )
    store.upsert_decision(
        _decision(
            decision_id="dec-approval-iac",
            session_id="session-1",
            agent_id="codex-agent",
            decision="require_approval",
            severity="high",
        )
    )
    store.upsert_session({"session_id": "session-1", "state": "completed"})

    posture = build_aispm_posture(store)

    assert posture["schema_version"] == "cavra.aispm.dashboard.v1"
    assert posture["edition"] == "community"
    assert posture["data_provenance"] == "local_activity_store"
    assert posture["overview"]["blocked_actions"] == 1
    assert posture["overview"]["approval_required_actions"] == 1
    assert posture["overview"]["risk_findings"] == 2
    assert posture["overview"]["evidence_confidence"] == "signed_evidence"
    assert posture["agents"][0]["agent_id"] == "codex-agent"
    assert posture["agents"][0]["drift_status"] == "review_required"
    assert {item["risk_classification"] for item in posture["findings"]} == {
        "credential_or_sensitive_data_exposure",
        "infrastructure_change_risk",
    }
    coverage = {item["surface_id"]: item for item in posture["control_coverage"]}
    assert coverage["sensitive_data"]["coverage_status"] == "enforced"
    assert coverage["infrastructure_iac"]["coverage_status"] == "approval_gated"
    assert coverage["mcp_tools"]["coverage_status"] == "not_observed_locally"
    assert [item["decision"] for item in posture["near_misses"]] == ["require_approval"]
    assert posture["near_misses"][0]["operator_signal"] == "approval_prevented_unreviewed_execution"
    assert posture["control_plane"]["kill_switch"] == "requires_cavra_enterprise"


def test_aispm_sample_dashboard_matches_packaged_schema() -> None:
    dashboard_schema = Path("src/cavra/schemas/aispm-dashboard.schema.json")
    sample = build_sample_aispm_dashboard()

    assert dashboard_schema.is_file()
    jsonschema.validate(sample, schema=json.loads(dashboard_schema.read_text(encoding="utf-8")))


def test_aispm_trace_replay_packet_redacts_sensitive_targets(tmp_path: Path) -> None:
    store = ActivityStore(tmp_path / "activity.json")
    store.upsert_decision(
        {
            **_decision(
                decision_id="dec-approval-iac",
                session_id="session-1",
                agent_id="codex-agent",
                decision="require_approval",
                severity="high",
            ),
            "timestamp": "2026-06-09T00:01:00+00:00",
        }
    )
    store.upsert_decision(
        {
            **_decision(
                decision_id="dec-block-secret",
                session_id="session-1",
                agent_id="codex-agent",
                decision="block",
                severity="critical",
                action_type="read_file",
                target=".env.production",
                rule_id="secrets.block-sensitive-read",
            ),
            "timestamp": "2026-06-09T00:00:00+00:00",
        }
    )
    store.upsert_session(
        {
            "session_id": "session-1",
            "agent_id": "codex-agent",
            "repository": "payments/api",
            "state": "completed",
            "started_at": "2026-06-09T00:00:00+00:00",
            "updated_at": "2026-06-09T00:01:00+00:00",
        }
    )

    packet = build_aispm_trace_replay_packet(store, "session-1")

    assert packet is not None
    assert packet["schema_version"] == "cavra.aispm.trace_replay.v1"
    assert packet["edition"] == "community"
    assert packet["summary"]["blocked_actions"] == 1
    assert packet["summary"]["approval_required_actions"] == 1
    assert packet["summary"]["critical_or_high_steps"] == 2
    assert packet["summary"]["evidence_confidence"] == "signed_evidence"
    assert [step["decision_id"] for step in packet["steps"]] == ["dec-block-secret", "dec-approval-iac"]
    assert packet["steps"][0]["target_summary"] == "sensitive target redacted"
    assert packet["steps"][0]["target_redacted"] is True
    assert packet["steps"][1]["target_summary"] == "terraform apply"
    assert packet["redaction"]["prompt_capture"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"
    assert packet["evidence_refs"] == [
        "signed://evidence/dec-approval-iac",
        "signed://evidence/dec-block-secret",
    ]


def test_aispm_trace_replay_sample_matches_packaged_schema() -> None:
    replay_schema = Path("src/cavra/schemas/aispm-trace-replay.schema.json")
    sample = Path("examples/aispm/community-trace-replay-sample.json")

    assert replay_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(replay_schema.read_text(encoding="utf-8")),
    )
