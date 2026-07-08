# CAVRA Managed And Enterprise Operating Release Certificate

The Managed and Enterprise operating release certificate is the customer-safe summary artifact for a completed launch-to-operations sequence. It references the operating chain result and records certificate sections, owner signoffs, public-safe claims, evidence custody, validity window, and next review without exposing private tenant or commercial material.

Use it after the [Managed And Enterprise Operating Chain](managed-enterprise-operating-chain.md) is complete.

## What It Proves

The certificate requires sanitized references for:

- operating chain result;
- certificate owner, version, evidence room, publication record, and validity window;
- scope, readiness basis, operating model, trust controls, and customer next-step sections;
- release owner, security owner, support owner, customer-success owner, and evidence-custodian signoffs;
- certificate decision, operating release reference, public-safe claims, open blockers, and next review.

## Generate Templates

```bash
python3 scripts/validate_managed_enterprise_operating_certificate.py \
  --export-dir examples/managed-enterprise-operating-certificate
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-certificate \
  --export-dir examples/managed-enterprise-operating-certificate
```

## Validate A Live Sanitized Certificate

```bash
python3 scripts/validate_managed_enterprise_operating_certificate.py \
  --certificate examples/managed-enterprise-operating-certificate/managed-enterprise-operating-certificate.live.sanitized.example.json \
  --require-live
```

Installed/operator CLI equivalent:

```bash
cavra release managed-enterprise-operating-certificate \
  --certificate examples/managed-enterprise-operating-certificate/managed-enterprise-operating-certificate.live.sanitized.example.json \
  --require-live
```

The completion condition is:

```json
{
  "ready_for_managed_enterprise_operating_certificate": true,
  "blocker_count": 0
}
```

## Required Certificate Sections

| Section | Purpose |
| --- | --- |
| Scope | Customer-safe statement of the Managed or Enterprise operating release scope. |
| Readiness basis | References the operating chain, live validation, cutover, stabilization, handoff, index, and announcement. |
| Operating model | Summarizes named ownership, support path, review cadence, and AISPM operations. |
| Trust controls | Summarizes evidence custody, redaction boundary, audit posture, and security signoff. |
| Customer next steps | Customer-safe next actions, support path, and review cadence. |

## Required Signoffs

| Signoff | Purpose |
| --- | --- |
| Release owner | Release owner approves the operating certificate. |
| Security owner | Security owner approves the public-safe trust and evidence claims. |
| Support owner | Support owner approves the support and escalation path. |
| Customer-success owner | Customer-success owner approves customer-safe next steps. |
| Evidence custodian | Evidence custodian approves archive and verifier access references. |

## Evidence Boundary

Do not commit customer identities, tenant names, email addresses, SMTP credentials, connector tokens, alert payloads, raw logs, raw prompts, model data, private incident details, pricing, contracts, legal terms, or private release notes.

Commit only sanitized references such as `certificate://`, `content://`, `evidence://`, `ticket://`, `audit://`, `release://`, `runbook://`, `workflow://`, `vault://`, or `share://`.

## Relationship To Operating Chain

The operating chain validates the full evidence sequence. The certificate summarizes that validated chain into a customer-safe release artifact for executive, customer-success, support, and security review.
