# Go Enforcement Roadmap

Python remains the authoritative management and policy plane. The Go runtime is being introduced as a low-latency enforcement plane only where parity is proven by tests and release evidence.

## Delivered Scaffold

- Go module under `go/cavra-runtime/`.
- Runtime evaluator for critical file, command, Git, and MCP decisions.
- CLI entrypoint at `go/cavra-runtime/cmd/cavra-runtime`.
- Shared parity fixture at `go/cavra-runtime/testdata/parity_cases.json`.
- Python parity test that verifies the same fixture against the authoritative `RuntimeGuard`.
- Go unit test that loads the fixture and verifies the Go evaluator.
- GitHub Actions `go-runtime-parity` job with `actions/setup-go`.
- Required governance check now runs the Go parity suite before publishing evidence.

## Current Boundary

The scaffold intentionally mirrors a critical subset of policy behavior. It does not yet load compiled policy artifacts, expose a daemon interface, or ship as the production enforcement backend.

## Next Implementation Steps

1. Load compiled policy JSON from `cavra policy compile` instead of relying on built-in scaffold rules.
2. Generate Go request and response types from `proto/cavra/enforcement/v1/enforcement.proto`.
3. Add a local daemon interface over Unix socket or gRPC.
4. Expand golden parity tests for approvals, evidence references, registry-backed MCP decisions, and policy inheritance overlays.
5. Package the Go binary for CI runner and air-gapped usage.
6. Promote Go to an optional backend only after audited parity and deployment tests pass.
