package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net"
	"os"
	"path/filepath"

	"github.com/Huzefaaa2/cavra/go/cavra-runtime/daemon"
	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
	cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"
)

func main() {
	inputPath := flag.String("input", "-", "JSON request file, or - for stdin")
	policyPath := flag.String("policy", "", "compiled policy JSON file from `cavra policy compile`; built-in scaffold policy is used when omitted")
	serve := flag.Bool("serve", false, "serve the generated enforcement contract over a local Unix socket")
	clientMode := flag.Bool("daemon", false, "send an EvaluateRequest to a running local daemon and print the DecisionResponse")
	socketPath := flag.String("socket", ".cavra/cavra-runtime.sock", "Unix socket path for --serve or --daemon")
	flag.Parse()

	if *clientMode {
		runDaemonClient(*socketPath, *inputPath)
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
	if *serve {
		serveUnixSocket(*socketPath, policy)
		return
	}

	reader, closeInput, err := inputReader(*inputPath)
	if err != nil {
		fail(err)
	}
	defer closeInput()

	var request cavraruntime.Request
	if err := json.NewDecoder(reader).Decode(&request); err != nil {
		fail(err)
	}
	var decision cavraruntime.Decision
	if policy != nil {
		decision = cavraruntime.EvaluateWithPolicy(request, *policy)
	} else {
		decision = cavraruntime.Evaluate(request)
	}
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(decision); err != nil {
		fail(err)
	}
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

func runDaemonClient(socket string, inputPath string) {
	reader, closeInput, err := inputReader(inputPath)
	if err != nil {
		fail(err)
	}
	defer closeInput()
	var request enforcementv1.EvaluateRequest
	if err := json.NewDecoder(reader).Decode(&request); err != nil {
		fail(err)
	}
	response, err := daemon.NewClient(socket).Evaluate(request)
	if err != nil {
		fail(err)
	}
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(response); err != nil {
		fail(err)
	}
}

func serveUnixSocket(socket string, policy *cavraruntime.Policy) {
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
	if err := daemon.Serve(listener, daemon.RuntimeEvaluator(policy)); err != nil {
		fail(err)
	}
}
