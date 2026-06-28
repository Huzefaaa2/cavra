# The Runtime Authority Model

CAVRA is built on a runtime authority model. The runtime authority is the control layer that evaluates agent actions before execution and produces evidence after evaluation.

![CAVRA runtime authority map](assets/textbook/cavra-runtime-authority-map.svg)

## Actors

CAVRA models several kinds of actors:

- AI coding agents that propose file edits, shell commands, Git operations, or tool calls.
- Human operators who approve, deny, or break glass.
- MCP servers and tools that expose external capabilities to agents.
- CI/CD runners that enforce policy in automated delivery paths.
- Enterprise connectors that deliver evidence, notifications, incidents, tickets, or reports.

## Actions

CAVRA evaluates actions rather than vague intent. Example action families include:

- `read_file`, `write_file`, and repository modifications.
- Shell commands and high-risk command patterns.
- Git operations, branch protection changes, and pull request activity.
- MCP tool calls against repositories, filesystems, cloud tools, ticketing systems, or custom tools.
- Infrastructure and cloud changes through Terraform, OpenTofu, Kubernetes, GitHub, IAM, or deployment workflows.
- Evidence generation, report delivery, and release governance tasks.

## Decisions

A CAVRA decision tells the calling workflow what should happen next.

| Decision | Meaning |
| --- | --- |
| `allow` | The action can proceed and evidence should be recorded. |
| `deny` | The action is blocked because policy does not permit it. |
| `requires_approval` | The action needs a human or external approval route. |
| `shadow` | The action is observed and recorded without hard enforcement. |
| `break_glass` | An emergency path is used with explicit justification and evidence. |

## Authority Sources

CAVRA can evaluate decisions from several inputs:

- Static policy packs.
- Repository and file metadata.
- Runtime action payloads.
- Agent registry records.
- MCP trust registry records.
- OIDC identity claims and RBAC mappings.
- Approval store state.
- Evidence and attestation history.
- Enterprise tenant, connector, and entitlement state.

## Anti-Bypass Design

CAVRA treats bypass risk as a first-class design problem. The runtime authority model assumes agents may try alternate tools, indirect file paths, generated scripts, shell wrappers, or CI/CD side channels. CAVRA therefore documents anti-bypass principles in [AI Agent Enforcement And Anti-Bypass Model](AI-Agent-Enforcement-And-Anti-Bypass-Model) and uses evidence to detect whether expected gates were used.

## Control Loop

The runtime authority loop is:

1. Agent proposes an action.
2. CAVRA normalizes the action into a decision request.
3. Policy, identity, registry, and approval context are evaluated.
4. A decision is returned.
5. Approved execution or blocked activity is recorded.
6. Evidence is signed, indexed, searched, exported, or transformed into AISPM posture.

This loop is the heart of the product.
