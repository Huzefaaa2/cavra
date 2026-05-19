# Go Enforcement Parity Scaffold

Python remains the authoritative CAVRA runtime. The Go enforcement plane now has a bounded parity scaffold under `go/cavra-runtime/` so the project can evolve toward low-latency local and CI enforcement without creating inconsistent decisions.

## Delivered

- Go module and runtime evaluator.
- JSON request to JSON decision CLI entrypoint.
- Shared critical parity fixture.
- Compiled-policy loader for normalized JSON from `cavra policy compile`.
- CLI `--policy` flag for evaluating against compiled policy JSON.
- Trust-registry loader and CLI `--registry` flag for registry-backed MCP decisions.
- Runtime evidence metadata with decision IDs, correlation IDs, timestamps, and `evidence://...` references.
- Compiled-policy parity across every bundled policy pack through Python-to-Go CLI validation.
- Go release package workflow with checksums, SPDX SBOM metadata, detached signatures, release evidence, GitHub Release asset attachment, and CLI verification.
- Go unit tests for file, command, Git, and MCP decisions.
- Python parity tests against the same fixture.
- `go-runtime-parity` GitHub Actions job.
- Required governance check execution of the Go test suite.

## How To Use

```bash
python3 -m pytest tests/test_go_runtime_parity.py -q
cd go/cavra-runtime
go test ./...
```

```bash
PYTHONPATH=src python3 -m cavra.cli policy compile --policy-pack cavra-ai-agent-baseline > /tmp/cavra-compiled-policy.json
echo '{"action_type":"read_file","target":".env"}' \
  | go run ./cmd/cavra-runtime --policy /tmp/cavra-compiled-policy.json
echo '{"session_id":"registry-demo","action_type":"mcp_tool_call","server":"github-mcp","tool":"delete_repository","capability":"repository","policy_pack":"cavra-mcp-enterprise"}' \
  | go run ./cmd/cavra-runtime --registry testdata/mcp_registry.json
```

## User Stories

- As a CI owner, I can verify Go decisions before adopting a runner-side backend.
- As a platform engineer, I can review the decision boundary before deploying binaries.
- As an auditor, I can see parity evidence in required checks.

## Enterprise Challenge Solved

Large engineering fleets need fast enforcement, but regulated environments need proof that every backend evaluates policy consistently. The parity scaffold creates the proof path before promotion.

## Next

Add signed promotion approval requests for endpoint rollout readiness and continue broadening approval-route parity as new policy packs are added.
