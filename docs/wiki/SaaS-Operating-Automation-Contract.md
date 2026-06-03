# SaaS Operating Automation Contract

CAVRA Community Edition now exposes a public-safe SaaS operating automation
contract for future Enterprise and SaaS Control Plane handoff. The contract
defines request and response shapes only. It does not implement SaaS automation
workers, schedulers, billing integrations, license telemetry jobs, support
workflows, customer-success workflows, dashboard refresh jobs, escalation
drills, closeout retry workers, or customer data storage.

## Operation

The public operation is `saas_operating_automation`.

Required public-safe checks:

- `billing_monitoring`
- `license_telemetry_sync`
- `support_followup`
- `customer_success_review`
- `dashboard_refresh`
- `escalation_drill`
- `closeout_retry`

Supported public-safe statuses are `ready`, `scheduled`, `enabled`,
`automated`, `blocked`, and `unknown`.

## User Stories

- As a support leader, I can understand which post-closeout support follow-up
  and escalation drill checks must be validated privately.
- As a customer-success owner, I can see where recurring customer review
  cadence fits into SaaS operations.
- As a commercial operations owner, I can trace billing monitoring and license
  telemetry sync into the post-launch automation plan.
- As a platform engineer, I can build private automation services against a
  stable Community contract without placing private code in the public repo.

## Enterprise Challenge Solved

The contract gives teams a shared vocabulary for recurring SaaS operations
after final closeout. It makes billing, license telemetry, support,
customer-success, dashboard, escalation, and closeout retry readiness auditable
without exposing private implementation.

## Boundary

Public documentation and code may contain request and response shapes, schema
versions, synthetic examples, and tests. They must not contain Enterprise
source, SaaS backend code, scheduler implementation, automation workers,
billing records, support tickets, customer-success notes, customer identifiers,
production dashboard URLs, escalation webhooks, connector credentials, license
keys, signing material, paid policy packs, or customer audit payloads.

## API And CLI Surfaces

Community users can inspect the public contract with:

```bash
cavra saas contract
cavra saas operating-automation tenant-demo --requested-by console
```

The public API exposes `GET /saas/control-plane/contract` and `POST
/saas/operating-automation`. These surfaces generate public-safe request and
response payloads only. They do not run SaaS automation workers, schedulers,
connectors, billing checks, support workflows, customer-success workflows, or
private SaaS services.

## Evidence Console

The public Evidence Console includes a SaaS Operating Automation Contract panel
that renders the public request, public response, required checks, and
private-service boundary. It reads the API endpoints when configured and falls
back to a synthetic public-safe preview in hosted demo mode.

## Next Recommendation

Add public-safe documentation and interface guidance for future private
Enterprise/SaaS automation worker handoff packages while keeping private
automation execution, scheduler internals, connector credentials, customer
records, billing records, support workflows, and SaaS backend implementation
inside Enterprise or SaaS repositories.
