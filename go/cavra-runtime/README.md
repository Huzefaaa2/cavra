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
PYTHONPATH=../../src python3 -m cavra.cli policy compile --policy-pack cavra-ai-agent-baseline > /tmp/cavra-compiled-policy.json
echo '{"action_type":"read_file","target":".env"}' \
  | go run ./cmd/cavra-runtime --policy /tmp/cavra-compiled-policy.json
```

`--policy` accepts normalized JSON from `cavra policy compile`. When omitted, the runtime uses the built-in scaffold policy subset for local parity tests.

Next Go work:

- Generate protobuf or JSON-RPC service boundaries for local daemon mode.
- Add Python-to-Go golden parity for every bundled policy pack, approval route, and registry-backed MCP decision.
- Package signed CI runner and air-gapped binaries only after audited parity coverage exists.
