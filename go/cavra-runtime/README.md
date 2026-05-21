# CAVRA Go Runtime

This directory contains the first Go enforcement plane parity scaffold.

The Python runtime remains authoritative. The Go package intentionally covers only the critical parity contract used by `go/cavra-runtime/testdata/parity_cases.json`:

- sensitive file reads
- approval-required file writes
- allowed and blocked commands
- protected branch Git pushes
- policy-backed MCP allow/block decisions
- registry-backed MCP allow, approval, and block decisions
- release governance record checks for approval state, delivery failures, critical drift, inventory freshness, endpoint publication, and SLA evidence
- typed release-governance evidence contract payloads
- runtime evidence reference metadata
- representative compiled-policy decisions across every bundled policy pack
- release packages with checksums, SPDX SBOM, detached signatures, and release evidence

Run the scaffold locally:

```bash
cd go/cavra-runtime
go test ./...
echo '{"action_type":"execute_command","target":"terraform plan","policy_pack":"cavra-ai-agent-baseline"}' \
  | go run ./cmd/cavra-runtime
PYTHONPATH=../../src python3 -m cavra.cli policy compile --policy-pack cavra-ai-agent-baseline > /tmp/cavra-compiled-policy.json
echo '{"action_type":"read_file","target":".env"}' \
  | go run ./cmd/cavra-runtime --policy /tmp/cavra-compiled-policy.json
echo '{"session_id":"registry-demo","action_type":"mcp_tool_call","server":"github-mcp","tool":"delete_repository","capability":"repository","policy_pack":"cavra-mcp-enterprise"}' \
  | go run ./cmd/cavra-runtime --registry testdata/mcp_registry.json
echo '{"session_id":"release-demo","action_type":"release_governance_record","release_governance":{"metadata_kind":"rollout-promotion-execution","approval_state":"approved","approval_id":"apr_prod"}}' \
  | go run ./cmd/cavra-runtime
go run ./cmd/cavra-runtime --serve --socket .cavra/cavra-runtime.sock --policy /tmp/cavra-compiled-policy.json
echo '{"action_type":"execute_command","target":"terraform plan","requested_operation":"terraform plan","policy_pack":"cavra-ai-agent-baseline"}' \
  | go run ./cmd/cavra-runtime --daemon --socket .cavra/cavra-runtime.sock
go run ./cmd/cavra-runtime --lifecycle start --socket .cavra/cavra-runtime.sock --policy /tmp/cavra-compiled-policy.json
go run ./cmd/cavra-runtime --lifecycle status --socket .cavra/cavra-runtime.sock
go run ./cmd/cavra-runtime --lifecycle stop --socket .cavra/cavra-runtime.sock
go run ./cmd/cavra-runtime --serve --socket .cavra/cavra-runtime.sock --evidence-log .cavra/go-daemon/evidence.jsonl
```

`--policy` accepts normalized JSON from `cavra policy compile`. `--registry` accepts CAVRA trust-registry JSON with MCP server records and applies the same approved, pending, blocked, tool-scope, and capability-scope decisions as the Python registry path. When omitted, the runtime uses the built-in scaffold policy subset for local parity tests.

Generated enforcement contracts live under `enforcement/v1` and are generated from `../../proto/cavra/enforcement/v1/enforcement.proto`. They include `EvaluateRequest`, `ReleaseGovernanceEvidence`, and `DecisionResponse`; typed `release_governance` payloads are converted into runtime release-governance records. The daemon transport accepts one JSON `EvaluateRequest` per Unix-socket connection and returns one JSON `DecisionResponse`. The `daemon.Client` helper and CLI `--daemon` mode can send contract-shaped requests to a running socket daemon. The daemon lifecycle helper supports `start`, `status`, and `stop` with PID-file tracking, socket readiness probing, and graceful signal cleanup. `--evidence-log` writes JSONL request/response records and appends `go-daemon-evidence://...` references to `DecisionResponse.evidence_refs`.

```bash
cd ../..
python3 scripts/generate_go_enforcement_contracts.py
```

Packaged runner wrappers:

- `examples/ci-runners/cavra-release-governance-runner.sh` runs a typed release-governance request through the daemon and fails closed on unexpected or blocking decisions.
- `examples/github-actions/actions/cavra-release-governance-go-runtime/action.yml` wraps the shell runner as a reusable GitHub composite action.
- `scripts/package_go_release.py` includes both wrappers plus `cavra-runtime.ci-runner-bundles.json` in signed Go runtime release packages.

Next Go work:

- Add runner authentication and signed streaming evidence for release governance daemon checks.
