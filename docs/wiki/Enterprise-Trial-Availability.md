# Enterprise Trial Availability

CAVRA Enterprise Trial is ready for approved private evaluators.

Public-safe package status:

- package ID: `cavra-enterprise-trial-2026.06.05`;
- image: `ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05`;
- digest: `sha256:2d5f0d338a5528205f11674917d1526db7aa9732ef2af6ca3bd957b6230b4b47`;
- distribution: gated private GHCR image;
- trial duration: 30 days;
- source code excluded from the runtime package layer;
- customer data excluded;
- signed license validation passed;
- revoked-license validation failed closed;
- private registry push and pull validation passed;
- runtime license enforcement passed.

Approved evaluators need private GHCR access plus a time-limited CAVRA trial
license. Public CAVRA does not publish Enterprise source code, license keys,
signing keys, registry pull secrets, customer records, revocation state, or paid
policy packs.

Public docs:

- [Enterprise Trial](Enterprise-Trial)
- [Enterprise Trial Distribution Sync](Enterprise-Trial-Distribution-Sync)
- [Trial License Evaluator Access Sync](Trial-License-Evaluator-Access-Sync)
