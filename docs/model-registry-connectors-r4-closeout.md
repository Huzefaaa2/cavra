# CAVRA Model Registry Connectors R4.3 Closeout

Last updated: 2026-07-08

R4.3 is closed for the public CAVRA repository. The repository now contains the metadata-only model registry connector registry, four provider manifests, R4.1 SDK-compatible certification packets, compatibility matrix generation, metadata event builder, no-raw-model-egress validator, sample packet, sanitized live-mode packet, strict CI gate, documentation, and tests needed to prove the model registry connector boundary.

Customer registry credentials, private model owner mapping, registry sandbox transcripts, private model card payloads, model artifact access paths, zero-trust scanner deployment logs, and live production registry evidence belong to Managed or Enterprise evidence rooms, not public source.

## What Is Complete

- Model registry connector registry in `src/cavra/model_registry_connectors.py`.
- Four public-safe provider manifests under `examples/model-registries/connectors/`.
- Provider coverage for MLflow, Amazon SageMaker Model Registry, Hugging Face, and Weights & Biases.
- R4.1 SDK-compatible manifest validation for every model registry provider.
- Certification packet generation and compatibility matrix generation for the model registry provider set.
- Metadata-only event builder for model reference, digest, lineage, owner, risk tier, and evidence references.
- Negative validator that blocks raw model bytes, weights, training data, prompts, private features, raw artifacts, and embedded payload content.
- Public-safe sample model registry readiness packet.
- Sanitized live-mode packet at `examples/model-registries/enterprise-model-registry-connectors.live.sanitized.example.json`.
- Strict live validation workflow.
- Tests for registry coverage, checked-in manifest parity, missing-provider blocking, metadata-only event construction, raw-egress rejection, sample/live packet behavior, workflow coverage, and closeout documentation.

## Evidence Boundary

Public evidence proves provider coverage, manifest shape, R4.1 SDK compatibility, compatibility matrix generation, metadata-only payload shape, no-raw-model-egress behavior, sample readiness, and sanitized live readiness. Private deployments attach real registry sandbox logs, credential custody evidence, private model owner mapping, customer registry routing, artifact access controls, token rotation proof, scanner deployment evidence, production monitoring, and incident escalation records.

## Verification

```bash
python3 scripts/validate_model_registry_connectors.py \
  --registry \
  --output dist/test/model-registry-connector-registry.json

python3 scripts/validate_model_registry_connectors.py \
  --manifest-dir examples/model-registries/connectors \
  --output dist/test/model-registry-connector-manifests.json

python3 scripts/validate_model_registry_connectors.py \
  --metadata examples/model-registries/metadata.sample.json \
  --output dist/test/model-registry-metadata-validation.json

! python3 scripts/validate_model_registry_connectors.py \
  --metadata examples/model-registries/metadata.invalid-raw-content.json \
  --output dist/test/model-registry-metadata-invalid.json

python3 scripts/validate_model_registry_connectors.py \
  --metadata examples/model-registries/metadata.sample.json \
  --build-event \
  --output dist/test/model-registry-metadata-event.json

python3 scripts/validate_model_registry_connectors.py \
  --packet examples/model-registries/enterprise-model-registry-connectors.sample.json \
  --output dist/test/enterprise-model-registry-connectors-sample.json

python3 scripts/validate_model_registry_connectors.py \
  --packet examples/model-registries/enterprise-model-registry-connectors.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-model-registry-connectors-live-sanitized.json

python3 -m pytest tests/test_model_registry_connectors.py -q
python3 -m ruff check \
  src/cavra/model_registry_connectors.py \
  scripts/validate_model_registry_connectors.py \
  tests/test_model_registry_connectors.py
```

Expected sanitized live-style result:

```json
{
  "ready_for_live_model_registry_connectors": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## R4.4 Handoff

R4.4 zero-trust scanner agents must consume the R4.3 metadata-only registry contract without expanding data egress. Scanner results should reference model registry assets by stable URI, emit hashes, risk scores, and evidence references only, preserve raw-egress negative tests, attach sanitized live readiness packets, and keep customer VPC/on-prem scanner deployment evidence private.
