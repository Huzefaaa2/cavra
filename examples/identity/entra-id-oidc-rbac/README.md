# CAVRA OIDC/RBAC Reference: Microsoft Entra ID

This reference creates CAVRA identity configuration files for a Microsoft Entra ID OpenID Connect application.

It generates:

- `.cavra/identity/entra/approval-oidc.json`
- `.cavra/identity/entra/approval-jwks.json`
- `.cavra/identity/entra/approval-rbac.yaml`

CAVRA uses these files through:

```bash
export CAVRA_APPROVAL_OIDC_CONFIG=.cavra/identity/entra/approval-oidc.json
export CAVRA_APPROVAL_RBAC_FILE=.cavra/identity/entra/approval-rbac.yaml
export CAVRA_CORS_ORIGINS=https://cavra-console.example.com
```

## Prerequisites

- An Entra app registration for the CAVRA API or console.
- A v2.0 token audience that matches the app client ID or application ID URI.
- ID or access tokens that include `groups` or `roles` claims.
- `curl` and `python3` on the operator workstation.

## Configure

```bash
cp variables.example.env .env
source .env
bash generate-cavra-identity-config.sh
```

## Validate

Start the API with the generated files, then validate a bearer token:

```bash
curl http://127.0.0.1:8000/console/session \
  -H "Authorization: Bearer $CAVRA_CONSOLE_TOKEN"
```

## Notes

- Use tenant-specific issuer metadata for production. Avoid `common` unless your deployment explicitly supports multi-tenant issuer validation.
- Group IDs from Entra tokens can be mapped to human-readable CAVRA approval groups in `approval-rbac.yaml`.
- Refresh `approval-jwks.json` on a controlled schedule or when signing keys rotate.
