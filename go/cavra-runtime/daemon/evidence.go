package daemon

import (
	"bufio"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

const EvidenceSchemaVersion = "cavra.go-daemon.evidence.v1"

type EvidenceRecorder struct {
	Path         string
	Clock        func() time.Time
	SigningKey   string
	SigningKeyID string
	sequence     int
	previousHash string
	mu           sync.Mutex
}

type EvidenceRecord struct {
	SchemaVersion string                         `json:"schema_version"`
	Product       string                         `json:"product"`
	EventType     string                         `json:"event_type"`
	RecordID      string                         `json:"record_id"`
	Sequence      int                            `json:"sequence"`
	PreviousHash  string                         `json:"previous_hash,omitempty"`
	RecordHash    string                         `json:"record_hash,omitempty"`
	Timestamp     string                         `json:"timestamp"`
	Request       enforcementv1.EvaluateRequest  `json:"request"`
	Response      enforcementv1.DecisionResponse `json:"response"`
	Signature     *EvidenceSignature             `json:"signature,omitempty"`
}

type EvidenceSignature struct {
	Algorithm string `json:"algorithm"`
	KeyID     string `json:"key_id,omitempty"`
	Value     string `json:"value"`
}

func NewEvidenceRecorder(path string) *EvidenceRecorder {
	if path == "" {
		return nil
	}
	return &EvidenceRecorder{Path: path}
}

func (recorder *EvidenceRecorder) WithSigningKey(key string, keyID string) *EvidenceRecorder {
	if recorder == nil {
		return nil
	}
	recorder.SigningKey = key
	recorder.SigningKeyID = keyID
	return recorder
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
	recorder.mu.Lock()
	defer recorder.mu.Unlock()
	if err := os.MkdirAll(filepath.Dir(recorder.Path), 0o755); err != nil {
		return response, err
	}
	if err := recorder.loadStreamState(); err != nil {
		return response, err
	}
	record.Sequence = recorder.sequence + 1
	record.PreviousHash = recorder.previousHash
	record.RecordHash = evidenceRecordHash(record)
	if recorder.SigningKey != "" {
		record.Signature = &EvidenceSignature{
			Algorithm: "HMAC-SHA256",
			KeyID:     recorder.SigningKeyID,
			Value:     signEvidenceRecord(record, recorder.SigningKey),
		}
	}
	data, err := json.Marshal(record)
	if err != nil {
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
	recorder.sequence = record.Sequence
	recorder.previousHash = record.RecordHash
	return response, nil
}

func (recorder *EvidenceRecorder) loadStreamState() error {
	if recorder.sequence > 0 || recorder.previousHash != "" {
		return nil
	}
	file, err := os.Open(recorder.Path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil
		}
		return err
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		var record EvidenceRecord
		if err := json.Unmarshal([]byte(line), &record); err != nil {
			return err
		}
		recorder.sequence = record.Sequence
		recorder.previousHash = record.RecordHash
	}
	return scanner.Err()
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

func evidenceRecordHash(record EvidenceRecord) string {
	record.RecordHash = ""
	record.Signature = nil
	data, _ := json.Marshal(record)
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

func signEvidenceRecord(record EvidenceRecord, key string) string {
	mac := hmac.New(sha256.New, []byte(key))
	mac.Write([]byte(EvidenceSchemaVersion))
	mac.Write([]byte("\n"))
	mac.Write([]byte(record.PreviousHash))
	mac.Write([]byte("\n"))
	mac.Write([]byte(record.RecordHash))
	return hex.EncodeToString(mac.Sum(nil))
}
