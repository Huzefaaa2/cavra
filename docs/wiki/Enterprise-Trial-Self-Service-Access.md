# Enterprise Trial Self-Service Access

CAVRA Enterprise Trial is available through self-service approved access, not
anonymous public download.

Current approved private package:

- image: `ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05`
- digest: `sha256:2d5f0d338a5528205f11674917d1526db7aa9732ef2af6ca3bd957b6230b4b47`
- access model: self-service request plus approved private evaluator access
- license model: time-limited signed trial license
- runtime control: `CAVRA_LICENSE_KEY` is validated before use
- lifecycle: expiry and revocation are tracked privately

The public portal includes an Enterprise Trial request page. Live deployments
can point it at the private `CAVRA Trial Access Portal` service. Public CAVRA
does not expose Enterprise source, trial license tokens, signing keys, registry
pull secrets, customer records, revocation state, private approval notes, or
paid policy packs.

Related pages:

- [Enterprise Trial Availability](Enterprise-Trial-Availability)
- [Enterprise Trial](Enterprise-Trial)
- [Trial License Evaluator Access Sync](Trial-License-Evaluator-Access-Sync)
