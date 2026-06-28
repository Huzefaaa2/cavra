# Final Closeout Pilot Intake API

CAVRA includes a public-safe API scaffold for saving production pilot intake records after a final closeout trial.

## Endpoints

```http
POST /pilot-intakes
GET  /pilot-intakes
GET  /pilot-intakes/{intake_id}
GET  /pilot-intakes/{intake_id}/readiness
POST /pilot-intakes/{intake_id}/private-handoff-plan
```

## What It Does

- Accepts the public `cavra.final_closeout_pilot_intake.v1` intake shape.
- Persists normalized records in a local JSON store for self-hosted evaluation.
- Computes readiness for repository/agent, CI/CD, connector, SSO/RBAC, retention, and Enterprise/SaaS handoff.
- Rejects secret-like field names and common token-shaped values.
- Exposes the endpoints through `/console/config`.
- Allows the Evidence Console to save a pilot intake snapshot when a CAVRA API is configured.
- Produces a public-safe private handoff plan for tenant-scoped storage, authenticated updates, encrypted storage, and connector-backed implementation tasks.

## Configuration

```bash
export CAVRA_PILOT_INTAKE_STORE=/var/lib/cavra/pilot-intakes.json
```

Default local path:

```bash
.cavra/api/pilot-intakes.json
```

## Boundary

The Community repository contains only API contracts, local development persistence, readiness scoring, and public-safe documentation. Customer-specific pilot responses, private connector routes, production identity mappings, commercial data, and production evidence archives belong in private Enterprise or SaaS storage.

## Private Handoff Plan

`POST /pilot-intakes/{intake_id}/private-handoff-plan` returns:

- tenant persistence contract,
- authenticated update requirements,
- encrypted storage requirements,
- private connector task placeholders for CRM, ITSM, GRC, SaaS tenant, enterprise repository, customer success, and security review workflows.

The endpoint does not perform private connector mutation from Community code.

## Recommended Next Issue

Move this handoff plan into private Enterprise or SaaS services with tenant database writes, encrypted storage, authenticated update decisions, audit trails, and live connector execution.
