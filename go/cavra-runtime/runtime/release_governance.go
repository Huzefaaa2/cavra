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
	requiresApproval := requiredCount > 0 || approvalState != "" || approvalRequiredKind(kind)
	requested := request.operation()
	if requested == "" {
		requested = "verify"
	}

	switch approvalState {
	case "approved":
		if approvalID == "" && requiresApproval {
			return baseDecision("block", fmt.Sprintf("%s is approved but does not include an approval_id.", kind), request.ActionType, target, requested, pack, "release_governance.approval.missing", "critical", "Release Governance")
		}
		return baseDecision("allow", fmt.Sprintf("%s is backed by an approved release governance approval.", kind), request.ActionType, target, requested, pack, "release_governance.approval.approved", "low", "")
	case "pending":
		return baseDecision("require_approval", fmt.Sprintf("%s is waiting for release governance approval.", kind), request.ActionType, target, requested, pack, "release_governance.approval.pending", "high", "Release Governance")
	case "denied", "rejected", "expired", "cancelled", "canceled":
		return baseDecision("block", fmt.Sprintf("%s is bound to a non-approved approval state: %s.", kind, approvalState), request.ActionType, target, requested, pack, "release_governance.approval.denied", "critical", "Release Governance")
	case "":
		if deliveryFailed(record) {
			return baseDecision("block", fmt.Sprintf("%s includes failed release delivery evidence.", kind), request.ActionType, target, requested, pack, "release_governance.delivery.failed", "high", "Release Governance")
		}
		if criticalReleaseSignal(record) {
			return baseDecision("require_approval", fmt.Sprintf("%s contains critical release governance signals.", kind), request.ActionType, target, requested, pack, "release_governance.signal.critical", "high", "Release Governance")
		}
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
		if knownReleaseGovernanceKind(kind) {
			return baseDecision("allow", fmt.Sprintf("%s is recognized release governance evidence with no blocking signal.", kind), request.ActionType, target, requested, pack, "release_governance.record.verified", "low", "")
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
		"endpoint-remediation-handoff",
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

func knownReleaseGovernanceKind(kind string) bool {
	switch kind {
	case "endpoint-inventory-ingestion",
		"endpoint-inventory-freshness-report",
		"managed-endpoint-reconciliation",
		"endpoint-management-export",
		"endpoint-management-publication-delivery",
		"endpoint-reconciliation-automation",
		"endpoint-drift-remediation-request",
		"endpoint-drift-remediation-execution",
		"endpoint-remediation-handoff",
		"endpoint-remediation-handoff-status",
		"endpoint-remediation-sla-report",
		"endpoint-remediation-sla-notification-plan",
		"endpoint-remediation-sla-notification-ack",
		"endpoint-remediation-sla-escalation-plan",
		"endpoint-remediation-sla-escalation-review",
		"endpoint-remediation-sla-escalation-recurrence-plan",
		"endpoint-remediation-sla-escalation-suppression-audit",
		"endpoint-remediation-sla-escalation-recurrence-retry-plan",
		"endpoint-remediation-sla-escalation-owner-digest",
		"endpoint-remediation-sla-escalation-suppression-trend",
		"endpoint-remediation-sla-escalation-recurrence-automation-run",
		"endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan",
		"endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack",
		"release-channel-promotion-request",
		"release-connector-delivery",
		"rollout-promotion-execution",
		"rollout-rollback-execution":
		return true
	default:
		return false
	}
}

func deliveryFailed(record map[string]any) bool {
	if !knownDeliveryKind(stringValue(record, "metadata_kind")) {
		return false
	}
	if boolValue(record, "delivery_success") {
		return false
	}
	return true
}

func knownDeliveryKind(kind string) bool {
	switch kind {
	case "endpoint-management-publication-delivery",
		"release-connector-delivery":
		return true
	default:
		return false
	}
}

func criticalReleaseSignal(record map[string]any) bool {
	if alertLevel := normalizeState(stringValue(record, "alert_level")); alertLevel == "critical" || alertLevel == "blocked" || alertLevel == "breached" {
		return true
	}
	if driftStatus := normalizeState(stringValue(record, "drift_status")); driftStatus == "drifted" || driftStatus == "non_compliant" {
		return true
	}
	if handoffStatus := normalizeState(stringValue(record, "handoff_status")); handoffStatus == "blocked" || handoffStatus == "failed" {
		return true
	}
	return intValue(record, "blocked_count") > 0 ||
		intValue(record, "critical_count") > 0 ||
		intValue(record, "breached_count") > 0 ||
		intValue(record, "failed_delivery_count") > 0 ||
		intValue(record, "connector_delivery_failure_count") > 0
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

func boolValue(record map[string]any, key string) bool {
	if record == nil {
		return false
	}
	value, ok := record[key]
	if !ok || value == nil {
		return false
	}
	switch typed := value.(type) {
	case bool:
		return typed
	case string:
		normalized := normalizeState(typed)
		return normalized == "true" || normalized == "yes" || normalized == "success" || normalized == "succeeded"
	default:
		return strings.EqualFold(fmt.Sprint(typed), "true")
	}
}

func normalizeState(value string) string {
	return strings.ToLower(strings.ReplaceAll(strings.TrimSpace(value), "-", "_"))
}
