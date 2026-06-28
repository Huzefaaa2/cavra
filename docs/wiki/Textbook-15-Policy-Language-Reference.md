# Policy Language Reference

This chapter is the compact reference for writing CAVRA policy packs. Earlier chapters show how policy fits into runtime authority. This chapter shows the policy shape, syntax, matching rules, and practical examples.

![Policy authoring journey](assets/textbook/policy-authoring-journey.svg)

## Policy Pack Shape

A CAVRA policy pack is a YAML document with identity, metadata, default behavior, rules, approval routes, evidence requirements, and optional test cases.

```yaml
id: cavra-ai-agent-baseline
version: 1.0.0
description: Baseline runtime authority policy for AI-assisted engineering.
mode: enforce

defaults:
  decision: deny
  evidence_required: true

actors:
  allowed_agent_profiles:
    - claude-code
    - codex
  human_approvers:
    - platform-security
    - release-manager

rules:
  - id: allow-safe-readme-edit
    action: write_file
    resources:
      - README.md
      - docs/**/*.md
    decision: allow
    evidence:
      level: standard

  - id: protect-identity-and-infra
    action: write_file
    resources:
      - iam/**
      - terraform/**
      - .github/workflows/**
    decision: requires_approval
    approval_route: production-change
    evidence:
      level: signed

  - id: block-dangerous-shell
    action: execute_command
    command_patterns:
      - "terraform apply -auto-approve*"
      - "kubectl delete namespace production*"
      - "rm -rf /"
    decision: deny
    evidence:
      level: signed

mcp_trust:
  allowed_servers:
    - github-mcp
  blocked_servers:
    - unknown-filesystem

approval_routes:
  production-change:
    required_approvers: 1
    approvers:
      - platform-security
      - release-manager
    expires_after: 8h
    require_reason: true

tests:
  - name: dangerous terraform apply is blocked
    action: execute_command
    target: "terraform apply -auto-approve"
    expect: deny
  - name: IAM write is approval routed
    action: write_file
    target: iam/admin-role.tf
    expect: requires_approval
```

## Top-Level Fields

| Field | Required | Purpose |
| --- | --- | --- |
| `id` | Yes | Stable policy pack identifier used in evidence and decisions. |
| `version` | Yes | Semantic policy version for audit and rollback. |
| `description` | Recommended | Human-readable policy purpose. |
| `mode` | Yes | `enforce`, `shadow`, or another supported runtime mode. |
| `defaults` | Recommended | Fallback decision and evidence posture when no rule matches. |
| `actors` | Optional | Agent profiles and human roles expected by the policy. |
| `rules` | Yes | Ordered runtime decision rules. |
| `mcp_trust` | Optional | MCP server trust and block rules. |
| `approval_routes` | Optional | Human or provider-backed approval routes. |
| `tests` | Recommended | Policy examples that can be validated repeatedly. |

## Rule Matching

Rules should be specific enough to explain the decision. CAVRA policies usually match by:

- action family, such as `write_file`, `execute_command`, `git_operation`, or `mcp_tool_call`;
- resource path, such as `iam/**`, `.github/workflows/**`, or `docs/**/*.md`;
- command pattern, such as `terraform apply*` or `kubectl delete*`;
- Git branch or ref, such as `main`, `release/*`, or `origin/main`;
- MCP server, capability, and tool name;
- actor, profile, tenant, or approval state where available.

Rules are easiest to operate when they are ordered from specific to broad. A precise allow rule for `docs/**/*.md` should appear before a broad approval rule for repository writes.

## Decisions

| Decision | Use when |
| --- | --- |
| `allow` | The action is low risk and should proceed with evidence. |
| `deny` | The action is not permitted under the policy. |
| `requires_approval` | The action may be legitimate but needs human or provider-backed approval. |
| `shadow` | The action should be observed without hard enforcement during rollout. |
| `break_glass` | Emergency action is allowed only with explicit justification and audit trail. |

## Evidence Requirements

Evidence policy should say what proof is required after the decision.

| Evidence level | Typical use |
| --- | --- |
| `standard` | Local development, low-risk decisions, learning labs. |
| `signed` | Protected branches, infrastructure, identity, CI/CD, and release workflows. |
| `delivery_audit` | Reports, connector delivery, SMTP/provider validation, ticketing, and incident workflows. |
| `retained` | Compliance, trial evidence rooms, production readiness, and customer operating archives. |

## Policy Authoring Workflow

Use this loop for any new policy:

```bash
cavra policy init --destination .cavra/policy.yaml
cavra policy validate .cavra/policy.yaml
cavra policy explain execute_command "terraform apply -auto-approve"
cavra policy test --policy-pack cavra-ai-agent-baseline
cavra policy sign .cavra/policy.yaml --private-key .cavra/keys/policy-ed25519-private.pem --output .cavra/policy.yaml.sig
cavra policy verify .cavra/policy.yaml --signature .cavra/policy.yaml.sig --public-key .cavra/keys/policy-ed25519-public.pem
```

## Common Recipes

### Protect Production Infrastructure

```yaml
- id: route-production-infra
  action: write_file
  resources:
    - terraform/prod/**
    - kubernetes/prod/**
    - iam/**
  decision: requires_approval
  approval_route: production-change
```

### Block Dangerous Commands

```yaml
- id: block-destructive-commands
  action: execute_command
  command_patterns:
    - "rm -rf /*"
    - "kubectl delete namespace production*"
    - "terraform apply -auto-approve*"
  decision: deny
```

### Govern MCP Tools

```yaml
mcp_trust:
  allowed_servers:
    - github-mcp
  approval_required:
    - filesystem-mcp
  blocked_servers:
    - unknown-filesystem
```

### Require Evidence For Pull Requests

```yaml
- id: require-pr-attestation
  action: git_operation
  resources:
    - main
    - release/*
  decision: requires_approval
  evidence:
    level: signed
    attest_pr: true
```

## Policy Review Checklist

- Does every high-risk resource have a rule?
- Are broad deny or allow patterns justified?
- Are production, identity, secrets, CI/CD, and MCP tool changes approval-routed?
- Does evidence include the policy pack ID and version?
- Are tests included for expected allow, deny, and approval decisions?
- Has the policy been validated, tested, signed, and verified?

## Check Your Understanding

1. Why should a policy route some actions for approval instead of denying them outright?
2. Which field gives auditors a stable identifier for the policy that made a decision?
3. What command explains why a specific action was blocked or allowed?
4. Why should policy tests include both safe and risky examples?

## What's Next

Next, read [Troubleshooting Playbook](Textbook-16-Troubleshooting-And-FAQ.md) to diagnose policy, evidence, connector, GUI, and AISPM issues in a production-like workflow.
