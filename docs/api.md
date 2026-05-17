# API

CAVRA API exposes health, version, policy packs, decisions, sessions, agents, repositories, approvals, evidence, integrations, MCP trust, risk events, compliance mappings, and sandbox endpoints. OpenAPI title: CAVRA API.

## Evidence Metadata

Evidence metadata endpoints:

- `GET /evidence`: list persisted evidence metadata.
- `POST /evidence`: upsert metadata by `session_id`.
- `GET /evidence/{session_id}`: fetch one metadata record.

Default metadata path: `.cavra/api/evidence-metadata.json`.

Set `CAVRA_EVIDENCE_METADATA_STORE` to override the metadata store path for local or self-hosted deployments.

Set `CAVRA_EVIDENCE_METADATA_DB` to use SQLite-backed metadata persistence. `GET /evidence` supports query parameters in both JSON and SQLite modes:

- `session_id`
- `signer`
- `min_blocked`
- `has_approvals`
- `limit`
- `offset`

For security, the API does not accept arbitrary server-side bundle paths. Use `cavra evidence index` locally to extract metadata from a bundle, then persist the resulting metadata with `POST /evidence`.

## Console

The static console under `apps/sandbox-ui` includes evidence search and PR attestation verification views. It can run as a standalone static demo or query the API evidence metadata endpoint when hosted on the same origin or an allowed cross origin.

`GET /console/config` returns the console API base URL, metadata mode, allowed CORS origins, and endpoint paths. Configure cross-origin deployments with:

- `CAVRA_PUBLIC_API_BASE_URL`
- `CAVRA_CORS_ORIGINS`
