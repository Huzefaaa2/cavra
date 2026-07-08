# CAVRA Managed And Enterprise Certificate Publication Index

The Managed and Enterprise certificate publication index is the downstream publication-control artifact for a completed operating release certificate. It proves where the customer-safe certificate can be surfaced, which channel owners approved each target, which claims are safe to repeat, and how each publication target can be rolled back without exposing tenant, contract, credential, or raw operational material.

Use it after the [Managed And Enterprise Operating Release Certificate](managed-enterprise-operating-certificate.md) is complete.

## What It Proves

The publication index requires sanitized references for:

- operating certificate, publication owner, approval record, evidence room, publication window, and rollback plan;
- approved publication channels for the product website, GitHub README, GitHub Wiki, customer-success communication, sales enablement, and support portal;
- public-safe claims for validated operating chain, certificate approval, evidence custody, support path, and AISPM operations;
- publication decision, blocker state, published certificate pointer, next review, and customer-safe support contact path;
- redaction controls proving no secrets, credentials, tenant names, raw logs, raw prompts, raw model data, raw alert payloads, private release notes, contracts, or customer PII are present.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_certificate_publication_index.py \
  --export-dir examples/managed-enterprise-certificate-publication
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-certificate-publication-index \
  --export-dir examples/managed-enterprise-certificate-publication
```

## Validate A Live Sanitized Index

```bash
python3 scripts/validate_managed_enterprise_certificate_publication_index.py \
  --index examples/managed-enterprise-certificate-publication/managed-enterprise-certificate-publication-index.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-certificate-publication-index \
  --index examples/managed-enterprise-certificate-publication/managed-enterprise-certificate-publication-index.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_certificate_publication": true,
  "blocker_count": 0
}
```

## Required Publication Channels

| Channel | Purpose |
| --- | --- |
| Product website | Commercial product site certificate reference. |
| GitHub README | Repository README certificate pointer. |
| GitHub Wiki | Wiki textbook and operating docs certificate pointer. |
| Customer success | Customer-success communication reference. |
| Sales enablement | Sales and partner enablement reference. |
| Support portal | Support portal or customer helpdesk reference. |

## Required Public-Safe Claims

| Claim | Purpose |
| --- | --- |
| Operating chain validated | The launch-to-operations sequence was validated as a chain. |
| Certificate approved | The operating certificate has owner signoff. |
| Evidence custody active | Evidence custody and verifier access are active. |
| Support path active | Customer-safe support and escalation route is active. |
| AISPM operations active | AISPM review and posture operations are active. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, private incident details, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `certificate://`, `content://`, `evidence://`, `ticket://`, `audit://`, `release://`, `runbook://`, `workflow://`, `vault://`, `share://`, or `sample://`.

## Relationship To The Operating Certificate

The operating certificate proves customer-safe readiness. The publication index proves the certificate can be safely referenced across approved public, customer-success, sales, support, and repository channels.
