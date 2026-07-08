# CAVRA Managed And Enterprise Cutover Runbook

The Managed and Enterprise cutover runbook turns the live validation plan into an executable production activation checklist. It is public-safe by design: it records sanitized references to private evidence, not tenant names, customer names, SMTP credentials, connector payloads, raw logs, prompts, or model data.

Use it after the [Managed And Enterprise Live Validation Plan](managed-enterprise-live-validation-plan.md) is ready and before a Managed or Enterprise environment is activated for a customer.

## What It Proves

The runbook requires sanitized references for:

- preflight freeze, staffing, release candidate, and evidence-room readiness;
- Enterprise identity, SSO/RBAC, break-glass, and tenant isolation validation;
- live connectors, scanners, runtime workflows, MCP/tool controls, and SMTP/report delivery;
- AISPM production gate readiness with no blockers;
- executive go/no-go decision and approval references;
- activation, rollback trigger, rollback rehearsal, and incident channel references;
- customer evidence-room, operating-review, public-safe status, and documentation closeout.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_cutover_runbook.py \
  --export-dir examples/managed-enterprise-cutover
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-cutover-runbook \
  --export-dir examples/managed-enterprise-cutover
```

## Validate A Live Sanitized Cutover Runbook

```bash
python3 scripts/validate_managed_enterprise_cutover_runbook.py \
  --runbook examples/managed-enterprise-cutover/managed-enterprise-cutover-runbook.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-cutover-runbook \
  --runbook examples/managed-enterprise-cutover/managed-enterprise-cutover-runbook.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_cutover": true,
  "blocker_count": 0
}
```

## Required Cutover Steps

| Step | Purpose |
| --- | --- |
| Preflight freeze | Confirm release candidate, change freeze, operator staffing, and evidence-room readiness. |
| Identity access | Validate Enterprise identity, SSO/RBAC, and break-glass controls. |
| Tenant isolation | Validate tenant isolation and persistence boundaries. |
| Connectors runtime | Validate live connectors, scanners, runtime workflows, and MCP/tool controls. |
| SMTP reporting | Validate production SMTP/report delivery and recipient policy. |
| AISPM gate | Validate AISPM production readiness with no blockers. |
| Go/no-go | Record executive go/no-go decision and approval references. |
| Activation | Activate Managed or Enterprise control plane under operator supervision. |
| Rollback rehearsal | Confirm rollback trigger, owner, and rehearsal evidence references. |
| Customer closeout | Attach customer evidence-room, operating-review, and closeout references. |
| Public status sync | Publish only customer-safe status and documentation references. |

## Evidence Boundary

Do not commit:

- tenant names;
- customer names;
- email addresses;
- SMTP credentials;
- connector tokens;
- raw connector responses;
- raw runtime logs;
- raw prompts;
- raw model data;
- customer payloads;
- private pricing, contracts, or legal terms.

Commit only sanitized references such as `evidence://`, `ticket://`, `audit://`, `runbook://`, `workflow://`, `vault://`, or `share://`.

## Relationship To Live Validation

The live validation plan proves each validator has run. The cutover runbook proves the production activation was controlled: the right operators were present, rollback was ready, go/no-go was recorded, customer evidence was archived, and only safe public status was synchronized.
