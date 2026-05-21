package daemon

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"strings"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

const RunnerAuthAlgorithm = "HMAC-SHA256"

type RunnerAuthenticator struct {
	HMACKey string
	KeyID   string
}

func (auth RunnerAuthenticator) Enabled() bool {
	return auth.HMACKey != ""
}

func (auth RunnerAuthenticator) Validate(request enforcementv1.EvaluateRequest) error {
	if !auth.Enabled() {
		return nil
	}
	if request.RunnerAuth == nil {
		return errors.New("runner_auth is required")
	}
	runnerAuth := *request.RunnerAuth
	if runnerAuth.Algorithm != RunnerAuthAlgorithm {
		return fmt.Errorf("runner_auth algorithm must be %s", RunnerAuthAlgorithm)
	}
	if auth.KeyID != "" && runnerAuth.KeyID != auth.KeyID {
		return fmt.Errorf("runner_auth key_id mismatch: %s", runnerAuth.KeyID)
	}
	if strings.TrimSpace(runnerAuth.Signature) == "" {
		return errors.New("runner_auth signature is required")
	}
	expected := SignRunnerIdentity(runnerAuth.Identity, auth.HMACKey)
	if !hmac.Equal([]byte(strings.ToLower(runnerAuth.Signature)), []byte(expected)) {
		return errors.New("runner_auth signature is invalid")
	}
	if runnerAuth.Identity.Provider == "" || runnerAuth.Identity.Repository == "" {
		return errors.New("runner_auth identity requires provider and repository")
	}
	return nil
}

func SignRunnerAuthentication(
	identity enforcementv1.RunnerIdentity,
	key string,
	keyID string,
) (enforcementv1.RunnerAuthentication, error) {
	if key == "" {
		return enforcementv1.RunnerAuthentication{}, errors.New("runner auth HMAC key is required")
	}
	if identity.Provider == "" || identity.Repository == "" {
		return enforcementv1.RunnerAuthentication{}, errors.New("runner auth identity requires provider and repository")
	}
	return enforcementv1.RunnerAuthentication{
		Identity:  identity,
		Algorithm: RunnerAuthAlgorithm,
		KeyID:     keyID,
		Signature: SignRunnerIdentity(identity, key),
	}, nil
}

func SignRunnerIdentity(identity enforcementv1.RunnerIdentity, key string) string {
	mac := hmac.New(sha256.New, []byte(key))
	mac.Write([]byte(runnerIdentitySigningPayload(identity)))
	return hex.EncodeToString(mac.Sum(nil))
}

func runnerIdentitySigningPayload(identity enforcementv1.RunnerIdentity) string {
	fields := []string{
		"cavra.runner-auth.v1",
		"provider=" + identity.Provider,
		"repository=" + identity.Repository,
		"workflow=" + identity.Workflow,
		"run_id=" + identity.RunID,
		"run_attempt=" + identity.RunAttempt,
		"ref=" + identity.Ref,
		"sha=" + identity.SHA,
		"actor=" + identity.Actor,
		"job=" + identity.Job,
		"runner_name=" + identity.RunnerName,
	}
	return strings.Join(fields, "\n")
}

func RunnerAuthBlockedResponse(
	request enforcementv1.EvaluateRequest,
	authErr error,
) enforcementv1.DecisionResponse {
	reason := "runner authentication failed"
	if authErr != nil {
		reason = reason + ": " + authErr.Error()
	}
	return enforcementv1.DecisionResponse{
		SessionID:          request.SessionID,
		AgentID:            request.AgentID,
		Actor:              request.Actor,
		ActionType:         request.ActionType,
		Target:             request.Target,
		RequestedOperation: request.RequestedOperation,
		PolicyPack:         request.PolicyPack,
		RuleID:             "runner_auth.invalid",
		Decision:           "block",
		Severity:           "critical",
		Reason:             reason,
	}
}
