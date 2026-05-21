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
	runnerAuthKey := flag.String("runner-auth-key", os.Getenv("CAVRA_RUNNER_AUTH_HMAC_KEY"), "optional HMAC key for CI runner authentication")
	runnerAuthKeyID := flag.String("runner-auth-key-id", os.Getenv("CAVRA_RUNNER_AUTH_KEY_ID"), "optional key ID for CI runner authentication")
	runnerAuthClaims := flag.String("runner-auth-claims", "", "optional JSON file with CI runner identity claims to sign in --daemon mode")
	flag.Parse()

	if *lifecycle != "" {
		runLifecycle(*lifecycle, daemon.LifecycleConfig{
			SocketPath:      *socketPath,
			PIDPath:         *pidPath,
			PolicyPath:      *policyPath,
			RegistryPath:    *registryPath,
			EvidenceLogPath: *evidenceLogPath,
			EvidenceKey:     *evidenceSigningKey,
			EvidenceKeyID:   *evidenceSigningKeyID,
			RunnerAuthKey:   *runnerAuthKey,
			RunnerAuthKeyID: *runnerAuthKeyID,
			StartupTimeout:  *lifecycleTimeout,
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
		auth, err := daemon.SignRunnerAuthentication(identity, runnerAuthKey, runnerAuthKeyID)
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
	authenticator := daemon.RunnerAuthenticator{HMACKey: runnerAuthKey, KeyID: runnerAuthKeyID}
	if err := daemon.ServeWithSecurity(listener, daemon.RuntimeEvaluatorWithRegistry(policy, registry), recorder, authenticator); err != nil {
		fail(err)
	}
}
