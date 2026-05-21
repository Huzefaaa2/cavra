# Recurrence Automation Deployment

CAVRA recurrence automation turns indexed endpoint remediation escalation metadata into retry plans, owner digests, suppression trend evidence, and worker-run history. The worker is public-safe in Community Edition: dry-run is the default, connector delivery requires an explicit execute flag, and connector credentials are loaded only from deployment-specific secret stores.

## Deployment Templates

Reference templates:

- GitHub Actions: `examples/github-actions/cavra-recurrence-automation.yml`
- Kubernetes CronJob: `examples/kubernetes/cavra-recurrence-automation-cronjob.yaml`
- systemd timer: `examples/systemd/cavra-recurrence-automation.service`, `examples/systemd/cavra-recurrence-automation.timer`, and `examples/systemd/cavra-recurrence-automation.env.example`

All templates run:

```bash
cavra release endpoint-remediation-sla-escalation-recurrence-automation \
  --metadata-json .cavra/evidence/metadata.json \
  --sqlite .cavra/evidence/metadata.db \
  --schedule-interval-minutes 30 \
  --dry-run \
  --json
```

Manual execute mode adds `--execute --config <connector-config> --provider <provider>`. Use execute mode only after reviewing the latest dry-run payload and confirming connector configuration, owner routing, and maintenance-window policies.

## GitHub Actions

Copy `examples/github-actions/cavra-recurrence-automation.yml` into `.github/workflows/` in the repository where recurrence evidence is produced.

The scheduled trigger runs every 30 minutes in dry-run mode. Manual `workflow_dispatch` can run execute mode when `execute=true` and a repository secret named `CAVRA_CONNECTORS_JSON` is configured.

Operational notes:

- Keep scheduled runs in dry-run mode.
- Use manual execute mode for controlled owner digest delivery.
- Upload `.cavra/evidence/` and `.cavra/release/endpoint-remediation-sla-escalation-recurrence-automation/` artifacts for audit review.
- Store long-lived metadata in a durable evidence store when runners are ephemeral.

## Kubernetes CronJob

Apply `examples/kubernetes/cavra-recurrence-automation-cronjob.yaml` after creating a persistent volume claim named `cavra-state`.

The CronJob mounts:

- `/var/lib/cavra` for evidence metadata and worker outputs.
- Optional secret `cavra-connectors` at `/etc/cavra/connectors`.

Dry-run mode is controlled by:

```yaml
- name: CAVRA_RECURRENCE_EXECUTE
  value: "false"
```

Set it to `"true"` only for a controlled deployment that has the `cavra-connectors` secret mounted with `connectors.json`. Keep `concurrencyPolicy: Forbid` so overlapping workers do not deliver duplicate owner digests.

## systemd Timer

Install the systemd example on a self-hosted Linux worker:

```bash
sudo useradd --system --home-dir /var/lib/cavra --shell /usr/sbin/nologin cavra || true
sudo install -d -o cavra -g cavra -m 0750 /var/lib/cavra
sudo install -d -o root -g root -m 0750 /etc/cavra
sudo install -o root -g root -m 0644 examples/systemd/cavra-recurrence-automation.service /etc/systemd/system/
sudo install -o root -g root -m 0644 examples/systemd/cavra-recurrence-automation.timer /etc/systemd/system/
sudo install -o root -g root -m 0640 examples/systemd/cavra-recurrence-automation.env.example /etc/cavra/recurrence-automation.env
sudo systemctl daemon-reload
sudo systemctl enable --now cavra-recurrence-automation.timer
```

Review status and logs:

```bash
systemctl status cavra-recurrence-automation.timer
journalctl -u cavra-recurrence-automation.service -n 100 --no-pager
```

## Connector Configuration

Connector config must be supplied by the deployment platform:

- GitHub Actions: `CAVRA_CONNECTORS_JSON` repository secret.
- Kubernetes: `cavra-connectors` secret with `connectors.json`.
- systemd: `/etc/cavra/connectors.json` with root-managed permissions.

Do not commit connector config to the public repository. The templates fail execute mode when connector config is missing.

## Rollback and Disable

Disable scheduled execution without deleting evidence:

- GitHub Actions: disable the workflow or remove the scheduled trigger.
- Kubernetes: suspend the CronJob with `kubectl patch cronjob cavra-recurrence-automation -p '{"spec":{"suspend":true}}'`.
- systemd: run `sudo systemctl disable --now cavra-recurrence-automation.timer`.

Rollback execute mode by setting `CAVRA_RECURRENCE_EXECUTE=false` and rerunning a dry-run. Review the Evidence Console Worker Runs table or run:

```bash
cavra release endpoint-remediation-sla-escalation-recurrence-automation-history \
  --metadata-json .cavra/evidence/metadata.json
```

## Health Reporting

After the scheduler is running, monitor missed runs, stale metadata, failed job records, and owner digest connector failures:

```bash
cavra release endpoint-remediation-sla-escalation-recurrence-automation-health \
  --metadata-json .cavra/evidence/metadata.json \
  --expected-interval-minutes 30 \
  --stale-metadata-minutes 120
```

The Evidence Console Recurrence Operations panel shows the same health status, missed-run count, failed-job count, stale metadata count, connector failure count, and latest-run age from `/endpoint-remediation-sla-escalation-recurrence-automations/health`.

## Health Alert Delivery

Unhealthy recurrence automation status can now be routed to configured webhook, Slack, Teams, Jira, or ServiceNow connectors with duplicate suppression and acknowledgement tracking:

```bash
cavra release deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert \
  --config .cavra/connectors.json \
  --provider all \
  --metadata-json .cavra/evidence/metadata.json \
  --json
```

Acknowledgements are indexed separately so release-governance owners can prove review without storing connector secrets:

```bash
cavra release ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert erslah_123 \
  --provider slack \
  --acknowledged-by release-manager \
  --metadata-json .cavra/evidence/metadata.json \
  --json
```

Use `endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history` and `endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard` to inspect delivery attempts, duplicate suppression, failed providers, and outstanding acknowledgements.

## User Stories

- As a release manager, I can schedule recurrence automation safely in dry-run mode before delivering owner digests.
- As a platform engineer, I can deploy the worker to GitHub Actions, Kubernetes, or Linux hosts using public-safe templates.
- As an auditor, I can inspect worker history, dry-run status, executed status, retryable routes, digests, and suppression events from persisted evidence.
- As a release-governance owner, I can route unhealthy scheduler signals to ITSM or ChatOps and record acknowledgement evidence.

## Enterprise Challenge Solved

Enterprises need repeatable remediation follow-up without turning scheduled jobs into hidden automation. These templates make recurrence automation observable, dry-run-first, and easy to disable while still supporting controlled connector delivery when operators explicitly enable execution.

## Next Recommendation

Add an explicitly opt-in Go enforcement backend pilot with audited fallback to Python and parity-gate evidence.
