# Entitlement Status Contract

CAVRA Community Edition exposes a public-safe entitlement status contract for
future Enterprise and SaaS subscription workflows. The contract defines request
and response shapes only. It does not implement billing, payment-provider
integration, license-server validation, feature-grant storage, customer
subscription records, or SaaS backend logic.

## Purpose

The entitlement status contract gives Community clients, Trial workflows,
Enterprise packages, and future SaaS services a stable vocabulary for checking:

- subscription plan;
- license status;
- entitlement state;
- enabled features;
- locked features;
- expiration metadata.

## Request Shape

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "entitlement_status",
  "tenant_id": "tenant-demo",
  "requested_by": "console",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "feature_names": ["sso", "audit_export"],
    "requested_checks": [
      "subscription_status",
      "license_status",
      "feature_grants"
    ],
    "entitlement_boundary": "public request shape only; billing and license validation are private"
  }
}
```

## Response Shape

```json
{
  "schema_version": "cavra.saas_control_plane.response.v1",
  "operation": "entitlement_status",
  "status": "requires_private_service",
  "message": "Entitlement status requires private billing, subscription, and license-service validation.",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "summary": {
      "tenant_id": "tenant-demo",
      "entitlement_status": "trial",
      "subscription_plan": "enterprise-trial",
      "license_status": "valid",
      "enabled_features": ["sso"],
      "locked_features": ["ai_remediation"],
      "expires_at": "2026-07-02T00:00:00Z",
      "private_validation_required": true,
      "billing_boundary": "billing and subscription verification are private service responsibilities"
    }
  }
}
```

## Supported Entitlement States

- `active`
- `trial`
- `suspended`
- `expired`
- `missing`
- `unknown`

## Private Responsibilities

Private Enterprise or SaaS services must implement:

- billing-provider integration;
- subscription status checks;
- license signature and revocation validation;
- feature entitlement registry;
- tenant-specific feature grants;
- commercial account status;
- audit evidence for entitlement changes.

## Public Boundary

This repository may contain request builders, response summaries, schema
versions, validation, tests, and documentation.

This repository must not contain billing provider secrets, license keys,
license signing material, customer subscription records, customer payment data,
private entitlement registry data, SaaS backend implementation, or Enterprise
source code.

## Validation

Public tests cover entitlement request serialization, response summary
serialization, unknown entitlement status rejection, and private-module
requirement messaging.

## Next Recommendation

Delivered in the tenant, entitlement, and commercialization batch sync. The
hosted policy registry readiness and tenant audit-store operating contracts are
now delivered; continue with public billing/subscription boundary
documentation.
