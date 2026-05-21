from cavra.approvals import apply_approval_decision, create_approval_request
from cavra.policy_authoring import (
    build_policy_pack_draft,
    build_policy_pack_publish_plan,
    build_policy_publish_decision,
    build_rollout_change_plan,
    policy_content_digest,
    production_readiness_report,
    publish_policy_pack,
)


def test_build_policy_pack_draft_validates_and_summarizes() -> None:
    draft = build_policy_pack_draft(
        {
            "id": "cavra-platform-baseline",
            "title": "Platform Baseline",
            "description": "Platform engineering controls.",
            "version": "2026.05",
            "inherits": "cavra-ai-agent-baseline",
            "filesystem": {"block_read": [".env"], "require_approval_write": ["iam/"]},
            "commands": {"block": ["terraform apply -auto-approve"]},
            "git": {"require_ai_attestation": True},
        }
    )

    assert draft["valid"] is True
    assert draft["policy_pack"]["metadata"]["id"] == "cavra-platform-baseline"
    assert draft["summary"]["rule_counts"]["filesystem"] == 2
    assert draft["summary"]["rule_counts"]["commands"] == 1


def test_build_policy_pack_draft_reports_schema_errors() -> None:
    draft = build_policy_pack_draft({"id": "platform", "title": "Bad", "description": "Bad id"})

    assert draft["valid"] is False
    assert any("metadata.id" in error for error in draft["errors"])


def test_build_rollout_change_plan_flags_enforcement_risk() -> None:
    current = {
        "rollout_id": "payments-api-baseline",
        "repository": "payments/api",
        "policy_pack": "cavra-ai-agent-baseline",
        "mode": "audit_only",
        "state": "planned",
    }

    plan = build_rollout_change_plan(current, {"mode": "strict", "state": "active", "coverage_percent": 90})

    assert plan["operation"] == "update"
    assert plan["risk"] == "high"
    assert plan["approval_required"] is True
    assert any(change["field"] == "mode" for change in plan["changes"])


def test_policy_publish_plan_requires_approval_and_digest() -> None:
    payload = {
        "id": "cavra-platform-baseline",
        "title": "Platform Baseline",
        "description": "Platform engineering controls.",
        "version": "2026.05",
        "commands": {"block": ["terraform apply -auto-approve"]},
    }

    plan = build_policy_pack_publish_plan(payload)
    decision = build_policy_publish_decision(plan, requested_by="platform@example.com")

    assert plan["approval_required"] is True
    assert plan["policy_digest"] == policy_content_digest(build_policy_pack_draft(payload)["policy_pack"])
    assert decision["action_type"] == "policy_publish"
    assert decision["policy_digest"] == plan["policy_digest"]
    assert decision["approver_group"] == "Platform Security"


def test_publish_policy_pack_writes_policy_and_signature_after_approval(tmp_path) -> None:
    payload = {
        "id": "cavra-platform-baseline",
        "title": "Platform Baseline",
        "description": "Platform engineering controls.",
        "version": "2026.05",
        "filesystem": {"block_read": [".env"]},
    }
    plan = build_policy_pack_publish_plan(payload)
    approval = create_approval_request(build_policy_publish_decision(plan, requested_by="platform@example.com"))
    approved = apply_approval_decision(approval, state="approved", actor="security@example.com", reason="approved")

    result = publish_policy_pack(payload, approved, policy_root=tmp_path, signer="security@example.com", key="secret")

    assert result["status"] == "published"
    assert (tmp_path / "cavra-platform-baseline" / "policy.yaml").exists()
    assert (tmp_path / "cavra-platform-baseline" / "policy.yaml.sig.json").exists()
    assert result["signature_verified"] is True


def test_publish_policy_pack_rejects_mismatched_approval_digest(tmp_path) -> None:
    payload = {
        "id": "cavra-platform-baseline",
        "title": "Platform Baseline",
        "description": "Platform engineering controls.",
        "version": "2026.05",
        "filesystem": {"block_read": [".env"]},
    }
    changed = {**payload, "filesystem": {"block_read": [".env", "secrets/"]}}
    plan = build_policy_pack_publish_plan(payload)
    approval = create_approval_request(build_policy_publish_decision(plan, requested_by="platform@example.com"))
    approved = apply_approval_decision(approval, state="approved", actor="security@example.com", reason="approved")

    try:
        publish_policy_pack(changed, approved, policy_root=tmp_path, signer="security@example.com")
    except ValueError as exc:
        assert "approval does not match policy draft digest" in str(exc)
    else:
        raise AssertionError("publish should reject mismatched approval digest")


def test_production_readiness_report_marks_missing_controls() -> None:
    report = production_readiness_report(
        oidc_configured=False,
        rbac_configured=True,
        cors_origins=[],
        evidence_artifact_root_configured=True,
        policy_pack_count=2,
        store_status={"items": [{"name": "activity", "exists": False}]},
    )

    assert report["status"] == "needs_attention"
    assert any(item["id"] == "oidc_configured" and item["status"] == "warn" for item in report["checks"])
    assert any(item["id"] == "go_backend_pilot" and item["status"] == "pass" for item in report["checks"])
    assert any(item["id"] == "go_backend_deployment_paths" and item["status"] == "pass" for item in report["checks"])
    assert any(item["id"] == "go_backend_promotion_gate" and item["status"] == "pass" for item in report["checks"])
    assert any(item["id"] == "go_backend_rollback_controls" and item["status"] == "pass" for item in report["checks"])
    assert report["go_backend_pilot"]["status"] == "disabled"
    assert report["go_backend_deployment"]["status"] == "not_configured"
    assert report["go_backend_promotion"]["status"] == "not_requested"
    assert report["go_backend_rollback"]["status"] == "not_requested"
    assert report["store_summary"]["missing"] == ["activity"]
