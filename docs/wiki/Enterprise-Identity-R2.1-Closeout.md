# CAVRA Enterprise Identity R2.1 Closeout

Last updated: 2026-07-07

R2.1 is closed for the public CAVRA repository. The remaining real IdP, SCIM worker, customer directory, and tenant-specific evidence belongs to Managed or Enterprise deployment evidence rooms, not to public source code.

## What Is Complete

| Control | Public Status |
| --- | --- |
| OIDC/JWKS token validation contract | Implemented |
| SAML bridge output contract | Implemented |
| SCIM lifecycle contract | Implemented |
| RBAC role model | Implemented |
| ABAC runtime scope model | Implemented |
| Break-glass controls | Implemented |
| Runtime scoped approval enforcement | Implemented |
| API endpoints for identity contract and readiness | Implemented |
| Entra ID and Okta reference configuration | Implemented |
| Public-safe live identity packet validator | Implemented |
| Sanitized live-style packet example | Implemented |

## Evidence Boundary

The public repository proves CAVRA can:

- define the Enterprise identity contract;
- validate OIDC/JWKS, RBAC, ABAC, SAML bridge, SCIM lifecycle, and break-glass control shape;
- enforce scoped approval decisions at runtime;
- reject secret-like fields in live identity packets;
- validate a sanitized live-style packet without storing secrets.

Private Managed or Enterprise deployments must still attach their own:

- live IdP tenant configuration;
- SAML metadata or bridge evidence;
- SCIM sync worker logs;
- deprovisioning evidence;
- tenant directory membership evidence;
- production break-glass audit records.

Those artifacts must stay private or sanitized before publication.

## Verification

```bash
python3 scripts/validate_enterprise_identity_readiness.py

python3 scripts/validate_enterprise_live_identity_packet.py \
  --packet examples/identity/enterprise-live-identity-validation.live.sanitized.example.json \
  --output dist/test/enterprise-live-identity-validation-result.json

python3 -m pytest tests/test_enterprise_identity.py tests/test_identity_references.py -q
```

Expected live-style packet result:

```json
{
  "ready_for_live_enterprise_identity": true,
  "status": "ready",
  "blocker_count": 0
}
```

## R2.2 Handoff

R2.2 tenant persistence and isolation must consume the same `tenant_id` and `workspace_id` claims validated in R2.1. If a deployment changes IdP claim shape, SCIM group sync, or tenant/workspace mapping, the R2.1 live packet must be regenerated before R2.2 is accepted.

