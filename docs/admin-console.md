# CAVRA Admin Console

The CAVRA Admin Console is a dedicated operator surface for self-hosted and managed deployments. It is separate from the public sandbox GUI. The sandbox is for evaluators and policy operators; the Admin Console is for deployment administrators who manage runtime topology, stores, backup plans, retention posture, readiness checks, and policy-pack lifecycle controls.

The admin API is disabled by default. Enable it only for trusted administrator environments:

```bash
export CAVRA_ADMIN_ENABLED=true
export CAVRA_ADMIN_DEFAULT_ACTOR=local-admin
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

For Docker Desktop testing, `docker compose up -d --build` enables the admin API for the local compose stack and serves:

| Surface | URL |
| --- | --- |
| CAVRA API | `http://127.0.0.1:8000` |
| Sandbox GUI | `http://127.0.0.1:5173` |
| Admin Console | `http://127.0.0.1:5174` |

## Admin Capabilities

The console currently covers:

- deployment context and runtime topology;
- production readiness gate;
- persistent API store inventory;
- backup planning and explicit backup run confirmation;
- retention plan generation;
- policy-pack catalog review;
- policy-pack upload validation;
- policy-pack publish plan;
- approval request creation for policy publishing.

## API Boundary

All admin endpoints are under `/admin/*`.

| Endpoint | Purpose |
| --- | --- |
| `GET /admin/status` | Admin availability, actor context, deployment context, security boundary, and store summary. |
| `GET /admin/readiness` | Production readiness gate using the same backend contract as `/deployment/production-readiness`. |
| `GET /admin/stores` | Persistent store inventory. |
| `POST /admin/backups/plan` | Non-mutating backup plan. |
| `POST /admin/backups/run` | Backup execution; requires `confirm` set to `BACKUP`. |
| `POST /admin/retention-plan` | Retention plan generation. |
| `GET /admin/policy-packs` | Policy-pack catalog. |
| `POST /admin/policy-packs/upload` | Parse and validate YAML/JSON policy pack content. |
| `POST /admin/policy-packs/publish-plan` | Build a publish plan and digest-bound diff. |
| `POST /admin/policy-packs/publish-request` | Create an approval-bound publish request. |
| `POST /admin/policy-packs/publish` | Publish after approval validation. |

## Security Notes

- Keep `CAVRA_ADMIN_ENABLED` unset for public demos and evaluator-only deployments.
- In production, pair admin routes with OIDC/RBAC settings through `CAVRA_APPROVAL_OIDC_CONFIG` and `CAVRA_APPROVAL_RBAC_FILE`.
- Do not expose the admin console through an unauthenticated public origin.
- Backup execution writes to the API runtime filesystem path supplied by the administrator. For production, use a mounted volume or managed backup workflow.

## Local Smoke Test

```bash
docker compose up -d --build
curl http://127.0.0.1:8000/admin/status
open http://127.0.0.1:5174
```

To verify the guard:

```bash
CAVRA_ADMIN_ENABLED=false uvicorn cavra.api:app --host 127.0.0.1 --port 8000
curl -i http://127.0.0.1:8000/admin/status
```

The disabled response should be `404`.
