# CAVRA Full CLI Reference

Generated from Typer help output for CAVRA `1.0.0` on 2026-07-10.

This is the authoritative command reference for the public CAVRA CLI. If a shorter guide and this generated reference disagree, prefer this file and regenerate it from the current source tree.

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```

## Command Index

- [cavra](#cavra)
- [cavra agent](#cavra-agent)
- [cavra policy](#cavra-policy)
- [cavra demo](#cavra-demo)
- [cavra init](#cavra-init)
- [cavra integration](#cavra-integration)
- [cavra evidence](#cavra-evidence)
- [cavra approval](#cavra-approval)
- [cavra registry](#cavra-registry)
- [cavra ops](#cavra-ops)
- [cavra release](#cavra-release)
- [cavra runtime](#cavra-runtime)
- [cavra saas](#cavra-saas)
- [cavra aispm](#cavra-aispm)
- [cavra monitor](#cavra-monitor)
- [cavra benchmark](#cavra-benchmark)
- [cavra adapter](#cavra-adapter)
- [cavra ai-red-team](#cavra-ai-red-team)
- [cavra deployment](#cavra-deployment)
- [cavra setup](#cavra-setup)
- [cavra version](#cavra-version)
- [cavra ai-red-team guardrails](#cavra-ai-red-team-guardrails)
- [cavra ai-red-team supply-chain](#cavra-ai-red-team-supply-chain)
- [cavra ai-red-team malicious-model](#cavra-ai-red-team-malicious-model)
- [cavra ai-red-team export](#cavra-ai-red-team-export)
- [cavra ai-red-team readiness](#cavra-ai-red-team-readiness)
- [cavra ai-red-team packet](#cavra-ai-red-team-packet)
- [cavra adapter taxonomy](#cavra-adapter-taxonomy)
- [cavra adapter manifest-validate](#cavra-adapter-manifest-validate)
- [cavra adapter evaluate](#cavra-adapter-evaluate)
- [cavra adapter export](#cavra-adapter-export)
- [cavra adapter readiness](#cavra-adapter-readiness)
- [cavra deployment zero-trust-catalog](#cavra-deployment-zero-trust-catalog)
- [cavra deployment zero-trust-export](#cavra-deployment-zero-trust-export)
- [cavra deployment zero-trust-readiness](#cavra-deployment-zero-trust-readiness)
- [cavra benchmark export](#cavra-benchmark-export)
- [cavra benchmark run](#cavra-benchmark-run)
- [cavra benchmark readiness](#cavra-benchmark-readiness)
- [cavra monitor sample-events](#cavra-monitor-sample-events)
- [cavra monitor replay](#cavra-monitor-replay)
- [cavra monitor export](#cavra-monitor-export)
- [cavra monitor readiness](#cavra-monitor-readiness)
- [cavra aispm validate-review-packet](#cavra-aispm-validate-review-packet)
- [cavra aispm validate-ci-gate-readiness](#cavra-aispm-validate-ci-gate-readiness)
- [cavra evaluate](#cavra-evaluate)
- [cavra setup status](#cavra-setup-status)
- [cavra setup init](#cavra-setup-init)
- [cavra setup wizard](#cavra-setup-wizard)
- [cavra setup demo-env](#cavra-setup-demo-env)
- [cavra setup validate](#cavra-setup-validate)
- [cavra setup complete](#cavra-setup-complete)
- [cavra setup smtp](#cavra-setup-smtp)
- [cavra setup policy-actions](#cavra-setup-policy-actions)
- [cavra setup policy-action-test](#cavra-setup-policy-action-test)
- [cavra setup policy-action-plan](#cavra-setup-policy-action-plan)
- [cavra saas contract](#cavra-saas-contract)
- [cavra saas operating-automation](#cavra-saas-operating-automation)
- [cavra saas worker-handoff](#cavra-saas-worker-handoff)
- [cavra runtime go-pilot-readiness](#cavra-runtime-go-pilot-readiness)
- [cavra runtime go-deployment-readiness](#cavra-runtime-go-deployment-readiness)
- [cavra runtime go-promotion-readiness](#cavra-runtime-go-promotion-readiness)
- [cavra runtime go-rollback-readiness](#cavra-runtime-go-rollback-readiness)
- [cavra runtime go-rollback-rehearsal](#cavra-runtime-go-rollback-rehearsal)
- [cavra runtime go-rollback-drills](#cavra-runtime-go-rollback-drills)
- [cavra runtime go-rollback-drill-schedule](#cavra-runtime-go-rollback-drill-schedule)
- [cavra runtime go-rollback-drill-notification-plan](#cavra-runtime-go-rollback-drill-notification-plan)
- [cavra runtime go-rollback-drill-notification-ack](#cavra-runtime-go-rollback-drill-notification-ack)
- [cavra runtime go-rollback-drill-escalation-plan](#cavra-runtime-go-rollback-drill-escalation-plan)
- [cavra runtime go-pilot-evaluate](#cavra-runtime-go-pilot-evaluate)
- [cavra agent start](#cavra-agent-start)
- [cavra agent exec](#cavra-agent-exec)
- [cavra agent attest](#cavra-agent-attest)
- [cavra agent enforcement-readiness](#cavra-agent-enforcement-readiness)
- [cavra policy list](#cavra-policy-list)
- [cavra policy validate](#cavra-policy-validate)
- [cavra policy test](#cavra-policy-test)
- [cavra policy explain](#cavra-policy-explain)
- [cavra policy compile](#cavra-policy-compile)
- [cavra policy rego-export](#cavra-policy-rego-export)
- [cavra policy rego-test](#cavra-policy-rego-test)
- [cavra policy rego-readiness](#cavra-policy-rego-readiness)
- [cavra policy lifecycle-plan](#cavra-policy-lifecycle-plan)
- [cavra policy lifecycle-readiness](#cavra-policy-lifecycle-readiness)
- [cavra policy diff](#cavra-policy-diff)
- [cavra policy sign](#cavra-policy-sign)
- [cavra policy verify](#cavra-policy-verify)
- [cavra policy keygen](#cavra-policy-keygen)
- [cavra policy simulate](#cavra-policy-simulate)
- [cavra policy dry-run](#cavra-policy-dry-run)
- [cavra policy init](#cavra-policy-init)
- [cavra policy describe](#cavra-policy-describe)
- [cavra init claude-code](#cavra-init-claude-code)
- [cavra evidence bundle](#cavra-evidence-bundle)
- [cavra evidence generate-keypair](#cavra-evidence-generate-keypair)
- [cavra evidence trust-root](#cavra-evidence-trust-root)
- [cavra evidence trust-bundle](#cavra-evidence-trust-bundle)
- [cavra evidence trust-distribution](#cavra-evidence-trust-distribution)
- [cavra evidence verify](#cavra-evidence-verify)
- [cavra evidence siem-event](#cavra-evidence-siem-event)
- [cavra evidence retention-policy](#cavra-evidence-retention-policy)
- [cavra evidence export-siem](#cavra-evidence-export-siem)
- [cavra evidence storage-plan](#cavra-evidence-storage-plan)
- [cavra evidence verify-attestation](#cavra-evidence-verify-attestation)
- [cavra evidence index](#cavra-evidence-index)
- [cavra evidence search](#cavra-evidence-search)
- [cavra evidence migrate](#cavra-evidence-migrate)
- [cavra approval create](#cavra-approval-create)
- [cavra approval list](#cavra-approval-list)
- [cavra approval approve](#cavra-approval-approve)
- [cavra approval deny](#cavra-approval-deny)
- [cavra approval expire](#cavra-approval-expire)
- [cavra approval break-glass](#cavra-approval-break-glass)
- [cavra approval route](#cavra-approval-route)
- [cavra approval export-notifications](#cavra-approval-export-notifications)
- [cavra approval provider-requests](#cavra-approval-provider-requests)
- [cavra approval deliver](#cavra-approval-deliver)
- [cavra integration deliver](#cavra-integration-deliver)
- [cavra approval migrate](#cavra-approval-migrate)
- [cavra registry agent-register](#cavra-registry-agent-register)
- [cavra registry agent-list](#cavra-registry-agent-list)
- [cavra registry profiles](#cavra-registry-profiles)
- [cavra registry mcp-register](#cavra-registry-mcp-register)
- [cavra registry mcp-list](#cavra-registry-mcp-list)
- [cavra registry mcp-check](#cavra-registry-mcp-check)
- [cavra registry mcp-classifications](#cavra-registry-mcp-classifications)
- [cavra registry migrate](#cavra-registry-migrate)
- [cavra ops stores](#cavra-ops-stores)
- [cavra ops backup](#cavra-ops-backup)
- [cavra ops restore](#cavra-ops-restore)
- [cavra ops retention-plan](#cavra-ops-retention-plan)
- [cavra release phase6-rollup](#cavra-release-phase6-rollup)
- [cavra release phase4-closeout](#cavra-release-phase4-closeout)
- [cavra release phase5-closeout](#cavra-release-phase5-closeout)
- [cavra release customer-live-evidence](#cavra-release-customer-live-evidence)
- [cavra release customer-evidence-room](#cavra-release-customer-evidence-room)
- [cavra release customer-closeout-handoff](#cavra-release-customer-closeout-handoff)
- [cavra release customer-operating-review](#cavra-release-customer-operating-review)
- [cavra release customer-renewal-expansion](#cavra-release-customer-renewal-expansion)
- [cavra release customer-renewal-outcome](#cavra-release-customer-renewal-outcome)
- [cavra release customer-lifecycle-rollup](#cavra-release-customer-lifecycle-rollup)
- [cavra release customer-lifecycle-archive](#cavra-release-customer-lifecycle-archive)
- [cavra release customer-lifecycle-status](#cavra-release-customer-lifecycle-status)
- [cavra release customer-lifecycle-final-seal](#cavra-release-customer-lifecycle-final-seal)
- [cavra release customer-lifecycle-verification-index](#cavra-release-customer-lifecycle-verification-index)
- [cavra release managed-enterprise-live-validation-plan](#cavra-release-managed-enterprise-live-validation-plan)
- [cavra release managed-enterprise-cutover-runbook](#cavra-release-managed-enterprise-cutover-runbook)
- [cavra release managed-enterprise-stabilization-report](#cavra-release-managed-enterprise-stabilization-report)
- [cavra release managed-enterprise-steady-state-handoff](#cavra-release-managed-enterprise-steady-state-handoff)
- [cavra release managed-enterprise-operating-release-index](#cavra-release-managed-enterprise-operating-release-index)
- [cavra release managed-enterprise-operating-announcement](#cavra-release-managed-enterprise-operating-announcement)
- [cavra release managed-enterprise-operating-chain](#cavra-release-managed-enterprise-operating-chain)
- [cavra release managed-enterprise-operating-certificate](#cavra-release-managed-enterprise-operating-certificate)
- [cavra release managed-enterprise-certificate-publication-index](#cavra-release-managed-enterprise-certificate-publication-index)
- [cavra release roadmap-intake-gate](#cavra-release-roadmap-intake-gate)
- [cavra release roadmap-candidate-charter](#cavra-release-roadmap-candidate-charter)
- [cavra release roadmap-future-phase-opening-gate](#cavra-release-roadmap-future-phase-opening-gate)
- [cavra release roadmap-future-phase-registry](#cavra-release-roadmap-future-phase-registry)
- [cavra release roadmap-future-work-governance-index](#cavra-release-roadmap-future-work-governance-index)
- [cavra release roadmap-governance-quickcheck](#cavra-release-roadmap-governance-quickcheck)
- [cavra release customer-lifecycle-announcement](#cavra-release-customer-lifecycle-announcement)
- [cavra release customer-lifecycle-retrospective](#cavra-release-customer-lifecycle-retrospective)
- [cavra release customer-lifecycle-phase8-backlog](#cavra-release-customer-lifecycle-phase8-backlog)
- [cavra release customer-lifecycle-phase8-kickoff](#cavra-release-customer-lifecycle-phase8-kickoff)
- [cavra release customer-lifecycle-phase8-sprint1-checkpoint](#cavra-release-customer-lifecycle-phase8-sprint1-checkpoint)
- [cavra release customer-lifecycle-phase8-telemetry-depth](#cavra-release-customer-lifecycle-phase8-telemetry-depth)
- [cavra release customer-lifecycle-phase8-support-automation](#cavra-release-customer-lifecycle-phase8-support-automation)
- [cavra release customer-lifecycle-phase8-lifecycle-analytics](#cavra-release-customer-lifecycle-phase8-lifecycle-analytics)
- [cavra release customer-lifecycle-phase8-customer-health-review](#cavra-release-customer-lifecycle-phase8-customer-health-review)
- [cavra release customer-lifecycle-phase8-executive-health-rollup](#cavra-release-customer-lifecycle-phase8-executive-health-rollup)
- [cavra release customer-lifecycle-phase8-executive-action-plan](#cavra-release-customer-lifecycle-phase8-executive-action-plan)
- [cavra release customer-lifecycle-phase8-action-followup-checkpoint](#cavra-release-customer-lifecycle-phase8-action-followup-checkpoint)
- [cavra release customer-lifecycle-phase8-executive-followup-closeout](#cavra-release-customer-lifecycle-phase8-executive-followup-closeout)
- [cavra release customer-lifecycle-phase8-next-cycle-readiness-index](#cavra-release-customer-lifecycle-phase8-next-cycle-readiness-index)
- [cavra release customer-lifecycle-phase8-public-operating-scorecard](#cavra-release-customer-lifecycle-phase8-public-operating-scorecard)
- [cavra release customer-lifecycle-phase8-public-scorecard-publication-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-publication-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-refresh-checkpoint](#cavra-release-customer-lifecycle-phase8-public-scorecard-refresh-checkpoint)
- [cavra release customer-lifecycle-phase8-public-scorecard-refresh-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-refresh-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-operating-loop-index](#cavra-release-customer-lifecycle-phase8-public-scorecard-operating-loop-index)
- [cavra release customer-lifecycle-phase8-public-scorecard-executive-summary-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-executive-summary-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-distribution-readiness](#cavra-release-customer-lifecycle-phase8-public-scorecard-distribution-readiness)
- [cavra release customer-lifecycle-phase8-public-scorecard-distribution-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-distribution-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-distribution-audit-index](#cavra-release-customer-lifecycle-phase8-public-scorecard-distribution-audit-index)
- [cavra release customer-lifecycle-phase8-public-scorecard-audit-review-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-audit-review-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness](#cavra-release-customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness)
- [cavra release customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review](#cavra-release-customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review)
- [cavra release customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness](#cavra-release-customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness)
- [cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout)
- [cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review](#cavra-release-customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review)
- [cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout](#cavra-release-customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout)
- [cavra release verify-go-package](#cavra-release-verify-go-package)
- [cavra release verify-airgap-bundle](#cavra-release-verify-airgap-bundle)
- [cavra release validate-upgrade](#cavra-release-validate-upgrade)
- [cavra release smoke-installers](#cavra-release-smoke-installers)
- [cavra release channel-manifest](#cavra-release-channel-manifest)
- [cavra release updater-policy](#cavra-release-updater-policy)
- [cavra release request-channel-promotion](#cavra-release-request-channel-promotion)
- [cavra release export-endpoint-management](#cavra-release-export-endpoint-management)
- [cavra release deliver-endpoint-export](#cavra-release-deliver-endpoint-export)
- [cavra release ingest-endpoint-inventory](#cavra-release-ingest-endpoint-inventory)
- [cavra release reconcile-endpoint-deployment](#cavra-release-reconcile-endpoint-deployment)
- [cavra release capture-rollout](#cavra-release-capture-rollout)
- [cavra release verify-rollout](#cavra-release-verify-rollout)
- [cavra release request-rollout-promotion](#cavra-release-request-rollout-promotion)
- [cavra release execute-rollout-promotion](#cavra-release-execute-rollout-promotion)
- [cavra release execute-rollout-rollback](#cavra-release-execute-rollout-rollback)
- [cavra release export-promotion-audit](#cavra-release-export-promotion-audit)
- [cavra release deliver-promotion-audit](#cavra-release-deliver-promotion-audit)
- [cavra release deliver-rollback-execution](#cavra-release-deliver-rollback-execution)
- [cavra release connector-delivery-history](#cavra-release-connector-delivery-history)
- [cavra release connector-delivery-dashboard](#cavra-release-connector-delivery-dashboard)
- [cavra release endpoint-publication-history](#cavra-release-endpoint-publication-history)
- [cavra release endpoint-publication-dashboard](#cavra-release-endpoint-publication-dashboard)
- [cavra release endpoint-reconciliation-history](#cavra-release-endpoint-reconciliation-history)
- [cavra release endpoint-reconciliation-dashboard](#cavra-release-endpoint-reconciliation-dashboard)
- [cavra release endpoint-inventory-history](#cavra-release-endpoint-inventory-history)
- [cavra release endpoint-inventory-dashboard](#cavra-release-endpoint-inventory-dashboard)
- [cavra release endpoint-inventory-freshness](#cavra-release-endpoint-inventory-freshness)
- [cavra release endpoint-inventory-freshness-history](#cavra-release-endpoint-inventory-freshness-history)
- [cavra release endpoint-inventory-freshness-dashboard](#cavra-release-endpoint-inventory-freshness-dashboard)
- [cavra release automate-endpoint-reconciliation](#cavra-release-automate-endpoint-reconciliation)
- [cavra release endpoint-reconciliation-automation-history](#cavra-release-endpoint-reconciliation-automation-history)
- [cavra release endpoint-reconciliation-automation-dashboard](#cavra-release-endpoint-reconciliation-automation-dashboard)
- [cavra release request-endpoint-remediation](#cavra-release-request-endpoint-remediation)
- [cavra release export-endpoint-remediation-handoff](#cavra-release-export-endpoint-remediation-handoff)
- [cavra release record-endpoint-remediation-handoff-status](#cavra-release-record-endpoint-remediation-handoff-status)
- [cavra release execute-endpoint-remediation](#cavra-release-execute-endpoint-remediation)
- [cavra release endpoint-remediation-handoff-history](#cavra-release-endpoint-remediation-handoff-history)
- [cavra release endpoint-remediation-handoff-dashboard](#cavra-release-endpoint-remediation-handoff-dashboard)
- [cavra release endpoint-remediation-handoff-status-history](#cavra-release-endpoint-remediation-handoff-status-history)
- [cavra release endpoint-remediation-handoff-status-dashboard](#cavra-release-endpoint-remediation-handoff-status-dashboard)
- [cavra release endpoint-remediation-sla-report](#cavra-release-endpoint-remediation-sla-report)
- [cavra release deliver-endpoint-remediation-sla](#cavra-release-deliver-endpoint-remediation-sla)
- [cavra release endpoint-remediation-sla-history](#cavra-release-endpoint-remediation-sla-history)
- [cavra release endpoint-remediation-sla-dashboard](#cavra-release-endpoint-remediation-sla-dashboard)
- [cavra release ack-endpoint-remediation-sla](#cavra-release-ack-endpoint-remediation-sla)
- [cavra release endpoint-remediation-sla-notification-history](#cavra-release-endpoint-remediation-sla-notification-history)
- [cavra release endpoint-remediation-sla-notification-dashboard](#cavra-release-endpoint-remediation-sla-notification-dashboard)
- [cavra release endpoint-remediation-sla-escalation-plan](#cavra-release-endpoint-remediation-sla-escalation-plan)
- [cavra release endpoint-remediation-sla-escalation-history](#cavra-release-endpoint-remediation-sla-escalation-history)
- [cavra release endpoint-remediation-sla-escalation-dashboard](#cavra-release-endpoint-remediation-sla-escalation-dashboard)
- [cavra release deliver-endpoint-remediation-sla-escalation](#cavra-release-deliver-endpoint-remediation-sla-escalation)
- [cavra release review-endpoint-remediation-sla-escalation](#cavra-release-review-endpoint-remediation-sla-escalation)
- [cavra release endpoint-remediation-sla-escalation-action-history](#cavra-release-endpoint-remediation-sla-escalation-action-history)
- [cavra release endpoint-remediation-sla-escalation-action-dashboard](#cavra-release-endpoint-remediation-sla-escalation-action-dashboard)
- [cavra release endpoint-remediation-sla-escalation-recurrence-plan](#cavra-release-endpoint-remediation-sla-escalation-recurrence-plan)
- [cavra release endpoint-remediation-sla-escalation-recurrence-history](#cavra-release-endpoint-remediation-sla-escalation-recurrence-history)
- [cavra release endpoint-remediation-sla-escalation-recurrence-dashboard](#cavra-release-endpoint-remediation-sla-escalation-recurrence-dashboard)
- [cavra release deliver-endpoint-remediation-sla-escalation-recurrence](#cavra-release-deliver-endpoint-remediation-sla-escalation-recurrence)
- [cavra release export-endpoint-remediation-sla-escalation-suppression-audit](#cavra-release-export-endpoint-remediation-sla-escalation-suppression-audit)
- [cavra release endpoint-remediation-sla-escalation-recurrence-retry-plan](#cavra-release-endpoint-remediation-sla-escalation-recurrence-retry-plan)
- [cavra release deliver-endpoint-remediation-sla-escalation-owner-digest](#cavra-release-deliver-endpoint-remediation-sla-escalation-owner-digest)
- [cavra release endpoint-remediation-sla-escalation-suppression-trends](#cavra-release-endpoint-remediation-sla-escalation-suppression-trends)
- [cavra release endpoint-remediation-sla-escalation-recurrence-automation](#cavra-release-endpoint-remediation-sla-escalation-recurrence-automation)
- [cavra release endpoint-remediation-sla-escalation-recurrence-automation-history](#cavra-release-endpoint-remediation-sla-escalation-recurrence-automation-history)
- [cavra release endpoint-remediation-sla-escalation-recurrence-automation-dashboard](#cavra-release-endpoint-remediation-sla-escalation-recurrence-automation-dashboard)
- [cavra release endpoint-remediation-sla-escalation-recurrence-automation-health](#cavra-release-endpoint-remediation-sla-escalation-recurrence-automation-health)
- [cavra release deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert](#cavra-release-deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert)
- [cavra release ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert](#cavra-release-ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert)
- [cavra release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history](#cavra-release-endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history)
- [cavra release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard](#cavra-release-endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard)
- [cavra release endpoint-remediation-history](#cavra-release-endpoint-remediation-history)
- [cavra release endpoint-remediation-dashboard](#cavra-release-endpoint-remediation-dashboard)
- [cavra demo before-the-agent-acts](#cavra-demo-before-the-agent-acts)

## `cavra`

```text
                                                                                                                                            
 Usage: python -m cavra.cli [OPTIONS] COMMAND [ARGS]...                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ version                                                                                                                                  │
│ evaluate     Evaluate one action before an AI agent performs it.                                                                         │
│ agent        AI agent runtime commands.                                                                                                  │
│ policy       Policy registry commands.                                                                                                   │
│ demo         Runnable CAVRA demos.                                                                                                       │
│ init         Initialize CAVRA integrations.                                                                                              │
│ integration  Enterprise connector delivery commands.                                                                                     │
│ evidence     Evidence bundle commands.                                                                                                   │
│ approval     Human approval router commands.                                                                                             │
│ registry     Agent and MCP trust registry commands.                                                                                      │
│ ops          Persistent API operations commands.                                                                                         │
│ release      Release package verification commands.                                                                                      │
│ runtime      Runtime backend pilot commands.                                                                                             │
│ saas         Public-safe SaaS Control Plane contract commands.                                                                           │
│ aispm        AI Security Posture Management commands.                                                                                    │
│ monitor      Continuous monitoring event commands.                                                                                       │
│ benchmark    Benchmark and SLO regression commands.                                                                                      │
│ adapter      Generic agent adapter and action taxonomy commands.                                                                         │
│ ai-red-team  Native AI red-team, guardrail, and supply-chain commands.                                                                   │
│ deployment   Reference deployment and zero-trust packaging commands.                                                                     │
│ setup        First-run setup, defaults, demo workspace, SMTP, and validation commands.                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra agent`

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                                            
 AI agent runtime commands.                                                                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ start                  Start an AI agent governance session.                                                                             │
│ exec                   Execute a command under governance policy.                                                                        │
│ attest                 Generate PR attestation from audit session.                                                                       │
│ enforcement-readiness  Report whether a repository can enforce CAVRA for AI coding agents.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy [OPTIONS] COMMAND [ARGS]...                                                                              
                                                                                                                                            
 Policy registry commands.                                                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ list                 List available policy packs.                                                                                        │
│ validate             Validate a policy pack against the CAVRA JSON Schema.                                                               │
│ test                 Run core CAVRA policy assertions.                                                                                   │
│ explain              Explain the policy decision for an action.                                                                          │
│ compile              Compile a policy pack and optional overlays to normalized JSON.                                                     │
│ rego-export          Export a CAVRA policy pack to a public-safe OPA/Rego compatibility bundle.                                          │
│ rego-test            Run Rego/Python parity tests for the generated policy path.                                                         │
│ rego-readiness       Validate an OPA/Rego policy readiness packet.                                                                       │
│ lifecycle-plan       Export policy lifecycle lint, version, shadow, dry-run, rollback, and approval artifacts.                           │
│ lifecycle-readiness  Validate a policy lifecycle readiness packet.                                                                       │
│ diff                 Show a semantic diff between two policies.                                                                          │
│ sign                 Create CAVRA policy signature metadata.                                                                             │
│ verify               Verify CAVRA policy signature metadata.                                                                             │
│ keygen               Generate a local Ed25519 keypair for public policy signing workflows.                                               │
│ simulate             Simulate the flagship CAVRA decision sequence.                                                                      │
│ dry-run              Run policy simulation without enforcing changes.                                                                    │
│ init                 Create a starter CAVRA policy.                                                                                      │
│ describe             Describe a policy pack.                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra demo`

```text
                                                                                                                                            
 Usage: python -m cavra.cli demo [OPTIONS] COMMAND [ARGS]...                                                                                
                                                                                                                                            
 Runnable CAVRA demos.                                                                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ before-the-agent-acts  Run the flagship CAVRA demo and generate evidence.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra init`

```text
                                                                                                                                            
 Usage: python -m cavra.cli init [OPTIONS] COMMAND [ARGS]...                                                                                
                                                                                                                                            
 Initialize CAVRA integrations.                                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ claude-code  Initialize first-class Claude Code governance with CAVRA.                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra integration`

```text
                                                                                                                                            
 Usage: python -m cavra.cli integration [OPTIONS] COMMAND [ARGS]...                                                                         
                                                                                                                                            
 Enterprise connector delivery commands.                                                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ deliver  Send live connector requests and write redacted delivery evidence.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence [OPTIONS] COMMAND [ARGS]...                                                                            
                                                                                                                                            
 Evidence bundle commands.                                                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ bundle              Generate a CAVRA evidence bundle from the flagship decision sequence.                                                │
│ generate-keypair    Generate an Ed25519 keypair for evidence manifest signatures.                                                        │
│ trust-root          Create a CAVRA evidence signing trust-root document.                                                                 │
│ trust-bundle        Create a distributable bundle of CAVRA evidence trust roots.                                                         │
│ trust-distribution  Create an offline distribution package for CAVRA evidence trust roots.                                               │
│ verify              Verify evidence bundle manifest, checksums, and optional signature.                                                  │
│ siem-event          Print the SIEM event from an evidence bundle.                                                                        │
│ retention-policy    Export evidence retention controls for an existing bundle.                                                           │
│ export-siem         Export provider-specific SIEM payloads from an evidence bundle.                                                      │
│ storage-plan        Create S3 Object Lock and Azure immutable blob reference plans.                                                      │
│ verify-attestation  Verify PR attestation content against bundle evidence.                                                               │
│ index               Persist searchable evidence metadata from a bundle.                                                                  │
│ search              Search SQLite-backed evidence metadata with filters and pagination.                                                  │
│ migrate             Apply SQLite migrations for evidence metadata search.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval [OPTIONS] COMMAND [ARGS]...                                                                            
                                                                                                                                            
 Human approval router commands.                                                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create                Create a pending approval request from a CAVRA decision.                                                           │
│ list                  List approval queue entries.                                                                                       │
│ approve               Approve a pending request.                                                                                         │
│ deny                  Deny a pending request.                                                                                            │
│ expire                Expire a pending request.                                                                                          │
│ break-glass           Record a break-glass override with mandatory evidence.                                                             │
│ route                 Show the approver group selected by approval routing policy.                                                       │
│ export-notifications  Export reference notification payloads for approval providers.                                                     │
│ provider-requests     Export credential-free HTTP request specs for approval providers.                                                  │
│ deliver               Send live approval provider requests and write redacted delivery evidence.                                         │
│ migrate               Apply SQLite migrations for approval persistence.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry [OPTIONS] COMMAND [ARGS]...                                                                            
                                                                                                                                            
 Agent and MCP trust registry commands.                                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ agent-register       Register or update a governed AI-agent identity.                                                                    │
│ agent-list           List governed AI-agent identities.                                                                                  │
│ profiles             List predefined AI-agent capability profiles.                                                                       │
│ mcp-register         Register or update an MCP server trust record.                                                                      │
│ mcp-list             List MCP server trust records.                                                                                      │
│ mcp-check            Evaluate an MCP tool call against the trust registry.                                                               │
│ mcp-classifications  List MCP tool capability classifications.                                                                           │
│ migrate              Apply SQLite migrations for the registry and other CAVRA metadata tables.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ops`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops [OPTIONS] COMMAND [ARGS]...                                                                                 
                                                                                                                                            
 Persistent API operations commands.                                                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ stores          List configured persistent API stores and whether each path exists.                                                      │
│ backup          Back up configured JSON and SQLite persistent API stores.                                                                │
│ restore         Restore a persistent API backup after checksum validation.                                                               │
│ retention-plan  Export backup, restore-test, and retention controls for persistent API stores.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release [OPTIONS] COMMAND [ARGS]...                                                                             
                                                                                                                                            
 Release package verification commands.                                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ phase6-rollup                                                                                  Validate or export the Phase 6 ecosystem  │
│                                                                                                expansion rollup.                         │
│ phase4-closeout                                                                                Validate or export the Phase 4 connector  │
│                                                                                                and scanner closeout.                     │
│ phase5-closeout                                                                                Validate or export the Phase 5 policy     │
│                                                                                                lifecycle and event core closeout.        │
│ customer-live-evidence                                                                         Validate or export the customer-live      │
│                                                                                                evidence intake packet.                   │
│ customer-evidence-room                                                                         Validate or export the customer           │
│                                                                                                evidence-room closeout index.             │
│ customer-closeout-handoff                                                                      Validate or export the customer closeout  │
│                                                                                                handoff packet.                           │
│ customer-operating-review                                                                      Validate or export the recurring customer │
│                                                                                                operating review packet.                  │
│ customer-renewal-expansion                                                                     Validate or export the customer renewal   │
│                                                                                                and expansion readiness packet.           │
│ customer-renewal-outcome                                                                       Validate or export the customer renewal   │
│                                                                                                outcome closeout packet.                  │
│ customer-lifecycle-rollup                                                                      Validate or export the customer lifecycle │
│                                                                                                executive rollup packet.                  │
│ customer-lifecycle-archive                                                                     Validate or export the customer lifecycle │
│                                                                                                archive manifest.                         │
│ customer-lifecycle-status                                                                      Validate or export the customer lifecycle │
│                                                                                                public status packet.                     │
│ customer-lifecycle-final-seal                                                                  Validate or export the customer lifecycle │
│                                                                                                final release seal packet.                │
│ customer-lifecycle-verification-index                                                          Validate or export the customer lifecycle │
│                                                                                                verification index.                       │
│ managed-enterprise-live-validation-plan                                                        Validate or export the Managed/Enterprise │
│                                                                                                live validation plan.                     │
│ managed-enterprise-cutover-runbook                                                             Validate or export the Managed/Enterprise │
│                                                                                                cutover runbook.                          │
│ managed-enterprise-stabilization-report                                                        Validate or export the Managed/Enterprise │
│                                                                                                post-cutover stabilization report.        │
│ managed-enterprise-steady-state-handoff                                                        Validate or export the Managed/Enterprise │
│                                                                                                steady-state handoff packet.              │
│ managed-enterprise-operating-release-index                                                     Validate or export the Managed/Enterprise │
│                                                                                                operating release index.                  │
│ managed-enterprise-operating-announcement                                                      Validate or export the Managed/Enterprise │
│                                                                                                operating announcement packet.            │
│ managed-enterprise-operating-chain                                                             Validate or export the full               │
│                                                                                                Managed/Enterprise operating chain.       │
│ managed-enterprise-operating-certificate                                                       Validate or export the Managed/Enterprise │
│                                                                                                operating release certificate.            │
│ managed-enterprise-certificate-publication-index                                               Validate or export the Managed/Enterprise │
│                                                                                                certificate publication index.            │
│ roadmap-intake-gate                                                                            Validate or export the roadmap intake     │
│                                                                                                gate.                                     │
│ roadmap-candidate-charter                                                                      Validate or export the roadmap candidate  │
│                                                                                                charter.                                  │
│ roadmap-future-phase-opening-gate                                                              Validate or export the roadmap future     │
│                                                                                                phase opening gate.                       │
│ roadmap-future-phase-registry                                                                  Validate or export the roadmap future     │
│                                                                                                phase registry.                           │
│ roadmap-future-work-governance-index                                                           Validate or export the roadmap future     │
│                                                                                                work governance index.                    │
│ roadmap-governance-quickcheck                                                                  Validate the closed roadmap boundary and  │
│                                                                                                future-work governance chain in one pass. │
│ customer-lifecycle-announcement                                                                Validate or export the customer lifecycle │
│                                                                                                closeout announcement packet.             │
│ customer-lifecycle-retrospective                                                               Validate or export the customer lifecycle │
│                                                                                                retrospective packet.                     │
│ customer-lifecycle-phase8-backlog                                                              Validate or export the customer lifecycle │
│                                                                                                Phase 8 backlog packet.                   │
│ customer-lifecycle-phase8-kickoff                                                              Validate or export the customer lifecycle │
│                                                                                                Phase 8 kickoff packet.                   │
│ customer-lifecycle-phase8-sprint1-checkpoint                                                   Validate or export the customer lifecycle │
│                                                                                                Phase 8 Sprint 1 checkpoint packet.       │
│ customer-lifecycle-phase8-telemetry-depth                                                      Validate or export the customer lifecycle │
│                                                                                                Phase 8 telemetry depth packet.           │
│ customer-lifecycle-phase8-support-automation                                                   Validate or export the customer lifecycle │
│                                                                                                Phase 8 support automation packet.        │
│ customer-lifecycle-phase8-lifecycle-analytics                                                  Validate or export the customer lifecycle │
│                                                                                                Phase 8 lifecycle analytics packet.       │
│ customer-lifecycle-phase8-customer-health-review                                               Validate or export the customer lifecycle │
│                                                                                                Phase 8 customer health review packet.    │
│ customer-lifecycle-phase8-executive-health-rollup                                              Validate or export the customer lifecycle │
│                                                                                                Phase 8 executive health rollup packet.   │
│ customer-lifecycle-phase8-executive-action-plan                                                Validate or export the customer lifecycle │
│                                                                                                Phase 8 executive action plan packet.     │
│ customer-lifecycle-phase8-action-followup-checkpoint                                           Validate or export the customer lifecycle │
│                                                                                                Phase 8 action follow-up checkpoint       │
│                                                                                                packet.                                   │
│ customer-lifecycle-phase8-executive-followup-closeout                                          Validate or export the customer lifecycle │
│                                                                                                Phase 8 executive follow-up closeout      │
│                                                                                                packet.                                   │
│ customer-lifecycle-phase8-next-cycle-readiness-index                                           Validate or export the customer lifecycle │
│                                                                                                Phase 8 next-cycle readiness index        │
│                                                                                                packet.                                   │
│ customer-lifecycle-phase8-public-operating-scorecard                                           Validate or export the customer lifecycle │
│                                                                                                Phase 8 public operating scorecard        │
│                                                                                                packet.                                   │
│ customer-lifecycle-phase8-public-scorecard-publication-closeout                                Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard publication      │
│                                                                                                closeout packet.                          │
│ customer-lifecycle-phase8-public-scorecard-refresh-checkpoint                                  Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard refresh          │
│                                                                                                checkpoint packet.                        │
│ customer-lifecycle-phase8-public-scorecard-refresh-closeout                                    Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard refresh closeout │
│                                                                                                packet.                                   │
│ customer-lifecycle-phase8-public-scorecard-operating-loop-index                                Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard operating loop   │
│                                                                                                index packet.                             │
│ customer-lifecycle-phase8-public-scorecard-executive-summary-closeout                          Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard executive        │
│                                                                                                summary closeout packet.                  │
│ customer-lifecycle-phase8-public-scorecard-distribution-readiness                              Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard distribution     │
│                                                                                                readiness packet.                         │
│ customer-lifecycle-phase8-public-scorecard-distribution-closeout                               Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard distribution     │
│                                                                                                closeout packet.                          │
│ customer-lifecycle-phase8-public-scorecard-distribution-audit-index                            Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard distribution     │
│                                                                                                audit index packet.                       │
│ customer-lifecycle-phase8-public-scorecard-audit-review-closeout                               Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard audit review     │
│                                                                                                closeout packet.                          │
│ customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness                     Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard continuous       │
│                                                                                                monitoring readiness packet.              │
│ customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout                      Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard monitoring       │
│                                                                                                activation closeout packet.               │
│ customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review                       Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard monitoring       │
│                                                                                                first-cycle review packet.                │
│ customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout               Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard monitoring drift │
│                                                                                                remediation closeout packet.              │
│ customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness                   Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard monitoring       │
│                                                                                                second-cycle readiness packet.            │
│ customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout         Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard monitoring       │
│                                                                                                second-cycle activation closeout packet.  │
│ customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review                Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard monitoring       │
│                                                                                                second-cycle first review packet.         │
│ customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout  Validate or export the customer lifecycle │
│                                                                                                Phase 8 public scorecard monitoring       │
│                                                                                                second-cycle drift remediation closeout   │
│                                                                                                packet.                                   │
│ verify-go-package                                                                              Verify a CAVRA Go runtime release         │
│                                                                                                package.                                  │
│ verify-airgap-bundle                                                                           Verify an air-gapped CAVRA Go runtime     │
│                                                                                                release zip.                              │
│ validate-upgrade                                                                               Validate a Go runtime release-candidate   │
│                                                                                                upgrade before promotion.                 │
│ smoke-installers                                                                               Smoke-test Go runtime installer metadata  │
│                                                                                                and the native packaged binary.           │
│ channel-manifest                                                                               Inspect release package channel metadata  │
│                                                                                                for managed workstations.                 │
│ updater-policy                                                                                 Inspect managed workstation updater       │
│                                                                                                policy for a release package.             │
│ request-channel-promotion                                                                      Create a signed approval request for      │
│                                                                                                release channel promotion.                │
│ export-endpoint-management                                                                     Export Jamf, Intune, and Linux            │
│                                                                                                endpoint-management bundles for a release │
│                                                                                                channel.                                  │
│ deliver-endpoint-export                                                                        Publish an endpoint-management export to  │
│                                                                                                Jamf, Intune, or Linux fleet connectors.  │
│ ingest-endpoint-inventory                                                                      Normalize provider endpoint inventory     │
│                                                                                                exports into CAVRA endpoint observations. │
│ reconcile-endpoint-deployment                                                                  Compare desired signed endpoint           │
│                                                                                                deployment state with observed endpoint   │
│                                                                                                inventory.                                │
│ capture-rollout                                                                                Capture rollout evidence for managed      │
│                                                                                                endpoint deployment targets.              │
│ verify-rollout                                                                                 Verify managed endpoint rollout evidence  │
│                                                                                                and optionally index its metadata.        │
│ request-rollout-promotion                                                                      Create a signed approval request for      │
│                                                                                                endpoint rollout promotion.               │
│ execute-rollout-promotion                                                                      Record an approved endpoint rollout ring  │
│                                                                                                promotion execution.                      │
│ execute-rollout-rollback                                                                       Record an approved endpoint rollout       │
│                                                                                                rollback execution.                       │
│ export-promotion-audit                                                                         Export SIEM and ITSM audit payloads for a │
│                                                                                                rollout promotion execution.              │
│ deliver-promotion-audit                                                                        Deliver a rollout promotion audit event   │
│                                                                                                through configured connectors.            │
│ deliver-rollback-execution                                                                     Deliver a rollout rollback execution      │
│                                                                                                event through configured connectors.      │
│ connector-delivery-history                                                                     Show persisted release governance         │
│                                                                                                connector delivery history.               │
│ connector-delivery-dashboard                                                                   Summarize release governance connector    │
│                                                                                                delivery health and alerts.               │
│ endpoint-publication-history                                                                   Show persisted endpoint-management export │
│                                                                                                publication history.                      │
│ endpoint-publication-dashboard                                                                 Summarize endpoint-management publication │
│                                                                                                health and provider failures.             │
│ endpoint-reconciliation-history                                                                Show managed endpoint deployment          │
│                                                                                                reconciliation history.                   │
│ endpoint-reconciliation-dashboard                                                              Summarize managed endpoint deployment     │
│                                                                                                drift and stale endpoint observations.    │
│ endpoint-inventory-history                                                                     Show endpoint inventory ingestion         │
│                                                                                                history.                                  │
│ endpoint-inventory-dashboard                                                                   Summarize normalized endpoint inventory   │
│                                                                                                coverage by provider.                     │
│ endpoint-inventory-freshness                                                                   Create an endpoint inventory freshness    │
│                                                                                                SLA report from indexed ingestions.       │
│ endpoint-inventory-freshness-history                                                           Show endpoint inventory freshness report  │
│                                                                                                history.                                  │
│ endpoint-inventory-freshness-dashboard                                                         Summarize endpoint inventory freshness    │
│                                                                                                SLA alerts.                               │
│ automate-endpoint-reconciliation                                                               Reconcile a fresh inventory ingestion and │
│                                                                                                open remediation when drift is detected.  │
│ endpoint-reconciliation-automation-history                                                     Show endpoint reconciliation automation   │
│                                                                                                history.                                  │
│ endpoint-reconciliation-automation-dashboard                                                   Summarize endpoint reconciliation         │
│                                                                                                automations and pending remediation       │
│                                                                                                approvals.                                │
│ request-endpoint-remediation                                                                   Create an approval-bound endpoint drift   │
│                                                                                                remediation plan.                         │
│ export-endpoint-remediation-handoff                                                            Export public-safe ITSM, ChatOps, and     │
│                                                                                                private connector handoff payloads.       │
│ record-endpoint-remediation-handoff-status                                                     Record public-safe provider status for an │
│                                                                                                endpoint remediation handoff.             │
│ execute-endpoint-remediation                                                                   Record an approved endpoint drift         │
│                                                                                                remediation execution.                    │
│ endpoint-remediation-handoff-history                                                           Show endpoint remediation handoff package │
│                                                                                                history.                                  │
│ endpoint-remediation-handoff-dashboard                                                         Summarize endpoint remediation handoff    │
│                                                                                                packages by provider and approval state.  │
│ endpoint-remediation-handoff-status-history                                                    Show endpoint remediation handoff status  │
│                                                                                                history.                                  │
│ endpoint-remediation-handoff-status-dashboard                                                  Summarize endpoint remediation handoff    │
│                                                                                                status callbacks by provider and state.   │
│ endpoint-remediation-sla-report                                                                Generate endpoint remediation SLA,        │
│                                                                                                escalation, and executive reporting.      │
│ deliver-endpoint-remediation-sla                                                               Deliver endpoint remediation SLA          │
│                                                                                                notifications through configured release  │
│                                                                                                connectors.                               │
│ endpoint-remediation-sla-history                                                               Show endpoint remediation SLA report      │
│                                                                                                history.                                  │
│ endpoint-remediation-sla-dashboard                                                             Summarize endpoint remediation SLA        │
│                                                                                                reports for executive release governance. │
│ ack-endpoint-remediation-sla                                                                   Record acknowledgement for an endpoint    │
│                                                                                                remediation SLA notification.             │
│ endpoint-remediation-sla-notification-history                                                  Show endpoint remediation SLA             │
│                                                                                                notification plans, deliveries, and       │
│                                                                                                acknowledgements.                         │
│ endpoint-remediation-sla-notification-dashboard                                                Summarize endpoint remediation SLA        │
│                                                                                                notification routing and                  │
│                                                                                                acknowledgements.                         │
│ endpoint-remediation-sla-escalation-plan                                                       Build owner-specific SLO and              │
│                                                                                                escalation-ladder status for SLA          │
│                                                                                                notifications.                            │
│ endpoint-remediation-sla-escalation-history                                                    Show endpoint remediation SLA escalation  │
│                                                                                                plans.                                    │
│ endpoint-remediation-sla-escalation-dashboard                                                  Summarize endpoint remediation SLA        │
│                                                                                                escalation ladders and owner SLOs.        │
│ deliver-endpoint-remediation-sla-escalation                                                    Deliver active endpoint remediation SLA   │
│                                                                                                escalations through configured release    │
│                                                                                                connectors.                               │
│ review-endpoint-remediation-sla-escalation                                                     Record owner review for an endpoint       │
│                                                                                                remediation SLA escalation route.         │
│ endpoint-remediation-sla-escalation-action-history                                             Show endpoint remediation SLA escalation  │
│                                                                                                plans, deliveries, and owner reviews.     │
│ endpoint-remediation-sla-escalation-action-dashboard                                           Summarize endpoint remediation SLA        │
│                                                                                                escalation delivery and owner review      │
│                                                                                                actions.                                  │
│ endpoint-remediation-sla-escalation-recurrence-plan                                            Plan recurring escalation follow-up with  │
│                                                                                                owner calendar and maintenance-window     │
│                                                                                                suppression.                              │
│ endpoint-remediation-sla-escalation-recurrence-history                                         Show endpoint remediation SLA escalation  │
│                                                                                                recurrence and suppression plans.         │
│ endpoint-remediation-sla-escalation-recurrence-dashboard                                       Summarize endpoint remediation SLA        │
│                                                                                                escalation recurrence suppression.        │
│ deliver-endpoint-remediation-sla-escalation-recurrence                                         Deliver recurrence-plan routes that are   │
│                                                                                                ready for follow-up escalation.           │
│ export-endpoint-remediation-sla-escalation-suppression-audit                                   Export public-safe suppression audit      │
│                                                                                                evidence from a recurrence plan.          │
│ endpoint-remediation-sla-escalation-recurrence-retry-plan                                      Plan safe retries for failed recurrence   │
│                                                                                                delivery batches.                         │
│ deliver-endpoint-remediation-sla-escalation-owner-digest                                       Deliver owner digest notifications for    │
│                                                                                                unresolved recurrence routes.             │
│ endpoint-remediation-sla-escalation-suppression-trends                                         Summarize recurrence suppression trends   │
│                                                                                                by reason, owner, and provider.           │
│ endpoint-remediation-sla-escalation-recurrence-automation                                      Run one scheduled recurrence automation   │
│                                                                                                pass for retry, digest, and trend         │
│                                                                                                follow-up.                                │
│ endpoint-remediation-sla-escalation-recurrence-automation-history                              List scheduled recurrence automation      │
│                                                                                                worker runs.                              │
│ endpoint-remediation-sla-escalation-recurrence-automation-dashboard                            Summarize scheduled recurrence automation │
│                                                                                                worker runs.                              │
│ endpoint-remediation-sla-escalation-recurrence-automation-health                               Report missed recurrence automation runs, │
│                                                                                                stale metadata, and delivery failures.    │
│ deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert                 Deliver recurrence automation health      │
│                                                                                                alerts through configured release         │
│                                                                                                connectors.                               │
│ ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert                     Record acknowledgement for a recurrence   │
│                                                                                                automation health alert.                  │
│ endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history                 Show recurrence automation health alert   │
│                                                                                                plans, deliveries, and acknowledgements.  │
│ endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard               Summarize recurrence automation health    │
│                                                                                                alert delivery and acknowledgements.      │
│ endpoint-remediation-history                                                                   Show endpoint drift remediation request   │
│                                                                                                and execution history.                    │
│ endpoint-remediation-dashboard                                                                 Summarize endpoint drift remediation      │
│                                                                                                approvals and executions.                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime [OPTIONS] COMMAND [ARGS]...                                                                             
                                                                                                                                            
 Runtime backend pilot commands.                                                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ go-pilot-readiness                   Show opt-in Go backend pilot readiness.                                                             │
│ go-deployment-readiness              Show Go backend CI runner and workstation deployment readiness.                                     │
│ go-promotion-readiness               Show Go backend promotion readiness for optional backend use.                                       │
│ go-rollback-readiness                Show Go backend rollback readiness for promoted pilots.                                             │
│ go-rollback-rehearsal                Show automated rollback rehearsal evidence status for promoted Go pilots.                           │
│ go-rollback-drills                   Show operational rollback drill history status for promoted Go pilots.                              │
│ go-rollback-drill-schedule           Show recurring rollback drill schedule and stale-drill notification readiness.                      │
│ go-rollback-drill-notification-plan  Build a public-safe stale rollback drill notification plan.                                         │
│ go-rollback-drill-notification-ack   Build public-safe rollback drill notification acknowledgement metadata.                             │
│ go-rollback-drill-escalation-plan    Build an empty public-safe rollback drill notification escalation plan template.                    │
│ go-pilot-evaluate                    Evaluate through the opt-in Go backend pilot with Python fallback.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra saas`

```text
                                                                                                                                            
 Usage: python -m cavra.cli saas [OPTIONS] COMMAND [ARGS]...                                                                                
                                                                                                                                            
 Public-safe SaaS Control Plane contract commands.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ contract              Print the public-safe SaaS Control Plane contract description.                                                     │
│ operating-automation  Print a public-safe SaaS operating automation request and placeholder response.                                    │
│ worker-handoff        Print a public-safe SaaS operating automation worker handoff request and response.                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra aispm`

```text
                                                                                                                                            
 Usage: python -m cavra.cli aispm [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                                            
 AI Security Posture Management commands.                                                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ validate-review-packet      Validate an AISPM replay-to-policy review packet before PR attachment.                                       │
│ validate-ci-gate-readiness  Validate AISPM replay-to-policy CI gate readiness before production use.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra monitor`

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor [OPTIONS] COMMAND [ARGS]...                                                                             
                                                                                                                                            
 Continuous monitoring event commands.                                                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ sample-events  Emit deterministic sample continuous monitoring events.                                                                   │
│ replay         Replay continuous monitoring events and report dedupe, latency, and freshness.                                            │
│ export         Export sample continuous monitoring artifacts.                                                                            │
│ readiness      Validate a continuous monitoring readiness packet.                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra benchmark`

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark [OPTIONS] COMMAND [ARGS]...                                                                           
                                                                                                                                            
 Benchmark and SLO regression commands.                                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ export     Export benchmark, SLO gate, and readiness artifacts.                                                                          │
│ run        Run or emit the benchmark/SLO report and fail when the gate has blockers.                                                     │
│ readiness  Validate a benchmark/SLO readiness packet.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra adapter`

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter [OPTIONS] COMMAND [ARGS]...                                                                             
                                                                                                                                            
 Generic agent adapter and action taxonomy commands.                                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ taxonomy           Emit the public generic action taxonomy.                                                                              │
│ manifest-validate  Validate a generic adapter manifest.                                                                                  │
│ evaluate           Evaluate generic non-coding agent actions through the CAVRA taxonomy.                                                 │
│ export             Export reference generic adapter taxonomy, manifest, scenario, evaluation, and packet artifacts.                      │
│ readiness          Validate a generic adapter readiness packet.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ai-red-team`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team [OPTIONS] COMMAND [ARGS]...                                                                         
                                                                                                                                            
 Native AI red-team, guardrail, and supply-chain commands.                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ guardrails       Run native LLM guardrail tests.                                                                                         │
│ supply-chain     Validate AI artifact supply-chain metadata.                                                                             │
│ malicious-model  Run malicious model checks against AI artifact metadata.                                                                │
│ export           Export native AI red-team, supply-chain, malicious-model, and readiness artifacts.                                      │
│ readiness        Validate an AI red-team readiness packet.                                                                               │
│ packet           Emit a generated AI red-team readiness packet.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra deployment`

```text
                                                                                                                                            
 Usage: python -m cavra.cli deployment [OPTIONS] COMMAND [ARGS]...                                                                          
                                                                                                                                            
 Reference deployment and zero-trust packaging commands.                                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ zero-trust-catalog    Emit and validate the zero-trust reference deployment catalog.                                                     │
│ zero-trust-export     Export zero-trust reference deployment catalog and readiness packets.                                              │
│ zero-trust-readiness  Validate a zero-trust reference deployment readiness packet.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup [OPTIONS] COMMAND [ARGS]...                                                                               
                                                                                                                                            
 First-run setup, defaults, demo workspace, SMTP, and validation commands.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ status              Show first-run setup status.                                                                                         │
│ init                Create default first-run CAVRA setup state.                                                                          │
│ wizard              Run the non-interactive default setup wizard for local Community validation.                                         │
│ demo-env            Create a safe local demo workspace with known policy-triggering scenarios.                                           │
│ validate            Validate default setup, policy pack discovery, demo scenarios, and AISPM readiness inputs.                           │
│ complete            Mark setup as complete after validation.                                                                             │
│ smtp                Validate or save SMTP/report-delivery setup metadata without storing passwords.                                      │
│ policy-actions      List editable allow, block, approval, and MCP action catalog entries from a policy pack.                             │
│ policy-action-test  Test one action against the selected policy pack.                                                                    │
│ policy-action-plan  Create a policy draft plan for an allow/block/approval catalog change.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra version`

```text
                                                                                                                                            
 Usage: python -m cavra.cli version [OPTIONS]                                                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ai-red-team guardrails`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team guardrails [OPTIONS]                                                                                
                                                                                                                                            
 Run native LLM guardrail tests.                                                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --suite        PATH                                                                                                                      │
│ --help               Show this message and exit.                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ai-red-team supply-chain`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team supply-chain [OPTIONS]                                                                              
                                                                                                                                            
 Validate AI artifact supply-chain metadata.                                                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --artifact        PATH                                                                                                                   │
│ --help                  Show this message and exit.                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ai-red-team malicious-model`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team malicious-model [OPTIONS]                                                                           
                                                                                                                                            
 Run malicious model checks against AI artifact metadata.                                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --artifact        PATH                                                                                                                   │
│ --help                  Show this message and exit.                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ai-red-team export`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team export [OPTIONS]                                                                                    
                                                                                                                                            
 Export native AI red-team, supply-chain, malicious-model, and readiness artifacts.                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir        PATH  [default: dist/ai-red-team]                                                                                    │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ai-red-team readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team readiness [OPTIONS] PACKET                                                                          
                                                                                                                                            
 Validate an AI red-team readiness packet.                                                                                                  
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ai-red-team packet`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ai-red-team packet [OPTIONS]                                                                                    
                                                                                                                                            
 Emit a generated AI red-team readiness packet.                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --evidence-mode        TEXT  [default: sample]                                                                                           │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra adapter taxonomy`

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter taxonomy [OPTIONS]                                                                                      
                                                                                                                                            
 Emit the public generic action taxonomy.                                                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output        PATH                                                                                                                     │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra adapter manifest-validate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter manifest-validate [OPTIONS] MANIFEST                                                                    
                                                                                                                                            
 Validate a generic adapter manifest.                                                                                                       
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    manifest      PATH  [required]                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra adapter evaluate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter evaluate [OPTIONS] ACTIONS                                                                              
                                                                                                                                            
 Evaluate generic non-coding agent actions through the CAVRA taxonomy.                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    actions      PATH  [required]                                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra adapter export`

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter export [OPTIONS]                                                                                        
                                                                                                                                            
 Export reference generic adapter taxonomy, manifest, scenario, evaluation, and packet artifacts.                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir        PATH  [default: dist/generic-agent-adapter]                                                                          │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra adapter readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli adapter readiness [OPTIONS] PACKET                                                                              
                                                                                                                                            
 Validate a generic adapter readiness packet.                                                                                               
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra deployment zero-trust-catalog`

```text
                                                                                                                                            
 Usage: python -m cavra.cli deployment zero-trust-catalog [OPTIONS]                                                                         
                                                                                                                                            
 Emit and validate the zero-trust reference deployment catalog.                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root        PATH                                                                                                                  │
│ --help                   Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra deployment zero-trust-export`

```text
                                                                                                                                            
 Usage: python -m cavra.cli deployment zero-trust-export [OPTIONS]                                                                          
                                                                                                                                            
 Export zero-trust reference deployment catalog and readiness packets.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir        PATH  [default: dist/zero-trust-reference-deployments]                                                               │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra deployment zero-trust-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli deployment zero-trust-readiness                                                                                 
            [OPTIONS] PACKET                                                                                                                
                                                                                                                                            
 Validate a zero-trust reference deployment readiness packet.                                                                               
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root                            PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra benchmark export`

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark export [OPTIONS]                                                                                      
                                                                                                                                            
 Export benchmark, SLO gate, and readiness artifacts.                                                                                       
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir                        PATH     [default: dist/benchmark-slo]                                                               │
│ --measured         --no-measured             [default: no-measured]                                                                      │
│ --iterations                        INTEGER  [default: 25]                                                                               │
│ --evidence-mode                     TEXT     [default: sample]                                                                           │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra benchmark run`

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark run [OPTIONS]                                                                                         
                                                                                                                                            
 Run or emit the benchmark/SLO report and fail when the gate has blockers.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --measured      --no-measured             [default: no-measured]                                                                         │
│ --iterations                     INTEGER  [default: 25]                                                                                  │
│ --help                                    Show this message and exit.                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra benchmark readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli benchmark readiness [OPTIONS] PACKET                                                                            
                                                                                                                                            
 Validate a benchmark/SLO readiness packet.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra monitor sample-events`

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor sample-events [OPTIONS]                                                                                 
                                                                                                                                            
 Emit deterministic sample continuous monitoring events.                                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output        PATH                                                                                                                     │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra monitor replay`

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor replay [OPTIONS] EVENTS                                                                                 
                                                                                                                                            
 Replay continuous monitoring events and report dedupe, latency, and freshness.                                                             
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    events      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --now                        TEXT     [default: 2026-07-04T10:00:00+00:00]                                                               │
│ --latency-slo-ms             INTEGER  [default: 5000]                                                                                    │
│ --stale-after-minutes        INTEGER  [default: 60]                                                                                      │
│ --help                                Show this message and exit.                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra monitor export`

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor export [OPTIONS]                                                                                        
                                                                                                                                            
 Export sample continuous monitoring artifacts.                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir           PATH  [default: dist/continuous-monitoring]                                                                       │
│ --evidence-mode        TEXT  [default: sample]                                                                                           │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra monitor readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli monitor readiness [OPTIONS] PACKET                                                                              
                                                                                                                                            
 Validate a continuous monitoring readiness packet.                                                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra aispm validate-review-packet`

```text
                                                                                                                                            
 Usage: python -m cavra.cli aispm validate-review-packet [OPTIONS] PATH                                                                     
                                                                                                                                            
 Validate an AISPM replay-to-policy review packet before PR attachment.                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --json          Print the validation report JSON.                                                                                        │
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra aispm validate-ci-gate-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli aispm validate-ci-gate-readiness                                                                                
            [OPTIONS] PATH                                                                                                                  
                                                                                                                                            
 Validate AISPM replay-to-policy CI gate readiness before production use.                                                                   
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root        PATH                                                                                                                  │
│ --json                   Print the validation report JSON.                                                                               │
│ --help                   Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evaluate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evaluate [OPTIONS] ACTION_TYPE TARGET                                                                           
                                                                                                                                            
 Evaluate one action before an AI agent performs it.                                                                                        
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action_type      TEXT  [required]                                                                                                   │
│ *    target           TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack               TEXT  [default: cavra-ai-agent-baseline]                                                                     │
│ --policy-mode               TEXT  [default: enforce]                                                                                     │
│ --break-glass-reason        TEXT                                                                                                         │
│ --break-glass-actor         TEXT                                                                                                         │
│ --json                            Print the full decision JSON.                                                                          │
│ --help                            Show this message and exit.                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup status`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup status [OPTIONS]                                                                                          
                                                                                                                                            
 Show first-run setup status.                                                                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --state        PATH                                                                                                                      │
│ --help               Show this message and exit.                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup init`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup init [OPTIONS]                                                                                            
                                                                                                                                            
 Create default first-run CAVRA setup state.                                                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --state                               PATH                                                                                               │
│ --workspace-name                      TEXT  [default: local-community]                                                                   │
│ --policy-pack                         TEXT  [default: cavra-ai-agent-baseline]                                                           │
│ --overwrite         --no-overwrite          [default: no-overwrite]                                                                      │
│ --complete          --no-complete           [default: no-complete]                                                                       │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup wizard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup wizard [OPTIONS]                                                                                          
                                                                                                                                            
 Run the non-interactive default setup wizard for local Community validation.                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --state                               PATH                                                                                               │
│ --workspace-name                      TEXT  [default: local-community]                                                                   │
│ --overwrite         --no-overwrite          [default: no-overwrite]                                                                      │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup demo-env`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup demo-env [OPTIONS]                                                                                        
                                                                                                                                            
 Create a safe local demo workspace with known policy-triggering scenarios.                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                         PATH  [default: .cavra/demo-workspace]                                                                  │
│ --overwrite    --no-overwrite          [default: no-overwrite]                                                                           │
│ --help                                 Show this message and exit.                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup validate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup validate [OPTIONS]                                                                                        
                                                                                                                                            
 Validate default setup, policy pack discovery, demo scenarios, and AISPM readiness inputs.                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --state                                        PATH                                                                                      │
│ --record-decisions    --no-record-decisions          [default: no-record-decisions]                                                      │
│ --activity-store                               PATH  [default: .cavra/api/activity.json]                                                 │
│ --help                                               Show this message and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup complete`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup complete [OPTIONS]                                                                                        
                                                                                                                                            
 Mark setup as complete after validation.                                                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --state        PATH                                                                                                                      │
│ --help               Show this message and exit.                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup smtp`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup smtp [OPTIONS]                                                                                            
                                                                                                                                            
 Validate or save SMTP/report-delivery setup metadata without storing passwords.                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --host                         TEXT                                                                                                      │
│ --port                         INTEGER  [default: 587]                                                                                   │
│ --from-email                   TEXT                                                                                                      │
│ --recipient                    TEXT                                                                                                      │
│ --username                     TEXT                                                                                                      │
│ --password-ref                 TEXT     [default: CAVRA_REPORT_SMTP_PASSWORD]                                                            │
│ --state                        PATH                                                                                                      │
│ --live            --no-live             [default: no-live]                                                                               │
│ --save            --no-save             [default: no-save]                                                                               │
│ --help                                  Show this message and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup policy-actions`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup policy-actions [OPTIONS]                                                                                  
                                                                                                                                            
 List editable allow, block, approval, and MCP action catalog entries from a policy pack.                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup policy-action-test`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup policy-action-test [OPTIONS]                                                                              
                                                                                                                                            
 Test one action against the selected policy pack.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --action-type        TEXT  [default: execute_command]                                                                                    │
│ --target             TEXT                                                                                                                │
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra setup policy-action-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli setup policy-action-plan [OPTIONS]                                                                              
                                                                                                                                            
 Create a policy draft plan for an allow/block/approval catalog change.                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --operation          TEXT     [default: add]                                                                                             │
│ --section            TEXT     [default: commands]                                                                                        │
│ --action             TEXT     [default: block]                                                                                           │
│ --value              TEXT                                                                                                                │
│ --policy-pack        TEXT     [default: cavra-ai-agent-baseline]                                                                         │
│ --index              INTEGER  [default: -1]                                                                                              │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra saas contract`

```text
                                                                                                                                            
 Usage: python -m cavra.cli saas contract [OPTIONS]                                                                                         
                                                                                                                                            
 Print the public-safe SaaS Control Plane contract description.                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra saas operating-automation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli saas operating-automation [OPTIONS] TENANT_ID                                                                   
                                                                                                                                            
 Print a public-safe SaaS operating automation request and placeholder response.                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    tenant_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --requested-by                          TEXT  [default: community]                                                                       │
│ --automation-scope                      TEXT  [default: trial-to-paid-customer-scale]                                                    │
│ --automation-cadence                    TEXT  [default: daily]                                                                           │
│ --required-check                        TEXT                                                                                             │
│ --automation-status                     TEXT  [default: unknown]                                                                         │
│ --billing-monitoring-status             TEXT  [default: unknown]                                                                         │
│ --license-telemetry-status              TEXT  [default: unknown]                                                                         │
│ --support-followup-status               TEXT  [default: unknown]                                                                         │
│ --customer-success-review-status        TEXT  [default: unknown]                                                                         │
│ --dashboard-refresh-status              TEXT  [default: unknown]                                                                         │
│ --escalation-drill-status               TEXT  [default: unknown]                                                                         │
│ --closeout-retry-status                 TEXT  [default: unknown]                                                                         │
│ --blocker                               TEXT                                                                                             │
│ --help                                        Show this message and exit.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra saas worker-handoff`

```text
                                                                                                                                            
 Usage: python -m cavra.cli saas worker-handoff [OPTIONS] TENANT_ID                                                                         
                                                                                                                                            
 Print a public-safe SaaS operating automation worker handoff request and response.                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    tenant_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --requested-by                  TEXT  [default: community]                                                                               │
│ --deployment-environment        TEXT  [default: production]                                                                              │
│ --worker-mode                   TEXT  [default: dry_run]                                                                                 │
│ --required-check                TEXT                                                                                                     │
│ --worker-target                 TEXT                                                                                                     │
│ --handoff-status                TEXT  [default: requires_private_service]                                                                │
│ --scheduler-ref                 TEXT  [default: scheduler-pending]                                                                       │
│ --evidence-sink-ref             TEXT  [default: evidence-sink-pending]                                                                   │
│ --retry-policy-ref              TEXT  [default: retry-policy-pending]                                                                    │
│ --worker-owner                  TEXT  [default: operations-owner]                                                                        │
│ --blocker                       TEXT                                                                                                     │
│ --help                                Show this message and exit.                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-pilot-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-pilot-readiness [OPTIONS]                                                                            
                                                                                                                                            
 Show opt-in Go backend pilot readiness.                                                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                               TEXT   [default: disabled]                                                                          │
│ --runtime-path                       TEXT                                                                                                │
│ --policy-path                        TEXT                                                                                                │
│ --registry-path                      TEXT                                                                                                │
│ --package-dir                        TEXT                                                                                                │
│ --endpoint-deployment-path           TEXT                                                                                                │
│ --ci-runner-bundles-path             TEXT                                                                                                │
│ --channel-manifest-path              TEXT                                                                                                │
│ --updater-policy-path                TEXT                                                                                                │
│ --promotion-evidence-path            TEXT                                                                                                │
│ --rollback-plan-path                 TEXT                                                                                                │
│ --rollback-rehearsal-path            TEXT                                                                                                │
│ --rollback-drill-history-path        TEXT                                                                                                │
│ --rollback-drill-max-age-days        FLOAT  [default: 90.0]                                                                              │
│ --timeout-seconds                    FLOAT  [default: 5.0]                                                                               │
│ --json                                      Print readiness JSON.                                                                        │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-deployment-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-deployment-readiness                                                                                 
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show Go backend CI runner and workstation deployment readiness.                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                            TEXT  [default: disabled]                                                                              │
│ --package-dir                     TEXT                                                                                                   │
│ --endpoint-deployment-path        TEXT                                                                                                   │
│ --ci-runner-bundles-path          TEXT                                                                                                   │
│ --channel-manifest-path           TEXT                                                                                                   │
│ --updater-policy-path             TEXT                                                                                                   │
│ --json                                  Print deployment readiness JSON.                                                                 │
│ --help                                  Show this message and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-promotion-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-promotion-readiness [OPTIONS]                                                                        
                                                                                                                                            
 Show Go backend promotion readiness for optional backend use.                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                               TEXT   [default: disabled]                                                                          │
│ --runtime-path                       TEXT                                                                                                │
│ --policy-path                        TEXT                                                                                                │
│ --registry-path                      TEXT                                                                                                │
│ --package-dir                        TEXT                                                                                                │
│ --endpoint-deployment-path           TEXT                                                                                                │
│ --ci-runner-bundles-path             TEXT                                                                                                │
│ --channel-manifest-path              TEXT                                                                                                │
│ --updater-policy-path                TEXT                                                                                                │
│ --promotion-evidence-path            TEXT                                                                                                │
│ --rollback-plan-path                 TEXT                                                                                                │
│ --rollback-rehearsal-path            TEXT                                                                                                │
│ --rollback-drill-history-path        TEXT                                                                                                │
│ --rollback-drill-max-age-days        FLOAT  [default: 90.0]                                                                              │
│ --timeout-seconds                    FLOAT  [default: 5.0]                                                                               │
│ --json                                      Print promotion readiness JSON.                                                              │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-rollback-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-readiness [OPTIONS]                                                                         
                                                                                                                                            
 Show Go backend rollback readiness for promoted pilots.                                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                           TEXT  [default: disabled]                                                                               │
│ --rollback-plan-path             TEXT                                                                                                    │
│ --rollback-rehearsal-path        TEXT                                                                                                    │
│ --json                                 Print rollback readiness JSON.                                                                    │
│ --help                                 Show this message and exit.                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-rollback-rehearsal`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-rehearsal [OPTIONS]                                                                         
                                                                                                                                            
 Show automated rollback rehearsal evidence status for promoted Go pilots.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                               TEXT   [default: disabled]                                                                          │
│ --rollback-plan-path                 TEXT                                                                                                │
│ --rollback-rehearsal-path            TEXT                                                                                                │
│ --rollback-drill-history-path        TEXT                                                                                                │
│ --rollback-drill-max-age-days        FLOAT  [default: 90.0]                                                                              │
│ --json                                      Print rollback rehearsal JSON.                                                               │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-rollback-drills`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-drills [OPTIONS]                                                                            
                                                                                                                                            
 Show operational rollback drill history status for promoted Go pilots.                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                               TEXT   [default: disabled]                                                                          │
│ --rollback-drill-history-path        TEXT                                                                                                │
│ --rollback-drill-max-age-days        FLOAT  [default: 90.0]                                                                              │
│ --json                                      Print rollback drill history JSON.                                                           │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-rollback-drill-schedule`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-drill-schedule                                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show recurring rollback drill schedule and stale-drill notification readiness.                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                                TEXT   [default: disabled]                                                                         │
│ --rollback-drill-history-path         TEXT                                                                                               │
│ --rollback-drill-max-age-days         FLOAT  [default: 90.0]                                                                             │
│ --rollback-drill-schedule-path        TEXT                                                                                               │
│ --rollback-drill-due-soon-days        FLOAT  [default: 14.0]                                                                             │
│ --json                                       Print rollback drill schedule JSON.                                                         │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-rollback-drill-notification-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-drill-notification-plan                                                                     
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Build a public-safe stale rollback drill notification plan.                                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --mode                                          TEXT  [default: disabled]                                                                │
│ --rollback-drill-history-path                   TEXT                                                                                     │
│ --rollback-drill-schedule-path                  TEXT                                                                                     │
│ --routing-policy                                PATH                                                                                     │
│ --provider                                      TEXT  [default: all]                                                                     │
│ --force                           --no-force          [default: no-force]                                                                │
│ --json                                                Print notification plan JSON.                                                      │
│ --help                                                Show this message and exit.                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-rollback-drill-notification-ack`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-drill-notification-ack                                                                      
            [OPTIONS] SCHEDULE_ID                                                                                                           
                                                                                                                                            
 Build public-safe rollback drill notification acknowledgement metadata.                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    schedule_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --provider                     TEXT                                                                                                      │
│ --acknowledged-by              TEXT                                                                                                      │
│ --acknowledgement-state        TEXT  [default: acknowledged]                                                                             │
│ --plan-id                      TEXT                                                                                                      │
│ --external-ref                 TEXT                                                                                                      │
│ --notes                        TEXT                                                                                                      │
│ --json                               Print acknowledgement JSON.                                                                         │
│ --help                               Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-rollback-drill-escalation-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-rollback-drill-escalation-plan                                                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Build an empty public-safe rollback drill notification escalation plan template.                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --acknowledgement-minutes        INTEGER  [default: 60]                                                                                  │
│ --routing-policy                 PATH                                                                                                    │
│ --json                                    Print escalation plan JSON.                                                                    │
│ --help                                    Show this message and exit.                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra runtime go-pilot-evaluate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli runtime go-pilot-evaluate [OPTIONS] ACTION_TYPE                                                                 
                                                      TARGET                                                                                
                                                                                                                                            
 Evaluate through the opt-in Go backend pilot with Python fallback.                                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action_type      TEXT  [required]                                                                                                   │
│ *    target           TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack                         TEXT   [default: cavra-ai-agent-baseline]                                                          │
│ --mode                                TEXT   [default: shadow]                                                                           │
│ --runtime-path                        TEXT                                                                                               │
│ --policy-path                         TEXT                                                                                               │
│ --registry-path                       TEXT                                                                                               │
│ --package-dir                         TEXT                                                                                               │
│ --endpoint-deployment-path            TEXT                                                                                               │
│ --ci-runner-bundles-path              TEXT                                                                                               │
│ --channel-manifest-path               TEXT                                                                                               │
│ --updater-policy-path                 TEXT                                                                                               │
│ --promotion-evidence-path             TEXT                                                                                               │
│ --rollback-plan-path                  TEXT                                                                                               │
│ --rollback-rehearsal-path             TEXT                                                                                               │
│ --rollback-drill-history-path         TEXT                                                                                               │
│ --rollback-drill-max-age-days         FLOAT  [default: 90.0]                                                                             │
│ --rollback-drill-schedule-path        TEXT                                                                                               │
│ --rollback-drill-due-soon-days        FLOAT  [default: 14.0]                                                                             │
│ --timeout-seconds                     FLOAT  [default: 5.0]                                                                              │
│ --operation                           TEXT                                                                                               │
│ --tool                                TEXT   [default: unknown]                                                                          │
│ --capability                          TEXT                                                                                               │
│ --json                                       Print evaluation JSON.                                                                      │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra agent start`

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent start [OPTIONS] TOOL                                                                                      
                                                                                                                                            
 Start an AI agent governance session.                                                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    tool      TEXT  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo               PATH  [default: .]                                                                                                  │
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --output             PATH  [default: .cavra]                                                                                             │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra agent exec`

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent exec [OPTIONS] COMMAND                                                                                    
                                                                                                                                            
 Execute a command under governance policy.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    command      TEXT  [required]                                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --tool               TEXT  [default: claude-code]                                                                                        │
│ --repo               PATH  [default: .]                                                                                                  │
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --output             PATH  [default: .cavra]                                                                                             │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra agent attest`

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent attest [OPTIONS] SESSION_ID                                                                               
                                                                                                                                            
 Generate PR attestation from audit session.                                                                                                
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    session_id      TEXT  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --audit-dir        PATH  [default: .cavra]                                                                                               │
│ --format           TEXT  [default: markdown]                                                                                             │
│ --help                   Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra agent enforcement-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli agent enforcement-readiness [OPTIONS]                                                                           
                                                                                                                                            
 Report whether a repository can enforce CAVRA for AI coding agents.                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root        PATH  [default: .]                                                                                                    │
│ --settings         PATH                                                                                                                  │
│ --json                   Print the full readiness report JSON.                                                                           │
│ --help                   Show this message and exit.                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy list`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy list [OPTIONS]                                                                                           
                                                                                                                                            
 List available policy packs.                                                                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy validate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy validate [OPTIONS] PATH                                                                                  
                                                                                                                                            
 Validate a policy pack against the CAVRA JSON Schema.                                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy test`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy test [OPTIONS]                                                                                           
                                                                                                                                            
 Run core CAVRA policy assertions.                                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy explain`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy explain [OPTIONS] ACTION_TYPE TARGET                                                                     
                                                                                                                                            
 Explain the policy decision for an action.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    action_type      TEXT  [required]                                                                                                   │
│ *    target           TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy compile`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy compile [OPTIONS]                                                                                        
                                                                                                                                            
 Compile a policy pack and optional overlays to normalized JSON.                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --overlay            PATH                                                                                                                │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy rego-export`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy rego-export [OPTIONS]                                                                                    
                                                                                                                                            
 Export a CAVRA policy pack to a public-safe OPA/Rego compatibility bundle.                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --output-dir         PATH  [default: dist/opa-rego]                                                                                      │
│ --overlay            PATH                                                                                                                │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy rego-test`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy rego-test [OPTIONS]                                                                                      
                                                                                                                                            
 Run Rego/Python parity tests for the generated policy path.                                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy rego-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy rego-readiness [OPTIONS] PACKET                                                                          
                                                                                                                                            
 Validate an OPA/Rego policy readiness packet.                                                                                              
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy lifecycle-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy lifecycle-plan [OPTIONS]                                                                                 
                                                                                                                                            
 Export policy lifecycle lint, version, shadow, dry-run, rollback, and approval artifacts.                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack                 TEXT  [default: cavra-ai-agent-baseline]                                                                   │
│ --previous-policy-pack        TEXT                                                                                                       │
│ --output-dir                  PATH  [default: dist/policy-lifecycle]                                                                     │
│ --requested-by                TEXT  [default: policy-owner@example.com]                                                                  │
│ --source-ref                  TEXT  [default: git://Huzefaaa2/cavra/main/policies]                                                       │
│ --help                              Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy lifecycle-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy lifecycle-readiness [OPTIONS] PACKET                                                                     
                                                                                                                                            
 Validate a policy lifecycle readiness packet.                                                                                              
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    packet      PATH  [required]                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-live    --no-require-live      [default: no-require-live]                                                                      │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy diff`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy diff [OPTIONS] LEFT RIGHT                                                                                
                                                                                                                                            
 Show a semantic diff between two policies.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    left       PATH  [required]                                                                                                         │
│ *    right      PATH  [required]                                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy sign`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy sign [OPTIONS] PATH                                                                                      
                                                                                                                                            
 Create CAVRA policy signature metadata.                                                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --signer             TEXT  [default: local]                                                                                              │
│ --key                TEXT                                                                                                                │
│ --private-key        PATH                                                                                                                │
│ --key-id             TEXT                                                                                                                │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy verify`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy verify [OPTIONS] PATH                                                                                    
                                                                                                                                            
 Verify CAVRA policy signature metadata.                                                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    path      PATH  [required]                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --signature         PATH                                                                                                                 │
│ --key               TEXT                                                                                                                 │
│ --public-key        PATH                                                                                                                 │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy keygen`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy keygen [OPTIONS]                                                                                         
                                                                                                                                            
 Generate a local Ed25519 keypair for public policy signing workflows.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output        PATH  [default: .cavra/policy-signing]                                                                                   │
│ --key-id        TEXT  [default: local-policy-signing-key]                                                                                │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy simulate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy simulate [OPTIONS]                                                                                       
                                                                                                                                            
 Simulate the flagship CAVRA decision sequence.                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy dry-run`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy dry-run [OPTIONS]                                                                                        
                                                                                                                                            
 Run policy simulation without enforcing changes.                                                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy init`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy init [OPTIONS]                                                                                           
                                                                                                                                            
 Create a starter CAVRA policy.                                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --destination        PATH  [default: .cavra/policy.yaml]                                                                                 │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra policy describe`

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy describe [OPTIONS] PACK_ID                                                                               
                                                                                                                                            
 Describe a policy pack.                                                                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    pack_id      TEXT  [required]                                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra init claude-code`

```text
                                                                                                                                            
 Usage: python -m cavra.cli init claude-code [OPTIONS]                                                                                      
                                                                                                                                            
 Initialize first-class Claude Code governance with CAVRA.                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence bundle`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence bundle [OPTIONS]                                                                                       
                                                                                                                                            
 Generate a CAVRA evidence bundle from the flagship decision sequence.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                               PATH     [default: .cavra/evidence/latest]                                                        │
│ --policy-pack                          TEXT     [default: cavra-ai-agent-baseline]                                                       │
│ --signer                               TEXT     [default: local]                                                                         │
│ --key                                  TEXT                                                                                              │
│ --private-key                          PATH                                                                                              │
│ --key-id                               TEXT                                                                                              │
│ --retention-days                       INTEGER  [default: 2555]                                                                          │
│ --classification                       TEXT     [default: regulated-sdlc]                                                                │
│ --legal-hold        --no-legal-hold             [default: no-legal-hold]                                                                 │
│ --help                                          Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence generate-keypair`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence generate-keypair [OPTIONS]                                                                             
                                                                                                                                            
 Generate an Ed25519 keypair for evidence manifest signatures.                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --private-key        PATH  [default: .cavra/keys/evidence-ed25519-private.pem]                                                           │
│ --public-key         PATH  [default: .cavra/keys/evidence-ed25519-public.pem]                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence trust-root`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence trust-root [OPTIONS] PUBLIC_KEY                                                                        
                                                                                                                                            
 Create a CAVRA evidence signing trust-root document.                                                                                       
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    public_key      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output        PATH  [default: .cavra/keys/evidence-trust-root.json]                                                                    │
│ --key-id        TEXT                                                                                                                     │
│ --owner         TEXT  [default: platform-security]                                                                                       │
│ --status        TEXT  [default: active]                                                                                                  │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence trust-bundle`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence trust-bundle [OPTIONS] TRUST_ROOTS...                                                                  
                                                                                                                                            
 Create a distributable bundle of CAVRA evidence trust roots.                                                                               
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    trust_roots      TRUST_ROOTS...  [required]                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output        PATH  [default: .cavra/keys/evidence-trust-roots.json]                                                                   │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence trust-distribution`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence trust-distribution [OPTIONS]                                                                           
                                                        TRUST_ROOTS...                                                                      
                                                                                                                                            
 Create an offline distribution package for CAVRA evidence trust roots.                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    trust_roots      TRUST_ROOTS...  [required]                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                 PATH  [default: .cavra/keys/trust-root-distribution]                                                            │
│ --environment            TEXT  [default: production]                                                                                     │
│ --distribution-id        TEXT                                                                                                            │
│ --channel                TEXT                                                                                                            │
│ --help                         Show this message and exit.                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence verify`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence verify [OPTIONS] BUNDLE_DIR                                                                            
                                                                                                                                            
 Verify evidence bundle manifest, checksums, and optional signature.                                                                        
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --key                           TEXT                                                                                                     │
│ --public-key                    PATH                                                                                                     │
│ --trust-root                    PATH                                                                                                     │
│ --key-id                        TEXT                                                                                                     │
│ --minimum-retention-days        INTEGER                                                                                                  │
│ --help                                   Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence siem-event`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence siem-event [OPTIONS] BUNDLE_DIR                                                                        
                                                                                                                                            
 Print the SIEM event from an evidence bundle.                                                                                              
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence retention-policy`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence retention-policy [OPTIONS] BUNDLE_DIR                                                                  
                                                                                                                                            
 Export evidence retention controls for an existing bundle.                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                               PATH     [default: .cavra/evidence/retention]                                                     │
│ --retention-days                       INTEGER  [default: 2555]                                                                          │
│ --classification                       TEXT     [default: regulated-sdlc]                                                                │
│ --legal-hold        --no-legal-hold             [default: no-legal-hold]                                                                 │
│ --help                                          Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence export-siem`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence export-siem [OPTIONS] BUNDLE_DIR                                                                       
                                                                                                                                            
 Export provider-specific SIEM payloads from an evidence bundle.                                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                 PATH  [default: .cavra/evidence/export]                                                                         │
│ --provider               TEXT  [default: all]                                                                                            │
│ --splunk-index           TEXT  [default: cavra]                                                                                          │
│ --datadog-service        TEXT  [default: cavra]                                                                                          │
│ --help                         Show this message and exit.                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence storage-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence storage-plan [OPTIONS] BUNDLE_DIR                                                                      
                                                                                                                                            
 Create S3 Object Lock and Azure immutable blob reference plans.                                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                 PATH     [default: .cavra/evidence/storage]                                                                     │
│ --retention-days         INTEGER  [default: 2555]                                                                                        │
│ --s3-bucket              TEXT     [default: cavra-evidence]                                                                              │
│ --s3-prefix              TEXT     [default: evidence/]                                                                                   │
│ --azure-account          TEXT     [default: cavraevidence]                                                                               │
│ --azure-container        TEXT     [default: evidence]                                                                                    │
│ --help                            Show this message and exit.                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence verify-attestation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence verify-attestation [OPTIONS] BUNDLE_DIR                                                                
                                                                                                                                            
 Verify PR attestation content against bundle evidence.                                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output        PATH  [default: .cavra/evidence/attestation]                                                                             │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence index [OPTIONS] BUNDLE_DIR                                                                             
                                                                                                                                            
 Persist searchable evidence metadata from a bundle.                                                                                        
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_dir      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store         PATH  [default: .cavra/evidence/metadata.json]                                                                           │
│ --sqlite        PATH                                                                                                                     │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence search`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence search [OPTIONS]                                                                                       
                                                                                                                                            
 Search SQLite-backed evidence metadata with filters and pagination.                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --sqlite                                              PATH     [default: .cavra/evidence/metadata.db]                                    │
│ --session-id                                          TEXT                                                                               │
│ --signer                                              TEXT                                                                               │
│ --min-blocked                                         INTEGER                                                                            │
│ --has-approvals                 --no-has-approvals                                                                                       │
│ --metadata-kind                                       TEXT                                                                               │
│ --rollout-status                                      TEXT                                                                               │
│ --environment                                         TEXT                                                                               │
│ --deployment-target                                   TEXT                                                                               │
│ --target-ring                                         TEXT                                                                               │
│ --approval-state                                      TEXT                                                                               │
│ --promotion-execution-status                          TEXT                                                                               │
│ --rollback-execution-status                           TEXT                                                                               │
│ --limit                                               INTEGER  [default: 50]                                                             │
│ --offset                                              INTEGER  [default: 0]                                                              │
│ --help                                                         Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra evidence migrate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli evidence migrate [OPTIONS]                                                                                      
                                                                                                                                            
 Apply SQLite migrations for evidence metadata search.                                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --sqlite                PATH  [default: .cavra/evidence/metadata.db]                                                                     │
│ --migrations-dir        PATH  [default: migrations/sqlite]                                                                               │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval create`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval create [OPTIONS] DECISION_FILE                                                                         
                                                                                                                                            
 Create a pending approval request from a CAVRA decision.                                                                                   
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    decision_file      PATH  [required]                                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH     [default: .cavra/approvals.json]                                                                        │
│ --sqlite                PATH                                                                                                             │
│ --approver-group        TEXT                                                                                                             │
│ --routing-file          PATH                                                                                                             │
│ --requested-by          TEXT     [default: ai-agent]                                                                                     │
│ --ttl-hours             INTEGER  [default: 24]                                                                                           │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval list`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval list [OPTIONS]                                                                                         
                                                                                                                                            
 List approval queue entries.                                                                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH     [default: .cavra/approvals.json]                                                                        │
│ --sqlite                PATH                                                                                                             │
│ --state                 TEXT                                                                                                             │
│ --approver-group        TEXT                                                                                                             │
│ --limit                 INTEGER  [default: 50]                                                                                           │
│ --offset                INTEGER  [default: 0]                                                                                            │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval approve`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval approve [OPTIONS] APPROVAL_ID                                                                          
                                                                                                                                            
 Approve a pending request.                                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    approval_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store               PATH  [default: .cavra/approvals.json]                                                                             │
│ --sqlite              PATH                                                                                                               │
│ --actor               TEXT                                                                                                               │
│ --actor-claims        PATH                                                                                                               │
│ --actor-token         PATH                                                                                                               │
│ --oidc-config         PATH                                                                                                               │
│ --rbac-file           PATH                                                                                                               │
│ --reason              TEXT                                                                                                               │
│ --external-ref        TEXT                                                                                                               │
│ --help                      Show this message and exit.                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval deny`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval deny [OPTIONS] APPROVAL_ID                                                                             
                                                                                                                                            
 Deny a pending request.                                                                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    approval_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store               PATH  [default: .cavra/approvals.json]                                                                             │
│ --sqlite              PATH                                                                                                               │
│ --actor               TEXT                                                                                                               │
│ --actor-claims        PATH                                                                                                               │
│ --actor-token         PATH                                                                                                               │
│ --oidc-config         PATH                                                                                                               │
│ --rbac-file           PATH                                                                                                               │
│ --reason              TEXT                                                                                                               │
│ --external-ref        TEXT                                                                                                               │
│ --help                      Show this message and exit.                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval expire`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval expire [OPTIONS] APPROVAL_ID                                                                           
                                                                                                                                            
 Expire a pending request.                                                                                                                  
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    approval_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store         PATH  [default: .cavra/approvals.json]                                                                                   │
│ --sqlite        PATH                                                                                                                     │
│ --actor         TEXT  [default: system]                                                                                                  │
│ --reason        TEXT  [default: approval expired]                                                                                        │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval break-glass`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval break-glass [OPTIONS] DECISION_FILE                                                                    
                                                                                                                                            
 Record a break-glass override with mandatory evidence.                                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    decision_file      PATH  [required]                                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH     [default: .cavra/approvals.json]                                                                        │
│ --sqlite                PATH                                                                                                             │
│ --actor                 TEXT                                                                                                             │
│ --reason                TEXT                                                                                                             │
│ --approver-group        TEXT     [default: Change Advisory Board]                                                                        │
│ --external-ref          TEXT                                                                                                             │
│ --ttl-hours             INTEGER  [default: 4]                                                                                            │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval route`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval route [OPTIONS] DECISION_FILE                                                                          
                                                                                                                                            
 Show the approver group selected by approval routing policy.                                                                               
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    decision_file      PATH  [required]                                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --routing-file        PATH                                                                                                               │
│ --help                      Show this message and exit.                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval export-notifications`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval export-notifications [OPTIONS] APPROVAL_ID                                                             
                                                                                                                                            
 Export reference notification payloads for approval providers.                                                                             
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    approval_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store           PATH  [default: .cavra/approvals.json]                                                                                 │
│ --sqlite          PATH                                                                                                                   │
│ --output          PATH  [default: .cavra/approvals/notifications]                                                                        │
│ --provider        TEXT  [default: all]                                                                                                   │
│ --help                  Show this message and exit.                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval provider-requests`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval provider-requests [OPTIONS] APPROVAL_ID                                                                
                                                                                                                                            
 Export credential-free HTTP request specs for approval providers.                                                                          
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    approval_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store           PATH  [default: .cavra/approvals.json]                                                                                 │
│ --sqlite          PATH                                                                                                                   │
│ --output          PATH  [default: .cavra/approvals/provider-requests]                                                                    │
│ --provider        TEXT  [default: all]                                                                                                   │
│ --help                  Show this message and exit.                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval deliver`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval deliver [OPTIONS] APPROVAL_ID                                                                          
                                                                                                                                            
 Send live approval provider requests and write redacted delivery evidence.                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    approval_id      TEXT  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                  PATH     [default: .cavra/approvals.json]                                                                       │
│ --sqlite                 PATH                                                                                                            │
│ --config                 PATH                                                                                                            │
│ --output                 PATH     [default: .cavra/approvals/deliveries]                                                                 │
│ --provider               TEXT     [default: all]                                                                                         │
│ --retries                INTEGER  [default: 2]                                                                                           │
│ --timeout-seconds        FLOAT    [default: 10.0]                                                                                        │
│ --help                            Show this message and exit.                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra integration deliver`

```text
                                                                                                                                            
 Usage: python -m cavra.cli integration deliver [OPTIONS] EVENT                                                                             
                                                                                                                                            
 Send live connector requests and write redacted delivery evidence.                                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    event      PATH  [required]                                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --output                 PATH     [default: .cavra/integrations/deliveries]                                                           │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra approval migrate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli approval migrate [OPTIONS]                                                                                      
                                                                                                                                            
 Apply SQLite migrations for approval persistence.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --sqlite                PATH  [default: .cavra/approvals.db]                                                                             │
│ --migrations-dir        PATH  [default: migrations/sqlite]                                                                               │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry agent-register`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry agent-register [OPTIONS] AGENT_ID                                                                      
                                                                                                                                            
 Register or update a governed AI-agent identity.                                                                                           
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    agent_id      TEXT  [required]                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store             PATH  [default: .cavra/registry.json]                                                                                │
│ --sqlite            PATH                                                                                                                 │
│ --agent-type        TEXT  [default: coding-agent]                                                                                        │
│ --vendor            TEXT  [default: unknown]                                                                                             │
│ --version           TEXT  [default: unknown]                                                                                             │
│ --capability        TEXT                                                                                                                 │
│ --scope             TEXT                                                                                                                 │
│ --repository        TEXT                                                                                                                 │
│ --tool              TEXT                                                                                                                 │
│ --risk-tier         TEXT  [default: medium]                                                                                              │
│ --owner             TEXT  [default: unassigned]                                                                                          │
│ --status            TEXT  [default: active]                                                                                              │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry agent-list`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry agent-list [OPTIONS]                                                                                   
                                                                                                                                            
 List governed AI-agent identities.                                                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store         PATH  [default: .cavra/registry.json]                                                                                    │
│ --sqlite        PATH                                                                                                                     │
│ --status        TEXT                                                                                                                     │
│ --owner         TEXT                                                                                                                     │
│ --help                Show this message and exit.                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry profiles`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry profiles [OPTIONS]                                                                                     
                                                                                                                                            
 List predefined AI-agent capability profiles.                                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry mcp-register`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry mcp-register [OPTIONS] SERVER_ID                                                                       
                                                                                                                                            
 Register or update an MCP server trust record.                                                                                             
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    server_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH  [default: .cavra/registry.json]                                                                            │
│ --sqlite                PATH                                                                                                             │
│ --name                  TEXT                                                                                                             │
│ --trust-tier            TEXT  [default: unknown]                                                                                         │
│ --capability            TEXT                                                                                                             │
│ --owner                 TEXT  [default: unassigned]                                                                                      │
│ --approval-state        TEXT  [default: pending]                                                                                         │
│ --tool                  TEXT                                                                                                             │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry mcp-list`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry mcp-list [OPTIONS]                                                                                     
                                                                                                                                            
 List MCP server trust records.                                                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store                 PATH  [default: .cavra/registry.json]                                                                            │
│ --sqlite                PATH                                                                                                             │
│ --trust-tier            TEXT                                                                                                             │
│ --approval-state        TEXT                                                                                                             │
│ --capability            TEXT                                                                                                             │
│ --help                        Show this message and exit.                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry mcp-check`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry mcp-check [OPTIONS] SERVER_ID TOOL                                                                     
                                                                                                                                            
 Evaluate an MCP tool call against the trust registry.                                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    server_id      TEXT  [required]                                                                                                     │
│ *    tool           TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --store             PATH  [default: .cavra/registry.json]                                                                                │
│ --sqlite            PATH                                                                                                                 │
│ --capability        TEXT                                                                                                                 │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry mcp-classifications`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry mcp-classifications [OPTIONS]                                                                          
                                                                                                                                            
 List MCP tool capability classifications.                                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --capability        TEXT                                                                                                                 │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra registry migrate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli registry migrate [OPTIONS]                                                                                      
                                                                                                                                            
 Apply SQLite migrations for the registry and other CAVRA metadata tables.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --sqlite            PATH  [default: .cavra/registry.db]                                                                                  │
│ --migrations        PATH  [default: migrations/sqlite]                                                                                   │
│ --help                    Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ops stores`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops stores [OPTIONS]                                                                                            
                                                                                                                                            
 List configured persistent API stores and whether each path exists.                                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ops backup`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops backup [OPTIONS]                                                                                            
                                                                                                                                            
 Back up configured JSON and SQLite persistent API stores.                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                     PATH  [default: .cavra/backups/latest]                                                      │
│ --include-missing    --no-include-missing          [default: no-include-missing]                                                         │
│ --help                                             Show this message and exit.                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ops restore`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops restore [OPTIONS] MANIFEST                                                                                  
                                                                                                                                            
 Restore a persistent API backup after checksum validation.                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    manifest      PATH  [required]                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --target-dir                      PATH                                                                                                   │
│ --overwrite     --no-overwrite          [default: no-overwrite]                                                                          │
│ --help                                  Show this message and exit.                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra ops retention-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli ops retention-plan [OPTIONS]                                                                                    
                                                                                                                                            
 Export backup, restore-test, and retention controls for persistent API stores.                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                               PATH     [default: .cavra/operations/retention]                                                   │
│ --retention-days                       INTEGER  [default: 2555]                                                                          │
│ --classification                       TEXT     [default: regulated-sdlc]                                                                │
│ --legal-hold        --no-legal-hold             [default: no-legal-hold]                                                                 │
│ --help                                          Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release phase6-rollup`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release phase6-rollup [OPTIONS]                                                                                 
                                                                                                                                            
 Validate or export the Phase 6 ecosystem expansion rollup.                                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                                 PATH                                                                            │
│ --repo-root                                              PATH  [default: .]                                                              │
│ --export-dir                                             PATH                                                                            │
│ --require-customer-live    --no-require-customer-live          [default: no-require-customer-live]                                       │
│ --help                                                         Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release phase4-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release phase4-closeout [OPTIONS]                                                                               
                                                                                                                                            
 Validate or export the Phase 4 connector and scanner closeout.                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                                 PATH                                                                            │
│ --repo-root                                              PATH  [default: .]                                                              │
│ --export-dir                                             PATH                                                                            │
│ --require-customer-live    --no-require-customer-live          [default: no-require-customer-live]                                       │
│ --help                                                         Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release phase5-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release phase5-closeout [OPTIONS]                                                                               
                                                                                                                                            
 Validate or export the Phase 5 policy lifecycle and event core closeout.                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                                 PATH                                                                            │
│ --repo-root                                              PATH  [default: .]                                                              │
│ --export-dir                                             PATH                                                                            │
│ --require-customer-live    --no-require-customer-live          [default: no-require-customer-live]                                       │
│ --help                                                         Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-live-evidence`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-live-evidence [OPTIONS]                                                                        
                                                                                                                                            
 Validate or export the customer-live evidence intake packet.                                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-evidence-room`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-evidence-room [OPTIONS]                                                                        
                                                                                                                                            
 Validate or export the customer evidence-room closeout index.                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --index                                 PATH                                                                                             │
│ --intake-packet                         PATH                                                                                             │
│ --export-dir                            PATH                                                                                             │
│ --require-live     --no-require-live          [default: no-require-live]                                                                 │
│ --help                                        Show this message and exit.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-closeout-handoff`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-closeout-handoff                                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer closeout handoff packet.                                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                      PATH                                                                                       │
│ --evidence-room-index                         PATH                                                                                       │
│ --export-dir                                  PATH                                                                                       │
│ --require-live           --no-require-live          [default: no-require-live]                                                           │
│ --help                                              Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-operating-review`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-operating-review                                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the recurring customer operating review packet.                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                   PATH                                                                                          │
│ --closeout-handoff                         PATH                                                                                          │
│ --export-dir                               PATH                                                                                          │
│ --require-live        --no-require-live          [default: no-require-live]                                                              │
│ --help                                           Show this message and exit.                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-renewal-expansion`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-renewal-expansion                                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer renewal and expansion readiness packet.                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                   PATH                                                                                          │
│ --operating-review                         PATH                                                                                          │
│ --export-dir                               PATH                                                                                          │
│ --require-live        --no-require-live          [default: no-require-live]                                                              │
│ --help                                           Show this message and exit.                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-renewal-outcome`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-renewal-outcome                                                                                
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer renewal outcome closeout packet.                                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                    PATH                                                                                         │
│ --renewal-expansion                         PATH                                                                                         │
│ --export-dir                                PATH                                                                                         │
│ --require-live         --no-require-live          [default: no-require-live]                                                             │
│ --help                                            Show this message and exit.                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-rollup`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-rollup                                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle executive rollup packet.                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-archive`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-archive                                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle archive manifest.                                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --rollup                               PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-status`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-status                                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle public status packet.                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --archive                              PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-final-seal`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-final-seal                                                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle final release seal packet.                                                                       
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --status                               PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-verification-index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-verification-index                                                                   
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle verification index.                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --index                                PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-live-validation-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-live-validation-plan                                                                 
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise live validation plan.                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --plan                                 PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-cutover-runbook`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-cutover-runbook                                                                      
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise cutover runbook.                                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --runbook                              PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-stabilization-report`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-stabilization-report                                                                 
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise post-cutover stabilization report.                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --report                               PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-steady-state-handoff`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-steady-state-handoff                                                                 
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise steady-state handoff packet.                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --handoff                              PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-operating-release-index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-operating-release-index                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise operating release index.                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --index                                PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-operating-announcement`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-operating-announcement                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise operating announcement packet.                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --announcement                         PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-operating-chain`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-operating-chain                                                                      
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the full Managed/Enterprise operating chain.                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --manifest                             PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-operating-certificate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-operating-certificate                                                                
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise operating release certificate.                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --certificate                          PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release managed-enterprise-certificate-publication-index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release managed-enterprise-certificate-publication-index                                                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the Managed/Enterprise certificate publication index.                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --index                                PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release roadmap-intake-gate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release roadmap-intake-gate [OPTIONS]                                                                           
                                                                                                                                            
 Validate or export the roadmap intake gate.                                                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --change-type                          TEXT  [default: customer_monitoring_cycle]                                                        │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release roadmap-candidate-charter`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release roadmap-candidate-charter                                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the roadmap candidate charter.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --charter                              PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --change-type                          TEXT  [default: new_product_capability]                                                           │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release roadmap-future-phase-opening-gate`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release roadmap-future-phase-opening-gate                                                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the roadmap future phase opening gate.                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --gate                                 PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --change-type                          TEXT  [default: new_product_capability]                                                           │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release roadmap-future-phase-registry`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release roadmap-future-phase-registry                                                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the roadmap future phase registry.                                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --registry                             PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --change-type                          TEXT  [default: new_product_capability]                                                           │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release roadmap-future-work-governance-index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release roadmap-future-work-governance-index                                                                    
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the roadmap future work governance index.                                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --index                                PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --change-type                          TEXT  [default: new_product_capability]                                                           │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release roadmap-governance-quickcheck`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release roadmap-governance-quickcheck                                                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate the closed roadmap boundary and future-work governance chain in one pass.                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --repo-root                            PATH  [default: .]                                                                                │
│ --index                                PATH                                                                                              │
│ --export-dir                           PATH                                                                                              │
│ --change-type                          TEXT  [default: new_product_capability]                                                           │
│ --output                               PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-announcement`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-announcement                                                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle closeout announcement packet.                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --index                                PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-retrospective`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-retrospective                                                                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle retrospective packet.                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --announcement                         PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-backlog`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-backlog                                                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 backlog packet.                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                                PATH                                                                                             │
│ --retrospective                         PATH                                                                                             │
│ --repo-root                             PATH  [default: .]                                                                               │
│ --export-dir                            PATH                                                                                             │
│ --require-live     --no-require-live          [default: no-require-live]                                                                 │
│ --help                                        Show this message and exit.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-kickoff`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-kickoff                                                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 kickoff packet.                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --backlog                              PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-sprint1-checkpoint`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-sprint1-checkpoint                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 Sprint 1 checkpoint packet.                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --kickoff                              PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-telemetry-depth`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-telemetry-depth                                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 telemetry depth packet.                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --sprint1                              PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-support-automation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-support-automation                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 support automation packet.                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --sprint1                              PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-lifecycle-analytics`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-lifecycle-analytics                                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 lifecycle analytics packet.                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --sprint1                              PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-customer-health-review`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-customer-health-review                                                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 customer health review packet.                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-executive-health-rollup`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-executive-health-rollup                                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 executive health rollup packet.                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-executive-action-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-executive-action-plan                                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 executive action plan packet.                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-action-followup-checkpoint`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-action-followup-checkpoint                                                    
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 action follow-up checkpoint packet.                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-executive-followup-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-executive-followup-closeout                                                   
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 executive follow-up closeout packet.                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-next-cycle-readiness-index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-next-cycle-readiness-index                                                    
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 next-cycle readiness index packet.                                                       
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-operating-scorecard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-operating-scorecard                                                    
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public operating scorecard packet.                                                       
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-publication-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-publication-closeout                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard publication closeout packet.                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-refresh-checkpoint`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-refresh-checkpoint                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard refresh checkpoint packet.                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-refresh-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-refresh-closeout                                             
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard refresh closeout packet.                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-operating-loop-index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-operating-loop-index                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard operating loop index packet.                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-executive-summary-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-executive-summary-closeout                                   
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard executive summary closeout packet.                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-distribution-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-distribution-readiness                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard distribution readiness packet.                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-distribution-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-distribution-closeout                                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard distribution closeout packet.                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-distribution-audit-index`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-distribution-audit-index                                     
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard distribution audit index packet.                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-audit-review-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-audit-review-closeout                                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard audit review closeout packet.                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard continuous monitoring readiness packet.                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard monitoring activation closeout packet.                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review                                
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard monitoring first-cycle review packet.                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard monitoring drift remediation closeout packet.                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle readiness packet.                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout                  
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle activation closeout packet.                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle first review packet.                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle drift remediation closeout packet.              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --packet                               PATH                                                                                              │
│ --repo-root                            PATH  [default: .]                                                                                │
│ --export-dir                           PATH                                                                                              │
│ --require-live    --no-require-live          [default: no-require-live]                                                                  │
│ --help                                       Show this message and exit.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release verify-go-package`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release verify-go-package [OPTIONS] PACKAGE_DIR                                                                 
                                                                                                                                            
 Verify a CAVRA Go runtime release package.                                                                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-signatures    --allow-unsigned                Require detached Ed25519 signatures for release artifacts.                       │
│                                                         [default: require-signatures]                                                    │
│ --require-provenance    --allow-missing-provenance      Require SLSA provenance for release artifacts. [default: require-provenance]     │
│ --json                                                  Print machine-readable verification output.                                      │
│ --help                                                  Show this message and exit.                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release verify-airgap-bundle`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release verify-airgap-bundle [OPTIONS] BUNDLE_PATH                                                              
                                                                                                                                            
 Verify an air-gapped CAVRA Go runtime release zip.                                                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    bundle_path      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --extract-dir                                         PATH                                                                               │
│ --require-signatures    --allow-unsigned                    Require detached Ed25519 signatures for release artifacts.                   │
│                                                             [default: require-signatures]                                                │
│ --require-provenance    --allow-missing-provenance          Require SLSA provenance for release artifacts. [default: require-provenance] │
│ --require-bootstrap     --allow-missing-bootstrap           Require offline trust-root bootstrap metadata. [default: require-bootstrap]  │
│ --json                                                      Print machine-readable verification output.                                  │
│ --help                                                      Show this message and exit.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release validate-upgrade`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release validate-upgrade [OPTIONS]                                                                              
                                                     PREVIOUS_PACKAGE_DIR                                                                   
                                                     CANDIDATE_PACKAGE_DIR                                                                  
                                                                                                                                            
 Validate a Go runtime release-candidate upgrade before promotion.                                                                          
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    previous_package_dir       PATH  [required]                                                                                         │
│ *    candidate_package_dir      PATH  [required]                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-signatures    --allow-unsigned                Require detached Ed25519 signatures for both release packages.                   │
│                                                         [default: require-signatures]                                                    │
│ --require-provenance    --allow-missing-provenance      Require SLSA provenance for both release packages. [default: require-provenance] │
│ --allow-same-version                                    Allow rebuilt release candidates with the same semantic version.                 │
│ --json                                                  Print machine-readable validation output.                                        │
│ --help                                                  Show this message and exit.                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release smoke-installers`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release smoke-installers [OPTIONS] PACKAGE_DIR                                                                  
                                                                                                                                            
 Smoke-test Go runtime installer metadata and the native packaged binary.                                                                   
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --require-signatures    --allow-unsigned                     Require detached Ed25519 signatures for release artifacts.                  │
│                                                              [default: require-signatures]                                               │
│ --require-provenance    --allow-missing-provenance           Require SLSA provenance for release artifacts.                              │
│                                                              [default: require-provenance]                                               │
│ --execute-native        --skip-execution                     Execute the packaged binary matching the current OS and architecture.       │
│                                                              [default: execute-native]                                                   │
│ --timeout-seconds                                     FLOAT  Native binary smoke-test timeout. [default: 5.0]                            │
│ --json                                                       Print machine-readable validation output.                                   │
│ --help                                                       Show this message and exit.                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release channel-manifest`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release channel-manifest [OPTIONS] PACKAGE_DIR                                                                  
                                                                                                                                            
 Inspect release package channel metadata for managed workstations.                                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --channel        TEXT                                                                                                                    │
│ --json                 Print machine-readable channel output.                                                                            │
│ --help                 Show this message and exit.                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release updater-policy`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release updater-policy [OPTIONS] PACKAGE_DIR                                                                    
                                                                                                                                            
 Inspect managed workstation updater policy for a release package.                                                                          
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --json          Print machine-readable updater policy output.                                                                            │
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release request-channel-promotion`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release request-channel-promotion                                                                               
            [OPTIONS] PACKAGE_DIR                                                                                                           
                                                                                                                                            
 Create a signed approval request for release channel promotion.                                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                              PATH     [default: .cavra/release/channel-promotion]                               │
│ --channel                                             TEXT     [default: stable]                                                         │
│ --target-ring                                         TEXT     [default: enterprise]                                                     │
│ --requested-by                                        TEXT     [default: release-manager]                                                │
│ --approver-group                                      TEXT     [default: Endpoint Change Advisory Board]                                 │
│ --ttl-hours                                           INTEGER  [default: 24]                                                             │
│ --signing-key                                         PATH                                                                               │
│ --signer                                              TEXT     [default: release-manager]                                                │
│ --approval-store                                      PATH                                                                               │
│ --approval-sqlite                                     PATH                                                                               │
│ --metadata-json                                       PATH                                                                               │
│ --sqlite                                              PATH                                                                               │
│ --require-signatures    --allow-unsigned                       Require detached Ed25519 signatures for referenced release artifacts.     │
│                                                                [default: require-signatures]                                             │
│ --require-provenance    --allow-missing-provenance             Require SLSA provenance for referenced release artifacts.                 │
│                                                                [default: require-provenance]                                             │
│ --json                                                         Print machine-readable channel promotion output.                          │
│ --help                                                         Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release export-endpoint-management`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release export-endpoint-management                                                                              
            [OPTIONS] PACKAGE_DIR                                                                                                           
                                                                                                                                            
 Export Jamf, Intune, and Linux endpoint-management bundles for a release channel.                                                          
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                              PATH  [default: .cavra/release/endpoint-management-export]                         │
│ --channel                                             TEXT  [default: stable]                                                            │
│ --provider                                            TEXT  [default: all]                                                               │
│ --promotion-request                                   PATH                                                                               │
│ --metadata-json                                       PATH                                                                               │
│ --sqlite                                              PATH                                                                               │
│ --require-signatures    --allow-unsigned                    Require detached Ed25519 signatures for referenced release artifacts.        │
│                                                             [default: require-signatures]                                                │
│ --require-provenance    --allow-missing-provenance          Require SLSA provenance for referenced release artifacts.                    │
│                                                             [default: require-provenance]                                                │
│ --json                                                      Print machine-readable endpoint export output.                               │
│ --help                                                      Show this message and exit.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-endpoint-export`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-endpoint-export                                                                                 
            [OPTIONS] EXPORT_MANIFEST                                                                                                       
                                                                                                                                            
 Publish an endpoint-management export to Jamf, Intune, or Linux fleet connectors.                                                          
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    export_manifest      PATH  [required]                                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --output                 PATH     [default: .cavra/release/endpoint-publication-deliveries]                                           │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --metadata-json          PATH                                                                                                         │
│    --sqlite                 PATH                                                                                                         │
│    --json                            Print machine-readable delivery output.                                                             │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release ingest-endpoint-inventory`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release ingest-endpoint-inventory                                                                               
            [OPTIONS] SOURCE_INVENTORY                                                                                                      
                                                                                                                                            
 Normalize provider endpoint inventory exports into CAVRA endpoint observations.                                                            
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    source_inventory      PATH  [required]                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --provider             TEXT  [default: linux]                                                                                            │
│ --output               PATH  [default: .cavra/release/endpoint-inventory]                                                                │
│ --channel              TEXT                                                                                                              │
│ --observed-at          TEXT                                                                                                              │
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH                                                                                                              │
│ --json                       Print machine-readable ingestion output.                                                                    │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release reconcile-endpoint-deployment`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release reconcile-endpoint-deployment                                                                           
            [OPTIONS] PACKAGE_DIR OBSERVED_INVENTORY                                                                                        
                                                                                                                                            
 Compare desired signed endpoint deployment state with observed endpoint inventory.                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir             PATH  [required]                                                                                            │
│ *    observed_inventory      PATH  [required]                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                                         PATH     [default: .cavra/release/endpoint-reconciliation]              │
│ --stale-after-hours                                              INTEGER  [default: 24]                                                  │
│ --metadata-json                                                  PATH                                                                    │
│ --sqlite                                                         PATH                                                                    │
│ --require-package-verification    --skip-package-verification             Verify the Go release package before reconciling observed      │
│                                                                           endpoints.                                                     │
│                                                                           [default: require-package-verification]                        │
│ --json                                                                    Print machine-readable reconciliation output.                  │
│ --help                                                                    Show this message and exit.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release capture-rollout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release capture-rollout [OPTIONS] PACKAGE_DIR                                                                   
                                                                                                                                            
 Capture rollout evidence for managed endpoint deployment targets.                                                                          
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                              PATH  [default: .cavra/release/rollout]                                            │
│ --deployment-id                                       TEXT                                                                               │
│ --environment                                         TEXT  [default: production]                                                        │
│ --rollout-id                                          TEXT                                                                               │
│ --rollout-ring                                        TEXT  [default: staging]                                                           │
│ --status                                              TEXT  [default: planned]                                                           │
│ --actor                                               TEXT  [default: release-manager]                                                   │
│ --change-record                                       TEXT  [default: unassigned]                                                        │
│ --require-signatures    --allow-unsigned                    Require detached Ed25519 signatures for release artifacts.                   │
│                                                             [default: require-signatures]                                                │
│ --require-provenance    --allow-missing-provenance          Require SLSA provenance for release artifacts. [default: require-provenance] │
│ --json                                                      Print machine-readable evidence output.                                      │
│ --help                                                      Show this message and exit.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release verify-rollout`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release verify-rollout [OPTIONS] ROLLOUT_DIR                                                                    
                                                                                                                                            
 Verify managed endpoint rollout evidence and optionally index its metadata.                                                                
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    rollout_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --package-dir                                                    PATH                                                                    │
│ --require-package-verification    --skip-package-verification          Verify the referenced release package while verifying rollout     │
│                                                                        evidence.                                                         │
│                                                                        [default: require-package-verification]                           │
│ --require-signatures              --allow-unsigned                     Require detached Ed25519 signatures for referenced release        │
│                                                                        artifacts.                                                        │
│                                                                        [default: require-signatures]                                     │
│ --require-provenance              --allow-missing-provenance           Require SLSA provenance for referenced release artifacts.         │
│                                                                        [default: require-provenance]                                     │
│ --metadata-json                                                  PATH                                                                    │
│ --sqlite                                                         PATH                                                                    │
│ --json                                                                 Print machine-readable verification output.                       │
│ --help                                                                 Show this message and exit.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release request-rollout-promotion`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release request-rollout-promotion                                                                               
            [OPTIONS] ROLLOUT_DIR                                                                                                           
                                                                                                                                            
 Create a signed approval request for endpoint rollout promotion.                                                                           
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    rollout_dir      PATH  [required]                                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                                         PATH     [default: .cavra/release/rollout-promotion]                    │
│ --target-ring                                                    TEXT     [default: production]                                          │
│ --requested-by                                                   TEXT     [default: release-manager]                                     │
│ --approver-group                                                 TEXT     [default: Change Advisory Board]                               │
│ --ttl-hours                                                      INTEGER  [default: 24]                                                  │
│ --signing-key                                                    PATH                                                                    │
│ --signer                                                         TEXT     [default: release-manager]                                     │
│ --package-dir                                                    PATH                                                                    │
│ --approval-store                                                 PATH                                                                    │
│ --approval-sqlite                                                PATH                                                                    │
│ --require-package-verification    --skip-package-verification             Verify the referenced release package while preparing the      │
│                                                                           promotion request.                                             │
│                                                                           [default: require-package-verification]                        │
│ --require-signatures              --allow-unsigned                        Require detached Ed25519 signatures for referenced release     │
│                                                                           artifacts.                                                     │
│                                                                           [default: require-signatures]                                  │
│ --require-provenance              --allow-missing-provenance              Require SLSA provenance for referenced release artifacts.      │
│                                                                           [default: require-provenance]                                  │
│ --json                                                                    Print machine-readable promotion request output.               │
│ --help                                                                    Show this message and exit.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release execute-rollout-promotion`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release execute-rollout-promotion                                                                               
            [OPTIONS] PROMOTION_REQUEST                                                                                                     
                                                                                                                                            
 Record an approved endpoint rollout ring promotion execution.                                                                              
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    promotion_request      PATH  [required]                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                       PATH  [default: .cavra/release/rollout-promotion-execution]                                               │
│ --approval-json                PATH                                                                                                      │
│ --approval-store               PATH                                                                                                      │
│ --approval-sqlite              PATH                                                                                                      │
│ --approval-id                  TEXT                                                                                                      │
│ --executed-by                  TEXT  [default: release-manager]                                                                          │
│ --execution-environment        TEXT                                                                                                      │
│ --notes                        TEXT                                                                                                      │
│ --metadata-json                PATH                                                                                                      │
│ --sqlite                       PATH                                                                                                      │
│ --json                               Print machine-readable promotion execution output.                                                  │
│ --help                               Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release execute-rollout-rollback`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release execute-rollout-rollback                                                                                
            [OPTIONS] PROMOTION_EXECUTION                                                                                                   
                                                                                                                                            
 Record an approved endpoint rollout rollback execution.                                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    promotion_execution      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                       PATH  [default: .cavra/release/rollout-rollback-execution]                                                │
│ --approval-json                PATH                                                                                                      │
│ --approval-store               PATH                                                                                                      │
│ --approval-sqlite              PATH                                                                                                      │
│ --approval-id                  TEXT                                                                                                      │
│ --executed-by                  TEXT  [default: release-manager]                                                                          │
│ --rollback-reason              TEXT  [default: Rollback approved from promotion execution audit.]                                        │
│ --execution-environment        TEXT                                                                                                      │
│ --notes                        TEXT                                                                                                      │
│ --metadata-json                PATH                                                                                                      │
│ --sqlite                       PATH                                                                                                      │
│ --json                               Print machine-readable rollback execution output.                                                   │
│ --help                               Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release export-promotion-audit`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release export-promotion-audit [OPTIONS]                                                                        
                                                           PROMOTION_EXECUTION                                                              
                                                                                                                                            
 Export SIEM and ITSM audit payloads for a rollout promotion execution.                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    promotion_execution      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                  PATH  [default: .cavra/release/promotion-audit-export]                                                         │
│ --provider                TEXT  [default: all]                                                                                           │
│ --splunk-index            TEXT  [default: cavra]                                                                                         │
│ --datadog-service         TEXT  [default: cavra]                                                                                         │
│ --itsm-project-key        TEXT  [default: CAVRA]                                                                                         │
│ --json                          Print machine-readable export output.                                                                    │
│ --help                          Show this message and exit.                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-promotion-audit`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-promotion-audit                                                                                 
            [OPTIONS] PROMOTION_EXECUTION                                                                                                   
                                                                                                                                            
 Deliver a rollout promotion audit event through configured connectors.                                                                     
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    promotion_execution      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --output                 PATH     [default: .cavra/release/promotion-audit-deliveries]                                                │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --metadata-json          PATH                                                                                                         │
│    --sqlite                 PATH                                                                                                         │
│    --json                            Print machine-readable delivery output.                                                             │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-rollback-execution`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-rollback-execution                                                                              
            [OPTIONS] ROLLBACK_EXECUTION                                                                                                    
                                                                                                                                            
 Deliver a rollout rollback execution event through configured connectors.                                                                  
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    rollback_execution      PATH  [required]                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --output                 PATH     [default: .cavra/release/rollback-deliveries]                                                       │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --metadata-json          PATH                                                                                                         │
│    --sqlite                 PATH                                                                                                         │
│    --json                            Print machine-readable delivery output.                                                             │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release connector-delivery-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release connector-delivery-history                                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show persisted release governance connector delivery history.                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json                    PATH                                                                                                  │
│ --sqlite                           PATH     [default: .cavra/evidence/metadata.db]                                                       │
│ --provider                         TEXT                                                                                                  │
│ --event-type                       TEXT                                                                                                  │
│ --event-id                         TEXT                                                                                                  │
│ --success          --no-success                                                                                                          │
│ --limit                            INTEGER  [default: 50]                                                                                │
│ --offset                           INTEGER  [default: 0]                                                                                 │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release connector-delivery-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release connector-delivery-dashboard                                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize release governance connector delivery health and alerts.                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-publication-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-publication-history                                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show persisted endpoint-management export publication history.                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json                    PATH                                                                                                  │
│ --sqlite                           PATH     [default: .cavra/evidence/metadata.db]                                                       │
│ --provider                         TEXT                                                                                                  │
│ --export-id                        TEXT                                                                                                  │
│ --channel                          TEXT                                                                                                  │
│ --success          --no-success                                                                                                          │
│ --limit                            INTEGER  [default: 50]                                                                                │
│ --offset                           INTEGER  [default: 0]                                                                                 │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-publication-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-publication-dashboard                                                                          
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint-management publication health and provider failures.                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-reconciliation-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-reconciliation-history                                                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show managed endpoint deployment reconciliation history.                                                                                   
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json            PATH                                                                                                          │
│ --sqlite                   PATH     [default: .cavra/evidence/metadata.db]                                                               │
│ --drift-status             TEXT                                                                                                          │
│ --alert-level              TEXT                                                                                                          │
│ --deployment-target        TEXT                                                                                                          │
│ --limit                    INTEGER  [default: 50]                                                                                        │
│ --offset                   INTEGER  [default: 0]                                                                                         │
│ --help                              Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-reconciliation-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-reconciliation-dashboard                                                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize managed endpoint deployment drift and stale endpoint observations.                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-inventory-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-inventory-history                                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint inventory ingestion history.                                                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json            PATH                                                                                                          │
│ --sqlite                   PATH     [default: .cavra/evidence/metadata.db]                                                               │
│ --provider                 TEXT                                                                                                          │
│ --channel                  TEXT                                                                                                          │
│ --deployment-target        TEXT                                                                                                          │
│ --limit                    INTEGER  [default: 50]                                                                                        │
│ --offset                   INTEGER  [default: 0]                                                                                         │
│ --help                              Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-inventory-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-inventory-dashboard                                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize normalized endpoint inventory coverage by provider.                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-inventory-freshness`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-inventory-freshness                                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Create an endpoint inventory freshness SLA report from indexed ingestions.                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                    PATH     [default: .cavra/release/endpoint-inventory-freshness]                                              │
│ --metadata-json             PATH                                                                                                         │
│ --sqlite                    PATH     [default: .cavra/evidence/metadata.db]                                                              │
│ --provider                  TEXT                                                                                                         │
│ --channel                   TEXT                                                                                                         │
│ --deployment-target         TEXT                                                                                                         │
│ --max-age-hours             INTEGER  [default: 24]                                                                                       │
│ --critical-age-hours        INTEGER  [default: 48]                                                                                       │
│ --json                               Print machine-readable freshness report output.                                                     │
│ --help                               Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-inventory-freshness-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-inventory-freshness-history                                                                    
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint inventory freshness report history.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json            PATH                                                                                                          │
│ --sqlite                   PATH     [default: .cavra/evidence/metadata.db]                                                               │
│ --alert-level              TEXT                                                                                                          │
│ --provider                 TEXT                                                                                                          │
│ --channel                  TEXT                                                                                                          │
│ --deployment-target        TEXT                                                                                                          │
│ --limit                    INTEGER  [default: 50]                                                                                        │
│ --offset                   INTEGER  [default: 0]                                                                                         │
│ --help                              Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-inventory-freshness-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-inventory-freshness-dashboard                                                                  
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint inventory freshness SLA alerts.                                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release automate-endpoint-reconciliation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release automate-endpoint-reconciliation                                                                        
            [OPTIONS] PACKAGE_DIR INVENTORY_INGESTION                                                                                       
                                                                                                                                            
 Reconcile a fresh inventory ingestion and open remediation when drift is detected.                                                         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    package_dir              PATH  [required]                                                                                           │
│ *    inventory_ingestion      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                                                         PATH     [default: .cavra/release/endpoint-reconciliation-automation]   │
│ --stale-after-hours                                              INTEGER  [default: 24]                                                  │
│ --remediation-strategy                                           TEXT     [default: mixed]                                               │
│ --requested-by                                                   TEXT     [default: release-agent]                                       │
│ --approver-group                                                 TEXT     [default: Endpoint Change Advisory Board]                      │
│ --ttl-hours                                                      INTEGER  [default: 24]                                                  │
│ --approval-store                                                 PATH                                                                    │
│ --approval-sqlite                                                PATH                                                                    │
│ --metadata-json                                                  PATH                                                                    │
│ --sqlite                                                         PATH                                                                    │
│ --require-package-verification    --skip-package-verification             Verify the Go release package before reconciling observed      │
│                                                                           endpoints.                                                     │
│                                                                           [default: skip-package-verification]                           │
│ --json                                                                    Print machine-readable automation output.                      │
│ --help                                                                    Show this message and exit.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-reconciliation-automation-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-reconciliation-automation-history                                                              
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint reconciliation automation history.                                                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json         PATH                                                                                                             │
│ --sqlite                PATH     [default: .cavra/evidence/metadata.db]                                                                  │
│ --drift-status          TEXT                                                                                                             │
│ --alert-level           TEXT                                                                                                             │
│ --approval-state        TEXT                                                                                                             │
│ --provider              TEXT                                                                                                             │
│ --limit                 INTEGER  [default: 50]                                                                                           │
│ --offset                INTEGER  [default: 0]                                                                                            │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-reconciliation-automation-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-reconciliation-automation-dashboard                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint reconciliation automations and pending remediation approvals.                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release request-endpoint-remediation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release request-endpoint-remediation                                                                            
            [OPTIONS] RECONCILIATION_REPORT                                                                                                 
                                                                                                                                            
 Create an approval-bound endpoint drift remediation plan.                                                                                  
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    reconciliation_report      PATH  [required]                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                 PATH     [default: .cavra/release/endpoint-remediation]                                                         │
│ --strategy               TEXT     [default: mixed]                                                                                       │
│ --requested-by           TEXT     [default: release-manager]                                                                             │
│ --approver-group         TEXT     [default: Endpoint Change Advisory Board]                                                              │
│ --ttl-hours              INTEGER  [default: 24]                                                                                          │
│ --approval-store         PATH                                                                                                            │
│ --approval-sqlite        PATH                                                                                                            │
│ --metadata-json          PATH                                                                                                            │
│ --sqlite                 PATH                                                                                                            │
│ --json                            Print machine-readable remediation request output.                                                     │
│ --help                            Show this message and exit.                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release export-endpoint-remediation-handoff`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release export-endpoint-remediation-handoff                                                                     
            [OPTIONS] REMEDIATION_REQUEST                                                                                                   
                                                                                                                                            
 Export public-safe ITSM, ChatOps, and private connector handoff payloads.                                                                  
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    remediation_request      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output               PATH  [default: .cavra/release/endpoint-remediation-handoff]                                                      │
│ --provider             TEXT  [default: all]                                                                                              │
│ --requested-by         TEXT  [default: release-manager]                                                                                  │
│ --delivery-mode        TEXT  [default: manual]                                                                                           │
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH                                                                                                              │
│ --json                       Print machine-readable handoff output.                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release record-endpoint-remediation-handoff-status`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release record-endpoint-remediation-handoff-status                                                              
            [OPTIONS] HANDOFF_JSON                                                                                                          
                                                                                                                                            
 Record public-safe provider status for an endpoint remediation handoff.                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    handoff_json      PATH  [required]                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --provider             TEXT  [default: private_queue]                                                                                    │
│ --status               TEXT  [default: delivered]                                                                                        │
│ --output               PATH  [default: .cavra/release/endpoint-remediation-handoff-status]                                               │
│ --external-ref         TEXT                                                                                                              │
│ --external-url         TEXT                                                                                                              │
│ --callback-json        PATH                                                                                                              │
│ --recorded-by          TEXT  [default: release-manager]                                                                                  │
│ --notes                TEXT                                                                                                              │
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH                                                                                                              │
│ --json                       Print machine-readable status output.                                                                       │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release execute-endpoint-remediation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release execute-endpoint-remediation                                                                            
            [OPTIONS] REMEDIATION_REQUEST                                                                                                   
                                                                                                                                            
 Record an approved endpoint drift remediation execution.                                                                                   
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    remediation_request      PATH  [required]                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                       PATH  [default: .cavra/release/endpoint-remediation-execution]                                            │
│ --approval-json                PATH                                                                                                      │
│ --approval-store               PATH                                                                                                      │
│ --approval-sqlite              PATH                                                                                                      │
│ --approval-id                  TEXT                                                                                                      │
│ --executed-by                  TEXT  [default: release-manager]                                                                          │
│ --execution-environment        TEXT                                                                                                      │
│ --notes                        TEXT                                                                                                      │
│ --metadata-json                PATH                                                                                                      │
│ --sqlite                       PATH                                                                                                      │
│ --json                               Print machine-readable remediation execution output.                                                │
│ --help                               Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-handoff-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-handoff-history                                                                    
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint remediation handoff package history.                                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json            PATH                                                                                                          │
│ --sqlite                   PATH     [default: .cavra/evidence/metadata.db]                                                               │
│ --provider                 TEXT                                                                                                          │
│ --approval-state           TEXT                                                                                                          │
│ --request-id               TEXT                                                                                                          │
│ --reconciliation-id        TEXT                                                                                                          │
│ --limit                    INTEGER  [default: 50]                                                                                        │
│ --offset                   INTEGER  [default: 0]                                                                                         │
│ --help                              Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-handoff-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-handoff-dashboard                                                                  
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint remediation handoff packages by provider and approval state.                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-handoff-status-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-handoff-status-history                                                             
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint remediation handoff status history.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json         PATH                                                                                                             │
│ --sqlite                PATH     [default: .cavra/evidence/metadata.db]                                                                  │
│ --provider              TEXT                                                                                                             │
│ --handoff-status        TEXT                                                                                                             │
│ --handoff-id            TEXT                                                                                                             │
│ --request-id            TEXT                                                                                                             │
│ --external-ref          TEXT                                                                                                             │
│ --limit                 INTEGER  [default: 50]                                                                                           │
│ --offset                INTEGER  [default: 0]                                                                                            │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-handoff-status-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-handoff-status-dashboard                                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint remediation handoff status callbacks by provider and state.                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-report`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-report                                                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Generate endpoint remediation SLA, escalation, and executive reporting.                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                     PATH     [default: .cavra/release/endpoint-remediation-sla]                                                 │
│ --metadata-json              PATH                                                                                                        │
│ --sqlite                     PATH     [default: .cavra/evidence/metadata.db]                                                             │
│ --warning-hours              INTEGER  [default: 24]                                                                                      │
│ --critical-hours             INTEGER  [default: 48]                                                                                      │
│ --generated-by               TEXT     [default: release-manager]                                                                         │
│ --index-metadata-json        PATH                                                                                                        │
│ --index-sqlite               PATH                                                                                                        │
│ --json                                Print machine-readable SLA report output.                                                          │
│ --help                                Show this message and exit.                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-endpoint-remediation-sla`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-endpoint-remediation-sla                                                                        
            [OPTIONS] SLA_REPORT                                                                                                            
                                                                                                                                            
 Deliver endpoint remediation SLA notifications through configured release connectors.                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    sla_report      PATH  [required]                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                                      PATH     Connector config JSON/YAML path. [required]                                    │
│    --output                                      PATH     [default: .cavra/release/endpoint-remediation-sla-deliveries]                  │
│    --provider                                    TEXT     [default: all]                                                                 │
│    --retries                                     INTEGER  [default: 2]                                                                   │
│    --timeout-seconds                             FLOAT    [default: 10.0]                                                                │
│    --generated-by                                TEXT     [default: release-manager]                                                     │
│    --routing-policy                              PATH                                                                                    │
│    --suppression-window-minutes                  INTEGER                                                                                 │
│    --force                         --no-force             [default: no-force]                                                            │
│    --metadata-json                               PATH                                                                                    │
│    --sqlite                                      PATH                                                                                    │
│    --json                                                 Print machine-readable delivery output.                                        │
│    --help                                                 Show this message and exit.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-history                                                                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint remediation SLA report history.                                                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH     [default: .cavra/evidence/metadata.db]                                                                   │
│ --alert-level          TEXT                                                                                                              │
│ --min-breached         INTEGER                                                                                                           │
│ --limit                INTEGER  [default: 50]                                                                                            │
│ --offset               INTEGER  [default: 0]                                                                                             │
│ --help                          Show this message and exit.                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-dashboard                                                                      
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint remediation SLA reports for executive release governance.                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release ack-endpoint-remediation-sla`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release ack-endpoint-remediation-sla                                                                            
            [OPTIONS] REPORT_ID                                                                                                             
                                                                                                                                            
 Record acknowledgement for an endpoint remediation SLA notification.                                                                       
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    report_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --provider                     TEXT                                                                                                      │
│ --acknowledged-by              TEXT                                                                                                      │
│ --acknowledgement-state        TEXT  [default: acknowledged]                                                                             │
│ --external-ref                 TEXT                                                                                                      │
│ --notes                        TEXT                                                                                                      │
│ --plan-id                      TEXT                                                                                                      │
│ --metadata-json                PATH                                                                                                      │
│ --sqlite                       PATH                                                                                                      │
│ --json                               Print machine-readable acknowledgement output.                                                      │
│ --help                               Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-notification-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-notification-history                                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint remediation SLA notification plans, deliveries, and acknowledgements.                                                        
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json                               PATH                                                                                       │
│ --sqlite                                      PATH     [default: .cavra/evidence/metadata.db]                                            │
│ --report-id                                   TEXT                                                                                       │
│ --provider                                    TEXT                                                                                       │
│ --metadata-kind                               TEXT                                                                                       │
│ --acknowledgement-state                       TEXT                                                                                       │
│ --suppressed               --no-suppressed                                                                                               │
│ --limit                                       INTEGER  [default: 50]                                                                     │
│ --offset                                      INTEGER  [default: 0]                                                                      │
│ --help                                                 Show this message and exit.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-notification-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-notification-dashboard                                                         
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint remediation SLA notification routing and acknowledgements.                                                              
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-plan                                                                
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Build owner-specific SLO and escalation-ladder status for SLA notifications.                                                               
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --slo-policy           PATH                                                                                                              │
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --generated-by         TEXT  [default: release-manager]                                                                                  │
│ --json                       Print machine-readable escalation plan output.                                                              │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-history                                                             
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint remediation SLA escalation plans.                                                                                            
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json                        PATH                                                                                              │
│ --sqlite                               PATH     [default: .cavra/evidence/metadata.db]                                                   │
│ --owner                                TEXT                                                                                              │
│ --provider                             TEXT                                                                                              │
│ --alert-level                          TEXT                                                                                              │
│ --active-only      --no-active-only             [default: no-active-only]                                                                │
│ --limit                                INTEGER  [default: 50]                                                                            │
│ --offset                               INTEGER  [default: 0]                                                                             │
│ --help                                          Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-dashboard                                                           
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint remediation SLA escalation ladders and owner SLOs.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-endpoint-remediation-sla-escalation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-endpoint-remediation-sla-escalation                                                             
            [OPTIONS] ESCALATION_PLAN                                                                                                       
                                                                                                                                            
 Deliver active endpoint remediation SLA escalations through configured release connectors.                                                 
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    escalation_plan      PATH  [required]                                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --output                 PATH     [default: .cavra/release/endpoint-remediation-sla-escalation-deliveries]                            │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --generated-by           TEXT     [default: release-manager]                                                                          │
│    --max-routes             INTEGER  [default: 20]                                                                                       │
│    --metadata-json          PATH                                                                                                         │
│    --sqlite                 PATH                                                                                                         │
│    --json                            Print machine-readable delivery output.                                                             │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release review-endpoint-remediation-sla-escalation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release review-endpoint-remediation-sla-escalation                                                              
            [OPTIONS] PLAN_ID                                                                                                               
                                                                                                                                            
 Record owner review for an endpoint remediation SLA escalation route.                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    plan_id      TEXT  [required]                                                                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --report-id            TEXT                                                                                                              │
│ --provider             TEXT                                                                                                              │
│ --owner                TEXT                                                                                                              │
│ --reviewed-by          TEXT                                                                                                              │
│ --review-state         TEXT  [default: accepted]                                                                                         │
│ --external-ref         TEXT                                                                                                              │
│ --notes                TEXT                                                                                                              │
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH                                                                                                              │
│ --json                       Print machine-readable review output.                                                                       │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-action-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-action-history                                                      
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint remediation SLA escalation plans, deliveries, and owner reviews.                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH     [default: .cavra/evidence/metadata.db]                                                                   │
│ --plan-id              TEXT                                                                                                              │
│ --owner                TEXT                                                                                                              │
│ --provider             TEXT                                                                                                              │
│ --metadata-kind        TEXT                                                                                                              │
│ --review-state         TEXT                                                                                                              │
│ --limit                INTEGER  [default: 50]                                                                                            │
│ --offset               INTEGER  [default: 0]                                                                                             │
│ --help                          Show this message and exit.                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-action-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-action-dashboard                                                    
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint remediation SLA escalation delivery and owner review actions.                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-plan                                                     
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Plan recurring escalation follow-up with owner calendar and maintenance-window suppression.                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --recurrence-policy        PATH                                                                                                          │
│ --metadata-json            PATH                                                                                                          │
│ --sqlite                   PATH  [default: .cavra/evidence/metadata.db]                                                                  │
│ --generated-by             TEXT  [default: release-manager]                                                                              │
│ --json                           Print machine-readable recurrence plan output.                                                          │
│ --help                           Show this message and exit.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-history                                                  
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint remediation SLA escalation recurrence and suppression plans.                                                                 
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH     [default: .cavra/evidence/metadata.db]                                                                   │
│ --plan-id              TEXT                                                                                                              │
│ --owner                TEXT                                                                                                              │
│ --provider             TEXT                                                                                                              │
│ --action               TEXT                                                                                                              │
│ --limit                INTEGER  [default: 50]                                                                                            │
│ --offset               INTEGER  [default: 0]                                                                                             │
│ --help                          Show this message and exit.                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-dashboard                                                
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint remediation SLA escalation recurrence suppression.                                                                      
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-endpoint-remediation-sla-escalation-recurrence`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-endpoint-remediation-sla-escalation-recurrence                                                  
            [OPTIONS] RECURRENCE_PLAN                                                                                                       
                                                                                                                                            
 Deliver recurrence-plan routes that are ready for follow-up escalation.                                                                    
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    recurrence_plan      PATH  [required]                                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --output                 PATH     [default: .cavra/release/endpoint-remediation-sla-escalation-recurrence-deliveries]                 │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --generated-by           TEXT     [default: release-manager]                                                                          │
│    --max-routes             INTEGER  [default: 50]                                                                                       │
│    --metadata-json          PATH                                                                                                         │
│    --sqlite                 PATH                                                                                                         │
│    --json                            Print machine-readable delivery output.                                                             │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release export-endpoint-remediation-sla-escalation-suppression-audit`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release export-endpoint-remediation-sla-escalation-suppression-audit                                            
            [OPTIONS] RECURRENCE_PLAN                                                                                                       
                                                                                                                                            
 Export public-safe suppression audit evidence from a recurrence plan.                                                                      
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    recurrence_plan      PATH  [required]                                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output               PATH  [default: .cavra/release/endpoint-remediation-sla-escalation-suppression-audit]                             │
│ --generated-by         TEXT  [default: release-manager]                                                                                  │
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH                                                                                                              │
│ --json                       Print machine-readable export output.                                                                       │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-retry-plan`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-retry-plan                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Plan safe retries for failed recurrence delivery batches.                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --retry-policy         PATH                                                                                                              │
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --generated-by         TEXT  [default: release-manager]                                                                                  │
│ --json                       Print machine-readable retry plan output.                                                                   │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-endpoint-remediation-sla-escalation-owner-digest`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-endpoint-remediation-sla-escalation-owner-digest                                                
            [OPTIONS] RECURRENCE_PLAN                                                                                                       
                                                                                                                                            
 Deliver owner digest notifications for unresolved recurrence routes.                                                                       
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    recurrence_plan      PATH  [required]                                                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                 PATH     Connector config JSON/YAML path. [required]                                                         │
│    --retry-plan             PATH                                                                                                         │
│    --output                 PATH     [default: .cavra/release/endpoint-remediation-sla-escalation-owner-digests]                         │
│    --provider               TEXT     [default: all]                                                                                      │
│    --retries                INTEGER  [default: 2]                                                                                        │
│    --timeout-seconds        FLOAT    [default: 10.0]                                                                                     │
│    --generated-by           TEXT     [default: release-manager]                                                                          │
│    --metadata-json          PATH                                                                                                         │
│    --sqlite                 PATH                                                                                                         │
│    --json                            Print machine-readable delivery output.                                                             │
│    --help                            Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-suppression-trends`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-suppression-trends                                                  
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize recurrence suppression trends by reason, owner, and provider.                                                                    
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --generated-by         TEXT  [default: release-manager]                                                                                  │
│ --json                       Print machine-readable suppression trend output.                                                            │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-automation`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-automation                                               
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Run one scheduled recurrence automation pass for retry, digest, and trend follow-up.                                                       
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --retry-policy                              PATH                                                                                         │
│ --config                                    PATH                                                                                         │
│ --output                                    PATH     [default: .cavra/release/endpoint-remediation-sla-escalation-recurrence-automation] │
│ --provider                                  TEXT     [default: all]                                                                      │
│ --retries                                   INTEGER  [default: 2]                                                                        │
│ --timeout-seconds                           FLOAT    [default: 10.0]                                                                     │
│ --schedule-interval-minutes                 INTEGER  [default: 60]                                                                       │
│ --max-digest-plans                          INTEGER  [default: 5]                                                                        │
│ --dry-run                      --execute             Plan by default; use --execute to deliver owner digests through configured          │
│                                                      connectors.                                                                         │
│                                                      [default: dry-run]                                                                  │
│ --generated-by                              TEXT     [default: release-manager]                                                          │
│ --metadata-json                             PATH                                                                                         │
│ --sqlite                                    PATH     [default: .cavra/evidence/metadata.db]                                              │
│ --json                                               Print machine-readable automation output.                                           │
│ --help                                               Show this message and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-automation-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-automation-history                                       
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 List scheduled recurrence automation worker runs.                                                                                          
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json                    PATH                                                                                                  │
│ --sqlite                           PATH     [default: .cavra/evidence/metadata.db]                                                       │
│ --dry-run          --no-dry-run                                                                                                          │
│ --limit                            INTEGER  [default: 50]                                                                                │
│ --offset                           INTEGER  [default: 0]                                                                                 │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-automation-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-automation-dashboard                                     
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize scheduled recurrence automation worker runs.                                                                                     
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-automation-health`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-automation-health                                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Report missed recurrence automation runs, stale metadata, and delivery failures.                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json                    PATH                                                                                                  │
│ --sqlite                           PATH     [default: .cavra/evidence/metadata.db]                                                       │
│ --expected-interval-minutes        INTEGER  [default: 30]                                                                                │
│ --stale-metadata-minutes           INTEGER  [default: 120]                                                                               │
│ --help                                      Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert                          
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Deliver recurrence automation health alerts through configured release connectors.                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config                                      PATH     Connector config JSON/YAML path. [required]                                    │
│    --output                                      PATH     [default:                                                                      │
│                                                           .cavra/release/endpoint-remediation-sla-escalation-recurrence-automation-heal… │
│    --provider                                    TEXT     [default: all]                                                                 │
│    --retries                                     INTEGER  [default: 2]                                                                   │
│    --timeout-seconds                             FLOAT    [default: 10.0]                                                                │
│    --generated-by                                TEXT     [default: release-manager]                                                     │
│    --routing-policy                              PATH                                                                                    │
│    --suppression-window-minutes                  INTEGER                                                                                 │
│    --expected-interval-minutes                   INTEGER  [default: 30]                                                                  │
│    --stale-metadata-minutes                      INTEGER  [default: 120]                                                                 │
│    --force                         --no-force             [default: no-force]                                                            │
│    --metadata-json                               PATH                                                                                    │
│    --sqlite                                      PATH                                                                                    │
│    --json                                                 Print machine-readable delivery output.                                        │
│    --help                                                 Show this message and exit.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert                              
            [OPTIONS] HEALTH_ID                                                                                                             
                                                                                                                                            
 Record acknowledgement for a recurrence automation health alert.                                                                           
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    health_id      TEXT  [required]                                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --provider                     TEXT                                                                                                      │
│ --acknowledged-by              TEXT                                                                                                      │
│ --acknowledgement-state        TEXT  [default: acknowledged]                                                                             │
│ --external-ref                 TEXT                                                                                                      │
│ --notes                        TEXT                                                                                                      │
│ --plan-id                      TEXT                                                                                                      │
│ --metadata-json                PATH                                                                                                      │
│ --sqlite                       PATH                                                                                                      │
│ --json                               Print machine-readable acknowledgement output.                                                      │
│ --help                               Show this message and exit.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history                          
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show recurrence automation health alert plans, deliveries, and acknowledgements.                                                           
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json                               PATH                                                                                       │
│ --sqlite                                      PATH     [default: .cavra/evidence/metadata.db]                                            │
│ --health-id                                   TEXT                                                                                       │
│ --provider                                    TEXT                                                                                       │
│ --metadata-kind                               TEXT                                                                                       │
│ --acknowledgement-state                       TEXT                                                                                       │
│ --suppressed               --no-suppressed                                                                                               │
│ --limit                                       INTEGER  [default: 50]                                                                     │
│ --offset                                      INTEGER  [default: 0]                                                                      │
│ --help                                                 Show this message and exit.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard                        
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize recurrence automation health alert delivery and acknowledgements.                                                                
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-history`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-history                                                                            
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Show endpoint drift remediation request and execution history.                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json            PATH                                                                                                          │
│ --sqlite                   PATH     [default: .cavra/evidence/metadata.db]                                                               │
│ --metadata-kind            TEXT                                                                                                          │
│ --reconciliation-id        TEXT                                                                                                          │
│ --approval-state           TEXT                                                                                                          │
│ --execution-status         TEXT                                                                                                          │
│ --limit                    INTEGER  [default: 50]                                                                                        │
│ --offset                   INTEGER  [default: 0]                                                                                         │
│ --help                              Show this message and exit.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra release endpoint-remediation-dashboard`

```text
                                                                                                                                            
 Usage: python -m cavra.cli release endpoint-remediation-dashboard                                                                          
            [OPTIONS]                                                                                                                       
                                                                                                                                            
 Summarize endpoint drift remediation approvals and executions.                                                                             
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --metadata-json        PATH                                                                                                              │
│ --sqlite               PATH  [default: .cavra/evidence/metadata.db]                                                                      │
│ --help                       Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## `cavra demo before-the-agent-acts`

```text
                                                                                                                                            
 Usage: python -m cavra.cli demo before-the-agent-acts [OPTIONS]                                                                            
                                                                                                                                            
 Run the flagship CAVRA demo and generate evidence.                                                                                         
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output             PATH  [default: examples/demos/before-the-agent-acts/generated]                                                     │
│ --policy-pack        TEXT  [default: cavra-ai-agent-baseline]                                                                            │
│ --help                     Show this message and exit.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
