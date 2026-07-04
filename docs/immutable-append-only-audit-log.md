# CAVRA Enterprise Immutable Append-Only Audit Log

Last updated: 2026-07-04

This page defines the R3.2 public-safe immutable append-only audit log contract for CAVRA Enterprise and Managed deployments.

The audit log is deliberately separate from evidence bundles. Evidence bundles package reviewer and auditor artifacts for a session. The audit log is the continuous operating record of decisions, approvals, exports, failures, recovery actions, and administrative changes.

## Scope

R3.2 covers:

- append-only JSONL audit events;
- sequence numbers and previous-record hash chaining;
- record hash verification and optional HMAC signatures;
- immutable or append-protected production storage;
- retention, legal hold, and delete protection;
- SIEM, JSONL, and auditor export support;
- write, integrity, retention, and export failure alerts;
- tamper drill, recovery drill, and auditor handoff evidence.

## Public Artifacts

| Artifact | Purpose |
| --- | --- |
| `src/cavra/audit_log.py` | Implements local append-only hash-chained audit records and the Enterprise audit-log readiness validator. |
| `scripts/validate_enterprise_audit_log.py` | Verifies local JSONL audit logs or validates sample/live Enterprise audit-log readiness packets. |
| `examples/audit/enterprise-audit-log.sample.json` | Public-safe sample packet showing the expected readiness evidence shape. |
| `examples/audit/enterprise-audit-log.live.sanitized.example.json` | Sanitized live-mode packet that passes `--require-live` without exposing customer infrastructure. |
| `.github/workflows/enterprise-audit-log.yml` | CI workflow for sample validation and manual strict live validation. |
| `tests/test_audit_log.py` | Hash-chain, tamper detection, sample, live-mode, blocker, and workflow tests. |

## Local Hash-Chain Verification

The local audit log format is JSON Lines. Each record contains:

- `sequence`;
- `created_at`;
- `event_type`;
- `actor`;
- `action`;
- `target`;
- `decision`;
- tenant/workspace scope when available;
- evidence refs;
- `previous_hash`;
- `record_hash`;
- optional HMAC `signature`.

Validation command:

```bash
python3 scripts/validate_enterprise_audit_log.py \
  --log .cavra/audit/audit.jsonl \
  --key "$CAVRA_AUDIT_LOG_HMAC_KEY" \
  --key-id audit-prod-2026-q3
```

## Readiness Packet Validation

Public/sample validation:

```bash
python3 scripts/validate_enterprise_audit_log.py \
  --packet examples/audit/enterprise-audit-log.sample.json \
  --output dist/test/enterprise-audit-log-sample.json
```

Sanitized live-mode validation:

```bash
python3 scripts/validate_enterprise_audit_log.py \
  --packet examples/audit/enterprise-audit-log.live.sanitized.example.json \
  --require-live \
  --output dist/test/enterprise-audit-log-live-sanitized.json
```

Private live validation:

```bash
python3 scripts/validate_enterprise_audit_log.py \
  --packet .cavra/enterprise/enterprise-audit-log-live.json \
  --require-live \
  --output dist/enterprise/enterprise-audit-log-result.json
```

## Completion Criteria

R3.2 is production-complete only when the live packet returns:

```json
{
  "ready_for_enterprise_live_audit_log": true,
  "blocker_count": 0,
  "warning_count": 0
}
```

Until then, the public contract is implemented but the Enterprise deployment remains pending private immutable audit-store evidence.

## AISPM Production Gate Link

The final AISPM production readiness gate should include the live audit-log packet. A deployment is not launch-ready if:

- audit storage is not separate from evidence bundles;
- append-only controls are not enforced;
- hash-chain verification or tamper detection is missing;
- retention is below regulated target;
- SIEM or auditor export has not been tested;
- write, integrity, retention, or export alerts are missing;
- tamper and recovery drill evidence is missing.

## Production Storage Mapping

Public Community code validates the contract and local JSONL chain. Enterprise operators should map this to one of:

- Azure immutable Blob with versioning and immutability policy;
- AWS S3 Object Lock in compliance mode;
- append-only Postgres table with restricted mutation path and immutable archive export;
- SIEM archive with retention lock;
- WORM storage with auditor export package.
