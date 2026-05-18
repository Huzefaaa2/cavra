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
- Runtime evaluator that can use either the built-in scaffold policy or compiled policy JSON loaded through `--policy`.
- Go tests for contract request handling, client calls, lifecycle status, and compiled-policy-backed daemon evaluation.

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

The daemon returns a `DecisionResponse` JSON object matching the generated contract package under `go/cavra-runtime/enforcement/v1`.

## User Stories

- As a developer, I can run a local enforcement daemon without starting the Python API.
- As a developer, I can start, inspect, and stop the daemon without hand-managing socket and PID files.
- As a CI owner, I can connect runner-side tooling to a stable socket protocol.
- As a platform engineer, I can call the daemon through a typed Go helper instead of hand-rolled socket code.
- As an enterprise architect, I can evaluate a path toward a lightweight air-gapped enforcement binary.

## Enterprise Challenge Solved

Daemon transport moves the Go runtime from a CLI-only prototype toward an embeddable local enforcement service. This reduces latency and avoids shelling out for every guarded action while preserving the same contract and policy evidence path.

## Current Limits

- The daemon handles one request per connection.
- There is no authentication layer or streaming evidence writer yet.
- Expanded parity is still needed for approvals, registry-backed MCP trust, and evidence references.

## Next Recommended Work

1. Add request/response evidence hooks.
2. Expand golden parity across approvals and registry-backed MCP decisions.
