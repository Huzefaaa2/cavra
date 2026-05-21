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

Sign daemon evidence as a hash-chained stream:

```bash
export CAVRA_DAEMON_EVIDENCE_HMAC_KEY="set-this-from-a-ci-secret"
go run ./cmd/cavra-runtime --serve \
  --socket .cavra/cavra-runtime.sock \
  --evidence-log .cavra/go-daemon/evidence.jsonl \
  --evidence-signing-key-id ci-evidence-2026-q2
```

When `--evidence-signing-key` or `CAVRA_DAEMON_EVIDENCE_HMAC_KEY` is configured, each record includes `sequence`, `previous_hash`, `record_hash`, and an `HMAC-SHA256` signature. The signing key is never written to the evidence stream.

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

Verify the release package first, install the referenced runtime binary, then use the shell wrapper or composite action to execute a typed release-governance daemon check and publish `.cavra/go-daemon/` as CI evidence. The runner wrapper writes `runner-auth-claims.json`, signs claims when `CAVRA_RUNNER_AUTH_HMAC_KEY` is set, and signs the evidence stream when `CAVRA_DAEMON_EVIDENCE_HMAC_KEY` is set.

## User Stories

- As a developer, I can run a local enforcement daemon without starting the Python API.
- As a developer, I can start, inspect, and stop the daemon without hand-managing socket and PID files.
- As a CI owner, I can connect runner-side tooling to a stable socket protocol.
- As a CI owner, I can reuse a signed release-governance runner wrapper instead of rebuilding CAVRA from source in each pipeline.
- As a CI owner, I can require signed runner claims before the daemon accepts release-governance checks.
- As a platform engineer, I can call the daemon through a typed Go helper instead of hand-rolled socket code.
- As a release manager, I can gate promotion or rollback workflows on typed release-governance evidence without relying on ad hoc JSON maps.
- As an auditor, I can trace daemon decisions to a hash-chained, optionally signed request/response evidence stream.
- As an enterprise architect, I can evaluate a path toward a lightweight air-gapped enforcement binary.

## Enterprise Challenge Solved

Daemon transport moves the Go runtime from a CLI-only prototype toward an embeddable local enforcement service. This reduces latency and avoids shelling out for every guarded action while preserving the same contract and policy evidence path.

## Current Limits

- The daemon handles one request per connection.
- Evidence signing uses public-safe HMAC hooks in this repository; production key custody and rotation policy must be supplied by deployment automation.
- Runner authentication validates signed claims but does not yet validate CI-provider OIDC tokens directly.

## Next Recommended Work

1. Add CI-provider OIDC token verification for runner authentication.
2. Add verifier CLI support for daemon evidence stream signatures and hash chains.
