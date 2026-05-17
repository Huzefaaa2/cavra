# Console Security Boundary

Phase 6 now exposes a read-only console security boundary endpoint and console panel.

## API

```bash
curl http://127.0.0.1:8000/console/security-boundary
```

The response reports:

- OIDC configuration status from `CAVRA_APPROVAL_OIDC_CONFIG`.
- Repository RBAC configuration status from `CAVRA_APPROVAL_RBAC_FILE`.
- CORS origins from `CAVRA_CORS_ORIGINS`.
- Browser-visible console permission categories.
- Operator notes for production console deployments.

## Boundary Model

The boundary endpoint is intentionally read-only and does not expose secrets. It tells operators whether the console/API topology is ready to rely on signed OIDC actor tokens and repository RBAC for approval decisions. `GET /console/session` validates signed bearer-token context and reports the active console actor and repository permissions.

Production deployments should:

- Host the console behind enterprise identity.
- Configure `CAVRA_APPROVAL_OIDC_CONFIG`.
- Configure `CAVRA_APPROVAL_RBAC_FILE`.
- Restrict `CAVRA_CORS_ORIGINS`.
- Keep backup and restore operations in CLI or platform runbooks.

## Console

The sandbox console includes a Console Security Boundary panel that displays mode, OIDC status, RBAC status, CORS origins, allowed console permission categories, and operator notes. It also includes a Console Session panel for bearer-token validation.

## User Stories

- As a platform engineer, I can see whether the deployed console is wired for OIDC and repository RBAC.
- As a platform engineer, I can validate the signed actor context used for console actions.
- As a security architect, I can confirm that browser-visible console actions are bounded and that backup/restore remains outside the browser.
- As an auditor, I can inspect the control boundary for approval decisions that use signed identity claims.

## Enterprise Challenge Solved

Enterprises need to separate demo console convenience from production identity boundaries. The security boundary view makes that separation explicit and avoids implying that an unauthenticated static console is a production auth layer.
