# Go Daemon Transport

CAVRA now includes the first local daemon transport for the Go enforcement plane.

## What Was Added

- `go/cavra-runtime/daemon` package.
- Unix-socket server mode through `go run ./cmd/cavra-runtime --serve`.
- One JSON `EvaluateRequest` per connection.
- One JSON `DecisionResponse` returned per connection.
- Runtime evaluator that can use either the built-in scaffold policy or compiled policy JSON loaded through `--policy`.
- Go tests for contract request handling and compiled-policy-backed daemon evaluation.

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

The daemon returns a `DecisionResponse` JSON object matching the generated contract package under `go/cavra-runtime/enforcement/v1`.

## User Stories

- As a developer, I can run a local enforcement daemon without starting the Python API.
- As a CI owner, I can connect runner-side tooling to a stable socket protocol.
- As an enterprise architect, I can evaluate a path toward a lightweight air-gapped enforcement binary.

## Enterprise Challenge Solved

Daemon transport moves the Go runtime from a CLI-only prototype toward an embeddable local enforcement service. This reduces latency and avoids shelling out for every guarded action while preserving the same contract and policy evidence path.

## Current Limits

- The daemon handles one request per connection.
- There is no lifecycle supervisor, authentication layer, or streaming evidence writer yet.
- Expanded parity is still needed for approvals, registry-backed MCP trust, and evidence references.

## Next Recommended Work

1. Add a small client helper for the Unix-socket protocol.
2. Add daemon lifecycle management for developer laptops and CI runners.
3. Add request/response evidence hooks.
4. Expand golden parity across approvals and registry-backed MCP decisions.
