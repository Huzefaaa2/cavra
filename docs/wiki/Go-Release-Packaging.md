# Go Release Packaging

CAVRA includes a GitHub Actions workflow for packaging the Go enforcement-plane runtime with checksums, SPDX-style SBOM metadata, signed installer metadata, reproducibility manifests, managed endpoint deployment manifests, release channel manifests, managed workstation updater policy, signed release-channel promotion approvals, Jamf/Intune/Linux endpoint-management export bundles, endpoint export publication delivery, endpoint inventory ingestion, installer smoke validation, SLSA provenance, detached Ed25519 signatures, GitHub keyless OIDC attestations, offline trust bootstrap metadata, air-gapped zip verification, release-candidate upgrade validation, and release evidence.

## Workflow

Workflow file: `.github/workflows/go-release.yml`

The workflow:

- Runs on manual dispatch for dry-run packaging and on published GitHub releases.
- Builds `cavra-runtime` for Linux, macOS, and Windows on `amd64` and `arm64`.
- Uses `CGO_ENABLED=0`, `GOFLAGS="-trimpath -mod=readonly -buildvcs=false"`, and `go build -ldflags="-s -w -buildid="` for reproducible, stripped binaries.
- Exports Go module metadata with `go list -m -json all`.
- Generates `cavra-runtime.sbom.spdx.json`.
- Generates `cavra-runtime.installers.json` with per-platform install metadata, binary checksums, install paths, and verification commands.
- Generates `cavra-runtime.reproducibility.json` with build flags, target matrix, rebuild commands, and per-binary digests for air-gapped rebuild checks.
- Generates `cavra-runtime.endpoint-deployment.json` with approved CI runner and developer workstation deployment targets.
- Generates `cavra-runtime.ci-runner-bundles.json` with GitHub Actions, GitLab CI, and Azure Pipelines runner metadata for the signed Linux runtime binary.
- Packages `ci-runners/cavra-release-governance-runner.sh` and `ci-runners/github-action/action.yml` into the signed release package.
- Generates `cavra-runtime.channels.json` with canary, beta, and stable release channels mapped to workstation targets.
- Generates `cavra-runtime.updater-policy.json` with manual approval, staged rollout, hold condition, and rollback requirements.
- Generates `cavra-runtime.provenance.intoto.json` using an in-toto Statement and SLSA provenance predicate.
- Generates `offline-trust-root-bootstrap.json` with offline operator notes and verification commands.
- Generates `checksums.txt`.
- Generates `release-evidence.json` and `release-evidence.md`.
- Signs release artifacts with detached Ed25519 signature JSON files when `CAVRA_GO_RELEASE_SIGNING_KEY` is configured.
- Requires signing material for real release events or non-dry-run manual dispatches.
- Creates a distributable zip named `cavra-go-runtime-<version>.zip`.
- Generates a GitHub keyless attestation for `cavra-go-runtime-<version>.zip` using the workflow's OIDC identity through `actions/attest@v4`.
- Records `github-keyless-attestation.json` with the attestation ID, URL, issuer, and verification command.
- Attaches the signed zip and keyless attestation metadata directly to the GitHub Release on published release events.
- Uploads the full package directory as the CI artifact `cavra-go-runtime-release-package`.

## How To Use

Dry run:

```bash
gh workflow run go-release.yml --repo Huzefaaa2/cavra \
  -f version=dry-run \
  -f dry_run=true
```

Production release:

1. Configure repository secret `CAVRA_GO_RELEASE_SIGNING_KEY` with an Ed25519 private key PEM.
2. Publish a GitHub release.
3. Download `cavra-go-runtime-<version>.zip` from the GitHub Release assets or the `cavra-go-runtime-release-package` workflow artifact.
4. Verify the package with the CAVRA CLI.

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-v0.1.0
```

Verify the air-gapped zip before transferring it into a restricted environment:

```bash
cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-v0.1.0.zip
```

Verify the GitHub keyless attestation for the release zip:

```bash
gh attestation verify go/cavra-runtime/dist/cavra-go-runtime-v0.1.0.zip \
  --repo Huzefaaa2/cavra
```

Validate a release-candidate upgrade before promotion:

```bash
cavra release validate-upgrade \
  go/cavra-runtime/dist/go-runtime-v0.1.0 \
  go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1
```

The upgrade validator verifies both packages, rejects rollback versions, detects removed release controls, and flags missing Go runtime binary targets across Linux, macOS, and Windows packages.

Inspect signed installer metadata before deploying to developer workstations, CI runners, or restricted networks:

```bash
jq '.targets[] | {target, binary, install_path, binary_sha256}' \
  go/cavra-runtime/dist/go-runtime-v0.1.0/cavra-runtime.installers.json
```

`cavra release verify-go-package` requires `cavra-runtime.installers.json`, checks every referenced binary digest, confirms checksum guidance, and verifies the metadata through checksums, SLSA provenance, and detached signatures.

Inspect reproducibility metadata before rebuilding a package in a controlled or restricted environment:

```bash
jq '.binaries[] | {target, binary, binary_sha256, rebuild_command}' \
  go/cavra-runtime/dist/go-runtime-v0.1.0/cavra-runtime.reproducibility.json
```

`cavra release verify-go-package` requires `cavra-runtime.reproducibility.json`. The verifier checks that the manifest declares `CGO_ENABLED=0`, `-trimpath`, read-only module resolution, disabled VCS stamping, an empty Go build ID, a declared target matrix, per-binary digests, and operator rebuild guidance. Air-gapped operators should rebuild from the recorded commit and compare rebuilt SHA-256 values to this manifest before placing binaries on runner images or developer workstations.

Inspect managed endpoint deployment guidance before publishing binaries into runner images, Jamf, Intune, Linux endpoint management, or restricted workstation channels:

```bash
jq '.deployment_targets[] | {id, surface, platform, installer_target, deployment_channel}' \
  go/cavra-runtime/dist/go-runtime-v0.1.0/cavra-runtime.endpoint-deployment.json
```

`cavra release verify-go-package` also requires `cavra-runtime.endpoint-deployment.json`. The verifier checks that each deployment target maps back to signed installer metadata, references an existing binary digest, and includes package verification plus installer smoke-test commands before rollout.

Inspect CI runner bundle metadata before copying the signed runtime into GitHub Actions, GitLab CI, or Azure Pipelines runner images:

```bash
jq '.runner_bundles[] | {platform, deployment_target, runtime_binary, reusable_wrapper}' \
  go/cavra-runtime/dist/go-runtime-v0.1.0/cavra-runtime.ci-runner-bundles.json
```

`cavra-runtime.ci-runner-bundles.json` binds the Linux `amd64` runtime binary to reusable runner wrappers for typed release-governance daemon checks. The release verifier requires this manifest, validates the packaged shell wrapper and GitHub composite action digests, confirms every runner bundle maps to a CI deployment target in `cavra-runtime.endpoint-deployment.json`, and checks that operator guidance includes package verification, checksum verification, GitHub keyless attestation verification, signed runner authentication claims, CI-provider OIDC runner JWT verification, signed daemon evidence stream controls, verifier CLI controls, and daemon evidence outputs.

The packaged shell runner can be used by GitLab CI, Azure Pipelines, or a custom runner image after the package is verified and the binary is installed:

```bash
export CAVRA_RUNTIME_PATH=./cavra-runtime
export CAVRA_RELEASE_GOVERNANCE_REQUEST=examples/go-runtime/typed-release-governance/approved-promotion.json
export CAVRA_EXPECTED_DECISION=allow
export CAVRA_EXPECTED_RULE_ID=release_governance.approval.approved
export CAVRA_RUNNER_AUTH_HMAC_KEY="$CI_CAVRA_RUNNER_AUTH_HMAC_KEY"
export CAVRA_RUNNER_AUTH_KEY_ID=ci-runner-2026-q2
export CAVRA_DAEMON_EVIDENCE_HMAC_KEY="$CI_CAVRA_DAEMON_EVIDENCE_HMAC_KEY"
export CAVRA_DAEMON_EVIDENCE_KEY_ID=ci-evidence-2026-q2
bash ci-runners/cavra-release-governance-runner.sh
```

To require CI-provider OIDC JWT verification instead of shared-secret runner signatures, configure the daemon-side issuer, audience, and JWKS source. The runner wrapper can auto-acquire provider JWTs with `CAVRA_RUNNER_OIDC_AUTO=true`, or it can use a token supplied through `CAVRA_RUNNER_AUTH_OIDC_TOKEN` or `CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE`:

```bash
export CAVRA_RUNNER_PROVIDER=github-actions
export CAVRA_RUNNER_OIDC_ISSUER=https://token.actions.githubusercontent.com
export CAVRA_RUNNER_OIDC_AUDIENCE=cavra-release-governance
export CAVRA_RUNNER_OIDC_JWKS_URL=https://token.actions.githubusercontent.com/.well-known/jwks
export CAVRA_RUNNER_OIDC_AUTO=true
bash ci-runners/cavra-release-governance-runner.sh
```

For GitLab CI, configure `id_tokens` and use `CAVRA_GITLAB_OIDC_TOKEN` or set `CAVRA_RUNNER_AUTH_OIDC_TOKEN_ENV` to the variable that contains the JWT. For Azure Pipelines, expose `SYSTEM_OIDCREQUESTURI` with `SYSTEM_ACCESSTOKEN` or set `CAVRA_AZURE_OIDC_TOKEN` after an approved token acquisition step. The runtime sends `runner_auth.algorithm=OIDC-JWT`, verifies RS256 signatures with JWKS, checks issuer, audience, expiry, not-before, provider, repository, and matching runner identity claims, and redacts the bearer JWT from daemon evidence records.

GitHub Actions can use the packaged composite action from `ci-runners/github-action/action.yml` after the signed package is unpacked into the workspace:

```yaml
- uses: ./ci-runners/github-action
  with:
    runtime-path: ./cavra-runtime
    request-path: examples/go-runtime/typed-release-governance/approved-promotion.json
    expected-decision: allow
    expected-rule-id: release_governance.approval.approved
    runner-auth-key-id: ci-runner-2026-q2
    evidence-signing-key-id: ci-evidence-2026-q2
    runner-oidc-issuer: https://token.actions.githubusercontent.com
    runner-oidc-audience: cavra-release-governance
    runner-oidc-jwks-url: https://token.actions.githubusercontent.com/.well-known/jwks
    runner-oidc-auto: "true"
```

For GitHub Actions, grant `id-token: write`, pass `CAVRA_RUNNER_AUTH_HMAC_KEY` and `CAVRA_DAEMON_EVIDENCE_HMAC_KEY` through repository or organization secrets when using HMAC mode, or use OIDC auto-acquisition plus issuer, audience, and JWKS settings when using OIDC mode. The action records CI identity claims in `runner-auth-claims.json`, writes `release-governance-evidence-verification.json` when evidence signing is enabled, and signs the daemon evidence stream without writing HMAC keys to disk. Custody and rotation guidance lives in `docs/runner-auth-evidence-key-custody.md`.

Inspect channel manifests and managed workstation updater policy before publishing package metadata to endpoint-management tooling:

```bash
cavra release channel-manifest \
  go/cavra-runtime/dist/go-runtime-v0.1.0 \
  --channel stable

cavra release updater-policy \
  go/cavra-runtime/dist/go-runtime-v0.1.0

jq '.channels[] | {channel, version, auto_update, approval_required}' \
  go/cavra-runtime/dist/go-runtime-v0.1.0/cavra-runtime.channels.json
```

`cavra release verify-go-package` requires `cavra-runtime.channels.json` and `cavra-runtime.updater-policy.json`. The verifier checks that each channel disables automatic updates, requires approval, maps to signed workstation binaries, includes package and smoke validation commands, and references a policy that defines staged rollout rings, hold conditions, and rollback requirements.

Create a signed release-channel promotion request before endpoint teams publish a channel to managed developer workstations:

```bash
cavra release request-channel-promotion \
  go/cavra-runtime/dist/go-runtime-v0.1.0 \
  --channel stable \
  --target-ring enterprise \
  --approval-store .cavra/api/approvals.json \
  --metadata-json .cavra/evidence/metadata.json
```

The request verifies the signed package, binds the selected release channel to `cavra-runtime.channels.json` and `cavra-runtime.updater-policy.json`, signs the request payload, creates a pending approval for endpoint change control, and can index `metadata_kind=release-channel-promotion-request` into the JSON or SQLite evidence metadata store.

Export endpoint-management bundles for Jamf, Intune, and Linux fleet tooling:

```bash
cavra release export-endpoint-management \
  go/cavra-runtime/dist/go-runtime-v0.1.0 \
  --channel stable \
  --provider all \
  --promotion-request .cavra/release/channel-promotion/release-channel-promotion-request.json \
  --metadata-json .cavra/evidence/metadata.json
```

The export writes `jamf-policy.json`, `intune-win32-app.json`, `linux-fleet-manifest.json`, `linux-install-cavra-runtime.sh`, `endpoint-management-export-manifest.json`, and `checksums.txt` when matching workstation targets exist in the channel manifest. The bundle keeps promotion approval IDs, package verification results, endpoint target digests, rollback requirements, and staged rollout policy together for endpoint engineering review. When `--metadata-json` or `--sqlite` is supplied, CAVRA also indexes `metadata_kind=endpoint-management-export` so release managers can audit which endpoint tooling received which release channel export.

Capture rollout evidence when a package is approved for a managed endpoint channel:

```bash
cavra release capture-rollout \
  go/cavra-runtime/dist/go-runtime-v0.1.0 \
  --deployment-id github-actions-linux-amd64-runner \
  --rollout-ring pilot \
  --status staged \
  --change-record CHG-123
```

The command verifies the package first, selects one or more deployment targets from `cavra-runtime.endpoint-deployment.json`, and writes `managed-endpoint-rollout-evidence.json`, `managed-endpoint-rollout-evidence.md`, and `checksums.txt` for the rollout change record.

Verify rollout evidence and index it into the same evidence metadata stores used by the CAVRA API and console:

```bash
cavra release verify-rollout \
  .cavra/release/rollout \
  --metadata-json .cavra/evidence/metadata.json \
  --sqlite .cavra/evidence/metadata.db
```

The verifier checks rollout artifact checksums, source package artifact checksums, release package verification results, deployment targets, rollout status, and required rollout controls before indexing rollout metadata by `rollout_id`.

Search rollout evidence from the CLI, API, or hosted console:

```bash
cavra evidence search \
  --sqlite .cavra/evidence/metadata.db \
  --metadata-kind managed-endpoint-rollout \
  --rollout-status staged \
  --environment production \
  --deployment-target github-actions-linux-amd64-runner
```

The `/evidence` API and console Evidence Search view support the same rollout metadata filters for `metadata_kind`, `rollout_status`, `environment`, and `deployment_target`.

Download governed rollout evidence artifacts from the same evidence API after configuring `CAVRA_EVIDENCE_ARTIFACT_ROOT` to contain the indexed rollout directory:

```bash
curl http://127.0.0.1:8000/evidence/chg-123-v0.1.0/artifacts
curl -OJ http://127.0.0.1:8000/evidence/chg-123-v0.1.0/artifacts/managed-endpoint-rollout-evidence.json
curl -OJ http://127.0.0.1:8000/evidence/chg-123-v0.1.0/artifact-bundle
```

Rollout artifact retrieval only serves `managed-endpoint-rollout-evidence.json`, `managed-endpoint-rollout-evidence.md`, and `checksums.txt`, and the rollout `bundle_dir` must resolve inside the configured artifact root.

The artifact listing reports rollout checksum integrity and promotion readiness so release owners can see whether evidence is verified, incomplete, blocked, or ready before moving to the next deployment ring.

Create a signed approval request before promoting a verified rollout into the next ring:

```bash
cavra release request-rollout-promotion \
  .cavra/release/rollout \
  --target-ring production \
  --approval-store .cavra/api/approvals.json
```

The command re-verifies rollout evidence, requires staged or succeeded rollout status, signs the promotion request with `CAVRA_ROLLOUT_PROMOTION_SIGNING_KEY` or `CAVRA_GO_RELEASE_SIGNING_KEY`, writes JSON and Markdown request artifacts, and can persist the pending approval into JSON or SQLite approval stores. The API exposes the same workflow through `POST /evidence/{session_id}/promotion-request`, and the console can request promotion approval from the rollout artifact panel.

After the approval is approved, record the rollout ring advancement:

```bash
cavra release execute-rollout-promotion \
  .cavra/release/rollout-promotion/rollout-promotion-approval-request.json \
  --approval-store .cavra/api/approvals.json \
  --metadata-json .cavra/evidence/metadata.json
```

The execution command verifies the signed promotion request, requires the approval record to be `approved`, checks that the approval decision is bound to the rollout and target ring, writes JSON plus Markdown execution records, and can index the execution into JSON or SQLite evidence metadata stores.

Search and inspect promotion executions:

```bash
cavra evidence search \
  --sqlite .cavra/evidence/metadata.db \
  --metadata-kind rollout-promotion-execution \
  --rollout-status promoted \
  --target-ring production \
  --approval-state approved \
  --promotion-execution-status executed \
  --deployment-target github-actions-linux-amd64-runner
```

The API exposes execution recording through `POST /evidence/{session_id}/promotion-execution`, search through `/promotion-executions`, and audit drill-down through `/promotion-executions/{execution_id}`. The console can record the promotion execution from the rollout artifact panel and inspect execution audit links plus rollback evidence references from evidence search.

Export promotion execution audit payloads for SOC and change-management systems:

```bash
cavra release export-promotion-audit \
  .cavra/release/rollout-promotion-execution/rollout-promotion-execution.json \
  --output .cavra/release/promotion-audit-export \
  --provider all
```

The export command writes a normalized CAVRA promotion audit event plus Splunk HEC, Microsoft Sentinel, Datadog, webhook, Jira, and ServiceNow-shaped payloads. The API exposes the normalized audit event from `/promotion-executions/{execution_id}/audit-export` so hosted consoles and connector services can route the same promotion execution evidence without re-parsing release artifacts.

When a promoted ring must be rolled back, record a separate approved rollback execution:

```bash
cavra release execute-rollout-rollback \
  .cavra/release/rollout-promotion-execution/rollout-promotion-execution.json \
  --approval-store .cavra/api/approvals.json \
  --approval-id apr_rollback_prod \
  --rollback-reason "Production validation failed" \
  --metadata-json .cavra/evidence/metadata.json
```

Rollback execution requires an approved rollback approval whose decision authorizes `release_rollback_endpoint_rollout`, binds to the promotion execution ID, and preserves rollback evidence references from the governed rollout target. The API exposes the same workflow through `POST /promotion-executions/{execution_id}/rollback-execution` and returns rollback audit metadata retrievable from `/rollback-executions/{rollback_id}`.

Deliver promotion audit and rollback execution records through configured connectors:

```bash
cavra release deliver-promotion-audit \
  .cavra/release/rollout-promotion-execution/rollout-promotion-execution.json \
  --config .cavra/connectors.json \
  --provider webhook \
  --retries 1 \
  --metadata-json .cavra/evidence/metadata.json

cavra release deliver-rollback-execution \
  .cavra/release/rollout-rollback-execution/rollout-rollback-execution.json \
  --config .cavra/connectors.json \
  --provider webhook \
  --retries 1 \
  --metadata-json .cavra/evidence/metadata.json
```

Connector delivery reuses the enterprise connector layer for Splunk, Sentinel, Datadog, webhook, Slack, Teams, Jira, and ServiceNow. The CLI writes `cavra.connector.delivery.v1` evidence with event ID, provider, success state, status code, attempt count, redacted URL and headers, and delivery errors. When `--metadata-json` or `--sqlite` is supplied, the delivery is also indexed as `metadata_kind=release-connector-delivery`.

Review persisted delivery history and dashboard alerts:

```bash
cavra release connector-delivery-history \
  --metadata-json .cavra/evidence/metadata.json \
  --provider webhook \
  --no-success

cavra release connector-delivery-dashboard \
  --metadata-json .cavra/evidence/metadata.json
```

The API exposes the same delivery path through `POST /promotion-executions/{execution_id}/audit-export/deliver` and `POST /rollback-executions/{rollback_id}/deliver`. API deliveries are persisted into the active evidence metadata store. `/release-connector-deliveries` returns delivery history filters by provider, event type, source event ID, and success state. `/release-connector-deliveries/dashboard` summarizes total delivery batches, failed providers, success rate, and critical rollback-delivery alerts. The Evidence Console includes a Release Connector Delivery panel for release managers, SOC analysts, and auditors.

## Release Channel And Endpoint Export History

The same evidence metadata store now acts as the operational history for channel publishing. `/release-channel-promotions` returns indexed channel promotion requests filtered by channel, target ring, approval state, and approval ID. `/release-channel-promotions/{request_id}` returns the signed request metadata, approval link, target ring, deployment targets, and audit links for review.

Endpoint-management exports are available from `/endpoint-management-exports` with channel, provider, approval ID, and promotion request filters. `/endpoint-management-exports/{export_id}` returns the export manifest metadata, provider list, file list, release identity, and approval binding. `/endpoint-management-exports/dashboard` summarizes export counts, pending approvals, provider coverage, channel coverage, and latest indexed export records.

The Evidence Console includes a Release Channel Publishing panel that combines promotion request rows, endpoint export rows, provider metrics, and pending approval indicators. This gives release managers, endpoint engineering owners, and auditors a single view of whether a runtime channel was approved before Jamf, Intune, or Linux fleet artifacts were generated.

## Governed Endpoint Export Downloads

Endpoint-management export artifacts use the same configured artifact root as evidence bundles. Set `CAVRA_EVIDENCE_ARTIFACT_ROOT`, index the export metadata with `bundle_dir`, and retrieve allowlisted files:

```bash
curl http://127.0.0.1:8000/endpoint-management-exports/eme_stable/artifacts
curl -OJ http://127.0.0.1:8000/endpoint-management-exports/eme_stable/artifacts/jamf-policy.json
curl -OJ http://127.0.0.1:8000/endpoint-management-exports/eme_stable/artifact-bundle
```

The API serves only files listed in the endpoint export metadata and known to CAVRA: export manifest JSON, export summary Markdown, Jamf policy JSON, Intune app JSON, Linux fleet manifest JSON, Linux install script, and `checksums.txt`. Provider files must match `checksums.txt` before download. Responses include `x-cavra-artifact-sha256`, and the artifact listing exposes `endpoint_management_export_integrity` plus `download_readiness` so release managers can see whether downloads are blocked or ready.

## Endpoint Export Publication Delivery

Endpoint-management exports can be published through the same connector runtime used by release governance events. Configure `jamf`, `intune`, or `linux` connectors in `.cavra/connectors.json`, then deliver a checksum-verified endpoint export manifest:

```bash
cavra release deliver-endpoint-export \
  .cavra/release/endpoint-management-export/endpoint-management-export-manifest.json \
  --config .cavra/connectors.json \
  --provider jamf \
  --metadata-json .cavra/evidence/metadata.json
```

The command builds a `cavra.endpoint-management-publication.v1` event, selects provider-specific payloads from `jamf-policy.json`, `intune-win32-app.json`, or `linux-fleet-manifest.json`, verifies export checksums when the export directory is present, writes redacted connector delivery evidence, and indexes `metadata_kind=endpoint-management-publication-delivery`.

Publication history and health are available from both CLI and API:

```bash
cavra release endpoint-publication-history --metadata-json .cavra/evidence/metadata.json --provider jamf --no-success
cavra release endpoint-publication-dashboard --metadata-json .cavra/evidence/metadata.json
curl -X POST http://127.0.0.1:8000/endpoint-management-exports/eme_stable/publish \
  -H 'content-type: application/json' \
  -d '{"provider":"jamf","retries":1}'
curl http://127.0.0.1:8000/endpoint-management-publications
curl http://127.0.0.1:8000/endpoint-management-publications/dashboard
```

The Evidence Console includes an Endpoint Publication Delivery panel with publication counts, failed delivery alerts, provider rows, and attempt history. This lets endpoint engineering and release managers distinguish "export generated" from "export delivered to fleet tooling" during a controlled runtime rollout.

## Managed Endpoint Reconciliation

CAVRA can compare the desired runtime state from `cavra-runtime.endpoint-deployment.json` with an observed endpoint inventory captured from fleet tooling. The public repo defines the reconciliation model and evidence records; private Enterprise connectors can later automate collection from Jamf, Intune, Linux management, EDR, or SaaS inventory systems.

Observed inventory input is intentionally simple:

```json
{
  "schema_version": "cavra.endpoint-observations.v1",
  "observed_at": "2026-05-19T00:00:00+00:00",
  "channel": "stable",
  "endpoints": [
    {
      "endpoint_id": "workstation-1",
      "deployment_target": "linux-systemd-amd64-workstation",
      "installed_version": "v0.2.0-rc.1",
      "binary_sha256": "..."
    }
  ]
}
```

Run reconciliation and index drift evidence:

```bash
cavra release ingest-endpoint-inventory \
  .cavra/release/jamf-inventory.json \
  --provider jamf \
  --channel stable \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-inventory-history \
  --metadata-json .cavra/evidence/metadata.json \
  --provider jamf

cavra release endpoint-inventory-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-inventory-freshness \
  --metadata-json .cavra/evidence/metadata.json \
  --max-age-hours 24 \
  --critical-age-hours 48

cavra release endpoint-inventory-freshness-history \
  --metadata-json .cavra/evidence/metadata.json \
  --alert-level critical

cavra release endpoint-inventory-freshness-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release reconcile-endpoint-deployment \
  go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 \
  .cavra/release/endpoint-inventory/endpoint-inventory.json \
  --metadata-json .cavra/evidence/metadata.json

cavra release automate-endpoint-reconciliation \
  go/cavra-runtime/dist/go-runtime-v0.2.0-rc.1 \
  .cavra/release/endpoint-inventory/endpoint-inventory-ingestion.json \
  --approval-store .cavra/api/approvals.json \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-reconciliation-history \
  --metadata-json .cavra/evidence/metadata.json \
  --drift-status drift_detected

cavra release endpoint-reconciliation-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-reconciliation-automation-history \
  --metadata-json .cavra/evidence/metadata.json \
  --approval-state pending

cavra release endpoint-reconciliation-automation-dashboard \
  --metadata-json .cavra/evidence/metadata.json
```

Inventory ingestion records are indexed as `metadata_kind=endpoint-inventory-ingestion` and normalize Jamf, Intune, Linux fleet, or EDR exports into `cavra.endpoint-observations.v1` without storing private connector credentials. Freshness reports are indexed as `metadata_kind=endpoint-inventory-freshness-report` and flag provider, channel, and deployment-target inventory that is older than warning or critical SLA thresholds. Reconciliation automation indexes `metadata_kind=endpoint-reconciliation-automation` and can create a pending approval-bound remediation request whenever a new inventory ingestion shows drift. Reconciliation reports remain indexed as `metadata_kind=managed-endpoint-reconciliation` with desired target counts, observed endpoint counts, compliant endpoints, version drift, binary checksum drift, missing target observations, stale endpoint observations, and alert level. The API exposes the same workflow through `POST /endpoint-inventory/ingest`, `/endpoint-inventory-ingestions`, `/endpoint-inventory-ingestions/dashboard`, `POST /endpoint-inventory/freshness-report`, `/endpoint-inventory-freshness`, `/endpoint-inventory-freshness/dashboard`, `POST /endpoint-inventory-ingestions/{inventory_id}/reconcile`, `/endpoint-reconciliation-automations`, `/endpoint-reconciliation-automations/dashboard`, `POST /endpoint-deployment/reconcile`, `/endpoint-reconciliations`, and `/endpoint-reconciliations/dashboard`. The Evidence Console includes Endpoint Inventory Ingestion, Endpoint Inventory Freshness, Endpoint Drift Monitoring, and Endpoint Drift Remediation panels for provider coverage, freshness alerts, drift counts, pending approvals, and alert summaries.

Plan and record approved remediation:

```bash
cavra release request-endpoint-remediation \
  .cavra/release/endpoint-reconciliation/managed-endpoint-reconciliation.json \
  --strategy mixed \
  --approval-store .cavra/api/approvals.json \
  --metadata-json .cavra/evidence/metadata.json

cavra approval approve apr_123 \
  --store .cavra/api/approvals.json \
  --actor endpoint-cab \
  --reason "Reviewed republish and rollback plan"

cavra release execute-endpoint-remediation \
  .cavra/release/endpoint-remediation/endpoint-remediation-request.json \
  --approval-store .cavra/api/approvals.json \
  --metadata-json .cavra/evidence/metadata.json

cavra release export-endpoint-remediation-handoff \
  .cavra/release/endpoint-remediation/endpoint-remediation-request.json \
  --provider all \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-handoff-history \
  --metadata-json .cavra/evidence/metadata.json \
  --provider private_queue

cavra release endpoint-remediation-handoff-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release record-endpoint-remediation-handoff-status \
  .cavra/release/endpoint-remediation-handoff/endpoint-remediation-handoff.json \
  --provider private_queue \
  --status completed \
  --external-ref queue-job-123 \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-handoff-status-history \
  --metadata-json .cavra/evidence/metadata.json \
  --provider private_queue

cavra release endpoint-remediation-handoff-status-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-report \
  --metadata-json .cavra/evidence/metadata.json \
  --index-metadata-json .cavra/evidence/metadata.json \
  --warning-hours 24 \
  --critical-hours 48

cavra release deliver-endpoint-remediation-sla \
  .cavra/release/endpoint-remediation-sla/endpoint-remediation-sla-report.json \
  --config .cavra/connectors.json \
  --routing-policy .cavra/sla-notification-policy.json \
  --provider all \
  --metadata-json .cavra/evidence/metadata.json

cavra release ack-endpoint-remediation-sla ersla_123 \
  --provider slack \
  --acknowledged-by release-manager \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-notification-history \
  --metadata-json .cavra/evidence/metadata.json \
  --provider slack

cavra release endpoint-remediation-sla-notification-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-plan \
  --slo-policy .cavra/sla-escalation-policy.json \
  --metadata-json .cavra/evidence/metadata.json

cavra release deliver-endpoint-remediation-sla-escalation \
  .cavra/release/endpoint-remediation-sla-escalation-plan.json \
  --config .cavra/connectors.json \
  --provider all \
  --metadata-json .cavra/evidence/metadata.json

cavra release review-endpoint-remediation-sla-escalation erslaesc_123 \
  --report-id ersla_123 \
  --provider slack \
  --owner release-governance \
  --reviewed-by release-manager \
  --review-state escalated \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-action-history \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-action-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-recurrence-plan \
  --recurrence-policy .cavra/sla-escalation-recurrence-policy.json \
  --metadata-json .cavra/evidence/metadata.json

cavra release deliver-endpoint-remediation-sla-escalation-recurrence \
  .cavra/release/endpoint-remediation-sla-escalation-recurrence-plan.json \
  --config .cavra/connectors.json \
  --provider all \
  --metadata-json .cavra/evidence/metadata.json

cavra release export-endpoint-remediation-sla-escalation-suppression-audit \
  .cavra/release/endpoint-remediation-sla-escalation-recurrence-plan.json \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-recurrence-retry-plan \
  --metadata-json .cavra/evidence/metadata.json

cavra release deliver-endpoint-remediation-sla-escalation-owner-digest \
  .cavra/release/endpoint-remediation-sla-escalation-recurrence-plan.json \
  --retry-plan .cavra/release/endpoint-remediation-sla-escalation-recurrence-retry-plan.json \
  --config .cavra/connectors.json \
  --provider all \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-suppression-trends \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-recurrence-history \
  --metadata-json .cavra/evidence/metadata.json \
  --action suppress

cavra release endpoint-remediation-sla-escalation-recurrence-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-escalation-history \
  --metadata-json .cavra/evidence/metadata.json \
  --active-only

cavra release endpoint-remediation-sla-escalation-dashboard \
  --metadata-json .cavra/evidence/metadata.json

cavra release endpoint-remediation-sla-history \
  --metadata-json .cavra/evidence/metadata.json \
  --alert-level critical

cavra release endpoint-remediation-sla-dashboard \
  --metadata-json .cavra/evidence/metadata.json
```

Remediation requests are indexed as `metadata_kind=endpoint-drift-remediation-request`; execution records are indexed as `metadata_kind=endpoint-drift-remediation-execution`; handoff packages are indexed as `metadata_kind=endpoint-remediation-handoff`; callback and operator status records are indexed as `metadata_kind=endpoint-remediation-handoff-status`; SLA reports are indexed as `metadata_kind=endpoint-remediation-sla-report`; notification plans are indexed as `metadata_kind=endpoint-remediation-sla-notification-plan`; acknowledgements are indexed as `metadata_kind=endpoint-remediation-sla-notification-ack`; escalation plans are indexed as `metadata_kind=endpoint-remediation-sla-escalation-plan`; escalation owner reviews are indexed as `metadata_kind=endpoint-remediation-sla-escalation-review`; recurrence plans are indexed as `metadata_kind=endpoint-remediation-sla-escalation-recurrence-plan`; suppression audits are indexed as `metadata_kind=endpoint-remediation-sla-escalation-suppression-audit`; recurrence retry plans are indexed as `metadata_kind=endpoint-remediation-sla-escalation-recurrence-retry-plan`; owner digests are indexed as `metadata_kind=endpoint-remediation-sla-escalation-owner-digest`; suppression trends are indexed as `metadata_kind=endpoint-remediation-sla-escalation-suppression-trend`; scheduled recurrence automation runs are indexed as `metadata_kind=endpoint-remediation-sla-escalation-recurrence-automation-run`; notification delivery attempts are indexed as `metadata_kind=release-connector-delivery` with `connector_delivery_source=endpoint_remediation_sla_notification`; escalation delivery attempts use `connector_delivery_source=endpoint_remediation_sla_escalation_delivery`; recurrence delivery attempts use `connector_delivery_source=endpoint_remediation_sla_escalation_recurrence_delivery`; owner digest delivery attempts use `connector_delivery_source=endpoint_remediation_sla_escalation_owner_digest`; recurrence automation health alert plans are indexed as `metadata_kind=endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan`; health alert acknowledgements are indexed as `metadata_kind=endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack`; health alert delivery attempts use `connector_delivery_source=endpoint_remediation_sla_escalation_recurrence_automation_health_alert`. Community Edition records the governed plan, approval binding, handoff payloads, external status references, redacted provider callback evidence, SLA breach state, escalation payloads, executive release governance summaries, routing policy decisions, duplicate suppression windows, acknowledgement evidence, owner-specific acknowledgement and resolution SLO state, escalation ladder state, escalation delivery evidence, owner review records, recurrence intervals, maximum recurrence limits, owner calendar availability, maintenance-window suppression, recurrence delivery batches, suppression audit exports, recurrence retry policies, owner digest notifications, suppression trend analytics, dry-run-by-default recurrence automation worker runs, recurrence automation health reporting, recurrence automation health alert delivery plans, health alert acknowledgements, and redacted notification delivery evidence for Jira, ServiceNow, Slack, Teams, generic webhooks, and private connector queues. Actual endpoint mutation is intentionally left to private connector implementations or operator runbooks.

Routing policy files can be JSON or YAML:

```json
{
  "default_providers": ["slack"],
  "suppression_window_minutes": 120,
  "rules": [
    {
      "rule_id": "critical-release-governance",
      "alert_levels": ["critical"],
      "providers": ["jira", "servicenow", "slack", "teams"],
      "min_breached": 1,
      "owner": "release-cab",
      "acknowledgement_required": true
    }
  ]
}
```

Owner SLO and escalation policy files can also be JSON or YAML:

```json
{
  "default_slo": {
    "acknowledgement_minutes": 60,
    "resolution_minutes": 240
  },
  "owner_slos": {
    "release-cab": {
      "acknowledgement_minutes": 30,
      "resolution_minutes": 120
    }
  },
  "ladders": [
    {
      "level": "release-governance",
      "after_minutes": 60,
      "providers": ["jira", "slack"],
      "action": "Escalate unresolved endpoint remediation notification to release governance."
    }
  ]
}
```

Escalation recurrence policy files are JSON or YAML and remain public-safe metadata:

```json
{
  "recurrence_interval_minutes": 60,
  "max_recurrences_per_route": 3,
  "maintenance_windows": [
    {
      "window_id": "change-freeze",
      "owners": ["release-governance"],
      "providers": ["jira"],
      "start_at": "2026-05-20T00:00:00+00:00",
      "end_at": "2026-05-20T02:00:00+00:00",
      "reason": "release change freeze"
    }
  ],
  "owner_calendars": {
    "release-governance": {
      "business_hours": [
        {"days": ["mon", "tue", "wed", "thu", "fri"], "start": "09:00", "end": "17:00"}
      ],
      "unavailable_windows": []
    }
  }
}
```

Smoke-test installer metadata and execute the native packaged runtime when the current OS and architecture are present:

```bash
cavra release smoke-installers go/cavra-runtime/dist/go-runtime-v0.1.0
```

For cross-compiled packages on a nonmatching host, run static installer validation without execution:

```bash
cavra release smoke-installers go/cavra-runtime/dist/go-runtime-v0.1.0 --skip-execution
```

For unsigned dry-run artifacts only:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-dry-run --allow-unsigned
```

Generate an Ed25519 keypair with CAVRA:

```bash
cavra evidence generate-keypair \
  --private-key .cavra/keys/go-release-private.pem \
  --public-key .cavra/keys/go-release-public.pem
```

Do not commit private keys. Store production signing keys in GitHub Actions secrets or an enterprise secret manager.

## User Stories

- As a release manager, I can publish Go runtime binaries with checksums, SBOM, SLSA provenance, signatures, keyless attestations, and evidence.
- As a security engineer, I can verify that binaries map to a specific commit, ref, workflow identity, and dependency set.
- As an enterprise architect, I can verify an air-gapped runtime zip before restricted-network transfer.
- As a platform engineer, I can compare the current approved package with a release candidate before promoting it to developers or CI runners.
- As an endpoint engineering owner, I can approve signed installer metadata before placing CAVRA binaries on managed developer workstations.
- As an endpoint engineering owner, I can map signed runtime binaries to approved CI runner and workstation deployment channels before rollout.
- As a CI owner, I can reuse a packaged release-governance runner wrapper or GitHub composite action after verifying the signed Go runtime package.
- As a CI owner, I can require signed runner authentication claims and signed daemon evidence streams for release-governance checks.
- As an endpoint engineering owner, I can publish canary, beta, and stable channel manifests that require approval before workstation updates.
- As an endpoint engineering owner, I can enforce updater policy with staged rings, hold conditions, and rollback package requirements.
- As an endpoint engineering owner, I can create a signed release-channel promotion request before publishing managed workstation updates.
- As an endpoint engineering owner, I can export Jamf, Intune, and Linux fleet import bundles from the approved release channel metadata.
- As an endpoint engineering owner, I can capture rollout evidence for approved endpoint channels and preserve it with a change record.
- As an endpoint engineering owner, I can verify captured rollout evidence and index it for API or console retrieval.
- As an endpoint engineering owner, I can search rollout evidence by environment, status, and deployment target from the CLI, API, or console.
- As a release manager, I can generate a signed promotion approval request only after rollout evidence is verified and ready.
- As a release manager, I can record a promotion execution only after the signed request is approved and bound to the rollout ring advancement.
- As a release manager, I can search promotion executions and open audit details with approval, request, rollout, change, and rollback evidence links.
- As a release manager, I can export promotion execution audit records to SIEM and ITSM payloads without hand-translating CAVRA evidence.
- As an incident commander, I can record an approved rollback execution tied to the original promotion execution and rollback evidence.
- As a SOC analyst, I can deliver promotion audit and rollback execution records through configured connectors with retry evidence.
- As a release engineer, I can smoke-test installer metadata and the native packaged runtime before publishing a release asset.
- As an auditor, I can run a single CLI verifier and see checksum, evidence, and signature failures before approval.
- As a release manager, I can review persisted connector delivery history after promotion and rollback audit events are sent.
- As a SOC analyst, I can see dashboard alerts when release governance delivery to SIEM, ITSM, ChatOps, or webhook targets fails.
- As a release manager, I can review channel promotion request history, endpoint-management export history, and endpoint publication delivery status from the API or Evidence Console.
- As an auditor, I can confirm that endpoint export bundles were generated from an approved channel promotion request before publication.
- As an endpoint engineering owner, I can download only checksum-verified endpoint export provider files from a governed API.
- As a release manager, I can see endpoint export download readiness before handing artifacts to Jamf, Intune, or Linux fleet tooling.
- As an endpoint engineering owner, I can normalize Jamf, Intune, Linux fleet, or EDR inventory exports into a single CAVRA observation schema.
- As an endpoint engineering owner, I can reconcile observed runtime versions and checksums against signed deployment targets.
- As a release manager, I can see endpoint drift, missing observations, and stale endpoint reports from CLI, API, or Evidence Console.
- As an endpoint change owner, I can create an approval-bound remediation plan before republishing endpoint exports, rolling back runtimes, or refreshing stale inventory.
- As an auditor, I can see the approved remediation execution record without exposing private endpoint connector implementation.
- As an endpoint operations lead, I can package approved or pending remediation work for ITSM, ChatOps, and private endpoint queues with the original approval and reconciliation context.
- As an endpoint operations lead, I can reconcile provider callback status, external ticket IDs, and completion evidence without exposing connector credentials.
- As an executive release owner, I can review breached, at-risk, and completed endpoint remediation handoffs before approving release governance exceptions.
- As a release manager, I can deliver SLA breach notifications to ITSM, ChatOps, and release governance connectors with redacted retry evidence.
- As a release manager, I can route SLA notifications by severity and channel, suppress duplicate notifications, and track acknowledgement status.
- As a release manager, I can evaluate owner-specific acknowledgement and resolution SLOs before escalating notification follow-up.
- As a release manager, I can batch only deliverable recurrence routes and keep suppressed or waiting routes out of connector payloads.
- As an auditor, I can export suppression audit evidence for maintenance windows, owner unavailability, maximum recurrence limits, and recurrence interval waits.
- As a release manager, I can plan retries for failed recurrence batches without embedding connector credentials.
- As an owner, I can receive a digest of unresolved recurrence routes grouped by provider and owner.
- As an auditor, I can inspect suppression trend categories across maintenance windows, owner calendars, maximum recurrences, and interval waits.

## Enterprise Challenge Solved

Enterprise buyers require release integrity before allowing local enforcement binaries onto developer laptops, CI runners, or air-gapped environments. The Go release package turns runtime binaries into auditable artifacts with checksums, SBOM metadata, signed installer metadata, managed endpoint deployment manifests, signed CI runner bundle metadata, reusable release-governance runner wrappers, signed runner authentication claims, signed daemon evidence stream controls, release channel manifests, managed workstation updater policy, signed channel promotion approvals, Jamf/Intune/Linux endpoint export bundles, governed endpoint export downloads, checksum-enforced endpoint export integrity, public-safe endpoint inventory ingestion, endpoint inventory freshness SLA alerts, endpoint drift reconciliation, reconciliation automation from fresh inventory, approval-bound endpoint drift remediation plans, approved remediation execution records, endpoint remediation handoff packages, endpoint remediation handoff status reconciliation, endpoint remediation SLA and executive reporting, endpoint remediation SLA notification delivery, notification routing policies, duplicate suppression windows, acknowledgement tracking, escalation ladders, owner-specific service-level objectives, escalation delivery actions, owner review workflows, recurrence policies, owner calendars, maintenance-window suppression, recurrence delivery batching, suppression audit exports, recurrence retry policies, owner digest notifications, suppression trend analytics, channel promotion request history, endpoint export history, Evidence Console release channel publishing views, rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters and console/API views, governed rollout evidence artifact retrieval, rollout artifact integrity status, promotion readiness indicators, signed promotion approval requests, approved promotion execution records, promotion execution search and audit drill-downs, rollback evidence links, approved rollback execution records, SIEM/ITSM promotion audit exports, connector delivery for promotion audit and rollback execution records, persisted delivery history, alerting dashboards, installer smoke validation, SLSA provenance, detached signatures, GitHub OIDC-backed keyless attestations, offline bootstrap metadata, CAVRA release evidence, release-candidate upgrade validation, release-asset attachment, and local plus GitHub verifier commands.

## Next Work

1. Add contract-level Go fixtures for the next high-risk release-governance metadata kinds.
2. Document production release-signing operations and key rotation.
