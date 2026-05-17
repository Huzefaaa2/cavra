# Before the Agent Acts Sandbox and Evidence Console

Run locally:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

The sandbox is a simulated AI-agent scenario using real CAVRA policy decisions. It shows agent actions, CAVRA decisions, policy rules, risk, evidence, compliance mapping, and Claude Code install CTA.

The same surface now includes the first hosted evidence console views:

- Evidence metadata search with signer, blocked-action, approval-state, and limit filters.
- PR attestation verification for selected sessions.
- Approval queue view with state and approver group filters.
- Approval queue actions for approve, deny, and expire on pending requests.
- Operational readiness summary for trust roots, SQLite search, attestation verification, and database migrations.

When the API is available at the same origin, the console attempts to load `GET /evidence?limit=50`. If the API is not available, it uses built-in sample evidence metadata so the console remains usable as a static demo.

## API Wiring

The console supports both same-origin and cross-origin deployments.

Same-origin deployment:

```bash
CAVRA_EVIDENCE_METADATA_DB=.cavra/evidence/metadata.db uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

Host the console behind the same reverse proxy as the API and route `/evidence`, `/approvals`, and `/console/config` to the FastAPI service.

Cross-origin deployment:

```bash
CAVRA_PUBLIC_API_BASE_URL=https://api.cavra.example \
CAVRA_CORS_ORIGINS=https://console.cavra.example \
CAVRA_EVIDENCE_METADATA_DB=.cavra/evidence/metadata.db \
CAVRA_APPROVAL_PROVIDER_CONFIG=.cavra/approval-providers.yaml \
CAVRA_APPROVAL_OIDC_CONFIG=.cavra/approval-oidc.json \
CAVRA_APPROVAL_RBAC_FILE=.cavra/approval-rbac.yaml \
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

If the page is hosted separately, set `window.CAVRA_API_BASE = "https://api.cavra.example"` before loading `sandbox.js`. The console first reads `/console/config`, then queries `/evidence` with signer, blocked-count, approval-state, and limit filters and `/approvals` with state and approver-group filters. Pending approval actions post to `/approvals/{approval_id}/approve`, `/approvals/{approval_id}/deny`, or `/approvals/{approval_id}/expire`.

For security, the API does not index server-side bundle paths. Index evidence locally with `cavra evidence index` or `cavra evidence index --sqlite`, then persist metadata through the API or SQLite store.
