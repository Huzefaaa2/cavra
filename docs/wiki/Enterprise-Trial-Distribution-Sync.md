# Enterprise Trial Distribution Sync

This public-safe sync records that the private Enterprise repository now has a
trial distribution pipeline for licensed evaluator access.

Private implementation status:

- private repository: `Huzefaaa2/cavra-enterprise`;
- private PR: `#86`;
- distribution target: gated GHCR image
  `ghcr.io/huzefaaa2/cavra-enterprise-trial:<version>`;
- release evidence: private trial package readiness JSON, release approval JSON,
  and image digest evidence;
- release gate: trial package approval is blocked unless private license-service
  readiness is true;
- runtime boundary: the private trial runtime image is built in the private
  repository and validated for Enterprise source exclusion in the runtime
  package layer.

## What Public Users Can See

The public Community repository may document:

- trial request and evaluator onboarding instructions;
- the private image name and expected pull pattern;
- license activation requirements;
- public-safe trial success criteria;
- Community-to-Enterprise upgrade boundaries.

## What Must Stay Private

Do not publish:

- Enterprise source code;
- trial image layers or binaries;
- bytecode artifacts;
- private workflow logs with operational details;
- license keys, signing material, or revocation state;
- registry credentials or pull secrets;
- customer records or tenant identifiers;
- paid policy packs;
- SaaS backend implementation details.

## Trial Access Model

Approved evaluators should receive one of these access paths:

1. gated private GHCR image access plus a time-limited trial license;
2. private compiled binary access plus a time-limited trial license;
3. hosted SaaS trial tenant using hosted license validation.

Community Edition remains usable without a license key. Enterprise Trial access
is licensed and must validate through private Enterprise or SaaS services.

## Next Recommendation

Connect private trial release approvals to live license issuance and evaluator
access workflows, then sync public docs again with only public-safe references.
