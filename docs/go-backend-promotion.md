# Go Backend Promotion Gate

CAVRA now has an explicit promotion gate for selecting Go as an optional backend. Python remains the default and authoritative backend unless an operator opts into `promoted` mode and supplies current promotion evidence.

## What Promotion Requires

Promotion readiness requires all of the following:

- Go runtime readiness is `ready`.
- Go deployment readiness is `ready`.
- `CAVRA_GO_PROMOTION_EVIDENCE` points to valid JSON evidence.
- The evidence records audited parity status as `pass`.
- The evidence records deployment status as `ready`.
- The evidence records an approved promotion decision.

The public evidence schema is `cavra.go-backend-promotion-evidence.v1`:

```json
{
  "schema_version": "cavra.go-backend-promotion-evidence.v1",
  "parity_status": "pass",
  "deployment_status": "ready",
  "approved": true,
  "approval_id": "apr_go_backend_promotion",
  "evidence_refs": [
    "go-runtime-parity://ci/run-id",
    "go-deployment-readiness://release/package-id"
  ]
}
```

## Environment Variables

```bash
export CAVRA_GO_BACKEND_MODE=promoted
export CAVRA_GO_RUNTIME_PATH=/opt/cavra/bin/cavra-runtime
export CAVRA_GO_RUNTIME_POLICY=/etc/cavra/compiled-policy.json
export CAVRA_GO_RUNTIME_PACKAGE_DIR=/opt/cavra/go-runtime-release
export CAVRA_GO_PROMOTION_EVIDENCE=/etc/cavra/go-backend-promotion-evidence.json
export CAVRA_GO_ROLLBACK_PLAN=/etc/cavra/go-backend-rollback-plan.json
```

`promoted` mode fails closed to Python when any promotion or rollback input is missing, malformed, stale, or unapproved.

## CLI Usage

```bash
cavra runtime go-promotion-readiness \
  --mode promoted \
  --runtime-path /opt/cavra/bin/cavra-runtime \
  --policy-path /etc/cavra/compiled-policy.json \
  --package-dir /opt/cavra/go-runtime-release \
  --promotion-evidence-path /etc/cavra/go-backend-promotion-evidence.json \
  --rollback-plan-path /etc/cavra/go-backend-rollback-plan.json \
  --json
```

Evaluate in promoted mode:

```bash
cavra runtime go-pilot-evaluate execute_command "terraform plan" \
  --mode promoted \
  --runtime-path /opt/cavra/bin/cavra-runtime \
  --policy-path /etc/cavra/compiled-policy.json \
  --package-dir /opt/cavra/go-runtime-release \
  --promotion-evidence-path /etc/cavra/go-backend-promotion-evidence.json \
  --json
```

## API Usage

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/promotion-readiness
curl http://127.0.0.1:8000/deployment/production-readiness
```

Production readiness includes `go_backend_promotion` and `go_backend_rollback` sections. `not_requested` is acceptable when Go promotion is not configured. `needs_attention` blocks readiness when promoted mode is requested without complete promotion evidence or rollback controls.

## User Stories

- As a platform owner, I can keep Python authoritative while testing Go in shadow and enforce modes.
- As a release owner, I can require audited parity and deployment evidence before Go becomes the selected optional backend.
- As a security reviewer, I can prove promoted mode falls back to Python when promotion evidence is missing.
- As an incident commander, I can require rollback controls before promoted mode can select Go.
- As an auditor, I can attach parity, deployment, and approval references to every promoted backend decision path.

## Enterprise Challenge Solved

Runtime backend changes are high-risk because a silent drift can alter enforcement. The promotion gate turns backend selection into an auditable release-control decision with explicit evidence, approval, and rollback-friendly fallback to Python.

## Next Work

The next recommended implementation step is to add automated rollback rehearsal evidence and dashboards for promoted Go backend pilots.
