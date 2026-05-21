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
    acknowledge_go_rollback_drill_notification,
    build_go_rollback_drill_notification_ack_metadata,
    build_go_rollback_drill_notification_dashboard,
    build_go_rollback_drill_notification_escalation_plan,
    build_go_rollback_drill_notification_escalation_plan_metadata,
    build_go_rollback_drill_notification_event,
    build_go_rollback_drill_notification_plan_metadata,
    build_go_rollback_drill_notification_plan,
    filter_go_rollback_drill_notification_history,
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
