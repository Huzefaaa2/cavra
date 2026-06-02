# Customer Operating Dashboard and Support Handoff Contract

CAVRA Community Edition exposes public-safe request and response contracts for
future Enterprise and SaaS customer operating dashboards and support handoff
readiness. These contracts define vocabulary and payload shapes only. They do
not implement dashboards, support queues, customer-success systems, billing
telemetry, license-service telemetry, escalation routing, customer health
records, or SaaS backend logic.

## Purpose

After private Enterprise PRs #70-#73, CAVRA can describe the final customer
operating closeout path without exposing the private implementation. This
contract gives Community clients, Enterprise packages, and future SaaS services
stable public shapes for:

- customer operating dashboard readiness;
- support and customer-success handoff readiness;
- escalation readiness;
- billing and license-service observability status vocabulary;
- release acceptance and final operating closeout boundaries.

## Customer Operating Dashboard Request

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "customer_operating_dashboard",
  "tenant_id": "tenant-demo",
  "requested_by": "console",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "dashboard_scope": "hosted-saas-operations",
    "evidence_window": "last-7d",
    "required_checks": [
      "dashboard_visibility",
      "billing_observability",
      "license_service_telemetry",
      "support_handoff",
      "customer_success_health",
      "escalation_readiness",
      "release_acceptance"
    ],
    "dashboard_boundary": "public request shape only; customer operating dashboards are private"
  }
}
```

## Customer Operating Dashboard Response

```json
{
  "schema_version": "cavra.saas_control_plane.response.v1",
  "operation": "customer_operating_dashboard",
  "status": "requires_private_service",
  "message": "Customer operating dashboard status requires private billing, license-service, support, customer-success, escalation, and release closeout validation.",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "summary": {
      "tenant_id": "tenant-demo",
      "dashboard_status": "ready",
      "billing_status": "ready",
      "license_service_status": "degraded",
      "support_handoff_status": "ready",
      "customer_success_status": "ready",
      "escalation_status": "blocked",
      "release_closeout_status": "ready",
      "latest_dashboard_at": "2026-06-02T00:00:00Z",
      "dashboard_scope": "hosted-saas-operations",
      "blockers": [
        "escalation route approval pending"
      ],
      "private_validation_required": true
    }
  }
}
```

## Support Handoff Request

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "support_handoff_readiness",
  "tenant_id": "tenant-demo",
  "requested_by": "console",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "handoff_scope": "hosted-saas-support",
    "support_tier": "enterprise",
    "required_checks": [
      "support_owner_assignment",
      "customer_success_owner_assignment",
      "escalation_routing",
      "customer_health_review",
      "handoff_dashboard",
      "release_owner_acceptance"
    ],
    "handoff_boundary": "public request shape only; support and customer-success handoff is private"
  }
}
```

## Support Handoff Response

```json
{
  "schema_version": "cavra.saas_control_plane.response.v1",
  "operation": "support_handoff_readiness",
  "status": "requires_private_service",
  "message": "Support handoff readiness requires private support, customer-success, escalation, health-review, and dashboard validation.",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "summary": {
      "tenant_id": "tenant-demo",
      "support_status": "ready",
      "customer_success_status": "ready",
      "escalation_status": "degraded",
      "health_review_status": "ready",
      "dashboard_status": "blocked",
      "support_tier": "enterprise",
      "handoff_scope": "hosted-saas-support",
      "blockers": [
        "handoff dashboard approval pending"
      ],
      "private_validation_required": true
    }
  }
}
```

## Supported Statuses

- `ready`
- `degraded`
- `blocked`
- `unknown`

## Private Responsibilities

Private Enterprise or SaaS services must implement:

- customer operating dashboard data collection;
- billing and subscription observability;
- license-service telemetry;
- support queue and owner lookup;
- customer-success owner lookup;
- customer health review;
- escalation routing and on-call validation;
- release owner acceptance;
- final customer operating closeout evidence;
- dashboard persistence, reporting, and access controls.

## Public Boundary

This repository may contain request builders, response summaries, schema
versions, validation, tests, documentation, and synthetic examples.

This repository must not contain customer records, customer health scores,
support ticket contents, customer-success notes, production dashboard URLs,
billing-provider integration code, invoice data, license-service source code,
license keys, signing material, provider account IDs, webhook URLs, connector
credentials, SaaS backend implementation, or Enterprise source code.

## Validation

Public tests cover:

- customer operating dashboard request serialization;
- support handoff readiness request serialization;
- default check lists;
- empty check rejection;
- token-like value rejection;
- summary serialization;
- invalid state rejection;
- mismatched response request rejection;
- private-module handoff messaging.

## Next Recommendation

Continue private SaaS operating automation for trial-to-paid customer scale
using these public-safe contracts as the Community boundary.
