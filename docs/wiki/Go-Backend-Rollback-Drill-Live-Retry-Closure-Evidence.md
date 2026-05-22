# Go Backend Rollback Drill Live Retry Closure Evidence

CAVRA now records approval-bound live retry execution evidence and connector recovery closure evidence for acknowledgement audit delivery failures.

## What This Adds

- Non-dry-run acknowledgement audit retry workers persist `go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record` metadata for approved retry decisions.
- Retry execution records bind the worker run, retry plan, approval decision, delivery plan, connector delivery result, selected provider, and public evidence references.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbooks/{playbook_id}/closures` records resolved, mitigated, deferred, escalated, or reopened recovery outcomes.
- Rollback drill notification history and dashboard metrics now include retry execution records, execution success/failure counts, connector recovery closures, and closed recovery counts.
- Evidence Console actions for **Execute Retry** and **Close Recovery** complete the operator flow after retry approval and recovery playbook generation.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Use **Deliver Audit** to send an acknowledgement audit package through a configured connector.
2. Use **Plan Audit Retry** after a failed acknowledgement audit delivery.
3. Use **Ack Retry** to record retry review evidence.
4. Use **Plan Retry Approval** and **Approve Retry** before live retry execution.
5. Use **Execute Retry** to run the non-dry-run worker for approved retry decisions.
6. Use **Recovery Playbook** to generate connector recovery guidance for repeated failures.
7. Use **Close Recovery** to record the final recovery state, external ticket reference, and verification evidence.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbooks/{playbook_id}/closures
GET  /runtime/go-pilot/rollback-drill-notifications
GET  /runtime/go-pilot/rollback-drill-notifications/dashboard
```

Live retry workers support `retry_policy.allow_immediate_retry=true` for approved manual executions. The default delayed retry behavior remains unchanged when that flag is omitted.

Connector recovery closure states:

- `resolved`
- `mitigated`
- `deferred`
- `escalated`
- `reopened`

## Evidence Model

Retry execution records include:

- `execution_id` and `execution_hash`
- worker `run_id`
- retry `retry_plan_id`
- approval `approval_plan_id` and `approval_decision_id`
- target `delivery_id`, `audit_id`, and `provider`
- connector `delivery_success`, selected providers, skipped reason, and public evidence references

Recovery closure records include:

- `closure_id` and `closure_hash`
- `playbook_id`, provider, closure state, actor, timestamp, notes, external reference, and verification references
- controls proving that closure evidence is public-safe and secret-free

## Security Boundary

Live retry execution records do not contain connector credentials, private URLs, customer secrets, Enterprise source code, private policy packs, or license server logic. Recovery closures record public-safe operator outcomes only. Real ticket mutation, credential rotation, private incident metadata, and customer-specific connector recovery remain outside this public Community Edition.

## User Stories

- As a release manager, I can prove that live retry execution happened only after approval.
- As a platform owner, I can see whether approved retries were delivered, failed, or skipped.
- As a SOC analyst, I can close connector recovery work with verification evidence.
- As an auditor, I can trace failed delivery, retry acknowledgement, approval, execution, playbook, and closure records from one history view.

## Enterprise Challenge Solved

Regulated teams need retry execution to be auditable, approval-bound, and closed with evidence. This phase completes that chain without exposing connector secrets or proprietary recovery logic.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-live-retry-closure-evidence.svg`.

## Next Work

Automated recovery escalation retry execution and scheduled executive report delivery are now covered in [[Go Backend Rollback Drill Recovery Escalation Retry Execution And Executive Delivery]].
