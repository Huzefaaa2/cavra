# Roadmap Status and Next Slice

Status date: 2026-06-02.

## Current Position

The Trial and SaaS commercialization readiness batch is complete:

- public trial-to-pilot intake plan is delivered;
- public licensing interface hardening is delivered;
- public SaaS Control Plane contract is delivered;
- private trial package readiness gates are delivered in `cavra-enterprise`
  PR #61;
- private customer pilot handoff evidence is delivered in `cavra-enterprise`
  PR #62;
- public-safe batch sync is delivered.

The SaaS tenant onboarding and entitlement readiness batch is complete:

- public tenant onboarding contract is delivered;
- public entitlement status contract is delivered;
- private tenant onboarding readiness evidence is delivered in
  `cavra-enterprise` PR #63;
- private entitlement and license-service handoff evidence is delivered in
  `cavra-enterprise` PR #64;
- private paid-pilot promotion evidence is delivered in `cavra-enterprise`
  PR #65;
- private customer rollout closeout evidence is delivered in
  `cavra-enterprise` PR #66;
- private hosted policy registry readiness evidence is delivered in
  `cavra-enterprise` PR #67;
- private tenant audit-store operating evidence is delivered in
  `cavra-enterprise` PR #68;
- private SaaS operating readiness rollup evidence is delivered in
  `cavra-enterprise` PR #69;
- private billing and license-service observability evidence is delivered in
  `cavra-enterprise` PR #70;
- private support and customer-success operating handoff evidence is delivered
  in `cavra-enterprise` PR #71;
- private operating dashboard and support escalation rollup evidence is
  delivered in `cavra-enterprise` PR #72;
- private final SaaS customer operating closeout evidence is delivered in
  `cavra-enterprise` PR #73;
- public-safe batch sync is delivered in
  [tenant-entitlement-commercialization-batch-sync.md](tenant-entitlement-commercialization-batch-sync.md).

The post-onboarding SaaS operating readiness slice is now complete through the
SaaS operating readiness rollup and public-safe documentation sync:

- public hosted policy registry readiness contract is delivered.
- public tenant audit-store operating contract is delivered.
- public billing/subscription boundary documentation is delivered.
- public post-onboarding SaaS operating batch sync is delivered in
  [post-onboarding-saas-operating-batch-sync.md](post-onboarding-saas-operating-batch-sync.md).
- public SaaS customer operating closeout batch sync is delivered in
  [saas-customer-operating-closeout-batch-sync.md](saas-customer-operating-closeout-batch-sync.md).

## Remaining Production Themes

CAVRA is ready for the next production-readiness slice, but the product is not
yet fully production-complete. Remaining themes are:

- hosted policy registry readiness and policy-pack catalog operation;
- tenant audit-store health, retention posture, and export readiness;
- customer operating dashboard contracts and support handoff contracts;
- private SaaS operating automation for support, customer-success, and
  commercial closeout at trial-to-paid scale;
- production observability and support runbooks;
- final release hardening, packaging, and commercialization closeout.

## Next Slice

Customer operating closeout hardening.

## Why This Is Next

CAVRA now has a public trial path, private trial-to-pilot gates, public tenant
and entitlement contracts, and private evidence from tenant activation through
final SaaS customer operating closeout. The next commercial blocker is making
the customer operating dashboard and support handoff model public-safe and
repeatable, then extending private automation for trial-to-paid customer scale.

## Proposed PR Sequence

1. Public hosted policy registry readiness contract. Delivered with
   `docs/architecture/hosted-policy-registry-readiness-contract.md`.
   - Add public-safe request and response shapes for hosted policy registry
     availability, policy-pack catalog freshness, version state, and private
     implementation requirements.
   - Keep hosted registry service implementation, paid policy packs, customer
     policy catalogs, and entitlement lookups private.

2. Public tenant audit-store operating contract. Delivered with
   `docs/architecture/tenant-audit-store-operating-contract.md`.
   - Add public-safe request and response shapes for audit-store health,
     retention posture, evidence freshness, and export readiness.
   - Keep tenant archive storage, customer evidence, retention enforcement, and
     export connectors private.

3. Public billing/subscription boundary documentation. Delivered with
   `docs/architecture/billing-subscription-boundary.md`.
   - Document billing-provider ownership, subscription state, renewal handoff,
     and license-service observability boundaries.
   - Keep billing provider integrations, customer payment data, and license
     service implementation private.

4. Private hosted policy registry readiness evidence. Delivered in
   `cavra-enterprise` PR #67.
   - Add private evidence for registry availability, catalog freshness, policy
     pack entitlement, approval state, and rollout blockers.

5. Private tenant audit-store operating evidence. Delivered in
   `cavra-enterprise` PR #68.
   - Add private evidence for audit-store health, retention readiness, export
     availability, and operating dashboard approval state.

6. Private SaaS operating readiness rollup. Delivered in `cavra-enterprise`
   PR #69.
   - Combine hosted policy registry readiness, tenant audit-store operating
     evidence, control-plane health, and release approval into one private
     promotion gate.

7. Public docs/wiki sync. Delivered with
   [post-onboarding-saas-operating-batch-sync.md](post-onboarding-saas-operating-batch-sync.md).
   - Publish public-safe outcomes and update the phase log after the private
     operating-readiness batch.

8. Private billing/subscription and license-service observability evidence.
   Delivered in `cavra-enterprise` PR #70.
   - Add private evidence for subscription status, billing handoff, license
     service telemetry, support ownership, and escalation readiness.

9. Private support and customer-success operating handoff evidence. Delivered
   in `cavra-enterprise` PR #71.
   - Add private evidence for support ownership, customer-success ownership,
     escalation routing, customer health review, and handoff dashboard
     readiness.

10. Private operating dashboard and support escalation rollup evidence.
    Delivered in `cavra-enterprise` PR #72.
    - Add private evidence for dashboard visibility, support escalation,
      customer-success health, on-call readiness, and executive visibility.

11. Private final SaaS customer operating closeout evidence. Delivered in
    `cavra-enterprise` PR #73.
    - Add private evidence for billing observability, support handoff,
      customer-success handoff, dashboard visibility, escalation readiness, and
      release acceptance.

12. Public docs/wiki sync. Delivered with
    [saas-customer-operating-closeout-batch-sync.md](saas-customer-operating-closeout-batch-sync.md).
    - Publish public-safe outcomes and update the phase log after the private
      customer operating closeout batch.

13. Public customer operating dashboard and support handoff contracts.
    - Define public-safe request and response shapes for operating dashboards,
      support ownership, customer-success ownership, escalation readiness, and
      closeout evidence boundaries.

## Acceptance Criteria

- Public docs explain post-onboarding SaaS operating readiness without exposing
  SaaS backend implementation.
- Public contracts do not contain billing secrets, license keys, customer data,
  private policy packs, provider URLs, or connector credentials.
- Private evidence can block steady-state operation when policy registry,
  audit-store, billing/subscription, license-service, support, dashboard, or
  closeout readiness is missing.
- README, roadmap, and wiki-ready pages remain current after each release.

## Recommended Next PR

Define public-safe customer operating dashboard and support handoff contracts,
then continue private SaaS operating automation required for trial-to-paid
customer scale.
