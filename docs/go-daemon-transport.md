# Go Daemon Transport

CAVRA now includes the first local daemon transport for the Go enforcement plane.

## What Was Added

- `go/cavra-runtime/daemon` package.
- Unix-socket server mode through `go run ./cmd/cavra-runtime --serve`.
- One JSON `EvaluateRequest` per connection.
- One JSON `DecisionResponse` returned per connection.
- Reusable Go `daemon.Client` helper for Unix-socket requests.
- CLI `--daemon` client mode for one-shot `EvaluateRequest` calls.
- Daemon lifecycle helper with `--lifecycle start`, `status`, and `stop`.
- PID-file tracking, readiness probing, and graceful signal cleanup for local daemon processes.
- Request/response evidence hooks through `--evidence-log`.
- JSONL evidence records with `cavra.go-daemon.evidence.v1` schema, `go-daemon-evidence://...` references, hash chaining, optional `HMAC-SHA256` signatures, and key IDs.
- Optional CI runner authentication through `runner_auth` claims signed with `HMAC-SHA256`.
- Optional CI-provider OIDC runner authentication through `OIDC-JWT`, issuer, audience, and JWKS verification.
- Provider-native OIDC token acquisition helpers for GitHub Actions, GitLab CI, and Azure Pipelines runner wrappers.
- Evidence verifier CLI support through `--verify-evidence` for daemon JSONL hash chains and HMAC signatures.
- Runtime evaluator that can use either the built-in scaffold policy or compiled policy JSON loaded through `--policy`.
- Typed release-governance daemon request examples under `examples/go-runtime/typed-release-governance/`.
- CI runner examples for GitHub Actions, GitLab CI, and Azure Pipelines that send typed `release_governance` payloads through the daemon.
- Packaged CI runner wrappers under `examples/ci-runners/` plus a reusable GitHub composite action under `examples/github-actions/actions/cavra-release-governance-go-runtime/`.
- Signed release-package metadata in `cavra-runtime.ci-runner-bundles.json` that binds runner wrappers to verified Go runtime binaries and CI deployment targets.
- Go tests for contract request handling, client calls, lifecycle status, evidence recording, and compiled-policy-backed daemon evaluation.

## How To Use

Start the daemon:

```bash
cd go/cavra-runtime
go run ./cmd/cavra-runtime --serve --socket .cavra/cavra-runtime.sock --policy testdata/compiled_policy.json
```

Send a contract-shaped request:

```bash
printf '{"action_type":"read_file","target":"config/prod.secret"}\n' \
  | nc -U .cavra/cavra-runtime.sock
```

Or use the CAVRA Go client mode:

```bash
printf '{"action_type":"execute_command","target":"terraform plan","requested_operation":"terraform plan"}\n' \
  | go run ./cmd/cavra-runtime --daemon --socket .cavra/cavra-runtime.sock
```

Manage the daemon lifecycle:

```bash
go run ./cmd/cavra-runtime --lifecycle start --socket .cavra/cavra-runtime.sock --policy testdata/compiled_policy.json
go run ./cmd/cavra-runtime --lifecycle status --socket .cavra/cavra-runtime.sock
go run ./cmd/cavra-runtime --lifecycle stop --socket .cavra/cavra-runtime.sock
```

Write daemon evidence records:

```bash
go run ./cmd/cavra-runtime --serve --socket .cavra/cavra-runtime.sock --evidence-log .cavra/go-daemon/evidence.jsonl
printf '{"action_type":"execute_command","target":"terraform plan","requested_operation":"terraform plan"}\n' \
  | go run ./cmd/cavra-runtime --daemon --socket .cavra/cavra-runtime.sock
```

The daemon returns a `DecisionResponse` JSON object matching the generated contract package under `go/cavra-runtime/enforcement/v1`.
When evidence logging is enabled, the response includes a `go-daemon-evidence://...` reference and the JSONL record contains both the request and response.

## Production Interface Boundary

The delivered local production transport is Unix-socket based. gRPC remains a
future interface boundary rather than a promoted Community runtime transport.
Any future gRPC service must use the generated `EvaluateRequest` and
`DecisionResponse` contracts, preserve runner authentication and evidence
redaction behavior, and pass the same parity and operational readiness gates as
the Unix-socket daemon.

Performance smoke evidence is captured through the runtime benchmark:

```bash
cd go/cavra-runtime
go test -bench BenchmarkEvaluateAllowCommand ./runtime
```

Operational readiness evidence for the daemon includes lifecycle
`start/status/stop`, signed daemon evidence verification, runner authentication
mode, package verification, and Python fallback status.

Sign daemon evidence as a hash-chained stream:

```bash
export CAVRA_DAEMON_EVIDENCE_HMAC_KEY="set-this-from-a-ci-secret"
go run ./cmd/cavra-runtime --serve \
  --socket .cavra/cavra-runtime.sock \
  --evidence-log .cavra/go-daemon/evidence.jsonl \
  --evidence-signing-key-id ci-evidence-2026-q2
```

When `--evidence-signing-key` or `CAVRA_DAEMON_EVIDENCE_HMAC_KEY` is configured, each record includes `sequence`, `previous_hash`, `record_hash`, and an `HMAC-SHA256` signature. The signing key is never written to the evidence stream.

Verify daemon evidence after a runner check:

```bash
go run ./cmd/cavra-runtime --verify-evidence \
  --evidence-log .cavra/go-daemon/evidence.jsonl \
  --evidence-signing-key-id ci-evidence-2026-q2
```

When `CAVRA_DAEMON_EVIDENCE_HMAC_KEY` is available, the verifier checks every record hash, sequence number, previous hash, signature key ID, and HMAC signature. The JSON report returns `valid`, record counts, signed-record counts, and any verification errors.

Require authenticated runner claims:

```bash
cat > .cavra/go-daemon/runner-auth-claims.json <<'JSON'
{
  "provider": "github-actions",
  "repository": "Huzefaaa2/cavra",
  "workflow": "CAVRA Release Governance",
  "run_id": "123456",
  "ref": "refs/heads/main",
  "sha": "abc123"
}
JSON

export CAVRA_RUNNER_AUTH_HMAC_KEY="set-this-from-a-ci-secret"
go run ./cmd/cavra-runtime --lifecycle start \
  --socket .cavra/cavra-runtime.sock \
  --evidence-log .cavra/go-daemon/release-governance-evidence.jsonl \
  --runner-auth-key-id ci-runner-2026-q2

go run ./cmd/cavra-runtime --daemon \
  --socket .cavra/cavra-runtime.sock \
  --input ../../examples/go-runtime/typed-release-governance/approved-promotion.json \
  --runner-auth-claims .cavra/go-daemon/runner-auth-claims.json \
  --runner-auth-key-id ci-runner-2026-q2
```

When `--runner-auth-key` or `CAVRA_RUNNER_AUTH_HMAC_KEY` is configured on the daemon, unauthenticated requests return a clean `block` decision with rule `runner_auth.invalid`.

Require CI-provider OIDC runner JWTs instead of shared-secret runner signatures:

```bash
export CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE=".cavra/go-daemon/runner-oidc.jwt"
go run ./cmd/cavra-runtime --lifecycle start \
  --socket .cavra/cavra-runtime.sock \
  --evidence-log .cavra/go-daemon/release-governance-evidence.jsonl \
  --runner-oidc-issuer https://token.actions.githubusercontent.com \
  --runner-oidc-audience cavra-release-governance \
  --runner-oidc-jwks-url https://token.actions.githubusercontent.com/.well-known/jwks

go run ./cmd/cavra-runtime --daemon \
  --socket .cavra/cavra-runtime.sock \
  --input ../../examples/go-runtime/typed-release-governance/approved-promotion.json \
  --runner-auth-claims .cavra/go-daemon/runner-auth-claims.json \
  --runner-auth-oidc-token-file "${CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE}"
```

OIDC mode stores `runner_auth.algorithm` as `OIDC-JWT`, verifies RS256 JWT signatures against the configured JWKS, checks issuer, audience, expiry, not-before, provider, repository, and matching runner identity claims, and redacts the bearer JWT from daemon evidence records.

Evaluate a typed release-governance request:

```bash
go run ./cmd/cavra-runtime --lifecycle start \
  --socket .cavra/cavra-runtime.sock \
  --evidence-log .cavra/go-daemon/release-governance-evidence.jsonl

go run ./cmd/cavra-runtime --daemon \
  --socket .cavra/cavra-runtime.sock \
  --input ../../examples/go-runtime/typed-release-governance/approved-promotion.json

go run ./cmd/cavra-runtime --lifecycle stop --socket .cavra/cavra-runtime.sock
```

Runner templates are available at:

- `examples/github-actions/cavra-release-governance-go-runtime.yml`
- `examples/github-actions/actions/cavra-release-governance-go-runtime/action.yml`
- `examples/gitlab-ci/cavra-release-governance-go-runtime.gitlab-ci.yml`
- `examples/azure-pipelines/cavra-release-governance-go-runtime.azure-pipelines.yml`

Signed Go runtime release packages now also include:

- `cavra-runtime.ci-runner-bundles.json`
- `ci-runners/cavra-release-governance-runner.sh`
- `ci-runners/github-action/action.yml`

Verify the release package first, install the referenced runtime binary, then use the shell wrapper or composite action to execute a typed release-governance daemon check and publish `.cavra/go-daemon/` as CI evidence. The runner wrapper writes `runner-auth-claims.json`, signs claims when `CAVRA_RUNNER_AUTH_HMAC_KEY` is set, auto-acquires CI-provider OIDC JWTs when `CAVRA_RUNNER_OIDC_AUTO=true`, sends OIDC JWTs when `CAVRA_RUNNER_AUTH_OIDC_TOKEN` or `CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE` is set, signs the evidence stream when `CAVRA_DAEMON_EVIDENCE_HMAC_KEY` is set, and writes an evidence verification report.

## User Stories

- As a developer, I can run a local enforcement daemon without starting the Python API.
- As a developer, I can start, inspect, and stop the daemon without hand-managing socket and PID files.
- As a CI owner, I can connect runner-side tooling to a stable socket protocol.
- As a CI owner, I can reuse a signed release-governance runner wrapper instead of rebuilding CAVRA from source in each pipeline.
- As a CI owner, I can require signed runner claims before the daemon accepts release-governance checks.
- As a CI owner, I can require CI-provider OIDC JWT verification before the daemon accepts release-governance checks.
- As a CI owner, I can let the wrapper request GitHub Actions, GitLab CI, or Azure Pipelines OIDC tokens without storing a long-lived runner auth secret.
- As a platform engineer, I can call the daemon through a typed Go helper instead of hand-rolled socket code.
- As a release manager, I can gate promotion or rollback workflows on typed release-governance evidence without relying on ad hoc JSON maps.
- As an auditor, I can trace daemon decisions to a hash-chained, optionally signed request/response evidence stream.
- As an auditor, I can verify daemon evidence hash chains and signatures with the packaged runtime CLI.
- As an enterprise architect, I can evaluate a path toward a lightweight air-gapped enforcement binary.

## Enterprise Challenge Solved

Daemon transport moves the Go runtime from a CLI-only prototype toward an embeddable local enforcement service. This reduces latency and avoids shelling out for every guarded action while preserving the same contract and policy evidence path.

## Current Limits

- The daemon handles one request per connection.
- Evidence signing uses public-safe HMAC hooks in this repository; production key custody and rotation policy is documented in `docs/runner-auth-evidence-key-custody.md`.
- OIDC verification currently supports RS256 JWKS-backed CI-provider JWTs and validates common GitHub Actions, GitLab CI, Azure Pipelines, and generic runner identity claims. Provider-specific acquisition helpers are implemented for GitHub Actions, GitLab CI, and Azure Pipelines, but Azure issuer and JWKS configuration must still be pinned by the operator from approved tenant metadata.

## Next Recommended Work

1. Promote Go to an optional backend only after audited parity and deployment tests pass.
2. Promote Go to an optional backend only after audited parity and deployment tests pass.
