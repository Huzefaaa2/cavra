# OIDC/RBAC Deployment References

CAVRA can validate signed OIDC bearer tokens and apply repository-scoped RBAC before approval, break-glass, and policy write-back actions. This release adds deployment references for Microsoft Entra ID and Okta.

## Reference Bundles

- `examples/identity/entra-id-oidc-rbac`: generates CAVRA OIDC config, JWKS cache, RBAC policy, and environment exports from Entra ID OIDC discovery.
- `examples/identity/okta-oidc-rbac`: generates CAVRA OIDC config, JWKS cache, RBAC policy, and environment exports from Okta OIDC discovery.

Both references are operator-owned. CAVRA validates tokens and RBAC rules; identity administrators own application registration, token claims, group assignment, and key-rotation runbooks.

## Runtime Wiring

```bash
export CAVRA_APPROVAL_OIDC_CONFIG=.cavra/identity/entra/approval-oidc.json
export CAVRA_APPROVAL_RBAC_FILE=.cavra/identity/entra/approval-rbac.yaml
export CAVRA_CORS_ORIGINS=https://cavra-console.example.com
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

Validate the console/API identity boundary:

```bash
curl http://127.0.0.1:8000/console/security-boundary
curl http://127.0.0.1:8000/console/session \
  -H "Authorization: Bearer $CAVRA_CONSOLE_TOKEN"
```

## Entra ID

```bash
cd examples/identity/entra-id-oidc-rbac
cp variables.example.env .env
source .env
bash generate-cavra-identity-config.sh
```

Production controls:

- Use a tenant-specific v2.0 issuer.
- Configure the token audience to the CAVRA API application ID URI or client ID.
- Emit `groups` or `roles` claims for CAVRA approval groups.
- Map Entra group IDs to CAVRA approval groups in `approval-rbac.yaml`.
- Refresh `approval-jwks.json` when Entra signing keys rotate.

## Okta

```bash
cd examples/identity/okta-oidc-rbac
cp variables.example.env .env
source .env
bash generate-cavra-identity-config.sh
```

Production controls:

- Use the exact Okta issuer that appears in CAVRA tokens.
- Configure the token audience to the CAVRA API app or authorization server audience.
- Emit a constrained `groups` claim for CAVRA approval groups.
- Map Okta group names to CAVRA approval groups in `approval-rbac.yaml`.
- Refresh `approval-jwks.json` when Okta signing keys rotate.

## RBAC Model

CAVRA maps external groups to approval groups, then grants repository-scoped permissions:

```yaml
approval_rbac:
  group_mappings:
    CAVRA-IAM-Approvers: IAM
    CAVRA-Platform-Security: Platform Security
    CAVRA-Change-Advisory-Board: Change Advisory Board
  repository_permissions:
    - repository: payments/api
      approver_group: IAM
      groups:
        - IAM
      actions:
        - approved
        - denied
```

Break-glass actions require `Change Advisory Board` group membership when OIDC or RBAC is configured.

## User Stories

- As an IAM administrator, I can connect CAVRA approval decisions to Entra ID or Okta groups.
- As a platform engineer, I can generate CAVRA-ready OIDC and RBAC files from enterprise identity metadata.
- As a repository owner, I can approve only the repositories and approver groups granted to my identity group.
- As an auditor, I can inspect identity configuration, RBAC mappings, and console session output.

## Enterprise Challenge Solved

Enterprise consoles cannot rely on local demo identity. OIDC/RBAC deployment references make CAVRA's browser-visible approval and break-glass workflows align with enterprise identity, group assignment, and repository-specific authorization.

## Next Work

The next recommended work is public sandbox URL validation after deployment from `main` and continued release-governance record parity.
