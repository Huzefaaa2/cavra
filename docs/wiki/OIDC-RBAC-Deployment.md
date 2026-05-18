# OIDC/RBAC Deployment

CAVRA now includes deployment references for Microsoft Entra ID and Okta OIDC with repository-scoped RBAC.

## Reference Bundles

- `examples/identity/entra-id-oidc-rbac`
- `examples/identity/okta-oidc-rbac`

Each bundle generates:

- `approval-oidc.json`
- `approval-jwks.json`
- `approval-rbac.yaml`
- `cavra-identity.env`

## Runtime Wiring

```bash
export CAVRA_APPROVAL_OIDC_CONFIG=.cavra/identity/entra/approval-oidc.json
export CAVRA_APPROVAL_RBAC_FILE=.cavra/identity/entra/approval-rbac.yaml
export CAVRA_CORS_ORIGINS=https://cavra-console.example.com
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

Validate the boundary:

```bash
curl http://127.0.0.1:8000/console/security-boundary
curl http://127.0.0.1:8000/console/session -H "Authorization: Bearer $CAVRA_CONSOLE_TOKEN"
```

## Controls

- Use tenant-specific Entra issuer metadata.
- Use exact Okta issuer metadata.
- Emit constrained `groups` or `roles` claims.
- Map external groups to CAVRA approval groups.
- Scope repository permissions by repository and approver group.
- Keep JWKS refresh in an operator runbook.
- Restrict `CAVRA_CORS_ORIGINS` for hosted consoles.

## User Stories

- As an IAM administrator, I can map enterprise groups to CAVRA approval groups.
- As a platform engineer, I can generate CAVRA-ready identity files from Entra or Okta metadata.
- As an auditor, I can inspect console session identity and repository permissions.

## Enterprise Value

OIDC/RBAC deployment references move CAVRA from local approval claims to production identity boundaries. Browser-visible console actions can rely on signed identity context and repository-scoped authorization.

## Next

Generated Go enforcement contracts and public sandbox URL validation after deployment from `main`.
