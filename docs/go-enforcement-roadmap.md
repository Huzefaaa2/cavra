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
- Unix-socket daemon transport under `go/cavra-runtime/daemon`.
- Reusable daemon client helper and CLI `--daemon` mode for one-shot socket calls.
- Daemon lifecycle `start/status/stop` with PID-file tracking and readiness probing.
- Daemon request/response evidence hooks with JSONL output and `go-daemon-evidence://...` refs.
- `cavra-runtime --serve --socket ...` server mode.
- Python parity test that verifies the same fixture against the authoritative `RuntimeGuard`.
- Python parity test that verifies release-governance record fixtures for approvals, delivery failures, rollout evidence verification, and artifact integrity.
- Go unit test that loads the fixture and verifies the Go evaluator.
- Go release packaging reproducibility manifest for air-gapped rebuild checks.
- GitHub Actions `go-runtime-parity` job with `actions/setup-go`.
- Required governance check now runs the Go parity suite before publishing evidence.

## Current Boundary

The scaffold intentionally mirrors a critical subset of policy behavior. It can now load compiled policy artifacts, expose generated Go request/response contracts, serve one-request-per-connection daemon calls over a Unix socket, call the daemon through a typed client helper, manage local daemon lifecycle through PID-file-backed `start/status/stop`, write request/response evidence records, verify release-governance fixtures across Python and Go, cover high-risk rollout evidence and audit export contract cases, and package reproducibility metadata for air-gapped rebuild checks. It does not yet include production signing key rotation operations.

## Next Implementation Steps

1. Add remaining high-risk command and cloud/IaC decision parity cases that are still Python-only.
2. Add remaining high-risk command and cloud/IaC decision parity cases that are still Python-only.
3. Promote Go to an optional backend only after audited parity and deployment tests pass.
