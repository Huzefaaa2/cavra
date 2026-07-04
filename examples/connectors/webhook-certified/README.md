# CAVRA Reference Webhook Connector

This folder contains the public-safe reference connector manifest for the R4.1 connector SDK and certification harness.

Validate the manifest:

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

The example is intentionally metadata-only. It does not contain live webhook URLs, tokens, customer records, or provider credentials.
