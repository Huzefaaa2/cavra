# Hosted Policy Registry Readiness Contract

CAVRA Community Edition exposes a public-safe hosted policy registry readiness
contract for future Enterprise and SaaS operating workflows. The contract
defines request and response shapes only. It does not implement the hosted
registry service, artifact delivery, tenant catalog storage, paid policy packs,
entitlement lookups, approval workflows, rollout telemetry, or SaaS backend
logic.

## Purpose

The hosted policy registry readiness contract gives Community clients,
Enterprise packages, and future SaaS services a stable vocabulary for checking
whether a tenant can depend on hosted policy registry operation after launch.

The public request captures:

- tenant identifier;
- catalog scope;
- optional policy-pack references;
- required readiness checks;
- public correlation metadata.

## Request Shape

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "policy_registry_readiness",
  "tenant_id": "tenant-demo",
  "requested_by": "console",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "policy_pack_refs": [
      "starter-policy-1",
      "starter-policy-2"
    ],
    "catalog_scope": "tenant-default",
    "required_checks": [
      "service_availability",
      "catalog_freshness",
      "policy_pack_versions",
      "artifact_integrity",
      "entitlement_scope",
      "approval_state"
    ],
    "readiness_boundary": "public request shape only; hosted policy registry operation is private"
  }
}
```

## Response Shape

```json
{
  "schema_version": "cavra.saas_control_plane.response.v1",
  "operation": "policy_registry_readiness",
  "status": "requires_private_service",
  "message": "Hosted policy registry readiness requires private registry, artifact, entitlement, and rollout validation.",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "summary": {
      "tenant_id": "tenant-demo",
      "readiness_status": "degraded",
      "catalog_status": "ready",
      "latest_catalog_version": "catalog-2026.06.02",
      "policy_pack_count": 12,
      "checked_at": "2026-06-02T00:00:00Z",
      "blockers": [
        "approval workflow pending"
      ],
      "private_validation_required": true,
      "registry_boundary": "hosted registry availability, artifact delivery, and tenant catalog validation are private service responsibilities"
    }
  }
}
```

## Supported Readiness States

- `ready`
- `degraded`
- `blocked`
- `unknown`

## Supported Readiness Checks

- `service_availability`
- `catalog_freshness`
- `policy_pack_versions`
- `artifact_integrity`
- `entitlement_scope`
- `approval_state`

## Private Responsibilities

Private Enterprise or SaaS services must implement:

- hosted registry availability checks;
- tenant policy catalog storage;
- policy-pack artifact storage and delivery;
- artifact integrity verification;
- tenant entitlement lookups;
- approval workflow state;
- rollout telemetry and operating dashboards;
- evidence for readiness blockers and operator decisions.

## Public Boundary

This repository may contain request builders, response summaries, schema
versions, validation, tests, documentation, and synthetic examples.

This repository must not contain hosted registry source code, paid policy pack
content, tenant policy catalogs, customer identifiers, customer policy
metadata, entitlement registry records, provider URLs, connector credentials,
SaaS backend implementation, or Enterprise source code.

## Validation

Public tests cover:

- readiness request serialization;
- default readiness check lists;
- empty readiness check rejection;
- token-like value rejection;
- readiness summary serialization;
- invalid readiness state rejection;
- negative policy-pack count rejection;
- private-module requirement messaging.

## Next Recommendation

Delivered in the public tenant audit-store operating contract and
billing/subscription boundary documentation. Continue with private hosted
policy registry readiness evidence in `cavra-enterprise`.
