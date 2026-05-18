# Persistent API Operations

Phase 6 now includes operational controls for CAVRA's JSON and SQLite persistent API stores.

## Covered Stores

The operational commands inspect the active API persistence mode for:

- Evidence metadata.
- Approval requests.
- Agent and MCP registry records.
- Activity sessions and decisions.
- Repository inventory and policy rollouts.
- Enterprise integration inventory.

The CLI resolves the same environment variables used by the API. If a SQLite environment variable is set, SQLite is treated as the active store. Otherwise the JSON store path or API default is used.

## Store Status

```bash
cavra ops stores
```

This reports store name, mode, configured path, configuration source, existence, and size.

## Backup

```bash
cavra ops backup --output .cavra/backups/20260518
```

The backup command writes:

- `manifest.json` with schema version, source paths, backup paths, sizes, and SHA-256 checksums.
- `stores/*.json` for active JSON stores that exist.
- `stores/*.db` for active SQLite stores that exist.

SQLite backups use the SQLite backup API so running deployments can produce a consistent copy.

## Restore

Restore into a test directory first:

```bash
cavra ops restore .cavra/backups/20260518/manifest.json --target-dir /tmp/cavra-restore-test
```

Restore to configured live paths only after a successful restore test:

```bash
cavra ops restore .cavra/backups/20260518/manifest.json --overwrite
```

The restore command validates checksums before copying files. Existing files are not overwritten unless `--overwrite` is supplied.

## Retention Plan

```bash
cavra ops retention-plan \
  --output .cavra/operations/retention \
  --retention-days 2555 \
  --classification regulated-sdlc \
  --legal-hold
```

The command writes:

- `persistent-api-retention-plan.json`
- `persistent-api-retention-plan.md`

The plan records minimum retention, legal hold, delete protection, backup frequency, restore-test frequency, and the active persistence stores.

## API

Read-only operations endpoints:

- `GET /operations/stores`
- `GET /operations/retention-plan`

Backup and restore are CLI-only so self-hosted operators keep file-system authority outside the unauthenticated demo API.

## User Stories

- As a platform engineer, I can back up every CAVRA API store before migrations and releases.
- As an auditor, I can review retention and restore-test requirements for operational metadata.
- As an SRE, I can restore CAVRA stores into a test directory before touching live data.

## Enterprise Challenge Solved

Persistent governance data becomes useful only when it survives migrations, outages, operator mistakes, and audit lookbacks. These controls make CAVRA's operational data lifecycle explicit without giving the API dangerous file-write restore powers.
