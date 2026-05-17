# Production Deployment Validation

CAVRA exposes `GET /deployment/production-readiness` for production console/API readiness checks.

## Checks

- OIDC configured.
- Repository RBAC configured.
- CORS origins restricted.
- Evidence artifact root configured.
- Policy pack catalog available.
- Persistent API stores exist.

## Console

The sandbox console includes a Production Readiness panel that displays status, checks, store summary, and operator notes.

## User Stories

- As a platform engineer, I can validate production controls before rollout.
- As a security architect, I can see missing identity, RBAC, CORS, persistence, or evidence controls.
- As an auditor, I can attach readiness status to release evidence.
