#!/usr/bin/env python3
"""Generate lightweight Go enforcement contracts from enforcement.proto."""

from __future__ import annotations

import subprocess
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
\tReleaseGovernance *ReleaseGovernanceEvidence `json:"release_governance,omitempty"`
\tRunnerAuth        *RunnerAuthentication `json:"runner_auth,omitempty"`
}

type ReleaseGovernanceEvidence struct {
\tMetadataKind                     string   `json:"metadata_kind,omitempty"`
\tReleaseChannel                   string   `json:"release_channel,omitempty"`
\tReleaseVersion                   string   `json:"release_version,omitempty"`
\tApprovalState                    string   `json:"approval_state,omitempty"`
\tApprovalID                       string   `json:"approval_id,omitempty"`
\tApprovalRequiredCount            int      `json:"approval_required_count,omitempty"`
\tDeliverySuccess                  bool     `json:"delivery_success,omitempty"`
\tFailedProviders                  []string `json:"failed_providers,omitempty"`
\tFailedDeliveryCount              int      `json:"failed_delivery_count,omitempty"`
\tConnectorDeliveryFailureCount    int      `json:"connector_delivery_failure_count,omitempty"`
\tAlertLevel                       string   `json:"alert_level,omitempty"`
\tDriftStatus                      string   `json:"drift_status,omitempty"`
\tHandoffStatus                    string   `json:"handoff_status,omitempty"`
\tBlockedCount                     int      `json:"blocked_count,omitempty"`
\tCriticalCount                    int      `json:"critical_count,omitempty"`
\tBreachedCount                    int      `json:"breached_count,omitempty"`
\tDriftedEndpointCount             int      `json:"drifted_endpoint_count,omitempty"`
\tMissingTargetCount               int      `json:"missing_target_count,omitempty"`
\tEvidenceRefs                     []string `json:"evidence_refs,omitempty"`
\tConnectorDeliverySource          string   `json:"connector_delivery_source,omitempty"`
}

type RunnerAuthentication struct {
\tIdentity  RunnerIdentity `json:"identity,omitempty"`
\tAlgorithm string         `json:"algorithm,omitempty"`
\tKeyID     string         `json:"key_id,omitempty"`
\tSignature string         `json:"signature,omitempty"`
}

type RunnerIdentity struct {
\tProvider   string `json:"provider,omitempty"`
\tRepository string `json:"repository,omitempty"`
\tWorkflow   string `json:"workflow,omitempty"`
\tRunID      string `json:"run_id,omitempty"`
\tRunAttempt string `json:"run_attempt,omitempty"`
\tRef        string `json:"ref,omitempty"`
\tSHA        string `json:"sha,omitempty"`
\tActor      string `json:"actor,omitempty"`
\tJob        string `json:"job,omitempty"`
\tRunnerName string `json:"runner_name,omitempty"`
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
\truntimeRequest := cavraruntime.Request{
\t\tSessionID:           request.SessionID,
\t\tAgentID:             request.AgentID,
\t\tActor:               request.Actor,
\t\tActionType:          request.ActionType,
\t\tTarget:              request.Target,
\t\tRequestedOperation:  request.RequestedOperation,
\t\tPolicyPack:          request.PolicyPack,
\t}
\tif request.ReleaseGovernance != nil {
\t\tif record := request.ReleaseGovernance.RuntimeRecord(); record != nil {
\t\t\truntimeRequest.Record = record
\t\t\tif runtimeRequest.ActionType == "" {
\t\t\t\truntimeRequest.ActionType = "release_governance_record"
\t\t\t}
\t\t}
\t}
\treturn runtimeRequest
}

func (evidence ReleaseGovernanceEvidence) RuntimeRecord() map[string]any {
\trecord := map[string]any{}
\taddString(record, "metadata_kind", evidence.MetadataKind)
\taddString(record, "release_channel", evidence.ReleaseChannel)
\taddString(record, "release_version", evidence.ReleaseVersion)
\taddString(record, "approval_state", evidence.ApprovalState)
\taddString(record, "approval_id", evidence.ApprovalID)
\taddInt(record, "approval_required_count", evidence.ApprovalRequiredCount)
\tif evidence.DeliverySuccess {
\t\trecord["delivery_success"] = true
\t}
\tif len(evidence.FailedProviders) > 0 {
\t\trecord["failed_providers"] = evidence.FailedProviders
\t}
\taddInt(record, "failed_delivery_count", evidence.FailedDeliveryCount)
\taddInt(record, "connector_delivery_failure_count", evidence.ConnectorDeliveryFailureCount)
\taddString(record, "alert_level", evidence.AlertLevel)
\taddString(record, "drift_status", evidence.DriftStatus)
\taddString(record, "handoff_status", evidence.HandoffStatus)
\taddInt(record, "blocked_count", evidence.BlockedCount)
\taddInt(record, "critical_count", evidence.CriticalCount)
\taddInt(record, "breached_count", evidence.BreachedCount)
\taddInt(record, "drifted_endpoint_count", evidence.DriftedEndpointCount)
\taddInt(record, "missing_target_count", evidence.MissingTargetCount)
\tif len(evidence.EvidenceRefs) > 0 {
\t\trecord["evidence_refs"] = evidence.EvidenceRefs
\t}
\taddString(record, "connector_delivery_source", evidence.ConnectorDeliverySource)
\tif len(record) == 0 {
\t\treturn nil
\t}
\treturn record
}

func addString(record map[string]any, key string, value string) {
\tif value != "" {
\t\trecord[key] = value
\t}
}

func addInt(record map[string]any, key string, value int) {
\tif value != 0 {
\t\trecord[key] = value
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
        "release_governance",
        "runner_auth",
        "RunnerAuthentication",
        "RunnerIdentity",
        "ReleaseGovernanceEvidence",
        "metadata_kind",
        "release_channel",
        "release_version",
        "approval_state",
        "approval_id",
        "approval_required_count",
        "delivery_success",
        "failed_providers",
        "failed_delivery_count",
        "connector_delivery_failure_count",
        "alert_level",
        "drift_status",
        "handoff_status",
        "blocked_count",
        "critical_count",
        "breached_count",
        "drifted_endpoint_count",
        "missing_target_count",
        "evidence_refs",
        "connector_delivery_source",
        "provider",
        "repository",
        "workflow",
        "run_id",
        "run_attempt",
        "ref",
        "sha",
        "job",
        "runner_name",
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
    subprocess.run(["gofmt", "-w", str(OUTPUT)], check=True)


if __name__ == "__main__":
    main()
