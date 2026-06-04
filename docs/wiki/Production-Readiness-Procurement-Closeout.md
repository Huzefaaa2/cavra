# Production Readiness Procurement Closeout

This release gate closes the current public Community production-readiness
batch by tying operational readiness, procurement evidence, security response,
and release integrity into one validator. It is public-safe: it does not
include Enterprise source code, customer records, live provider credentials,
private signing keys, license-service internals, or SaaS backend code.

## Validation Command

Run the validator from the repository root:

```bash
python scripts/validate-production-readiness-procurement-closeout.py
```

Expected success output:

```text
CAVRA production readiness procurement closeout validation passed.
```

## Closeout Matrix

| Area | Public Control | Evidence Artifact |
| --- | --- | --- |
| Performance | Go runtime performance smoke is documented through `BenchmarkEvaluateAllowCommand`. | `docs/go-enforcement-production-hardening.md` and `go/cavra-runtime/runtime/decision_test.go`. |
| Concurrency | Recurrence automation and worker deployment examples use explicit concurrency controls, and Go daemon lifecycle validation remains bounded to local enforcement paths. | `examples/kubernetes/cavra-recurrence-automation-cronjob.yaml`, `.github/workflows/cavra-governance.yml`, and Go runtime tests. |
| Backup and restore | Persistent API operations document active store inspection, checksum-backed backup, test restore, live restore with overwrite controls, and retention plans. | `docs/persistent-api-operations.md` and `cavra ops backup` / `cavra ops restore`. |
| Upgrade and migration | SQLite migrations are idempotent, release-candidate upgrades are validated, and release packets preserve upgrade evidence. | `docs/evidence-metadata-migrations.md`, `docs/go-release-packaging.md`, and `cavra release validate-upgrade`. |
| SOC 2 readiness | Procurement readiness maps public evidence to Security, Availability, Processing Integrity, Confidentiality, and Privacy readiness themes. | `docs/procurement-readiness.md`. |
| Security advisory drill | Vulnerability disclosure and release advisory docs define reporter intake, maintainer workflow, affected components, mitigation, fixed release evidence, and verification commands. | `SECURITY.md`, `docs/vulnerability-disclosure.md`, `docs/release-security-advisories.md`, and `.github/workflows/release-security.yml`. |
| Final release integrity | Release verification is tied to checksums, SBOM, SLSA provenance, detached signatures, signing operations metadata, GitHub keyless attestations, air-gapped verification, and release evidence. | `docs/release-signing-operations.md`, `docs/go-release-packaging.md`, `scripts/package_go_release.py`, and `scripts/verify-community-release-artifacts.py`. |
| Public boundary | Boundary validation blocks risky private/commercial terms in public code paths. | `scripts/validate-boundaries.sh`. |

## Operator Runbook

1. Run the complete validator chain:

   ```bash
   python scripts/validate-release-packets.py
   python scripts/validate-maintenance-release-evidence.py
   python scripts/validate-community-release-note-freshness.py
   python scripts/validate-community-release-index.py
   python scripts/validate-community-release-readiness-dashboard.py
   python scripts/validate-sandbox-portal.py
   python scripts/validate-console-closeout.py
   python scripts/validate-community-ga-path.py
   python scripts/validate-production-deployment-guide.py
   python scripts/validate-go-production-hardening.py
   python scripts/validate-enterprise-integration-readiness.py
   python scripts/validate-production-readiness-procurement-closeout.py
   bash scripts/validate-boundaries.sh .
   ```

2. Run the implementation test gates:

   ```bash
   python -m ruff check src tests scripts
   python -m pytest -q
   cd go/cavra-runtime && go test ./...
   cd go/cavra-runtime && go test -bench BenchmarkEvaluateAllowCommand ./runtime
   ```

3. Exercise operational continuity in a non-production workspace:

   ```bash
   cavra ops stores
   cavra ops backup --output .cavra/backups/procurement-closeout
   cavra ops restore .cavra/backups/procurement-closeout/manifest.json \
     --target-dir /tmp/cavra-procurement-restore-test
   cavra evidence migrate --sqlite .cavra/evidence/metadata.db
   ```

4. Exercise final release integrity verification:

   ```bash
   cavra release verify-go-package go/cavra-runtime/dist/go-runtime-<version>
   cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-<version>.zip
   cavra release validate-upgrade \
     go/cavra-runtime/dist/go-runtime-<previous-version> \
     go/cavra-runtime/dist/go-runtime-<candidate-version>
   ```

5. Run a security advisory drill using synthetic data:
   - open an internal advisory draft;
   - map affected components and fixed release artifacts;
   - document mitigation before upgrade;
   - attach verification commands;
   - confirm no exploit details, customer data, or private findings are
     committed to the public repository.

6. Assemble a procurement packet from public links:
   - README and release notes;
   - release packets and verification packets;
   - security policy and advisory docs;
   - procurement readiness map;
   - production deployment guide validation;
   - Enterprise integration validation;
   - release integrity documentation.

## Public Boundary

This closeout is a public Community readiness gate. It must not contain private
Enterprise source, paid policy pack implementation, production SaaS code,
customer questionnaires, customer contracts, live support records, private SOC
2 workpapers, provider credentials, customer records, signing keys, license
keys, or private vulnerability details.

## User Stories

- As a procurement reviewer, I can see one evidence map for release integrity,
  vulnerability response, operational continuity, and SOC 2 readiness.
- As a platform owner, I can verify backup, restore, migration, and upgrade
  procedures before a pilot.
- As a security engineer, I can run a security advisory drill without exposing
  private exploit details or customer data.
- As a release manager, I can prove that Community artifacts and Go runtime
  packages have verification paths before publication.
- As an auditor, I can trace each public readiness claim to a command, page,
  workflow, or release packet.

## Enterprise Challenge Solved

Enterprise adoption often stalls between technical evaluation and procurement.
This gate gives CAVRA a public, repeatable closeout path that connects release
verification, operational continuity, vulnerability response, SOC 2 readiness,
and source-boundary evidence without exposing the private Enterprise product.

## Next Recommendation

Prepare Community v0.1.3 maintenance planning and GitHub Actions Node 24 readiness.
