# CAVRA OIDC/RBAC Reference: Okta

This reference creates CAVRA identity configuration files for an Okta OpenID Connect application or authorization server.

It generates:

- `.cavra/identity/okta/approval-oidc.json`
- `.cavra/identity/okta/approval-jwks.json`
- `.cavra/identity/okta/approval-rbac.yaml`

CAVRA uses these files through:

```bash
export CAVRA_APPROVAL_OIDC_CONFIG=.cavra/identity/okta/approval-oidc.json
export CAVRA_APPROVAL_RBAC_FILE=.cavra/identity/okta/approval-rbac.yaml
export CAVRA_CORS_ORIGINS=https://cavra-console.example.com
```

## Prerequisites

- An Okta OIDC app integration for CAVRA.
- An issuer URL for the Okta org authorization server or a custom authorization server.
- A token audience that matches the CAVRA app/client configuration.
- A `groups` claim in ID or access tokens.
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

- The issuer must exactly match the `iss` claim in tokens that CAVRA validates.
- Configure Okta group claims so only CAVRA-relevant groups are emitted.
- Refresh `approval-jwks.json` on a controlled schedule or when signing keys rotate.
