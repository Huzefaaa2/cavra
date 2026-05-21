# Go Backend Deployment Readiness

CAVRA now separates Go backend pilot readiness from deployment readiness. Pilot readiness proves that a local Go runtime can be selected safely. Deployment readiness proves that CI runner and workstation rollout paths have the metadata needed for controlled production use.

## What It Checks

The deployment readiness report evaluates public-safe release metadata:

- `cavra-runtime.endpoint-deployment.json`
- `cavra-runtime.ci-runner-bundles.json`
- `cavra-runtime.channels.json`
- `cavra-runtime.updater-policy.json`

It checks that:

- CI runner bundles reference endpoint deployment metadata.
- CI runner targets are declared as `ci-runner` surfaces.
- CI runner controls include signed runtime verification, runner authentication, signed daemon evidence, evidence verification output, and fail-closed behavior.
- Workstation release channels require approval.
- Workstation channels disable automatic updates by default.
- Workstation channel targets include deployment guidance.
- Workstation updater policy references the channel manifest and matches channel names.

## Environment Variables

Use a verified Go runtime release package directory:

```bash
export CAVRA_GO_RUNTIME_PACKAGE_DIR=/opt/cavra/go-runtime-release
```

Or configure individual metadata files:

```bash
export CAVRA_GO_ENDPOINT_DEPLOYMENT_MANIFEST=/opt/cavra/cavra-runtime.endpoint-deployment.json
export CAVRA_GO_CI_RUNNER_BUNDLES=/opt/cavra/cavra-runtime.ci-runner-bundles.json
export CAVRA_GO_WORKSTATION_CHANNELS=/opt/cavra/cavra-runtime.channels.json
export CAVRA_GO_WORKSTATION_UPDATER_POLICY=/opt/cavra/cavra-runtime.updater-policy.json
```

## CLI Usage

```bash
cavra runtime go-deployment-readiness \
  --mode shadow \
  --package-dir /opt/cavra/go-runtime-release \
  --json
```

## API Usage

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/deployment-readiness
```

The production readiness endpoint includes the same result under `go_backend_deployment`:

```bash
curl http://127.0.0.1:8000/deployment/production-readiness
```

## Status Rules

- `not_configured`: acceptable when the Go backend pilot is disabled.
- `needs_attention`: deployment metadata is missing, malformed, or incomplete when the Go backend pilot is enabled.
- `ready`: CI runner and workstation metadata passed readiness checks.

## User Stories

- As a CI owner, I can prove runner bundles publish required daemon evidence before enabling Go-backed enforcement in pipelines.
- As an endpoint engineering lead, I can verify workstation release channels remain approval-bound before distributing the Go runtime.
- As a security architect, I can block Go pilot promotion until runner and workstation deployment paths have documented controls.
- As an auditor, I can attach deployment readiness evidence to a release or pilot approval record.

## Enterprise Challenge Solved

Go runtime adoption touches developer laptops and CI runners. Those surfaces need tighter change-control evidence than a local smoke test. This readiness report gives platform teams a repeatable way to verify runner and workstation rollout metadata before production use.

## Next Work

The next recommended implementation step is to add recurring rollback drill scheduling and stale-drill notification delivery.
