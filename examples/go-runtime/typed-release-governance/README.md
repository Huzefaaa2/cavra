# Typed Release Governance Go Runtime Examples

These examples show public-safe `EvaluateRequest` JSON payloads that use the generated `release_governance` contract field instead of a raw runtime `record` map.

The payloads can be evaluated directly:

```bash
cd go/cavra-runtime
go run ./cmd/cavra-runtime --input ../../examples/go-runtime/typed-release-governance/approved-promotion.json
```

They can also be sent through the local daemon transport:

```bash
cd go/cavra-runtime
go run ./cmd/cavra-runtime --lifecycle start \
  --socket .cavra/cavra-runtime.sock \
  --evidence-log .cavra/go-daemon/release-governance-evidence.jsonl

go run ./cmd/cavra-runtime --daemon \
  --socket .cavra/cavra-runtime.sock \
  --input ../../examples/go-runtime/typed-release-governance/failed-connector-delivery.json

go run ./cmd/cavra-runtime --lifecycle stop --socket .cavra/cavra-runtime.sock
```

## Request Files

- `approved-promotion.json` should return `allow` with `release_governance.approval.approved`.
- `failed-connector-delivery.json` should return `block` with `release_governance.delivery.failed`.
- `critical-inventory-freshness.json` should return `require_approval` with `release_governance.signal.critical`.

## CI Runner Usage

Reference CI templates are available for:

- GitHub Actions: `examples/github-actions/cavra-release-governance-go-runtime.yml`
- GitLab CI: `examples/gitlab-ci/cavra-release-governance-go-runtime.gitlab-ci.yml`
- Azure Pipelines: `examples/azure-pipelines/cavra-release-governance-go-runtime.azure-pipelines.yml`

The templates run the Go daemon, send the typed request, validate the expected decision, and publish daemon evidence artifacts.

Reusable runner assets are available for signed runtime packages:

- Shell wrapper: `examples/ci-runners/cavra-release-governance-runner.sh`
- GitHub composite action: `examples/github-actions/actions/cavra-release-governance-go-runtime/action.yml`
- Release package manifest: `cavra-runtime.ci-runner-bundles.json`

The shell wrapper and composite action are included in signed Go runtime release packages by `scripts/package_go_release.py`, so CI owners can verify the package once, install the referenced runtime binary, and run typed release-governance daemon checks without rebuilding from source.
