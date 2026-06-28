# Foreword, Preface, And Reader Paths

## Foreword

AI agents are becoming operating actors inside engineering organizations. They read source code, propose patches, run shell commands, open pull requests, call MCP tools, trigger CI/CD jobs, and increasingly touch infrastructure and cloud configuration. The important question is no longer whether agents can act. The question is who governs them at the moment they try to act.

CAVRA is built for that moment. It is a runtime authority layer that sits between an agent and the action it wants to perform. It evaluates intent, context, policy, identity, approval state, and evidence requirements before the action proceeds. CAVRA is not just a scanner and not just a dashboard. It is a control point.

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

- [Install And Deploy CAVRA](Textbook-05-Install-And-Deploy-CAVRA)
- [Community Edition User Guide](Textbook-06-Community-Edition-User-Guide)
- [CAVRA CLI Command Reference](Textbook-08-CAVRA-CLI-Command-Reference)
- [CAVRA GUI And Sandbox Guide](Textbook-09-CAVRA-GUI-And-Sandbox-Guide)

Enterprise evaluators should read:

- [Enterprise Edition User Guide](Textbook-07-Enterprise-Edition-User-Guide)
- [AISPM Guide](Textbook-10-AISPM-Guide)
- [Operations, Integrations, And Deployment Patterns](Textbook-12-Operations-Integrations-And-Deployment-Patterns)
- [Use Cases, Labs, And Example Workflows](Textbook-13-Use-Cases-Labs-And-Example-Workflows)

Security architects should read:

- [Why CAVRA Exists](Textbook-01-Why-CAVRA-Exists)
- [The Runtime Authority Model](Textbook-02-Runtime-Authority-Model)
- [Policies, Approvals, Evidence, And Attestations](Textbook-11-Policies-Approvals-Evidence-And-Attestations)
- [Reference Appendices](Textbook-14-Reference-Appendices)

## Book Structure

Each chapter includes references to product pages, diagrams, examples, or screenshots. The wiki keeps historical development artifacts in [Development And Testing Artifacts](Development-And-Testing-Artifacts/Index), while this book remains the reader-facing product guide.
