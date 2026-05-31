# Release Governance Final Closeout Operator Guide

This guide packages the completed final closeout workflow into an operator runbook for release managers, platform owners, auditors, and trial teams.

## Runbook Checklist

1. Generate final readiness evidence.
2. Attach external signature metadata to the archive manifest.
3. Generate and deliver the release closeout summary.
4. Request and approve retention review.
5. Build the downloadable closeout artifact bundle.
6. Run retention health for approval, expiry, and failed delivery findings.
7. Send retention health alerts when health is not healthy.
8. Create retry plans for failed closeout deliveries.
9. Run the retry worker in dry-run mode before live redelivery.
10. Link the final decision to the release record or audit case.

## Role Responsibilities

| Role | Responsibility |
| --- | --- |
| Release manager | Owns closeout execution and final acceptance. |
| Platform owner | Owns connectors, retries, and operational routing. |
| Security architect | Reviews retention health and open-core boundaries. |
| Auditor | Reviews the artifact bundle and evidence chain. |
| Trial owner | Explains Community versus Enterprise responsibilities. |

## Evidence To Retain

- Final readiness bundle metadata
- Signed archive manifest metadata
- Release closeout summary and delivery metadata
- Retention review request and approval decision
- Closeout artifact bundle metadata
- Retention health report
- Retention alert plan and delivery evidence
- Closeout retry plan, worker run, and execution record
- External release record or audit case reference

## Diagram

See `release-governance-final-closeout-operator-guide.svg`.

## Open-Core Boundary

Community Edition records evidence and public-safe metadata. Enterprise Edition or operator-owned systems enforce private retention policies, perform archive writes or deletions, handle SSO/RBAC, execute live connector delivery with secrets, validate licenses, and run paid policy packs.

## Recommended Next Issue

Delivered in Final-Closeout-Trial-Walkthrough.md, Final-Closeout-Trial-Sample-Evidence.md, and Final-Closeout-Sales-Engineering-Demo.md. Continue by converting the onboarding package into an interactive public sandbox flow.
