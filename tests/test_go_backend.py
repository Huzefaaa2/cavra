from __future__ import annotations

import json
import textwrap
from pathlib import Path

from cavra.go_backend import (
    GO_BACKEND_DISABLED,
    GO_BACKEND_ENFORCE,
    GO_BACKEND_PROMOTED,
    GO_BACKEND_SHADOW,
    GoBackendConfig,
    evaluate_with_go_pilot,
    go_backend_config_from_env,
    go_backend_readiness_report,
    go_deployment_readiness_report,
    go_promotion_readiness_report,
    go_rollback_readiness_report,
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


def test_go_promoted_mode_selects_go_when_promotion_gate_passes(tmp_path: Path) -> None:
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
