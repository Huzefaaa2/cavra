# CAVRA Go Runtime

This directory contains the first Go enforcement plane parity scaffold.

The Python runtime remains authoritative. The Go package intentionally covers only the critical parity contract used by `go/cavra-runtime/testdata/parity_cases.json`:

- sensitive file reads
- approval-required file writes
- allowed and blocked commands
- protected branch Git pushes
- unknown MCP server blocks

Run the scaffold locally:

```bash
cd go/cavra-runtime
go test ./...
echo '{"action_type":"execute_command","target":"terraform plan","policy_pack":"cavra-ai-agent-baseline"}' \
  | go run ./cmd/cavra-runtime
```

Next Go work:

- Load compiled policy artifacts instead of built-in policy subsets.
- Add protobuf or JSON-RPC service boundaries for local daemon mode.
- Add Python-to-Go golden parity for every bundled policy pack.
- Package an air-gapped binary only after audited parity coverage exists.
