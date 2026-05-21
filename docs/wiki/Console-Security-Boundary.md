# Console Security Boundary

Phase 6 now reports the deployed console/API security boundary.

## What It Provides

- Read-only `GET /console/security-boundary`.
- Read-only `GET /console/session` for signed bearer-token actor context.
- OIDC readiness from `CAVRA_APPROVAL_OIDC_CONFIG`.
- Repository RBAC readiness from `CAVRA_APPROVAL_RBAC_FILE`.
- CORS origin visibility from `CAVRA_CORS_ORIGINS`.
- Browser-visible console permission categories.
- Operator notes for production deployments.

## How To Use

```bash
curl http://127.0.0.1:8000/console/security-boundary
```

The sandbox console displays the same information in the Console Security Boundary panel.

## Boundary

The boundary endpoint reports whether the console/API topology is ready for signed OIDC actor tokens and repository RBAC on approval decisions, break-glass actions, and policy publish write-back. `GET /console/session` validates a bearer token and reports actor context. Production deployments should host the console behind enterprise identity and restrict CORS.

## User Stories

- As a platform engineer, I can confirm OIDC and RBAC wiring before production console rollout.
- As a security architect, I can separate static demo console behavior from production identity boundaries.
- As an auditor, I can inspect the control boundary for approval decisions.

## Next

The next recommended work is daemon and CI runner examples for typed release governance enforcement requests.
