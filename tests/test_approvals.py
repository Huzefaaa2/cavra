from pathlib import Path

from cavra.approvals import ApprovalStore, attach_approval_to_decision, create_approval_request
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
