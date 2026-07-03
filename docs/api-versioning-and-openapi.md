# CAVRA API Versioning And OpenAPI Contract

Last updated: 2026-07-03

CAVRA publishes a checked-in OpenAPI contract for the public API surface. This implements Phase 1 roadmap item R1.4 and gives Community, Managed, Enterprise Subscription, connector, and SDK work a stable compatibility baseline.

## Canonical Contract

The canonical contract is:

```text
openapi/cavra-api.openapi.json
```

Regenerate it with:

```bash
python3 scripts/export_openapi_contract.py
```

Validate it with:

```bash
python3 scripts/validate_openapi_contract.py
```

The validator checks that the checked-in contract matches `create_app().openapi()`, uses the package version, includes CAVRA versioning metadata, and exposes required stable paths.

## Versioning Rules

| Change Type | Allowed In `cavra.api.v1` | Requirement |
| --- | --- | --- |
| Add optional response fields | Yes | Document the field and keep existing fields stable. |
| Add optional request fields | Yes | Defaults must preserve existing behavior. |
| Add a new endpoint | Yes | Add OpenAPI coverage and docs. |
| Rename or remove fields | No | Requires new versioned path, media type, or major API contract. |
| Change decision semantics | No | Requires RFC, migration guidance, and compatibility tests. |
| Change auth/RBAC behavior | No | Requires RFC, security review, and regression tests. |
| Change evidence schema semantics | No | Requires RFC, verifier compatibility review, and migration plan. |

## Stability Classes

| Surface | Stability |
| --- | --- |
| `/health`, `/version`, `/console/config` | Stable |
| `/decisions`, `/approvals`, `/evidence` | Stable |
| `/aispm/*` | Stable public contract unless marked preview. |
| `/runtime/go-pilot/*` | Preview until promoted in release notes. |
| Future connector SDK endpoints | Must be versioned before certified connector release. |
| Future model/artifact endpoints | Must preserve no-raw-model-egress and by-reference artifact handling. |

## Breaking Change Gate

Breaking API changes require:

1. RFC approval.
2. OpenAPI diff showing the change.
3. Migration guidance.
4. Compatibility tests.
5. Roadmap status update.
6. Release note with deprecation or replacement path.

## Public Contract Metadata

The OpenAPI document includes:

- `x-cavra-api-versioning.public_contract`: `cavra.api.v1`;
- `x-cavra-api-versioning.compatibility`: breaking-change guidance;
- `x-cavra-api-versioning.stability`: endpoint stability classes;
- `x-cavra-governed-assets`: `agent_actions` and `models_and_artifacts`.
