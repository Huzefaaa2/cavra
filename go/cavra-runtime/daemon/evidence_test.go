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
	if len(response.EvidenceRefs) != 2 {
		t.Fatalf("evidence refs mismatch: %+v", response.EvidenceRefs)
	}
	if !strings.HasPrefix(response.EvidenceRefs[0], "evidence://session-server/") {
		t.Fatalf("unexpected runtime evidence ref: %q", response.EvidenceRefs[0])
	}
	if !strings.HasPrefix(response.EvidenceRefs[1], "go-daemon-evidence://") {
		t.Fatalf("unexpected daemon evidence ref: %q", response.EvidenceRefs[1])
	}
	records := readEvidenceRecords(t, evidencePath)
	if len(records) != 1 {
		t.Fatalf("record count mismatch: got %d", len(records))
	}
	if records[0].Response.EvidenceRefs[1] != response.EvidenceRefs[1] {
		t.Fatalf("record evidence ref mismatch: got %+v", records[0].Response.EvidenceRefs)
	}
}

func TestEvidenceRecorderWritesSignedHashChainedStream(t *testing.T) {
	evidencePath := filepath.Join(t.TempDir(), "daemon-evidence.jsonl")
	recorder := NewEvidenceRecorder(evidencePath).WithSigningKey("evidence-secret", "evidence-key-1")
	recorder.Clock = func() time.Time {
		return time.Date(2026, 5, 18, 12, 0, 0, 0, time.UTC)
	}

	request := enforcementv1.EvaluateRequest{
		SessionID:          "session-signed",
		ActionType:         "execute_command",
		Target:             "terraform plan",
		RequestedOperation: "terraform plan",
	}
	if _, err := recorder.Record(request, enforcementv1.DecisionResponse{Decision: "allow"}); err != nil {
		t.Fatal(err)
	}
	if _, err := recorder.Record(request, enforcementv1.DecisionResponse{Decision: "allow"}); err != nil {
		t.Fatal(err)
	}

	records := readEvidenceRecords(t, evidencePath)
	if len(records) != 2 {
		t.Fatalf("record count mismatch: got %d", len(records))
	}
	if records[0].Sequence != 1 || records[1].Sequence != 2 {
		t.Fatalf("sequence mismatch: %+v %+v", records[0].Sequence, records[1].Sequence)
	}
	if records[0].RecordHash == "" || records[1].RecordHash == "" {
		t.Fatal("expected record hashes")
	}
	if records[1].PreviousHash != records[0].RecordHash {
		t.Fatalf("previous hash mismatch: got %q want %q", records[1].PreviousHash, records[0].RecordHash)
	}
	for _, record := range records {
		if record.Signature == nil {
			t.Fatal("expected evidence signature")
		}
		if record.Signature.Algorithm != "HMAC-SHA256" {
			t.Fatalf("signature algorithm mismatch: %q", record.Signature.Algorithm)
		}
		if record.Signature.KeyID != "evidence-key-1" {
			t.Fatalf("signature key id mismatch: %q", record.Signature.KeyID)
		}
		if record.Signature.Value == "" {
			t.Fatal("expected signature value")
		}
	}
}

func TestVerifyEvidenceStreamValidatesHashChainAndSignature(t *testing.T) {
	evidencePath := filepath.Join(t.TempDir(), "daemon-evidence.jsonl")
	recorder := NewEvidenceRecorder(evidencePath).WithSigningKey("evidence-secret", "evidence-key-1")
	recorder.Clock = func() time.Time {
		return time.Date(2026, 5, 18, 12, 0, 0, 0, time.UTC)
	}
	request := enforcementv1.EvaluateRequest{SessionID: "session-verify", ActionType: "execute_command"}
	if _, err := recorder.Record(request, enforcementv1.DecisionResponse{Decision: "allow"}); err != nil {
		t.Fatal(err)
	}
	if _, err := recorder.Record(request, enforcementv1.DecisionResponse{Decision: "allow"}); err != nil {
		t.Fatal(err)
	}
	report, err := VerifyEvidenceStream(evidencePath, "evidence-secret", "evidence-key-1")
	if err != nil {
		t.Fatal(err)
	}
	if !report.Valid {
		t.Fatalf("expected valid report: %+v", report)
	}
	if report.Records != 2 || report.SignedRecords != 2 {
		t.Fatalf("report counts mismatch: %+v", report)
	}
	report, err = VerifyEvidenceStream(evidencePath, "wrong-secret", "evidence-key-1")
	if err != nil {
		t.Fatal(err)
	}
	if report.Valid {
		t.Fatal("expected wrong signing key to invalidate evidence stream")
	}
}

func TestEvidenceRecorderRedactsOIDCToken(t *testing.T) {
	evidencePath := filepath.Join(t.TempDir(), "daemon-evidence.jsonl")
	request := enforcementv1.EvaluateRequest{
		SessionID: "session-oidc",
		RunnerAuth: &enforcementv1.RunnerAuthentication{
			Algorithm: RunnerAuthOIDCAlgorithm,
			Signature: "header.claims.signature",
			Identity: enforcementv1.RunnerIdentity{
				Provider:   "github-actions",
				Repository: "Huzefaaa2/cavra",
			},
		},
	}
	if _, err := NewEvidenceRecorder(evidencePath).Record(request, enforcementv1.DecisionResponse{Decision: "allow"}); err != nil {
		t.Fatal(err)
	}
	records := readEvidenceRecords(t, evidencePath)
	if records[0].Request.RunnerAuth.Signature != "<redacted-oidc-jwt>" {
		t.Fatalf("expected redacted OIDC token, got %q", records[0].Request.RunnerAuth.Signature)
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
