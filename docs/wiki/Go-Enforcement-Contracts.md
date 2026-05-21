# Go Enforcement Contracts

CAVRA now has a generated Go contract package for the enforcement boundary.

Source contract: `proto/cavra/enforcement/v1/enforcement.proto`

Generated package: `go/cavra-runtime/enforcement/v1`

Generator: `scripts/generate_go_enforcement_contracts.py`

## What Was Added

- `EvaluateRequest` generated from the protobuf request shape.
- `ReleaseGovernanceEvidence` generated from the protobuf release-governance evidence payload shape.
- `DecisionResponse` generated from the protobuf response shape.
- Conversion from generated request contracts to runtime requests.
- Conversion from typed release-governance contract payloads into public-safe runtime records.
- Conversion from runtime decisions to generated response contracts.
- Contract tests that verify expected proto fields remain present.
- Contract-level fixtures for approval, failed delivery, and critical inventory freshness release-governance payloads.
- Daemon and CI runner examples that send typed release-governance payloads through the generated request contract.
- Runtime support for both legacy `operation` and proto-aligned `requested_operation`.

## How To Use

Regenerate the Go contract file:

```bash
python3 scripts/generate_go_enforcement_contracts.py
```

Run contract tests when the Go toolchain is installed:

```bash
cd go/cavra-runtime
go test ./...
```

Example proto-shaped JSON request:

```json
{
  "session_id": "session-1",
  "agent_id": "codex-agent",
  "actor": "developer@example.com",
  "action_type": "execute_command",
  "target": "terraform plan",
  "requested_operation": "terraform plan",
  "policy_pack": "cavra-ai-agent-baseline"
}
```

Example release-governance evidence contract request:

```json
{
  "session_id": "release-contract-demo",
  "agent_id": "release-agent",
  "actor": "release.manager@example.com",
  "action_type": "release_governance_record",
  "target": "release-connectors",
  "requested_operation": "verify",
  "policy_pack": "cavra-ai-agent-baseline",
  "release_governance": {
    "metadata_kind": "release-connector-delivery",
    "release_channel": "stable",
    "release_version": "v0.2.0",
    "failed_providers": ["servicenow"],
    "failed_delivery_count": 1,
    "blocked_count": 1,
    "connector_delivery_source": "release_governance_promotion"
  }
}
```

## User Stories

- As a platform engineer, I can build daemon transport on a stable request and response shape.
- As a CI owner, I can validate the same contract before wiring runner-side enforcement.
- As an auditor, I can see that the Go enforcement boundary follows the documented protobuf contract.
- As a release manager, I can send typed release-governance metadata into the Go runtime without relying on ad hoc JSON maps.

## Enterprise Challenge Solved

Generated contracts reduce integration drift between Python, Go, future daemon transport, and CI runner integrations. Enterprises can review one enforcement boundary instead of reverse-engineering each runtime implementation.

## Current Limits

- The generated package is a lightweight JSON transport contract, not a full gRPC server.
- The current daemon transport and `daemon.Client` helper use these contracts over a one-request-per-connection Unix socket.
- GitHub Actions, GitLab CI, and Azure Pipelines examples now use typed release-governance contract payloads directly.
- Next work should package signed runner binaries and reusable runner actions around these examples.
