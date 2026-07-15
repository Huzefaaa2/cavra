# CAVRA Admin Console

The Admin Console is the administrator surface for CAVRA deployments. It is
separate from the public sandbox GUI and is intended for trusted operators who
manage deployment context, persistent stores, backups, retention, readiness, and
policy-pack lifecycle administration.

The admin API is disabled by default. Enable it only in trusted environments:

```bash
export CAVRA_ADMIN_ENABLED=true
export CAVRA_ADMIN_DEFAULT_ACTOR=local-admin
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

For Docker Desktop:

```bash
docker compose up -d --build
```

Then open:

- API: `http://127.0.0.1:8000`
- Sandbox GUI: `http://127.0.0.1:5173`
- Admin Console: `http://127.0.0.1:5174`

The full repository guide is maintained at
[`docs/admin-console.md`](https://github.com/Huzefaaa2/cavra/blob/main/docs/admin-console.md).
