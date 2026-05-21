# Diagrams

## C4 Context

See `docs/diagrams/c4-context.md`.

## C4 Container

See `docs/diagrams/c4-container.md`. The current container diagram marks the Approval Router as an implemented JSON/SQLite-backed lifecycle service with repository routing, signed OIDC/JWKS validation, repository RBAC, Entra/Okta deployment references, console actions, console break-glass creation, approval audit details, provider request specs, and live provider delivery evidence. It also marks the Agent and MCP Trust Registry as a JSON/SQLite implementation for governed agent identities, MCP trust decisions, predefined agent profiles, MCP capability classifications, and console registry views. The metadata store now includes JSON/SQLite evidence, session, decision, approval, registry, repository inventory, policy rollout metadata, policy authoring previews, approval-bound signed policy publishing, rollout change plans, deployment readiness checks, integration inventory, connector delivery records, backup/restore operations, retention planning, and governed evidence artifact retrieval. The evidence plane now feeds CI/CD required-check artifacts for GitHub, GitLab, Azure DevOps templates, configured SIEM/ITSM/ChatOps/webhook connector hooks, and AWS/Azure immutable evidence storage references. The console security boundary and console session context are exposed as OIDC/RBAC/CORS readiness and authenticated actor metadata. The Go enforcement plane is now shown as a scaffolded parity-tested container with daemon transport and client mode, and the sandbox is shown as GitHub Pages deployable.

## Agent and MCP Registry

See `docs/diagrams/agent-mcp-registry.svg` for the dedicated registry view that separates profiles, registered identities, trust records, classifications, storage modes, runtime decisions, console views, and evidence consumers.

## Runtime Components

See `docs/diagrams/c4-component-runtime.md`.

## Runtime Decision Flow

See `docs/diagrams/runtime-decision-flow.md`.

## Evidence Lifecycle

See `docs/diagrams/evidence-lifecycle.md`.

## Immutable Evidence Storage

See `docs/diagrams/immutable-evidence-storage.svg` for the dedicated immutable storage flow from runtime decision, signed bundle, verifier gate, and storage plan into AWS S3 Object Lock and Azure Blob immutability.

## OIDC/RBAC Deployment

See `docs/diagrams/oidc-rbac-deployment.svg` for the dedicated identity flow from Entra ID or Okta discovery metadata and group claims into CAVRA OIDC config, repository RBAC, console sessions, approvals, and break-glass decisions.

## Go Parity and Sandbox Deployment

See `docs/diagrams/go-parity-sandbox-deployment.svg` for the dedicated flow from authoritative Python runtime behavior through shared parity fixtures, Go runtime tests, required CI checks, sandbox source, GitHub Pages deployment, and the future promotion gate.

## Runner OIDC and Evidence Verification

The release-governance runner wrapper now acquires provider OIDC tokens from GitHub Actions, GitLab CI, or Azure Pipelines when available, sends signed or OIDC-backed `runner_auth` to the Go daemon, records hash-chained evidence, verifies the evidence stream, and publishes `release-governance-evidence-verification.json` as an audit artifact. Custody and rotation guidance is documented in `Runner-Auth-And-Evidence-Key-Custody.md`.

## Go Reproducible Air-Gapped Build Flow

See `docs/diagrams/go-reproducible-airgap.svg` for the release path from connected GitHub Actions build, checksums, SBOM, signatures, provenance, and reproducibility metadata to restricted-environment verification and optional binary rebuild.

## Release Signing Operations

See `docs/diagrams/release-signing-operations.svg` for the release path from external signing key custody into signed package generation, verifier enforcement, planned key rotation, and emergency revocation evidence.

## High-Risk Command And Cloud/IaC Parity

See `docs/diagrams/high-risk-command-cloud-iac-parity.svg` for the shared fixture path that compares authoritative Python runtime decisions with Go runtime decisions before Go is allowed into deployment paths.

## Opt-In Go Backend Pilot

See `docs/diagrams/go-backend-pilot.svg` for the guarded backend-selection flow from operator opt-in through Python evaluation, Go comparison, parity gate, fallback, and readiness evidence.

## Go Backend Deployment Readiness

See `docs/diagrams/go-backend-deployment-readiness.svg` for the CI runner and workstation readiness path that checks release metadata before Go backend promotion.

## Go Backend Promotion Gate

See `docs/diagrams/go-backend-promotion.svg` for the promotion gate that requires runtime readiness, deployment readiness, audited parity evidence, and approval before `promoted` mode selects Go.

## Go Backend Rollback Controls

See `docs/diagrams/go-backend-rollback.svg` for the rollback gate that requires an approved plan back to Python-only mode before `promoted` mode selects Go.

## SVG Images

Repository diagram images:

- `docs/diagrams/architecture-context.svg`
- `docs/diagrams/c4-container.svg`
- `docs/diagrams/runtime-flow.svg`
- `docs/diagrams/evidence-hub.svg`
- `docs/diagrams/immutable-evidence-storage.svg`
- `docs/diagrams/oidc-rbac-deployment.svg`
- `docs/diagrams/go-parity-sandbox-deployment.svg`
- `docs/diagrams/go-reproducible-airgap.svg`
- `docs/diagrams/release-signing-operations.svg`
- `docs/diagrams/high-risk-command-cloud-iac-parity.svg`
- `docs/diagrams/go-backend-pilot.svg`
- `docs/diagrams/go-backend-deployment-readiness.svg`
- `docs/diagrams/go-backend-promotion.svg`
- `docs/diagrams/go-backend-rollback.svg`
- `docs/diagrams/policy-lifecycle.svg`
- `docs/diagrams/developer-journey.svg`
- `docs/diagrams/agent-orchestration.svg`
