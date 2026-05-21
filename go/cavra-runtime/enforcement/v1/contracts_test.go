package v1

import (
	"encoding/json"
	"os"
	"regexp"
	"testing"

	cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"
)

func TestGeneratedContractsMatchProtoFields(t *testing.T) {
	data, err := os.ReadFile("../../../../proto/cavra/enforcement/v1/enforcement.proto")
	if err != nil {
		t.Fatal(err)
	}
	proto := string(data)

	assertProtoFields(t, proto, "EvaluateRequest", []string{
		"session_id",
		"agent_id",
		"actor",
		"action_type",
		"target",
		"requested_operation",
		"policy_pack",
		"release_governance",
	})
	assertProtoFields(t, proto, "ReleaseGovernanceEvidence", []string{
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
	})
	assertProtoFields(t, proto, "DecisionResponse", []string{
		"decision_id",
		"session_id",
		"agent_id",
		"actor",
		"action_type",
		"target",
		"requested_operation",
		"policy_pack",
		"policy_id",
		"rule_id",
		"decision",
		"severity",
		"reason",
		"evidence_refs",
		"approver_group",
		"timestamp",
		"correlation_id",
	})
}

func TestContractRoundTripToRuntimeTypes(t *testing.T) {
	request := EvaluateRequest{
		SessionID:          "session-1",
		AgentID:            "codex-agent",
		Actor:              "developer@example.com",
		ActionType:         "execute_command",
		Target:             "terraform plan",
		RequestedOperation: "terraform plan",
		PolicyPack:         "cavra-ai-agent-baseline",
	}
	runtimeRequest := request.RuntimeRequest()
	if runtimeRequest.RequestedOperation != "terraform plan" {
		t.Fatalf("requested operation mismatch: got %q", runtimeRequest.RequestedOperation)
	}
	decision := cavraruntime.Evaluate(runtimeRequest)
	response := DecisionResponseFromRuntime(decision)
	if response.Decision != "allow" {
		t.Fatalf("decision mismatch: got %q", response.Decision)
	}
	if response.RequestedOperation != "terraform plan" {
		t.Fatalf("requested operation mismatch: got %q", response.RequestedOperation)
	}
	if response.PolicyPack != "cavra-ai-agent-baseline" {
		t.Fatalf("policy pack mismatch: got %q", response.PolicyPack)
	}
}

func TestReleaseGovernanceContractFixtures(t *testing.T) {
	data, err := os.ReadFile("../../testdata/release_governance_contracts.json")
	if err != nil {
		t.Fatal(err)
	}
	var cases []struct {
		Name     string          `json:"name"`
		Request  EvaluateRequest `json:"request"`
		Expected struct {
			Decision      string `json:"decision"`
			RuleID        string `json:"rule_id"`
			Severity      string `json:"severity"`
			ApproverGroup string `json:"approver_group"`
		} `json:"expected"`
	}
	if err := json.Unmarshal(data, &cases); err != nil {
		t.Fatal(err)
	}
	if len(cases) == 0 {
		t.Fatal("expected release governance contract cases")
	}
	for _, item := range cases {
		t.Run(item.Name, func(t *testing.T) {
			runtimeRequest := item.Request.RuntimeRequest()
			if runtimeRequest.Record == nil {
				t.Fatalf("expected release governance contract to map into runtime record")
			}
			decision := cavraruntime.Evaluate(runtimeRequest)
			response := DecisionResponseFromRuntime(decision)
			if response.Decision != item.Expected.Decision {
				t.Fatalf("decision mismatch: got %q want %q", response.Decision, item.Expected.Decision)
			}
			if response.RuleID != item.Expected.RuleID {
				t.Fatalf("rule id mismatch: got %q want %q", response.RuleID, item.Expected.RuleID)
			}
			if response.Severity != item.Expected.Severity {
				t.Fatalf("severity mismatch: got %q want %q", response.Severity, item.Expected.Severity)
			}
			if response.ApproverGroup != item.Expected.ApproverGroup {
				t.Fatalf("approver group mismatch: got %q want %q", response.ApproverGroup, item.Expected.ApproverGroup)
			}
		})
	}
}

func assertProtoFields(t *testing.T, proto string, message string, fields []string) {
	t.Helper()
	blockPattern := regexp.MustCompile(`(?s)message\s+` + regexp.QuoteMeta(message) + `\s+\{(.*?)\}`)
	matches := blockPattern.FindStringSubmatch(proto)
	if len(matches) != 2 {
		t.Fatalf("message %s not found", message)
	}
	for _, field := range fields {
		fieldPattern := regexp.MustCompile(`\b` + regexp.QuoteMeta(field) + `\s*=`)
		if !fieldPattern.MatchString(matches[1]) {
			t.Fatalf("field %s.%s not found in proto", message, field)
		}
	}
}
