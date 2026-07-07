# CAVRA Enterprise KMS/HSM Evidence Custody

Last updated: 2026-07-07

This page defines the R3.1 public-safe KMS/HSM evidence signing, key rotation, custody policy, revocation, and independent verifier readiness contract for CAVRA Enterprise and Managed deployments.

The public repository implements the readiness contract, sample packets, strict live validation gate, and documentation. Private Enterprise deployments must supply the real KMS/HSM provider references, operator approvals, signer logs, rotation evidence, revocation drill evidence, and verifier handoff evidence.

R3.1 is public-repository complete. The closeout boundary is documented in [CAVRA Enterprise KMS/HSM Evidence Custody R3.1 Closeout](evidence-custody-r3-closeout.md). Real KMS/HSM key identifiers, signer logs, operator approvals, custody exports, revocation transcripts, verifier handoff packets, provider account details, and tenant evidence remain deployment-specific Managed or Enterprise evidence-room records.

## Scope

R3.1 covers:

- evidence signing through external KMS, managed HSM, Vault Transit, or PKCS#11-backed providers;
- non-exportable private signing keys;
- dual-control custody and separation of duties;
- key rotation cadence, overlap, and historical verification retention;
- emergency revocation drill evidence;
- public trust-root distribution for independent verifiers;
- offline evidence bundle and PR attestation verification.

## Public Artifacts

| Artifact | Purpose |
| --- | --- |
| `src/cavra/evidence_custody.py` | Defines the custody contract and packet validator. |
| `scripts/validate_enterprise_evidence_custody.py` | Validates sample or live evidence custody packets. |
| `examples/evidence/enterprise-evidence-custody.sample.json` | Public-safe sample packet showing the required evidence shape. |
| `examples/evidence/enterprise-evidence-custody.live.sanitized.example.json` | Sanitized live-mode packet that passes `--require-live` without exposing customer infrastructure. |
| `.github/workflows/enterprise-evidence-custody.yml` | CI workflow for sample validation and manual strict live validation. |
| `tests/test_evidence_custody.py` | Contract, sample, live-mode, blocker, and workflow tests. |

## Supported Signing Providers

The public contract accepts these provider categories:

| Provider type | Intended implementation |
| --- | --- |
| `aws_kms` | AWS KMS asymmetric signing key. |
| `azure_key_vault` | Azure Key Vault key with sign operation. |
| `managed_hsm` | Azure Managed HSM, CloudHSM, or equivalent managed HSM. |
| `gcp_cloud_kms` | Google Cloud KMS asymmetric signing key. |
| `hashicorp_vault_transit` | Vault Transit signing key with export disabled. |
| `pkcs11_hsm` | PKCS#11-backed HSM integration. |

Private key export must be disabled. CAVRA should receive signatures or public trust material, not raw private signing keys.

## Evidence Packet

The packet schema is:

```json
{
  "schema_version": "cavra.evidence.custody.v1",
  "evidence_mode": "sample",
  "signing_provider": {
    "type": "azure_key_vault",
    "key_ref": "azure://keyvault/cavra-evidence/keys/prod-evidence-2026-q3",
    "key_id": "prod-evidence-2026-q3",
    "algorithm": "Ed25519",
    "private_key_exportable": false,
    "external_signing_enforced": true
  },
  "custody_policy": {
    "custody_boundary": "cloud_kms",
    "owners": ["platform-security", "security-operations"],
    "dual_control_required": true,
    "separation_of_duties": true,
    "break_glass_process": true,
    "private_key_export_allowed": false
  },
  "rotation": {
    "cadence_days": 90,
    "overlap_days": 14,
    "previous_key_retained_for_verification": true,
    "emergency_revocation_tested": true,
    "latest_rotation_evidence_ref": "evidence://custody/sample-rotation-drill",
    "next_rotation_due_at": "2026-10-01T00:00:00Z"
  },
  "trust_roots": {
    "active_key_ids": ["prod-evidence-2026-q3"],
    "retired_key_ids": ["prod-evidence-2026-q2"],
    "revoked_key_ids": [],
    "distribution_package_ref": "evidence://trust-roots/prod-trust-roots-2026-q3",
    "distribution_checksum_verified": true,
    "verifier_access_confirmed": true
  },
  "independent_verifier": {
    "enabled": true,
    "offline_verification_supported": true,
    "sample_bundle_verified": true,
    "attestation_verified": true,
    "latest_verification_evidence_ref": "evidence://custody/sample-independent-verifier",
    "commands": [
      "cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-roots.json --key-id prod-evidence-2026-q3",
      "cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation"
    ]
  }
}
```

`evidence_mode: sample` validates packet shape only. Production readiness requires `evidence_mode: live` and `--require-live`.

## Validation

Public/sample validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.sample.json \
  --output dist/test/enterprise-evidence-custody-sample.json
```

Sanitized live-mode validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet examples/evidence/enterprise-evidence-custody.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-evidence-custody-live-sanitized.json
```

Private live validation:

```bash
python3 scripts/validate_enterprise_evidence_custody.py \
  --packet .cavra/enterprise/enterprise-evidence-custody-live.json \
  --require-live \
  --output dist/enterprise/enterprise-evidence-custody-result.json
```

Unit tests:

```bash
python3 -m pytest tests/test_evidence_custody.py -q
```

## Completion Criteria

R3.1 is public-repository complete when the sample and sanitized live-mode packet validate, tests pass, and the closeout boundary is documented. A specific Managed or Enterprise deployment is production-complete only when its private live packet returns:

```json
{
  "ready_for_enterprise_live_evidence_custody": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

The public repository ships a sanitized live-mode packet that proves this validator path without exposing real custody details. Private deployments must replace the sanitized packet with actual KMS/HSM signer, custody, rotation, revocation, trust-root, and verifier evidence.

## AISPM Production Gate Link

The final AISPM production readiness gate should include the live evidence custody packet. A deployment is not launch-ready if:

- private evidence signing keys are exportable;
- signing does not happen through an approved external provider;
- dual-control custody is missing;
- rotation cadence exceeds policy;
- revoked and retired keys are not handled in trust-root distribution;
- independent verifier access is missing;
- sample bundle or PR attestation verification has not passed.

## Relationship To Existing Evidence Commands

The current public CLI already supports local Ed25519 evidence signing, trust-root creation, trust-root bundle distribution, bundle verification, and PR attestation verification:

```bash
cavra evidence trust-distribution .cavra/keys/prod-evidence-trust-root.json \
  --output .cavra/keys/trust-root-distribution \
  --distribution-id prod-trust-roots-2026-q3

cavra evidence verify .cavra/evidence/latest \
  --trust-root .cavra/keys/evidence-trust-roots.json \
  --key-id prod-evidence-2026-q3 \
  --minimum-retention-days 2555

cavra evidence verify-attestation .cavra/evidence/latest \
  --output .cavra/evidence/attestation
```

Enterprise KMS/HSM integrations should preserve this verifier-facing shape while keeping signing operations and private custody inside the operator-owned provider boundary.
