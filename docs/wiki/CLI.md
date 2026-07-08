# CAVRA CLI Guide

The `cavra` CLI is the main automation surface for Community users, CI/CD jobs,
release operators, and evidence workflows.

For every command and every option generated directly from Typer help output, use
the authoritative reference:

- [CAVRA Full CLI Reference](CLI-Reference.md)
- [GitHub-style CAVRA CLI Manual](CLI-Manual.md)

## Core Command Families

| Family | Purpose |
| --- | --- |
| `cavra version` | Print the installed CAVRA version. |
| `cavra evaluate` | Evaluate a file, command, Git, or MCP/tool action before it happens. |
| `cavra agent` | Start governed sessions, execute commands, and generate attestations. |
| `cavra policy` | List, validate, test, explain, compile, diff, sign, and verify policies. |
| `cavra approval` | Create, route, approve, deny, expire, break-glass, and deliver approval requests. |
| `cavra evidence` | Bundle, sign, verify, export, index, search, and manage evidence. |
| `cavra registry` | Register and check governed agents and MCP/tool trust metadata. |
| `cavra ops` | Inspect, back up, restore, and plan retention for local stores. |
| `cavra runtime` | Validate Go/runtime pilot, deployment, promotion, rollback, and drill readiness. |
| `cavra release` | Run release, endpoint, roadmap, Managed/Enterprise, customer-lifecycle, and governance validators. |
| `cavra aispm` | Validate AISPM review and CI-gate readiness packets. |
| `cavra monitor` | Generate and replay monitoring events. |
| `cavra benchmark` | Run benchmark/SLO regression readiness checks. |
| `cavra adapter` | Validate action taxonomy and generic agent adapter manifests. |
| `cavra ai-red-team` | Run public-safe guardrail, supply-chain, malicious-model, and readiness checks. |
| `cavra deployment` | Generate and validate zero-trust deployment catalogs. |

## Five-Minute CLI Path

```bash
cavra version
cavra policy list
cavra evaluate read_file .env --json
cavra evaluate execute_command "terraform apply -auto-approve" --json
cavra demo before-the-agent-acts
```

## Policy Authoring Loop

```bash
cavra policy init --destination .cavra/policy.yaml
cavra policy validate .cavra/policy.yaml
cavra policy test --policy-pack cavra-ai-agent-baseline
cavra policy explain execute_command "terraform apply -auto-approve"
cavra policy keygen
cavra policy sign .cavra/policy.yaml --signer platform-security --private-key .cavra/policy-signing/local-policy-signing-key.private.pem --key-id local-policy-signing-key
cavra policy verify .cavra/policy.yaml --public-key .cavra/policy-signing/local-policy-signing-key.public.pem
```

## Approval Loop

```bash
cavra evaluate write_file iam/admin-role.tf --json > /tmp/cavra-decision.json
cavra approval create /tmp/cavra-decision.json --requested-by developer
cavra approval route /tmp/cavra-decision.json
cavra approval list --state pending
cavra approval approve apr_123 --actor platform-security --reason "Scoped IAM change reviewed"
```

## Evidence Loop

```bash
cavra evidence bundle --output .cavra/evidence/latest
cavra evidence verify .cavra/evidence/latest
cavra evidence export-siem .cavra/evidence/latest --output .cavra/evidence/siem
cavra evidence index .cavra/evidence/latest --sqlite .cavra/evidence/metadata.db
cavra evidence search --sqlite .cavra/evidence/metadata.db --min-blocked 1 --limit 25
```

## Managed/Enterprise Public-Safe Validators

Managed and Enterprise live operations use sanitized manifest and evidence refs.
Do not commit private tenant, SMTP, connector, license, or customer data.

```bash
cavra release managed-enterprise-live-validation-plan --require-live
cavra release managed-enterprise-cutover-runbook --require-live
cavra release managed-enterprise-operating-chain --require-live
cavra release roadmap-governance-quickcheck --repo-root . --require-live
```

## Notes

- Use `--help` on any command for local help.
- Use [CAVRA Full CLI Reference](CLI-Reference.md) for complete command options.
- Use [GitHub-style CAVRA CLI Manual](CLI-Manual.md) when you want one page per command, similar to GitHub CLI manual pages.
- Use [Public Documentation Map](Public-Documentation-Map.md) to find user guides,
  release evidence, and archive material.
