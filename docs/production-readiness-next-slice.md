# Production Readiness Next Slice

This slice turns the completed private managed-infrastructure readiness batch
into a commercialization-ready path for trials, Enterprise pilots, and future
SaaS onboarding. It is public-safe by design: it does not expose Enterprise
source code, license-server logic, customer data, commercial policy packs,
private connector payloads, signing keys, or SaaS secrets.

## Slice Name

Trial and SaaS commercialization readiness.

Status: complete. Follow-up SaaS tenant onboarding and entitlement readiness is
also complete through public contracts, private Enterprise evidence gates, and
public-safe documentation sync.

## Why This Is Next

CAVRA now has Community source, open-core boundaries, public trial guidance,
private Enterprise handoff contracts, managed infrastructure evidence, and
release-readiness dashboards. The remaining production risk is not another
single connector feature. It is the handoff from public Community adoption into
a repeatable commercial trial and pilot process.

## Scope

Public Community repository:
- trial request and intake workflow documentation;
- public-safe trial license interface contract;
- trial evidence package checklist;
- SaaS Control Plane API boundary documentation;
- README, roadmap, wiki, and diagram updates;
- tests for public-safe licensing and boundary validation.

Private Enterprise repository:
- private trial package build checklist;
- private license validation client boundary;
- customer-specific pilot handoff records;
- private managed infrastructure readiness dashboards;
- private connector and storage implementation evidence.

Future SaaS repository or service:
- tenant onboarding workflow;
- license service;
- billing and subscription status integration;
- hosted policy registry and audit store;
- tenant dashboard and compliance export APIs.

## Proposed PR Sequence

1. Public trial-to-pilot intake plan. Delivered in
   `docs/enterprise/trial-to-pilot-intake.md` with the public-safe template at
   `examples/demos/trial-to-pilot-intake/trial-to-pilot-intake-template.json`.
   - Add public-safe trial request, pilot intake, and evidence checklist docs.
   - Update README, roadmap, wiki, and phase log.

2. Public licensing interface hardening. Delivered with validation reports,
   safer expiry handling, invalid/revoked/suspended status handling, and tests
   for feature locking.
   - Add tests and docs for license object status handling, expiry boundaries,
     and locked Enterprise features in Community mode.
   - Keep validation local and placeholder-only.

3. Public SaaS Control Plane contract. Delivered with
   `src/cavra/saas_control_plane.py`,
   `docs/architecture/saas-control-plane-contract.md`, and wiki-ready
   documentation.
   - Define public-safe request/response shapes for tenant status, policy
     registry lookup, evidence export, and license validation boundaries.
   - Document that implementation belongs in private SaaS code.

4. Private trial package readiness. Delivered in private PR #61.
   - Add private package checklist, trial artifact metadata, and release gate
     evidence in `cavra-enterprise`.
   - Keep binaries, customer identifiers, license keys, and private modules out
     of public source.

5. Private customer pilot handoff evidence. Delivered in private PR #62.
   - Add private handoff dashboard records for trial-to-pilot conversion,
     operator acknowledgements, and support ownership.

6. Public docs/wiki sync. Delivered by this public-safe batch sync.
   - Sync public-safe outcomes after the private batch according to the
     10-PR documentation cadence or earlier if roadmap guidance becomes stale.

## Acceptance Criteria

- Public repo explains how Community users request or run a trial without
  exposing private code or fake license keys.
- Enterprise and SaaS responsibilities are documented as extension points.
- Community continues to run without a license key.
- Enterprise-only features remain locked in Community mode with clear upgrade
  messaging.
- Trial/SaaS docs explain data boundaries, security boundaries, and private
  implementation ownership.
- Tests cover public licensing and feature-lock behavior.

## User Stories

- As a prospect, I can understand how to move from Community Edition to a trial
  without seeing private source code.
- As a sales engineer, I can run a repeatable trial checklist using synthetic
  public-safe evidence.
- As a platform owner, I can distinguish Community, Trial, Enterprise, and SaaS
  responsibilities before a pilot starts.
- As a security reviewer, I can verify that license secrets, customer data, and
  SaaS implementation details are not present in the public repository.

## Enterprise Challenge Solved

This slice reduces commercial adoption friction. It gives buyers a clean path
from public evaluation to governed trial, private Enterprise deployment, or SaaS
onboarding without compromising open-core boundaries.

## Immediate Next PR

The next production-readiness slice is documented in
[Post-Onboarding SaaS Operating Readiness](post-onboarding-saas-operating-readiness.md).
Continue with private hosted policy registry readiness evidence in
`cavra-enterprise`.
