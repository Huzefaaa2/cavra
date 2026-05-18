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
	cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"
)

func main() {
	inputPath := flag.String("input", "-", "JSON request file, or - for stdin")
	policyPath := flag.String("policy", "", "compiled policy JSON file from `cavra policy compile`; built-in scaffold policy is used when omitted")
	serve := flag.Bool("serve", false, "serve the generated enforcement contract over a local Unix socket")
	socketPath := flag.String("socket", ".cavra/cavra-runtime.sock", "Unix socket path for --serve")
	flag.Parse()

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

	var reader io.Reader = os.Stdin
	if *inputPath != "-" {
		file, err := os.Open(*inputPath)
		if err != nil {
			fail(err)
		}
		defer file.Close()
		reader = file
	}

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
