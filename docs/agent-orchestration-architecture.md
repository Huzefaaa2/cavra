# Agent Orchestration Architecture

CAVRA's transparent engineering-agent model is designed as a governed GitHub-native delivery loop. GitHub provides the collaboration surface. CAVRA provides pre-action enforcement, policy evaluation, evidence, and approval gates. The orchestrator routes work but does not bypass CAVRA decisions.

## Architecture

```mermaid
flowchart LR
    Human[Human Owner] --> Issue[GitHub Issue]
    Issue --> PM[Product Manager Agent]
    PM --> Architect[Architect Agent]
    Architect --> Dev[Backend or Frontend Agent]
    Dev --> Branch[agent/{role}/{issue-slug} Branch]
    Branch --> PR[Pull Request]
    PR --> Test[Test Agent]
    PR --> Security[Security Agent]
    PR --> Docs[Documentation Agent]
    Test --> Reviewer[Reviewer Agent]
    Security --> Reviewer
    Docs --> Reviewer
    Reviewer --> Approval[Human Maintainer Approval]
    Approval --> Release[Release Agent]
    Release --> Notes[Release Notes and Wiki]

    CAVRA[CAVRA Runtime Authority] --> PM
    CAVRA --> Architect
    CAVRA --> Dev
    CAVRA --> Test
    CAVRA --> Security
    CAVRA --> Docs
    CAVRA --> Reviewer
    CAVRA --> Release

    CAVRA --> Policy[Policy Packs]
    CAVRA --> Evidence[Evidence Hub]
    CAVRA --> Approvals[Approval Gates]
```

## Control Plane

The control plane contains:

- GitHub Issues, labels, PRs, reviews, branch protection, and Actions.
- Declarative agent manifests in `.github/agents/`.
- Issue templates that collect objective, acceptance criteria, scope, risk, and evidence requirements.
- Documentation and wiki pages that keep users, reviewers, and buyers aligned.

## Enforcement Plane

CAVRA evaluates agent actions before execution:

- File reads and writes.
- Shell commands.
- Git operations.
- MCP tool calls.
- Policy changes.
- Evidence creation.
- Approval requirements.

The current implementation is Python-based. The Go enforcement plane remains on the roadmap for lower latency local enforcement, CI runner enforcement, and air-gapped single-binary deployments.

## Orchestrator Responsibilities

A future orchestrator service should:

- Listen to GitHub issue, label, comment, PR, and release events.
- Map labels such as `agent:backend` or `agent:security` to declared manifests.
- Open branches with the `agent/{role}/{issue-slug}` convention.
- Run each agent through CAVRA action evaluation.
- Attach CAVRA evidence to PRs.
- Request human approval when a manifest or policy requires it.
- Stop rather than continue when CAVRA blocks or requires approval.

The orchestrator should not own policy decisions. CAVRA owns policy decisions.

## GitHub Actions Responsibilities

The current `Transparent Agent Orchestrator` workflow is intentionally conservative. It validates manifest presence and publishes a governance summary. It does not autonomously modify source code.

Future workflow extensions can:

- Sync `.github/labels.yml` labels.
- Validate branch naming.
- Verify PR attestations.
- Require docs/wiki/diagram updates for user-facing changes.
- Upload CAVRA evidence bundles as artifacts.

## Human Approval Gates

Human approval is required for:

- Protected branch merge.
- Security settings changes.
- CI workflow permission changes.
- Policy relaxations.
- Runtime allow/block semantic changes.
- Release publication.
- Package publication.
- Public roadmap, pricing, licensing, or compliance claims.

## Diagram Asset

The user-facing architecture diagram is maintained at `docs/diagrams/agent-orchestration.svg` and mirrored into the GitHub Wiki.
