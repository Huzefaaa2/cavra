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

## Approvals

Approval endpoints:

- `GET /approvals`: list approval requests with `state`, `approver_group`, `limit`, and `offset` filters.
- `POST /approvals`: create a pending approval request from a CAVRA decision.
- `GET /approvals/{approval_id}`: fetch one approval request.
- `POST /approvals/{approval_id}/approve`: approve a pending request with actor, reason, and optional external reference.
- `POST /approvals/{approval_id}/deny`: deny a pending request with actor, reason, and optional external reference.
- `POST /approvals/{approval_id}/expire`: expire a pending request.
- `POST /approvals/{approval_id}/deliver`: send configured approval provider requests and return redacted delivery evidence.
- `POST /approvals/{approval_id}/attach-decision`: attach approval summary and evidence refs to a decision payload.
- `POST /approvals/break-glass`: create a mandatory-reason emergency override.

Default approval path: `.cavra/api/approvals.json`.

Set `CAVRA_APPROVAL_STORE` to override the approval store path for local or self-hosted deployments.

Set `CAVRA_APPROVAL_DB` to use SQLite-backed approval persistence. `GET /approvals` supports the same `state`, `approver_group`, `limit`, and `offset` filters in JSON and SQLite modes. `GET /console/config` includes `approval_mode`.

Set `CAVRA_APPROVAL_ROUTING_FILE` to load repository-specific JSON or YAML approval routing rules at API startup. `POST /approvals` uses those rules unless the request payload supplies an explicit `approver_group`.

Approval decision endpoints accept an optional `actor_claims` object with OIDC-style fields such as `email`, `preferred_username`, `sub`, `groups`, `roles`, and `iss`. When claims are present, the actor must belong to the approval request's approver group before the API accepts approve or deny decisions.

Set `CAVRA_APPROVAL_OIDC_CONFIG` to enable signed OIDC JWT validation for approval decision payloads that include `actor_token`. The config must include `issuer`, `audience`, and `jwks` or `jwks_path`. RS256 signatures, issuer, audience, expiry, and not-before claims are validated before group authorization.

Set `CAVRA_APPROVAL_RBAC_FILE` to enable repository RBAC rules. The policy supports `group_mappings` and `repository_permissions` so repository owner groups can approve specific approver groups without receiving global approval authority.

Set `CAVRA_APPROVAL_PROVIDER_CONFIG` to a JSON or YAML provider config file to enable `POST /approvals/{approval_id}/deliver`. Delivery requests accept `provider`, `retries`, and `timeout_seconds`; responses include redacted request metadata, status, attempt count, and error state for evidence.

## Console

The static console under `apps/sandbox-ui` includes evidence search, PR attestation verification, and approval queue views. It can run as a standalone static demo or query the API evidence metadata and approval endpoints when hosted on the same origin or an allowed cross origin.

`GET /console/config` returns the console API base URL, metadata mode, allowed CORS origins, and endpoint paths. Configure cross-origin deployments with:

- `CAVRA_PUBLIC_API_BASE_URL`
- `CAVRA_CORS_ORIGINS`
