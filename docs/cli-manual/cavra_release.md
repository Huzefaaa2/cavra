# cavra release

## Name

`cavra release` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra release --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

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

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra policy`](cavra_policy.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra registry`](cavra_registry.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
