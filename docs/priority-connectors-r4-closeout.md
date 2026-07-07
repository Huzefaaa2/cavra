# CAVRA Priority Certified Connectors R4.2 Closeout

Last updated: 2026-07-08

R4.2 is closed for the public CAVRA repository. The repository now contains the public-safe certified connector registry, eleven priority provider manifests, compatibility matrix generation, certification packet generation through the R4.1 SDK, request-spec support for SCM and CI/CD providers, readiness validator, sample packet, sanitized live-mode packet, strict CI gate, documentation, and tests needed to prove the first priority connector wave boundary.

Tenant-specific credentials, provider sandbox transcripts, webhook secrets, firewall allowlists, customer routing policies, token rotation records, production support records, and live provider run evidence belong to Managed or Enterprise evidence rooms, not public source.

## What Is Complete

- Certified connector registry in `src/cavra/certified_connectors.py`.
- Eleven public-safe provider manifests under `examples/connectors/priority-certified/`.
- Priority provider coverage for GitHub, GitLab, Azure Repos, GitHub Actions, Jenkins, Splunk, Microsoft Sentinel, ServiceNow, Jira, Slack, and Microsoft Teams.
- Required group coverage for SCM, CI/CD, SIEM, ITSM, and ChatOps.
- R4.1 SDK-compatible manifest validation for every priority provider.
- Certification packet generation and compatibility matrix generation for the priority provider set.
- Delivery request-spec support for GitHub, GitLab, Azure Repos, GitHub Actions, Jenkins, Splunk, Sentinel, ServiceNow, Jira, Slack, and Teams.
- Readiness validator for sample and live priority connector packets.
- Public-safe sample priority connector readiness packet.
- Sanitized live-mode packet at `examples/connectors/enterprise-priority-connectors.live.sanitized.example.json`.
- Strict live validation workflow.
- Tests for registry coverage, checked-in manifest parity, missing-provider blocking, sample/live packet behavior, SCM and CI/CD request specs, and auth failure behavior.

## Evidence Boundary

Public evidence proves provider coverage, manifest shape, R4.1 SDK compatibility, compatibility matrix generation, request-spec generation, credential redaction expectations, sample readiness, and sanitized live readiness. Private deployments attach real provider sandbox logs, credential custody evidence, token rotation proof, customer routing policies, firewall allowlisting, support ownership, production monitoring, and incident escalation records.

## Verification

```bash
python3 scripts/validate_priority_connectors.py \
  --registry \
  --output dist/test/priority-connector-registry.json

python3 scripts/validate_priority_connectors.py \
  --manifest-dir examples/connectors/priority-certified \
  --output dist/test/priority-connector-manifests.json

python3 scripts/validate_priority_connectors.py \
  --packet examples/connectors/enterprise-priority-connectors.sample.json \
  --output dist/test/enterprise-priority-connectors-sample.json

python3 scripts/validate_priority_connectors.py \
  --packet examples/connectors/enterprise-priority-connectors.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-priority-connectors-live-sanitized-result.json

python3 -m pytest tests/test_certified_connectors.py -q
python3 -m ruff check \
  src/cavra/certified_connectors.py \
  src/cavra/integrations.py \
  scripts/validate_priority_connectors.py \
  tests/test_certified_connectors.py
```

Expected sanitized live-style result:

```json
{
  "ready_for_live_priority_connectors": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## R4.3 Handoff

R4.3 model registry connectors must follow the R4.1 SDK contract and R4.2 provider evidence boundary. Model registry connectors should expose metadata-only, no-raw-model-egress behavior while preserving certified manifest validation, compatibility matrix publication, sanitized live readiness packets, and private customer credential custody.
