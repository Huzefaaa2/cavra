# Implementation Guide: AI Agent Governance for Enterprises

This guide provides step-by-step instructions for implementing CAVRA in regulated enterprise environments.

## 1. Local developer machine setup

### Prerequisites
- Python 3.10+
- Git
- AI coding agent (Claude Code, GitHub Copilot, Cursor, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/Huzefaaa2/cavra
cd cavra

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install CAVRA
pip install -e .
```

### Initialize a workspace

```bash
# Start a governed session
cavra agent start \
  --tool claude-code \
  --repo . \
  --policy-pack cavra-banking-baseline \
  --output .cavra/audit
```

### Test the runtime guard

```bash
# This should be blocked
cavra agent exec "terraform apply" \
  --policy-pack cavra-terraform-prod

# This should be allowed
cavra agent exec "terraform plan" \
  --policy-pack cavra-terraform-prod
```

---

## 2. GitHub Actions integration

### Add CAVRA to your CI/CD

For a complete required-check template, copy `examples/github-actions/cavra-required-check.yml` into `.github/workflows/cavra-required-check.yml`. The template validates the selected policy pack, verifies the evidence bundle, verifies the PR attestation, and uploads CAVRA evidence as a workflow artifact.

Minimal workflow:

```yaml
name: CAVRA Required Check

on:
  pull_request:

jobs:
  cavra:
    name: cavra-required-check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install CAVRA
        run: pip install cavra
      - name: Verify CAVRA policy and evidence
        run: |
          cavra policy validate policies/cavra-agentic-delivery/policy.yaml
          cavra evidence verify .cavra/evidence/latest --key "$CAVRA_EVIDENCE_SIGNING_KEY"
          cavra evidence verify-attestation .cavra/evidence/latest --output .cavra/evidence/attestation
```

Set the GitHub branch protection required status check to `cavra-required-check`. For stricter regulated repositories, use `examples/github-actions/cavra-enterprise-enforcement.yml` with trust-root verification, key IDs, and minimum retention thresholds. GitLab users can start from `examples/gitlab-ci/cavra-required-check.gitlab-ci.yml`.

---

## 3. SIEM integration (Splunk)

### Configure webhook

```bash
export TERRAGUARD_WEBHOOK_URL=https://your-splunk-instance.com/services/collector/event \
  -H "Authorization: Splunk your-hec-token"
```

### Create Splunk input

In Splunk, create an HTTP Event Collector input:

```
Settings → Data Inputs → HTTP Event Collector
Create New Token: cavra
Source Type: cavra:audit
Index: security
```

### Send evidence

```bash
cavra agent exec "terraform plan" \
  --webhook-url "https://your-splunk-instance.com:8088/services/collector/event" \
  --policy-pack cavra-banking-baseline
```

Splunk will automatically ingest:
```
session_id=abc123
tool=claude-code
actions=5
blocked_actions=2
required_approvals=1
```

---

## 4. Jira integration

### Create Jira webhook

In Jira, set up a webhook to receive CAVRA evidence:

```
Project Settings → Automation → Webhook
URL: https://your-jira-instance.com/rest/api/2/issue/
Auth: Basic (Jira API token)
```

### Jira linking function

Create `jira_integration.py`:

```python
import requests
from cavra.audit import SessionAudit

def link_to_jira(audit: SessionAudit, jira_url: str, api_token: str, project_key: str):
    """Link AI governance evidence to a Jira ticket."""
    
    if any(action.decision == "block" for action in audit.actions):
        severity = "High"
    elif any(action.decision == "require_approval" for action in audit.actions):
        severity = "Medium"
    else:
        severity = "Low"
    
    issue = {
        "fields": {
            "project": {"key": project_key},
            "issuetype": {"name": "Task"},
            "summary": f"AI Agent Governance Review: {audit.tool}",
            "description": f"Session: {audit.session_id}\nSeverity: {severity}\n\n" +
                          "\n".join(f"- {a.type}: {a.target} ({a.decision})" for a in audit.actions),
            "labels": ["ai-governance", "cavra"],
        }
    }
    
    response = requests.post(
        f"{jira_url}/rest/api/2/issue",
        json=issue,
        auth=(api_token.split(":")[0], api_token.split(":")[1]),
    )
    return response.status_code == 201
```

---

## 5. ServiceNow integration

### Configure change request

Create a ServiceNow flow that creates change requests from AI governance evidence:

```bash
# Export as JSON for ServiceNow API
cavra agent attest <session-id> \
  --format json | \
  curl -X POST \
    -H "Content-Type: application/json" \
    -d @- \
    "https://your-servicenow-instance.service-now.com/api/now/table/change_request" \
    -u admin:password
```

---

## 6. Policy pack customization

### Create your organization's policy

`policies/org-custom-ai/policy.yaml`:

```yaml
metadata:
  id: org-custom-ai
  title: ACME Corp AI Governance
  description: Custom policy for ACME regulated workloads
  version: 1.0.0

filesystem:
  block_read:
    - ".env"
    - "**/*secrets*"
    - "**/credentials/**"
  require_approval_write:
    - "**/iam/**"
    - "**/security/**"

commands:
  block:
    - "terraform apply*"
    - "kubectl delete*"
  allow:
    - "terraform plan*"
    - "git*"

git:
  require_pull_request: true
  require_human_reviewer: true
  require_ai_attestation: true
```

### Load in CI/CD

```bash
cavra agent start \
  --tool claude-code \
  --repo . \
  --policy-pack cavra-ai-agent-baseline \
  --policy-pack org-custom-ai
```

---

## 7. Enterprise deployment

### Architecture

```
Developer Workstation
  └─ Claude Code / Copilot / Cursor
     └─ CAVRA CLI
        └─ Session Audit → .cavra/
           └─ GitHub (PR comment + artifact)
           └─ SIEM webhook (Splunk)
           └─ Jira (linked issues)
           └─ ServiceNow (change requests)
```

### Deployment checklist

- [ ] Install CAVRA on dev workstations (via Homebrew or pip)
- [ ] Configure organization policy pack in `.cavra/policy.yaml`
- [ ] Set up GitHub Actions workflow for PR attestation
- [ ] Configure SIEM webhook URL in CI/CD environment variables
- [ ] Create Jira integration function in your automation engine
- [ ] Set up ServiceNow change request sync
- [ ] Publish policy pack documentation to internal wiki
- [ ] Train developers on `cavra agent` commands
- [ ] Monitor audit logs for policy violations
- [ ] Iterate on policies based on blocked actions

---

## 8. Monitoring and metrics

### Key metrics to track

```
cavra.agent.sessions_started
cavra.agent.actions_total
cavra.agent.actions_allowed
cavra.agent.actions_blocked
cavra.agent.actions_requiring_approval

Breakdown by:
  - tool (claude-code, copilot, cursor, duo)
  - policy_pack (cavra-ai-agent-baseline, cavra-banking-baseline, cavra-terraform-prod)
  - decision (allow, block, require_approval)
```

### Health check

```bash
# Test that cavra is running and policies are loaded
cavra policy list
# Should return all available policy packs
```

---

## 9. Security considerations

- Store `.cavra/` audit logs in a secure location
- Rotate webhook URLs and API tokens regularly
- Enforce HTTPS for all webhook connections
- Use signed YAML policy bundles (future feature)
- Monitor audit logs for suspicious patterns
- Periodically review and update policies

---

## Support and troubleshooting

### Common issues

**Issue**: `Policy pack not found`
```bash
# Solution: Verify the policy pack exists
cavra policy list
```

**Issue**: Command not intercepted as expected
```bash
# Solution: Check the runtime pattern matching
cavra policy describe <pack-id>
```

**Issue**: Webhook not sending evidence
```bash
# Solution: Verify webhook URL is reachable
curl -X POST <webhook-url> -d '{"test": "ok"}'
```

### Get help

- GitHub Issues: https://github.com/Huzefaaa2/cavra/issues
- LinkedIn: https://www.linkedin.com/in/huzefaaa
