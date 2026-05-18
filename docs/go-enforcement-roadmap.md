# Go Enforcement Roadmap

Python remains the authoritative management and policy plane. The Go runtime is being introduced as a low-latency enforcement plane only where parity is proven by tests and release evidence.

## Delivered Scaffold

- Go module under `go/cavra-runtime/`.
- Runtime evaluator for critical file, command, Git, and MCP decisions.
- CLI entrypoint at `go/cavra-runtime/cmd/cavra-runtime`.
- Shared parity fixture at `go/cavra-runtime/testdata/parity_cases.json`.
- Compiled-policy loader for normalized JSON from `cavra policy compile`.
- CLI `--policy` flag for evaluating requests against compiled policy JSON.
- Generated Go request and response contracts under `go/cavra-runtime/enforcement/v1`.
- Contract generator at `scripts/generate_go_enforcement_contracts.py`.
- Python parity test that verifies the same fixture against the authoritative `RuntimeGuard`.
- Go unit test that loads the fixture and verifies the Go evaluator.
- GitHub Actions `go-runtime-parity` job with `actions/setup-go`.
- Required governance check now runs the Go parity suite before publishing evidence.

## Current Boundary

The scaffold intentionally mirrors a critical subset of policy behavior. It can now load compiled policy artifacts and expose generated Go request/response contracts, but it does not yet expose a daemon interface or ship as the production enforcement backend.

## Next Implementation Steps

1. Add a local daemon interface over Unix socket or gRPC.
2. Expand golden parity tests for approvals, evidence references, registry-backed MCP decisions, and policy inheritance overlays.
3. Package the Go binary for CI runner and air-gapped usage.
4. Promote Go to an optional backend only after audited parity and deployment tests pass.
