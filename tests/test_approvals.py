from pathlib import Path

from cavra.approvals import (
    ApprovalStore,
    SQLiteApprovalStore,
    actor_context_from_claims,
    build_provider_request_specs,
    attach_approval_to_decision,
    create_approval_request,
    export_approval_notification_payloads,
    load_routing_rules,
    route_approver_group,
)
from cavra.evidence import build_evidence_metadata, create_evidence_bundle
from cavra.runtime import RuntimeGuard


def _approval_decision() -> dict[str, object]:
    return RuntimeGuard(policy_pack="cavra-ai-agent-baseline").evaluate_file_access(
        Path("iam/admin-role.tf"),
        "write",
    ).to_dict()


def test_create_and_approve_request(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    decided = store.decide(
        approval["approval_id"],
        state="approved",
        actor="platform-security",
        reason="Reviewed scoped IAM change.",
        external_ref="CHG-100",
    )

    assert approval["state"] == "pending"
    assert decided["state"] == "approved"
    assert decided["decided_by"] == "platform-security"
    assert decided["external_ref"] == "CHG-100"
    assert store.list(state="approved")["total"] == 1


def test_approval_requires_reason_and_blocks_double_decision(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision())

    try:
        store.decide(approval["approval_id"], state="approved", actor="security", reason="")
    except ValueError as exc:
        assert "reason is required" in str(exc)
    else:
        raise AssertionError("expected missing reason to fail")

    store.decide(approval["approval_id"], state="denied", actor="security", reason="Not enough context.")
    try:
        store.decide(approval["approval_id"], state="approved", actor="security", reason="Changed mind.")
    except ValueError as exc:
        assert "only pending approvals" in str(exc)
    else:
        raise AssertionError("expected final approval to reject a second decision")


def test_break_glass_records_mandatory_evidence(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")

    approval = store.break_glass(
        decision=_approval_decision(),
        actor="incident-commander",
        reason="Production recovery for active incident.",
        external_ref="INC-777",
    )

    assert approval["state"] == "break_glass"
    assert approval["break_glass"] is True
    assert approval["break_glass_reason"] == "Production recovery for active incident."
    assert approval["external_ref"] == "INC-777"
    assert any(item["event"] == "break_glass" for item in approval["history"])


def test_approval_outcome_is_recorded_in_evidence(tmp_path: Path) -> None:
    decision = _approval_decision()
    approval = create_approval_request(decision, requested_by="developer")
    decision_with_approval = attach_approval_to_decision(decision, approval)

    create_evidence_bundle([decision_with_approval], tmp_path / "bundle", session_id="approval-session")
    metadata = build_evidence_metadata(tmp_path / "bundle")
    attestation = (tmp_path / "bundle" / "pr-attestation.md").read_text(encoding="utf-8")

    assert metadata["approval_outcomes"][0]["approval_id"] == approval["approval_id"]
    assert "Approval Outcomes" in attestation
    assert approval["approval_id"] in attestation


def test_routing_rules_select_approver_group() -> None:
    decision = _approval_decision()
    decision.pop("approver_group", None)

    assert route_approver_group(decision) == "IAM"


def test_repository_routing_file_overrides_default(tmp_path: Path) -> None:
    routing = tmp_path / "routing.json"
    routing.write_text(
        """
        {
          "approval_routing": [
            {
              "rule_id_prefix": "filesystem.write",
              "target_contains": "iam/",
              "approver_group": "Cloud IAM Owners"
            }
          ]
        }
        """,
        encoding="utf-8",
    )
    decision = _approval_decision()
    decision.pop("approver_group", None)

    assert route_approver_group(decision, load_routing_rules(routing)) == "Cloud IAM Owners"


def test_routing_file_accepts_raw_rule_list(tmp_path: Path) -> None:
    routing = tmp_path / "routing.json"
    routing.write_text(
        '[{"rule_id_prefix":"filesystem.write","target_contains":"iam/","approver_group":"Cloud IAM Owners"}]',
        encoding="utf-8",
    )

    assert load_routing_rules(routing)[0]["approver_group"] == "Cloud IAM Owners"


def test_actor_claims_authorize_matching_approval_group(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")
    actor_context = actor_context_from_claims({"email": "iam@example.com", "groups": ["IAM"]})

    decided = store.decide(
        approval["approval_id"],
        state="approved",
        actor="iam@example.com",
        reason="Reviewed IAM change.",
        actor_context=actor_context,
    )

    assert decided["state"] == "approved"


def test_actor_claims_can_map_external_groups() -> None:
    context = actor_context_from_claims(
        {"email": "owner@example.com", "groups": ["github-team:iam-admins"]},
        rbac_rules={"group_mappings": {"github-team:iam-admins": "IAM"}},
    )

    assert "IAM" in context["groups"]


def test_actor_claims_reject_wrong_approval_group(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")
    actor_context = actor_context_from_claims({"email": "dev@example.com", "groups": ["Developers"]})

    try:
        store.decide(
            approval["approval_id"],
            state="approved",
            actor="dev@example.com",
            reason="Trying to approve.",
            actor_context=actor_context,
        )
    except ValueError as exc:
        assert "not authorized" in str(exc)
    else:
        raise AssertionError("expected unauthorized actor to fail")


def test_sqlite_approval_store_searches_and_updates(tmp_path: Path) -> None:
    store = SQLiteApprovalStore(tmp_path / "approvals.db")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    store.decide(approval["approval_id"], state="approved", actor="iam-owner", reason="Reviewed.")
    result = store.list(state="approved", approver_group="IAM")

    assert result["total"] == 1
    assert result["items"][0]["state"] == "approved"


def test_export_approval_notification_payloads(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    result = export_approval_notification_payloads(approval, tmp_path / "notifications")

    assert (tmp_path / "notifications" / "slack-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "teams-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "jira-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "servicenow-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "webhook-approval-payload.json").exists()
    assert len(result.files) == 5


def test_provider_request_specs_do_not_require_live_credentials(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    specs = build_provider_request_specs(approval)

    assert specs["jira"]["method"] == "POST"
    assert "${JIRA_TOKEN}" in specs["jira"]["headers"]["authorization"]
    assert specs["slack"]["body"]["text"].startswith("CAVRA approval")
