package daemon

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"math/big"
	"os"
	"path/filepath"
	"testing"
	"time"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

func TestRunnerOIDCVerifierAcceptsGitHubActionsToken(t *testing.T) {
	privateKey, jwksPath := writeTestJWKS(t)
	now := time.Date(2026, 5, 21, 12, 0, 0, 0, time.UTC)
	identity := enforcementv1.RunnerIdentity{
		Provider:   "github-actions",
		Repository: "Huzefaaa2/cavra",
		Workflow:   "CAVRA Release Governance",
		RunID:      "123",
		RunAttempt: "1",
		Ref:        "refs/heads/main",
		SHA:        "abc123",
		Actor:      "release-bot",
	}
	token := signedTestJWT(t, privateKey, map[string]any{
		"iss":         "https://token.actions.githubusercontent.com",
		"aud":         "cavra-release-governance",
		"exp":         now.Add(time.Hour).Unix(),
		"nbf":         now.Add(-time.Minute).Unix(),
		"repository":  identity.Repository,
		"workflow":    identity.Workflow,
		"run_id":      identity.RunID,
		"run_attempt": identity.RunAttempt,
		"ref":         identity.Ref,
		"sha":         identity.SHA,
		"actor":       identity.Actor,
	})
	auth, err := BuildRunnerOIDCAuthentication(identity, token)
	if err != nil {
		t.Fatal(err)
	}
	authenticator := RunnerAuthenticator{OIDCVerifier: &RunnerOIDCVerifier{
		Issuer:   "https://token.actions.githubusercontent.com",
		Audience: "cavra-release-governance",
		JWKSPath: jwksPath,
		Clock: func() time.Time {
			return now
		},
	}}
	if err := authenticator.Validate(enforcementv1.EvaluateRequest{RunnerAuth: &auth}); err != nil {
		t.Fatal(err)
	}
}

func TestRunnerOIDCVerifierRejectsClaimMismatch(t *testing.T) {
	privateKey, jwksPath := writeTestJWKS(t)
	now := time.Date(2026, 5, 21, 12, 0, 0, 0, time.UTC)
	token := signedTestJWT(t, privateKey, map[string]any{
		"iss":        "https://token.actions.githubusercontent.com",
		"aud":        "cavra-release-governance",
		"exp":        now.Add(time.Hour).Unix(),
		"repository": "attacker/repo",
	})
	auth, err := BuildRunnerOIDCAuthentication(
		enforcementv1.RunnerIdentity{Provider: "github-actions", Repository: "Huzefaaa2/cavra"},
		token,
	)
	if err != nil {
		t.Fatal(err)
	}
	err = (RunnerAuthenticator{OIDCVerifier: &RunnerOIDCVerifier{
		Issuer:   "https://token.actions.githubusercontent.com",
		Audience: "cavra-release-governance",
		JWKSPath: jwksPath,
		Clock: func() time.Time {
			return now
		},
	}}).Validate(enforcementv1.EvaluateRequest{RunnerAuth: &auth})
	if err == nil {
		t.Fatal("expected mismatched repository claim to fail")
	}
}

func writeTestJWKS(t *testing.T) (*rsa.PrivateKey, string) {
	t.Helper()
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		t.Fatal(err)
	}
	key := privateKey.PublicKey
	exponent := big.NewInt(int64(key.E)).Bytes()
	jwks := jwkSet{Keys: []jwk{{
		Kty: "RSA",
		Kid: "test-key",
		Alg: "RS256",
		N:   base64.RawURLEncoding.EncodeToString(key.N.Bytes()),
		E:   base64.RawURLEncoding.EncodeToString(exponent),
	}}}
	data, err := json.Marshal(jwks)
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(t.TempDir(), "jwks.json")
	if err := os.WriteFile(path, data, 0o644); err != nil {
		t.Fatal(err)
	}
	return privateKey, path
}

func signedTestJWT(t *testing.T, privateKey *rsa.PrivateKey, claims map[string]any) string {
	t.Helper()
	header := map[string]any{"alg": "RS256", "kid": "test-key", "typ": "JWT"}
	headerData, err := json.Marshal(header)
	if err != nil {
		t.Fatal(err)
	}
	claimsData, err := json.Marshal(claims)
	if err != nil {
		t.Fatal(err)
	}
	signed := base64.RawURLEncoding.EncodeToString(headerData) + "." +
		base64.RawURLEncoding.EncodeToString(claimsData)
	digest := sha256.Sum256([]byte(signed))
	signature, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, digest[:])
	if err != nil {
		t.Fatal(err)
	}
	return signed + "." + base64.RawURLEncoding.EncodeToString(signature)
}
