# Go Backend Rollback Controls

CAVRA now requires rollback controls before `promoted` mode can select Go as an optional backend. Python remains the recovery backend. If rollback readiness is missing or invalid, promoted-mode evaluation falls back to Python.

## What Rollback Requires

Rollback readiness requires:

- `CAVRA_GO_BACKEND_MODE=promoted` or an explicit rollback plan request.
- Python fallback remains available.
- `CAVRA_GO_ROLLBACK_PLAN` points to valid JSON metadata.
- The rollback plan has `status=ready`.
- The rollback plan has `target_mode=disabled`.
- The rollback plan is approved.
- Required controls are present.
- Rollback steps and evidence references are public-safe and parseable.

The public rollback plan schema is `cavra.go-backend-rollback-plan.v1`:

```json
{
  "schema_version": "cavra.go-backend-rollback-plan.v1",
  "status": "ready",
  "target_mode": "disabled",
  "approved": true,
  "approval_id": "apr_go_backend_rollback",
  "max_recovery_minutes": 15,
  "controls": [
    "python-fallback-available",
    "promoted-mode-disable-tested",
    "rollback-approval-recorded",
    "operator-runbook-linked",
    "evidence-capture-enabled"
  ],
  "rollback_steps": [
    "Set CAVRA_GO_BACKEND_MODE=disabled.",
    "Restart API, CI runner, or workstation process using CAVRA.",
    "Capture rollback readiness and production readiness reports."
  ],
  "evidence_refs": [
    "go-rollback-readiness://ci/ready",
    "go-promotion-rollback-runbook://docs/current"
  ]
}
```

Do not include secrets, private customer details, private endpoint identifiers, or proprietary operational data in the public rollback plan.

## Environment Variables

```bash
export CAVRA_GO_BACKEND_MODE=promoted
export CAVRA_GO_PROMOTION_EVIDENCE=/etc/cavra/go-backend-promotion-evidence.json
export CAVRA_GO_ROLLBACK_PLAN=/etc/cavra/go-backend-rollback-plan.json
export CAVRA_GO_ROLLBACK_REHEARSAL_EVIDENCE=/etc/cavra/go-backend-rollback-rehearsal.json
```

To roll back immediately:

```bash
export CAVRA_GO_BACKEND_MODE=disabled
```

Then restart the API, CI runner wrapper, workstation service, or process hosting CAVRA so the disabled mode is loaded.

## CLI Usage

```bash
cavra runtime go-rollback-readiness \
  --mode promoted \
  --rollback-plan-path /etc/cavra/go-backend-rollback-plan.json \
  --json
```

Promoted-mode evaluation also checks rollback readiness:

```bash
cavra runtime go-pilot-evaluate execute_command "terraform plan" \
  --mode promoted \
  --runtime-path /opt/cavra/bin/cavra-runtime \
  --policy-path /etc/cavra/compiled-policy.json \
  --package-dir /opt/cavra/go-runtime-release \
  --promotion-evidence-path /etc/cavra/go-backend-promotion-evidence.json \
  --rollback-plan-path /etc/cavra/go-backend-rollback-plan.json \
  --rollback-rehearsal-path /etc/cavra/go-backend-rollback-rehearsal.json \
  --json
```

## API Usage

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/rollback-readiness
curl http://127.0.0.1:8000/deployment/production-readiness
```

Production readiness includes a `go_backend_rollback` section and a `go_backend_rollback_controls` check. `not_requested` is acceptable when promoted mode is not configured. `needs_attention` blocks readiness when promoted mode is requested without an approved rollback plan. Rehearsal evidence is documented in [Go backend rollback rehearsal evidence](go-backend-rollback-rehearsal.md).

## User Stories

- As a platform owner, I can prove that promoted Go backend pilots have a documented path back to Python-only mode.
- As an incident commander, I can disable promoted Go selection by setting `CAVRA_GO_BACKEND_MODE=disabled`.
- As a security reviewer, I can require rollback approval before Go becomes the selected optional backend.
- As an auditor, I can attach rollback plan, approval, evidence references, and recovery-time expectations to promoted backend evidence.

## Enterprise Challenge Solved

Backend promotion is only production-ready when rollback is boring, explicit, and auditable. These controls keep Go backend adoption reversible and give regulated teams a clear recovery path before they allow promoted-mode enforcement in CI runners or workstation services.

## Next Work

The next recommended implementation step is to add bulk drill acknowledgement workflows and exportable acknowledgement audit packages.
