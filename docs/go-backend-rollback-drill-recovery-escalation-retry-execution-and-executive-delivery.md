# Go Backend Rollback Drill Recovery Escalation Retry Execution And Executive Delivery

CAVRA now automates the next recovery escalation operations step: dry-run-by-default retry execution for failed recovery escalation deliveries and connector delivery for scheduled executive recovery reports.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-worker-run` runs a public-safe recovery escalation retry worker.
- Non-dry-run escalation retry execution persists immutable execution records bound to the worker run, escalation plan, provider, delivery metadata, and execution status.
- Live escalation retry execution requires a prior accepted, acknowledged, or resolved recovery escalation acknowledgement for the provider.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-runs/{run_id}/deliver` delivers scheduled executive report summaries through configured connectors.
- Evidence Console now includes **Run Escalation Retry** and **Deliver Executive Report** actions.
- Rollback drill dashboards now count recovery escalation retry worker runs, retry execution records, executive report delivery attempts, and failed executive report deliveries.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Build and deliver a recovery escalation plan.
2. Record provider acknowledgement for the escalation.
3. Create a recovery escalation retry plan if delivery failed.
4. Run **Run Escalation Retry** in dry-run mode first.
5. Use the API with `execute=true` only after the escalation acknowledgement is accepted and connector configuration is ready.
6. Schedule an executive report and deliver the scheduled report summary through a configured connector.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-worker-run
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-runs/{run_id}/deliver
```

Retry worker request fields:

- `dry_run`: defaults to `true` unless `execute=true` is supplied.
- `execute`: enables live retry execution when `true`.
- `max_retry_deliveries`: caps selected retry attempts.
- `retry_policy.max_retry_attempts`
- `retry_policy.retry_delay_minutes`
- `retry_policy.allow_immediate_retry`
- `retry_policy.backoff_multiplier`
- `schedule.interval_minutes`
- `schedule.cadence`

Executive delivery request fields:

- `provider`: connector provider such as `webhook`, `slack`, `teams`, `jira`, or `servicenow`.
- `retries`
- `timeout_seconds`
- `max_risks`: caps key risks included in the public-safe delivery payload.

## Security Boundary

The worker and delivery event only use public-safe CAVRA metadata. Connector credentials remain in runtime connector configuration and are not serialized into evidence records. The public Community repository contains no Enterprise source code, customer incident payloads, private policy packs, connector secrets, or license server logic.

## User Stories

- As a release manager, I can retry failed recovery escalation delivery only after an operator acknowledgement exists.
- As a platform owner, I can dry-run the retry worker before any live connector side effect.
- As an executive stakeholder, I can receive scheduled recovery report summaries through approved channels.
- As an auditor, I can verify retry worker selection, execution status, and executive report delivery from one evidence timeline.

## Enterprise Challenge Solved

Recovery escalation workflows need a controlled way to retry failed notifications and deliver leadership reporting without exposing connector secrets or private incident data. This phase creates that operating loop with auditable, public-safe records.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-recovery-escalation-retry-execution-and-executive-delivery.svg`.

## Next Work

Recovery escalation retry health reporting and executive report delivery retry planning are now covered in `docs/go-backend-rollback-drill-recovery-retry-health-and-executive-delivery-retry.md`.
