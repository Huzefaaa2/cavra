# CAVRA Zero-Trust Scanner Agent R4.4 Closeout

Last updated: 2026-07-08

R4.4 is closed for the public CAVRA repository. The repository now contains the public-safe zero-trust scanner result contract, recursive egress sanitizer, hash-only reference file scan, raw-egress negative fixture, sample packet, sanitized live-mode packet, strict CI gate, documentation, and tests needed to prove the customer-side scanner boundary.

Real customer-side scanner packaging, private network deployment evidence, tenant routing, scanner credentials, private endpoint/firewall evidence, production scanner operations, custody review logs, and incident drill artifacts belong to Managed or Enterprise evidence rooms, not public source.

## What Is Complete

- Scanner result contract in `src/cavra/zero_trust_scanner.py`.
- Supported customer-side execution modes for customer VPC, on-prem, private subnet, air-gapped, container, and Kubernetes deployments.
- Recursive sanitizer that removes raw model, training data, prompt, source, secret, credential, raw artifact, and file-content fields.
- Metadata-only scan result builder.
- Hash-only local reference file scan builder.
- Raw-egress negative fixture at `examples/zero-trust-scanner/scan-result.invalid-raw-egress.json`.
- Public-safe sample scanner readiness packet.
- Sanitized live-mode packet at `examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json`.
- Strict live validation workflow.
- Tests for scan result validation, raw-egress blocking, sanitizer behavior, hash-only file scanning, sample/live packet behavior, missing-control blockers, workflow coverage, and closeout documentation.

## Evidence Boundary

Public evidence proves scanner result shape, supported execution modes, hash-only artifact references, risk scoring fields, findings metadata, recursive raw-egress blocking, sample readiness, and sanitized live readiness. Private deployments attach scanner image or binary provenance, customer network placement evidence, tenant identity scope, key custody, firewall/private endpoint evidence, egress-control run logs, production monitoring, support ownership, and incident drill evidence.

## Verification

```bash
python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.sample.json \
  --output dist/test/zero-trust-scan-result-validation.json

! python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.invalid-raw-egress.json \
  --output dist/test/zero-trust-scan-result-invalid.json

python3 scripts/validate_zero_trust_scanner.py \
  --scan-result examples/zero-trust-scanner/scan-result.sample.json \
  --build-result \
  --output dist/test/zero-trust-scan-result-built.json

python3 scripts/validate_zero_trust_scanner.py \
  --scan-file examples/zero-trust-scanner/reference-artifact.txt \
  --output dist/test/zero-trust-reference-file-scan.json

python3 scripts/validate_zero_trust_scanner.py \
  --packet examples/zero-trust-scanner/enterprise-zero-trust-scanner.sample.json \
  --output dist/test/enterprise-zero-trust-scanner-sample.json

python3 scripts/validate_zero_trust_scanner.py \
  --packet examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-zero-trust-scanner-live-sanitized.json

python3 -m pytest tests/test_zero_trust_scanner.py -q
python3 -m ruff check \
  src/cavra/zero_trust_scanner.py \
  scripts/validate_zero_trust_scanner.py \
  tests/test_zero_trust_scanner.py
```

Expected sanitized live-style result:

```json
{
  "ready_for_live_zero_trust_scanner": true,
  "status": "ready",
  "blocker_count": 0,
  "warning_count": 0
}
```

## Phase 4 Closeout Handoff

Phase 4 connector and scanner closeout can now verify the complete public chain: R4.1 connector SDK, R4.2 priority certified connectors, R4.3 metadata-only model registry connectors, and R4.4 zero-trust scanner agent. The closeout gate should prove all public contracts run in CI and clearly preserve the private evidence boundary for tenant credentials, provider sandboxes, customer registry access, scanner deployment proof, network controls, and production operations.
