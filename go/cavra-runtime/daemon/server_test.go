package daemon

import (
	"encoding/json"
	"net"
	"testing"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
	cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"
)

func TestHandleConnectionEvaluatesContractRequest(t *testing.T) {
	server, client := net.Pipe()
	done := make(chan error, 1)
	go func() {
		done <- HandleConnection(server, RuntimeEvaluator(nil))
	}()

	request := enforcementv1.EvaluateRequest{
		SessionID:          "session-1",
		AgentID:            "codex-agent",
		Actor:              "developer@example.com",
		ActionType:         "execute_command",
		Target:             "terraform plan",
		RequestedOperation: "terraform plan",
		PolicyPack:         "cavra-ai-agent-baseline",
	}
	if err := json.NewEncoder(client).Encode(request); err != nil {
		t.Fatal(err)
	}

	var response enforcementv1.DecisionResponse
	if err := json.NewDecoder(client).Decode(&response); err != nil {
		t.Fatal(err)
	}
	if err := <-done; err != nil {
		t.Fatal(err)
	}
	if response.Decision != "allow" {
		t.Fatalf("decision mismatch: got %q", response.Decision)
	}
	if response.SessionID != "session-1" {
		t.Fatalf("session id mismatch: got %q", response.SessionID)
	}
	if response.RequestedOperation != "terraform plan" {
		t.Fatalf("requested operation mismatch: got %q", response.RequestedOperation)
	}
}

func TestRuntimeEvaluatorUsesCompiledPolicy(t *testing.T) {
	policy, err := cavraruntime.LoadCompiledPolicy("../testdata/compiled_policy.json")
	if err != nil {
		t.Fatal(err)
	}
	response := RuntimeEvaluator(&policy)(enforcementv1.EvaluateRequest{
		ActionType: "read_file",
		Target:     "config/prod.secret",
	})
	if response.Decision != "block" {
		t.Fatalf("decision mismatch: got %q", response.Decision)
	}
	if response.PolicyPack != "cavra-go-compiled-fixture" {
		t.Fatalf("policy pack mismatch: got %q", response.PolicyPack)
	}
}
