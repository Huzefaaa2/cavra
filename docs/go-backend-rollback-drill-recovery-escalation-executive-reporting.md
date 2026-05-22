# Go Backend Rollback Drill Recovery Escalation And Executive Reporting

CAVRA now turns retry recovery SLO evidence into recovery escalation notifications and executive reporting for promoted Go backend rollback drill operations.

## What This Adds

- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan` builds a public-safe escalation plan from retry execution records, connector recovery playbooks, and recovery closure evidence.
- `POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/deliver` routes escalation events through configured connectors and persists redacted delivery evidence.
- `GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report` creates a leadership-ready report with status, business impact, key risks, provider summaries, closure trends, and recommended actions.
- Evidence Console now includes controls for planning recovery escalation, delivering recovery escalation, and building executive recovery reports.
- Rollback drill dashboards now count recovery escalation plans, escalation routes, and executive reports.

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
2. Plan, acknowledge, approve, and execute retry work.
3. Generate and close connector recovery playbooks.
4. Review the **Retry Recovery SLO** table.
5. Select **Plan Recovery Escalation** for failed executions or open/breached recoveries.
6. Select **Deliver Recovery Escalation** to notify the configured operations channel.
7. Select **Executive Recovery Report** for leadership-ready recovery status.

## API

```text
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan
POST /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/deliver
GET /runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report
```

Escalation plan request fields:

- `recovery_slo_minutes`: public-safe recovery SLO threshold. Defaults to `240`.
- `generated_by`: actor label. Defaults to `console`.

Escalation delivery request fields:

- `provider`: connector provider such as `webhook`, `slack`, `teams`, `jira`, or `servicenow`.
- `retries`: connector retry count.
- `timeout_seconds`: connector timeout.
- `max_routes`: maximum public-safe escalation rows to include.

Executive report query parameters:

- `recovery_slo_minutes`: public-safe recovery SLO threshold. Defaults to `240`.
- `generated_by`: report actor label. Defaults to `console`.

## Security Boundary

Recovery escalation plans and executive reports are derived only from public-safe metadata. They do not include connector credentials, private ticket payloads, customer incident text, Enterprise source code, private policy packs, or license server logic. Connector delivery uses the existing configured connector boundary and persists only redacted delivery metadata.

## User Stories

- As a release manager, I can escalate failed retry execution and open recovery work before promotion readiness is affected.
- As a platform owner, I can deliver recovery escalation notifications to the right operations channel.
- As an executive stakeholder, I can read a concise recovery status report without needing raw connector or ticket details.
- As an auditor, I can trace retry recovery reports, escalation plans, delivery attempts, and executive reports as public-safe evidence.

## Enterprise Challenge Solved

Regulated engineering teams need proof that failed recovery work is escalated, visible, and closed. This phase converts retry recovery evidence into operational notification workflows and leadership reporting while preserving the open-core security boundary.

## Diagram

See `docs/diagrams/go-backend-rollback-drill-recovery-escalation-executive-reporting.svg`.

## Next Work

The next recommended implementation step is automated recovery escalation retry execution and scheduled executive report delivery.
