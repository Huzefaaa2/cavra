#!/usr/bin/env python3
"""Generate lightweight Go enforcement contracts from enforcement.proto."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTO = ROOT / "proto/cavra/enforcement/v1/enforcement.proto"
OUTPUT = ROOT / "go/cavra-runtime/enforcement/v1/contracts.go"

TEMPLATE = """// Code generated from proto/cavra/enforcement/v1/enforcement.proto. DO NOT EDIT.
package v1

import cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"

type EvaluateRequest struct {
\tSessionID          string `json:"session_id,omitempty"`
\tAgentID            string `json:"agent_id,omitempty"`
\tActor              string `json:"actor,omitempty"`
\tActionType         string `json:"action_type,omitempty"`
\tTarget             string `json:"target,omitempty"`
\tRequestedOperation string `json:"requested_operation,omitempty"`
\tPolicyPack         string `json:"policy_pack,omitempty"`
}

type DecisionResponse struct {
\tDecisionID         string   `json:"decision_id,omitempty"`
\tSessionID          string   `json:"session_id,omitempty"`
\tAgentID            string   `json:"agent_id,omitempty"`
\tActor              string   `json:"actor,omitempty"`
\tActionType         string   `json:"action_type,omitempty"`
\tTarget             string   `json:"target,omitempty"`
\tRequestedOperation string   `json:"requested_operation,omitempty"`
\tPolicyPack         string   `json:"policy_pack,omitempty"`
\tPolicyID           string   `json:"policy_id,omitempty"`
\tRuleID             string   `json:"rule_id,omitempty"`
\tDecision           string   `json:"decision,omitempty"`
\tSeverity           string   `json:"severity,omitempty"`
\tReason             string   `json:"reason,omitempty"`
\tEvidenceRefs       []string `json:"evidence_refs,omitempty"`
\tApproverGroup      string   `json:"approver_group,omitempty"`
\tTimestamp          string   `json:"timestamp,omitempty"`
\tCorrelationID      string   `json:"correlation_id,omitempty"`
}

func (request EvaluateRequest) RuntimeRequest() cavraruntime.Request {
\treturn cavraruntime.Request{
\t\tSessionID:           request.SessionID,
\t\tAgentID:             request.AgentID,
\t\tActor:               request.Actor,
\t\tActionType:          request.ActionType,
\t\tTarget:              request.Target,
\t\tRequestedOperation:  request.RequestedOperation,
\t\tPolicyPack:          request.PolicyPack,
\t}
}

func DecisionResponseFromRuntime(decision cavraruntime.Decision) DecisionResponse {
\treturn DecisionResponse{
\t\tDecisionID:         decision.DecisionID,
\t\tSessionID:          decision.SessionID,
\t\tAgentID:            decision.AgentID,
\t\tActor:              decision.Actor,
\t\tActionType:         decision.ActionType,
\t\tTarget:             decision.Target,
\t\tRequestedOperation: decision.RequestedOperation,
\t\tPolicyPack:         decision.PolicyPack,
\t\tPolicyID:           decision.PolicyID,
\t\tRuleID:             decision.RuleID,
\t\tDecision:           decision.Decision,
\t\tSeverity:           decision.Severity,
\t\tReason:             decision.Reason,
\t\tEvidenceRefs:       decision.EvidenceRefs,
\t\tApproverGroup:      decision.ApproverGroup,
\t\tTimestamp:          decision.Timestamp,
\t\tCorrelationID:      decision.CorrelationID,
\t}
}
"""


def main() -> None:
    proto = PROTO.read_text(encoding="utf-8")
    required_fields = [
        "session_id",
        "agent_id",
        "actor",
        "action_type",
        "target",
        "requested_operation",
        "policy_pack",
        "decision_id",
        "policy_id",
        "rule_id",
        "decision",
        "severity",
        "reason",
        "evidence_refs",
        "approver_group",
        "timestamp",
        "correlation_id",
    ]
    missing = [field for field in required_fields if field not in proto]
    if missing:
        raise SystemExit(f"{PROTO} is missing expected fields: {', '.join(missing)}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(TEMPLATE, encoding="utf-8")


if __name__ == "__main__":
    main()
