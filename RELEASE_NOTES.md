# CAVRA Release Notes

## Current Release: CAVRA Community v1.0.0

CAVRA Community `1.0.0` is the stable public Community baseline for Controlled
Agentic Verification and Runtime Authority.

- **GitHub release:** [`community-v1.0.0`](https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0)
- **Release documentation:** [`docs/releases/community-v1.0.0.md`](docs/releases/community-v1.0.0.md)
- **Release index:** [`docs/community-release-index.md`](docs/community-release-index.md)
- **Readiness dashboard:** [`docs/community-release-readiness-dashboard.md`](docs/community-release-readiness-dashboard.md)
- **Post-publication verification:** [`docs/release-verifications/community-v1.0.0-post-publication-verification.md`](docs/release-verifications/community-v1.0.0-post-publication-verification.md)

The release was published from merged `main` commit
`bb5dd1005e9c2efb6e7e4df40ad153751476a6d2` at `2026-06-05T07:30:35Z`.

## What Is Included

Community v1.0.0 includes the public self-hosted CAVRA baseline:

- Python package and `cavra` CLI.
- FastAPI/Uvicorn API surface.
- Runtime authority checks for files, commands, Git, MCP/tool workflows, and agent actions.
- YAML policy packs with JSON Schema validation.
- Policy signing, verification, lifecycle, diff, compile, dry-run, and Rego export paths.
- Approval routing, provider payloads, and delivery contracts.
- Evidence bundles, signed manifests, trust roots, SIEM exports, retention plans, and searchable metadata.
- Agent registry, MCP trust registry, and trust classifications.
- AISPM report, review-packet, CI-gate, trial, pilot, production-readiness, and operating evidence contracts.
- Community sandbox UI and product documentation surfaces.
- Docker and Azure deployment references for Community API and static UI.
- Release governance, roadmap closeout, and future-work intake validators.

## Published Artifacts

| Artifact | SHA-256 | Size |
| --- | --- | --- |
| `cavra-1.0.0-py3-none-any.whl` | `464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914` | 324060 bytes |
| `cavra-1.0.0.tar.gz` | `851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331` | 1043690 bytes |
| `cavra-1.0.0-SHA256SUMS.txt` | `c9049c68d23e089f2129ab3f1f130f7a8e07aecc4bb1e8b4b5360b22a5c617fd` | 274 bytes |
| `cavra-1.0.0.provenance.json` | `38b6e2127695050e697d33dde22f111eaee5cccbcf598cb82fc60c6a795c99aa` | 893 bytes |

Verification command:

```bash
python3 scripts/verify-community-release-artifacts.py \
  --tag community-v1.0.0 \
  --version 1.0.0 \
  --wheel-sha256 464e7146f74a039b89fe1f163f9b825df7a700942be480c32e611f00fe625914 \
  --sdist-sha256 851f28a38a6e9df6cbe7637a3963a1dc8eb535478730d3ff3eccf260a025d331
```

Observed clean install smoke:

```text
cavra 1.0.0
```

## Attestation And Verification

The release uses GitHub keyless release asset attestation through
`.github/workflows/attest-community-release.yml`.

Workflow run `27003626701` downloaded the published assets, validated SHA-256
checksums, generated a Sigstore-backed attestation with `actions/attest@v4`,
and verified each asset with `gh attestation verify`.

Attestation `29988580` is available at
<https://github.com/Huzefaaa2/cavra/attestations/29988580>.

## Upgrade Notes

- From Community v0.1.x: install the final `1.0.0` wheel or source distribution,
  then run `cavra version`, `cavra policy list`, and an evidence bundle smoke.
- From Community v1.0.0 RC1: replace the release-candidate package with the
  final `1.0.0` package, rerun policy validation, and verify evidence bundle
  generation.
- Enterprise source, paid policy packs, managed service internals, private
  connector credentials, license-service internals, customer records, and private
  signing material are outside this public Community artifact.

## Release History

| Release | Status | Notes |
| --- | --- | --- |
| [`community-v1.0.0`](docs/releases/community-v1.0.0.md) | Stable public baseline | Current Community release. |
| [`community-v1.0.0-rc.1`](docs/releases/community-v1.0.0-rc.1.md) | Superseded RC | Release candidate before final GA. |
| [`community-v1.0.0-aispm`](docs/releases/community-v1.0.0-aispm.md) | AISPM milestone | AISPM public release readiness record. |
| [`community-v0.1.3`](docs/releases/community-v0.1.3.md) | Superseded | Pre-GA Community milestone. |
| [`community-v0.1.2`](docs/releases/community-v0.1.2.md) | Superseded | Pre-GA Community milestone. |
| [`community-v0.1.1`](docs/releases/community-v0.1.1.md) | Superseded | Pre-GA Community milestone. |
| [`community-v0.1.0`](docs/releases/community-v0.1.0.md) | Superseded | Initial public Community release record. |

## Documentation Start Points

- Public documentation map: [`docs/public-documentation-map.md`](docs/public-documentation-map.md)
- Full CLI reference: [`docs/cli-reference.md`](docs/cli-reference.md)
- GitHub Wiki textbook: <https://github.com/Huzefaaa2/cavra/wiki>
- Product website: <https://cavra.mind-ops.cloud/>
