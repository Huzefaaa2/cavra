# SaaS Operating Automation Contract

CAVRA Community Edition exposes a public-safe SaaS operating automation
contract for future Enterprise and SaaS Control Plane handoff. The contract
defines request and response shapes only. It does not implement SaaS automation
workers, schedulers, billing-provider integrations, license telemetry jobs,
support workflows, customer-success workflows, dashboard refresh jobs,
escalation drills, closeout retry workers, or customer data storage.

## Purpose

After final customer operating closeout, Enterprise teams need recurring
evidence that trial-to-paid customers remain operationally governed. This
contract gives Community clients, Enterprise packages, and future SaaS services
a stable vocabulary for checking whether post-closeout automation is ready.

The public operation is `saas_operating_automation`.

## Public Request Shape

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "saas_operating_automation",
  "tenant_id": "tenant-demo",
  "requested_by": "console",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "automation_scope": "trial-to-paid-customer-scale",
    "automation_cadence": "daily",
    "required_checks": [
      "billing_monitoring",
      "license_telemetry_sync",
      "support_followup",
      "customer_success_review",
      "dashboard_refresh",
      "escalation_drill",
      "closeout_retry"
    ],
    "automation_boundary": "public request shape only; SaaS operating automation execution is private"
  }
}
```

## Public Response Shape

```json
{
  "schema_version": "cavra.saas_control_plane.response.v1",
  "operation": "saas_operating_automation",
  "status": "requires_private_service",
  "message": "SaaS operating automation requires private billing monitoring, license telemetry, support, customer-success, dashboard, escalation, closeout retry, and scheduler validation.",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "summary": {
      "tenant_id": "tenant-demo",
      "automation_status": "scheduled",
      "billing_monitoring_status": "enabled",
      "license_telemetry_status": "automated",
      "support_followup_status": "ready",
      "customer_success_review_status": "scheduled",
      "dashboard_refresh_status": "automated",
      "escalation_drill_status": "blocked",
      "closeout_retry_status": "enabled",
      "automation_scope": "trial-to-paid-customer-scale",
      "automation_cadence": "daily",
      "blockers": ["escalation drill owner pending"],
      "private_validation_required": true,
      "automation_boundary": "billing systems, license telemetry, support workflows, customer-success records, dashboard refresh jobs, escalation drills, closeout retries, and scheduler execution remain private service responsibilities"
    },
    "private_modules_required": [
      "billing monitoring",
      "license telemetry sync",
      "support follow-up",
      "customer-success review",
      "dashboard refresh automation",
      "escalation drill scheduler",
      "closeout retry automation"
    ],
    "next_step": "See docs/architecture/saas-operating-automation-contract.md"
  }
}
```

## Operating Checks

| Check | Private responsibility |
| --- | --- |
| `billing_monitoring` | Verify recurring subscription and billing observability checks. |
| `license_telemetry_sync` | Verify recurring license-service telemetry sync. |
| `support_followup` | Verify scheduled support follow-up after closeout. |
| `customer_success_review` | Verify recurring customer-success review cadence. |
| `dashboard_refresh` | Verify operating dashboard refresh automation. |
| `escalation_drill` | Verify recurring escalation and on-call drill readiness. |
| `closeout_retry` | Verify failed closeout delivery and follow-up retry automation. |

Supported public-safe statuses are `ready`, `scheduled`, `enabled`,
`automated`, `blocked`, and `unknown`.

## Boundary

This public repository may contain:

- request and response dataclasses;
- schema version constants;
- public-safe check names;
- local serialization and validation tests;
- documentation and synthetic examples.

This public repository must not contain:

- Enterprise source code;
- SaaS backend implementation;
- scheduler or automation worker implementation;
- billing-provider integration code;
- billing records or invoice data;
- license telemetry payloads;
- support ticket contents;
- customer-success notes;
- customer health scores;
- private customer identifiers;
- production dashboard URLs;
- escalation webhooks;
- provider account IDs;
- connector credentials;
- license keys or signing material;
- paid policy packs;
- customer audit payloads.

## Validation

Public tests cover:

- contract description listing the operation;
- request serialization;
- empty-check rejection;
- token-like value rejection;
- response serialization;
- invalid status rejection;
- mismatched request/response rejection;
- private service handoff messaging.

## API And CLI Surfaces

Community Edition exposes public-safe surfaces for contract consumers:

```bash
cavra saas contract
cavra saas operating-automation tenant-demo --requested-by console
```

The API exposes:

- `GET /saas/control-plane/contract`
- `POST /saas/operating-automation`

Both surfaces return request and response shapes only. `POST
/saas/operating-automation` returns a `requires_private_service` response by
default and does not run automation workers, schedulers, connectors, billing
checks, support workflows, or customer-success workflows.

## Evidence Console Surface

The public Evidence Console includes a SaaS Operating Automation Contract panel
that renders the public-safe request, response, required checks, private
modules required, and private-service boundary. It reads `GET
/saas/control-plane/contract` and `POST /saas/operating-automation` when a
CAVRA API is configured, and it falls back to a synthetic public-safe preview in
hosted demo mode.

## Next Recommendation

Add private Enterprise/SaaS implementation handoff readiness for real SaaS
operating automation workers while keeping Enterprise source, SaaS services,
credentials, and customer data outside the public Community repository.
