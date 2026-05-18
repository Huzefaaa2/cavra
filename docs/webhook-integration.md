# Webhook Integration

CAVRA can export audit evidence and attestations to webhook endpoints for integration with SOC, GRC, and change management systems.

## Overview

Webhooks allow you to:
- Send audit evidence to SIEM or logging systems
- Notify approval systems of high-risk agent actions
- Trigger downstream compliance workflows
- Archive attestation evidence for audits

## Configuration

Set the webhook URL via environment variable:

```bash
export TERRAGUARD_WEBHOOK_URL=https://your-webhook-endpoint/events
```

Or pass it directly to the CLI:

```bash
cavra agent exec "terraform plan" \
  --webhook-url https://your-webhook-endpoint/events
```

## Event payload

All events are sent as JSON POST requests with this structure:

```json
{
  "session_id": "abc123def456",
  "tool": "claude-code",
  "repo": "/path/to/repo",
  "started_at": "2026-05-14T10:30:00Z",
  "actions": [
    {
      "type": "execute_command",
      "target": "terraform apply",
      "decision": "block",
      "reason": "Matched blocked command policy: terraform apply*"
    }
  ]
}
```

## Webhook receiver requirements

Your webhook receiver should:
- Accept POST requests with JSON body
- Return HTTP 200, 201, or 204 on success
- Handle requests within 10 seconds
- Log or process the evidence asynchronously

## Example SIEM integration

### Splunk

```python
def splunk_webhook(request):
    event = request.json
    # Send to Splunk HEC
    hec_client.send(
        event=event,
        source="cavra",
        sourcetype="cavra:audit"
    )
    return {"status": "ok"}, 200
```

### Datadog

```python
def datadog_webhook(request):
    event = request.json
    statsd.increment("cavra.agent.actions", tags=[
        f"tool:{event['tool']}",
        f"session:{event['session_id']}"
    ])
    return {"status": "ok"}, 200
```

## Error handling

If a webhook request fails:
- CAVRA logs the failure but does not block the agent session
- The local audit JSON is always persisted to `.cavra/`
- Consider implementing retry logic in your webhook handler
