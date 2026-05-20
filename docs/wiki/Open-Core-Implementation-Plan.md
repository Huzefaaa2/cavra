# Open-Core Implementation Plan

CAVRA now uses a public Community Edition and private Enterprise architecture.
The public `Huzefaaa2/cavra` repository remains the product landing repository
and Community source tree.

## Editions

- Community: public source, no license required, core local governance.
- Enterprise: private source, paid modules, private policy packs, SSO, RBAC,
  dashboards, compliance reports, and support.
- Trial: private binary, private image, or hosted SaaS trial with license
  validation outside the public repo.
- SaaS Control Plane: future private hosted service for tenants, billing,
  license validation, policy registry, audit history, dashboards, and AI
  recommendations.

## Public Repo Rules

The public repo may include Community source, public docs, Enterprise feature
docs, trial instructions, and extension interfaces. It must not include
Enterprise source, proprietary algorithms, license signing keys, SaaS secrets,
commercial policy pack source, customer templates, or customer data.

## Implementation Phases

1. Open-core foundation: edition boundaries, public license interfaces, feature
   registry, plugin runtime, trial docs, Community Docker, public workflows,
   boundary validator, and migration report.
2. Release connector observability: persisted delivery history views and
   alerting dashboards for release governance connectors. Delivered.
3. Community packaging hardening: public artifact signing, release channel
   manifests, managed workstation updater policy, release-channel promotion
   approvals, endpoint-management export bundles, Community release notes, and
   install smoke tests. Delivered for channel, updater, and endpoint export
   governance.
4. Private Enterprise bootstrap: create `cavra-enterprise`, implement private
   package `cavra_enterprise`, and wire private plugin manifests.
5. Trial distribution: private Docker image or binary, trial license service,
   and trial onboarding docs.
6. SaaS Control Plane: tenant, billing, license, policy registry, audit store,
   dashboard, and AI recommendation services in private infrastructure.

## Current Next Recommendation

Add deployment templates for scheduled recurrence automation workers, including GitHub Actions cron, Kubernetes CronJob, systemd timer, and secrets-safe connector guidance.
