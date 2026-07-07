# CAVRA Connector SDK And Certification R4.1 Closeout

Last updated: 2026-07-08

R4.1 is closed for the public CAVRA repository. The repository now contains the public connector SDK manifest contract, reference webhook connector manifest, connector manifest validator, certification packet builder, compatibility matrix builder, readiness validator, sample packet, sanitized live-mode packet, strict CI gate, documentation, and tests needed to prove the connector SDK boundary.

Provider-specific certified connector implementations, live provider sandbox transcripts, customer credentials, tenant routing policies, support ownership evidence, partner onboarding records, and production connector run evidence belong to R4.2 or private Managed and Enterprise evidence rooms, not the public SDK contract.

## What Is Complete

- Connector manifest schema in `src/cavra/connector_sdk.py`.
- Reference webhook connector manifest at `examples/connectors/webhook-certified/connector-manifest.json`.
- Manifest validator for identity, capabilities, auth, runtime, security, tests, and compatibility.
- Certification packet builder for certified connector evidence.
- Compatibility matrix builder for connector manifests.
- Required certification suites: unit, contract, redaction, retry, timeout, auth, and compatibility.
- Readiness validator for sample and live connector SDK packets.
- Public-safe sample connector SDK readiness packet.
- Sanitized live-mode packet at `examples/connectors/enterprise-connector-sdk.live.sanitized.example.json`.
- Strict live validation workflow.
- Tests for manifest parity, validation, certification packet generation, matrix generation, live readiness, failure modes, and workflow coverage.
- Documentation for certification suites, validation commands, and public/private operating boundary.

## Evidence Boundary

Public evidence proves the connector SDK contract, reference connector shape, certification harness behavior, compatibility matrix generation, sample readiness, and sanitized live readiness. Private deployments attach provider-specific sandbox logs, real credentials custody, customer routing policies, partner certification approvals, support ownership records, and production connector run evidence.

## Verification

```bash
python3 scripts/validate_connector_sdk.py \
  --manifest examples/connectors/webhook-certified/connector-manifest.json \
  --output dist/test/reference-webhook-manifest-validation.json

python3 scripts/validate_connector_sdk.py \
  --manifest examples/connectors/webhook-certified/connector-manifest.json \
  --certify \
  --output dist/test/reference-webhook-certification.json

python3 scripts/validate_connector_sdk.py \
  --matrix examples/connectors/webhook-certified/connector-manifest.json \
  --output dist/test/connector-sdk-compatibility-matrix.json

python3 scripts/validate_connector_sdk.py \
  --packet examples/connectors/enterprise-connector-sdk.sample.json \
  --output dist/test/enterprise-connector-sdk-sample.json

python3 scripts/validate_connector_sdk.py \
  --packet examples/connectors/enterprise-connector-sdk.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-connector-sdk-live-sanitized-result.json

python3 -m pytest tests/test_connector_sdk.py -q
python3 -m ruff check \
  src/cavra/connector_sdk.py \
  scripts/validate_connector_sdk.py \
  tests/test_connector_sdk.py
```

Expected sanitized live-style result:

```json
{
  "ready_for_enterprise_live_connector_certification": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## R4.2 Handoff

R4.2 priority certified connectors must consume the R4.1 SDK contract without changing the certification semantics. Provider manifests should pass the R4.1 validation harness, publish compatibility rows, attach sanitized live readiness packets, and keep tenant-specific credentials and provider sandbox evidence private.
