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

The SaaS tenant onboarding and entitlement readiness batch is also complete:

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
- public-safe batch sync is delivered in
  [tenant-entitlement-commercialization-batch-sync.md](tenant-entitlement-commercialization-batch-sync.md).

## Remaining Production Themes

CAVRA is ready for the next production-readiness slice, but the product is not
yet fully production-complete. Remaining themes are:

- hosted policy registry readiness and tenant audit-store operating dashboards;
- billing/subscription operations and license-service observability;
- Enterprise/SaaS dashboard operating evidence;
- production observability, billing, and support handoff runbooks;
- final release hardening, packaging, and commercialization closeout.

## Next Slice

Post-onboarding SaaS operating readiness.

## Why This Is Next

CAVRA now has a public trial path, private trial-to-pilot gates, public tenant
and entitlement contracts, and private evidence from tenant activation through
customer rollout closeout. The next commercial blocker is operating a live SaaS
or Enterprise tenant over time: hosted policy registry readiness, tenant
audit-store operations, billing/subscription monitoring, observability, and
support runbooks need the same evidence discipline.

## Proposed PR Sequence

1. Public tenant onboarding contract. Delivered with
   `docs/architecture/tenant-onboarding-contract.md` and the public-safe
   `tenant_onboarding` operation.
   - Extend public-safe SaaS contracts with tenant onboarding request and
     response shapes.
   - Document tenant activation boundaries without SaaS backend source.

2. Public entitlement status contract. Delivered with
   `docs/architecture/entitlement-status-contract.md` and the public-safe
   `entitlement_status` operation.
   - Define public-safe subscription, license, and feature entitlement response
     shapes.
   - Keep billing and license service implementation private.

3. Private tenant onboarding readiness evidence. Delivered in
   `cavra-enterprise` PR #63.
   - Add private tenant activation evidence in `cavra-enterprise`.
   - Track identity, license, audit-store, policy registry, and support owner
     readiness without storing secrets in source.

4. Private entitlement and license-service handoff evidence. Delivered in
   `cavra-enterprise` PR #64.
   - Add private entitlement validation handoff records.
   - Capture license-service reachability and subscription status evidence.

5. Private paid-pilot promotion evidence. Delivered in `cavra-enterprise`
   PR #65.
   - Record customer-success, support, release-management, and commercial
     closeout readiness.

6. Private customer rollout closeout evidence. Delivered in `cavra-enterprise`
   PR #66.
   - Record launch readiness, customer-success closeout, support handoff,
     release acceptance, and commercial confirmation.

7. Public docs/wiki sync. Delivered in
   `docs/tenant-entitlement-commercialization-batch-sync.md`.
   - Publish public-safe outcomes and update the phase log after the private
     batch.

## Acceptance Criteria

- Public docs explain how tenant onboarding and entitlement checks work.
- Public contracts do not contain SaaS backend code, billing secrets, license
  keys, customer data, or private policy packs.
- Private evidence can block onboarding, entitlement handoff, paid-pilot
  promotion, or customer rollout closeout when required readiness evidence is
  missing.
- README, roadmap, and wiki-ready pages remain current after each release.

## Recommended Next PR

Run a roadmap status pass and define the next production-readiness slice after
SaaS tenant onboarding and entitlement readiness.
