# CAVRA User Stories

## Developer

As a developer using Claude Code, I want CAVRA to block secret reads before they enter agent context, so I can use AI coding assistance without leaking `.env`, keys, kubeconfig, or state files.

As a developer, I want `terraform plan` to be allowed and `terraform apply -auto-approve` to be blocked, so safe planning remains fast while production changes remain controlled.

As a developer, I want CAVRA to generate a PR attestation automatically, so reviewers can understand what the agent attempted and what CAVRA allowed or blocked.

## CISO

As a CISO, I want one decision point for AI-agent engineering actions, so I can adopt coding agents without surrendering control over secrets, infrastructure, production changes, and audit evidence.

As a CISO, I want CAVRA policy packs mapped to PCI DSS, HIPAA, SOX, NIST SSDF, ISO 27001, EU AI Act, and OWASP LLM risks, so governance is explainable in enterprise risk language.

## Platform Engineering

As a platform engineer, I want reusable policy packs and repository overrides, so teams can adopt AI agents with a common enterprise safety floor.

As a platform engineer, I want Docker, API, CLI, and future Go enforcement modes, so CAVRA can run locally, in CI, self-hosted, or air-gapped.

As a platform engineer, I want the console to validate signed OIDC bearer tokens and show repository-scoped permissions, so browser-visible actions use the same identity boundary as approval workflows.

As a platform engineer, I want to preview policy drafts and rollout changes before applying them, so policy adoption is controlled and reviewable.

As a platform engineer, I want a production readiness report, so missing identity, RBAC, CORS, evidence, policy, or persistence controls are visible before rollout.

## DevSecOps

As a DevSecOps engineer, I want GitHub required checks and SIEM exports, so CAVRA decisions become part of existing SDLC controls.

As a DevSecOps engineer, I want CI to fail when CAVRA evidence or PR attestation verification fails, so AI-assisted changes cannot merge without verifier-ready proof.

As a DevSecOps engineer, I want signed policy and evidence bundles, so audit artifacts can be trusted after the fact.

## Auditor

As an auditor, I want session evidence that includes agent identity, action, decision, policy, rule, reason, timestamp, and correlation ID, so I can reconstruct what happened.

As an auditor, I want downloadable PR attestation and compliance mapping, so AI-assisted changes can be reviewed against regulated control objectives.

As an auditor, I want to download the full allowlisted evidence artifact bundle for an indexed session, so I can attach verifiable CAVRA evidence to audit requests and change records.

## AI Governance Lead

As an AI governance lead, I want an Agent Registry and MCP Trust Registry, so AI agents and tools are known, approved, scoped, and monitored.

As an AI governance lead, I want unknown MCP filesystem servers blocked, so prompt-injection-induced tool misuse cannot silently expand agent capability.
