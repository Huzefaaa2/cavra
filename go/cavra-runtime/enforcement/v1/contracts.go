// Code generated from proto/cavra/enforcement/v1/enforcement.proto. DO NOT EDIT.
package v1

import cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"

type EvaluateRequest struct {
	SessionID          string `json:"session_id,omitempty"`
	AgentID            string `json:"agent_id,omitempty"`
	Actor              string `json:"actor,omitempty"`
	ActionType         string `json:"action_type,omitempty"`
	Target             string `json:"target,omitempty"`
	RequestedOperation string `json:"requested_operation,omitempty"`
	PolicyPack         string `json:"policy_pack,omitempty"`
}

type DecisionResponse struct {
	DecisionID         string   `json:"decision_id,omitempty"`
	SessionID          string   `json:"session_id,omitempty"`
	AgentID            string   `json:"agent_id,omitempty"`
	Actor              string   `json:"actor,omitempty"`
	ActionType         string   `json:"action_type,omitempty"`
	Target             string   `json:"target,omitempty"`
	RequestedOperation string   `json:"requested_operation,omitempty"`
	PolicyPack         string   `json:"policy_pack,omitempty"`
	PolicyID           string   `json:"policy_id,omitempty"`
	RuleID             string   `json:"rule_id,omitempty"`
	Decision           string   `json:"decision,omitempty"`
	Severity           string   `json:"severity,omitempty"`
	Reason             string   `json:"reason,omitempty"`
	EvidenceRefs       []string `json:"evidence_refs,omitempty"`
	ApproverGroup      string   `json:"approver_group,omitempty"`
	Timestamp          string   `json:"timestamp,omitempty"`
	CorrelationID      string   `json:"correlation_id,omitempty"`
}

func (request EvaluateRequest) RuntimeRequest() cavraruntime.Request {
	return cavraruntime.Request{
		SessionID:           request.SessionID,
		AgentID:             request.AgentID,
		Actor:               request.Actor,
		ActionType:          request.ActionType,
		Target:              request.Target,
		RequestedOperation:  request.RequestedOperation,
		PolicyPack:          request.PolicyPack,
	}
}

func DecisionResponseFromRuntime(decision cavraruntime.Decision) DecisionResponse {
	return DecisionResponse{
		DecisionID:         decision.DecisionID,
		SessionID:          decision.SessionID,
		AgentID:            decision.AgentID,
		Actor:              decision.Actor,
		ActionType:         decision.ActionType,
		Target:             decision.Target,
		RequestedOperation: decision.RequestedOperation,
		PolicyPack:         decision.PolicyPack,
		PolicyID:           decision.PolicyID,
		RuleID:             decision.RuleID,
		Decision:           decision.Decision,
		Severity:           decision.Severity,
		Reason:             decision.Reason,
		EvidenceRefs:       decision.EvidenceRefs,
		ApproverGroup:      decision.ApproverGroup,
		Timestamp:          decision.Timestamp,
		CorrelationID:      decision.CorrelationID,
	}
}
