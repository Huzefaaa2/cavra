package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"syscall"
	"time"

	"github.com/Huzefaaa2/cavra/go/cavra-runtime/daemon"
	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
	cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"
)

func main() {
	inputPath := flag.String("input", "-", "JSON request file, or - for stdin")
	policyPath := flag.String("policy", "", "compiled policy JSON file from `cavra policy compile`; built-in scaffold policy is used when omitted")
	registryPath := flag.String("registry", "", "CAVRA trust registry JSON file for registry-backed MCP decisions")
	serve := flag.Bool("serve", false, "serve the generated enforcement contract over a local Unix socket")
	clientMode := flag.Bool("daemon", false, "send an EvaluateRequest to a running local daemon and print the DecisionResponse")
	lifecycle := flag.String("lifecycle", "", "manage daemon lifecycle: start, stop, or status")
	socketPath := flag.String("socket", ".cavra/cavra-runtime.sock", "Unix socket path for --serve, --daemon, or --lifecycle")
	pidPath := flag.String("pid", "", "PID file path for --lifecycle; defaults to <socket>.pid")
	lifecycleTimeout := flag.Duration("lifecycle-timeout", 5*time.Second, "timeout for daemon lifecycle readiness and shutdown")
	evidenceLogPath := flag.String("evidence-log", "", "JSONL evidence log path for daemon request/response records")
	evidenceSigningKey := flag.String("evidence-signing-key", os.Getenv("CAVRA_DAEMON_EVIDENCE_HMAC_KEY"), "optional HMAC key for chained daemon evidence signatures")
	evidenceSigningKeyID := flag.String("evidence-signing-key-id", os.Getenv("CAVRA_DAEMON_EVIDENCE_KEY_ID"), "optional key ID for chained daemon evidence signatures")
	verifyEvidence := flag.Bool("verify-evidence", false, "verify the evidence log hash chain and optional HMAC signatures, then exit")
	runnerAuthKey := flag.String("runner-auth-key", os.Getenv("CAVRA_RUNNER_AUTH_HMAC_KEY"), "optional HMAC key for CI runner authentication")
	runnerAuthKeyID := flag.String("runner-auth-key-id", os.Getenv("CAVRA_RUNNER_AUTH_KEY_ID"), "optional key ID for CI runner authentication")
	runnerAuthClaims := flag.String("runner-auth-claims", "", "optional JSON file with CI runner identity claims to sign in --daemon mode")
	runnerAuthOIDCToken := flag.String("runner-auth-oidc-token", os.Getenv("CAVRA_RUNNER_AUTH_OIDC_TOKEN"), "optional CI-provider OIDC token for runner authentication in --daemon mode")
	runnerAuthOIDCTokenFile := flag.String("runner-auth-oidc-token-file", os.Getenv("CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE"), "optional file containing a CI-provider OIDC token for runner authentication in --daemon mode")
	runnerOIDCIssuer := flag.String("runner-oidc-issuer", os.Getenv("CAVRA_RUNNER_OIDC_ISSUER"), "expected CI-provider OIDC issuer for daemon runner authentication")
	runnerOIDCAudience := flag.String("runner-oidc-audience", os.Getenv("CAVRA_RUNNER_OIDC_AUDIENCE"), "expected CI-provider OIDC audience for daemon runner authentication")
	runnerOIDCJWKSPath := flag.String("runner-oidc-jwks", os.Getenv("CAVRA_RUNNER_OIDC_JWKS"), "JWKS file path for daemon runner OIDC verification")
	runnerOIDCJWKSURL := flag.String("runner-oidc-jwks-url", os.Getenv("CAVRA_RUNNER_OIDC_JWKS_URL"), "JWKS URL for daemon runner OIDC verification")
	flag.Parse()

	if *verifyEvidence {
		runEvidenceVerifier(*evidenceLogPath, *evidenceSigningKey, *evidenceSigningKeyID)
		return
	}

	if *lifecycle != "" {
		runLifecycle(*lifecycle, daemon.LifecycleConfig{
			SocketPath:         *socketPath,
			PIDPath:            *pidPath,
			PolicyPath:         *policyPath,
			RegistryPath:       *registryPath,
			EvidenceLogPath:    *evidenceLogPath,
			EvidenceKey:        *evidenceSigningKey,
			EvidenceKeyID:      *evidenceSigningKeyID,
			RunnerAuthKey:      *runnerAuthKey,
			RunnerAuthKeyID:    *runnerAuthKeyID,
			RunnerOIDCIssuer:   *runnerOIDCIssuer,
			RunnerOIDCAudience: *runnerOIDCAudience,
			RunnerOIDCJWKSPath: *runnerOIDCJWKSPath,
			RunnerOIDCJWKSURL:  *runnerOIDCJWKSURL,
			StartupTimeout:     *lifecycleTimeout,
		})
		return
	}

	if *clientMode {
		runDaemonClient(
			*socketPath,
			*inputPath,
			*evidenceLogPath,
			*evidenceSigningKey,
			*evidenceSigningKeyID,
			*runnerAuthClaims,
			*runnerAuthKey,
			*runnerAuthKeyID,
			*runnerAuthOIDCToken,
			*runnerAuthOIDCTokenFile,
		)
		return
	}

	var policy *cavraruntime.Policy
	if *policyPath != "" {
		loadedPolicy, err := cavraruntime.LoadCompiledPolicy(*policyPath)
		if err != nil {
			fail(err)
		}
		policy = &loadedPolicy
	}
	var registry *cavraruntime.TrustRegistry
	if *registryPath != "" {
		loadedRegistry, err := cavraruntime.LoadTrustRegistry(*registryPath)
		if err != nil {
			fail(err)
		}
		registry = &loadedRegistry
	}
	if *serve {
		serveUnixSocket(
			*socketPath,
			policy,
			registry,
			*evidenceLogPath,
			*evidenceSigningKey,
			*evidenceSigningKeyID,
			*runnerAuthKey,
			*runnerAuthKeyID,
			*runnerOIDCIssuer,
			*runnerOIDCAudience,
			*runnerOIDCJWKSPath,
			*runnerOIDCJWKSURL,
		)
		return
	}

	reader, closeInput, err := inputReader(*inputPath)
	if err != nil {
		fail(err)
	}
	defer closeInput()

	request, err := decodeRuntimeRequest(reader)
	if err != nil {
		fail(err)
	}
	var decision cavraruntime.Decision
	switch {
	case policy != nil:
		decision = cavraruntime.EvaluateWithPolicyAndRegistry(request, *policy, registry)
	case registry != nil:
		decision = cavraruntime.EvaluateWithRegistry(request, *registry)
	default:
		decision = cavraruntime.Evaluate(request)
	}
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(decision); err != nil {
		fail(err)
	}
}

func decodeRuntimeRequest(reader io.Reader) (cavraruntime.Request, error) {
	data, err := io.ReadAll(reader)
	if err != nil {
		return cavraruntime.Request{}, err
	}
	var contractRequest enforcementv1.EvaluateRequest
	if err := json.Unmarshal(data, &contractRequest); err == nil && contractRequest.ReleaseGovernance != nil {
		return contractRequest.RuntimeRequest(), nil
	}
	var request cavraruntime.Request
	if err := json.Unmarshal(data, &request); err != nil {
		return cavraruntime.Request{}, err
	}
	return request, nil
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}

func inputReader(inputPath string) (io.Reader, func(), error) {
	if inputPath == "-" {
		return os.Stdin, func() {}, nil
	}
	file, err := os.Open(inputPath)
	if err != nil {
		return nil, nil, err
	}
	return file, func() {
		_ = file.Close()
	}, nil
}

func runDaemonClient(
	socket string,
	inputPath string,
	evidenceLogPath string,
	evidenceSigningKey string,
	evidenceSigningKeyID string,
	runnerAuthClaims string,
	runnerAuthKey string,
	runnerAuthKeyID string,
	runnerAuthOIDCToken string,
	runnerAuthOIDCTokenFile string,
) {
	reader, closeInput, err := inputReader(inputPath)
	if err != nil {
		fail(err)
	}
	defer closeInput()
	var request enforcementv1.EvaluateRequest
	if err := json.NewDecoder(reader).Decode(&request); err != nil {
		fail(err)
	}
	if runnerAuthClaims != "" {
		identity, err := loadRunnerIdentity(runnerAuthClaims)
		if err != nil {
			fail(err)
		}
		oidcToken, err := loadRunnerOIDCToken(runnerAuthOIDCToken, runnerAuthOIDCTokenFile)
		if err != nil {
			fail(err)
		}
		var auth enforcementv1.RunnerAuthentication
		if oidcToken != "" {
			auth, err = daemon.BuildRunnerOIDCAuthentication(identity, oidcToken)
		} else {
			auth, err = daemon.SignRunnerAuthentication(identity, runnerAuthKey, runnerAuthKeyID)
		}
		if err != nil {
			fail(err)
		}
		request.RunnerAuth = &auth
	}
	response, err := daemon.NewClient(socket).Evaluate(request)
	if err != nil {
		fail(err)
	}
	response, err = daemon.NewEvidenceRecorder(evidenceLogPath).
		WithSigningKey(evidenceSigningKey, evidenceSigningKeyID).
		Record(request, response)
	if err != nil {
		fail(err)
	}
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(response); err != nil {
		fail(err)
	}
}

func loadRunnerIdentity(path string) (enforcementv1.RunnerIdentity, error) {
	reader, closeInput, err := inputReader(path)
	if err != nil {
		return enforcementv1.RunnerIdentity{}, err
	}
	defer closeInput()
	var identity enforcementv1.RunnerIdentity
	if err := json.NewDecoder(reader).Decode(&identity); err != nil {
		return enforcementv1.RunnerIdentity{}, err
	}
	return identity, nil
}

func loadRunnerOIDCToken(token string, tokenPath string) (string, error) {
	if strings.TrimSpace(token) != "" {
		return strings.TrimSpace(token), nil
	}
	if strings.TrimSpace(tokenPath) == "" {
		return "", nil
	}
	data, err := os.ReadFile(tokenPath)
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(data)), nil
}

func runEvidenceVerifier(evidenceLogPath string, signingKey string, signingKeyID string) {
	if evidenceLogPath == "" {
		fail(fmt.Errorf("--evidence-log is required with --verify-evidence"))
	}
	report, err := daemon.VerifyEvidenceStream(evidenceLogPath, signingKey, signingKeyID)
	if err != nil {
		fail(err)
	}
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(report); err != nil {
		fail(err)
	}
	if !report.Valid {
		os.Exit(1)
	}
}

func runLifecycle(action string, config daemon.LifecycleConfig) {
	var (
		status daemon.LifecycleStatus
		err    error
	)
	switch action {
	case "start":
		status, err = daemon.StartDaemon(config)
	case "stop":
		status, err = daemon.StopDaemon(config)
	case "status":
		status, err = daemon.StatusDaemon(config)
	default:
		fail(fmt.Errorf("unknown lifecycle action %q; expected start, stop, or status", action))
	}
	if err != nil {
		fail(err)
	}
	data, err := status.JSON()
	if err != nil {
		fail(err)
	}
	fmt.Println(string(data))
}

func serveUnixSocket(
	socket string,
	policy *cavraruntime.Policy,
	registry *cavraruntime.TrustRegistry,
	evidenceLogPath string,
	evidenceSigningKey string,
	evidenceSigningKeyID string,
	runnerAuthKey string,
	runnerAuthKeyID string,
	runnerOIDCIssuer string,
	runnerOIDCAudience string,
	runnerOIDCJWKSPath string,
	runnerOIDCJWKSURL string,
) {
	if err := os.MkdirAll(filepath.Dir(socket), 0o755); err != nil {
		fail(err)
	}
	_ = os.Remove(socket)
	listener, err := net.Listen("unix", socket)
	if err != nil {
		fail(err)
	}
	defer listener.Close()
	defer os.Remove(socket)
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, os.Interrupt, syscall.SIGTERM)
	defer signal.Stop(signals)
	go func() {
		<-signals
		_ = listener.Close()
	}()
	recorder := daemon.NewEvidenceRecorder(evidenceLogPath).WithSigningKey(evidenceSigningKey, evidenceSigningKeyID)
	authenticator := daemon.RunnerAuthenticator{
		HMACKey: runnerAuthKey,
		KeyID:   runnerAuthKeyID,
		OIDCVerifier: &daemon.RunnerOIDCVerifier{
			Issuer:   runnerOIDCIssuer,
			Audience: runnerOIDCAudience,
			JWKSPath: runnerOIDCJWKSPath,
			JWKSURL:  runnerOIDCJWKSURL,
		},
	}
	if err := daemon.ServeWithSecurity(listener, daemon.RuntimeEvaluatorWithRegistry(policy, registry), recorder, authenticator); err != nil {
		fail(err)
	}
}
