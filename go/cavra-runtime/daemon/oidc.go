package daemon

import (
	"crypto"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math/big"
	"net/http"
	"os"
	"strings"
	"time"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

const RunnerAuthOIDCAlgorithm = "OIDC-JWT"

type RunnerOIDCVerifier struct {
	Issuer    string
	Audience  string
	JWKSPath  string
	JWKSURL   string
	Clock     func() time.Time
	Client    *http.Client
	keySet    *jwkSet
	keySetErr error
}

type oidcToken struct {
	Header map[string]any
	Claims map[string]any
	Signed string
	Sig    []byte
}

type jwkSet struct {
	Keys []jwk `json:"keys"`
}

type jwk struct {
	Kty string `json:"kty"`
	Use string `json:"use,omitempty"`
	Kid string `json:"kid,omitempty"`
	Alg string `json:"alg,omitempty"`
	N   string `json:"n,omitempty"`
	E   string `json:"e,omitempty"`
}

func (verifier *RunnerOIDCVerifier) Enabled() bool {
	return verifier != nil && verifier.Issuer != "" && verifier.Audience != "" && (verifier.JWKSPath != "" || verifier.JWKSURL != "")
}

func (verifier *RunnerOIDCVerifier) Validate(token string, identity enforcementv1.RunnerIdentity) error {
	if !verifier.Enabled() {
		return errors.New("runner OIDC verifier is not configured")
	}
	parsed, err := parseOIDCToken(token)
	if err != nil {
		return err
	}
	if err := verifier.validateClaims(parsed.Claims, identity); err != nil {
		return err
	}
	if err := verifier.verifySignature(parsed); err != nil {
		return err
	}
	return nil
}

func BuildRunnerOIDCAuthentication(
	identity enforcementv1.RunnerIdentity,
	token string,
) (enforcementv1.RunnerAuthentication, error) {
	if strings.TrimSpace(token) == "" {
		return enforcementv1.RunnerAuthentication{}, errors.New("runner OIDC token is required")
	}
	if identity.Provider == "" || identity.Repository == "" {
		return enforcementv1.RunnerAuthentication{}, errors.New("runner auth identity requires provider and repository")
	}
	parsed, err := parseOIDCToken(token)
	if err != nil {
		return enforcementv1.RunnerAuthentication{}, err
	}
	keyID, _ := parsed.Header["kid"].(string)
	return enforcementv1.RunnerAuthentication{
		Identity:  identity,
		Algorithm: RunnerAuthOIDCAlgorithm,
		KeyID:     keyID,
		Signature: strings.TrimSpace(token),
	}, nil
}

func parseOIDCToken(token string) (oidcToken, error) {
	parts := strings.Split(strings.TrimSpace(token), ".")
	if len(parts) != 3 {
		return oidcToken{}, errors.New("runner OIDC token must be a compact JWT")
	}
	headerData, err := base64.RawURLEncoding.DecodeString(parts[0])
	if err != nil {
		return oidcToken{}, fmt.Errorf("runner OIDC header is not base64url: %w", err)
	}
	claimsData, err := base64.RawURLEncoding.DecodeString(parts[1])
	if err != nil {
		return oidcToken{}, fmt.Errorf("runner OIDC claims are not base64url: %w", err)
	}
	signature, err := base64.RawURLEncoding.DecodeString(parts[2])
	if err != nil {
		return oidcToken{}, fmt.Errorf("runner OIDC signature is not base64url: %w", err)
	}
	var header map[string]any
	if err := json.Unmarshal(headerData, &header); err != nil {
		return oidcToken{}, fmt.Errorf("runner OIDC header is not JSON: %w", err)
	}
	var claims map[string]any
	if err := json.Unmarshal(claimsData, &claims); err != nil {
		return oidcToken{}, fmt.Errorf("runner OIDC claims are not JSON: %w", err)
	}
	return oidcToken{
		Header: header,
		Claims: claims,
		Signed: parts[0] + "." + parts[1],
		Sig:    signature,
	}, nil
}

func (verifier *RunnerOIDCVerifier) validateClaims(claims map[string]any, identity enforcementv1.RunnerIdentity) error {
	if claimString(claims, "iss") != verifier.Issuer {
		return fmt.Errorf("runner OIDC issuer mismatch: %q", claimString(claims, "iss"))
	}
	if !audienceContains(claims["aud"], verifier.Audience) {
		return errors.New("runner OIDC audience mismatch")
	}
	now := time.Now().UTC()
	if verifier.Clock != nil {
		now = verifier.Clock().UTC()
	}
	if exp, ok := numericDate(claims["exp"]); ok && now.After(exp) {
		return errors.New("runner OIDC token is expired")
	}
	if nbf, ok := numericDate(claims["nbf"]); ok && now.Before(nbf) {
		return errors.New("runner OIDC token is not valid yet")
	}
	if identity.Provider == "" || identity.Repository == "" {
		return errors.New("runner_auth identity requires provider and repository")
	}
	if expectedProvider := providerForIssuer(verifier.Issuer); expectedProvider != "" && identity.Provider != expectedProvider {
		return fmt.Errorf("runner OIDC provider mismatch: got %q want %q", identity.Provider, expectedProvider)
	}
	comparisons := map[string]string{
		"repository":  identity.Repository,
		"workflow":    identity.Workflow,
		"run_id":      identity.RunID,
		"run_attempt": identity.RunAttempt,
		"ref":         identity.Ref,
		"sha":         identity.SHA,
		"actor":       identity.Actor,
		"job":         identity.Job,
		"runner_name": identity.RunnerName,
	}
	for claim, expected := range comparisons {
		if expected == "" {
			continue
		}
		actual := claimString(claims, claim)
		if actual == "" {
			continue
		}
		if subtle.ConstantTimeCompare([]byte(actual), []byte(expected)) != 1 {
			return fmt.Errorf("runner OIDC claim %s mismatch", claim)
		}
	}
	if claimString(claims, "repository") == "" {
		return errors.New("runner OIDC token requires repository claim")
	}
	if claimString(claims, "repository") != identity.Repository {
		return errors.New("runner OIDC repository claim does not match runner identity")
	}
	return nil
}

func (verifier *RunnerOIDCVerifier) verifySignature(token oidcToken) error {
	alg, _ := token.Header["alg"].(string)
	if alg != "RS256" {
		return fmt.Errorf("runner OIDC alg %q is not supported; expected RS256", alg)
	}
	kid, _ := token.Header["kid"].(string)
	if kid == "" {
		return errors.New("runner OIDC token requires kid header")
	}
	keySet, err := verifier.loadKeySet()
	if err != nil {
		return err
	}
	for _, key := range keySet.Keys {
		if key.Kid != kid || key.Kty != "RSA" {
			continue
		}
		publicKey, err := key.rsaPublicKey()
		if err != nil {
			return err
		}
		digest := sha256.Sum256([]byte(token.Signed))
		if err := rsa.VerifyPKCS1v15(publicKey, crypto.SHA256, digest[:], token.Sig); err != nil {
			return errors.New("runner OIDC signature is invalid")
		}
		return nil
	}
	return fmt.Errorf("runner OIDC signing key %q was not found in JWKS", kid)
}

func (verifier *RunnerOIDCVerifier) loadKeySet() (jwkSet, error) {
	if verifier.keySet != nil || verifier.keySetErr != nil {
		if verifier.keySetErr != nil {
			return jwkSet{}, verifier.keySetErr
		}
		return *verifier.keySet, nil
	}
	var data []byte
	var err error
	switch {
	case verifier.JWKSPath != "":
		data, err = os.ReadFile(verifier.JWKSPath)
	case verifier.JWKSURL != "":
		client := verifier.Client
		if client == nil {
			client = &http.Client{Timeout: 10 * time.Second}
		}
		var response *http.Response
		response, err = client.Get(verifier.JWKSURL)
		if err == nil {
			defer response.Body.Close()
			if response.StatusCode < 200 || response.StatusCode > 299 {
				err = fmt.Errorf("JWKS URL returned %s", response.Status)
			} else {
				data, err = io.ReadAll(io.LimitReader(response.Body, 1<<20))
			}
		}
	default:
		err = errors.New("runner OIDC verifier requires JWKS path or URL")
	}
	if err != nil {
		verifier.keySetErr = err
		return jwkSet{}, err
	}
	var keys jwkSet
	if err := json.Unmarshal(data, &keys); err != nil {
		verifier.keySetErr = err
		return jwkSet{}, err
	}
	verifier.keySet = &keys
	return keys, nil
}

func (key jwk) rsaPublicKey() (*rsa.PublicKey, error) {
	modulusBytes, err := base64.RawURLEncoding.DecodeString(key.N)
	if err != nil {
		return nil, fmt.Errorf("JWKS modulus is not base64url: %w", err)
	}
	exponentBytes, err := base64.RawURLEncoding.DecodeString(key.E)
	if err != nil {
		return nil, fmt.Errorf("JWKS exponent is not base64url: %w", err)
	}
	exponent := 0
	for _, b := range exponentBytes {
		exponent = exponent<<8 + int(b)
	}
	if exponent == 0 {
		return nil, errors.New("JWKS exponent is empty")
	}
	return &rsa.PublicKey{N: new(big.Int).SetBytes(modulusBytes), E: exponent}, nil
}

func claimString(claims map[string]any, name string) string {
	if value, ok := claims[name].(string); ok {
		return value
	}
	return ""
}

func audienceContains(value any, expected string) bool {
	switch aud := value.(type) {
	case string:
		return aud == expected
	case []any:
		for _, item := range aud {
			if text, ok := item.(string); ok && text == expected {
				return true
			}
		}
	}
	return false
}

func numericDate(value any) (time.Time, bool) {
	switch number := value.(type) {
	case float64:
		return time.Unix(int64(number), 0).UTC(), true
	case json.Number:
		seconds, err := number.Int64()
		if err == nil {
			return time.Unix(seconds, 0).UTC(), true
		}
	}
	return time.Time{}, false
}

func providerForIssuer(issuer string) string {
	switch {
	case issuer == "https://token.actions.githubusercontent.com":
		return "github-actions"
	case issuer == "https://gitlab.com" || strings.Contains(issuer, "gitlab"):
		return "gitlab-ci"
	case strings.Contains(issuer, "vstoken.dev.azure.com"):
		return "azure-pipelines"
	default:
		return ""
	}
}
