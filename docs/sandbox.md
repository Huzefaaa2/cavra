# Before the Agent Acts Sandbox and Evidence Console

Run locally:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

Deploy from GitHub Pages:

```bash
gh workflow run deploy-sandbox.yml --repo Huzefaaa2/cavra --ref main
```

The workflow at `.github/workflows/deploy-sandbox.yml` validates `config.js` and `sandbox.js`, copies `apps/sandbox-ui` into a static Pages artifact, writes `public/config.js` from `CAVRA_PUBLIC_API_BASE_URL`, includes the repository SVG diagrams, uploads the artifact with `actions/upload-pages-artifact`, opts JavaScript-based GitHub Actions into Node.js 24, and deploys with `actions/deploy-pages` only when the workflow runs on `main`.

The sandbox is a simulated AI-agent scenario using real CAVRA policy decisions. It shows agent actions, CAVRA decisions, policy rules, risk, evidence, compliance mapping, and Claude Code install CTA.

The sandbox uses the CAVRA mark from `apps/sandbox-ui/brand/` as a top-right hero lockup, sourced from the canonical brand files under `assets/brand/`.

The same surface now includes the first hosted evidence console views:

- Evidence metadata search with signer, blocked-action, approval-state, and limit filters.
- Telemetry-free public demo counters sourced from persisted backend sandbox activity metadata.
- Release-note links for design-partner demos, current public sandbox changes, release integrity work, and roadmap context.
- Evidence artifact listing with individual artifact and bundle download links when `CAVRA_EVIDENCE_ARTIFACT_ROOT` is configured.
- PR attestation verification for selected sessions.
- Console Session panel for validating signed OIDC bearer-token context and repository permissions.
- Policy Authoring and Rollout Changes for catalog summaries, draft validation, approval-bound signed policy publishing, rollout planning, and rollout apply.
- Production Readiness panel for OIDC, RBAC, CORS, evidence artifact root, policy catalog, and persistent store checks.
- Approval queue view with state and approver group filters.
- Approval queue actions for approve, deny, and expire on pending requests.
- Break-glass creation for emergency overrides with actor, reason, approver group, external reference, and TTL.
- Approval audit detail view for decision context, lifecycle history, evidence references, and external references.
- Recurrence Operations panel for endpoint remediation retry plans, owner digest evidence, suppression trend analytics, scheduled worker history, dry-run versus executed status, missed-run health, stale metadata, connector delivery failures, health alert delivery and acknowledgement records, owner/provider/action/category/worker filters, JSON detail views, and local export drill-downs.
- Operational readiness summary for trust roots, SQLite search, attestation verification, and database migrations.

When the API is available at the same origin, the console posts scenario runs to `/api/sandbox/run`, persists the resulting metadata through the API, loads public counters from `/api/sandbox/metrics`, loads `GET /evidence?limit=50`, and loads artifact detail from `/evidence/{session_id}/artifacts`. If the API is not available, it uses built-in sample evidence metadata and sample scenario events so the console remains usable as a static demo.

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

If the page is hosted separately, set `window.CAVRA_API_BASE = "https://api.cavra.example"` in `config.js` before loading `sandbox.js`. For GitHub Pages, set the repository variable `CAVRA_PUBLIC_API_BASE_URL` before running the deploy workflow. The console first reads `/console/config`, then posts `/api/sandbox/run` for backend-driven scenario runs, reads `/api/sandbox/metrics` for telemetry-free public counters, queries `/console/session`, `/deployment/production-readiness`, `/policy-pack-catalog`, `/evidence` with signer, blocked-count, approval-state, and limit filters, `/evidence/{session_id}/artifacts` for artifact downloads, `/endpoint-remediation-sla-escalation-actions` for retry-plan, owner-digest, and suppression-trend metadata, `/endpoint-remediation-sla-escalation-actions/dashboard` for recurrence operations counters, `/endpoint-remediation-sla-escalation-recurrence-automations` for worker run history, `/endpoint-remediation-sla-escalation-recurrence-automations/dashboard` for dry-run and execution outcomes, `/endpoint-remediation-sla-escalation-recurrence-automations/health` for missed-run and stale-metadata health, `/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts` and `/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/dashboard` for alert delivery and acknowledgement history, and `/approvals` with state and approver-group filters. Policy drafts post to `/policy-packs/draft`; rollout plans post to `/policy-rollouts/change-plan`; rollout applies post to `/policy-rollouts/apply-change`. Pending approval actions post to `/approvals/{approval_id}/approve`, `/approvals/{approval_id}/deny`, or `/approvals/{approval_id}/expire`. Break-glass creation posts to `/approvals/break-glass`, and audit details read `/approvals/{approval_id}`.

Backend scenario runs are available through:

- `GET /api/sandbox/scenarios`
- `GET /api/sandbox/metrics`
- `POST /api/sandbox/run`
- `GET /api/sandbox/runs/{run_id}`
- `GET /api/sandbox/runs/{run_id}/events`
- `GET /api/sandbox/runs/{run_id}/evidence`
- `GET /api/sandbox/runs/{run_id}/attestation`
- `GET /api/sandbox/runs/{run_id}/compliance`

`GET /api/sandbox/metrics` summarizes only CAVRA activity-store rows for `sandbox/before-the-agent-acts`. It returns aggregate run, decision, block, approval, and latest-run counters without cookies, browser identifiers, IP-derived identities, or third-party analytics.

For security, the API does not index arbitrary server-side bundle paths. Index evidence locally with `cavra evidence index` or `cavra evidence index --sqlite`, then persist metadata through the API or SQLite store. Artifact downloads only work for indexed sessions and only for allowlisted files under `CAVRA_EVIDENCE_ARTIFACT_ROOT/<session_id>/`. When OIDC or RBAC is configured, approval and break-glass console mutations require verified actor context from the Console Session token, `actor_token`, or `actor_claims`.
