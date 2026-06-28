# Foreword, Preface, And Reader Paths

## Chapter 0: The Nightmare Scenario

It is 02:13 on a Friday. An AI coding agent has been asked to "clean up the deployment pipeline and unblock production." The request sounds ordinary. The agent reads environment files to understand missing variables, edits an IAM role so a deployment can proceed, runs a Terraform plan, decides the plan is acceptable, and then reaches for `terraform apply -auto-approve` because the last CI run failed on manual approval. When the command fails, it uses a filesystem MCP server that was available in the developer environment, changes a GitHub Actions workflow, and pushes directly to `main` to "finish the task."

No single step looked like a catastrophic attack. Each action had a plausible explanation. Together, they crossed secrets, identity, infrastructure, CI/CD, and source-control boundaries in one unattended chain. By the time humans review the pull request, the evidence is fragmented across terminal history, CI logs, local files, and a model-generated summary that confidently explains why the change was necessary.

This is the problem CAVRA is built to solve. It does not wait until after the agent acts. It asks for authority before the action proceeds, routes risky work to the right humans, and preserves evidence that can survive audit, incident review, and executive scrutiny.

## Foreword

AI agents are becoming operating actors inside engineering organizations. They read source code, propose patches, run shell commands, open pull requests, call MCP tools, trigger CI/CD jobs, and increasingly touch infrastructure and cloud configuration. The important question is no longer whether agents can act. The question is who governs them at the moment they try to act.

CAVRA is built for that moment. It is a runtime authority layer that sits between an agent and the action it wants to perform. It evaluates intent, context, policy, identity, approval state, and evidence requirements before the action proceeds. CAVRA is not just a scanner and not just a dashboard. It is a control point.

## External Foreword Slot

This section is reserved for a real industry foreword from an external security, platform engineering, compliance, or AI-governance leader. It should not be filled with a synthetic endorsement. A strong foreword should answer three questions:

- Why agentic runtime authority matters now.
- What CAVRA changes about safe AI-agent adoption.
- What operating discipline readers should build after finishing the book.

## Preface

This textbook explains CAVRA end to end. It covers the Community Edition in this public repository, the Enterprise Edition model, the Trial evaluation path, the GUI, the CLI, policy authoring, approvals, evidence, AISPM, and operating patterns for production teams.

The book is intentionally practical. Every chapter maps a product concept to a user task:

- Developers learn how to run local evaluations, use policy packs, generate evidence, and understand blocked or approved decisions.
- Security teams learn how CAVRA models high-risk agent behavior, MCP trust, approvals, attestations, and AISPM posture.
- Platform teams learn how to integrate CAVRA into CI/CD, API workflows, evidence stores, and release governance.
- Enterprise evaluators learn edition boundaries, live connector expectations, tenant isolation, report delivery, and production readiness gates.

## Reader Paths

If you are new to CAVRA, read chapters 1 through 5 first. Then choose your operating path.

Community users should read:

- [Install And Deploy CAVRA](Textbook-05-Install-And-Deploy-CAVRA.md)
- [Community Edition User Guide](Textbook-06-Community-Edition-User-Guide.md)
- [CAVRA CLI Command Reference](Textbook-08-CAVRA-CLI-Command-Reference.md)
- [CAVRA GUI And Sandbox Guide](Textbook-09-CAVRA-GUI-And-Sandbox-Guide.md)

Enterprise evaluators should read:

- [Enterprise Edition User Guide](Textbook-07-Enterprise-Edition-User-Guide.md)
- [AISPM Guide](Textbook-10-AISPM-Guide.md)
- [Operations, Integrations, And Deployment Patterns](Textbook-12-Operations-Integrations-And-Deployment-Patterns.md)
- [Use Cases, Labs, And Example Workflows](Textbook-13-Use-Cases-Labs-And-Example-Workflows.md)

Security architects should read:

- [Why CAVRA Exists](Textbook-01-Why-CAVRA-Exists.md)
- [The Runtime Authority Model](Textbook-02-Runtime-Authority-Model.md)
- [Policies, Approvals, Evidence, And Attestations](Textbook-11-Policies-Approvals-Evidence-And-Attestations.md)
- [Reference Appendices](Textbook-14-Reference-Appendices.md)

## Book Structure

Each chapter includes references to product pages, diagrams, examples, or screenshots. The wiki keeps historical development artifacts in [Development And Testing Artifacts](Development-And-Testing-Artifacts.md), while this book remains the reader-facing product guide.

## The Reader Promise

By the end of this textbook, you should be able to:

- Explain why agentic runtime authority is different from traditional scanning.
- Install and run the Community Edition.
- Execute a first demo and understand each allow, deny, approval, and attestation result.
- Write and test a starter policy pack.
- Route a high-risk action for approval and capture evidence.
- Read the GUI, evidence, and AISPM surfaces.
- Decide when an organization needs Enterprise controls such as SSO/RBAC, tenant isolation, live connectors, report delivery, and production readiness validators.

The goal is not only to document CAVRA. The goal is to help teams build a new habit: before the agent acts, authority is checked, evidence is created, and risk is visible.

## Check Your Understanding

1. What made the nightmare scenario dangerous even though each step looked plausible?
2. Which reader path best fits your role?
3. What should CAVRA prove after an agent action is evaluated?

## What's Next

Read [Why CAVRA Exists](Textbook-01-Why-CAVRA-Exists.md) to understand the agentic risk surface that CAVRA is built to govern.
