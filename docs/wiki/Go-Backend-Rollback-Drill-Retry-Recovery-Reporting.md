# Go Backend Rollback Drill Retry Recovery Reporting

CAVRA now provides retry execution dashboards, recovery SLO reporting, and closure trend analytics for acknowledgement audit delivery recovery.

## What This Adds

- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report` builds a public-safe report from retry execution records, connector recovery playbooks, and recovery closures.
- Provider-level summaries show retry execution count, delivered count, failed or skipped count, recovery playbook count, closure count, open recovery count, SLO breaches, latest execution, and latest closure.
- Recovery SLO rows show each provider playbook, current closure state, open or closed status, age, closure minutes, and SLO breach state.
- Closure trend analytics aggregate daily closure states and provider counts without exposing private ticket contents or connector credentials.
- Evidence Console now includes a **Retry Recovery SLO** table alongside drill notification history, escalation routes, routing history, and suppression summaries.

## How To Use

Start the API and sandbox UI:

```bash
cavra api
cd apps/sandbox-ui
python3 -m http.server 5173
```

Open `http://127.0.0.1:5173/index.html` and use the **Go Rollback Drill Notifications** section.

Recommended operator flow:

1. Deliver an acknowledgement audit package.
2. Plan and acknowledge audit delivery retry work.
3. Approve and execute live retry work.
4. Generate a connector recovery playbook.
5. Close recovery with verification evidence.
6. Review **Retry Recovery SLO** to see open recoveries, breached SLOs, failed executions, and closure status by provider.

## API

```text
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report
```

Query parameters:

- `recovery_slo_minutes`: public-safe recovery SLO threshold. Defaults to `240`.
- `generated_by`: report actor label. Defaults to `console`.

The endpoint returns:

- `report`: retry execution and recovery SLO analytics.
- `metadata`: persisted public-safe report metadata with kind `go-backend-rollback-drill-acknowledgement-audit-delivery-retry-recovery-report`.

## Report Fields

- `execution_count`
- `execution_success_count`
- `execution_failed_count`
- `execution_success_rate`
- `execution_status_counts`
- `recovery_playbook_provider_count`
- `recovery_closed_count`
- `recovery_open_count`
- `recovery_slo_breached_count`
- `closure_state_counts`
- `provider_summary`
- `recovery_rows`
- `closure_trends`
- `latest_executions`

## Security Boundary

Reports are derived only from public-safe execution records, recovery playbooks, and closure metadata. They do not include connector secrets, private URLs, customer incident notes, Enterprise source code, private policy packs, private ticket payloads, or license server logic.

## User Stories

- As a release manager, I can see which approved retries failed or succeeded by provider.
- As a platform owner, I can identify open connector recovery work and breached recovery SLOs.
- As a SOC analyst, I can track closure trends without exposing private ticket contents.
- As an auditor, I can review retry execution, recovery state, and closure proof from a single report.

## Enterprise Challenge Solved

Enterprise recovery work often stalls after a retry is executed. This phase turns retry execution and connector recovery closure metadata into operational reporting so teams can manage recovery SLOs, provider reliability, and audit readiness from one surface.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-retry-recovery-reporting.svg`.

## Next Work

The next recommended implementation step is automated recovery escalation notifications and executive reporting.
