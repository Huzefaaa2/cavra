# Go Enforcement Contracts

CAVRA now generates Go enforcement contract types from `proto/cavra/enforcement/v1/enforcement.proto`.

## Delivered

- Generated Go package under `go/cavra-runtime/enforcement/v1`.
- `EvaluateRequest` and `DecisionResponse` structs matching the protobuf field names.
- Conversion helpers between contract objects and runtime requests/decisions.
- Tests that keep generated contracts aligned with the proto field list.
- Runtime support for proto-shaped `requested_operation`.

## How To Use

```bash
python3 scripts/generate_go_enforcement_contracts.py
cd go/cavra-runtime
go test ./...
```

## User Stories

- As a platform engineer, I can build daemon transport against a stable contract.
- As a CI owner, I can validate enforcement payloads before runner integration.
- As an auditor, I can trace Go runtime payloads back to the protobuf contract.

## Enterprise Challenge Solved

Generated contracts reduce integration drift between management-plane policy decisions, Go enforcement, and future daemon or runner deployments.

## Next

Build the local daemon transport on these request and response types, then expand parity tests across approvals, registry-backed MCP decisions, and evidence references.
