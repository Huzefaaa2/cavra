# Model Registry Connectors

CAVRA R4.3 adds model registry connectors that work by reference. They collect metadata, hashes, lineage, owner, risk tier, and evidence references without exporting raw model bytes, weights, training data, prompts, private features, or raw artifacts.

## Certified Provider Set

| Provider | Public-safe scope |
| --- | --- |
| MLflow | Registered model and model-version metadata, stage, lineage reference |
| Amazon SageMaker | Model package metadata, approval status, model-card reference |
| Hugging Face | Repository metadata, model-card reference, revision hash |
| Weights & Biases | Artifact metadata, aliases, run lineage, risk metadata |

## What Is Implemented

- Versioned model registry connector manifests under `examples/model-registries/connectors/`.
- Built-in registry and compatibility matrix in `src/cavra/model_registry_connectors.py`.
- Metadata-only event builder and negative no-raw-model-egress validator.
- Sample and sanitized live evidence packets.
- Strict CI workflow and tests.

## Validate The Registry

```bash
python3 scripts/validate_model_registry_connectors.py \
  --registry \
  --output dist/test/model-registry-connector-registry.json
```

Validate checked-in manifests:

```bash
python3 scripts/validate_model_registry_connectors.py \
  --manifest-dir examples/model-registries/connectors \
  --output dist/test/model-registry-connector-manifests.json
```

Validate metadata-only payloads:

```bash
python3 scripts/validate_model_registry_connectors.py \
  --metadata examples/model-registries/metadata.sample.json \
  --output dist/test/model-registry-metadata-validation.json
```

Confirm raw content is blocked:

```bash
! python3 scripts/validate_model_registry_connectors.py \
  --metadata examples/model-registries/metadata.invalid-raw-content.json \
  --output dist/test/model-registry-metadata-invalid.json
```

Validate live sanitized evidence:

```bash
python3 scripts/validate_model_registry_connectors.py \
  --packet examples/model-registries/enterprise-model-registry-connectors.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-model-registry-connectors-live-sanitized.json
```

## Operating Boundary

The public repository certifies the manifest contract, metadata-only payload shape, no-raw-model-egress behavior, compatibility metadata, and readiness packet structure. Customer deployments still provide real registry credentials, tenant scoping, private model-owner mapping, registry sandbox evidence, and zero-trust scanner evidence when required.
