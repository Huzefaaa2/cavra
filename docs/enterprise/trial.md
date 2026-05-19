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
