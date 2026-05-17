from cavra.policy_authoring import build_policy_pack_draft, build_rollout_change_plan, production_readiness_report


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
    assert report["store_summary"]["missing"] == ["activity"]
