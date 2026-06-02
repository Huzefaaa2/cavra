# Post-Onboarding SaaS Operating Readiness

Status date: 2026-06-02.

## Slice Name

Post-onboarding SaaS operating readiness.

## Current Position

CAVRA has completed the public and private work needed to move from Community
adoption into trial, pilot, tenant activation, entitlement handoff, paid-pilot
promotion, and customer rollout closeout:

- public trial-to-pilot intake plan;
- public licensing interface hardening;
- public SaaS Control Plane contract;
- public tenant onboarding contract;
- public entitlement status contract;
- public hosted policy registry readiness contract;
- public tenant audit-store operating contract;
- public billing/subscription boundary documentation;
- private trial package readiness gates in `cavra-enterprise` PR #61;
- private customer pilot handoff evidence in `cavra-enterprise` PR #62;
- private tenant onboarding readiness evidence in `cavra-enterprise` PR #63;
- private entitlement and license-service handoff evidence in
  `cavra-enterprise` PR #64;
- private paid-pilot promotion evidence in `cavra-enterprise` PR #65;
- private customer rollout closeout evidence in `cavra-enterprise` PR #66;
- public-safe documentation syncs for both commercialization batches.

## Why This Is Next

The next production risk is steady-state operation after a customer is onboarded.
Enterprise and SaaS customers need proof that policy registry availability,
tenant audit-store health, billing/subscription status, license-service
observability, support ownership, and SaaS dashboards remain healthy after
launch.

This slice keeps Community public and safe while defining the operating
contracts private Enterprise and SaaS modules must satisfy.

## Public Community Scope

The public repository should define only safe contracts and documentation:

- hosted policy registry readiness contract;
- tenant audit-store operating contract;
- billing/subscription status boundary documentation;
- SaaS observability and support-handoff documentation;
- public-safe examples and unavailable responses;
- README, roadmap, wiki, and phase-log updates.

## Private Enterprise Scope

The private `cavra-enterprise` repository should implement evidence gates for:

- hosted policy registry readiness;
- tenant audit-store health and retention readiness;
- billing/subscription handoff status;
- license-service observability;
- SaaS support ownership and escalation readiness;
- operating dashboard rollups and approvals.

Private code must keep customer payloads, customer identifiers, billing provider
records, license keys, license signing material, provider URLs, connector
credentials, private policy packs, and SaaS backend internals outside the public
Community repository.

## Future SaaS Scope

Future SaaS service work should own:

- tenant dashboard APIs;
- hosted policy registry service;
- tenant audit-store service;
- billing/subscription provider integration;
- license-service telemetry;
- support and escalation integrations;
- operational SLO reporting.

## Proposed PR Sequence

1. Public hosted policy registry readiness contract. Delivered with
   `docs/architecture/hosted-policy-registry-readiness-contract.md`.
   - Add public-safe request and response shapes for registry availability,
     policy-pack catalog readiness, version freshness, and private-module
     requirements.
   - Keep hosted registry implementation and paid policy packs private.

2. Public tenant audit-store operating contract. Delivered with
   `docs/architecture/tenant-audit-store-operating-contract.md`.
   - Add public-safe request and response shapes for audit-store health,
     retention posture, export readiness, and evidence freshness.
   - Keep tenant archive storage, customer evidence, and retention enforcement
     private.

3. Public billing/subscription boundary documentation. Delivered with
   `docs/architecture/billing-subscription-boundary.md`.
   - Document subscription status, billing-provider ownership, and license
     service observability without implementing billing logic.

4. Private hosted policy registry readiness evidence.
   - Add private evidence for registry availability, catalog freshness, policy
     pack entitlement, approval state, and rollout blockers.

5. Private tenant audit-store operating evidence.
   - Add private evidence for audit-store health, retention readiness, export
     availability, and dashboard approval state.

6. Private billing/subscription and license-service observability evidence.
   - Add private evidence for subscription status, billing handoff, license
     service telemetry, support ownership, and escalation readiness.

7. Public docs/wiki sync.
   - Publish public-safe outcomes and update the phase log after the private
     operating-readiness batch.

## Acceptance Criteria

- Public contracts describe post-onboarding operating readiness without SaaS
  backend implementation.
- Community source remains free of Enterprise source, private policy packs,
  customer data, billing secrets, license keys, provider URLs, and connector
  credentials.
- Private evidence can block steady-state operation when policy registry,
  audit-store, subscription, license-service, support, or dashboard readiness is
  missing.
- README, roadmap, and wiki-ready pages point to the current next slice.

## Recommended Next PR

Implement private hosted policy registry readiness evidence in
`cavra-enterprise`.
