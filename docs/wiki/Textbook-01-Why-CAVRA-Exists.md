# Why CAVRA Exists

AI agents changed the software delivery threat model. Traditional application security tools inspect source code, dependencies, infrastructure definitions, and runtime services. Those tools are still necessary, but they do not govern the agent while it is operating.

An agent can combine many small actions into a high-impact workflow. It can inspect a repository, infer secrets from context, edit an IAM policy, run a shell command, call a deployment tool, change a GitHub workflow, and write persuasive justification in a pull request. Without a runtime authority layer, each step may look harmless while the workflow as a whole becomes risky.

## The New Risk Surface

CAVRA is designed around the risk that agentic systems create:

- Agents can act faster than review processes.
- Agents can cross boundaries between code, shell, cloud, Git, MCP, and CI/CD.
- Agents can generate plausible explanations for unsafe changes.
- Agents can operate through tools that were never designed for autonomous use.
- Agents can create evidence gaps when actions happen outside approved workflows.

The core problem is not that agents are malicious. The core problem is that an agent can be over-authorized, under-observed, or insufficiently constrained.

## The CAVRA Answer

CAVRA introduces a runtime decision point before meaningful action. It asks:

- Who or what is acting?
- What operation is being attempted?
- Which repository, file, environment, identity, tool, or cloud object is affected?
- Which policy applies?
- Does this require human approval?
- What evidence must be generated?
- Should this be allowed, denied, shadowed, or routed for review?

![Runtime flow](assets/textbook/runtime-flow.svg)

## Why AISPM Matters

Runtime decisions are useful individually. They become more valuable when aggregated into posture. AISPM, AI Security Posture Management, turns CAVRA evidence into questions executives and operators can answer:

- Which agents are covered?
- Which tools are trusted?
- Which controls are enforced?
- Which findings remain open?
- Which reports are ready for security, compliance, or board review?
- Which blockers prevent a trial, pilot, or production launch?

CAVRA therefore covers both sides of the problem: pre-action enforcement and post-action posture.

## What CAVRA Is Not

CAVRA is not a replacement for code review, SAST, DAST, SCA, secrets scanning, cloud posture management, IAM governance, or incident response. CAVRA works alongside those systems. Its unique role is runtime authority for agentic workflows.

If traditional tools answer "what is wrong with the artifact?", CAVRA answers "should this agent be allowed to perform this action right now, and what evidence proves the decision?"
