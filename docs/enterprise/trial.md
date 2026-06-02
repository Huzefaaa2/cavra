# Enterprise Trial

CAVRA Trial Edition is distributed as a private Docker image, compiled binary,
or hosted SaaS trial. Trial source code is not public.

Trial access requires a time-limited license key or hosted validation flow.
Public Community code includes only placeholder license interfaces; real
validation must be performed by the private license service.

Example future install flow:

```bash
docker login ghcr.io
docker pull ghcr.io/huzefaaa2/cavra-enterprise-trial:latest
docker run -e CAVRA_LICENSE_KEY=... ghcr.io/huzefaaa2/cavra-enterprise-trial:latest
```

## Final Closeout Trial Workflow

Use [trial-to-pilot-intake.md](trial-to-pilot-intake.md) for the general trial-to-pilot intake workflow. Use [final-closeout-trial.md](final-closeout-trial.md) for the customer-facing final closeout overview and [final-closeout-trial-walkthrough.md](final-closeout-trial-walkthrough.md) for the evaluator walkthrough. The onboarding package also includes [final-closeout-trial-sample-evidence.md](final-closeout-trial-sample-evidence.md), [final-closeout-sales-engineering-demo.md](final-closeout-sales-engineering-demo.md), [final-closeout-production-pilot-intake.md](final-closeout-production-pilot-intake.md), [final-closeout-pilot-intake-api.md](final-closeout-pilot-intake-api.md), [final-closeout-pilot-readiness-checklists.md](final-closeout-pilot-readiness-checklists.md), [final-closeout-enterprise-saas-handoff.md](final-closeout-enterprise-saas-handoff.md), a synthetic evidence package at `examples/demos/final-closeout-trial/sample-evidence-package.json`, a final-closeout pilot intake template at `examples/demos/final-closeout-trial/pilot-intake-template.json`, and a general trial-to-pilot intake template at `examples/demos/trial-to-pilot-intake/trial-to-pilot-intake-template.json`.

Trial teams must use synthetic or non-production evidence. Do not place Enterprise source code, private policy packs, customer templates, connector credentials, archive mutation logic, signing keys, or license validation secrets in this public repository.
