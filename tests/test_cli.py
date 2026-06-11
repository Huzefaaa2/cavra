import json
from pathlib import Path

from typer.testing import CliRunner

from cavra.cli import app
from cavra.evidence import create_evidence_bundle, export_key_trust_root, generate_ed25519_keypair
from cavra.runtime import RuntimeGuard


runner = CliRunner()


def _decisions() -> list[dict[str, object]]:
    guard = RuntimeGuard(policy_pack="cavra-ai-agent-baseline")
    return [
        guard.evaluate_file_access(Path(".env"), "read").to_dict(),
        guard.evaluate_command("terraform plan").to_dict(),
    ]


def test_verify_attestation_cli_fails_invalid_report(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    create_evidence_bundle(_decisions(), bundle, session_id="cli-test")
    (bundle / "pr-attestation.md").unlink()

    result = runner.invoke(
        app,
        [
            "evidence",
            "verify-attestation",
            str(bundle),
            "--output",
            str(tmp_path / "attestation"),
        ],
    )

    assert result.exit_code == 1
    assert "PR attestation verification failed" in result.output
    assert "missing pr-attestation.md" in result.output


def test_verify_attestation_cli_exports_valid_report(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    create_evidence_bundle(_decisions(), bundle, session_id="cli-test")

    result = runner.invoke(
        app,
        [
            "evidence",
            "verify-attestation",
            str(bundle),
            "--output",
            str(tmp_path / "attestation"),
        ],
    )

    assert result.exit_code == 0
    assert "PR attestation verification exported" in result.output


def test_runtime_go_pilot_readiness_cli_reports_disabled() -> None:
    result = runner.invoke(app, ["runtime", "go-pilot-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.readiness.v1"
    assert payload["status"] == "disabled"


def test_agent_enforcement_readiness_cli_reports_schema() -> None:
    result = runner.invoke(app, ["agent", "enforcement-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.agent-enforcement-readiness.v1"
    assert payload["required_check_name"] == "cavra-required-check"
    assert payload["status"] in {"ready", "needs_attention", "blocked"}


def test_saas_contract_cli_lists_operating_automation_operation() -> None:
    result = runner.invoke(app, ["saas", "contract"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert "saas_operating_automation" in {item["name"] for item in payload["operations"]}
    assert payload["public_repository_boundary"]["contains_saas_backend"] is False


def test_saas_operating_automation_cli_prints_public_request_and_response() -> None:
    result = runner.invoke(
        app,
        [
            "saas",
            "operating-automation",
            "tenant-demo",
            "--requested-by",
            "console",
            "--automation-status",
            "scheduled",
            "--billing-monitoring-status",
            "enabled",
            "--license-telemetry-status",
            "automated",
            "--support-followup-status",
            "ready",
            "--customer-success-review-status",
            "scheduled",
            "--dashboard-refresh-status",
            "automated",
            "--escalation-drill-status",
            "blocked",
            "--closeout-retry-status",
            "enabled",
            "--blocker",
            "escalation drill owner pending",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["request"]["operation"] == "saas_operating_automation"
    assert payload["request"]["payload"]["required_checks"] == [
        "billing_monitoring",
        "license_telemetry_sync",
        "support_followup",
        "customer_success_review",
        "dashboard_refresh",
        "escalation_drill",
        "closeout_retry",
    ]
    assert payload["response"]["status"] == "requires_private_service"
    assert payload["response"]["payload"]["summary"]["automation_status"] == "scheduled"
    assert payload["response"]["payload"]["summary"]["blockers"] == ["escalation drill owner pending"]


def test_saas_operating_automation_cli_rejects_sensitive_values() -> None:
    result = runner.invoke(
        app,
        [
            "saas",
            "operating-automation",
            "tenant-demo",
            "--automation-cadence",
            "ghp_123456789012345678901234567890",
        ],
    )

    assert result.exit_code == 1
    assert "sensitive value" in result.output


def test_saas_worker_handoff_cli_prints_public_request_and_response() -> None:
    result = runner.invoke(
        app,
        [
            "saas",
            "worker-handoff",
            "tenant-demo",
            "--requested-by",
            "console",
            "--deployment-environment",
            "production",
            "--worker-mode",
            "shadow",
            "--worker-target",
            "billing_monitoring",
            "--worker-target",
            "support_followup",
            "--handoff-status",
            "requires_private_service",
            "--scheduler-ref",
            "scheduler-saas-operating-automation",
            "--evidence-sink-ref",
            "evidence-sink-saas-operating-automation",
            "--retry-policy-ref",
            "retry-policy-saas-operating-automation",
            "--worker-owner",
            "operations-owner",
            "--blocker",
            "private scheduler validation required",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["request"]["operation"] == "saas_operating_automation_worker_handoff"
    assert payload["request"]["payload"]["worker_mode"] == "shadow"
    assert payload["request"]["payload"]["worker_targets"] == ["billing_monitoring", "support_followup"]
    assert payload["response"]["status"] == "requires_private_service"
    assert payload["response"]["payload"]["summary"]["handoff_status"] == "requires_private_service"
    assert payload["response"]["payload"]["summary"]["worker_targets"] == ["billing_monitoring", "support_followup"]


def test_saas_worker_handoff_cli_rejects_sensitive_values() -> None:
    result = runner.invoke(
        app,
        [
            "saas",
            "worker-handoff",
            "tenant-demo",
            "--worker-target",
            "ghp_123456789012345678901234567890",
        ],
    )

    assert result.exit_code == 1
    assert "sensitive value" in result.output


def test_aispm_validate_review_packet_cli_accepts_packaged_sample() -> None:
    result = runner.invoke(
        app,
        [
            "aispm",
            "validate-review-packet",
            "examples/aispm/community-replay-to-policy-review-packet-sample.json",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.aispm.review_packet_validation.v1"
    assert payload["valid"] is True
    assert payload["packet_schema_version"] == "cavra.aispm.replay_to_policy_review_packet.v1"


def test_aispm_validate_review_packet_cli_rejects_inconsistent_packet(tmp_path: Path) -> None:
    packet_path = tmp_path / "packet.json"
    payload = json.loads(
        Path("examples/aispm/community-replay-to-policy-review-packet-sample.json").read_text(encoding="utf-8")
    )
    payload["test_fixture"]["case_count"] = 999
    packet_path.write_text(json.dumps(payload), encoding="utf-8")

    result = runner.invoke(app, ["aispm", "validate-review-packet", str(packet_path)])

    assert result.exit_code == 1
    assert "invalid" in result.output
    assert "case_count must match" in result.output


def test_aispm_validate_ci_gate_readiness_cli_accepts_packaged_sample() -> None:
    result = runner.invoke(
        app,
        [
            "aispm",
            "validate-ci-gate-readiness",
            "examples/aispm/community-replay-to-policy-ci-gate-readiness-sample.json",
            "--repo-root",
            ".",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.aispm.ci_gate_readiness_validation.v1"
    assert payload["valid"] is True
    assert payload["checks"]["repository_templates"] == "pass"
    assert payload["packet_schema_version"] == "cavra.aispm.replay_to_policy_ci_gate_readiness.v1"


def test_aispm_validate_ci_gate_readiness_cli_rejects_wrong_check(tmp_path: Path) -> None:
    packet_path = tmp_path / "ci-gate-readiness.json"
    payload = json.loads(
        Path("examples/aispm/community-replay-to-policy-ci-gate-readiness-sample.json").read_text(encoding="utf-8")
    )
    payload["gates"][0]["required_check"] = "wrong-check"
    packet_path.write_text(json.dumps(payload), encoding="utf-8")

    result = runner.invoke(app, ["aispm", "validate-ci-gate-readiness", str(packet_path)])

    assert result.exit_code == 1
    assert "invalid" in result.output
    assert "required_check must be" in result.output
    assert "cavra-aispm-review-packet" in result.output


def test_policy_keygen_sign_and_verify_cli_round_trip(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.yaml"
    keys_dir = tmp_path / "keys"
    policy_path.write_text(
        """
metadata:
  id: cavra-cli-test-policy
  title: CLI Test Policy
  description: CLI test policy
  version: 1
commands:
  allow:
    - "terraform plan*"
""",
        encoding="utf-8",
    )

    keygen = runner.invoke(app, ["policy", "keygen", "--output", str(keys_dir), "--key-id", "cli-policy-key"])
    assert keygen.exit_code == 0
    key_payload = json.loads(keygen.output)
    private_key = Path(key_payload["private_key_path"])
    public_key = Path(key_payload["public_key_path"])
    assert private_key.exists()
    assert public_key.exists()

    signed = runner.invoke(
        app,
        [
            "policy",
            "sign",
            str(policy_path),
            "--signer",
            "platform-security",
            "--private-key",
            str(private_key),
            "--key-id",
            "cli-policy-key",
        ],
    )
    assert signed.exit_code == 0
    verified = runner.invoke(app, ["policy", "verify", str(policy_path), "--public-key", str(public_key)])
    assert verified.exit_code == 0
    assert "verified Ed25519 signature" in verified.output


def test_evaluate_cli_reports_strict_mode_effective_decision() -> None:
    result = runner.invoke(app, ["evaluate", "execute_command", "terraform plan", "--policy-mode", "strict", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.runtime-policy-mode-summary.v1"
    assert payload["base_decision"]["decision"] == "allow"
    assert payload["effective_decision"] == "require_approval"
    assert payload["mode"] == "strict"


def test_evaluate_cli_blocks_break_glass_without_reason() -> None:
    result = runner.invoke(app, ["evaluate", "execute_command", "terraform plan", "--policy-mode", "break_glass", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["effective_decision"] == "block"
    assert payload["break_glass_reason_present"] is False


def test_runtime_go_deployment_readiness_cli_reports_not_configured() -> None:
    result = runner.invoke(app, ["runtime", "go-deployment-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.deployment-readiness.v1"
    assert payload["status"] == "not_configured"


def test_runtime_go_promotion_readiness_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-promotion-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.promotion-readiness.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_readiness_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-readiness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-readiness.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_rehearsal_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-rehearsal", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-rehearsal.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_drills_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-drills", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-drill-history.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_drill_schedule_cli_reports_not_requested() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-drill-schedule", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-drill-schedule.v1"
    assert payload["status"] == "not_requested"


def test_runtime_go_rollback_drill_notification_plan_cli_reports_payload() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-drill-notification-plan", "--force", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["plan"]["schema_version"] == "cavra.go-backend-pilot.rollback-drill-notification-plan.v1"
    assert payload["event"]["event_type"] == "cavra.go_backend.rollback_drill.notification"


def test_runtime_go_rollback_drill_notification_plan_cli_accepts_routing_policy(tmp_path: Path) -> None:
    routing_policy = tmp_path / "routing-policy.json"
    routing_policy.write_text(
        json.dumps(
            {
                "owner_routes": {
                    "release-governance": {
                        "providers": ["slack"],
                        "acknowledgement_minutes": 15,
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    result = runner.invoke(
        app,
        [
            "runtime",
            "go-rollback-drill-notification-plan",
            "--routing-policy",
            str(routing_policy),
            "--force",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["plan"]["selected_providers"] == ["slack"]
    assert payload["plan"]["route_decisions"][0]["acknowledgement_minutes"] == 15


def test_runtime_go_rollback_drill_notification_ack_cli_reports_payload() -> None:
    result = runner.invoke(
        app,
        [
            "runtime",
            "go-rollback-drill-notification-ack",
            "go_backend_python_fallback_monthly",
            "--provider",
            "slack",
            "--acknowledged-by",
            "release-manager",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["acknowledgement"]["acknowledgement_state"] == "acknowledged"
    assert payload["metadata"]["metadata_kind"] == "go-backend-rollback-drill-notification-ack"


def test_runtime_go_rollback_drill_escalation_plan_cli_reports_payload() -> None:
    result = runner.invoke(app, ["runtime", "go-rollback-drill-escalation-plan", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["schema_version"] == "cavra.go-backend-pilot.rollback-drill-notification-escalation-plan.v1"
    assert payload["alert_level"] == "healthy"


def test_integration_deliver_cli_accepts_config_option(tmp_path: Path) -> None:
    event = tmp_path / "event.json"
    config = tmp_path / "connectors.json"
    output = tmp_path / "delivery"
    event.write_text(
        json.dumps(
            {
                "event_type": "cavra.evidence_bundle",
                "session_id": "cli-connector-test",
                "decision_count": 1,
                "blocked_count": 1,
                "approval_required_count": 0,
                "max_severity": "high",
            }
        ),
        encoding="utf-8",
    )
    config.write_text(
        json.dumps({"connectors": {"webhook": {"url": "http://127.0.0.1:9/cavra?token=secret"}}}),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "integration",
            "deliver",
            str(event),
            "--config",
            str(config),
            "--provider",
            "webhook",
            "--retries",
            "0",
            "--timeout-seconds",
            "0.1",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert "connector delivery evidence exported" in result.output
    assert list(output.glob("*.json"))


def test_trust_distribution_cli_exports_offline_package(tmp_path: Path) -> None:
    private_key = tmp_path / "private.pem"
    public_key = tmp_path / "public.pem"
    trust_root = tmp_path / "trust-root.json"
    output = tmp_path / "trust-distribution"
    generate_ed25519_keypair(private_key, public_key)
    export_key_trust_root(public_key, trust_root, key_id="cli-prod")

    result = runner.invoke(
        app,
        [
            "evidence",
            "trust-distribution",
            str(trust_root),
            "--output",
            str(output),
            "--environment",
            "prod",
            "--distribution-id",
            "cli-dist",
            "--channel",
            "source-control",
            "--channel",
            "offline-media",
        ],
    )

    assert result.exit_code == 0
    assert "trust-root distribution exported" in result.output
    manifest = json.loads((output / "trust-root-distribution-manifest.json").read_text(encoding="utf-8"))
    assert manifest["distribution_id"] == "cli-dist"
    assert manifest["channels"] == ["source-control", "offline-media"]
