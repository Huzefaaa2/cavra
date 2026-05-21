package daemon

import (
	"bufio"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
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

type EvidenceVerificationReport struct {
	Path          string   `json:"path"`
	Valid         bool     `json:"valid"`
	Records       int      `json:"records"`
	SignedRecords int      `json:"signed_records"`
	Errors        []string `json:"errors,omitempty"`
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
		Request:       evidenceSafeRequest(request),
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

func VerifyEvidenceStream(path string, signingKey string, signingKeyID string) (EvidenceVerificationReport, error) {
	report := EvidenceVerificationReport{Path: path, Valid: true}
	file, err := os.Open(path)
	if err != nil {
		return report, err
	}
	defer file.Close()

	var previousHash string
	expectedSequence := 1
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		report.Records++
		var record EvidenceRecord
		if err := json.Unmarshal([]byte(line), &record); err != nil {
			report.Valid = false
			report.Errors = append(report.Errors, fmt.Sprintf("record %d is not valid JSON: %v", report.Records, err))
			continue
		}
		if record.SchemaVersion != EvidenceSchemaVersion {
			report.Valid = false
			report.Errors = append(report.Errors, fmt.Sprintf("record %d schema mismatch: %s", report.Records, record.SchemaVersion))
		}
		if record.Sequence != expectedSequence {
			report.Valid = false
			report.Errors = append(report.Errors, fmt.Sprintf("record %d sequence mismatch: got %d want %d", report.Records, record.Sequence, expectedSequence))
		}
		if record.PreviousHash != previousHash {
			report.Valid = false
			report.Errors = append(report.Errors, fmt.Sprintf("record %d previous hash mismatch", report.Records))
		}
		expectedHash := evidenceRecordHash(record)
		if record.RecordHash != expectedHash {
			report.Valid = false
			report.Errors = append(report.Errors, fmt.Sprintf("record %d hash mismatch", report.Records))
		}
		if record.Signature != nil {
			report.SignedRecords++
			if record.Signature.Algorithm != "HMAC-SHA256" {
				report.Valid = false
				report.Errors = append(report.Errors, fmt.Sprintf("record %d signature algorithm mismatch", report.Records))
			}
			if signingKey == "" {
				report.Valid = false
				report.Errors = append(report.Errors, fmt.Sprintf("record %d signature present but verification key was not provided", report.Records))
			} else {
				if signingKeyID != "" && record.Signature.KeyID != signingKeyID {
					report.Valid = false
					report.Errors = append(report.Errors, fmt.Sprintf("record %d signature key_id mismatch", report.Records))
				}
				expectedSignature := signEvidenceRecord(record, signingKey)
				if !hmac.Equal([]byte(strings.ToLower(record.Signature.Value)), []byte(expectedSignature)) {
					report.Valid = false
					report.Errors = append(report.Errors, fmt.Sprintf("record %d signature mismatch", report.Records))
				}
			}
		}
		previousHash = record.RecordHash
		expectedSequence++
	}
	if err := scanner.Err(); err != nil {
		return report, err
	}
	if report.Records == 0 {
		report.Valid = false
		report.Errors = append(report.Errors, "evidence stream is empty")
	}
	return report, nil
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

func evidenceSafeRequest(request enforcementv1.EvaluateRequest) enforcementv1.EvaluateRequest {
	if request.RunnerAuth == nil || request.RunnerAuth.Algorithm != RunnerAuthOIDCAlgorithm {
		return request
	}
	copyRequest := request
	copyAuth := *request.RunnerAuth
	copyAuth.Signature = "<redacted-oidc-jwt>"
	copyRequest.RunnerAuth = &copyAuth
	return copyRequest
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
