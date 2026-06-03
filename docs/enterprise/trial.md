# Enterprise Trial

CAVRA Trial Edition is distributed as a private Docker image, compiled binary,
or hosted SaaS trial. Trial source code is not public.

Trial access requires a time-limited license key or hosted validation flow.
Public Community code includes only placeholder license interfaces; real
validation must be performed by the private license service.

Private Enterprise distribution status:

- `Huzefaaa2/cavra-enterprise` now contains the private trial package release
  pipeline.
- The first distribution target is the gated GHCR image
  `ghcr.io/huzefaaa2/cavra-enterprise-trial:<version>`.
- Private release evidence records image digest metadata, trial duration,
  release ownership, source-exclusion status, and license-service readiness.
- Trial package approval is blocked unless private license-service readiness is
  true.
- Approved trial package releases are followed by private license issuance and
  evaluator access evidence. The private evidence records references for license
  issuance, entitlement, evaluator access grants, support ownership, onboarding,
  and revocation without publishing license keys or registry secrets.
- Trial expiry evidence records whether approved evaluator access was revoked,
  renewed, or escalated at the end of the approved trial window. Public docs
  record the boundary and gates only.
- Expired-trial follow-up evidence records notification, grace-period, and
  commercial handoff references for revoked, renewed, and escalated trials
  without publishing customer records, CRM payloads, or provider secrets.
- Trial conversion readiness evidence records paid-pilot or production
  conversion references for renewed or escalated trials without publishing
  customer records, billing secrets, license-service internals, or production
  provisioning secrets.
- Trial conversion activation and production handoff evidence records
  paid-pilot activation, entitlement activation, license transition, billing
  handoff, customer-success handoff, support handoff, production provisioning,
  production entitlement, production license, onboarding runbook, owner, and
  target go-live references without publishing customer records, billing
  secrets, license-service internals, or production provisioning secrets.
- Trial conversion closeout and revenue handoff evidence records
  customer-success closeout, support closeout, release acceptance, finance
  owner, revenue owner, billing status, subscription or order handoff, renewal
  forecast, and revenue-recognition references without publishing customer
  records, customer health records, finance records, billing secrets,
  license-service internals, or production provisioning secrets.
- Trial conversion executive summary and renewal action evidence records
  executive summary, leadership report, account-team action, customer-success
  summary, risk owner, renewal owner, renewal stage, next milestone, expansion
  opportunity, commercial follow-up, and action due-date references without
  publishing customer records, customer health records, finance records, billing
  secrets, license-service internals, or production provisioning secrets.

Example future install flow:

```bash
docker login ghcr.io
docker pull ghcr.io/huzefaaa2/cavra-enterprise-trial:latest
docker run -e CAVRA_LICENSE_KEY=... ghcr.io/huzefaaa2/cavra-enterprise-trial:latest
```

Use the actual `<version>` and license key issued through the approved trial
process. Do not place license keys, registry pull secrets, customer records, or
Enterprise artifacts in this public repository.

## Final Closeout Trial Workflow

Use [trial-to-pilot-intake.md](trial-to-pilot-intake.md) for the general trial-to-pilot intake workflow. Use [final-closeout-trial.md](final-closeout-trial.md) for the customer-facing final closeout overview and [final-closeout-trial-walkthrough.md](final-closeout-trial-walkthrough.md) for the evaluator walkthrough. The onboarding package also includes [final-closeout-trial-sample-evidence.md](final-closeout-trial-sample-evidence.md), [final-closeout-sales-engineering-demo.md](final-closeout-sales-engineering-demo.md), [final-closeout-production-pilot-intake.md](final-closeout-production-pilot-intake.md), [final-closeout-pilot-intake-api.md](final-closeout-pilot-intake-api.md), [final-closeout-pilot-readiness-checklists.md](final-closeout-pilot-readiness-checklists.md), [final-closeout-enterprise-saas-handoff.md](final-closeout-enterprise-saas-handoff.md), a synthetic evidence package at `examples/demos/final-closeout-trial/sample-evidence-package.json`, a final-closeout pilot intake template at `examples/demos/final-closeout-trial/pilot-intake-template.json`, and a general trial-to-pilot intake template at `examples/demos/trial-to-pilot-intake/trial-to-pilot-intake-template.json`.

Trial teams must use synthetic or non-production evidence. Do not place Enterprise source code, private policy packs, customer templates, connector credentials, archive mutation logic, signing keys, or license validation secrets in this public repository.

See also
[../trial-enterprise-distribution-sync.md](../trial-enterprise-distribution-sync.md)
for the public-safe private distribution summary and
[../trial-license-evaluator-access-sync.md](../trial-license-evaluator-access-sync.md)
for the public-safe trial license and evaluator access summary, and
[../trial-access-expiry-sync.md](../trial-access-expiry-sync.md)
for the public-safe trial access expiry summary, and
[../trial-expired-followup-sync.md](../trial-expired-followup-sync.md)
for the public-safe expired-trial follow-up summary, and
[../trial-conversion-readiness-sync.md](../trial-conversion-readiness-sync.md)
for the public-safe trial conversion readiness summary, and
[../trial-conversion-activation-handoff-sync.md](../trial-conversion-activation-handoff-sync.md)
for the public-safe trial conversion activation handoff summary, and
[../trial-conversion-closeout-revenue-sync.md](../trial-conversion-closeout-revenue-sync.md)
for the public-safe trial conversion closeout and revenue handoff summary, and
[../trial-conversion-executive-renewal-sync.md](../trial-conversion-executive-renewal-sync.md)
for the public-safe trial conversion executive summary and renewal action
summary, and
[../trial-conversion-customer-followthrough-sync.md](../trial-conversion-customer-followthrough-sync.md)
for the public-safe trial conversion customer follow-through summary, and
[../trial-conversion-renewal-outcome-rollup-sync.md](../trial-conversion-renewal-outcome-rollup-sync.md)
for the public-safe trial conversion renewal outcome rollup summary, and
[../trial-final-commercial-renewal-closeout-sync.md](../trial-final-commercial-renewal-closeout-sync.md)
for the public-safe final commercial renewal closeout summary, and
[../trial-commercialization-closure-readiness-sync.md](../trial-commercialization-closure-readiness-sync.md)
for the public-safe trial commercialization closure readiness summary, and
[../trial-commercialization-closure-release-acceptance-sync.md](../trial-commercialization-closure-release-acceptance-sync.md)
for the public-safe trial commercialization closure release acceptance summary,
and
[../trial-commercialization-closure-final-closeout-sync.md](../trial-commercialization-closure-final-closeout-sync.md)
for the public-safe trial commercialization closure final closeout summary, and
[../trial-commercial-launch-readiness-handoff-sync.md](../trial-commercial-launch-readiness-handoff-sync.md)
for the public-safe trial commercial launch-readiness handoff summary, and
[../trial-commercial-launch-readiness-final-approval-sync.md](../trial-commercial-launch-readiness-final-approval-sync.md)
for the public-safe trial commercial launch-readiness final approval summary,
and
[../trial-commercial-launch-readiness-operating-transition-sync.md](../trial-commercial-launch-readiness-operating-transition-sync.md)
for the public-safe trial commercial launch-readiness operating transition
summary.
