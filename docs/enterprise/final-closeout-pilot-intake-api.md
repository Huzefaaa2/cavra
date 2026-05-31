# Final Closeout Pilot Intake API

CAVRA now includes a public-safe API scaffold for saving production pilot intake records after a final closeout trial. The API is intended for self-hosted Enterprise or SaaS deployments where the customer controls the backing store.

## Boundary

The Community repository includes:

- the API contract,
- local JSON persistence for development and self-hosted evaluation,
- readiness scoring,
- sensitive-field rejection,
- Evidence Console save integration.

The Community repository must not include:

- customer production pilot responses,
- private connector routes,
- identity provider secrets,
- signing keys,
- license keys,
- commercial contracts,
- production evidence archives.

## Configuration

By default, the API stores pilot intake records in:

```bash
.cavra/api/pilot-intakes.json
```

Override the path for self-hosted deployments:

```bash
export CAVRA_PILOT_INTAKE_STORE=/var/lib/cavra/pilot-intakes.json
```

For SaaS and paid Enterprise, replace this local JSON store with the private tenant store. The public implementation is intentionally small and contains no license validation, tenant isolation, billing logic, or private connector implementation.

## Endpoints

```http
POST /pilot-intakes
GET  /pilot-intakes
GET  /pilot-intakes/{intake_id}
GET  /pilot-intakes/{intake_id}/readiness
```

`POST /pilot-intakes` accepts the public-safe `cavra.final_closeout_pilot_intake.v1` template shape. The API normalizes the record, adds storage-boundary metadata, computes readiness, and persists it locally.

## Readiness Areas

The readiness scorer evaluates:

- repository and agent scope,
- CI/CD required check,
- connector route status,
- SSO/RBAC mapping,
- retention and archive destination,
- Enterprise or SaaS handoff owner and start date.

Overall status can be:

- `ready`,
- `planned`,
- `needs_input`,
- `blocked`.

## Sensitive Material Rejection

The public API rejects fields whose names look like secret-bearing values, including tokens, passwords, private keys, signing keys, API keys, and webhook secrets. It also rejects common token-shaped values.

This is a guardrail, not a replacement for enterprise data-loss prevention. Production deployments should also use tenant isolation, encrypted storage, platform secret scanning, audit logging, and RBAC.

## Evidence Console

The Evidence Console can now save the synthetic pilot intake template to the configured CAVRA API. In hosted public demo mode, saving is disabled unless `CAVRA_PUBLIC_API_BASE_URL` or `window.CAVRA_API_BASE` points at an API deployment.

## Example

```bash
curl -X POST http://127.0.0.1:8000/pilot-intakes \
  -H 'content-type: application/json' \
  --data @examples/demos/final-closeout-trial/pilot-intake-template.json

curl http://127.0.0.1:8000/pilot-intakes
curl http://127.0.0.1:8000/pilot-intakes/{intake_id}/readiness
```

## Next Private Implementation

Private Enterprise or SaaS should add:

- tenant-scoped persistence,
- authenticated create/update permissions,
- encrypted storage,
- commercial workflow fields,
- connector-backed handoff tasks,
- audit trails for intake updates,
- export to CRM, ITSM, GRC, and customer success systems.
