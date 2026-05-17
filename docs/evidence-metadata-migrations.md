# Evidence Metadata Migrations

CAVRA supports JSON metadata storage for local workflows and SQLite-backed metadata search for self-hosted pilots.

## SQLite Migration

The initial migration is:

```text
migrations/sqlite/001_evidence_metadata.sql
```

Apply it with:

```bash
cavra evidence migrate --sqlite .cavra/evidence/metadata.db
```

The migration command records applied SQL files in `schema_migrations`, so repeated runs are idempotent. Operators can still apply the SQL manually for inspection-only environments:

```bash
sqlite3 .cavra/evidence/metadata.db < migrations/sqlite/001_evidence_metadata.sql
```

Then run the API with:

```bash
CAVRA_EVIDENCE_METADATA_DB=.cavra/evidence/metadata.db uvicorn cavra.api:app --reload
```

## Search Filters

The SQLite metadata store supports:

- `session_id`
- `signer`
- `min_blocked`
- `has_approvals`
- `limit`
- `offset`

## Production Path

SQLite is the pilot database path. Production deployments should migrate the same logical table into the enterprise database selected for the CAVRA console. The required columns are:

- `session_id`
- `created_at`
- `signer`
- `decision_count`
- `blocked_count`
- `approval_required_count`
- `payload`

The `payload` column stores the full metadata JSON so schema additions remain backward compatible while indexed columns support common evidence search filters.
