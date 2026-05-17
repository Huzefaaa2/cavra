# Evidence Metadata Migrations

CAVRA supports SQLite-backed evidence metadata search for self-hosted pilots.

Migration:

```text
migrations/sqlite/001_evidence_metadata.sql
```

Apply:

```bash
sqlite3 .cavra/evidence/metadata.db < migrations/sqlite/001_evidence_metadata.sql
```

Run API:

```bash
CAVRA_EVIDENCE_METADATA_DB=.cavra/evidence/metadata.db uvicorn cavra.api:app --reload
```

Search filters: `session_id`, `signer`, `min_blocked`, `has_approvals`, `limit`, and `offset`.
