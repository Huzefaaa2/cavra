from __future__ import annotations

import json
import textwrap
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cavra.go_backend import (
    GO_BACKEND_DISABLED,
    GO_BACKEND_ENFORCE,
    GO_BACKEND_PROMOTED,
    GO_BACKEND_SHADOW,
    GoBackendConfig,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_retry,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert,
    acknowledge_go_rollback_drill_notification,
    build_go_rollback_drill_acknowledgement_audit_delivery_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_closure_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook,
    build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closure_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_decision_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_package,
    build_go_rollback_drill_acknowledgement_audit_package_metadata,
    build_go_rollback_drill_notification_ack_metadata,
    build_go_rollback_drill_notification_dashboard,
    build_go_rollback_drill_notification_escalation_plan,
    build_go_rollback_drill_notification_escalation_plan_metadata,
    build_go_rollback_drill_notification_event,
    build_go_rollback_drill_notification_plan_metadata,
    build_go_rollback_drill_notification_plan,
    build_go_rollback_drill_routing_suppression_trend,
    build_go_rollback_drill_routing_suppression_trend_metadata,
    close_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery,
    decide_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval,
    filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_history,
    filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_history,
    filter_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_history,
    filter_go_rollback_drill_acknowledgement_audit_delivery_worker_history,
    filter_go_rollback_drill_notification_history,
    filter_go_rollback_drill_routing_history,
    evaluate_with_go_pilot,
    go_backend_config_from_env,
    go_backend_readiness_report,
    go_deployment_readiness_report,
    go_promotion_readiness_report,
    go_rollback_readiness_report,
    go_rollback_drill_history_report,
    go_rollback_drill_schedule_report,
    go_rollback_rehearsal_report,
)


def test_go_backend_defaults_to_disabled(monkeypatch) -> None:
    monkeypatch.delenv("CAVRA_GO_BACKEND_MODE", raising=False)

    config = go_backend_config_from_env()
    report = go_backend_readiness_report(config)

    assert config.mode == GO_BACKEND_DISABLED
    assert report["status"] == "disabled"
    assert next(item for item in report["checks"] if item["id"] == "python_fallback")["status"] == "pass"


def test_go_backend_readiness_requires_binary_and_policy(tmp_path: Path) -> None:
    config = GoBackendConfig(
        mode=GO_BACKEND_SHADOW,
        runtime_path=str(tmp_path / "missing-runtime"),
        policy_path=str(tmp_path / "missing-policy.json"),
    )

    report = go_backend_readiness_report(config)

    assert report["status"] == "needs_attention"
    assert next(item for item in report["checks"] if item["id"] == "go_runtime_binary")["status"] == "warn"
    assert next(item for item in report["checks"] if item["id"] == "go_runtime_policy")["status"] == "warn"


def test_go_backend_shadow_uses_python_when_go_matches(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    request = {
        "action_type": "execute_command",
        "target": "terraform plan",
        "policy_pack": "cavra-ai-agent-baseline",
    }

    result = evaluate_with_go_pilot(
        request,
        config=GoBackendConfig(mode=GO_BACKEND_SHADOW, runtime_path=str(runtime), policy_path=str(policy)),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is False
    assert result["parity_match"] is True
    assert result["go_decision"]["decision"] == "allow"


def test_go_backend_enforce_selects_go_when_parity_matches(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(mode=GO_BACKEND_ENFORCE, runtime_path=str(runtime), policy_path=str(policy)),
    )

    assert result["selected_backend"] == "go"
    assert result["effective_decision"] == result["go_decision"]


def test_go_backend_falls_back_when_go_diverges(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="block", rule_id="commands.block", severity="critical")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(mode=GO_BACKEND_ENFORCE, runtime_path=str(runtime), policy_path=str(policy)),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is True
    assert result["fallback_reason"] == "go decision diverged from Python parity gate"
    assert result["effective_decision"]["decision"] == "allow"


def test_go_deployment_readiness_reports_not_configured_when_disabled() -> None:
    report = go_deployment_readiness_report(GoBackendConfig(mode=GO_BACKEND_DISABLED))

    assert report["status"] == "not_configured"
    assert next(item for item in report["checks"] if item["id"] == "go_deployment_metadata_configured")["status"] == "pass"


def test_go_deployment_readiness_requires_metadata_when_enabled() -> None:
    report = go_deployment_readiness_report(GoBackendConfig(mode=GO_BACKEND_SHADOW))

    assert report["status"] == "needs_attention"
    assert next(item for item in report["checks"] if item["id"] == "go_deployment_metadata_configured")["status"] == "warn"


def test_go_deployment_readiness_accepts_ci_runner_and_workstation_metadata(tmp_path: Path) -> None:
    _write_deployment_metadata(tmp_path)

    report = go_deployment_readiness_report(
        GoBackendConfig(mode=GO_BACKEND_SHADOW, package_dir=str(tmp_path))
    )

    assert report["status"] == "ready"
    assert report["ci_runner_targets"][0]["deployment_target"] == "github-actions-linux-amd64-runner"
    assert report["workstation_targets"][0]["deployment_target"] == "linux-systemd-amd64-workstation"
    assert report["channels"] == ["stable"]


def test_go_promotion_readiness_is_not_requested_by_default() -> None:
    report = go_promotion_readiness_report(GoBackendConfig(mode=GO_BACKEND_DISABLED))

    assert report["status"] == "not_requested"
    assert next(item for item in report["checks"] if item["id"] == "go_promotion_requested")["status"] == "warn"


def test_go_promotion_readiness_requires_audited_evidence(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)

    report = go_promotion_readiness_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
        )
    )

    assert report["status"] == "needs_attention"
    assert next(item for item in report["checks"] if item["id"] == "go_parity_evidence")["status"] == "warn"


def test_go_promotion_readiness_accepts_valid_audited_evidence(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)
    promotion = _write_promotion_evidence(tmp_path)

    report = go_promotion_readiness_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
            promotion_evidence_path=str(promotion),
        )
    )

    assert report["status"] == "ready"
    assert report["evidence"]["approval_id"] == "apr_go_backend_promotion"


def test_go_rollback_readiness_is_not_requested_by_default() -> None:
    report = go_rollback_readiness_report(GoBackendConfig(mode=GO_BACKEND_DISABLED))

    assert report["status"] == "not_requested"
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_requested")["status"] == "warn"


def test_go_rollback_readiness_requires_approved_plan() -> None:
    report = go_rollback_readiness_report(GoBackendConfig(mode=GO_BACKEND_PROMOTED))

    assert report["status"] == "needs_attention"
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_plan")["status"] == "warn"


def test_go_rollback_readiness_accepts_valid_plan(tmp_path: Path) -> None:
    rollback = _write_rollback_plan(tmp_path)

    report = go_rollback_readiness_report(
        GoBackendConfig(mode=GO_BACKEND_PROMOTED, rollback_plan_path=str(rollback))
    )

    assert report["status"] == "ready"
    assert report["rollback"]["target_mode"] == GO_BACKEND_DISABLED
    assert report["rollback"]["approval_id"] == "apr_go_backend_rollback"


def test_go_rollback_rehearsal_is_not_requested_by_default() -> None:
    report = go_rollback_rehearsal_report(GoBackendConfig(mode=GO_BACKEND_DISABLED))

    assert report["status"] == "not_requested"
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_rehearsal_requested")["status"] == "warn"


def test_go_rollback_rehearsal_requires_evidence_when_promoted(tmp_path: Path) -> None:
    rollback = _write_rollback_plan(tmp_path)

    report = go_rollback_rehearsal_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_plan_path=str(rollback),
            rollback_rehearsal_path=str(tmp_path / "missing-rehearsal.json"),
        )
    )

    assert report["status"] == "needs_attention"
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_rehearsal_evidence")["status"] == "warn"


def test_go_rollback_rehearsal_accepts_valid_evidence(tmp_path: Path) -> None:
    rollback = _write_rollback_plan(tmp_path)
    rehearsal = _write_rollback_rehearsal(tmp_path)

    report = go_rollback_rehearsal_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_plan_path=str(rollback),
            rollback_rehearsal_path=str(rehearsal),
        )
    )

    assert report["status"] == "ready"
    assert report["rehearsal"]["recovery_minutes"] == 6
    assert report["rehearsal"]["plan_approval_id"] == "apr_go_backend_rollback"


def test_go_rollback_drill_history_is_not_requested_by_default() -> None:
    report = go_rollback_drill_history_report(GoBackendConfig(mode=GO_BACKEND_DISABLED))

    assert report["status"] == "not_requested"
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_drill_history_requested")["status"] == "warn"


def test_go_rollback_drill_history_requires_valid_history_when_promoted(tmp_path: Path) -> None:
    report = go_rollback_drill_history_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(tmp_path / "missing-drills.json"),
        )
    )

    assert report["status"] == "needs_attention"
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_drill_history_file")["status"] == "warn"


def test_go_rollback_drill_history_accepts_latest_fresh_drill(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)

    report = go_rollback_drill_history_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_max_age_days=90,
        )
    )

    assert report["status"] == "ready"
    assert report["history"]["latest_drill_id"] == "drill_go_backend_python_fallback"
    assert report["history"]["latest_target_mode"] == GO_BACKEND_DISABLED


def test_go_rollback_drill_schedule_is_not_requested_by_default() -> None:
    report = go_rollback_drill_schedule_report(GoBackendConfig(mode=GO_BACKEND_DISABLED))

    assert report["status"] == "not_requested"
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_drill_schedule_requested")["status"] == "warn"


def test_go_rollback_drill_schedule_detects_stale_drills(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) - timedelta(days=1))

    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )

    assert report["status"] == "needs_attention"
    assert report["schedule"]["stale"] is True
    assert next(item for item in report["checks"] if item["id"] == "go_rollback_drill_schedule_not_stale")["status"] == "warn"


def test_go_rollback_drill_schedule_accepts_due_soon_notification_routes(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))

    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
            rollback_drill_due_soon_days=14,
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="slack")
    event = build_go_rollback_drill_notification_event(report, generated_by="test")

    assert report["status"] == "due_soon"
    assert report["schedule"]["notification_providers"] == ["slack", "teams"]
    assert plan["selected_providers"] == ["slack"]
    assert event["event_type"] == "cavra.go_backend.rollback_drill.notification"
    assert event["alert_level"] == "warning"


def test_go_rollback_drill_notification_plan_applies_owner_routes_and_maintenance(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    now = datetime.now(timezone.utc)
    policy = {
        "owner_routes": {
            "release-governance": {
                "providers": ["slack", "teams"],
                "acknowledgement_minutes": 15,
                "escalation_owner": "platform-lead",
            }
        },
        "maintenance_windows": [
            {
                "window_id": "change-freeze",
                "start_at": (now - timedelta(minutes=5)).isoformat(),
                "end_at": (now + timedelta(minutes=30)).isoformat(),
                "providers": ["slack"],
                "owners": ["release-governance"],
                "reason": "production change freeze",
            }
        ],
    }
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
            rollback_drill_due_soon_days=14,
        )
    )

    plan = build_go_rollback_drill_notification_plan(report, routing_policy=policy, now=now)

    assert plan["selected_providers"] == ["teams"]
    assert plan["maintenance_suppressed_count"] == 1
    assert plan["deliverable_route_count"] == 1
    assert next(route for route in plan["route_decisions"] if route["provider"] == "slack")["action"] == "suppress"
    teams = next(route for route in plan["route_decisions"] if route["provider"] == "teams")
    assert teams["acknowledgement_minutes"] == 15
    assert teams["escalation_owner"] == "platform-lead"


def test_go_rollback_drill_routing_history_and_suppression_trends(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    now = datetime.now(timezone.utc)
    policy = {
        "owner_routes": {
            "release-governance": {
                "providers": ["slack", "teams"],
                "acknowledgement_minutes": 15,
                "escalation_owner": "platform-lead",
            }
        },
        "maintenance_windows": [
            {
                "window_id": "change-freeze",
                "start_at": (now - timedelta(minutes=5)).isoformat(),
                "end_at": (now + timedelta(minutes=30)).isoformat(),
                "providers": ["slack"],
                "owners": ["release-governance"],
                "reason": "production change freeze",
            }
        ],
    }
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
            rollback_drill_due_soon_days=14,
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, routing_policy=policy, now=now)
    metadata = build_go_rollback_drill_notification_plan_metadata(plan)

    history = filter_go_rollback_drill_routing_history(
        [metadata],
        owner="platform-lead",
        category="maintenance_window",
    )
    trend = build_go_rollback_drill_routing_suppression_trend([metadata], owner="release-governance")
    trend_metadata = build_go_rollback_drill_routing_suppression_trend_metadata(trend)

    assert history["total"] == 1
    assert history["items"][0]["provider"] == "slack"
    assert history["items"][0]["maintenance_window_id"] == "change-freeze"
    assert trend["suppression_event_count"] == 1
    assert trend["category_counts"]["maintenance_window"] == 1
    assert trend["maintenance_suppressed_count"] == 1
    assert trend_metadata["metadata_kind"] == "go-backend-rollback-drill-routing-suppression-trend"


def test_go_rollback_drill_notification_plan_applies_owner_calendar(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    now = datetime.now(timezone.utc)
    policy = {
        "owner_routes": {"release-governance": {"providers": ["slack"]}},
        "owner_calendars": {
            "release-governance": {
                "unavailable_windows": [
                    {
                        "start_at": (now - timedelta(minutes=5)).isoformat(),
                        "end_at": (now + timedelta(minutes=30)).isoformat(),
                        "reason": "regional holiday",
                    }
                ]
            }
        },
    }
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
            rollback_drill_due_soon_days=14,
        )
    )

    plan = build_go_rollback_drill_notification_plan(report, routing_policy=policy, now=now)

    assert plan["selected_providers"] == []
    assert plan["calendar_suppressed_count"] == 1
    assert plan["route_decisions"][0]["reason"] == "regional holiday"


def test_go_rollback_drill_notification_acknowledgement_and_dashboard(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="slack")
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    dashboard_before = build_go_rollback_drill_notification_dashboard([plan_metadata])
    acknowledgement = acknowledge_go_rollback_drill_notification(
        "go_backend_python_fallback_monthly",
        provider="slack",
        acknowledged_by="release-manager",
        plan_id=plan["plan_id"],
    )
    ack_metadata = build_go_rollback_drill_notification_ack_metadata(acknowledgement)
    dashboard_after = build_go_rollback_drill_notification_dashboard([plan_metadata, ack_metadata])
    history = filter_go_rollback_drill_notification_history([plan_metadata, ack_metadata], provider="slack")

    assert dashboard_before["outstanding_acknowledgement_count"] == 1
    assert ack_metadata["metadata_kind"] == "go-backend-rollback-drill-notification-ack"
    assert dashboard_after["outstanding_acknowledgement_count"] == 0
    assert history["total"] == 2


def test_go_rollback_drill_acknowledgement_audit_package_summarizes_routes(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    policy = {
        "owner_routes": {
            "release-governance": {"providers": ["slack"], "acknowledgement_minutes": 30},
            "platform-operations": {"providers": ["teams"], "acknowledgement_minutes": 60},
        }
    }
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, routing_policy=policy)
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    acknowledgement = acknowledge_go_rollback_drill_notification(
        "go_backend_python_fallback_monthly",
        provider="slack",
        acknowledged_by="release-manager",
        plan_id=plan["plan_id"],
        external_ref="CHG-123",
        notes="Reviewed during release governance.",
    )
    ack_metadata = build_go_rollback_drill_notification_ack_metadata(acknowledgement)

    package = build_go_rollback_drill_acknowledgement_audit_package(
        [plan_metadata, ack_metadata],
        owner="release-governance",
        generated_by="test",
    )
    metadata = build_go_rollback_drill_acknowledgement_audit_package_metadata(package)

    assert package["route_count"] == 1
    assert package["acknowledged_count"] == 1
    assert package["outstanding_count"] == 0
    assert package["routes"][0]["acknowledged_by"] == "release-manager"
    assert package["routes"][0]["external_ref"] == "CHG-123"
    assert metadata["metadata_kind"] == "go-backend-rollback-drill-acknowledgement-audit-package"


def test_go_rollback_drill_acknowledgement_audit_delivery_redacts_route_notes(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="slack")
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    acknowledgement = acknowledge_go_rollback_drill_notification(
        "go_backend_python_fallback_monthly",
        provider="slack",
        acknowledged_by="release-manager",
        plan_id=plan["plan_id"],
        notes="Internal change-room context must stay out of connector payloads.",
    )
    ack_metadata = build_go_rollback_drill_notification_ack_metadata(acknowledgement)
    package = build_go_rollback_drill_acknowledgement_audit_package(
        [plan_metadata, ack_metadata],
        generated_by="test",
    )
    delivery_plan = build_go_rollback_drill_acknowledgement_audit_delivery_plan(
        package,
        requested_provider="splunk,jira",
        available_providers=["splunk", "jira", "webhook"],
        generated_by="test",
        cadence="hourly",
        schedule_ref="release-governance-hourly",
    )
    event = build_go_rollback_drill_acknowledgement_audit_delivery_event(package, delivery_plan, generated_by="test")
    metadata = build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata(delivery_plan)

    assert delivery_plan["selected_providers"] == ["splunk", "jira"]
    assert delivery_plan["cadence"] == "hourly"
    assert event["event_type"] == "cavra.go_backend.rollback_drill.acknowledgement_audit_delivery"
    assert "notes" not in event["routes"][0]
    assert event["provider_payloads"]["splunk"]["sourcetype"] == "cavra:rollback_drill_ack_audit"
    assert metadata["metadata_kind"] == "go-backend-rollback-drill-acknowledgement-audit-delivery-plan"


def test_go_rollback_drill_acknowledgement_audit_delivery_history_filters_and_dashboard(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="slack")
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    package = build_go_rollback_drill_acknowledgement_audit_package([plan_metadata], generated_by="test")
    package_metadata = build_go_rollback_drill_acknowledgement_audit_package_metadata(package)
    delivery_plan = build_go_rollback_drill_acknowledgement_audit_delivery_plan(
        package,
        requested_provider="splunk",
        available_providers=["splunk"],
        generated_by="test",
        cadence="hourly",
    )
    delivery_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata(delivery_plan)
    connector_metadata = {
        "session_id": "connector-delivery-1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit",
        "audit_id": package["audit_id"],
        "delivery_id": delivery_plan["delivery_id"],
        "event_id": delivery_plan["delivery_id"],
        "delivery_success": False,
        "providers": ["splunk"],
        "failed_providers": ["splunk"],
    }
    items = [plan_metadata, package_metadata, delivery_metadata, connector_metadata]

    source_history = filter_go_rollback_drill_notification_history(
        items,
        connector_delivery_source="go_backend_rollback_drill_acknowledgement_audit",
    )
    failed_history = filter_go_rollback_drill_notification_history(
        items,
        connector_delivery_source="go_backend_rollback_drill_acknowledgement_audit",
        delivery_success=False,
    )
    cadence_history = filter_go_rollback_drill_notification_history(items, cadence="hourly")
    audit_id_history = filter_go_rollback_drill_notification_history(items, audit_id=package["audit_id"])
    provider_history = filter_go_rollback_drill_notification_history(items, provider="splunk")
    dashboard = build_go_rollback_drill_notification_dashboard(items)

    assert source_history["total"] == 3
    assert failed_history["total"] == 1
    assert cadence_history["items"][0]["delivery_id"] == delivery_plan["delivery_id"]
    assert audit_id_history["total"] == 3
    assert provider_history["total"] == 2
    assert dashboard["acknowledgement_audit_delivery_plan_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_count"] == 1
    assert dashboard["failed_acknowledgement_audit_delivery_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_health"] == "critical"


def test_go_rollback_drill_acknowledgement_audit_delivery_retry_worker(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="webhook")
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    package = build_go_rollback_drill_acknowledgement_audit_package([plan_metadata], generated_by="test")
    package_metadata = build_go_rollback_drill_acknowledgement_audit_package_metadata(package)
    delivery_plan = build_go_rollback_drill_acknowledgement_audit_delivery_plan(
        package,
        requested_provider="webhook",
        available_providers=["webhook"],
        generated_by="test",
        cadence="hourly",
    )
    delivery_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata(delivery_plan)
    failed_at = datetime.now(timezone.utc) - timedelta(hours=2)
    connector_metadata = {
        "session_id": "connector-delivery-retry",
        "created_at": failed_at.isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit",
        "audit_id": package["audit_id"],
        "delivery_id": delivery_plan["delivery_id"],
        "event_id": delivery_plan["delivery_id"],
        "delivery_success": False,
        "providers": ["webhook"],
        "failed_providers": ["webhook"],
        "status_codes": [503],
    }
    items = [plan_metadata, package_metadata, delivery_metadata, connector_metadata]

    retry_plan = build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan(
        items,
        policy={"max_retry_attempts": 3, "retry_delay_minutes": 15},
        generated_by="test",
        now=datetime.now(timezone.utc),
    )
    retry_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan_metadata(retry_plan)
    worker_run = build_go_rollback_drill_acknowledgement_audit_delivery_worker_run(
        [*items, retry_metadata],
        retry_policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
        schedule={"interval_minutes": 30, "cadence": "every_30_minutes"},
        generated_by="test",
        dry_run=True,
        max_retry_deliveries=2,
        now=datetime.now(timezone.utc),
    )
    worker_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_worker_run_metadata(worker_run)
    history = filter_go_rollback_drill_acknowledgement_audit_delivery_worker_history(
        [*items, retry_metadata, worker_metadata],
        dry_run=True,
    )
    dashboard = build_go_rollback_drill_acknowledgement_audit_delivery_worker_dashboard(
        [*items, retry_metadata, worker_metadata]
    )
    notification_dashboard = build_go_rollback_drill_notification_dashboard([*items, retry_metadata, worker_metadata])

    assert retry_plan["retryable_count"] == 1
    assert retry_plan["retry_decisions"][0]["action"] == "retry"
    assert retry_metadata["metadata_kind"] == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan"
    assert worker_run["dry_run"] is True
    assert worker_run["summary"]["selected_retry_count"] == 1
    assert worker_run["selected_retries"][0]["provider"] == "webhook"
    assert worker_metadata["metadata_kind"] == "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run"
    assert history["total"] == 1
    assert dashboard["run_count"] == 1
    assert dashboard["dry_run_count"] == 1
    assert dashboard["retryable_count"] == 1
    assert notification_dashboard["acknowledgement_audit_delivery_retry_plan_count"] == 1
    assert notification_dashboard["acknowledgement_audit_delivery_worker_run_count"] == 1


def test_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alerts_and_retry_acks(
    tmp_path: Path,
) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="webhook")
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    package = build_go_rollback_drill_acknowledgement_audit_package([plan_metadata], generated_by="test")
    package_metadata = build_go_rollback_drill_acknowledgement_audit_package_metadata(package)
    delivery_plan = build_go_rollback_drill_acknowledgement_audit_delivery_plan(
        package,
        requested_provider="webhook",
        available_providers=["webhook"],
        generated_by="test",
    )
    delivery_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata(delivery_plan)
    connector_metadata = {
        "session_id": "connector-delivery-retry-health",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit",
        "audit_id": package["audit_id"],
        "delivery_id": delivery_plan["delivery_id"],
        "event_id": delivery_plan["delivery_id"],
        "delivery_success": False,
        "providers": ["webhook"],
        "failed_providers": ["webhook"],
    }
    items = [plan_metadata, package_metadata, delivery_metadata, connector_metadata]
    retry_plan = build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan(
        items,
        policy={"max_retry_attempts": 3, "retry_delay_minutes": 15},
        generated_by="test",
        now=datetime.now(timezone.utc),
    )
    retry_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan_metadata(retry_plan)
    worker_run = build_go_rollback_drill_acknowledgement_audit_delivery_worker_run(
        [*items, retry_metadata],
        retry_policy={"max_retry_attempts": 3, "retry_delay_minutes": 15},
        schedule={"interval_minutes": 30, "cadence": "every_30_minutes"},
        generated_by="test",
        dry_run=True,
        now=datetime.now(timezone.utc),
    )
    worker_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_worker_run_metadata(worker_run)
    health = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health(
        [*items, retry_metadata, worker_metadata],
        expected_interval_minutes=30,
        stale_metadata_minutes=120,
        now=datetime.now(timezone.utc),
    )
    health_alert_plan = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan(
        health,
        requested_provider="webhook",
        available_providers=["webhook"],
        generated_by="test",
        force=True,
    )
    health_alert_event = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_event(
        health,
        generated_by="test",
    )
    health_alert_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan_metadata(
        health_alert_plan
    )
    health_ack = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert(
        health["health_id"],
        provider="webhook",
        acknowledged_by="release-manager",
        plan_id=health_alert_plan["plan_id"],
    )
    health_ack_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_ack_metadata(
        health_ack
    )
    retry_ack = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_retry(
        retry_plan["retry_plan_id"],
        provider="webhook",
        acknowledged_by="release-manager",
        delivery_id=delivery_plan["delivery_id"],
        audit_id=package["audit_id"],
    )
    retry_ack_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_retry_ack_metadata(retry_ack)
    alert_history = filter_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_history(
        [health_alert_metadata, health_ack_metadata],
        health_id=health["health_id"],
    )
    alert_dashboard = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_dashboard(
        [health_alert_metadata, health_ack_metadata]
    )
    notification_dashboard = build_go_rollback_drill_notification_dashboard(
        [*items, retry_metadata, worker_metadata, health_alert_metadata, health_ack_metadata, retry_ack_metadata]
    )

    assert health["alert_level"] == "warning"
    assert health["retryable_count"] == 1
    assert health_alert_plan["selected_providers"] == ["webhook"]
    assert health_alert_event["event_type"] == "cavra.go_backend.rollback_drill.acknowledgement_audit_worker_health_alert"
    assert (
        health_alert_metadata["metadata_kind"]
        == "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan"
    )
    assert health_ack_metadata["metadata_kind"].endswith("worker-health-alert-ack")
    assert retry_ack["acknowledgement_state"] == "accepted"
    assert retry_ack_metadata["metadata_kind"] == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-ack"
    assert alert_history["total"] == 2
    assert alert_dashboard["acknowledgement_count"] == 1
    assert notification_dashboard["acknowledgement_audit_delivery_retry_ack_count"] == 1
    assert notification_dashboard["acknowledgement_audit_delivery_worker_health_alert_count"] == 1
    assert notification_dashboard["acknowledgement_audit_delivery_worker_health_alert_ack_count"] == 1


def test_go_rollback_drill_acknowledgement_audit_retry_execution_approvals_and_recovery_playbooks(
    tmp_path: Path,
) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="webhook")
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    package = build_go_rollback_drill_acknowledgement_audit_package([plan_metadata], generated_by="test")
    package_metadata = build_go_rollback_drill_acknowledgement_audit_package_metadata(package)
    delivery_plan = build_go_rollback_drill_acknowledgement_audit_delivery_plan(
        package,
        requested_provider="webhook",
        available_providers=["webhook"],
        generated_by="test",
    )
    delivery_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata(delivery_plan)
    connector_metadata = {
        "session_id": "connector-delivery-approval",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit",
        "audit_id": package["audit_id"],
        "delivery_id": delivery_plan["delivery_id"],
        "event_id": delivery_plan["delivery_id"],
        "delivery_success": False,
        "providers": ["webhook"],
        "failed_providers": ["webhook"],
        "status_codes": [503],
    }
    items = [plan_metadata, package_metadata, delivery_metadata, connector_metadata]
    retry_plan = build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan(
        items,
        policy={"max_retry_attempts": 3, "retry_delay_minutes": 15},
        generated_by="test",
        now=datetime.now(timezone.utc),
    )
    retry_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan_metadata(retry_plan)
    retry_decision = retry_plan["retry_decisions"][0]
    retry_ack = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_retry(
        retry_plan["retry_plan_id"],
        provider="webhook",
        acknowledged_by="release-manager",
        delivery_id=retry_decision["delivery_id"],
        audit_id=retry_decision["audit_id"],
    )
    retry_ack_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_retry_ack_metadata(retry_ack)
    approval_plan = build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan(
        [*items, retry_metadata, retry_ack_metadata],
        generated_by="test",
    )
    approval_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan_metadata(
        approval_plan
    )
    approval_decision = decide_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval(
        approval_plan["approval_plan_id"],
        provider="webhook",
        decided_by="release-manager",
        retry_plan_id=retry_plan["retry_plan_id"],
        delivery_id=retry_decision["delivery_id"],
        audit_id=retry_decision["audit_id"],
        external_ref="CHG-789",
    )
    approval_decision_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_decision_metadata(
            approval_decision
        )
    )
    worker_run = build_go_rollback_drill_acknowledgement_audit_delivery_worker_run(
        [*items, retry_metadata, retry_ack_metadata, approval_metadata, approval_decision_metadata],
        retry_policy={"max_retry_attempts": 3, "retry_delay_minutes": 15},
        generated_by="test",
        dry_run=False,
        max_retry_deliveries=2,
        now=datetime.now(timezone.utc),
    )
    execution_record = build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record(
        worker_run,
        worker_run["selected_retries"][0],
        approval_decision=approval_decision,
        delivery_plan=delivery_plan,
        delivery={"success": True},
        delivery_metadata={
            "session_id": "connector-delivery-live-retry",
            "delivery_success": True,
        },
        executed_by="release-manager",
    )
    execution_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record_metadata(
        execution_record
    )
    playbook = build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook(
        [
            *items,
            retry_metadata,
            retry_ack_metadata,
            approval_metadata,
            approval_decision_metadata,
            execution_metadata,
        ],
        generated_by="test",
        min_failure_count=1,
    )
    playbook_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook_metadata(
        playbook
    )
    closure = close_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery(
        playbook["playbook_id"],
        provider="webhook",
        closed_by="release-manager",
        closure_state="resolved",
        external_ref="INC-123",
        verification_refs=[execution_record["execution_id"]],
    )
    closure_metadata = build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_closure_metadata(
        closure
    )
    retry_recovery_report = build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report(
        [
            *items,
            retry_metadata,
            retry_ack_metadata,
            approval_metadata,
            approval_decision_metadata,
            execution_metadata,
            playbook_metadata,
            closure_metadata,
        ],
        recovery_slo_minutes=120,
        generated_by="test",
    )
    retry_recovery_report_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report_metadata(
            retry_recovery_report
        )
    )
    open_recovery_escalation_plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan(
        [
            *items,
            retry_metadata,
            retry_ack_metadata,
            approval_metadata,
            approval_decision_metadata,
            execution_metadata,
            playbook_metadata,
        ],
        recovery_slo_minutes=1,
        generated_by="test",
        now=datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    open_recovery_escalation_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan_metadata(
            open_recovery_escalation_plan
        )
    )
    open_recovery_escalation_event = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_event(
            open_recovery_escalation_plan,
            generated_by="test",
        )
    )
    executive_report = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report(
        [
            *items,
            retry_metadata,
            retry_ack_metadata,
            approval_metadata,
            approval_decision_metadata,
            execution_metadata,
            playbook_metadata,
        ],
        recovery_slo_minutes=1,
        generated_by="test",
        now=datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    executive_report_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_metadata(
            executive_report
        )
    )
    recovery_escalation_ack = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation(
        open_recovery_escalation_plan["plan_id"],
        provider="webhook",
        acknowledged_by="release-manager",
        acknowledgement_state="accepted",
        external_ref="INC-456",
        escalation_reason=open_recovery_escalation_plan["escalation_routes"][0]["reason"],
    )
    recovery_escalation_ack_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_ack_metadata(
            recovery_escalation_ack
        )
    )
    failed_recovery_escalation_delivery = {
        "session_id": "connector-delivery-recovery-escalation",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation",
        "plan_id": open_recovery_escalation_plan["plan_id"],
        "event_id": open_recovery_escalation_plan["plan_id"],
        "delivery_success": False,
        "providers": ["webhook"],
        "failed_providers": ["webhook"],
        "status_codes": [503],
    }
    recovery_escalation_retry_plan = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan(
            [open_recovery_escalation_metadata, failed_recovery_escalation_delivery],
            policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
        )
    )
    recovery_escalation_retry_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan_metadata(
            recovery_escalation_retry_plan
        )
    )
    executive_schedule_run = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run(
            [
                *items,
                retry_metadata,
                retry_ack_metadata,
                approval_metadata,
                approval_decision_metadata,
                execution_metadata,
                playbook_metadata,
            ],
            recovery_slo_minutes=1,
            generated_by="test",
            schedule={"interval_minutes": 60, "cadence": "hourly"},
            now=datetime.now(timezone.utc) + timedelta(minutes=5),
        )
    )
    executive_schedule_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run_metadata(
            executive_schedule_run
        )
    )
    recovery_escalation_retry_worker_run = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run(
            [
                open_recovery_escalation_metadata,
                recovery_escalation_ack_metadata,
                failed_recovery_escalation_delivery,
            ],
            retry_policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
            dry_run=False,
            max_retry_deliveries=2,
        )
    )
    recovery_escalation_retry_worker_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run_metadata(
            recovery_escalation_retry_worker_run
        )
    )
    recovery_escalation_retry_execution = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record(
            recovery_escalation_retry_worker_run,
            recovery_escalation_retry_worker_run["selected_retries"][0],
            plan=open_recovery_escalation_plan,
            delivery={"success": True, "providers": ["webhook"]},
            delivery_metadata={
                "session_id": "connector-delivery-recovery-escalation-live-retry",
                "delivery_success": True,
            },
            executed_by="release-manager",
        )
    )
    recovery_escalation_retry_execution_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_metadata(
            recovery_escalation_retry_execution
        )
    )
    failed_recovery_escalation_retry_execution = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record(
            recovery_escalation_retry_worker_run,
            recovery_escalation_retry_worker_run["selected_retries"][0],
            plan=open_recovery_escalation_plan,
            delivery={"success": False, "providers": ["webhook"], "failed_providers": ["webhook"]},
            delivery_metadata={
                "session_id": "connector-delivery-recovery-escalation-failed-live-retry",
                "delivery_success": False,
            },
            executed_by="release-manager",
        )
    )
    failed_recovery_escalation_retry_execution_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_metadata(
            failed_recovery_escalation_retry_execution
        )
    )
    recovery_escalation_retry_health = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health(
            [
                open_recovery_escalation_metadata,
                recovery_escalation_ack_metadata,
                recovery_escalation_retry_metadata,
                recovery_escalation_retry_worker_metadata,
                failed_recovery_escalation_retry_execution_metadata,
            ],
            generated_by="test",
            now=datetime.now(timezone.utc),
        )
    )
    recovery_escalation_retry_health_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_metadata(
            recovery_escalation_retry_health
        )
    )
    recovery_escalation_retry_health_alert_plan = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan(
            recovery_escalation_retry_health,
            requested_provider="webhook",
            available_providers=["webhook"],
            generated_by="test",
            force=True,
        )
    )
    recovery_escalation_retry_health_alert_event = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_event(
            recovery_escalation_retry_health,
            generated_by="test",
        )
    )
    recovery_escalation_retry_health_alert_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_metadata(
            recovery_escalation_retry_health_alert_plan
        )
    )
    recovery_escalation_retry_health_alert_ack = (
        acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert(
            recovery_escalation_retry_health["health_id"],
            provider="webhook",
            acknowledged_by="release-manager",
            acknowledgement_state="acknowledged",
            plan_id=recovery_escalation_retry_health_alert_plan["plan_id"],
        )
    )
    recovery_escalation_retry_health_alert_ack_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_ack_metadata(
            recovery_escalation_retry_health_alert_ack
        )
    )
    recovery_escalation_retry_health_alert_history = (
        filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_history(
            [
                recovery_escalation_retry_health_alert_metadata,
                recovery_escalation_retry_health_alert_ack_metadata,
            ]
        )
    )
    recovery_escalation_retry_health_alert_dashboard = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_dashboard(
            [
                recovery_escalation_retry_health_alert_metadata,
                recovery_escalation_retry_health_alert_ack_metadata,
            ]
        )
    )
    failed_recovery_retry_health_alert_delivery = {
        "session_id": "connector-delivery-recovery-retry-health-alert-failed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert",
        "health_id": recovery_escalation_retry_health["health_id"],
        "plan_id": recovery_escalation_retry_health_alert_plan["plan_id"],
        "event_id": recovery_escalation_retry_health["health_id"],
        "delivery_success": False,
        "providers": ["webhook"],
        "failed_providers": ["webhook"],
        "status_codes": [503],
    }
    recovery_retry_health_alert_delivery_retry_plan = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan(
            [failed_recovery_retry_health_alert_delivery],
            policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
        )
    )
    recovery_retry_health_alert_delivery_retry_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_metadata(
            recovery_retry_health_alert_delivery_retry_plan
        )
    )
    recovery_retry_health_alert_delivery_retry_worker_run = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run(
            [
                recovery_escalation_retry_health_metadata,
                failed_recovery_retry_health_alert_delivery,
            ],
            retry_policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
            dry_run=False,
            max_retry_deliveries=2,
        )
    )
    recovery_retry_health_alert_delivery_retry_worker_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_metadata(
            recovery_retry_health_alert_delivery_retry_worker_run
        )
    )
    recovery_retry_health_alert_delivery_retry_execution = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record(
            recovery_retry_health_alert_delivery_retry_worker_run,
            recovery_retry_health_alert_delivery_retry_worker_run["selected_retries"][0],
            health=recovery_escalation_retry_health,
            delivery={"success": True, "providers": ["webhook"]},
            delivery_metadata={
                "session_id": "connector-delivery-recovery-health-alert-live-retry",
                "delivery_success": True,
            },
            executed_by="release-manager",
        )
    )
    recovery_retry_health_alert_delivery_retry_execution_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record_metadata(
            recovery_retry_health_alert_delivery_retry_execution
        )
    )
    executive_report_delivery_event = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_event(
            executive_schedule_run,
            generated_by="test",
        )
    )
    failed_executive_report_delivery = {
        "session_id": "connector-delivery-recovery-executive-report-failed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report",
        "run_id": executive_schedule_run["run_id"],
        "event_id": executive_schedule_run["run_id"],
        "delivery_success": False,
        "providers": ["webhook"],
        "failed_providers": ["webhook"],
        "status_codes": [503],
    }
    executive_report_delivery_retry_plan = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan(
            [failed_executive_report_delivery],
            policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
        )
    )
    executive_report_delivery_retry_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan_metadata(
            executive_report_delivery_retry_plan
        )
    )
    executive_report_delivery_retry_worker_run = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run(
            [executive_schedule_metadata, failed_executive_report_delivery],
            retry_policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
            dry_run=False,
            max_retry_deliveries=2,
        )
    )
    executive_report_delivery_retry_worker_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run_metadata(
            executive_report_delivery_retry_worker_run
        )
    )
    executive_report_delivery_retry_execution = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record(
            executive_report_delivery_retry_worker_run,
            executive_report_delivery_retry_worker_run["selected_retries"][0],
            schedule_run=executive_schedule_run,
            delivery={"success": True, "providers": ["webhook"]},
            delivery_metadata={
                "session_id": "connector-delivery-recovery-executive-report-live-retry",
                "delivery_success": True,
            },
            executed_by="release-manager",
        )
    )
    executive_report_delivery_retry_execution_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record_metadata(
            executive_report_delivery_retry_execution
        )
    )
    executive_report_delivery_retry_health = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health(
            [
                executive_report_delivery_retry_metadata,
                executive_report_delivery_retry_worker_metadata,
                executive_report_delivery_retry_execution_metadata,
                failed_executive_report_delivery,
            ],
            generated_by="test",
            now=datetime.now(timezone.utc),
        )
    )
    executive_report_delivery_retry_health_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_metadata(
            executive_report_delivery_retry_health
        )
    )
    executive_report_delivery_retry_health_alert_plan = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan(
            executive_report_delivery_retry_health,
            requested_provider="webhook",
            available_providers=["webhook"],
            generated_by="test",
            force=True,
        )
    )
    executive_report_delivery_retry_health_alert_event = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_event(
            executive_report_delivery_retry_health,
            generated_by="test",
        )
    )
    executive_report_delivery_retry_health_alert_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_metadata(
            executive_report_delivery_retry_health_alert_plan
        )
    )
    executive_report_delivery_retry_health_alert_ack = (
        acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert(
            executive_report_delivery_retry_health["health_id"],
            provider="webhook",
            acknowledged_by="release-manager",
            acknowledgement_state="acknowledged",
            plan_id=executive_report_delivery_retry_health_alert_plan["plan_id"],
        )
    )
    executive_report_delivery_retry_health_alert_ack_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_ack_metadata(
            executive_report_delivery_retry_health_alert_ack
        )
    )
    executive_report_delivery_retry_health_alert_history = (
        filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_history(
            [
                executive_report_delivery_retry_health_alert_metadata,
                executive_report_delivery_retry_health_alert_ack_metadata,
            ]
        )
    )
    executive_report_delivery_retry_health_alert_dashboard = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_dashboard(
            [
                executive_report_delivery_retry_health_alert_metadata,
                executive_report_delivery_retry_health_alert_ack_metadata,
            ]
        )
    )
    failed_executive_retry_health_alert_delivery = {
        "session_id": "connector-delivery-executive-retry-health-alert-failed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata_kind": "release-connector-delivery",
        "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert",
        "health_id": executive_report_delivery_retry_health["health_id"],
        "plan_id": executive_report_delivery_retry_health_alert_plan["plan_id"],
        "event_id": executive_report_delivery_retry_health["health_id"],
        "delivery_success": False,
        "providers": ["webhook"],
        "failed_providers": ["webhook"],
        "status_codes": [503],
    }
    executive_retry_health_alert_delivery_retry_plan = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan(
            [failed_executive_retry_health_alert_delivery],
            policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
        )
    )
    executive_retry_health_alert_delivery_retry_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_metadata(
            executive_retry_health_alert_delivery_retry_plan
        )
    )
    executive_retry_health_alert_delivery_retry_worker_run = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run(
            [
                executive_report_delivery_retry_health_metadata,
                failed_executive_retry_health_alert_delivery,
            ],
            retry_policy={"max_retry_attempts": 3, "retry_delay_minutes": 0, "allow_immediate_retry": True},
            generated_by="test",
            dry_run=False,
            max_retry_deliveries=2,
        )
    )
    executive_retry_health_alert_delivery_retry_worker_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_metadata(
            executive_retry_health_alert_delivery_retry_worker_run
        )
    )
    executive_retry_health_alert_delivery_retry_execution = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record(
            executive_retry_health_alert_delivery_retry_worker_run,
            executive_retry_health_alert_delivery_retry_worker_run["selected_retries"][0],
            health=executive_report_delivery_retry_health,
            delivery={"success": True, "providers": ["webhook"]},
            delivery_metadata={
                "session_id": "connector-delivery-executive-health-alert-live-retry",
                "delivery_success": True,
            },
            executed_by="release-manager",
        )
    )
    executive_retry_health_alert_delivery_retry_execution_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record_metadata(
            executive_retry_health_alert_delivery_retry_execution
        )
    )
    dashboard_items = [
        *items,
        retry_metadata,
        retry_ack_metadata,
        approval_metadata,
        approval_decision_metadata,
        execution_metadata,
        playbook_metadata,
        closure_metadata,
        retry_recovery_report_metadata,
        open_recovery_escalation_metadata,
        recovery_escalation_ack_metadata,
        recovery_escalation_retry_metadata,
        executive_report_metadata,
        executive_schedule_metadata,
        recovery_escalation_retry_worker_metadata,
        recovery_escalation_retry_execution_metadata,
        failed_recovery_escalation_retry_execution_metadata,
        recovery_escalation_retry_health_metadata,
        recovery_escalation_retry_health_alert_metadata,
        recovery_escalation_retry_health_alert_ack_metadata,
        failed_recovery_retry_health_alert_delivery,
        recovery_retry_health_alert_delivery_retry_metadata,
        recovery_retry_health_alert_delivery_retry_worker_metadata,
        recovery_retry_health_alert_delivery_retry_execution_metadata,
        executive_report_delivery_retry_metadata,
        executive_report_delivery_retry_worker_metadata,
        executive_report_delivery_retry_execution_metadata,
        executive_report_delivery_retry_health_metadata,
        executive_report_delivery_retry_health_alert_metadata,
        executive_report_delivery_retry_health_alert_ack_metadata,
        failed_executive_retry_health_alert_delivery,
        executive_retry_health_alert_delivery_retry_metadata,
        executive_retry_health_alert_delivery_retry_worker_metadata,
        executive_retry_health_alert_delivery_retry_execution_metadata,
        {
            "session_id": "connector-delivery-recovery-executive-report",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "metadata_kind": "release-connector-delivery",
            "connector_delivery_source": "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report",
            "run_id": executive_schedule_run["run_id"],
            "delivery_success": True,
            "providers": ["webhook"],
            "failed_providers": [],
        },
        failed_executive_report_delivery,
    ]
    dashboard = build_go_rollback_drill_notification_dashboard(dashboard_items)
    final_reporting_closure_dashboard = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closure_dashboard(
        dashboard_items
    )
    final_reporting_release_readiness = (
        build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary(
            dashboard_items,
            generated_by="test",
        )
    )
    final_reporting_release_readiness_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary_metadata(
            final_reporting_release_readiness
        )
    )
    final_reporting_operator_runbook = (
        build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export(
            dashboard_items,
            generated_by="test",
        )
    )
    final_reporting_operator_runbook_metadata = (
        build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export_metadata(
            final_reporting_operator_runbook
        )
    )
    dashboard_with_final_reporting = build_go_rollback_drill_notification_dashboard(
        [
            *dashboard_items,
            final_reporting_release_readiness_metadata,
            final_reporting_operator_runbook_metadata,
        ]
    )

    assert approval_plan["approval_required_count"] == 1
    assert approval_metadata["metadata_kind"].endswith("retry-execution-approval-plan")
    assert approval_decision["approval_state"] == "approved"
    assert approval_decision_metadata["metadata_kind"].endswith("retry-execution-approval-decision")
    assert worker_run["dry_run"] is False
    assert worker_run["summary"]["selected_retry_count"] == 1
    assert worker_run["summary"]["approval_pending_count"] == 0
    assert execution_record["execution_status"] == "delivered"
    assert execution_record["approval_decision_id"] == approval_decision["decision_id"]
    assert execution_metadata["metadata_kind"].endswith("retry-execution-record")
    assert playbook["provider_count"] == 1
    assert playbook["provider_playbooks"][0]["category"] == "webhook"
    assert playbook_metadata["metadata_kind"].endswith("connector-recovery-playbook")
    assert closure["closure_state"] == "resolved"
    assert closure_metadata["metadata_kind"].endswith("connector-recovery-closure")
    assert retry_recovery_report["execution_count"] == 1
    assert retry_recovery_report["execution_success_count"] == 1
    assert retry_recovery_report["recovery_closed_count"] == 1
    assert retry_recovery_report["recovery_slo_breached_count"] == 0
    assert retry_recovery_report["provider_summary"][0]["provider"] == "webhook"
    assert retry_recovery_report["closure_trends"][0]["resolved_count"] == 1
    assert retry_recovery_report_metadata["metadata_kind"].endswith("retry-recovery-report")
    assert open_recovery_escalation_plan["escalation_count"] == 1
    assert open_recovery_escalation_plan["slo_breached_count"] == 1
    assert open_recovery_escalation_plan["selected_providers"] == ["webhook"]
    assert open_recovery_escalation_metadata["metadata_kind"].endswith("recovery-escalation-plan")
    assert open_recovery_escalation_event["event_type"].endswith("recovery_escalation")
    assert executive_report["executive_summary"]["escalation_count"] == 1
    assert executive_report["key_risks"][0]["risk"] == "Connector recovery SLO breached"
    assert executive_report_metadata["metadata_kind"].endswith("recovery-executive-report")
    assert recovery_escalation_ack["acknowledgement_state"] == "accepted"
    assert recovery_escalation_ack_metadata["metadata_kind"].endswith("recovery-escalation-ack")
    assert recovery_escalation_retry_plan["retryable_count"] == 1
    assert recovery_escalation_retry_metadata["metadata_kind"].endswith(
        "recovery-escalation-delivery-retry-plan"
    )
    assert executive_schedule_run["summary"]["executive_report_count"] == 1
    assert executive_schedule_metadata["metadata_kind"].endswith("recovery-executive-report-schedule-run")
    assert recovery_escalation_retry_worker_run["summary"]["selected_retry_count"] == 1
    assert recovery_escalation_retry_worker_metadata["metadata_kind"].endswith("recovery-escalation-retry-worker-run")
    assert recovery_escalation_retry_execution["execution_status"] == "delivered"
    assert recovery_escalation_retry_execution_metadata["metadata_kind"].endswith(
        "recovery-escalation-retry-execution-record"
    )
    assert failed_recovery_escalation_retry_execution["execution_status"] == "failed"
    assert recovery_escalation_retry_health["alert_count"] == 1
    assert recovery_escalation_retry_health["alert_level"] == "critical"
    assert recovery_escalation_retry_health_metadata["metadata_kind"].endswith(
        "recovery-escalation-retry-health"
    )
    assert recovery_escalation_retry_health_alert_plan["selected_providers"] == ["webhook"]
    assert recovery_escalation_retry_health_alert_event["event_type"].endswith(
        "recovery_escalation_retry_health_alert"
    )
    assert recovery_escalation_retry_health_alert_metadata["metadata_kind"].endswith(
        "recovery-escalation-retry-health-alert-plan"
    )
    assert recovery_escalation_retry_health_alert_ack["acknowledgement_state"] == "acknowledged"
    assert recovery_escalation_retry_health_alert_ack_metadata["metadata_kind"].endswith(
        "recovery-escalation-retry-health-alert-ack"
    )
    assert recovery_escalation_retry_health_alert_history["total"] == 2
    assert recovery_escalation_retry_health_alert_dashboard["acknowledgement_count"] == 1
    assert recovery_retry_health_alert_delivery_retry_plan["retryable_count"] == 1
    assert recovery_retry_health_alert_delivery_retry_metadata["metadata_kind"].endswith(
        "recovery-escalation-retry-health-alert-delivery-retry-plan"
    )
    assert recovery_retry_health_alert_delivery_retry_worker_run["summary"]["selected_retry_count"] == 1
    assert recovery_retry_health_alert_delivery_retry_worker_metadata["metadata_kind"].endswith(
        "recovery-escalation-retry-health-alert-delivery-retry-worker-run"
    )
    assert recovery_retry_health_alert_delivery_retry_execution["execution_status"] == "delivered"
    assert recovery_retry_health_alert_delivery_retry_execution_metadata["metadata_kind"].endswith(
        "recovery-escalation-retry-health-alert-delivery-retry-execution-record"
    )
    assert executive_report_delivery_event["event_type"].endswith("recovery_executive_report")
    assert executive_report_delivery_retry_plan["retryable_count"] == 1
    assert executive_report_delivery_retry_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-plan"
    )
    assert executive_report_delivery_retry_worker_run["summary"]["selected_retry_count"] == 1
    assert executive_report_delivery_retry_worker_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-worker-run"
    )
    assert executive_report_delivery_retry_execution["execution_status"] == "delivered"
    assert executive_report_delivery_retry_execution_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-execution-record"
    )
    assert executive_report_delivery_retry_health["alert_count"] >= 1
    assert executive_report_delivery_retry_health["alert_level"] == "critical"
    assert executive_report_delivery_retry_health_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-health"
    )
    assert executive_report_delivery_retry_health_alert_plan["selected_providers"] == ["webhook"]
    assert executive_report_delivery_retry_health_alert_event["event_type"].endswith(
        "recovery_executive_report_delivery_retry_health_alert"
    )
    assert executive_report_delivery_retry_health_alert_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-health-alert-plan"
    )
    assert executive_report_delivery_retry_health_alert_ack["acknowledgement_state"] == "acknowledged"
    assert executive_report_delivery_retry_health_alert_ack_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-health-alert-ack"
    )
    assert executive_report_delivery_retry_health_alert_history["total"] == 2
    assert executive_report_delivery_retry_health_alert_dashboard["acknowledgement_count"] == 1
    assert executive_retry_health_alert_delivery_retry_plan["retryable_count"] == 1
    assert executive_retry_health_alert_delivery_retry_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-health-alert-delivery-retry-plan"
    )
    assert executive_retry_health_alert_delivery_retry_worker_run["summary"]["selected_retry_count"] == 1
    assert executive_retry_health_alert_delivery_retry_worker_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-health-alert-delivery-retry-worker-run"
    )
    assert executive_retry_health_alert_delivery_retry_execution["execution_status"] == "delivered"
    assert executive_retry_health_alert_delivery_retry_execution_metadata["metadata_kind"].endswith(
        "recovery-executive-report-delivery-retry-health-alert-delivery-retry-execution-record"
    )
    assert final_reporting_closure_dashboard["closure_state"] == "open"
    assert final_reporting_closure_dashboard["summary"][
        "executive_retry_health_alert_retry_worker_run_count"
    ] == 1
    assert final_reporting_release_readiness["readiness_state"] == "blocked"
    assert final_reporting_release_readiness["failed_check_count"] >= 1
    assert final_reporting_release_readiness_metadata["metadata_kind"].endswith(
        "final-reporting-release-readiness-summary"
    )
    assert (
        final_reporting_operator_runbook["readiness_summary_id"]
        == final_reporting_operator_runbook["readiness_summary"]["summary_id"]
    )
    assert "CAVRA Rollback Drill Final Reporting Runbook Export" in final_reporting_operator_runbook["markdown"]
    assert final_reporting_operator_runbook_metadata["metadata_kind"].endswith(
        "final-reporting-operator-runbook-export"
    )
    assert dashboard["acknowledgement_audit_delivery_retry_execution_approval_plan_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_retry_execution_approval_decision_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_retry_execution_approved_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_retry_execution_record_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_retry_execution_success_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_connector_recovery_playbook_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_connector_recovery_closure_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_connector_recovery_closed_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_retry_recovery_report_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_plan_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_route_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_ack_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_plan_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retryable_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_worker_run_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_count"] == 2
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_execution_success_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_execution_failed_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_health_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_ack_count"] == 1
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retryable_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record_count"
        ]
        == 1
    )
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_schedule_run_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_count"] == 2
    assert dashboard["failed_acknowledgement_audit_delivery_recovery_executive_report_delivery_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_retryable_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_success_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_count"] == 1
    assert dashboard["acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_count"] >= 1
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_ack_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retryable_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_count"
        ]
        == 1
    )
    assert (
        dashboard[
            "acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record_count"
        ]
        == 1
    )
    assert (
        dashboard_with_final_reporting[
            "acknowledgement_audit_delivery_final_reporting_release_readiness_summary_count"
        ]
        == 1
    )
    assert (
        dashboard_with_final_reporting[
            "acknowledgement_audit_delivery_final_reporting_operator_runbook_export_count"
        ]
        == 1
    )


def test_go_rollback_drill_notification_escalation_plan_flags_breaches(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="slack")
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    plan_metadata["created_at"] = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()

    escalation = build_go_rollback_drill_notification_escalation_plan(
        [plan_metadata],
        policy={"acknowledgement_minutes": 5},
    )
    metadata = build_go_rollback_drill_notification_escalation_plan_metadata(escalation)

    assert escalation["alert_level"] == "critical"
    assert escalation["breached_count"] == 1
    assert escalation["routes"][0]["recommended_action"] == "escalate_missed_drill_notification"
    assert metadata["metadata_kind"] == "go-backend-rollback-drill-notification-escalation-plan"


def test_go_rollback_drill_notification_escalation_uses_owner_slo(tmp_path: Path) -> None:
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path, next_due_at=datetime.now(timezone.utc) + timedelta(days=3))
    now = datetime.now(timezone.utc)
    policy = {
        "owner_routes": {
            "release-governance": {
                "providers": ["slack"],
                "acknowledgement_minutes": 20,
            }
        }
    }
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        )
    )
    plan = build_go_rollback_drill_notification_plan(report, requested_provider="slack", routing_policy=policy, now=now)
    plan_metadata = build_go_rollback_drill_notification_plan_metadata(plan)
    plan_metadata["created_at"] = (now - timedelta(minutes=10)).isoformat()

    escalation = build_go_rollback_drill_notification_escalation_plan(
        [plan_metadata],
        policy=policy,
        now=now,
    )

    assert escalation["alert_level"] == "warning"
    assert escalation["breached_count"] == 0
    assert escalation["routes"][0]["acknowledgement_minutes"] == 20


def test_go_promoted_mode_falls_back_without_promotion_evidence(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
        ),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is True
    assert result["fallback_reason"] == "go backend promotion readiness check failed"
    assert result["promotion_readiness"]["status"] == "needs_attention"


def test_go_promoted_mode_falls_back_without_rollback_plan(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)
    promotion = _write_promotion_evidence(tmp_path)

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
            promotion_evidence_path=str(promotion),
        ),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is True
    assert result["fallback_reason"] == "go backend rollback readiness check failed"
    assert result["rollback_readiness"]["status"] == "needs_attention"


def test_go_promoted_mode_falls_back_without_rollback_rehearsal(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)
    promotion = _write_promotion_evidence(tmp_path)
    rollback = _write_rollback_plan(tmp_path)

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
            promotion_evidence_path=str(promotion),
            rollback_plan_path=str(rollback),
        ),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is True
    assert result["fallback_reason"] == "go backend rollback rehearsal check failed"
    assert result["rollback_rehearsal"]["status"] == "needs_attention"


def test_go_promoted_mode_falls_back_without_rollback_drill_history(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)
    promotion = _write_promotion_evidence(tmp_path)
    rollback = _write_rollback_plan(tmp_path)
    rehearsal = _write_rollback_rehearsal(tmp_path)

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
            promotion_evidence_path=str(promotion),
            rollback_plan_path=str(rollback),
            rollback_rehearsal_path=str(rehearsal),
        ),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is True
    assert result["fallback_reason"] == "go backend rollback drill history check failed"
    assert result["rollback_drill_history"]["status"] == "needs_attention"


def test_go_promoted_mode_falls_back_without_rollback_drill_schedule(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)
    promotion = _write_promotion_evidence(tmp_path)
    rollback = _write_rollback_plan(tmp_path)
    rehearsal = _write_rollback_rehearsal(tmp_path)
    drills = _write_rollback_drill_history(tmp_path)

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
            promotion_evidence_path=str(promotion),
            rollback_plan_path=str(rollback),
            rollback_rehearsal_path=str(rehearsal),
            rollback_drill_history_path=str(drills),
        ),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is True
    assert result["fallback_reason"] == "go backend rollback drill schedule check failed"
    assert result["rollback_drill_schedule"]["status"] == "needs_attention"


def test_go_promoted_mode_selects_go_when_promotion_gate_passes(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    _write_deployment_metadata(tmp_path)
    promotion = _write_promotion_evidence(tmp_path)
    rollback = _write_rollback_plan(tmp_path)
    rehearsal = _write_rollback_rehearsal(tmp_path)
    drills = _write_rollback_drill_history(tmp_path)
    schedule = _write_rollback_drill_schedule(tmp_path)

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(
            mode=GO_BACKEND_PROMOTED,
            runtime_path=str(runtime),
            policy_path=str(policy),
            package_dir=str(tmp_path),
            promotion_evidence_path=str(promotion),
            rollback_plan_path=str(rollback),
            rollback_rehearsal_path=str(rehearsal),
            rollback_drill_history_path=str(drills),
            rollback_drill_schedule_path=str(schedule),
        ),
    )

    assert result["selected_backend"] == "go"
    assert result["fallback_used"] is False
    assert result["effective_decision"] == result["go_decision"]


def _fake_go_runtime(tmp_path: Path, *, decision: str, rule_id: str, severity: str) -> Path:
    path = tmp_path / "fake-cavra-runtime"
    path.write_text(
        textwrap.dedent(
            f"""\
            #!/usr/bin/env python3
            import json
            import sys

            payload = json.loads(sys.stdin.read() or "{{}}")
            print(json.dumps({{
                "decision": "{decision}",
                "reason": "fake go runtime",
                "action_type": payload.get("action_type", "execute_command"),
                "target": payload.get("target", ""),
                "requested_operation": payload.get("target", ""),
                "policy_pack": payload.get("policy_pack", "cavra-ai-agent-baseline"),
                "policy_id": payload.get("policy_pack", "cavra-ai-agent-baseline"),
                "rule_id": "{rule_id}",
                "severity": "{severity}"
            }}))
            """
        ),
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path


def _write_deployment_metadata(path: Path) -> None:
    (path / "cavra-runtime.endpoint-deployment.json").write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-runtime.endpoint-deployment.v1",
                "deployment_targets": [
                    {
                        "id": "github-actions-linux-amd64-runner",
                        "surface": "ci-runner",
                        "platform": "linux/amd64",
                        "binary": "bin/cavra-runtime_linux_amd64",
                    },
                    {
                        "id": "linux-systemd-amd64-workstation",
                        "surface": "workstation",
                        "platform": "linux/amd64",
                        "binary": "bin/cavra-runtime_linux_amd64",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    (path / "cavra-runtime.ci-runner-bundles.json").write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-runtime.ci-runner-bundles.v1",
                "source_metadata": "cavra-runtime.endpoint-deployment.json",
                "controls": [
                    "verified-signed-runtime-before-runner-use",
                    "runner-authentication-claims-signed",
                    "runner-authentication-oidc-verified",
                    "daemon-evidence-stream-hmac-signed",
                    "evidence-verification-artifact-published",
                    "blocking-decision-fails-closed-by-default",
                ],
                "runner_bundles": [
                    {
                        "platform": "GitHub Actions",
                        "deployment_target": "github-actions-linux-amd64-runner",
                        "runtime_binary": "bin/cavra-runtime_linux_amd64",
                        "required_outputs": [
                            ".cavra/go-daemon/release-governance-evidence-verification.json"
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (path / "cavra-runtime.channels.json").write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-runtime.channels.v1",
                "source_metadata": "cavra-runtime.endpoint-deployment.json",
                "channels": [
                    {
                        "channel": "stable",
                        "auto_update": False,
                        "approval_required": True,
                        "workstation_targets": [
                            {
                                "id": "linux-systemd-amd64-workstation",
                                "platform": "linux/amd64",
                                "deployment_channel": "stable",
                                "management_tool": "linux",
                                "binary": "bin/cavra-runtime_linux_amd64",
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (path / "cavra-runtime.updater-policy.json").write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-runtime.updater-policy.v1",
                "source_channel_manifest": "cavra-runtime.channels.json",
                "default_auto_update": False,
                "policies": [{"channel": "stable", "auto_update": False, "approval_required": True}],
            }
        ),
        encoding="utf-8",
    )


def _write_promotion_evidence(path: Path) -> Path:
    evidence = path / "cavra-runtime.go-backend-promotion-evidence.json"
    evidence.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-promotion-evidence.v1",
                "parity_status": "pass",
                "deployment_status": "ready",
                "approved": True,
                "approval_id": "apr_go_backend_promotion",
                "evidence_refs": [
                    "go-runtime-parity://ci/238-passed",
                    "go-deployment-readiness://ci/ready",
                ],
            }
        ),
        encoding="utf-8",
    )
    return evidence


def _write_rollback_plan(path: Path) -> Path:
    plan = path / "cavra-runtime.go-backend-rollback-plan.json"
    plan.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-rollback-plan.v1",
                "status": "ready",
                "target_mode": "disabled",
                "approved": True,
                "approval_id": "apr_go_backend_rollback",
                "max_recovery_minutes": 15,
                "controls": [
                    "python-fallback-available",
                    "promoted-mode-disable-tested",
                    "rollback-approval-recorded",
                    "operator-runbook-linked",
                    "evidence-capture-enabled",
                ],
                "rollback_steps": [
                    "Set CAVRA_GO_BACKEND_MODE=disabled.",
                    "Restart API, CI runner, or workstation process using CAVRA.",
                    "Capture go rollback readiness and production readiness reports.",
                ],
                "evidence_refs": [
                    "go-rollback-readiness://ci/ready",
                    "go-promotion-rollback-runbook://docs/current",
                ],
            }
        ),
        encoding="utf-8",
    )
    return plan


def _write_rollback_rehearsal(path: Path) -> Path:
    rehearsal = path / "cavra-runtime.go-backend-rollback-rehearsal.json"
    rehearsal.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-rollback-rehearsal.v1",
                "status": "pass",
                "plan_approval_id": "apr_go_backend_rollback",
                "simulated": True,
                "fallback_verified": True,
                "recovery_minutes": 6,
                "max_recovery_minutes": 15,
                "runbook_ref": "docs/go-backend-rollback-rehearsal.md",
                "evidence_refs": [
                    "go-rollback-rehearsal://ci/fallback-restored",
                    "go-production-readiness://ci/after-rehearsal",
                ],
            }
        ),
        encoding="utf-8",
    )
    return rehearsal


def _write_rollback_drill_history(path: Path) -> Path:
    history = path / "cavra-runtime.go-backend-rollback-drills.json"
    history.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-rollback-drill-history.v1",
                "environment": "production-pilot",
                "drills": [
                    {
                        "drill_id": "drill_go_backend_python_fallback",
                        "executed_at": datetime.now(timezone.utc).isoformat(),
                        "actor": "release-agent",
                        "source_mode": "promoted",
                        "target_mode": "disabled",
                        "status": "pass",
                        "fallback_verified": True,
                        "recovery_minutes": 7,
                        "max_recovery_minutes": 15,
                        "runbook_ref": "docs/go-backend-rollback-drill-history.md",
                        "evidence_refs": [
                            "go-rollback-drill://ci/python-fallback-restored",
                            "go-production-readiness://ci/post-drill-ready",
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return history


def _write_rollback_drill_schedule(path: Path, *, next_due_at: datetime | None = None) -> Path:
    schedule = path / "cavra-runtime.go-backend-rollback-drill-schedule.json"
    schedule.write_text(
        json.dumps(
            {
                "schema_version": "cavra.go-backend-rollback-drill-schedule.v1",
                "schedule_id": "go_backend_python_fallback_monthly",
                "environment": "production-pilot",
                "status": "active",
                "interval_days": 30,
                "next_due_at": (next_due_at or datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
                "owners": ["release-governance"],
                "notification_providers": ["slack", "teams"],
                "runbook_ref": "docs/go-backend-rollback-drill-scheduling.md",
            }
        ),
        encoding="utf-8",
    )
    return schedule
