# Model Registry Connectors

CAVRA R4.3 adds model registry connectors that work by reference. They collect metadata, hashes, lineage, owner, risk tier, and evidence references without exporting raw model bytes, weights, training data, prompts, private features, or raw artifacts.

## Certified Provider Set

| Provider | Public-safe scope |
| --- | --- |
| MLflow | Registered model and model-version metadata, stage, lineage reference |
| Amazon SageMaker | Model package metadata, approval status, model-card reference |
| Hugging Face | Repository metadata, model-card reference, revision hash |
| Weights & Biases | Artifact metadata, aliases, run lineage, risk metadata |

## Validation Commands

```bash
python3 scripts/validate_model_registry_connectors.py --registry
python3 scripts/validate_model_registry_connectors.py --manifest-dir examples/model-registries/connectors
python3 scripts/validate_model_registry_connectors.py --metadata examples/model-registries/metadata.sample.json
! python3 scripts/validate_model_registry_connectors.py --metadata examples/model-registries/metadata.invalid-raw-content.json
python3 scripts/validate_model_registry_connectors.py --packet examples/model-registries/enterprise-model-registry-connectors.live.sanitized.example.json --require-live
python3 -m pytest tests/test_model_registry_connectors.py -q
```

## Operating Boundary

The public repository certifies the manifest contract, metadata-only payload shape, no-raw-model-egress behavior, compatibility metadata, and readiness packet structure. Customer deployments still provide real registry credentials, tenant scoping, private model-owner mapping, registry sandbox evidence, and zero-trust scanner evidence when required.
