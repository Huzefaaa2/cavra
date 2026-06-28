# CAVRA CLI Command Reference

The `cavra` CLI is the main command surface for local users, automation, CI/CD, release workflows, and evidence operations.

![CAVRA command map](assets/textbook/cavra-command-map.svg)

For the complete generated command list, see [CLI](CLI). This chapter groups the commands by job-to-be-done.

## Core Commands

```bash
cavra version
cavra evaluate <action> <resource>
```

Use `cavra evaluate` to ask CAVRA whether an action should proceed.

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

## Evidence Commands

```bash
cavra evidence generate-keypair
cavra evidence trust-root
cavra evidence trust-bundle
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

## Operations Commands

```bash
cavra ops stores
cavra ops backup
cavra ops restore
cavra ops retention-plan
```

Operations commands support persistence, backup, restore, and retention planning.

## Runtime And Release Commands

Runtime and release commands cover Go backend operations, rollback rehearsals, endpoint rollout, package verification, channel promotion, endpoint reconciliation, remediation, SLA reporting, and connector delivery. These commands are advanced and should be used with the detailed [CLI](CLI), [Go Backend Deployment Readiness](Go-Backend-Deployment-Readiness), and [Release Security Advisories](Release-Security-Advisories) pages.

## Demo And Setup Commands

```bash
cavra init claude-code
cavra demo before-the-agent-acts
```

Use these commands to initialize Claude Code integration and run the flagship demonstration.
