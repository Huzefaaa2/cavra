package v1

import (
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
