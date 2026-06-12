from pathlib import Path
from datetime import datetime, timedelta, timezone
import json

import jsonschema

from cavra.activity import ActivityStore
from cavra.aispm import (
    build_aispm_agent_blast_radius,
    build_aispm_approval_lineage,
    build_aispm_behavior_fingerprints,
    build_aispm_control_coverage_heatmap,
    build_aispm_dashboard_contract,
    build_aispm_evidence_confidence_drilldown,
    build_aispm_evidence_freshness_slo,
    build_aispm_executive_risk_narrative,
    build_aispm_intent_action_drift,
    build_aispm_policy_context_gaps,
    build_aispm_posture,
    build_aispm_pre_action_risk_forecasts,
    build_aispm_replay_to_policy_draft,
    build_aispm_replay_to_policy_tests,
    build_aispm_trace_replay_packet,
    build_aispm_tool_chain_graph,
    build_sample_aispm_dashboard,
)
from cavra.aispm_reports import (
    build_aispm_report_center_trial_evaluator_handoff_packet_contract,
    build_aispm_report_center_trial_lab_notebook_outline_contract,
    build_aispm_report_center_trial_lab_notebook_publication_readiness_contract,
    build_aispm_report_center_trial_operator_api_view_model_contract,
    build_aispm_report_center_trial_operator_dashboard_readiness_contract,
    build_aispm_report_center_trial_revocation_expiry_evidence_contract,
    build_aispm_report_center_trial_validation_packet_contract,
    build_aispm_report_approval_decision_contract,
    build_aispm_report_alert_drilldown_contract,
    build_aispm_report_alert_escalation_contract,
    build_aispm_report_alert_operations_dashboard_contract,
    build_aispm_report_alert_remediation_closure_contract,
    build_aispm_report_alert_remediation_plan_contract,
    build_aispm_report_delivery_audit_event_contract,
    build_aispm_report_delivery_contract,
    build_aispm_report_evidence_room_access_event_contract,
    build_aispm_report_evidence_room_contract,
    build_aispm_report_exception_lifecycle_contract,
    build_aispm_report_export_package_manifest_contract,
    build_aispm_report_incident_closure_contract,
    build_aispm_report_incident_packet_contract,
    build_aispm_report_kpi_metrics_contract,
    build_aispm_report_operations_dashboard_contract,
    build_aispm_report_recipient_policy_contract,
    build_aispm_report_remediation_closure_digest_distribution_contract,
    build_aispm_report_remediation_closure_executive_digest_contract,
    build_aispm_report_remediation_closure_operations_dashboard_contract,
    build_aispm_report_retention_lifecycle_contract,
    build_aispm_report_schedule_policy_contract,
    build_aispm_report_search_retrieval_contract,
    build_aispm_report_setup_wizard_contract,
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
    assert posture["tool_chain_graph"]["hotspots"][0]["risk_band"] == "critical"
    assert posture["tool_chain_graph"]["edges"][0]["relationship"] == "invoked_tool"
    assert posture["agent_blast_radius"][0]["agent_id"] == "codex-agent"
    assert posture["agent_blast_radius"][0]["blast_radius_level"] in {"high", "critical"}
    assert "sensitive_data_reach" in posture["agent_blast_radius"][0]["top_risks"]
    assert {item["risk_classification"] for item in posture["findings"]} == {
        "credential_or_sensitive_data_exposure",
        "infrastructure_change_risk",
    }
    coverage = {item["surface_id"]: item for item in posture["control_coverage"]}
    assert coverage["sensitive_data"]["coverage_status"] == "enforced"
    assert coverage["infrastructure_iac"]["coverage_status"] == "approval_gated"
    assert coverage["mcp_tools"]["coverage_status"] == "not_observed_locally"
    assert posture["control_coverage_heatmap"]["rows"][0]["agent_id"] == "codex-agent"
    assert posture["control_coverage_heatmap"]["coverage_score"] > 0
    assert any(cell["coverage_status"] == "enforced" for cell in posture["control_coverage_heatmap"]["rows"][0]["cells"])
    assert posture["evidence_confidence_drilldown"]["summary"]["signed_evidence_items"] == 2
    assert posture["evidence_confidence_drilldown"]["facts"][0]["confidence_level"] == "signed_evidence"
    assert posture["evidence_freshness_slo"]["summary"]["total_items"] == 2
    assert posture["evidence_freshness_slo"]["summary"]["freshness_score"] >= 0
    assert "CAVRA Community reports" in posture["executive_risk_narrative"]["headline"]
    assert posture["executive_risk_narrative"]["recommended_actions"]
    assert posture["executive_risk_narrative"]["key_metrics"]["blocked_actions"] == 1
    assert posture["replay_to_policy_draft"]["summary"]["recommended_rules"] == 2
    assert posture["replay_to_policy_draft"]["summary"]["draft_valid"] is True
    assert ".env*" in posture["replay_to_policy_draft"]["policy_draft"]["policy_pack"]["filesystem"]["block_read"]
    assert "terraform apply*" in posture["replay_to_policy_draft"]["policy_draft"]["policy_pack"]["commands"]["require_approval"]
    assert [item["decision"] for item in posture["near_misses"]] == ["require_approval"]
    assert posture["near_misses"][0]["operator_signal"] == "approval_prevented_unreviewed_execution"
    assert posture["control_plane"]["kill_switch"] == "requires_cavra_enterprise"


def test_aispm_sample_dashboard_matches_packaged_schema() -> None:
    dashboard_schema = Path("src/cavra/schemas/aispm-dashboard.schema.json")
    sample = build_sample_aispm_dashboard()

    assert dashboard_schema.is_file()
    jsonschema.validate(sample, schema=json.loads(dashboard_schema.read_text(encoding="utf-8")))


def test_aispm_replay_to_policy_draft_builds_valid_read_only_policy(tmp_path: Path) -> None:
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
            rule_id="iac.production-change",
        )
    )
    store.upsert_session({"session_id": "session-1", "state": "completed"})

    packet = build_aispm_replay_to_policy_draft(store, session_id="session-1")

    assert packet["schema_version"] == "cavra.aispm.replay_to_policy_draft.v1"
    assert packet["edition"] == "community"
    assert packet["summary"]["source_decisions"] == 2
    assert packet["summary"]["authorable_decisions"] == 2
    assert packet["summary"]["recommended_rules"] == 2
    assert packet["summary"]["draft_valid"] is True
    assert packet["policy_draft"]["valid"] is True
    assert packet["policy_draft"]["policy_pack"]["metadata"]["id"] == "cavra-replay-derived-session-1"
    assert packet["policy_draft"]["policy_pack"]["filesystem"]["block_read"] == [".env*"]
    assert packet["policy_draft"]["policy_pack"]["commands"]["require_approval"] == ["terraform apply*"]
    assert packet["write_back"]["status"] == "read_only_preview"
    assert packet["redaction"]["raw_prompts"] == "requires_cavra_enterprise"
    assert packet["redaction"]["private_asset_graph"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_replay_to_policy_tests_exports_public_safe_fixture(tmp_path: Path) -> None:
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
            rule_id="iac.production-change",
        )
    )

    packet = build_aispm_replay_to_policy_tests(store, session_id="session-1")

    assert packet["schema_version"] == "cavra.aispm.replay_to_policy_tests.v1"
    assert packet["edition"] == "community"
    assert packet["summary"]["test_cases"] == 2
    assert packet["summary"]["fixture_valid"] is True
    assert packet["test_fixture"]["schema_version"] == "cavra.policy_tests.replay_to_policy.v1"
    assert packet["test_fixture"]["case_count"] == 2
    assert packet["test_fixture"]["cases"][0]["public_safe"] is True
    assert packet["test_fixture"]["cases"][0]["expected"]["policy_section"] in {"filesystem", "commands"}
    assert packet["export"]["status"] == "read_only_preview"
    assert packet["redaction"]["private_simulation_history"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


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


def test_aispm_tool_chain_graph_maps_public_safe_edges(tmp_path: Path) -> None:
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
            "tool": "filesystem",
            "tool_capability": "file_read",
        }
    )
    store.upsert_decision(
        {
            **_decision(
                decision_id="dec-mcp-write",
                session_id="session-2",
                agent_id="claude-code-agent",
                decision="warn",
                severity="medium",
                action_type="mcp_tool_call",
                target="filesystem.write",
                rule_id="mcp.untrusted-tool",
            ),
            "server": "filesystem-mcp",
            "tool": "filesystem.write",
            "tool_capability": "workspace_write",
        }
    )

    packet = build_aispm_tool_chain_graph(store)

    assert packet["schema_version"] == "cavra.aispm.tool_chain_graph.v1"
    assert packet["summary"]["tool_nodes"] >= 2
    assert packet["summary"]["high_risk_edges"] >= 2
    assert packet["summary"]["blocked_edges"] >= 1
    assert packet["summary"]["evidence_confidence"] == "signed_evidence"
    assert packet["hotspots"][0]["agent_id"] == "codex-agent"
    assert packet["hotspots"][0]["risk_band"] == "critical"
    edge = packet["edges"][0]
    assert edge["risk_band"] == "critical"
    assert edge["risk_score"] >= 70
    assert edge["decision"] == "block"
    assert any(node["label"] == "sensitive target redacted" for node in packet["nodes"])
    assert packet["redaction"]["raw_tool_payload"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_agent_blast_radius_maps_public_safe_reach(tmp_path: Path) -> None:
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
            "tool": "filesystem",
            "tool_capability": "file_read",
        }
    )
    store.upsert_decision(
        {
            **_decision(
                decision_id="dec-approval-iac",
                session_id="session-1",
                agent_id="codex-agent",
                decision="require_approval",
                severity="high",
                action_type="execute_command",
                target="terraform apply",
            ),
            "tool": "shell",
            "tool_capability": "runtime_execution",
        }
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

    packet = build_aispm_agent_blast_radius(store)

    assert packet["schema_version"] == "cavra.aispm.agent_blast_radius.v1"
    assert packet["summary"]["total_agents"] == 1
    assert packet["summary"]["high_agents"] + packet["summary"]["critical_agents"] == 1
    assert packet["summary"]["affected_repositories"] == 1
    assert packet["summary"]["evidence_confidence"] == "signed_evidence"
    item = packet["items"][0]
    assert item["agent_id"] == "codex-agent"
    assert item["blast_radius_score"] >= 55
    assert item["repositories"] == ["payments/api"]
    assert "sensitive_data:redacted" in item["target_classes"]
    assert "production_infrastructure" in item["target_classes"]
    assert item["sensitive_target_count"] == 1
    assert item["production_infrastructure_count"] == 1
    assert item["blocked_actions"] == 1
    assert item["approval_required_actions"] == 1
    assert "sensitive_data_reach" in item["top_risks"]
    assert "require_blast_radius_context" in item["recommended_controls"]
    assert packet["redaction"]["private_asset_graph"] == "requires_cavra_enterprise"
    assert packet["redaction"]["identity_permission_graph"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_control_coverage_heatmap_maps_agent_repository_surface_cells(tmp_path: Path) -> None:
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
    store.upsert_session(
        {
            "session_id": "session-1",
            "agent_id": "codex-agent",
            "repository": "payments/api",
            "state": "completed",
            "updated_at": "2026-06-09T00:02:00+00:00",
        }
    )

    packet = build_aispm_control_coverage_heatmap(store)

    assert packet["schema_version"] == "cavra.aispm.control_coverage_heatmap.v1"
    assert packet["summary"]["row_count"] == 1
    assert packet["summary"]["surface_count"] == 6
    assert packet["summary"]["enforced_cells"] == 1
    assert packet["summary"]["approval_gated_cells"] == 1
    assert packet["summary"]["not_observed_cells"] == 4
    assert packet["summary"]["coverage_score"] > 0
    row = packet["rows"][0]
    assert row["agent_id"] == "codex-agent"
    assert row["repository"] == "payments/api"
    cells = {cell["surface_id"]: cell for cell in row["cells"]}
    assert cells["sensitive_data"]["coverage_status"] == "enforced"
    assert cells["infrastructure_iac"]["coverage_status"] == "approval_gated"
    assert cells["source_control"]["coverage_status"] == "not_observed_locally"
    assert "test evidence" in cells["source_control"]["recommended_action"]
    assert packet["redaction"]["repository_permission_matrix"] == "requires_cavra_enterprise"
    assert packet["redaction"]["live_org_baselines"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_evidence_confidence_drilldown_ranks_evidence_quality(tmp_path: Path) -> None:
    store = ActivityStore(tmp_path / "activity.json")
    store.upsert_decision(
        _decision(
            decision_id="dec-signed",
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
        {
            **_decision(
                decision_id="dec-metadata-only",
                session_id="session-1",
                agent_id="codex-agent",
                decision="warn",
                severity="medium",
            ),
            "evidence_refs": [],
        }
    )
    store.upsert_decision(
        {
            **_decision(
                decision_id="dec-activity-ref",
                session_id="session-2",
                agent_id="claude-code-agent",
                decision="require_approval",
                severity="high",
            ),
            "evidence_refs": ["artifact://evidence/dec-activity-ref"],
        }
    )
    store.upsert_session(
        {
            "session_id": "session-3",
            "agent_id": "docs-agent",
            "repository": "platform/docs",
            "state": "completed",
            "updated_at": "2026-06-09T00:04:00+00:00",
            "evidence_refs": ["sample://evidence/session"],
        }
    )

    packet = build_aispm_evidence_confidence_drilldown(store)

    assert packet["schema_version"] == "cavra.aispm.evidence_confidence.v1"
    assert packet["summary"]["total_facts"] == 4
    assert packet["summary"]["signed_evidence_items"] == 1
    assert packet["summary"]["activity_evidence_items"] == 1
    assert packet["summary"]["sample_evidence_items"] == 1
    assert packet["summary"]["metadata_only_items"] == 1
    assert packet["summary"]["evidence_score"] > 0
    levels = {item["source_id"]: item["confidence_level"] for item in packet["facts"]}
    assert levels["dec-signed"] == "signed_evidence"
    assert levels["dec-activity-ref"] == "activity_evidence_refs"
    assert levels["dec-metadata-only"] == "activity_metadata_only"
    assert levels["session-3"] == "sample_evidence_refs"
    assert packet["redaction"]["tenant_evidence_store"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_evidence_freshness_slo_flags_stale_and_retention_gaps() -> None:
    now = datetime.now(timezone.utc)

    class Store:
        def list_decisions(self, **_: object) -> dict[str, object]:
            return {
                "items": [
                    {
                        "decision_id": "dec-fresh-retained",
                        "session_id": "session-1",
                        "agent_id": "codex-agent",
                        "repository": "payments/api",
                        "policy_pack": "cloud-iam-prod",
                        "action_type": "execute_command",
                        "target": "terraform plan",
                        "decision": "allow_with_attestation",
                        "severity": "medium",
                        "timestamp": (now - timedelta(hours=1)).isoformat(),
                        "evidence_refs": ["archive://evidence/dec-fresh-retained"],
                    },
                    {
                        "decision_id": "dec-stale",
                        "session_id": "session-2",
                        "agent_id": "claude-code-agent",
                        "repository": "platform/infra",
                        "policy_pack": "mcp-enterprise",
                        "action_type": "mcp_tool_call",
                        "target": "filesystem.write",
                        "decision": "warn",
                        "severity": "medium",
                        "timestamp": (now - timedelta(days=10)).isoformat(),
                        "evidence_refs": ["artifact://evidence/dec-stale"],
                    },
                    {
                        "decision_id": "dec-missing-retention",
                        "session_id": "session-3",
                        "agent_id": "docs-agent",
                        "repository": "platform/docs",
                        "policy_pack": "cavra-ai-agent-baseline",
                        "action_type": "read_file",
                        "target": "README.md",
                        "decision": "allow",
                        "severity": "low",
                        "timestamp": (now - timedelta(days=2)).isoformat(),
                        "evidence_refs": [],
                    },
                    {
                        "decision_id": "dec-missing-time",
                        "session_id": "session-4",
                        "agent_id": "test-agent",
                        "repository": "quality/tests",
                        "policy_pack": "cavra-ai-agent-baseline",
                        "action_type": "execute_command",
                        "target": "pytest",
                        "decision": "allow",
                        "severity": "low",
                        "evidence_refs": ["sample://evidence/test"],
                    },
                ]
            }

        def list_sessions(self, **_: object) -> dict[str, object]:
            return {"items": []}

    packet = build_aispm_evidence_freshness_slo(Store())

    assert packet["schema_version"] == "cavra.aispm.evidence_freshness.v1"
    assert packet["summary"]["total_items"] == 4
    assert packet["summary"]["fresh_items"] == 1
    assert packet["summary"]["review_soon_items"] == 1
    assert packet["summary"]["stale_items"] == 1
    assert packet["summary"]["missing_timestamp_items"] == 1
    assert packet["summary"]["retention_ready_items"] == 1
    assert packet["summary"]["retention_gap_items"] == 2
    assert packet["summary"]["slo_breached_items"] == 3
    statuses = {item["source_id"]: item for item in packet["items"]}
    assert statuses["dec-fresh-retained"]["slo_status"] == "met"
    assert statuses["dec-stale"]["slo_status"] == "breached"
    assert statuses["dec-missing-retention"]["retention_status"] == "metadata_only"
    assert statuses["dec-missing-time"]["freshness_status"] == "timestamp_missing"
    assert packet["redaction"]["object_lock_status"] == "requires_cavra_enterprise"
    assert packet["enterprise_unlocks"]["private_package"] == "cavra_enterprise"


def test_aispm_executive_risk_narrative_summarizes_public_safe_posture(tmp_path: Path) -> None:
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

    packet = build_aispm_executive_risk_narrative(store)
    narrative = packet["narrative"]

    assert packet["schema_version"] == "cavra.aispm.executive_risk_narrative.v1"
    assert packet["edition"] == "community"
    assert "CAVRA Community reports" in narrative["headline"]
    assert narrative["risk_level"] in {"high", "critical"}
    assert narrative["key_metrics"]["blocked_actions"] == 1
    assert narrative["key_metrics"]["approval_required_actions"] == 1
    assert narrative["top_risks"][0]["agent_id"] == "codex-agent"
    assert {action["action_id"] for action in narrative["recommended_actions"]} >= {
        "review-top-ai-agent-risks",
        "validate-approval-latency",
    }
    assert "security leadership" in narrative["audience"]
    assert packet["redaction"]["ai_generated_board_summary"] == "requires_cavra_enterprise"
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


def test_aispm_tool_chain_graph_sample_matches_packaged_schema() -> None:
    graph_schema = Path("src/cavra/schemas/aispm-tool-chain-graph.schema.json")
    sample = Path("examples/aispm/community-tool-chain-graph-sample.json")

    assert graph_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(graph_schema.read_text(encoding="utf-8")),
    )


def test_aispm_agent_blast_radius_sample_matches_packaged_schema() -> None:
    blast_schema = Path("src/cavra/schemas/aispm-agent-blast-radius.schema.json")
    sample = Path("examples/aispm/community-agent-blast-radius-sample.json")

    assert blast_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(blast_schema.read_text(encoding="utf-8")),
    )


def test_aispm_control_coverage_heatmap_sample_matches_packaged_schema() -> None:
    heatmap_schema = Path("src/cavra/schemas/aispm-control-coverage-heatmap.schema.json")
    sample = Path("examples/aispm/community-control-coverage-heatmap-sample.json")

    assert heatmap_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(heatmap_schema.read_text(encoding="utf-8")),
    )


def test_aispm_evidence_confidence_sample_matches_packaged_schema() -> None:
    evidence_schema = Path("src/cavra/schemas/aispm-evidence-confidence.schema.json")
    sample = Path("examples/aispm/community-evidence-confidence-sample.json")

    assert evidence_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(evidence_schema.read_text(encoding="utf-8")),
    )


def test_aispm_evidence_freshness_sample_matches_packaged_schema() -> None:
    freshness_schema = Path("src/cavra/schemas/aispm-evidence-freshness.schema.json")
    sample = Path("examples/aispm/community-evidence-freshness-sample.json")

    assert freshness_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(freshness_schema.read_text(encoding="utf-8")),
    )


def test_aispm_executive_risk_narrative_sample_matches_packaged_schema() -> None:
    narrative_schema = Path("src/cavra/schemas/aispm-executive-risk-narrative.schema.json")
    sample = Path("examples/aispm/community-executive-risk-narrative-sample.json")

    assert narrative_schema.is_file()
    assert sample.is_file()
    jsonschema.validate(
        json.loads(sample.read_text(encoding="utf-8")),
        schema=json.loads(narrative_schema.read_text(encoding="utf-8")),
    )


def test_aispm_replay_to_policy_draft_sample_matches_packaged_schema() -> None:
    draft_schema = Path("src/cavra/schemas/aispm-replay-to-policy-draft.schema.json")
    sample = Path("examples/aispm/community-replay-to-policy-draft-sample.json")

    assert draft_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(draft_schema.read_text(encoding="utf-8")),
    )
    assert payload["summary"]["draft_valid"] is True
    assert payload["write_back"]["status"] == "read_only_preview"


def test_aispm_replay_to_policy_tests_sample_matches_packaged_schema() -> None:
    tests_schema = Path("src/cavra/schemas/aispm-replay-to-policy-tests.schema.json")
    sample = Path("examples/aispm/community-replay-to-policy-tests-sample.json")

    assert tests_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(tests_schema.read_text(encoding="utf-8")),
    )
    assert payload["summary"]["fixture_valid"] is True
    assert payload["test_fixture"]["case_count"] == payload["summary"]["test_cases"]


def test_aispm_replay_to_policy_review_packet_sample_matches_packaged_schema() -> None:
    review_schema = Path("src/cavra/schemas/aispm-replay-to-policy-review-packet.schema.json")
    sample = Path("examples/aispm/community-replay-to-policy-review-packet-sample.json")

    assert review_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(review_schema.read_text(encoding="utf-8")),
    )
    assert payload["export"]["status"] == "review_only_packet"
    assert payload["review_summary"]["ci_adoption"] == "requires_human_review"
    assert payload["test_fixture"]["case_count"] == len(payload["test_fixture"]["cases"])


def test_aispm_replay_to_policy_ci_gate_readiness_sample_matches_packaged_schema() -> None:
    readiness_schema = Path("src/cavra/schemas/aispm-replay-to-policy-ci-gate-readiness.schema.json")
    sample = Path("examples/aispm/community-replay-to-policy-ci-gate-readiness-sample.json")

    assert readiness_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(readiness_schema.read_text(encoding="utf-8")),
    )
    assert payload["source"]["review_packet"] == "cavra-replay-policy-review-packet.json"
    assert {gate["platform"] for gate in payload["gates"]} == {
        "GitHub Actions",
        "GitLab CI",
        "Azure Pipelines",
    }
    assert {gate["required_check"] for gate in payload["gates"]} == {"cavra-aispm-review-packet"}


def test_aispm_enterprise_live_ingestion_public_contract_sample_matches_packaged_schema() -> None:
    envelope_schema = Path("src/cavra/schemas/aispm-enterprise-live-ingestion-envelope.schema.json")
    sample = Path("examples/aispm/enterprise-live-ingestion-envelope-public-contract.example.json")

    assert envelope_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(envelope_schema.read_text(encoding="utf-8")),
    )
    assert payload["contract_visibility"] == "public_contract"
    assert payload["redaction"]["raw_prompt_included"] is False
    assert payload["redaction"]["reasoning_included"] is False
    assert payload["redaction"]["tool_output_included"] is False
    assert payload["enterprise_boundaries"]["collector_implementation"] == "requires_cavra_enterprise"


def test_aispm_report_delivery_contract_matches_packaged_schema() -> None:
    report_schema = Path("src/cavra/schemas/aispm-report-delivery-contract.schema.json")
    contract = build_aispm_report_delivery_contract()

    assert report_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(report_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["setup"]["secret_values_allowed_in_public_repo"] is False
    assert contract["api"]["send_endpoint"] == "POST /enterprise/aispm/reports/send"
    assert contract["enterprise_boundaries"]["email_delivery"] == "requires_cavra_enterprise"
    assert {report["availability"] for report in contract["community_reports"]} == {"community"}
    assert {report["availability"] for report in contract["enterprise_reports"]} == {
        "requires_cavra_enterprise"
    }


def test_aispm_report_delivery_public_contract_sample_matches_packaged_schema() -> None:
    report_schema = Path("src/cavra/schemas/aispm-report-delivery-contract.schema.json")
    sample = Path("examples/aispm/enterprise-report-delivery-contract-public.example.json")

    assert report_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(report_schema.read_text(encoding="utf-8")),
    )
    assert payload["delivery"]["implementation"] == "requires_cavra_enterprise"
    assert "CAVRA_REPORT_SMTP_PASSWORD_REF" in payload["setup"]["secret_reference_settings"]
    assert "CAVRA_REPORT_SMTP_PASSWORD" not in payload["setup"]["secret_reference_settings"]


def test_aispm_report_setup_wizard_contract_matches_packaged_schema() -> None:
    setup_schema = Path("src/cavra/schemas/aispm-report-setup-wizard-contract.schema.json")
    contract = build_aispm_report_setup_wizard_contract()

    assert setup_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(setup_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["wizard"]["implementation"] == "requires_cavra_enterprise"
    assert contract["admin_settings"]["secret_values_allowed"] is False
    assert "CAVRA_REPORT_DELIVERY_MODE" in contract["admin_settings"]["required_public_settings"]
    assert "CAVRA_REPORT_SMTP_PASSWORD_REF" in contract["admin_settings"]["secret_reference_settings"]
    assert contract["enterprise_boundaries"]["provider_validation"] == "requires_cavra_enterprise"


def test_aispm_report_setup_wizard_public_contract_sample_matches_packaged_schema() -> None:
    setup_schema = Path("src/cavra/schemas/aispm-report-setup-wizard-contract.schema.json")
    sample = Path("examples/aispm/enterprise-report-setup-wizard-contract-public.example.json")

    assert setup_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(setup_schema.read_text(encoding="utf-8")),
    )
    assert {step["step_id"] for step in payload["steps"]} == {
        "organization_profile",
        "delivery_provider",
        "recipient_governance",
        "schedule_and_audit",
    }
    assert payload["admin_settings"]["secret_values_allowed"] is False
    assert "CAVRA_REPORT_PROVIDER_TOKEN_REF" in payload["admin_settings"]["secret_reference_settings"]
    assert payload["enterprise_boundaries"]["test_delivery"] == "requires_cavra_enterprise"


def test_aispm_report_delivery_audit_event_contract_matches_packaged_schema() -> None:
    audit_schema = Path("src/cavra/schemas/aispm-report-delivery-audit-event.schema.json")
    contract = build_aispm_report_delivery_audit_event_contract()

    assert audit_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(audit_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["audit_event"]["action"] == "send"
    assert contract["recipient_summary"]["recipient_addresses_redacted"] is True
    assert contract["redaction"]["raw_report_content_included"] is False
    assert contract["redaction"]["provider_response_included"] is False
    assert contract["redaction"]["secrets_included"] is False
    assert contract["enterprise_boundaries"]["retry_worker"] == "requires_cavra_enterprise"


def test_aispm_report_delivery_audit_event_public_sample_matches_packaged_schema() -> None:
    audit_schema = Path("src/cavra/schemas/aispm-report-delivery-audit-event.schema.json")
    sample = Path("examples/aispm/enterprise-report-delivery-audit-event-public.example.json")

    assert audit_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(audit_schema.read_text(encoding="utf-8")),
    )
    assert payload["audit_event"]["status"] == "sent"
    assert payload["approval"]["decision"] == "approved"
    assert payload["retry"]["terminal"] is True
    assert payload["evidence"]["evidence_refs"]
    assert payload["redaction"]["recipient_addresses_included"] is False
    assert payload["enterprise_boundaries"]["audit_store"] == "requires_cavra_enterprise"


def test_aispm_report_operations_dashboard_contract_matches_packaged_schema() -> None:
    dashboard_schema = Path("src/cavra/schemas/aispm-report-operations-dashboard.schema.json")
    contract = build_aispm_report_operations_dashboard_contract()

    assert dashboard_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["summary"]["delivery_health"] == "degraded"
    assert contract["summary"]["failed_deliveries"] == 1
    assert contract["queues"][0]["queue"] == "delivery"
    assert contract["approval_bottlenecks"][0]["status"] == "pending"
    assert contract["redaction"]["secrets_included"] is False
    assert contract["enterprise_boundaries"]["retry_control"] == "requires_cavra_enterprise"


def test_aispm_report_operations_dashboard_public_sample_matches_packaged_schema() -> None:
    dashboard_schema = Path("src/cavra/schemas/aispm-report-operations-dashboard.schema.json")
    sample = Path("examples/aispm/enterprise-report-operations-dashboard-public.example.json")

    assert dashboard_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert payload["summary"]["retry_queue_depth"] == 3
    assert payload["failed_deliveries"][0]["failure_class"] == "provider_auth"
    assert payload["audit_coverage"]["coverage_status"] == "partial"
    assert payload["redaction"]["recipient_addresses_included"] is False
    assert payload["enterprise_boundaries"]["provider_health_probe"] == "requires_cavra_enterprise"


def test_aispm_report_retention_lifecycle_contract_matches_packaged_schema() -> None:
    lifecycle_schema = Path("src/cavra/schemas/aispm-report-retention-lifecycle.schema.json")
    contract = build_aispm_report_retention_lifecycle_contract()

    assert lifecycle_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(lifecycle_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["policy"]["immutable_storage_required"] is True
    assert contract["policy"]["legal_hold_supported"] is True
    assert "legal_hold" in contract["deletion_policy"]["blocked_states"]
    assert contract["redaction"]["customer_records_included"] is False
    assert contract["enterprise_boundaries"]["kms_integration"] == "requires_cavra_enterprise"


def test_aispm_report_retention_lifecycle_public_sample_matches_packaged_schema() -> None:
    lifecycle_schema = Path("src/cavra/schemas/aispm-report-retention-lifecycle.schema.json")
    sample = Path("examples/aispm/enterprise-report-retention-lifecycle-public.example.json")

    assert lifecycle_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(lifecycle_schema.read_text(encoding="utf-8")),
    )
    assert payload["audit_export_lifecycle"]["object_lock"] == "enabled"
    assert payload["deletion_policy"]["approval_required"] is True
    assert any(item["lifecycle_state"] == "legal_hold" for item in payload["report_lifecycle"])
    assert payload["evidence"]["retention_evidence_refs"]
    assert payload["redaction"]["raw_report_content_included"] is False
    assert payload["enterprise_boundaries"]["immutable_archive"] == "requires_cavra_enterprise"


def test_aispm_report_search_retrieval_contract_matches_packaged_schema() -> None:
    search_schema = Path("src/cavra/schemas/aispm-report-search-retrieval.schema.json")
    contract = build_aispm_report_search_retrieval_contract()

    assert search_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(search_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["query"]["retention_mode"] == "retention_aware"
    assert contract["retrieval"]["access_decision"] == "allow"
    assert contract["access_controls"]["rbac_enforced"] is True
    assert contract["access_controls"]["download_audit_required"] is True
    assert contract["redaction"]["download_url_included"] is False
    assert contract["enterprise_boundaries"]["signed_download_urls"] == "requires_cavra_enterprise"


def test_aispm_report_search_retrieval_public_sample_matches_packaged_schema() -> None:
    search_schema = Path("src/cavra/schemas/aispm-report-search-retrieval.schema.json")
    sample = Path("examples/aispm/enterprise-report-search-retrieval-public.example.json")

    assert search_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(search_schema.read_text(encoding="utf-8")),
    )
    assert payload["results"][0]["download_allowed"] is True
    assert payload["retrieval"]["watermark_required"] is True
    assert payload["access_controls"]["retention_checked"] is True
    assert payload["audit"]["evidence_refs"]
    assert payload["redaction"]["raw_report_content_included"] is False
    assert payload["enterprise_boundaries"]["rbac_authorization"] == "requires_cavra_enterprise"


def test_aispm_report_export_package_manifest_contract_matches_packaged_schema() -> None:
    manifest_schema = Path("src/cavra/schemas/aispm-report-export-package-manifest.schema.json")
    contract = build_aispm_report_export_package_manifest_contract()

    assert manifest_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(manifest_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["package"]["package_type"] == "board_and_audit_bundle"
    assert contract["integrity"]["checksums_required"] is True
    assert contract["delivery_targets"][0]["approval_required"] is True
    assert contract["redaction"]["raw_report_content_included"] is False
    assert contract["enterprise_boundaries"]["manifest_signing"] == "requires_cavra_enterprise"


def test_aispm_report_export_package_manifest_public_sample_matches_packaged_schema() -> None:
    manifest_schema = Path("src/cavra/schemas/aispm-report-export-package-manifest.schema.json")
    sample = Path("examples/aispm/enterprise-report-export-package-manifest-public.example.json")

    assert manifest_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(manifest_schema.read_text(encoding="utf-8")),
    )
    assert payload["package"]["signed_manifest_required"] is True
    assert len(payload["artifacts"]) == 2
    assert payload["evidence"]["source_evidence_refs"]
    assert payload["redaction"]["download_urls_included"] is False
    assert payload["enterprise_boundaries"]["artifact_storage"] == "requires_cavra_enterprise"


def test_aispm_report_schedule_policy_contract_matches_packaged_schema() -> None:
    schedule_schema = Path("src/cavra/schemas/aispm-report-schedule-policy.schema.json")
    contract = build_aispm_report_schedule_policy_contract()

    assert schedule_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(schedule_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["schedule"]["cadence"] == "weekly"
    assert contract["recipient_governance"]["recipient_addresses_redacted"] is True
    assert contract["approval_policy"]["change_requires_approval"] is True
    assert contract["retry_policy"]["dead_letter_required"] is True
    assert contract["redaction"]["secrets_included"] is False
    assert contract["enterprise_boundaries"]["scheduler_worker"] == "requires_cavra_enterprise"


def test_aispm_report_schedule_policy_public_sample_matches_packaged_schema() -> None:
    schedule_schema = Path("src/cavra/schemas/aispm-report-schedule-policy.schema.json")
    sample = Path("examples/aispm/enterprise-report-schedule-policy-public.example.json")

    assert schedule_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(schedule_schema.read_text(encoding="utf-8")),
    )
    assert payload["delivery"]["package_manifest_required"] is True
    assert payload["blackout_windows"][0]["behavior"] == "defer"
    assert payload["run_evidence"]["evidence_refs"]
    assert payload["redaction"]["provider_response_included"] is False
    assert payload["enterprise_boundaries"]["provider_delivery"] == "requires_cavra_enterprise"


def test_aispm_report_recipient_policy_contract_matches_packaged_schema() -> None:
    recipient_schema = Path("src/cavra/schemas/aispm-report-recipient-policy.schema.json")
    contract = build_aispm_report_recipient_policy_contract()

    assert recipient_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(recipient_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["policy"]["default_action"] == "deny"
    assert contract["domain_rules"][1]["approval_required"] is True
    assert contract["recipient_groups"][0]["addresses_redacted"] is True
    assert contract["approval_policy"]["approval_evidence_required"] is True
    assert contract["redaction"]["recipient_addresses_included"] is False
    assert contract["enterprise_boundaries"]["idp_group_resolution"] == "requires_cavra_enterprise"


def test_aispm_report_recipient_policy_public_sample_matches_packaged_schema() -> None:
    recipient_schema = Path("src/cavra/schemas/aispm-report-recipient-policy.schema.json")
    sample = Path("examples/aispm/enterprise-report-recipient-policy-public.example.json")

    assert recipient_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(recipient_schema.read_text(encoding="utf-8")),
    )
    assert payload["encryption_policy"]["kms_key_ref_required"] is True
    assert payload["delivery_channel_eligibility"][0]["requires_verified_sender"] is True
    assert payload["audit"]["review_evidence_refs"]
    assert payload["redaction"]["provider_tokens_included"] is False
    assert payload["enterprise_boundaries"]["domain_verification"] == "requires_cavra_enterprise"


def test_aispm_report_approval_decision_contract_matches_packaged_schema() -> None:
    approval_schema = Path("src/cavra/schemas/aispm-report-approval-decision.schema.json")
    contract = build_aispm_report_approval_decision_contract()

    assert approval_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(approval_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["approval_request"]["request_type"] == "external_delivery_exception"
    assert contract["decision"]["decision"] == "approved"
    assert contract["subject"]["recipient_addresses_redacted"] is True
    assert contract["evidence"]["approval_evidence_refs"]
    assert contract["redaction"]["approver_identity_included"] is False
    assert contract["enterprise_boundaries"]["policy_exception_store"] == "requires_cavra_enterprise"


def test_aispm_report_approval_decision_public_sample_matches_packaged_schema() -> None:
    approval_schema = Path("src/cavra/schemas/aispm-report-approval-decision.schema.json")
    sample = Path("examples/aispm/enterprise-report-approval-decision-public.example.json")

    assert approval_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(approval_schema.read_text(encoding="utf-8")),
    )
    assert payload["decision"]["conditions"]
    assert payload["policy_context"]["recipient_policy_ref"]
    assert payload["audit"]["audit_event_ref"]
    assert payload["redaction"]["private_justification_included"] is False
    assert payload["enterprise_boundaries"]["immutable_decision_audit"] == "requires_cavra_enterprise"


def test_aispm_report_exception_lifecycle_contract_matches_packaged_schema() -> None:
    lifecycle_schema = Path("src/cavra/schemas/aispm-report-exception-lifecycle.schema.json")
    contract = build_aispm_report_exception_lifecycle_contract()

    assert lifecycle_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(lifecycle_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["exception"]["status"] == "active"
    assert contract["review_policy"]["renewal_requires_approval"] is True
    assert contract["renewal"]["max_renewals"] == 1
    assert contract["closure"]["closure_state"] == "not_closed"
    assert contract["redaction"]["private_justification_included"] is False
    assert contract["enterprise_boundaries"]["exception_store"] == "requires_cavra_enterprise"


def test_aispm_report_exception_lifecycle_public_sample_matches_packaged_schema() -> None:
    lifecycle_schema = Path("src/cavra/schemas/aispm-report-exception-lifecycle.schema.json")
    sample = Path("examples/aispm/enterprise-report-exception-lifecycle-public.example.json")

    assert lifecycle_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(lifecycle_schema.read_text(encoding="utf-8")),
    )
    assert payload["lifecycle_events"][1]["event_type"] == "review_scheduled"
    assert payload["review_policy"]["closure_requires_evidence"] is True
    assert payload["evidence"]["evidence_refs"]
    assert payload["redaction"]["recipient_addresses_included"] is False
    assert payload["enterprise_boundaries"]["renewal_workflow"] == "requires_cavra_enterprise"


def test_aispm_report_evidence_room_contract_matches_packaged_schema() -> None:
    room_schema = Path("src/cavra/schemas/aispm-report-evidence-room.schema.json")
    contract = build_aispm_report_evidence_room_contract()

    assert room_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(room_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["room"]["status"] == "active"
    assert contract["access_scope"]["mfa_required"] is True
    assert contract["controls"]["access_log_required"] is True
    assert contract["redaction"]["download_urls_included"] is False
    assert contract["enterprise_boundaries"]["evidence_room_portal"] == "requires_cavra_enterprise"


def test_aispm_report_evidence_room_public_sample_matches_packaged_schema() -> None:
    room_schema = Path("src/cavra/schemas/aispm-report-evidence-room.schema.json")
    sample = Path("examples/aispm/enterprise-report-evidence-room-public.example.json")

    assert room_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(room_schema.read_text(encoding="utf-8")),
    )
    assert payload["artifacts"][0]["watermark_required"] is True
    assert payload["controls"]["time_limited_links"] is True
    assert payload["access_log"]["evidence_refs"]
    assert payload["redaction"]["auditor_identity_included"] is False
    assert payload["enterprise_boundaries"]["immutable_access_log"] == "requires_cavra_enterprise"


def test_aispm_report_evidence_room_access_event_contract_matches_packaged_schema() -> None:
    event_schema = Path("src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json")
    contract = build_aispm_report_evidence_room_access_event_contract()

    assert event_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(event_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["event"]["event_type"] == "download"
    assert contract["access_decision"]["decision"] == "allow"
    assert contract["controls"]["immutable_audit_required"] is True
    assert contract["redaction"]["download_urls_included"] is False
    assert contract["enterprise_boundaries"]["immutable_access_event_store"] == "requires_cavra_enterprise"


def test_aispm_report_evidence_room_access_event_public_sample_matches_packaged_schema() -> None:
    event_schema = Path("src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json")
    sample = Path("examples/aispm/enterprise-report-evidence-room-access-event-public.example.json")

    assert event_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(event_schema.read_text(encoding="utf-8")),
    )
    assert payload["actor"]["identity_redacted"] is True
    assert payload["actor"]["ip_address_redacted"] is True
    assert payload["artifacts"][0]["watermark_applied"] is True
    assert payload["integrity"]["evidence_refs"]
    assert payload["redaction"]["auditor_identity_included"] is False
    assert payload["enterprise_boundaries"]["signed_download_links"] == "requires_cavra_enterprise"


def test_aispm_report_incident_packet_contract_matches_packaged_schema() -> None:
    packet_schema = Path("src/cavra/schemas/aispm-report-incident-packet.schema.json")
    contract = build_aispm_report_incident_packet_contract()

    assert packet_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(packet_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["incident"]["incident_type"] == "evidence_room_access_review"
    assert contract["related_records"]["access_event_refs"]
    assert contract["controls"]["chain_of_custody_required"] is True
    assert contract["redaction"]["raw_report_content_included"] is False
    assert contract["enterprise_boundaries"]["incident_packet_builder"] == "requires_cavra_enterprise"


def test_aispm_report_incident_packet_public_sample_matches_packaged_schema() -> None:
    packet_schema = Path("src/cavra/schemas/aispm-report-incident-packet.schema.json")
    sample = Path("examples/aispm/enterprise-report-incident-packet-public.example.json")

    assert packet_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(packet_schema.read_text(encoding="utf-8")),
    )
    assert payload["incident"]["status"] == "under_review"
    assert payload["review"]["approval_required"] is True
    assert payload["evidence"]["evidence_refs"]
    assert payload["redaction"]["auditor_identity_included"] is False
    assert payload["redaction"]["download_urls_included"] is False
    assert payload["enterprise_boundaries"]["immutable_incident_store"] == "requires_cavra_enterprise"


def test_aispm_report_incident_closure_contract_matches_packaged_schema() -> None:
    closure_schema = Path("src/cavra/schemas/aispm-report-incident-closure.schema.json")
    contract = build_aispm_report_incident_closure_contract()

    assert closure_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(closure_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["incident"]["final_status"] == "closed"
    assert contract["closure_approval"]["decision"] == "approved"
    assert contract["controls"]["immutable_closure_required"] is True
    assert contract["redaction"]["approver_identity_included"] is False
    assert contract["enterprise_boundaries"]["closure_workflow"] == "requires_cavra_enterprise"


def test_aispm_report_incident_closure_public_sample_matches_packaged_schema() -> None:
    closure_schema = Path("src/cavra/schemas/aispm-report-incident-closure.schema.json")
    sample = Path("examples/aispm/enterprise-report-incident-closure-public.example.json")

    assert closure_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(closure_schema.read_text(encoding="utf-8")),
    )
    assert payload["remediation"]["actions"][0]["status"] == "completed"
    assert payload["lessons_learned"]["control_updates"]
    assert payload["follow_up_tasks"][0]["evidence_required"] is True
    assert payload["redaction"]["raw_report_content_included"] is False
    assert payload["enterprise_boundaries"]["immutable_closure_store"] == "requires_cavra_enterprise"


def test_aispm_report_kpi_metrics_contract_matches_packaged_schema() -> None:
    metrics_schema = Path("src/cavra/schemas/aispm-report-kpi-metrics.schema.json")
    contract = build_aispm_report_kpi_metrics_contract()

    assert metrics_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(metrics_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["summary"]["audit_readiness_score"] == 0.91
    assert contract["delivery_health"]["failed_deliveries"] == 3
    assert contract["controls"]["tenant_aggregated"] is True
    assert contract["redaction"]["tenant_drilldown_records_included"] is False
    assert contract["enterprise_boundaries"]["metrics_aggregation_worker"] == "requires_cavra_enterprise"


def test_aispm_report_kpi_metrics_public_sample_matches_packaged_schema() -> None:
    metrics_schema = Path("src/cavra/schemas/aispm-report-kpi-metrics.schema.json")
    sample = Path("examples/aispm/enterprise-report-kpi-metrics-public.example.json")

    assert metrics_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(metrics_schema.read_text(encoding="utf-8")),
    )
    assert payload["window"]["grain"] == "weekly"
    assert payload["approval_latency"]["breached_slo_count"] == 1
    assert payload["evidence_room_access"]["watermarked_downloads"] == 6
    assert payload["redaction"]["payload_handling"] == "aggregate_metrics_only"
    assert payload["enterprise_boundaries"]["dashboard_projection"] == "requires_cavra_enterprise"


def test_aispm_report_alert_escalation_contract_matches_packaged_schema() -> None:
    alert_schema = Path("src/cavra/schemas/aispm-report-alert-escalation.schema.json")
    contract = build_aispm_report_alert_escalation_contract()

    assert alert_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(alert_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["alert_policy"]["requires_acknowledgement"] is True
    assert contract["evaluations"][1]["severity"] == "critical"
    assert contract["routing"]["recipient_addresses_redacted"] is True
    assert contract["controls"]["derived_from_kpi_metrics"] is True
    assert contract["redaction"]["tenant_drilldown_records_included"] is False
    assert contract["enterprise_boundaries"]["alert_evaluator"] == "requires_cavra_enterprise"


def test_aispm_report_alert_escalation_public_sample_matches_packaged_schema() -> None:
    alert_schema = Path("src/cavra/schemas/aispm-report-alert-escalation.schema.json")
    sample = Path("examples/aispm/enterprise-report-alert-escalation-public.example.json")

    assert alert_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(alert_schema.read_text(encoding="utf-8")),
    )
    assert payload["trigger_rules"][0]["rule_id"] == "failed-delivery-spike"
    assert payload["evaluations"][2]["status"] == "suppressed"
    assert payload["escalation"]["current_level"] == 2
    assert payload["acknowledgement"]["ack_status"] == "pending"
    assert payload["incident_linkage"]["closure_required"] is True
    assert payload["redaction"]["payload_handling"] == "metadata_and_aggregate_metrics_only"
    assert payload["enterprise_boundaries"]["notification_delivery"] == "requires_cavra_enterprise"


def test_aispm_report_alert_operations_dashboard_contract_matches_packaged_schema() -> None:
    dashboard_schema = Path("src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json")
    contract = build_aispm_report_alert_operations_dashboard_contract()

    assert dashboard_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["dashboard"]["status"] == "degraded"
    assert contract["dashboard"]["overdue_acknowledgements"] == 2
    assert contract["queues"][3]["status"] == "breached"
    assert contract["active_alerts"][0]["severity"] == "critical"
    assert contract["controls"]["derived_from_alert_events"] is True
    assert contract["redaction"]["operator_identity_included"] is False
    assert contract["enterprise_boundaries"]["dashboard_projection"] == "requires_cavra_enterprise"


def test_aispm_report_alert_operations_dashboard_public_sample_matches_packaged_schema() -> None:
    dashboard_schema = Path("src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json")
    sample = Path("examples/aispm/enterprise-report-alert-operations-dashboard-public.example.json")

    assert dashboard_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert payload["dashboard"]["critical_open"] == 1
    assert payload["acknowledgement_slos"]["overdue_count"] == 2
    assert payload["suppression_summary"]["suppression_audit_coverage"] == 1.0
    assert payload["incident_linkage_health"]["unlinked_alerts"] == 1
    assert payload["routing_health"][1]["status"] == "degraded"
    assert payload["redaction"]["payload_handling"] == "alert_operations_metadata_only"
    assert payload["enterprise_boundaries"]["routing_health_checks"] == "requires_cavra_enterprise"


def test_aispm_report_alert_drilldown_contract_matches_packaged_schema() -> None:
    drilldown_schema = Path("src/cavra/schemas/aispm-report-alert-drilldown.schema.json")
    contract = build_aispm_report_alert_drilldown_contract()

    assert drilldown_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(drilldown_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["alert"]["severity"] == "critical"
    assert contract["timeline"][2]["event_type"] == "escalated"
    assert contract["acknowledgement_history"][1]["status"] == "overdue"
    assert contract["linked_incident"]["closure_required"] is True
    assert contract["controls"]["timeline_ordered"] is True
    assert contract["redaction"]["operator_identity_included"] is False
    assert contract["enterprise_boundaries"]["drilldown_projection"] == "requires_cavra_enterprise"


def test_aispm_report_alert_drilldown_public_sample_matches_packaged_schema() -> None:
    drilldown_schema = Path("src/cavra/schemas/aispm-report-alert-drilldown.schema.json")
    sample = Path("examples/aispm/enterprise-report-alert-drilldown-public.example.json")

    assert drilldown_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(drilldown_schema.read_text(encoding="utf-8")),
    )
    assert payload["alert"]["rule_id"] == "evidence-room-suspicious-access"
    assert payload["routing"][1]["channel"] == "itsm"
    assert payload["suppression_history"][0]["reason_code"] == "duplicate_signal"
    assert payload["escalation_path"]["next_level"] == 3
    assert payload["evidence_chain"]["timeline_digest_ref"]
    assert payload["redaction"]["payload_handling"] == "single_alert_metadata_only"
    assert payload["enterprise_boundaries"]["timeline_event_store"] == "requires_cavra_enterprise"


def test_aispm_report_alert_remediation_plan_contract_matches_packaged_schema() -> None:
    plan_schema = Path("src/cavra/schemas/aispm-report-alert-remediation-plan.schema.json")
    contract = build_aispm_report_alert_remediation_plan_contract()

    assert plan_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(plan_schema.read_text(encoding="utf-8")),
    )
    assert contract["contract_visibility"] == "public_contract"
    assert contract["plan"]["priority"] == "critical"
    assert contract["tasks"][0]["status"] == "completed"
    assert contract["approval_requirements"][1]["approval_type"] == "plan_closure"
    assert contract["closure_criteria"]["post_incident_review_required"] is True
    assert contract["controls"]["approval_gates_enforced"] is True
    assert contract["redaction"]["private_remediation_details_included"] is False
    assert contract["enterprise_boundaries"]["remediation_workflow"] == "requires_cavra_enterprise"


def test_aispm_report_alert_remediation_plan_public_sample_matches_packaged_schema() -> None:
    plan_schema = Path("src/cavra/schemas/aispm-report-alert-remediation-plan.schema.json")
    sample = Path("examples/aispm/enterprise-report-alert-remediation-plan-public.example.json")

    assert plan_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(plan_schema.read_text(encoding="utf-8")),
    )
    assert payload["scope"]["customer_records_redacted"] is True
    assert payload["tasks"][1]["approval_required"] is True
    assert payload["control_updates"][0]["update_type"] == "policy_threshold"
    assert payload["communications"]["executive_update_required"] is True
    assert payload["evidence"]["alert_drilldown_ref"]
    assert payload["redaction"]["payload_handling"] == "remediation_metadata_only"
    assert payload["enterprise_boundaries"]["immutable_plan_store"] == "requires_cavra_enterprise"


def test_aispm_report_alert_remediation_closure_contract_matches_packaged_schema() -> None:
    closure_schema = Path("src/cavra/schemas/aispm-report-alert-remediation-closure.schema.json")
    contract = build_aispm_report_alert_remediation_closure_contract()

    assert closure_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(closure_schema.read_text(encoding="utf-8")),
    )
    assert contract["closure"]["final_status"] == "closed"
    assert contract["residual_risk"]["accepted"] is True
    assert contract["post_incident_review"]["completed"] is True
    assert contract["controls"]["immutable_closure_required"] is True
    assert contract["redaction"]["private_remediation_details_included"] is False
    assert contract["enterprise_boundaries"]["closure_workflow"] == "requires_cavra_enterprise"


def test_aispm_report_alert_remediation_closure_public_sample_matches_packaged_schema() -> None:
    closure_schema = Path("src/cavra/schemas/aispm-report-alert-remediation-closure.schema.json")
    sample = Path("examples/aispm/enterprise-report-alert-remediation-closure-public.example.json")

    assert closure_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(closure_schema.read_text(encoding="utf-8")),
    )
    assert payload["completed_tasks"][0]["task_ref"] == "task:opaque-revoke-access"
    assert payload["final_approvals"][0]["decision"] == "approved"
    assert payload["control_updates"][0]["final_status"] == "completed"
    assert payload["communications"]["executive_update_sent"] is True
    assert payload["evidence"]["closure_digest_ref"]
    assert payload["redaction"]["payload_handling"] == "remediation_closure_metadata_only"
    assert payload["enterprise_boundaries"]["immutable_closure_store"] == "requires_cavra_enterprise"


def test_aispm_report_remediation_closure_operations_dashboard_contract_matches_schema() -> None:
    dashboard_schema = Path(
        "src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json"
    )
    contract = build_aispm_report_remediation_closure_operations_dashboard_contract()

    assert dashboard_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert contract["dashboard"]["status"] == "degraded"
    assert contract["throughput"]["closure_rate"] == 0.82
    assert contract["residual_risk_aging"]["overdue_reviews"] == 1
    assert contract["closure_slo"]["at_risk_count"] == 4
    assert contract["controls"]["slo_policy_enforced"] is True
    assert contract["redaction"]["private_remediation_details_included"] is False
    assert (
        contract["enterprise_boundaries"]["closure_operations_projection"]
        == "requires_cavra_enterprise"
    )


def test_aispm_report_remediation_closure_operations_dashboard_sample_matches_schema() -> None:
    dashboard_schema = Path(
        "src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-remediation-closure-operations-dashboard-public.example.json"
    )

    assert dashboard_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert payload["queues"][0]["queue"] == "closure_approval"
    assert payload["approval_bottlenecks"][0]["approver_role"] == "ciso"
    assert payload["post_incident_review_health"]["completion_rate"] == 0.83
    assert payload["recent_closures"][0]["final_status"] == "closed"
    assert payload["evidence"]["dashboard_digest_ref"]
    assert payload["redaction"]["payload_handling"] == "remediation_closure_operations_metadata_only"
    assert payload["enterprise_boundaries"]["slo_evaluator"] == "requires_cavra_enterprise"


def test_aispm_report_remediation_closure_executive_digest_contract_matches_schema() -> None:
    digest_schema = Path(
        "src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json"
    )
    contract = build_aispm_report_remediation_closure_executive_digest_contract()

    assert digest_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(digest_schema.read_text(encoding="utf-8")),
    )
    assert contract["digest"]["status"] == "attention_required"
    assert contract["executive_summary"]["closure_readiness"] == "attention_required"
    assert contract["metrics"]["closure_rate"] == 0.82
    assert contract["audit_readiness"]["auditor_ready"] is False
    assert contract["distribution"]["approval_required"] is True
    assert contract["controls"]["executive_approval_required"] is True
    assert contract["redaction"]["board_member_identity_included"] is False
    assert contract["enterprise_boundaries"]["digest_renderer"] == "requires_cavra_enterprise"


def test_aispm_report_remediation_closure_executive_digest_sample_matches_schema() -> None:
    digest_schema = Path(
        "src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-remediation-closure-executive-digest-public.example.json"
    )

    assert digest_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(digest_schema.read_text(encoding="utf-8")),
    )
    assert "board" in payload["digest"]["audiences"]
    assert payload["risk_summary"]["residual_risk_level"] == "medium"
    assert payload["remediation_status"]["closure_slo_status"] == "degraded"
    assert payload["board_talking_points"]
    assert "signed_json" in payload["distribution"]["formats"]
    assert payload["evidence"]["operations_dashboard_ref"]
    assert payload["redaction"]["payload_handling"] == "remediation_closure_executive_digest_metadata_only"
    assert payload["enterprise_boundaries"]["board_pack_renderer"] == "requires_cavra_enterprise"


def test_aispm_report_remediation_closure_digest_distribution_contract_matches_schema() -> None:
    distribution_schema = Path(
        "src/cavra/schemas/aispm-report-remediation-closure-digest-distribution.schema.json"
    )
    contract = build_aispm_report_remediation_closure_digest_distribution_contract()

    assert distribution_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(distribution_schema.read_text(encoding="utf-8")),
    )
    assert contract["distribution"]["status"] == "approval_pending"
    assert contract["approval"]["required_before_send"] is True
    assert contract["recipient_governance"]["recipient_addresses_redacted"] is True
    assert contract["delivery_status"][1]["status"] == "blocked_pending_approval"
    assert contract["controls"]["immutable_send_evidence_required"] is True
    assert contract["redaction"]["recipient_addresses_included"] is False
    assert contract["enterprise_boundaries"]["send_worker"] == "requires_cavra_enterprise"


def test_aispm_report_remediation_closure_digest_distribution_sample_matches_schema() -> None:
    distribution_schema = Path(
        "src/cavra/schemas/aispm-report-remediation-closure-digest-distribution.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-remediation-closure-digest-distribution-public.example.json"
    )

    assert distribution_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(distribution_schema.read_text(encoding="utf-8")),
    )
    assert payload["approval"]["status"] == "pending"
    assert "email" in payload["delivery_plan"]["delivery_modes"]
    assert payload["send_evidence"]["distribution_digest_ref"]
    assert (
        payload["redaction"]["payload_handling"]
        == "remediation_closure_digest_distribution_metadata_only"
    )
    assert payload["enterprise_boundaries"]["delivery_audit_store"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_validation_packet_contract_matches_schema() -> None:
    packet_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json"
    )
    contract = build_aispm_report_center_trial_validation_packet_contract()

    assert packet_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(packet_schema.read_text(encoding="utf-8")),
    )
    assert contract["validation_summary"]["status"] == "ready_for_evaluator_review"
    assert contract["validation_summary"]["passed_paths"] == 10
    assert contract["package_under_test"]["source_included"] is False
    assert contract["controls"]["approval_before_send_verified"] is True
    assert contract["redaction"]["source_code_included"] is False
    assert contract["enterprise_boundaries"]["trial_license_service"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_validation_packet_sample_matches_schema() -> None:
    packet_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json"
    )

    assert packet_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(packet_schema.read_text(encoding="utf-8")),
    )
    path_ids = {item["path_id"] for item in payload["validation_paths"]}
    assert "setup_wizard" in path_ids
    assert "executive_digest_distribution" in path_ids
    assert "revocation_and_retention" in path_ids
    assert payload["controls"]["license_validated"] is True
    assert payload["redaction"]["payload_handling"] == "report_center_trial_validation_metadata_only"
    assert payload["enterprise_boundaries"]["digest_distribution_worker"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_operator_dashboard_contract_matches_schema() -> None:
    dashboard_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json"
    )
    contract = build_aispm_report_center_trial_operator_dashboard_readiness_contract()

    assert dashboard_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert contract["dashboard"]["status"] == "ready_for_operator_review"
    assert contract["validation_rollup"]["handoff_ready"] is True
    assert contract["approval_blockers"] == []
    assert contract["operator_actions"][1]["requires_approval"] is True
    assert contract["evaluator_handoff"]["package_access_state"] == "ready"
    assert contract["redaction"]["evaluator_identity_included"] is False
    assert contract["enterprise_boundaries"]["operator_dashboard_api"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_operator_dashboard_sample_matches_schema() -> None:
    dashboard_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json"
    )

    assert dashboard_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(dashboard_schema.read_text(encoding="utf-8")),
    )
    assert payload["validation_rollup"]["passed_paths"] == 10
    assert payload["path_status"][8]["operator_state"] == "review_recommended"
    assert payload["evidence_links"][0]["status"] == "available"
    assert payload["evaluator_handoff"]["support_state"] == "operator_review_pending"
    assert payload["redaction"]["payload_handling"] == "report_center_trial_operator_dashboard_metadata_only"
    assert payload["enterprise_boundaries"]["support_queue"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_operator_api_view_model_contract_matches_schema() -> None:
    api_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json"
    )
    contract = build_aispm_report_center_trial_operator_api_view_model_contract()

    assert api_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(api_schema.read_text(encoding="utf-8")),
    )
    endpoint_ids = {endpoint["endpoint_id"] for endpoint in contract["api_surface"]["endpoints"]}
    assert "get-dashboard" in endpoint_ids
    assert "approve-handoff" in endpoint_ids
    assert contract["view_model"]["route"] == "/operator/report-center/trial"
    assert contract["controls"]["csrf_protection_required"] is True
    assert contract["redaction"]["operator_identity_included"] is False
    assert contract["enterprise_boundaries"]["operator_session_store"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_operator_api_view_model_sample_matches_schema() -> None:
    api_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json"
    )

    assert api_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(api_schema.read_text(encoding="utf-8")),
    )
    assert payload["api_surface"]["auth_required"] is True
    assert payload["view_model"]["sections"][0]["section_id"] == "validation_rollup"
    assert payload["view_model"]["primary_actions"][1]["endpoint_id"] == "approve-handoff"
    assert payload["action_state_machine"]["transitions"][1]["trigger"] == "approve_evaluator_handoff"
    assert payload["redaction"]["payload_handling"] == "report_center_trial_operator_api_metadata_only"
    assert payload["enterprise_boundaries"]["audit_store"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_evaluator_handoff_packet_contract_matches_schema() -> None:
    handoff_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json"
    )
    contract = build_aispm_report_center_trial_evaluator_handoff_packet_contract()

    assert handoff_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(handoff_schema.read_text(encoding="utf-8")),
    )
    assert contract["evaluator_experience"]["state"] == "ready_for_evaluator"
    assert contract["package_access"]["access_status"] == "ready"
    assert contract["package_access"]["download_urls_included"] is False
    assert contract["license_status"]["status"] == "active"
    assert contract["revocation"]["blocked_after_revocation"] is True
    assert contract["redaction"]["license_key_included"] is False
    assert contract["enterprise_boundaries"]["trial_portal"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_evaluator_handoff_packet_sample_matches_schema() -> None:
    handoff_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-center-trial-evaluator-handoff-packet-public.example.json"
    )

    assert handoff_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(handoff_schema.read_text(encoding="utf-8")),
    )
    step_ids = {step["step_id"] for step in payload["evaluator_experience"]["steps"]}
    assert "pull-trial-package" in step_ids
    assert payload["package_access"]["image_ref_redacted"] is True
    assert payload["license_status"]["license_key_included"] is False
    assert payload["support"]["channels"][0]["contact_detail_included"] is False
    assert payload["redaction"]["payload_handling"] == "report_center_trial_evaluator_handoff_metadata_only"
    assert payload["enterprise_boundaries"]["revocation_service"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_revocation_expiry_evidence_contract_matches_schema() -> None:
    revocation_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json"
    )
    contract = build_aispm_report_center_trial_revocation_expiry_evidence_contract()

    assert revocation_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(revocation_schema.read_text(encoding="utf-8")),
    )
    assert contract["revocation_expiry"]["state"] == "revoked"
    assert contract["access_state"]["license_state"] == "revoked"
    assert contract["operator_summary"]["blocked_checks"] == 5
    assert contract["controls"]["license_block_verified"] is True
    assert contract["redaction"]["download_urls_included"] is False
    assert contract["enterprise_boundaries"]["revocation_service"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_revocation_expiry_evidence_sample_matches_schema() -> None:
    revocation_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-center-trial-revocation-expiry-evidence-public.example.json"
    )

    assert revocation_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(revocation_schema.read_text(encoding="utf-8")),
    )
    check_ids = {check["check_id"] for check in payload["blocked_access_checks"]}
    assert "license_validation" in check_ids
    assert "package_pull" in check_ids
    assert "support_handoff" in check_ids
    assert payload["operator_summary"]["evidence_ready"] is True
    assert payload["redaction"]["payload_handling"] == "report_center_trial_revocation_expiry_metadata_only"
    assert payload["enterprise_boundaries"]["audit_store"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_lab_notebook_outline_contract_matches_schema() -> None:
    notebook_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json"
    )
    contract = build_aispm_report_center_trial_lab_notebook_outline_contract()

    assert notebook_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(notebook_schema.read_text(encoding="utf-8")),
    )
    assert contract["notebook"]["publication_target"] == "github_wiki"
    assert contract["notebook"]["public_safe"] is True
    assert contract["publishing"]["requires_screenshots"] is True
    assert contract["controls"]["enterprise_source_excluded"] is True
    assert contract["redaction"]["source_code_included"] is False
    assert contract["enterprise_boundaries"]["wiki_publication_workflow"] == "public_docs_only"


def test_aispm_report_center_trial_lab_notebook_outline_sample_matches_schema() -> None:
    notebook_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-center-trial-lab-notebook-outline-public.example.json"
    )

    assert notebook_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(notebook_schema.read_text(encoding="utf-8")),
    )
    chapter_ids = {chapter["chapter_id"] for chapter in payload["chapters"]}
    assert "trial-access" in chapter_ids
    assert "closeout" in chapter_ids
    lab_ids = {lab["lab_id"] for lab in payload["labs"]}
    assert "lab-revocation-expiry" in lab_ids
    assert payload["visual_assets"][0]["public_safe"] is True
    assert payload["redaction"]["payload_handling"] == "report_center_trial_lab_notebook_outline_metadata_only"
    assert payload["enterprise_boundaries"]["private_lab_fixtures"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_lab_notebook_publication_readiness_contract_matches_schema() -> None:
    readiness_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json"
    )
    contract = build_aispm_report_center_trial_lab_notebook_publication_readiness_contract()

    assert readiness_schema.is_file()
    jsonschema.validate(
        contract,
        schema=json.loads(readiness_schema.read_text(encoding="utf-8")),
    )
    assert contract["publication_readiness"]["target"] == "github_wiki"
    assert contract["publication_readiness"]["requires_no_private_artifacts"] is True
    assert contract["controls"]["wiki_nav_required"] is True
    assert contract["controls"]["link_health_required"] is True
    assert contract["redaction"]["download_urls_included"] is False
    assert contract["enterprise_boundaries"]["private_screenshot_capture"] == "requires_cavra_enterprise"


def test_aispm_report_center_trial_lab_notebook_publication_readiness_sample_matches_schema() -> None:
    readiness_schema = Path(
        "src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json"
    )
    sample = Path(
        "examples/aispm/enterprise-report-center-trial-lab-notebook-publication-readiness-public.example.json"
    )

    assert readiness_schema.is_file()
    assert sample.is_file()
    payload = json.loads(sample.read_text(encoding="utf-8"))
    jsonschema.validate(
        payload,
        schema=json.loads(readiness_schema.read_text(encoding="utf-8")),
    )
    assert payload["outline_contract_ref"].endswith("trial-lab-notebook-outline.schema.json")
    assert {page["page_id"] for page in payload["wiki_pages"]} == {
        "trial-lab-overview",
        "trial-access-flow",
        "trial-closeout",
    }
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    for page in payload["wiki_pages"]:
        source_ref = Path(page["source_ref"])
        assert source_ref.is_file()
        assert source_ref.name in wiki_home
    assert {asset["asset_type"] for asset in payload["visual_assets"]} >= {
        "screenshot",
        "diagram",
        "flow_chart",
    }
    assert payload["redaction"]["payload_handling"] == (
        "report_center_trial_lab_notebook_publication_readiness_metadata_only"
    )
    assert payload["enterprise_boundaries"]["wiki_publication_workflow"] == "public_docs_only"


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
