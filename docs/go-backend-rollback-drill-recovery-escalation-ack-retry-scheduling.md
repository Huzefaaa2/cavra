# Go Backend Rollback Drill Recovery Escalation Acknowledgements And Scheduling

CAVRA now adds operator acknowledgement, retry planning, and scheduled executive reporting around recovery escalation notifications.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/acknowledgements` records public-safe review state for a recovery escalation provider.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-plan` creates retry plans for failed recovery escalation connector delivery attempts.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-run` generates a scheduled executive recovery report run and persists the report metadata.
- Evidence Console now includes **Ack Recovery Escalation**, **Plan Escalation Retry**, and **Schedule Executive Report** controls.
- Rollback drill dashboards now count recovery escalation acknowledgements, retry plans, retryable escalation deliveries, and scheduled executive report runs.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Build a recovery escalation plan.
2. Deliver the recovery escalation notification through a configured connector.
3. Acknowledge the escalation for the target provider with a change, incident, or ticket reference.
4. Build a retry plan if escalation delivery failed.
5. Run the scheduled executive report action to persist leadership reporting evidence.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/acknowledgements
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-plan
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-run
```

Acknowledgement request fields:

- `provider`: escalation provider, such as `webhook`, `slack`, `teams`, `jira`, or `servicenow`.
- `acknowledged_by`: actor label when signed console actor context is not available.
- `acknowledgement_state`: `acknowledged`, `accepted`, `deferred`, `escalated`, `resolved`, or `dismissed`.
- `external_ref`: public-safe change, incident, or ticket reference.
- `notes`: public-safe operator notes.

Retry plan request fields:

- `retry_policy.max_retry_attempts`
- `retry_policy.retry_delay_minutes`
- `retry_policy.allow_immediate_retry`
- `retry_policy.backoff_multiplier`

Scheduled executive report request fields:

- `recovery_slo_minutes`: public-safe recovery SLO threshold.
- `schedule.interval_minutes`
- `schedule.cadence`
- `schedule.enabled`

## Security Boundary

Acknowledgements, retry plans, and scheduled report runs are derived from public-safe recovery escalation and connector delivery metadata. They do not include connector credentials, private ticket payloads, customer incident text, Enterprise source code, private policy packs, or license server logic.

## User Stories

- As a release manager, I can prove a recovery escalation was reviewed and accepted by the responsible provider.
- As a platform owner, I can plan retries for failed recovery escalation delivery without embedding connector secrets in public code.
- As an executive stakeholder, I can receive scheduled recovery status evidence.
- As an auditor, I can trace escalation, acknowledgement, retry planning, and executive reporting from one evidence stream.

## Enterprise Challenge Solved

Escalation workflows are not complete until teams prove who reviewed the escalation, which delivery failures require retry, and when leadership reporting was generated. This phase closes that governance loop with public-safe evidence records.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-recovery-escalation-ack-retry-scheduling.svg`.

## Next Work

Automated recovery escalation retry execution and scheduled executive report delivery are now covered in `docs/go-backend-rollback-drill-recovery-escalation-retry-execution-and-executive-delivery.md`.
