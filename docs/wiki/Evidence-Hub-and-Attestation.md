# Evidence Hub and Attestation

Phase 3 is in progress.

## What Changed

CAVRA now creates verifier-ready evidence bundles:

- `manifest.json`
- `evidence.json`
- `pr-attestation.md`
- `compliance-mapping.md`
- `siem-event.json`
- `sandbox-run-summary.json`

## Commands

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security
cavra evidence verify .cavra/evidence/latest
cavra evidence siem-event .cavra/evidence/latest
```

## Enterprise Value

Evidence bundles turn pre-action runtime decisions into artifacts that reviewers, auditors, and SOC teams can inspect. The manifest includes checksums and signature metadata so tampering can be detected.

## Next Work

- Public/private key evidence signatures.
- Provider-specific SIEM exporters.
- Immutable evidence store reference exporters.
- Evidence retention controls.
- Evidence metadata persistence in the API.
