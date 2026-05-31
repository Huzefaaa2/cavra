# Final Closeout Pilot Intake API

CAVRA includes a public-safe API scaffold for saving production pilot intake records after a final closeout trial.

## Endpoints

```http
POST /pilot-intakes
GET  /pilot-intakes
GET  /pilot-intakes/{intake_id}
GET  /pilot-intakes/{intake_id}/readiness
```

## What It Does

- Accepts the public `cavra.final_closeout_pilot_intake.v1` intake shape.
- Persists normalized records in a local JSON store for self-hosted evaluation.
- Computes readiness for repository/agent, CI/CD, connector, SSO/RBAC, retention, and Enterprise/SaaS handoff.
- Rejects secret-like field names and common token-shaped values.
- Exposes the endpoints through `/console/config`.
- Allows the Evidence Console to save a pilot intake snapshot when a CAVRA API is configured.

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

## Recommended Next Issue

Add tenant-scoped private persistence, authenticated update permissions, encrypted storage, and connector-backed handoff tasks in Enterprise or SaaS.
