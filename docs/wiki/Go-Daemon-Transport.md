# Go Daemon Transport

CAVRA now includes the first local daemon transport for the Go enforcement plane.

## Delivered

- `go/cavra-runtime/daemon` package.
- `--serve` mode for `go/cavra-runtime`.
- Unix-socket listener.
- One JSON `EvaluateRequest` per connection.
- One JSON `DecisionResponse` per connection.
- Reusable Go `daemon.Client` helper.
- CLI `--daemon` client mode for one-shot socket calls.
- Daemon lifecycle helper with `--lifecycle start`, `status`, and `stop`.
- PID-file tracking, socket readiness probing, and graceful signal cleanup.
- Request/response evidence hooks through `--evidence-log`.
- JSONL evidence records with `cavra.go-daemon.evidence.v1` schema and `go-daemon-evidence://...` references.
- Support for compiled policy JSON loaded with `--policy`.
- Go tests for contract handling, client calls, lifecycle status, evidence recording, and compiled-policy-backed evaluation.

## How To Use

```bash
cd go/cavra-runtime
go run ./cmd/cavra-runtime --serve --socket .cavra/cavra-runtime.sock --policy testdata/compiled_policy.json
printf '{"action_type":"read_file","target":"config/prod.secret"}\n' | nc -U .cavra/cavra-runtime.sock
printf '{"action_type":"execute_command","target":"terraform plan","requested_operation":"terraform plan"}\n' \
  | go run ./cmd/cavra-runtime --daemon --socket .cavra/cavra-runtime.sock
go run ./cmd/cavra-runtime --lifecycle start --socket .cavra/cavra-runtime.sock --policy testdata/compiled_policy.json
go run ./cmd/cavra-runtime --lifecycle status --socket .cavra/cavra-runtime.sock
go run ./cmd/cavra-runtime --lifecycle stop --socket .cavra/cavra-runtime.sock
go run ./cmd/cavra-runtime --serve --socket .cavra/cavra-runtime.sock --evidence-log .cavra/go-daemon/evidence.jsonl
```

## Enterprise Value

Daemon transport gives CAVRA a path to low-latency local and CI enforcement without requiring a Python API call for every guarded action.

## Next

Expand parity for approvals, evidence references, and registry-backed MCP decisions, then package signed runner binaries after audited parity coverage exists.
