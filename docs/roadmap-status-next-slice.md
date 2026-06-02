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

## Remaining Production Themes

CAVRA is ready for the next production-readiness slice, but the product is not
yet fully production-complete. Remaining themes are:

- SaaS tenant onboarding and entitlement readiness;
- private license service integration and subscription status evidence;
- hosted policy registry and tenant audit-store readiness;
- Enterprise/SaaS dashboard operating evidence;
- production observability, billing, and support handoff runbooks;
- final release hardening, packaging, and commercialization closeout.

## Next Slice

SaaS tenant onboarding and entitlement readiness.

## Why This Is Next

CAVRA now has a public trial path and private trial-to-pilot gates. The next
commercial blocker is tenant activation: a customer should be able to move from
trial approval into a governed SaaS or Enterprise tenant with clear entitlement
status, license validation handoff, onboarding ownership, and audit-store
readiness.

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

3. Private tenant onboarding readiness evidence.
   - Add private tenant activation evidence in `cavra-enterprise`.
   - Track identity, license, audit-store, policy registry, and support owner
     readiness without storing secrets in source.

4. Private entitlement and license-service handoff evidence.
   - Add private entitlement validation handoff records.
   - Capture license-service reachability and subscription status evidence.

5. Public docs/wiki sync.
   - Publish public-safe outcomes and update the phase log after the private
     batch.

## Acceptance Criteria

- Public docs explain how tenant onboarding and entitlement checks will work.
- Public contracts do not contain SaaS backend code, billing secrets, license
  keys, customer data, or private policy packs.
- Private evidence can block onboarding when identity, entitlement, audit-store,
  or support ownership is missing.
- README, roadmap, and wiki-ready pages remain current after each release.

## Recommended Next PR

Continue with private tenant onboarding readiness evidence in
`cavra-enterprise`.
