# Go Backend Rollback Drill Retry Approvals And Recovery Playbooks

CAVRA now adds governed approval evidence before acknowledgement audit retry execution and public-safe recovery playbooks for repeated connector delivery failures.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan` creates approval plans from accepted retry acknowledgements.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plans/{approval_plan_id}/decisions` records approved, denied, deferred, or expired retry execution decisions.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook` builds recovery playbooks for repeated SIEM, ITSM, ChatOps, and webhook delivery failures.
- Non-dry-run acknowledgement audit retry workers now select only retry decisions with approved execution evidence.
- Evidence Console actions for **Plan Retry Approval**, **Approve Retry**, and **Recovery Playbook**.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Use **Plan Audit Retry** after failed acknowledgement audit delivery.
2. Use **Ack Retry** to record that the retry decision was reviewed.
3. Use **Plan Retry Approval** to generate approval requirements for live retry execution.
4. Use **Approve Retry** to record governed operator approval.
5. Use **Run Audit Worker** for dry-run verification; live worker execution only selects approved retries.
6. Use **Recovery Playbook** when failures repeat for SIEM, ITSM, ChatOps, or webhook destinations.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plans/{approval_plan_id}/decisions
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook
```

Retry execution approval states:

- `approved`
- `denied`
- `deferred`
- `expired`

## Security Boundary

Approval plans and recovery playbooks are derived from retry plans, retry acknowledgements, and redacted connector delivery metadata. They do not include connector tokens, private URLs, customer secrets, Enterprise source code, private policy packs, or license server logic. Credential rotation, ticket mutation, chat updates, and customer-specific recovery side effects remain private connector or operator runbook responsibilities.

## User Stories

- As a release manager, I can require approval before failed audit delivery is retried live.
- As a platform owner, I can see which retry decisions are approved and which are still waiting.
- As a SOC analyst, I can classify repeated SIEM delivery failures into a recovery playbook.
- As an auditor, I can trace failed delivery, retry acknowledgement, execution approval, and recovery guidance without exposing secrets.

## Enterprise Challenge Solved

Enterprise release governance needs a hard boundary between planning a retry and executing a retry. This phase makes live retry execution approval-bound and gives operations teams a consistent recovery playbook when delivery failures repeat across SIEM, ITSM, ChatOps, or webhook destinations.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-retry-approvals-recovery-playbooks.svg`.

## Next Work

The next recommended implementation step is approval-bound live retry execution records and connector recovery closure evidence.
