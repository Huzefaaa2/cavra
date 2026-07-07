# CAVRA Enterprise Live Identity Validation Packet

Last updated: 2026-07-07

This page defines the R2.1 live identity evidence packet used to close the gap between the public Enterprise identity contract and a real customer or private Enterprise identity deployment.

The packet is intentionally public-safe. It records pass/fail status, sanitized context, and evidence references only. It must not contain OIDC bearer tokens, SCIM bearer tokens, SAML certificates, private keys, passwords, client secrets, raw directory exports, or user records.

## What It Proves

The live packet proves that a real environment has validated:

| Area | Evidence required |
| --- | --- |
| OIDC token validation | Issuer, audience, expiry, not-before, JWKS key, and RS256 signature validation passed. |
| RBAC group mapping | Customer groups map to CAVRA roles for CISO, security operator, platform security, model owner, auditor, and break-glass approver. |
| ABAC runtime scope | Tenant, workspace, repository, environment, model owner, and data classification attributes are present in actor and resource decisions. |
| SCIM group sync | Group-to-role synchronization completed in the private tenant directory. |
| SCIM deprovisioning | Disabled or removed identities lose active CAVRA role membership within 60 minutes. |
| Break-glass audit | CAB role, reason, external reference, short TTL, and retained audit evidence are present. |
| Audit evidence retention | Identity validation evidence is retained in the evidence room with public-safe redaction. |

## Packet Shape

Start from the sample packet:

```bash
cp examples/identity/enterprise-live-identity-validation.sample.json \
  .cavra/identity/enterprise-live-identity-validation.json
```

Replace sample values with live, redacted evidence metadata:

- set `environment.validation_mode` to `live`;
- set the real `identity_provider`, `issuer`, `tenant_id`, `workspace_id`, and repository context;
- keep only evidence references, counts, timestamps, and public-safe summaries;
- do not include secrets, raw tokens, SAML material, SCIM bearer values, private keys, or raw user records.

## Validation Command

```bash
python3 scripts/validate_enterprise_live_identity_packet.py \
  --packet .cavra/identity/enterprise-live-identity-validation.json \
  --output dist/enterprise-live-identity-validation-result.json
```

The completion condition is:

```json
{
  "ready_for_live_enterprise_identity": true,
  "status": "ready",
  "blocker_count": 0
}
```

The checked-in sample packet is intentionally marked `validation_mode: sample`, so it validates structurally but does not return ready:

```bash
python3 scripts/validate_enterprise_live_identity_packet.py \
  --packet examples/identity/enterprise-live-identity-validation.sample.json \
  --allow-not-ready
```

The repository also includes a sanitized live-style packet for public verification of the closeout gate:

```bash
python3 scripts/validate_enterprise_live_identity_packet.py \
  --packet examples/identity/enterprise-live-identity-validation.live.sanitized.example.json \
  --output dist/test/enterprise-live-identity-validation-result.json
```

## R2.1 Exit Criteria

R2.1 is public-code complete when the contract, API endpoints, runtime scoped approval enforcement, live packet validator, and sanitized live-style packet are implemented and tested.

R2.1 is production-evidence complete only after a private or customer deployment produces a live packet with:

- all required checks present;
- every required check passing;
- no secret-like fields;
- `validation_mode: live`;
- SCIM deprovisioning SLA at or below 60 minutes;
- retained public-safe evidence references.

The same `tenant_id` and `workspace_id` values become required inputs for R2.2 tenant persistence and isolation validation.

See [Enterprise Identity R2.1 Closeout](enterprise-identity-r2-closeout.md) for the public closeout boundary.
