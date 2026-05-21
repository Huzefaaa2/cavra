package daemon

import (
	"testing"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

func TestRunnerAuthenticatorAcceptsSignedIdentity(t *testing.T) {
	identity := enforcementv1.RunnerIdentity{
		Provider:   "github-actions",
		Repository: "Huzefaaa2/cavra",
		Workflow:   "CAVRA Release Governance",
		RunID:      "123",
		Ref:        "refs/heads/main",
		SHA:        "abc123",
		Actor:      "release-bot",
		Job:        "cavra-release-governance",
		RunnerName: "ubuntu-latest",
	}
	auth, err := SignRunnerAuthentication(identity, "runner-secret", "runner-key-1")
	if err != nil {
		t.Fatal(err)
	}
	request := enforcementv1.EvaluateRequest{RunnerAuth: &auth}
	if err := (RunnerAuthenticator{HMACKey: "runner-secret", KeyID: "runner-key-1"}).Validate(request); err != nil {
		t.Fatal(err)
	}
}

func TestRunnerAuthenticatorRejectsMissingAndTamperedIdentity(t *testing.T) {
	authenticator := RunnerAuthenticator{HMACKey: "runner-secret", KeyID: "runner-key-1"}
	if err := authenticator.Validate(enforcementv1.EvaluateRequest{}); err == nil {
		t.Fatal("expected missing runner auth to fail")
	}
	auth, err := SignRunnerAuthentication(
		enforcementv1.RunnerIdentity{Provider: "github-actions", Repository: "Huzefaaa2/cavra"},
		"runner-secret",
		"runner-key-1",
	)
	if err != nil {
		t.Fatal(err)
	}
	auth.Identity.Repository = "attacker/repo"
	if err := authenticator.Validate(enforcementv1.EvaluateRequest{RunnerAuth: &auth}); err == nil {
		t.Fatal("expected tampered runner identity to fail")
	}
}
