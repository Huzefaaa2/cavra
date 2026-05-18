package daemon

import (
	"encoding/json"
	"net"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

func TestEvidenceRecorderWritesRequestAndResponse(t *testing.T) {
	evidencePath := filepath.Join(t.TempDir(), "daemon-evidence.jsonl")
	recorder := NewEvidenceRecorder(evidencePath)
	recorder.Clock = func() time.Time {
		return time.Date(2026, 5, 18, 12, 0, 0, 0, time.UTC)
	}

	request := enforcementv1.EvaluateRequest{
		SessionID:          "session-evidence",
		AgentID:            "codex-agent",
		ActionType:         "execute_command",
		Target:             "terraform plan",
		RequestedOperation: "terraform plan",
	}
	response, err := recorder.Record(request, enforcementv1.DecisionResponse{
		SessionID: "session-evidence",
		Decision:  "allow",
	})
	if err != nil {
		t.Fatal(err)
	}
	if len(response.EvidenceRefs) != 1 {
		t.Fatalf("evidence refs mismatch: %+v", response.EvidenceRefs)
	}
	if !strings.HasPrefix(response.EvidenceRefs[0], "go-daemon-evidence://") {
		t.Fatalf("unexpected evidence ref: %q", response.EvidenceRefs[0])
	}

	records := readEvidenceRecords(t, evidencePath)
	if len(records) != 1 {
		t.Fatalf("record count mismatch: got %d", len(records))
	}
	record := records[0]
	if record.SchemaVersion != EvidenceSchemaVersion {
		t.Fatalf("schema mismatch: got %q", record.SchemaVersion)
	}
	if record.Request.SessionID != "session-evidence" {
		t.Fatalf("request session mismatch: got %q", record.Request.SessionID)
	}
	if record.Response.EvidenceRefs[0] != response.EvidenceRefs[0] {
		t.Fatalf("record evidence ref mismatch: got %+v", record.Response.EvidenceRefs)
	}
}

func TestHandleConnectionWithEvidenceAppendsEvidenceRef(t *testing.T) {
	evidencePath := filepath.Join(t.TempDir(), "daemon-evidence.jsonl")
	server, client := net.Pipe()
	done := make(chan error, 1)
	go func() {
		done <- HandleConnectionWithEvidence(server, RuntimeEvaluator(nil), NewEvidenceRecorder(evidencePath))
	}()

	request := enforcementv1.EvaluateRequest{
		SessionID:          "session-server",
		ActionType:         "execute_command",
		Target:             "terraform plan",
		RequestedOperation: "terraform plan",
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
	if len(response.EvidenceRefs) != 1 {
		t.Fatalf("evidence refs mismatch: %+v", response.EvidenceRefs)
	}
	records := readEvidenceRecords(t, evidencePath)
	if len(records) != 1 {
		t.Fatalf("record count mismatch: got %d", len(records))
	}
	if records[0].Response.EvidenceRefs[0] != response.EvidenceRefs[0] {
		t.Fatalf("record evidence ref mismatch: got %+v", records[0].Response.EvidenceRefs)
	}
}

func readEvidenceRecords(t *testing.T, path string) []EvidenceRecord {
	t.Helper()
	lines := strings.Split(strings.TrimSpace(readFile(t, path)), "\n")
	var records []EvidenceRecord
	for _, line := range lines {
		var record EvidenceRecord
		if err := json.Unmarshal([]byte(line), &record); err != nil {
			t.Fatal(err)
		}
		records = append(records, record)
	}
	return records
}

func readFile(t *testing.T, path string) string {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	return string(data)
}
