# Go Enforcement Parity Scaffold

The Go enforcement plane starts as a parity scaffold, not as a replacement for the Python runtime. Python remains authoritative for policy authoring, evidence, approvals, integrations, and production decisions until Go uses generated contracts, supports the full policy surface, and passes expanded golden tests.

## What Was Added

- `go/cavra-runtime/go.mod` defines the Go module.
- `go/cavra-runtime/runtime/decision.go` evaluates critical file, command, Git, and MCP decisions.
- `go/cavra-runtime/cmd/cavra-runtime/main.go` reads a JSON request and writes a JSON decision.
- `go/cavra-runtime/testdata/parity_cases.json` captures shared critical decision cases.
- `go/cavra-runtime/testdata/compiled_policy.json` captures a compiled-policy loading fixture.
- `go/cavra-runtime/testdata/mcp_registry.json` captures registry-backed MCP trust decisions.
- `go/cavra-runtime/testdata/release_governance_records.json` captures release governance record decisions for approvals, delivery failures, endpoint publication, inventory freshness, reconciliation drift, SLA reports, handoff status, rollout evidence verification, and rollout artifact integrity.
- `go/cavra-runtime/runtime/decision_test.go` verifies the Go evaluator against the shared fixture.
- `tests/test_go_runtime_parity.py` verifies the same runtime and release-governance fixtures against Python `RuntimeGuard` and compiles every bundled policy pack before checking representative Go CLI decisions.
- `go run ./cmd/cavra-runtime --policy compiled-policy.json` evaluates against normalized JSON from `cavra policy compile`.
- `go run ./cmd/cavra-runtime --registry mcp-registry.json` evaluates MCP calls with trust-registry decisions.
- `release_governance_record` requests verify pending, approved, denied, missing-approval, failed-delivery, and critical operational signal states without exposing private enterprise logic.
- `go/cavra-runtime/enforcement/v1` contains generated Go request, release-governance evidence, and response contracts from the enforcement protobuf.
- `go/cavra-runtime/testdata/release_governance_contracts.json` verifies typed release-governance contract payloads for approved, failed-delivery, critical-signal, rollout evidence verification, rollout artifact integrity, promotion audit export, and rollback audit export records.
- Go decisions now emit runtime evidence metadata: decision ID, correlation ID, timestamp, and `evidence://...` references.
- `.github/workflows/go-release.yml` packages Go runtime binaries with checksums, SPDX SBOM metadata, signed installer metadata, reproducibility manifests, release signing operations metadata, managed endpoint deployment manifests, release channel manifests, managed workstation updater policy, signed release-channel promotion approvals, Jamf/Intune/Linux endpoint-management export bundles, channel publishing history metadata, endpoint export publication delivery, endpoint inventory ingestion, endpoint inventory freshness SLA reports, reconciliation automation from ingested inventory, managed endpoint reconciliation, endpoint drift dashboards, approval-bound endpoint drift remediation plans, approved remediation execution records, endpoint remediation handoff packages, endpoint remediation handoff status reconciliation, rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters and console/API views, governed rollout artifact retrieval, rollout artifact integrity status, promotion readiness indicators, signed promotion approval requests, approved promotion execution records, promotion execution search and audit drill-downs, rollback evidence links, approved rollback execution records, SIEM/ITSM promotion audit exports, connector delivery for promotion audit and rollback execution records, endpoint remediation escalation delivery actions, owner review workflows, recurrence policies, owner calendars, maintenance-window suppression, recurrence delivery batching, suppression audit exports, recurrence retry policies, owner digest notifications, suppression trend analytics, installer smoke validation, detached signatures, GitHub keyless OIDC attestations, offline trust bootstrap metadata, air-gapped zip verification, release-candidate upgrade validation, and release evidence.
- `.github/workflows/test.yml` includes a `go-runtime-parity` job.
- `.github/workflows/cavra-governance.yml` runs the Go parity suite inside the required governance check.

## How To Use

Run the Python-side parity expectations:

```bash
python3 -m pytest tests/test_go_runtime_parity.py -q
```

Run the Go runtime tests when the Go toolchain is installed:

```bash
cd go/cavra-runtime
go test ./...
```

Evaluate one request through the Go CLI:

```bash
echo '{"action_type":"execute_command","target":"terraform apply -auto-approve","policy_pack":"cavra-ai-agent-baseline"}' \
  | go run ./cmd/cavra-runtime
```

Evaluate with compiled policy JSON:

```bash
PYTHONPATH=src python3 -m cavra.cli policy compile --policy-pack cavra-ai-agent-baseline > /tmp/cavra-compiled-policy.json
echo '{"action_type":"read_file","target":".env"}' \
  | go run ./cmd/cavra-runtime --policy /tmp/cavra-compiled-policy.json
```

Evaluate MCP trust through the registry fixture:

```bash
echo '{"session_id":"registry-demo","action_type":"mcp_tool_call","server":"github-mcp","tool":"delete_repository","capability":"repository","policy_pack":"cavra-mcp-enterprise"}' \
  | go run ./cmd/cavra-runtime --registry testdata/mcp_registry.json
```

Evaluate release governance evidence:

```bash
echo '{"session_id":"release-demo","action_type":"release_governance_record","release_governance":{"metadata_kind":"rollout-promotion-execution","approval_state":"approved","approval_id":"apr_prod"}}' \
  | go run ./cmd/cavra-runtime
```

## User Stories

- As a CI owner, I can verify that a future low-latency runtime returns the same critical decisions as the authoritative Python runtime.
- As a platform engineer, I can inspect a small Go implementation before allowing it into runners or developer laptops.
- As an auditor, I can see that parity is tested before CAVRA claims a second enforcement backend.
- As a release manager, I can verify that promotion, rollback, endpoint remediation, endpoint publication, inventory freshness, reconciliation drift, SLA, rollout evidence, artifact integrity, and rollout audit export evidence are evaluated consistently by the Go runtime.

## Enterprise Challenge Solved

Enterprises need fast local enforcement but cannot accept inconsistent policy decisions. This scaffold creates a controlled path to a Go runtime by making parity explicit, tested, and visible in the required governance check.

## Current Limits

- The Go runtime supports compiled policy JSON for the currently mirrored sections: filesystem, commands, and MCP trust lists.
- Registry-backed MCP parity is implemented for approved, pending, blocked, tool-scope, and capability-scope decisions.
- Release governance record parity is intentionally bounded to public-safe metadata checks for approval state, delivery success, drift status, alert level, blocked counts, SLA breach counts, rollout verification status, artifact integrity status, and rollout audit export status.
- It exposes an initial Unix-socket daemon transport using the generated request and response types.
- Managed endpoint deployment manifests are available for packaged CI runner and developer workstation rollout metadata.

## Next Recommended Work

1. Add remaining high-risk command and cloud/IaC decision parity cases that are still Python-only.
