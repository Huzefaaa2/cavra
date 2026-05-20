package runtime

import (
	"fmt"
	"strings"
)

func evaluateReleaseGovernanceRecord(request Request, pack string) Decision {
	record := request.Record
	kind := stringValue(record, "metadata_kind")
	target := request.Target
	if target == "" {
		target = kind
	}
	if target == "" {
		target = "release-governance-record"
	}
	if len(record) == 0 {
		return baseDecision("require_approval", "Release governance record payload is missing.", request.ActionType, target, "verify", pack, "release_governance.record.missing", "medium", "Release Governance")
	}

	if kind == "" {
		kind = target
	}
	approvalState := approvalState(record)
	approvalID := approvalID(record)
	requiredCount := intValue(record, "approval_required_count")
	requiresApproval := requiredCount > 0 || approvalState != "" || approvalID != "" || approvalRequiredKind(kind)
	requested := request.operation()
	if requested == "" {
		requested = "verify"
	}

	switch approvalState {
	case "approved":
		if approvalID == "" && approvalRequiredKind(kind) {
			return baseDecision("block", fmt.Sprintf("%s is approved but does not include an approval_id.", kind), request.ActionType, target, requested, pack, "release_governance.approval.missing", "critical", "Release Governance")
		}
		return baseDecision("allow", fmt.Sprintf("%s is backed by an approved release governance approval.", kind), request.ActionType, target, requested, pack, "release_governance.approval.approved", "low", "")
	case "pending":
		return baseDecision("require_approval", fmt.Sprintf("%s is waiting for release governance approval.", kind), request.ActionType, target, requested, pack, "release_governance.approval.pending", "high", "Release Governance")
	case "denied", "rejected", "expired", "cancelled", "canceled":
		return baseDecision("block", fmt.Sprintf("%s is bound to a non-approved approval state: %s.", kind, approvalState), request.ActionType, target, requested, pack, "release_governance.approval.denied", "critical", "Release Governance")
	case "":
		if requiresApproval {
			decision := "require_approval"
			ruleID := "release_governance.approval.required"
			severity := "high"
			if executionKind(kind) {
				decision = "block"
				ruleID = "release_governance.approval.missing"
				severity = "critical"
			}
			return baseDecision(decision, fmt.Sprintf("%s requires an approval record before execution.", kind), request.ActionType, target, requested, pack, ruleID, severity, "Release Governance")
		}
		return baseDecision("allow", fmt.Sprintf("%s does not require release governance approval.", kind), request.ActionType, target, requested, pack, "release_governance.approval.not_required", "low", "")
	default:
		return baseDecision("require_approval", fmt.Sprintf("%s has an unknown approval state: %s.", kind, approvalState), request.ActionType, target, requested, pack, "release_governance.approval.unknown", "medium", "Release Governance")
	}
}

func approvalRequiredKind(kind string) bool {
	switch kind {
	case "release-channel-promotion-request",
		"endpoint-reconciliation-automation",
		"endpoint-drift-remediation-request",
		"endpoint-drift-remediation-execution",
		"rollout-promotion-execution",
		"rollout-rollback-execution":
		return true
	default:
		return false
	}
}

func executionKind(kind string) bool {
	switch kind {
	case "endpoint-drift-remediation-execution",
		"rollout-promotion-execution",
		"rollout-rollback-execution":
		return true
	default:
		return false
	}
}

func approvalID(record map[string]any) string {
	value := stringValue(record, "approval_id")
	if value != "" {
		return value
	}
	if approval, ok := record["approval"].(map[string]any); ok {
		return stringValue(approval, "approval_id")
	}
	return ""
}

func approvalState(record map[string]any) string {
	state := stringValue(record, "approval_state")
	if state != "" {
		return normalizeState(state)
	}
	if approval, ok := record["approval"].(map[string]any); ok {
		return normalizeState(stringValue(approval, "state"))
	}
	return ""
}

func stringValue(record map[string]any, key string) string {
	if record == nil {
		return ""
	}
	value, ok := record[key]
	if !ok || value == nil {
		return ""
	}
	switch typed := value.(type) {
	case string:
		return strings.TrimSpace(typed)
	default:
		return strings.TrimSpace(fmt.Sprint(typed))
	}
}

func intValue(record map[string]any, key string) int {
	if record == nil {
		return 0
	}
	value, ok := record[key]
	if !ok || value == nil {
		return 0
	}
	switch typed := value.(type) {
	case int:
		return typed
	case int64:
		return int(typed)
	case float64:
		return int(typed)
	default:
		return 0
	}
}

func normalizeState(value string) string {
	return strings.ToLower(strings.ReplaceAll(strings.TrimSpace(value), "-", "_"))
}
