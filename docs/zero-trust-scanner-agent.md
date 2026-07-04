# Zero-Trust Scanner Agent

CAVRA zero-trust scanner agents run where sensitive AI assets already live: customer VPCs, private subnets, on-premises networks, containers, Kubernetes clusters, and air-gapped estates. The public contract is intentionally metadata-only. It lets CAVRA score and evidence AI assets without moving raw model bytes, training data, source code, prompts, credentials, or private artifacts out of the customer-controlled boundary.

This page documents the public Community/Enterprise contract. Actual Enterprise scanner packaging, network placement, private credentials, tenant routing, and customer-side operating evidence are deployment-specific.

## Operating Boundary

The scanner is designed around a strict boundary:

```text
Customer-controlled environment
  ├── AI model registry, artifact store, source repo, endpoint, or package cache
  ├── CAVRA scanner agent
  │     ├── reads local metadata and computes hashes
  │     ├── assigns risk scores and risk tiers
  │     ├── writes local evidence references
  │     └── blocks raw egress
  └── CAVRA API / evidence room receives metadata-only results
```

Allowed execution modes are:

- `customer_vpc`
- `on_prem`
- `private_subnet`
- `air_gapped`
- `container`
- `kubernetes`

## Result Contract

A scanner result must include:

- `scanner_id`
- `environment`
- `asset_ref`
- `asset_type`
- `artifact_digest`
- `risk_score`
- `risk_tier`
- `findings`
- `evidence_ref`

Example:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.sample.json
```

Normalized scanner result:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.sample.json \
  --build-result \
  --output dist/zero-trust-scan-result-built.json
```

Hash-only reference scan:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --scan-file examples/zero-trust-scanner/reference-artifact.txt \
  --output dist/zero-trust-reference-file-scan.json
```

## Forbidden Egress

The contract blocks fields that may carry raw data or secrets:

- `raw_model`
- `model_bytes`
- `model_weights`
- `training_data`
- `dataset_rows`
- `prompt_samples`
- `source_code`
- `secret`
- `private_key`
- `credential`
- `raw_artifact`
- `file_contents`

Negative fixture:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.invalid-raw-egress.json
```

The negative fixture must fail. CI uses this to prove that raw model weights, training data, and secrets cannot pass the public contract.

## Readiness Packet

The scanner readiness packet proves that the deployment has:

- customer-side deployment topology;
- scanner result contract artifact;
- egress sanitizer;
- reference scan sample;
- raw-egress negative fixture;
- deployment topology evidence;
- no-raw-model, no-training-data, no-source-code, no-secret egress controls;
- operating evidence references for deployment validation, egress tests, custody review, and incident drill.

Sample packet validation:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --packet examples/zero-trust-scanner/enterprise-zero-trust-scanner.sample.json
```

Live sanitized packet validation:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --packet examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json \
  --require-live
```

## Production Use

For an Enterprise deployment, replace the public sample packet with a live sanitized packet that references the customer's actual scanner deployment, egress-control test run, custody review, and incident drill. Do not attach raw model files, source files, prompt samples, datasets, or secrets to the public packet.

The public completion condition is:

```text
ready_for_live_zero_trust_scanner: true
blocker_count: 0
```

Private production completion additionally requires customer-side scanner deployment evidence, identity and tenant scoping, key custody, firewall or private endpoint evidence, and operational ownership.
