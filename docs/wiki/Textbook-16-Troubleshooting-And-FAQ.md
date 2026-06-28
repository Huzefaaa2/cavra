# Troubleshooting And FAQ

This chapter turns the troubleshooting decision tree into a field playbook. Use it when a command, policy, GUI page, evidence bundle, connector, or AISPM readiness packet does not behave as expected.

![Troubleshooting decision tree](assets/textbook/troubleshooting-decision-tree.svg)

## Triage First

Start with four questions:

1. Is the issue in the decision, the enforcement point, the evidence, or the reporting layer?
2. Can you reproduce it with the CLI?
3. Does `cavra policy explain` match the decision you expected?
4. Is the evidence fresh, signed, and tied to the action you are investigating?

## Decision Problems

| Symptom | Likely cause | First command | Fix |
| --- | --- | --- | --- |
| Safe action is denied | Rule is too broad or default is deny. | `cavra policy explain <action> <target>` | Add a narrower allow rule before the broad rule. |
| Risky action is allowed | Missing path, command, branch, or MCP rule. | `cavra policy explain <action> <target>` | Add explicit deny or approval routing. |
| Approval expected but not created | Rule returns `allow` or `deny`. | `cavra evaluate <action> <target> --json` | Change decision to `requires_approval` and define route. |
| Shadow mode records but does not block | Policy mode is `shadow`. | Inspect policy `mode`. | Move to `enforce` after rollout validation. |

## Evidence Problems

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `cavra evidence verify` fails | Missing trust root, wrong key ID, stale signature, or altered bundle. | Verify trust root path and key ID before regenerating evidence. |
| Evidence does not mention policy | Decision was generated without policy pack metadata. | Re-run evaluation with the intended policy pack loaded. |
| Evidence exists but CI fails | CI reads a different bundle path. | Align CI path, bundle output, and PR attestation configuration. |
| Evidence is stale | Bundle was generated before the current release or decision. | Regenerate evidence and rerun readiness checks. |

## Approval Problems

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Pending request is not visible | Wrong store, route, tenant, or state filter. | Run `cavra approval list --state pending`. |
| Approval expired too quickly | Route TTL is too short for the workflow. | Adjust `expires_after` for the route. |
| Break glass looks like a bypass | Missing reason, actor, or incident reference. | Require break-glass justification and review it after the incident. |
| Provider delivery failed | Connector or credentials failed. | Preserve failed delivery evidence and retry through approved provider settings. |

## GUI And Sandbox Problems

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Page loads but data looks old | Browser cache or static sample state. | Hard refresh and confirm the correct local build or hosted page. |
| Screenshot does not match docs | Local sandbox is from a different commit. | Rebuild or serve the current `apps/sandbox-ui` content. |
| AISPM page shows sample data | Public sandbox is intentionally public-safe. | Use Enterprise live ingestion for tenant-specific production posture. |
| Export button produces public sample packet | Running Community sandbox, not Enterprise tenant workflow. | Use Enterprise report delivery validators for real delivery evidence. |

## Connector And SMTP Problems

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| SMTP validation fails authentication | Wrong username, password, app password, host, port, or TLS mode. | Confirm provider settings and use environment variables or a secret store. |
| Report sent but not received | Recipient policy, spam filtering, DNS, or provider delay. | Check provider delivery logs and recipient mailbox. |
| SIEM or ITSM event missing | Connector endpoint, token, or payload schema mismatch. | Validate connector payload against the public contract and preserve failed audit evidence. |
| Secret appears in logs | Redaction is incomplete. | Stop the run, rotate the secret, and fix redaction before rerunning. |

## AISPM Readiness Problems

| Blocker | What it means | Closeout action |
| --- | --- | --- |
| Missing live connector evidence | Synthetic fixtures were used instead of real providers. | Run connector validation with approved real settings. |
| Tenant isolation unproven | Tenant data boundaries were not tested. | Run isolation checks with at least two real tenant scopes. |
| Runtime workflow synthetic only | Validators did not see real agent/tool execution. | Run file, command, Git, MCP, approval, and evidence workflows through CAVRA. |
| Report delivery unverified | Report packet was generated but not delivered and audited. | Send to approved recipients and capture delivery audit evidence. |
| Evidence stale | Evidence predates the release or pilot decision. | Regenerate source evidence and rerun final readiness gate. |

## FAQ

### Is CAVRA only for AI coding agents?

No. Coding agents are the most visible use case, but the model applies to any agentic workflow that can touch files, shell, Git, cloud, CI/CD, MCP tools, reports, or operating systems.

### Does CAVRA replace code review?

No. CAVRA evaluates runtime authority before action and produces evidence. Code review, SAST, SCA, secrets scanning, CSPM, IAM governance, and incident response still matter.

### Why did CAVRA block a command that a human can run?

CAVRA is governing agent authority, not human shell access in general. A command may be legitimate for a human with context but too risky for unattended agent execution.

### Can Community Edition prove production readiness?

Community Edition can teach the model, enforce local decisions, and create evidence. Full production readiness still requires Enterprise validation for real connectors, tenants, report delivery, identity, and runtime workflows.

### Can I use animated diagrams in the wiki?

Yes, where GitHub renders SVG image assets. The diagrams in this textbook are SVG-native and degrade to static diagrams when animation is disabled by browser settings or renderer policy.

## Check Your Understanding

1. What is the first command to run when a decision surprises you?
2. Why should failed connector deliveries still produce evidence?
3. What does an AISPM readiness blocker usually mean?
4. Why is stale evidence not enough for a production gate?

## What's Next

Finish with [Conclusion: The Runtime Authority Revolution](Textbook-17-The-Runtime-Authority-Revolution.md), which turns the technical model into an operating call to action.
