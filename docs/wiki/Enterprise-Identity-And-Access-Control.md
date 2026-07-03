# CAVRA Enterprise Identity And Access Control

CAVRA Enterprise identity uses a public-safe contract for OIDC, SAML bridge, SCIM lifecycle, RBAC, ABAC, and break-glass operations.

## What Is Public

- OIDC/JWKS validation through `CAVRA_APPROVAL_OIDC_CONFIG`.
- RBAC mappings through `CAVRA_APPROVAL_RBAC_FILE`.
- Enterprise identity policy contract through `CAVRA_ENTERPRISE_IDENTITY_POLICY`.
- API endpoints:
  - `/identity/enterprise-contract`
  - `/identity/enterprise-readiness`
  - `/console/session`
  - `/console/security-boundary`

## Required Identity Areas

| Area | Contract |
| --- | --- |
| OIDC | Validate issuer, audience, expiry, not-before, JWKS key, RS256 signature, groups, roles, tenant, and workspace claims. |
| SAML bridge | Normalize SAML assertions into the same CAVRA claim contract through the IdP, gateway, or private Enterprise bridge. |
| SCIM | Synchronize groups, roles, tenant/workspace membership, deprovisioning, and audit evidence. |
| RBAC | CISO, security operator, platform security, model owner, auditor, and break-glass approver roles. |
| ABAC | Tenant, workspace, repository, environment, model owner, and data classification boundaries. |
| Break-glass | CAB role, reason, external reference, short TTL, and retained audit event. |

## Runtime Enforcement

Scoped approval decisions now enforce the Enterprise contract before legacy group authorization succeeds:

| Approval type | Required role | Boundary |
| --- | --- | --- |
| Runtime action approval | `security_operator` or `platform_security` | Matching tenant and workspace when supplied. |
| Model or AI artifact approval | `model_owner` or `ciso` | Matching tenant and workspace when supplied, plus model owner context. |
| Break-glass approval | `break_glass_approver` and `Change Advisory Board` | Reason, external reference, short TTL, and audit evidence. |

Community approvals with no Enterprise ABAC fields still use the existing group and repository RBAC path.

## Validation

```bash
python3 scripts/validate_enterprise_identity_readiness.py
python3 -m pytest tests/test_enterprise_identity.py tests/test_identity_references.py -q
```

The detailed repo document is [Enterprise Identity And Access Control](https://github.com/Huzefaaa2/cavra/blob/main/docs/enterprise-identity-access-control.md).
