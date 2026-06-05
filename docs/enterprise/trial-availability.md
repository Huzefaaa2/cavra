# Enterprise Trial Availability

CAVRA Enterprise Trial is ready for approved private evaluators.

Request access through the live approved-access landing page:

```text
https://cavra-trial.mind-ops.cloud
```

The trial package is distributed as a gated private GHCR image:

```text
ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05
```

Public-safe release evidence records:

- package ID: `cavra-enterprise-trial-2026.06.05`;
- distribution channel: private Docker registry;
- trial duration: 30 days;
- image digest: `sha256:2d5f0d338a5528205f11674917d1526db7aa9732ef2af6ca3bd957b6230b4b47`;
- source code excluded from the runtime package layer;
- customer data excluded;
- license required;
- private distribution required;
- signed trial license validation passed;
- revoked trial license validation failed closed;
- pushed private registry image was pulled and runtime license validation passed.
- hosted request portal health, PostgreSQL storage, signup, approval, license
  validation, and revocation were validated on 2026-06-05 using synthetic
  public-safe evidence.

The private release workflow retained readiness evidence in the private
`Huzefaaa2/cavra-enterprise` repository. This public repository records only
public-safe references and evaluator instructions.

## Evaluator Access

Enterprise Trial access requires:

1. approval for private trial access;
2. GHCR package access for `ghcr.io/huzefaaa2/cavra-enterprise-trial`;
3. a time-limited trial license issued by CAVRA;
4. runtime configuration for the issued license and public validation key.

Example evaluator flow:

```bash
docker login ghcr.io
docker pull ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05
docker run --rm \
  -e CAVRA_LICENSE_KEY \
  -e CAVRA_LICENSE_PUBLIC_KEY_B64 \
  -e CAVRA_TRIAL_ARTIFACT_REFERENCE=ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05 \
  -e CAVRA_TRIAL_PACKAGE_VERSION=2026.06.05 \
  ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05
```

Do not place license keys, registry pull secrets, customer records, private
policy packs, Enterprise source, or license-service internals in this public
repository.

## Boundary

Enterprise source code, signing keys, evaluator license tokens, pull secrets,
revocation state, customer entitlement records, and commercial policy packs
remain private. Public CAVRA documents the access model and public-safe release
status only.
