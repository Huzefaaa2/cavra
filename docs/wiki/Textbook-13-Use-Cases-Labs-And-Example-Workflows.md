# Use Cases, Labs, And Example Workflows

This chapter gives practical ways to experience CAVRA.

## Lab 1: Block A Risky File Write

Goal: see runtime authority stop an unsafe agent change.

```bash
cavra evaluate write_file iam/admin-role.tf --json
```

Expected result: the decision explains whether the write is allowed, denied, or routed for approval. Use the result as input to an approval or evidence workflow.

## Lab 2: Approval-Routed Change

Goal: see human approval become part of the evidence chain.

```bash
cavra approval create /tmp/cavra-decision.json --requested-by developer
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Reviewed scoped production change"
```

Expected result: the approval record can be audited and referenced by later evidence.

## Lab 3: Evidence Bundle

Goal: create proof of governance.

```bash
cavra evidence bundle --output .cavra/evidence/latest
cavra evidence verify .cavra/evidence/latest
```

Expected result: evidence can be verified, indexed, searched, exported, or used by CI/CD.

## Lab 4: MCP Trust Check

Goal: govern tool calls, not just files.

```bash
cavra registry mcp-register github-mcp --trust-tier approved --approval-state approved --capability repository --tool create_pull_request
cavra registry mcp-check github-mcp create_pull_request --capability repository
```

Expected result: CAVRA has a record of which MCP tools are trusted for which actions.

## Lab 5: Sandbox Walkthrough

Goal: experience the GUI.

1. Start the sandbox.
2. Open Dashboard.
3. Run the flagship scenario.
4. Open Evidence.
5. Open AI Posture.
6. Export a public-safe readiness packet.

![AISPM desktop sentinel](assets/aispm-lab/aispm-desktop-sentinel.png)

## Lab 6: Enterprise Report Delivery Readiness

Goal: understand the production condition.

Enterprise users configure real tenant inputs, real connector credentials, SMTP or report provider settings, and runtime workflows. Then they run source validators and the final production gate. The completion condition is `ready_for_aispm_production: true` with no blockers.

## Use Case Map

| Use case | CAVRA surface |
| --- | --- |
| Local agent governance | CLI, policy, evidence |
| Pull request control | CLI, CI/CD, attestation |
| MCP tool governance | Agent registry, MCP trust registry |
| Cloud and IaC control | Policy engine, approvals, runtime decisions |
| Executive posture | AISPM, Report Center |
| Enterprise trial | Trial guide, labs, evidence room |
| Production readiness | Live validators, production gate |
