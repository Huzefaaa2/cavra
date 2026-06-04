# Production Deployment Guide Validation

This guide turns CAVRA Community production deployment documentation into a
repeatable public release gate. It checks that install, configuration, storage,
backup, restore, CORS/API, GitHub Pages portal, and release evidence guidance
remain connected for operators before a Community release or pilot-facing
documentation update is shipped.

## Validation Command

Run the validator from the repository root:

```bash
python scripts/validate-production-deployment-guide.py
```

Expected success output:

```text
CAVRA production deployment guide validation passed.
```

## Deployment Coverage Matrix

| Area | Required Public Guidance | Validation Signal |
| --- | --- | --- |
| Install | Install the Community package and run `cavra`; run the API with `uvicorn cavra.api:app --host 0.0.0.0 --port 8000`; run the portal with `python -m http.server 5173 --directory apps/sandbox-ui`. | `docs/deployment.md`, README quickstart links, and Community CI prove the public source path remains buildable. |
| Configuration | Configure runtime paths through environment variables instead of source edits. Key settings include `CAVRA_ACTIVITY_STORE`, `CAVRA_ACTIVITY_DB`, `CAVRA_INVENTORY_STORE`, `CAVRA_INVENTORY_DB`, `CAVRA_INTEGRATION_STORE`, `CAVRA_INTEGRATION_DB`, `CAVRA_EVIDENCE_ARTIFACT_ROOT`, `CAVRA_PUBLIC_API_BASE_URL`, and `CAVRA_CORS_ORIGINS`. | The guide requires configuration text in `docs/deployment.md`, `docs/production-deployment-validation.md`, `docs/persistent-api-operations.md`, and `docs/sandbox.md`. |
| Storage | Persistent stores must be explicit. JSON and SQLite stores are supported for activity, inventory, rollout, integration, and pilot-intake records; managed database drivers remain a later production/private deployment concern. | `cavra ops stores` and `/operations/stores` show active public store paths without exposing customer data. |
| Backup | Operators must export checksum-backed backups before upgrades, pilot resets, or release verification. | `cavra ops backup --output .cavra/backups/production-check` creates backup manifests for the public store set. |
| Restore | Restore must be tested to a separate target directory before any live overwrite. | `cavra ops restore .cavra/backups/production-check/manifest.json --target-dir /tmp/cavra-restore-test` validates checksums and proves restore readiness. |
| CORS/API | API deployments must restrict browser origins and expose console configuration intentionally. | Set `CAVRA_CORS_ORIGINS=https://huzefaaa2.github.io` or the deployed console origin, and confirm `curl http://127.0.0.1:8000/deployment/production-readiness` reports restricted CORS and production readiness checks. |
| GitHub Pages portal | The static portal must be independently smoke-tested before and after Pages deployment. | `python scripts/validate-sandbox-portal.py`, `python scripts/validate-console-closeout.py`, and the `deploy-sandbox` workflow validate routes, JavaScript, brand assets, evidence JSON, C4 diagrams, and smoke strings. |
| Evidence artifact root | Evidence retrieval must point to an allowlisted artifact root, not arbitrary filesystem paths. | Configure `CAVRA_EVIDENCE_ARTIFACT_ROOT` and verify release evidence through `python scripts/validate-community-ga-path.py`. |

## Operator Runbook

1. Install Community dependencies and run the local test suite:

   ```bash
   python -m pip install -e ".[dev]"
   python -m pytest -q
   ```

2. Start the API and confirm readiness:

   ```bash
   uvicorn cavra.api:app --host 0.0.0.0 --port 8000
   curl http://127.0.0.1:8000/deployment/production-readiness
   ```

3. Inspect configured stores:

   ```bash
   cavra ops stores
   ```

4. Create and test a backup/restore cycle:

   ```bash
   cavra ops backup --output .cavra/backups/production-check
   cavra ops restore .cavra/backups/production-check/manifest.json --target-dir /tmp/cavra-restore-test
   ```

5. Configure the portal/API boundary:

   ```bash
   export CAVRA_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
   export CAVRA_CORS_ORIGINS=http://127.0.0.1:5173
   python -m http.server 5173 --directory apps/sandbox-ui
   ```

6. Run the public deployment and release validators:

   ```bash
   python scripts/validate-production-deployment-guide.py
   python scripts/validate-sandbox-portal.py
   python scripts/validate-console-closeout.py
   python scripts/validate-community-ga-path.py
   bash scripts/validate-boundaries.sh .
   ```

7. Confirm GitHub Pages deployment status after merge through
   `.github/workflows/deploy-sandbox.yml`.

## Public Boundary

This guide covers public Community Edition deployment validation only. It does
not include Enterprise source code, private policy packs, SaaS backend
implementation, license-service secrets, license-signing keys, customer data,
customer templates, provider credentials, private connector configuration, or
commercial policy-pack implementation.

## User Stories

- As a platform engineer, I can prove that install, configuration, storage,
  backup, restore, CORS/API, and portal checks are documented before a pilot
  handoff.
- As an auditor, I can trace production-readiness evidence from commands to
  release validators and public docs.
- As a CISO, I can confirm that public deployment documentation does not expose
  Enterprise implementation details or customer secrets.
- As a maintainer, I can catch stale deployment guidance through CI before a
  release note or roadmap page is published.

## Enterprise Challenge Solved

Enterprise buyers need a clear path from public Community adoption to controlled
pilot validation. This guide makes the operational handoff inspectable without
publishing private deployment logic, customer data, license-service internals,
or commercial policy-pack source.

## Next Recommendation

Convert Community v0.1.2 dry-run into an official maintenance release after maintainer approval and artifact publication.
