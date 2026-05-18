# Go Enforcement Parity Scaffold

Python remains the authoritative CAVRA runtime. The Go enforcement plane now has a bounded parity scaffold under `go/cavra-runtime/` so the project can evolve toward low-latency local and CI enforcement without creating inconsistent decisions.

## Delivered

- Go module and runtime evaluator.
- JSON request to JSON decision CLI entrypoint.
- Shared critical parity fixture.
- Go unit tests for file, command, Git, and MCP decisions.
- Python parity tests against the same fixture.
- `go-runtime-parity` GitHub Actions job.
- Required governance check execution of the Go test suite.

## How To Use

```bash
python3 -m pytest tests/test_go_runtime_parity.py -q
cd go/cavra-runtime
go test ./...
```

## User Stories

- As a CI owner, I can verify Go decisions before adopting a runner-side backend.
- As a platform engineer, I can review the decision boundary before deploying binaries.
- As an auditor, I can see parity evidence in required checks.

## Enterprise Challenge Solved

Large engineering fleets need fast enforcement, but regulated environments need proof that every backend evaluates policy consistently. The parity scaffold creates the proof path before promotion.

## Next

Load compiled policy JSON, generate protobuf-backed contracts, add a local daemon interface, expand golden cases, and package signed binaries.
