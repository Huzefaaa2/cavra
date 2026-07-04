# Zero-Trust Scanner Agent

CAVRA zero-trust scanner agents run where sensitive AI assets already live: customer VPCs, private subnets, on-premises networks, containers, Kubernetes clusters, and air-gapped estates. The scanner emits metadata, hashes, risk scores, finding metadata, and evidence references only.

It is built to prevent raw model bytes, model weights, training data, source code, prompt samples, file contents, credentials, or private artifacts from leaving the customer-controlled environment.

## Boundary

```text
Customer-controlled environment
  ├── model registry / artifact store / code repo / endpoint
  ├── CAVRA zero-trust scanner
  │     ├── computes hashes
  │     ├── scores risk
  │     ├── emits findings metadata
  │     └── blocks raw egress
  └── CAVRA receives metadata-only evidence
```

Supported execution modes:

- `customer_vpc`
- `on_prem`
- `private_subnet`
- `air_gapped`
- `container`
- `kubernetes`

## What Leaves The Boundary

Allowed output:

- scanner ID;
- environment;
- asset reference;
- asset type;
- hash digest;
- risk score and tier;
- findings metadata;
- evidence references.

Forbidden output:

- raw model bytes or weights;
- training data;
- dataset rows;
- prompt samples;
- source code;
- secrets, private keys, credentials;
- raw artifacts or file contents.

## Validation

Validate a metadata-only scan result:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.sample.json
```

Prove raw egress is blocked:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.invalid-raw-egress.json
```

Validate a live sanitized scanner packet:

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --packet examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json \
  --require-live
```

The public gate passes when:

```text
ready_for_live_zero_trust_scanner: true
blocker_count: 0
```

Enterprise deployments still provide private scanner packaging, real network placement, tenant scoping, private credentials, egress-control run logs, and operating evidence inside the customer evidence room.
