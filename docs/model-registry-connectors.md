# Model Registry Connectors

Last updated: 2026-07-08

CAVRA R4.3 adds model registry connectors that work by reference. They collect metadata, hashes, lineage, owner, risk tier, and evidence references without exporting raw model bytes, weights, training data, prompts, private features, or raw artifacts.

R4.3 is public-repository complete. The closeout boundary is documented in [CAVRA Model Registry Connectors R4.3 Closeout](model-registry-connectors-r4-closeout.md). Customer registry credentials, private owner maps, registry sandbox transcripts, scanner deployment evidence, token rotation proof, and production registry run evidence remain deployment-specific evidence.

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

Public completion means the registry, provider manifests, SDK-compatible validation, compatibility matrix, metadata-only event builder, raw-egress negative test, sample packet, sanitized live gate, workflow, docs, and tests are present and repeatable. Production completion means each customer deployment attaches real registry sandbox validation, credential custody, private ownership mapping, artifact access controls, token rotation, scanner deployment evidence, monitoring, and support evidence.
