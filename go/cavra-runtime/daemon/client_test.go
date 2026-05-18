package daemon

import (
	"net"
	"path/filepath"
	"testing"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

func TestClientEvaluateUsesUnixSocketDaemon(t *testing.T) {
	socketPath := filepath.Join(t.TempDir(), "cavra-runtime.sock")
	listener, err := net.Listen("unix", socketPath)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	go func() {
		_ = Serve(listener, RuntimeEvaluator(nil))
	}()

	response, err := NewClient(socketPath).Evaluate(enforcementv1.EvaluateRequest{
		SessionID:          "session-client",
		AgentID:            "frontend-agent",
		Actor:              "developer@example.com",
		ActionType:         "execute_command",
		Target:             "terraform plan",
		RequestedOperation: "terraform plan",
		PolicyPack:         "cavra-ai-agent-baseline",
	})
	if err != nil {
		t.Fatal(err)
	}
	if response.Decision != "allow" {
		t.Fatalf("decision mismatch: got %q", response.Decision)
	}
	if response.SessionID != "session-client" {
		t.Fatalf("session id mismatch: got %q", response.SessionID)
	}
	if response.AgentID != "frontend-agent" {
		t.Fatalf("agent id mismatch: got %q", response.AgentID)
	}
}

func TestClientRequiresSocketPath(t *testing.T) {
	_, err := Client{}.Evaluate(enforcementv1.EvaluateRequest{})
	if err == nil {
		t.Fatal("expected missing socket path error")
	}
}
