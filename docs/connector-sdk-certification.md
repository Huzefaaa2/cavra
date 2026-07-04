# Connector SDK And Certification

CAVRA R4.1 introduces a public connector SDK contract and certification harness. It standardizes how connectors describe capabilities, authentication, runtime defaults, security controls, test suites, and compatibility with CAVRA API contracts.

This step does not certify the full priority connector backlog. That is R4.2. R4.1 provides the stable interface and validation path those provider connectors must pass.

## What Is Implemented

- Connector manifest schema in `src/cavra/connector_sdk.py`.
- Reference webhook connector manifest in `examples/connectors/webhook-certified/connector-manifest.json`.
- Manifest validator, certification packet builder, and compatibility matrix builder.
- Enterprise connector SDK readiness packet validator.
- GitHub Actions workflow for sample and strict live validation.
- Tests for manifest validation, certification packet generation, compatibility matrix, and live readiness gates.

## Required Certification Suites

Every certified connector must declare and pass:

- `unit`
- `contract`
- `redaction`
- `retry`
- `timeout`
- `auth`
- `compatibility`

## Validate The Reference Connector

```bash
python3 scripts/validate_connector_sdk.py \
  --manifest examples/connectors/webhook-certified/connector-manifest.json \
  --output dist/test/reference-webhook-manifest-validation.json
```

Generate a certification packet:

```bash
python3 scripts/validate_connector_sdk.py \
  --manifest examples/connectors/webhook-certified/connector-manifest.json \
  --certify \
  --output dist/test/reference-webhook-certification.json
```

Generate a compatibility matrix:

```bash
python3 scripts/validate_connector_sdk.py \
  --matrix examples/connectors/webhook-certified/connector-manifest.json \
  --output dist/test/connector-sdk-compatibility-matrix.json
```

## Readiness Gates

Sample contract validation:

```bash
python3 scripts/validate_connector_sdk.py \
  --packet examples/connectors/enterprise-connector-sdk.sample.json \
  --output dist/test/enterprise-connector-sdk-sample.json
```

Live sanitized validation:

```bash
python3 scripts/validate_connector_sdk.py \
  --packet examples/connectors/enterprise-connector-sdk.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-connector-sdk-live-sanitized.json
```

## Operating Boundary

The public repository ships the SDK contract, reference manifest, validator, sample certification packet, and public-safe tests. Production certified connectors still need provider-specific live sandbox validation, credential custody, customer routing policies, support ownership, and partner onboarding evidence.
