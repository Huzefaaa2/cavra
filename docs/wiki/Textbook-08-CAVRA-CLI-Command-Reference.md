# CAVRA CLI Command Reference

The `cavra` CLI is the main command surface for local users, automation, CI/CD, release workflows, and evidence operations.

![CAVRA command map](assets/textbook/cavra-command-map.svg)

For every command and option generated directly from Typer help output, see
[CAVRA Full CLI Reference](CLI-Reference.md). This chapter groups the commands
by job-to-be-done.

## Core Commands

```bash
cavra version
cavra evaluate <action> <resource>
```

Use `cavra evaluate` to ask CAVRA whether an action should proceed.

Practical examples:

```bash
cavra evaluate read_file .env --json
cavra evaluate write_file iam/admin-role.tf --json
cavra evaluate execute_command "terraform apply -auto-approve" --json
cavra evaluate git_operation origin/main --json
cavra evaluate mcp_tool_call unknown-filesystem --json
```

Expected outcomes under the starter baseline:

| Command | Why you run it | Typical decision |
| --- | --- | --- |
| `read_file .env` | Confirm secrets are protected. | Block |
| `write_file iam/admin-role.tf` | Test identity/IAM change control. | Requires approval |
| `execute_command "terraform plan"` | Confirm safe planning can proceed. | Allow |
| `execute_command "terraform apply -auto-approve"` | Confirm destructive unattended execution is stopped. | Block |
| `git_operation origin/main` | Confirm branch protection is respected. | Block |
| `mcp_tool_call unknown-filesystem` | Confirm untrusted tool calls are blocked. | Block |

## Agent Commands

```bash
cavra agent start
cavra agent exec
cavra agent attest
```

Use these commands to run governed agent sessions and produce attestations.

## Policy Commands

```bash
cavra policy list
cavra policy validate
cavra policy test
cavra policy explain
cavra policy sign
cavra policy verify
```

Use policy commands to manage policy packs and confirm that rules behave as expected.

Policy authoring loop:

```bash
cavra policy init --destination .cavra/policy.yaml
cavra policy validate .cavra/policy.yaml
cavra policy test --policy-pack cavra-ai-agent-baseline
cavra policy explain execute_command "terraform apply -auto-approve"
cavra policy keygen
cavra policy sign .cavra/policy.yaml --signer platform-security --private-key .cavra/policy-signing/local-policy-signing-key.private.pem --key-id local-policy-signing-key
cavra policy verify .cavra/policy.yaml --public-key .cavra/policy-signing/local-policy-signing-key.public.pem
```

Use `validate` for schema correctness, `test` for expected behavior, `explain` for human-readable reasoning, and `sign`/`verify` when the policy will be used in stricter governance workflows.

## Approval Commands

```bash
cavra approval create
cavra approval list
cavra approval approve
cavra approval deny
cavra approval expire
cavra approval break-glass
cavra approval route
cavra approval migrate
cavra approval export-notifications
cavra approval provider-requests
cavra approval deliver
```

Approval commands turn high-risk decisions into auditable human or external-provider workflows.

Approval example:

```bash
cavra evaluate write_file iam/admin-role.tf --json > /tmp/cavra-decision.json
cavra approval create /tmp/cavra-decision.json --requested-by developer
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Scoped IAM change reviewed"
```

Use approval routing when the action may be legitimate but should not proceed without a named human, reason, and review record.

## Evidence Commands

```bash
cavra evidence generate-keypair
cavra evidence trust-root .cavra/keys/evidence-ed25519-public.pem --key-id local-evidence-key
cavra evidence trust-bundle .cavra/keys/evidence-trust-root.json
cavra evidence trust-distribution
cavra evidence bundle
cavra evidence verify
cavra evidence verify-attestation
cavra evidence siem-event
cavra evidence export-siem
cavra evidence retention-policy
cavra evidence storage-plan
cavra evidence migrate
cavra evidence index
cavra evidence search
```

Evidence commands produce and validate the proof that CAVRA decisions were made and enforced.

Evidence example:

```bash
cavra evidence generate-keypair
cavra evidence trust-root .cavra/keys/evidence-ed25519-public.pem --key-id local-evidence-key
cavra evidence bundle --output .cavra/evidence/latest --private-key .cavra/keys/evidence-ed25519-private.pem --key-id local-evidence-key
cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-root.json
cavra evidence siem-event .cavra/evidence/latest
```

Use evidence commands whenever decisions must feed CI/CD gates, audit, SIEM export, AISPM, or report delivery.

## Registry Commands

```bash
cavra registry agent-register
cavra registry agent-list
cavra registry profiles
cavra registry mcp-register
cavra registry mcp-list
cavra registry mcp-check
cavra registry mcp-classifications
cavra registry migrate
```

Registry commands manage governed agent identities and MCP trust records.

MCP trust example:

```bash
cavra registry mcp-register github-mcp --trust-tier approved --approval-state approved --capability repository --tool create_pull_request
cavra registry mcp-check github-mcp create_pull_request --capability repository
```

Use the registry when a tool call is more important than a file operation. CAVRA should know which MCP servers are trusted, what capabilities they expose, and whether a tool is allowed for the current action.

## Operations Commands

```bash
cavra ops stores
cavra ops backup
cavra ops restore
cavra ops retention-plan
```

Operations commands support persistence, backup, restore, and retention planning.

## Runtime And Release Commands

Runtime and release commands cover Go backend operations, rollback rehearsals, endpoint rollout, package verification, channel promotion, endpoint reconciliation, remediation, SLA reporting, and connector delivery. These commands are advanced and should be used with the detailed [CLI](CLI.md), [Go Backend Deployment Readiness](Go-Backend-Deployment-Readiness.md), and [Release Security Advisories](Release-Security-Advisories.md) pages.

## Demo And Setup Commands

```bash
cavra init claude-code
cavra demo before-the-agent-acts
```

Use these commands to initialize Claude Code integration and run the flagship demonstration.

The fastest CLI learning path is:

```bash
cavra demo before-the-agent-acts
cavra policy explain execute_command "terraform apply -auto-approve"
cavra evidence bundle --output .cavra/evidence/latest --private-key .cavra/keys/evidence-ed25519-private.pem --key-id local-evidence-key
cavra evidence verify .cavra/evidence/latest
```

## Check Your Understanding

1. Which command explains a policy decision before you change the policy?
2. Which command family proves evidence after an action is evaluated?
3. Why should CLI examples be run against the same policy pack used in CI/CD?

## What's Next

Read [CAVRA GUI And Sandbox Guide](Textbook-09-CAVRA-GUI-And-Sandbox-Guide.md) to see the same runtime story in the visual product surface.
