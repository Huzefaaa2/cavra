# API

CAVRA API exposes health, version, policy packs, decisions, sessions, agents, repositories, approvals, evidence, integrations, MCP trust, risk events, compliance mappings, and sandbox endpoints. OpenAPI title: CAVRA API.

## Evidence Metadata

Evidence metadata endpoints:

- `GET /evidence`: list persisted evidence metadata.
- `POST /evidence`: upsert metadata by `session_id`.
- `GET /evidence/{session_id}`: fetch one metadata record.
- `POST /evidence/index-bundle`: index metadata from a local evidence bundle directory.

Default metadata path: `.cavra/api/evidence-metadata.json`.

Set `CAVRA_EVIDENCE_METADATA_STORE` to override the metadata store path for local or self-hosted deployments.
