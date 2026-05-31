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

Use [final-closeout-trial.md](final-closeout-trial.md) for the customer-facing final closeout walkthrough. It covers final readiness evidence, signed archive manifest metadata, release closeout delivery, retention approval, artifact bundle download, retention health alerts, failed delivery retry planning, and the Community-to-Enterprise boundary.

Trial teams must use synthetic or non-production evidence. Do not place Enterprise source code, private policy packs, customer templates, connector credentials, archive mutation logic, signing keys, or license validation secrets in this public repository.
