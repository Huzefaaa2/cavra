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
- Support for compiled policy JSON loaded with `--policy`.
- Go tests for contract handling, client calls, and compiled-policy-backed evaluation.

## How To Use

```bash
cd go/cavra-runtime
go run ./cmd/cavra-runtime --serve --socket .cavra/cavra-runtime.sock --policy testdata/compiled_policy.json
printf '{"action_type":"read_file","target":"config/prod.secret"}\n' | nc -U .cavra/cavra-runtime.sock
printf '{"action_type":"execute_command","target":"terraform plan","requested_operation":"terraform plan"}\n' \
  | go run ./cmd/cavra-runtime --daemon --socket .cavra/cavra-runtime.sock
```

## Enterprise Value

Daemon transport gives CAVRA a path to low-latency local and CI enforcement without requiring a Python API call for every guarded action.

## Next

Add lifecycle management, evidence hooks, and expanded parity for approvals and registry-backed MCP decisions.
