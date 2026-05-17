# Before the Agent Acts Sandbox and Evidence Console

Run locally:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

The sandbox is a simulated AI-agent scenario using real CAVRA policy decisions. It shows agent actions, CAVRA decisions, policy rules, risk, evidence, compliance mapping, and Claude Code install CTA.

The same surface now includes the first hosted evidence console views:

- Evidence metadata search with signer, blocked-action, approval-state, and limit filters.
- Evidence artifact listing with individual artifact and bundle download links when `CAVRA_EVIDENCE_ARTIFACT_ROOT` is configured.
- PR attestation verification for selected sessions.
- Console Session panel for validating signed OIDC bearer-token context and repository permissions.
- Policy Authoring and Rollout Changes for catalog summaries, draft validation, rollout planning, and rollout apply.
- Production Readiness panel for OIDC, RBAC, CORS, evidence artifact root, policy catalog, and persistent store checks.
- Approval queue view with state and approver group filters.
- Approval queue actions for approve, deny, and expire on pending requests.
- Break-glass creation for emergency overrides with actor, reason, approver group, external reference, and TTL.
- Approval audit detail view for decision context, lifecycle history, evidence references, and external references.
- Operational readiness summary for trust roots, SQLite search, attestation verification, and database migrations.

When the API is available at the same origin, the console attempts to load `GET /evidence?limit=50` and artifact detail from `/evidence/{session_id}/artifacts`. If the API is not available, it uses built-in sample evidence metadata so the console remains usable as a static demo.

## API Wiring

The console supports both same-origin and cross-origin deployments.

Same-origin deployment:

```bash
CAVRA_EVIDENCE_METADATA_DB=.cavra/evidence/metadata.db \
CAVRA_EVIDENCE_ARTIFACT_ROOT=.cavra/evidence/artifacts \
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

Host the console behind the same reverse proxy as the API and route `/evidence`, `/approvals`, and `/console/config` to the FastAPI service.

Cross-origin deployment:

```bash
CAVRA_PUBLIC_API_BASE_URL=https://api.cavra.example \
CAVRA_CORS_ORIGINS=https://console.cavra.example \
CAVRA_EVIDENCE_METADATA_DB=.cavra/evidence/metadata.db \
CAVRA_EVIDENCE_ARTIFACT_ROOT=.cavra/evidence/artifacts \
CAVRA_APPROVAL_PROVIDER_CONFIG=.cavra/approval-providers.yaml \
CAVRA_APPROVAL_OIDC_CONFIG=.cavra/approval-oidc.json \
CAVRA_APPROVAL_RBAC_FILE=.cavra/approval-rbac.yaml \
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

If the page is hosted separately, set `window.CAVRA_API_BASE = "https://api.cavra.example"` before loading `sandbox.js`. The console first reads `/console/config`, then queries `/console/session`, `/deployment/production-readiness`, `/policy-pack-catalog`, `/evidence` with signer, blocked-count, approval-state, and limit filters, `/evidence/{session_id}/artifacts` for artifact downloads, and `/approvals` with state and approver-group filters. Policy drafts post to `/policy-packs/draft`; rollout plans post to `/policy-rollouts/change-plan`; rollout applies post to `/policy-rollouts/apply-change`. Pending approval actions post to `/approvals/{approval_id}/approve`, `/approvals/{approval_id}/deny`, or `/approvals/{approval_id}/expire`. Break-glass creation posts to `/approvals/break-glass`, and audit details read `/approvals/{approval_id}`.

For security, the API does not index arbitrary server-side bundle paths. Index evidence locally with `cavra evidence index` or `cavra evidence index --sqlite`, then persist metadata through the API or SQLite store. Artifact downloads only work for indexed sessions and only for allowlisted files under `CAVRA_EVIDENCE_ARTIFACT_ROOT/<session_id>/`. When OIDC or RBAC is configured, approval and break-glass console mutations require verified actor context from the Console Session token, `actor_token`, or `actor_claims`.
