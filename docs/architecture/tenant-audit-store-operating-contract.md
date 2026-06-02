# Tenant Audit-Store Operating Contract

CAVRA Community Edition exposes a public-safe tenant audit-store operating
contract for future Enterprise and SaaS workflows. The contract defines request
and response shapes only. It does not implement tenant archive storage,
customer evidence storage, retention enforcement, export connector delivery,
immutable storage validation, operating dashboards, or SaaS backend logic.

## Purpose

The tenant audit-store operating contract gives Community clients, Enterprise
packages, and future SaaS services a stable vocabulary for checking whether a
tenant audit store is healthy after launch.

The public request captures:

- tenant identifier;
- retention profile;
- evidence freshness window;
- required operating checks;
- public correlation metadata.

## Request Shape

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "tenant_audit_store_operating",
  "tenant_id": "tenant-demo",
  "requested_by": "console",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "retention_profile": "standard-365",
    "evidence_window": "last-24h",
    "required_checks": [
      "store_health",
      "retention_posture",
      "evidence_freshness",
      "export_readiness",
      "immutable_storage",
      "dashboard_visibility"
    ],
    "operating_boundary": "public request shape only; tenant audit-store operation is private"
  }
}
```

## Response Shape

```json
{
  "schema_version": "cavra.saas_control_plane.response.v1",
  "operation": "tenant_audit_store_operating",
  "status": "requires_private_service",
  "message": "Tenant audit-store operating status requires private archive, retention, evidence, export, and dashboard validation.",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "summary": {
      "tenant_id": "tenant-demo",
      "health_status": "ready",
      "retention_status": "degraded",
      "evidence_freshness_status": "ready",
      "export_status": "blocked",
      "latest_evidence_at": "2026-06-02T00:00:00Z",
      "retention_profile": "standard-365",
      "supported_export_formats": [
        "json",
        "zip"
      ],
      "blockers": [
        "export connector approval pending"
      ],
      "private_validation_required": true,
      "audit_store_boundary": "tenant archive storage, retention enforcement, export connectors, and customer evidence remain private service responsibilities"
    }
  }
}
```

## Supported Operating States

- `ready`
- `degraded`
- `blocked`
- `unknown`

## Supported Operating Checks

- `store_health`
- `retention_posture`
- `evidence_freshness`
- `export_readiness`
- `immutable_storage`
- `dashboard_visibility`

## Private Responsibilities

Private Enterprise or SaaS services must implement:

- tenant audit-store provisioning and health checks;
- tenant archive storage and isolation;
- retention policy enforcement;
- immutable storage verification;
- evidence freshness monitoring;
- governed evidence export jobs;
- export connector delivery;
- operating dashboard rollups and approvals;
- evidence for blockers and operator decisions.

## Public Boundary

This repository may contain request builders, response summaries, schema
versions, validation, tests, documentation, and synthetic examples.

This repository must not contain tenant archive storage code, customer evidence
payloads, customer identifiers, customer retention schedules, production
storage provider references, export connector credentials, provider URLs, SaaS
backend implementation, or Enterprise source code.

## Validation

Public tests cover:

- operating request serialization;
- default operating check lists;
- empty check rejection;
- token-like value rejection;
- operating summary serialization;
- invalid operating state rejection;
- mismatched response request rejection;
- private-module handoff messaging.

## Next Recommendation

Delivered in public billing/subscription boundary documentation. Continue with
private hosted policy registry readiness evidence in `cavra-enterprise`.
