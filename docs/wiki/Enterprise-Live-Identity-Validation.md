# Enterprise Live Identity Validation

CAVRA R2.1 now includes a public-safe live identity validation packet for proving real IdP and SCIM evidence without publishing secrets.

## Required Checks

| Check | Required proof |
| --- | --- |
| `oidc_token_validation` | Issuer, audience, expiry, not-before, JWKS key, and RS256 signature validation passed. |
| `rbac_group_mapping` | Enterprise groups map to CISO, security operator, platform security, model owner, auditor, and break-glass roles. |
| `abac_runtime_scope` | Tenant, workspace, repository, environment, model owner, and data classification attributes are present. |
| `scim_group_sync` | SCIM group and role synchronization completed. |
| `scim_deprovisioning` | Deprovisioning evidence meets the 60 minute SLA. |
| `break_glass_audit` | CAB role, reason, external reference, short TTL, and audit event are retained. |
| `audit_evidence_retention` | Public-safe identity evidence references are retained. |

## Command

```bash
python3 scripts/validate_enterprise_live_identity_packet.py \
  --packet .cavra/identity/enterprise-live-identity-validation.json \
  --output dist/enterprise-live-identity-validation-result.json
```

The final packet must return:

```json
{
  "ready_for_live_enterprise_identity": true,
  "status": "ready",
  "blocker_count": 0
}
```

The sample at `examples/identity/enterprise-live-identity-validation.sample.json` is shape-only and stays blocked until `environment.validation_mode` is set to `live` with real redacted evidence.

Detailed repo documentation: [Enterprise Live Identity Validation](https://github.com/Huzefaaa2/cavra/blob/main/docs/enterprise-live-identity-validation.md).
