# Before the Agent Acts Sandbox and Evidence Console

Run locally:

```bash
python -m http.server 5173 --directory apps/sandbox-ui
```

The sandbox is a simulated AI-agent scenario using real CAVRA policy decisions. It shows agent actions, CAVRA decisions, policy rules, risk, evidence, compliance mapping, and Claude Code install CTA.

The same surface now includes the first hosted evidence console views:

- Evidence metadata search with signer, blocked-action, approval-state, and limit filters.
- PR attestation verification for selected sessions.
- Operational readiness summary for trust roots, SQLite search, attestation verification, and database migrations.

When the API is available at the same origin, the console attempts to load `GET /evidence?limit=50`. If the API is not available, it uses built-in sample evidence metadata so the console remains usable as a static demo.
