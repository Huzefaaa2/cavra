// Code generated from proto/cavra/enforcement/v1/enforcement.proto. DO NOT EDIT.
package v1

import cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"

type EvaluateRequest struct {
	SessionID          string                     `json:"session_id,omitempty"`
	AgentID            string                     `json:"agent_id,omitempty"`
	Actor              string                     `json:"actor,omitempty"`
	ActionType         string                     `json:"action_type,omitempty"`
	Target             string                     `json:"target,omitempty"`
	RequestedOperation string                     `json:"requested_operation,omitempty"`
	PolicyPack         string                     `json:"policy_pack,omitempty"`
	ReleaseGovernance  *ReleaseGovernanceEvidence `json:"release_governance,omitempty"`
	RunnerAuth         *RunnerAuthentication      `json:"runner_auth,omitempty"`
}

type ReleaseGovernanceEvidence struct {
	MetadataKind                  string   `json:"metadata_kind,omitempty"`
	ReleaseChannel                string   `json:"release_channel,omitempty"`
	ReleaseVersion                string   `json:"release_version,omitempty"`
	ApprovalState                 string   `json:"approval_state,omitempty"`
	ApprovalID                    string   `json:"approval_id,omitempty"`
	ApprovalRequiredCount         int      `json:"approval_required_count,omitempty"`
	DeliverySuccess               bool     `json:"delivery_success,omitempty"`
	FailedProviders               []string `json:"failed_providers,omitempty"`
	FailedDeliveryCount           int      `json:"failed_delivery_count,omitempty"`
	ConnectorDeliveryFailureCount int      `json:"connector_delivery_failure_count,omitempty"`
	AlertLevel                    string   `json:"alert_level,omitempty"`
	DriftStatus                   string   `json:"drift_status,omitempty"`
	HandoffStatus                 string   `json:"handoff_status,omitempty"`
	BlockedCount                  int      `json:"blocked_count,omitempty"`
	CriticalCount                 int      `json:"critical_count,omitempty"`
	BreachedCount                 int      `json:"breached_count,omitempty"`
	DriftedEndpointCount          int      `json:"drifted_endpoint_count,omitempty"`
	MissingTargetCount            int      `json:"missing_target_count,omitempty"`
	EvidenceRefs                  []string `json:"evidence_refs,omitempty"`
	ConnectorDeliverySource       string   `json:"connector_delivery_source,omitempty"`
	VerificationStatus            string   `json:"verification_status,omitempty"`
	IntegrityStatus               string   `json:"integrity_status,omitempty"`
	FailedVerificationCount       int      `json:"failed_verification_count,omitempty"`
	IntegrityFailureCount         int      `json:"integrity_failure_count,omitempty"`
	AuditExportStatus             string   `json:"audit_export_status,omitempty"`
	RollbackReferenceCount        int      `json:"rollback_reference_count,omitempty"`
}

type RunnerAuthentication struct {
	Identity  RunnerIdentity `json:"identity,omitempty"`
	Algorithm string         `json:"algorithm,omitempty"`
	KeyID     string         `json:"key_id,omitempty"`
	Signature string         `json:"signature,omitempty"`
}

type RunnerIdentity struct {
	Provider   string `json:"provider,omitempty"`
	Repository string `json:"repository,omitempty"`
	Workflow   string `json:"workflow,omitempty"`
	RunID      string `json:"run_id,omitempty"`
	RunAttempt string `json:"run_attempt,omitempty"`
	Ref        string `json:"ref,omitempty"`
	SHA        string `json:"sha,omitempty"`
	Actor      string `json:"actor,omitempty"`
	Job        string `json:"job,omitempty"`
	RunnerName string `json:"runner_name,omitempty"`
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
	runtimeRequest := cavraruntime.Request{
		SessionID:          request.SessionID,
		AgentID:            request.AgentID,
		Actor:              request.Actor,
		ActionType:         request.ActionType,
		Target:             request.Target,
		RequestedOperation: request.RequestedOperation,
		PolicyPack:         request.PolicyPack,
	}
	if request.ReleaseGovernance != nil {
		if record := request.ReleaseGovernance.RuntimeRecord(); record != nil {
			runtimeRequest.Record = record
			if runtimeRequest.ActionType == "" {
				runtimeRequest.ActionType = "release_governance_record"
			}
		}
	}
	return runtimeRequest
}

func (evidence ReleaseGovernanceEvidence) RuntimeRecord() map[string]any {
	record := map[string]any{}
	addString(record, "metadata_kind", evidence.MetadataKind)
	addString(record, "release_channel", evidence.ReleaseChannel)
	addString(record, "release_version", evidence.ReleaseVersion)
	addString(record, "approval_state", evidence.ApprovalState)
	addString(record, "approval_id", evidence.ApprovalID)
	addInt(record, "approval_required_count", evidence.ApprovalRequiredCount)
	if evidence.DeliverySuccess {
		record["delivery_success"] = true
	}
	if len(evidence.FailedProviders) > 0 {
		record["failed_providers"] = evidence.FailedProviders
	}
	addInt(record, "failed_delivery_count", evidence.FailedDeliveryCount)
	addInt(record, "connector_delivery_failure_count", evidence.ConnectorDeliveryFailureCount)
	addString(record, "alert_level", evidence.AlertLevel)
	addString(record, "drift_status", evidence.DriftStatus)
	addString(record, "handoff_status", evidence.HandoffStatus)
	addInt(record, "blocked_count", evidence.BlockedCount)
	addInt(record, "critical_count", evidence.CriticalCount)
	addInt(record, "breached_count", evidence.BreachedCount)
	addInt(record, "drifted_endpoint_count", evidence.DriftedEndpointCount)
	addInt(record, "missing_target_count", evidence.MissingTargetCount)
	if len(evidence.EvidenceRefs) > 0 {
		record["evidence_refs"] = evidence.EvidenceRefs
	}
	addString(record, "connector_delivery_source", evidence.ConnectorDeliverySource)
	addString(record, "verification_status", evidence.VerificationStatus)
	addString(record, "integrity_status", evidence.IntegrityStatus)
	addInt(record, "failed_verification_count", evidence.FailedVerificationCount)
	addInt(record, "integrity_failure_count", evidence.IntegrityFailureCount)
	addString(record, "audit_export_status", evidence.AuditExportStatus)
	addInt(record, "rollback_reference_count", evidence.RollbackReferenceCount)
	if len(record) == 0 {
		return nil
	}
	return record
}

func addString(record map[string]any, key string, value string) {
	if value != "" {
		record[key] = value
	}
}

func addInt(record map[string]any, key string, value int) {
	if value != 0 {
		record[key] = value
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
