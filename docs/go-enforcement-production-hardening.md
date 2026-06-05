# Go Enforcement Production Hardening

This release gate ties the public Go enforcement-plane production path into one
operator-verifiable checklist. Python remains authoritative for policy
authoring, evidence, integrations, and promotion decisions. The Go runtime is
allowed to move toward production only when transport, packaging, upgrade,
performance, and operational readiness evidence remain public, repeatable, and
bounded by the Community/Enterprise source boundary.

## Validation Command

Run the validator from the repository root:

```bash
python scripts/validate-go-production-hardening.py
```

Expected success output:

```text
CAVRA Go production hardening validation passed.
```

## Production Hardening Matrix

| Area | Public Control | Evidence Command |
| --- | --- | --- |
| Unix-socket transport | `go/cavra-runtime/daemon` provides one-request-per-connection local enforcement, client helper, lifecycle controls, runner authentication, and signed daemon evidence streams. | `go run ./cmd/cavra-runtime --lifecycle start --socket .cavra/cavra-runtime.sock`, `go run ./cmd/cavra-runtime --lifecycle status --socket .cavra/cavra-runtime.sock`, and `go run ./cmd/cavra-runtime --lifecycle stop --socket .cavra/cavra-runtime.sock`. |
| gRPC interface | gRPC remains a production interface boundary, not a promoted implementation in the public Community runtime. Generated contracts under `go/cavra-runtime/enforcement/v1` define the payloads that must back any future gRPC transport. | Validator confirms gRPC is documented as a required future transport gate before promoted production use. |
| Air-gapped packaging | The Go release workflow builds static binaries, creates `cavra-go-runtime-${version}.zip`, and records offline trust bootstrap material. | `cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-${version}.zip`. |
| Reproducibility | Release packages include `cavra-runtime.reproducibility.json`, `CGO_ENABLED=0`, `-trimpath`, read-only modules, disabled VCS stamping, and empty Go build IDs. | Rebuild with the recorded `rebuild_command` and compare SHA-256 digests before installing binaries in restricted environments. |
| Upgrade validation | Release-candidate packages must preserve required manifests, binary targets, signatures, and release controls before promotion. | `cavra release validate-upgrade go/cavra-runtime/dist/go-runtime-v0.1.0 go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1`. |
| Performance | The runtime includes `BenchmarkEvaluateAllowCommand` as a stable performance-smoke hook for the critical allow-command path. | `cd go/cavra-runtime && go test -bench BenchmarkEvaluateAllowCommand ./runtime`. |
| Operational readiness | Deployment readiness checks CI runner bundle metadata, workstation channel manifest, updater policy, promotion evidence, rollback controls, rollback rehearsal evidence, drill history, and drill scheduling before promoted mode can select Go. | `cavra runtime go-deployment-readiness` and `curl http://127.0.0.1:8000/deployment/production-readiness`. |

## Operator Runbook

1. Run Go unit and parity tests:

   ```bash
   cd go/cavra-runtime
   go test ./...
   ```

2. Capture performance smoke evidence:

   ```bash
   go test -bench BenchmarkEvaluateAllowCommand ./runtime
   ```

3. Exercise local daemon lifecycle:

   ```bash
   go run ./cmd/cavra-runtime --lifecycle start --socket .cavra/cavra-runtime.sock
   go run ./cmd/cavra-runtime --lifecycle status --socket .cavra/cavra-runtime.sock
   go run ./cmd/cavra-runtime --lifecycle stop --socket .cavra/cavra-runtime.sock
   ```

4. Verify release package and air-gapped bundle controls:

   ```bash
   cavra release verify-go-package go/cavra-runtime/dist/go-runtime-v0.1.0
   cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-v0.1.0.zip
   ```

5. Validate release-candidate upgrade posture:

   ```bash
   cavra release validate-upgrade \
     go/cavra-runtime/dist/go-runtime-v0.1.0 \
     go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1
   ```

6. Confirm production readiness from the Python management plane:

   ```bash
   cavra runtime go-deployment-readiness
   curl http://127.0.0.1:8000/deployment/production-readiness
   ```

7. Keep Go disabled unless parity, deployment, promotion, rollback,
   rehearsal, drill, packaging, upgrade, and performance evidence are all
   attached to release governance records.

## Public Boundary

This page documents public Community Edition Go runtime controls only. It does
not include Enterprise source code, private policy packs, SaaS license-service
logic, commercial release automation, customer deployment records, provider
credentials, private signing keys, or proprietary gRPC implementation code.

## User Stories

- As a platform engineer, I can prove that Go runtime promotion is blocked
  until transport, packaging, upgrade, performance, and readiness evidence are
  complete.
- As a CI owner, I can evaluate Unix-socket enforcement and signed daemon
  evidence while keeping Python authoritative.
- As a public-sector operator, I can verify air-gapped binaries and rebuild
  evidence before placing CAVRA on restricted runners.
- As an auditor, I can distinguish delivered Unix-socket controls from future
  gRPC interface requirements.

## Enterprise Challenge Solved

Large engineering organizations cannot promote a low-latency enforcement plane
based only on a working binary. This gate makes the Go path auditable: it links
transport status, air-gapped packaging, reproducibility, upgrade validation,
performance evidence, and operational readiness into one public-safe release
control.

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
