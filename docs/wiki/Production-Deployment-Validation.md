# Production Deployment Validation

CAVRA now exposes a deployment readiness report for authenticated console/API topologies.

## Endpoint

- `GET /deployment/production-readiness`

The report checks:

- OIDC configuration.
- Repository RBAC configuration.
- Restricted CORS origins.
- Evidence artifact root configuration.
- Policy pack catalog availability.
- Persistent API store presence.
- Opt-in Go backend pilot mode, runtime binary path, compiled policy path, optional registry path, Python fallback, and parity gate evidence.
- Go backend CI runner bundle metadata, workstation channel manifest, and updater policy readiness.

## Usage

```bash
curl http://127.0.0.1:8000/deployment/production-readiness
```

Run this in the same environment that hosts the API and console. Attach the report to release evidence before enterprise pilots.

## Console

The sandbox console includes a Production Readiness panel that displays deployment status, checks, store summary, Go backend pilot status, Go backend deployment readiness, and operator notes.

## User Stories

- As a platform engineer, I can validate whether production identity, RBAC, CORS, evidence, persistence controls, optional Go backend pilot inputs, and Go backend rollout metadata are configured.
- As a security architect, I can detect missing controls before exposing the console to enterprise users.
- As an auditor, I can attach a readiness report to release evidence.

## Enterprise Value

Deployment validation turns production readiness into a repeatable control check. It helps teams avoid launching a console/API topology without identity, RBAC, evidence retrieval, CORS restrictions, persistent stores, Go backend pilot evidence, or CI runner and workstation rollout controls when that pilot is enabled.
