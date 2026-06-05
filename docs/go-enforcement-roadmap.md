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
- Opt-in Python integration pilot through `src/cavra/go_backend.py`.
- CLI commands `cavra runtime go-pilot-readiness`, `cavra runtime go-deployment-readiness`, and `cavra runtime go-pilot-evaluate`.
- API endpoints `/runtime/go-pilot/readiness`, `/runtime/go-pilot/deployment-readiness`, and `/runtime/go-pilot/evaluate`.
- Production readiness check for Go backend pilot status, configured runtime binary, compiled policy path, optional registry path, Python fallback, parity gate evidence, CI runner bundle readiness, and workstation channel readiness.
- Python parity test that verifies the same fixture against the authoritative `RuntimeGuard`.
- Shared high-risk command and cloud/IaC parity cases for Cloud IAM, Kubernetes production, Terraform/OpenTofu production, GitHub Enterprise, OWASP LLM agentic command injection, and transparent agentic delivery controls.
- Python parity test that verifies release-governance record fixtures for approvals, delivery failures, rollout evidence verification, and artifact integrity.
- Go unit test that loads the fixture and verifies the Go evaluator.
- Go release packaging reproducibility manifest for air-gapped rebuild checks.
- GitHub Actions `go-runtime-parity` job with `actions/setup-go`.
- Required governance check now runs the Go parity suite before publishing evidence.
- Go enforcement production hardening is documented in
  [go-enforcement-production-hardening.md](go-enforcement-production-hardening.md)
  and enforced by `scripts/validate-go-production-hardening.py`.

## Current Boundary

The scaffold intentionally mirrors a critical subset of policy behavior. It can now load compiled policy artifacts, expose generated Go request/response contracts, serve one-request-per-connection daemon calls over a Unix socket, call the daemon through a typed client helper, manage local daemon lifecycle through PID-file-backed `start/status/stop`, write request/response evidence records, verify release-governance fixtures across Python and Go, cover high-risk command and cloud/IaC parity cases, cover high-risk rollout evidence and audit export contract cases, package reproducibility and signing operations metadata for release governance, run as an explicitly opt-in Python-side backend pilot with audited fallback, and validate CI runner plus workstation deployment metadata before promotion.

## Next Implementation Steps

1. Promote Go to an optional backend only after audited parity, deployment
   tests, production hardening validation, package verification,
   release-candidate upgrade validation, performance smoke evidence, and
   rollback evidence pass.
2. Publish Community v0.1.3 maintenance release after GitHub Actions Node 24 readiness and workflow verification are complete.
