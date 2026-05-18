package daemon

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"sync"
	"time"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

const EvidenceSchemaVersion = "cavra.go-daemon.evidence.v1"

type EvidenceRecorder struct {
	Path  string
	Clock func() time.Time
	mu    sync.Mutex
}

type EvidenceRecord struct {
	SchemaVersion string                         `json:"schema_version"`
	Product       string                         `json:"product"`
	EventType     string                         `json:"event_type"`
	RecordID      string                         `json:"record_id"`
	Timestamp     string                         `json:"timestamp"`
	Request       enforcementv1.EvaluateRequest  `json:"request"`
	Response      enforcementv1.DecisionResponse `json:"response"`
}

func NewEvidenceRecorder(path string) *EvidenceRecorder {
	if path == "" {
		return nil
	}
	return &EvidenceRecorder{Path: path}
}

func (recorder *EvidenceRecorder) Record(request enforcementv1.EvaluateRequest, response enforcementv1.DecisionResponse) (enforcementv1.DecisionResponse, error) {
	if recorder == nil || recorder.Path == "" {
		return response, nil
	}
	now := time.Now().UTC()
	if recorder.Clock != nil {
		now = recorder.Clock().UTC()
	}
	recordID := evidenceRecordID(request, response, now)
	response.EvidenceRefs = appendEvidenceRef(response.EvidenceRefs, "go-daemon-evidence://"+recordID)
	record := EvidenceRecord{
		SchemaVersion: EvidenceSchemaVersion,
		Product:       "CAVRA",
		EventType:     "cavra.go_daemon.decision",
		RecordID:      recordID,
		Timestamp:     now.Format(time.RFC3339Nano),
		Request:       request,
		Response:      response,
	}
	data, err := json.Marshal(record)
	if err != nil {
		return response, err
	}
	recorder.mu.Lock()
	defer recorder.mu.Unlock()
	if err := os.MkdirAll(filepath.Dir(recorder.Path), 0o755); err != nil {
		return response, err
	}
	file, err := os.OpenFile(recorder.Path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o644)
	if err != nil {
		return response, err
	}
	defer file.Close()
	if _, err := file.Write(append(data, '\n')); err != nil {
		return response, err
	}
	return response, nil
}

func evidenceRecordID(request enforcementv1.EvaluateRequest, response enforcementv1.DecisionResponse, timestamp time.Time) string {
	hash := sha256.New()
	encoder := json.NewEncoder(hash)
	_ = encoder.Encode(request)
	_ = encoder.Encode(response)
	_ = encoder.Encode(timestamp.Format(time.RFC3339Nano))
	return hex.EncodeToString(hash.Sum(nil))[:24]
}

func appendEvidenceRef(refs []string, ref string) []string {
	for _, existing := range refs {
		if existing == ref {
			return refs
		}
	}
	return append(refs, ref)
}
