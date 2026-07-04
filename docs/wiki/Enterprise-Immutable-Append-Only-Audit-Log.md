# Enterprise Immutable Append-Only Audit Log

CAVRA R3.2 defines a public-safe immutable append-only audit log contract for Enterprise and Managed deployments.

The audit log is separate from evidence bundles. Evidence bundles package reviewer and auditor artifacts for a session. The audit log is the continuous operating record of decisions, approvals, exports, failures, recovery actions, and administrative changes.

## Implemented Foundation

| Component | Purpose |
| --- | --- |
| `append_audit_event` | Appends JSONL audit records with sequence numbers, previous hash, record hash, and optional HMAC signature. |
| `verify_append_only_audit_log` | Verifies sequence order, hash-chain continuity, record hashes, and optional signatures. |
| `validate_enterprise_audit_log_packet` | Validates sample or live Enterprise immutable audit-log readiness packets. |
| `scripts/validate_enterprise_audit_log.py` | Verifies local JSONL audit logs and validates public sample or private live readiness packets. |
| `examples/audit/enterprise-audit-log.sample.json` | Public-safe packet showing the expected readiness evidence shape. |
| `examples/audit/enterprise-audit-log.live.sanitized.example.json` | Sanitized live-mode example that passes `--require-live` without exposing real customer infrastructure. |
| `.github/workflows/enterprise-audit-log.yml` | CI workflow for sample validation and manual strict live validation. |
| `tests/test_audit_log.py` | Hash-chain, tamper detection, sample, live-mode, blocker, and workflow tests. |

## Required Evidence

- Audit log is separate from evidence bundles.
- Records are append-only and hash chained.
- Tamper detection is tested.
- Retention is at least 2555 days for regulated evidence.
- Legal hold and delete protection are enabled.
- JSONL, SIEM, and auditor-package exports are supported.
- Alerts cover audit write, integrity, retention, and export failures.
- Tamper drill, recovery drill, and auditor handoff evidence are present.

## Validation

Local hash-chain validation:

```bash
python3 scripts/validate_enterprise_audit_log.py \
  --log .cavra/audit/audit.jsonl \
  --key "$CAVRA_AUDIT_LOG_HMAC_KEY" \
  --key-id audit-prod-2026-q3
```

Private live readiness validation:

```bash
python3 scripts/validate_enterprise_audit_log.py \
  --packet .cavra/enterprise/enterprise-audit-log-live.json \
  --require-live \
  --output dist/enterprise/enterprise-audit-log-result.json
```

Sanitized live-mode template validation:

```bash
python3 scripts/validate_enterprise_audit_log.py \
  --packet examples/audit/enterprise-audit-log.live.sanitized.example.json \
  --require-live
```

R3.2 is production-complete only when the live packet returns `ready_for_enterprise_live_audit_log: true`, `blocker_count: 0`, and `warning_count: 0`.

Detailed repo document: [Enterprise Immutable Append-Only Audit Log](https://github.com/Huzefaaa2/cavra/blob/main/docs/immutable-append-only-audit-log.md).
