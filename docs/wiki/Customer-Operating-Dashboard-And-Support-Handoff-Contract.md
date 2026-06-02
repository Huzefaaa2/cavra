# Customer Operating Dashboard And Support Handoff Contract

Status date: 2026-06-02.

## Purpose

CAVRA Community Edition now exposes public-safe request and response contracts
for customer operating dashboard readiness and support handoff readiness. The
contracts let future Enterprise and SaaS services report whether billing,
license-service telemetry, support ownership, customer-success ownership,
escalation readiness, dashboard visibility, and release acceptance are ready
after customer launch.

## Public Contract

Implemented in `src/cavra/saas_control_plane.py`:

- `customer_operating_dashboard` operation;
- `build_customer_operating_dashboard_request`;
- `CustomerOperatingDashboardSummary`;
- `build_customer_operating_dashboard_response`;
- `support_handoff_readiness` operation;
- `build_support_handoff_readiness_request`;
- `SupportHandoffReadinessSummary`;
- `build_support_handoff_readiness_response`.

Supported states:

- `ready`
- `degraded`
- `blocked`
- `unknown`

## Private Boundary

The public repository defines shapes and validation only. Customer records,
customer health scores, support ticket contents, customer-success notes,
production dashboard URLs, billing-provider integration code, invoice data,
license-service source code, license keys, signing material, provider account
IDs, webhook URLs, connector credentials, SaaS backend code, and Enterprise
source code remain private.

## User Story

As a SaaS operator, I can see whether billing observability, license telemetry,
support handoff, customer-success handoff, escalation routing, dashboard
visibility, and release acceptance would block steady-state customer operation
before the private service exposes actual customer data.

## Enterprise Value

This contract turns customer operating readiness into a stable public
vocabulary. It helps buyers understand the Enterprise operating model while
preserving strict open-core boundaries around dashboards, support systems,
customer records, and SaaS backend implementation.

## Validation

Public tests cover request serialization, default check lists, invalid status
rejection, sensitive payload rejection, summary serialization, mismatched
request rejection, and private-module handoff messaging.

## Next Recommendation

Continue private SaaS operating automation for trial-to-paid customer scale.
