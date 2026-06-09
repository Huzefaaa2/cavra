from pathlib import Path
import json

import jsonschema

from cavra.activity import ActivityStore
from cavra.aispm import (
    build_aispm_approval_lineage,
    build_aispm_behavior_fingerprints,
    build_aispm_dashboard_contract,
    build_aispm_intent_action_drift,
    build_aispm_policy_context_gaps,
    build_aispm_posture,
    build_aispm_pre_action_risk_forecasts,
    build_aispm_trace_replay_packet,
    build_sample_aispm_dashboard,
)
from cavra.approvals import ApprovalStore


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
    assert posture["behavior_fingerprints"][0]["agent_id"] == "codex-agent"
    assert posture["behavior_fingerprints"][0]["drift_status"] == "review_required"
    assert "blocked_action" in posture["behavior_fingerprints"][0]["risk_signals"]
    assert "sensitive_data_access" in posture["behavior_fingerprints"][0]["risk_signals"]
    assert posture["policy_context_gaps"][0]["gap_status"] == "requires_context_review"
    assert "environment_tier" in posture["policy_context_gaps"][0]["missing_context"]
    assert posture["pre_action_risk_forecasts"][0]["forecast_status"] == "block_recommended"
    assert posture["pre_action_risk_forecasts"][0]["projected_blast_radius"] == "secret_scope"
    assert posture["pre_action_risk_forecasts"][1]["forecast_status"] == "approval_recommended"
    assert posture["intent_action_drift"][0]["drift_status"] == "unknown_intent"
    assert "missing_declared_intent" in posture["intent_action_drift"][0]["drift_signals"]
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


def test_aispm_behavior_fingerprints_track_public_safe_drift(tmp_path: Path) -> None:
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
    store.upsert_session(
        {
            "session_id": "session-1",
            "agent_id": "codex-agent",
            "repository": "payments/api",
            "state": "completed",
            "updated_at": "2026-06-09T00:02:00+00:00",
        }
    )

    packet = build_aispm_behavior_fingerprints(store)

    assert packet["schema_version"] == "cavra.aispm.behavior_fingerprints.v1"
    assert packet["summary"]["review_required"] == 1
    assert packet["summary"]["evidence_confidence"] == "signed_evidence"
    assert packet["items"][0]["agent_id"] == "codex-agent"
    assert packet["items"][0]["drift_status"] == "review_required"
    assert packet["items"][0]["drift_score"] > 50
    assert "approval_gate" in packet["items"][0]["risk_signals"]
    assert packet["redaction"]["private_behavior_baselines"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_policy_context_gaps_detect_missing_business_context(tmp_path: Path) -> None:
    class _DecisionStore:
        def list_decisions(self, **_: object) -> dict[str, object]:
            return {
                "items": [
                    _decision(
                        decision_id="dec-context-gap",
                        session_id="session-1",
                        agent_id="codex-agent",
                        decision="require_approval",
                        severity="high",
                        action_type="execute_command",
                        target="terraform apply",
                    ),
                    {
                        **_decision(
                            decision_id="dec-context-complete",
                            session_id="session-2",
                            agent_id="codex-agent",
                            decision="allow",
                            severity="low",
                            action_type="mcp_tool_call",
                            target="filesystem.read",
                            rule_id="mcp.registered-tool",
                        ),
                        "context": {
                            "environment_tier": "development",
                            "system_criticality": "low",
                            "tool_owner": "platform",
                            "tool_trust_tier": "approved",
                            "business_justification": "Read generated docs.",
                        },
                    },
                ]
            }

    store = _DecisionStore()

    packet = build_aispm_policy_context_gaps(store)

    assert packet["schema_version"] == "cavra.aispm.policy_context_gaps.v1"
    assert packet["summary"]["decisions_with_gaps"] == 1
    assert packet["summary"]["requires_context_review"] == 1
    assert packet["items"][0]["decision_id"] == "dec-context-gap"
    assert packet["items"][0]["control_surface"] == "infrastructure_iac"
    assert "change_window" in packet["items"][0]["missing_context"]
    assert "approval_route" in packet["items"][0]["missing_context"]
    assert packet["redaction"]["private_cmdb_records"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_policy_context_gaps_from_activity_store_metadata(tmp_path: Path) -> None:
    store = ActivityStore(tmp_path / "activity.json")
    store.upsert_decision(
        _decision(
            decision_id="dec-context-gap",
            session_id="session-1",
            agent_id="codex-agent",
            decision="require_approval",
            severity="high",
            action_type="execute_command",
            target="terraform apply",
        )
    )

    packet = build_aispm_policy_context_gaps(store)

    assert packet["schema_version"] == "cavra.aispm.policy_context_gaps.v1"
    assert packet["summary"]["decisions_with_gaps"] == 1
    assert packet["summary"]["requires_context_review"] == 1
    assert packet["items"][0]["decision_id"] == "dec-context-gap"


def test_aispm_pre_action_risk_forecasts_project_public_safe_impact(tmp_path: Path) -> None:
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
            action_type="execute_command",
            target="terraform apply",
        )
    )

    packet = build_aispm_pre_action_risk_forecasts(store)

    assert packet["schema_version"] == "cavra.aispm.pre_action_risk_forecasts.v1"
    assert packet["summary"]["total_forecasts"] == 2
    assert packet["summary"]["block_recommended"] == 1
    assert packet["summary"]["approval_recommended"] == 1
    assert packet["summary"]["evidence_confidence"] == "signed_evidence"
    assert packet["items"][0]["forecast_status"] == "block_recommended"
    assert packet["items"][0]["target_redacted"] is True
    assert packet["items"][0]["projected_blast_radius"] == "secret_scope"
    assert "credential_or_sensitive_data_exposure" in packet["items"][0]["likely_impacts"]
    assert "redact_sensitive_target" in packet["items"][0]["pre_action_controls"]
    assert packet["items"][1]["forecast_status"] == "approval_recommended"
    assert packet["items"][1]["projected_blast_radius"] == "production_infrastructure"
    assert "require_blast_radius_context" in packet["items"][1]["pre_action_controls"]
    assert packet["redaction"]["private_asset_graph"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_intent_action_drift_detects_sensitive_scope_change(tmp_path: Path) -> None:
    store = ActivityStore(tmp_path / "activity.json")
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
            "declared_intent": "Inspect deployment configuration",
        }
    )
    store.upsert_decision(
        {
            **_decision(
                decision_id="dec-doc-write",
                session_id="session-2",
                agent_id="claude-code-agent",
                decision="warn",
                severity="medium",
                action_type="mcp_tool_call",
                target="filesystem.write",
                rule_id="mcp.untrusted-tool",
            ),
            "declared_intent": "Write generated infrastructure documentation",
        }
    )

    packet = build_aispm_intent_action_drift(store)

    assert packet["schema_version"] == "cavra.aispm.intent_action_drift.v1"
    assert packet["summary"]["total_items"] == 2
    assert packet["summary"]["high_drift"] == 1
    assert packet["summary"]["aligned"] == 1
    assert packet["summary"]["evidence_confidence"] == "signed_evidence"
    assert packet["items"][0]["drift_status"] == "high_drift"
    assert packet["items"][0]["target_redacted"] is True
    assert "sensitive_target_not_declared" in packet["items"][0]["drift_signals"]
    assert packet["items"][0]["recommended_action"].startswith("Block or escalate")
    assert packet["items"][1]["drift_status"] == "aligned"
    assert packet["redaction"]["raw_prompt"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


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


def test_aispm_pre_action_forecast_sample_matches_packaged_schema() -> None:
    forecast_schema = Path("src/cavra/schemas/aispm-pre-action-risk-forecasts.schema.json")
    sample = Path("examples/aispm/community-pre-action-risk-forecasts-sample.json")

    assert forecast_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(forecast_schema.read_text(encoding="utf-8")),
    )


def test_aispm_intent_action_drift_sample_matches_packaged_schema() -> None:
    drift_schema = Path("src/cavra/schemas/aispm-intent-action-drift.schema.json")
    sample = Path("examples/aispm/community-intent-action-drift-sample.json")

    assert drift_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(drift_schema.read_text(encoding="utf-8")),
    )


def test_aispm_approval_lineage_redacts_human_actors(tmp_path: Path) -> None:
    activity = ActivityStore(tmp_path / "activity.json")
    approval_store = ApprovalStore(tmp_path / "approvals.json")
    decision = activity.upsert_decision(
        _decision(
            decision_id="dec-approval-iac",
            session_id="session-1",
            agent_id="codex-agent",
            decision="require_approval",
            severity="high",
        )
    )
    approval = approval_store.create_request(
        decision,
        approver_group="Cloud Security",
        requested_by="codex-agent",
    )
    approval_store.decide(
        approval["approval_id"],
        state="approved",
        actor="human.approver@example.com",
        reason="Reviewed change window.",
        external_ref="CAB-123",
    )

    lineage = build_aispm_approval_lineage(approval_store, activity, session_id="session-1")

    assert lineage["schema_version"] == "cavra.aispm.approval_lineage.v1"
    assert lineage["summary"]["approved"] == 1
    assert lineage["summary"]["evidence_confidence"] == "approval_evidence_refs"
    assert lineage["items"][0]["requested_by"] == "automation:codex-agent"
    assert lineage["items"][0]["decided_by"] == "role:approver"
    assert lineage["items"][0]["decision"]["target_summary"] == "terraform apply"
    assert lineage["items"][0]["decision"]["risk_classification"] == "infrastructure_change_risk"
    assert lineage["redaction"]["identity_provider_claims"] == "requires_cavra_enterprise"
    assert "raw_rbac_context" in lineage["items"][0]["redacted_fields"]


def test_aispm_approval_lineage_sample_matches_packaged_schema() -> None:
    lineage_schema = Path("src/cavra/schemas/aispm-approval-lineage.schema.json")
    sample = Path("examples/aispm/community-approval-lineage-sample.json")

    assert lineage_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(lineage_schema.read_text(encoding="utf-8")),
    )


def test_aispm_behavior_fingerprint_sample_matches_packaged_schema() -> None:
    fingerprint_schema = Path("src/cavra/schemas/aispm-behavior-fingerprints.schema.json")
    sample = Path("examples/aispm/community-behavior-fingerprints-sample.json")

    assert fingerprint_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(fingerprint_schema.read_text(encoding="utf-8")),
    )


def test_aispm_policy_context_gap_sample_matches_packaged_schema() -> None:
    gap_schema = Path("src/cavra/schemas/aispm-policy-context-gaps.schema.json")
    sample = Path("examples/aispm/community-policy-context-gaps-sample.json")

    assert gap_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(gap_schema.read_text(encoding="utf-8")),
    )
