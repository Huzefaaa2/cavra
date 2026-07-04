# Zero-Trust Reference Deployments

CAVRA zero-trust reference deployments package the public Community runtime,
metadata-only scanner operation, and deployment smoke gates into reproducible
operator examples.

This is the public reference layer for R6.4 of the unified roadmap. It does not
claim that a customer's live environment is production-ready by itself. It gives
operators a validated starting point for Docker Compose, Kubernetes, Terraform,
Azure Container Apps, scanner operation, and readiness evidence.

## What Is Included

| Artifact | Path | Purpose |
| --- | --- | --- |
| Docker Compose | `examples/reference-deployments/zero-trust/docker-compose.yml` | Runs the CAVRA API plus a metadata-only customer-side scanner job. |
| Helm chart | `examples/reference-deployments/zero-trust/helm/cavra-zero-trust` | Kubernetes packaging baseline for private clusters and managed Kubernetes. |
| Terraform Azure | `examples/reference-deployments/zero-trust/terraform/azure` | Azure Container Apps, environment, logging, and scanner app skeleton. |
| Azure Bicep | `examples/reference-deployments/zero-trust/azure/container-apps.bicep` | Direct Azure Container Apps reference deployment. |
| Scanner runbook | `examples/reference-deployments/zero-trust/scanner-operation-runbook.md` | Customer-side metadata-only scanner operating checklist. |
| Quickstart demo | `examples/reference-deployments/zero-trust/quickstart-demo.md` | End-to-end validation commands and completion condition. |

## Security Controls

The reference catalog requires these controls:

- fail-closed runtime behavior;
- metadata-only scanner output;
- tenant and workspace scope;
- private network mode support;
- signed evidence references;
- no raw model, training data, prompt, source code, or secret egress.

## Validate The Catalog

```bash
python3 scripts/validate_zero_trust_reference_deployments.py \
  --catalog examples/reference-deployments/zero-trust-reference-deployments.json \
  --repo-root .
```

The validator checks that all required deployment artifacts are listed and that
each source file contains required zero-trust markers.

## Validate Sample Readiness

```bash
python3 scripts/validate_zero_trust_reference_deployments.py \
  --packet examples/reference-deployments/zero-trust-reference-deployments.sample.json \
  --repo-root .
```

Sample mode validates contract shape and file coverage. It returns warnings
because it is not live evidence.

## Validate Live Sanitized Readiness

```bash
python3 scripts/validate_zero_trust_reference_deployments.py \
  --packet examples/reference-deployments/zero-trust-reference-deployments.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Live completion condition:

```text
ready_for_live_zero_trust_reference_deployments: true
blocker_count: 0
```

For a real customer environment, replace the sanitized example references with
actual live evidence references from Docker Compose smoke tests, Helm template
rendering, Terraform validation, Azure what-if review, scanner operation,
evidence export, and tenant/workspace ownership.

## CLI

```bash
cavra deployment zero-trust-catalog --repo-root .
cavra deployment zero-trust-export --output-dir dist/zero-trust-reference-deployments
cavra deployment zero-trust-readiness \
  examples/reference-deployments/zero-trust-reference-deployments.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

## Relationship To The Scanner Agent

The reference deployment layer builds on the [Zero-Trust Scanner Agent](zero-trust-scanner-agent.md).
The scanner contract proves metadata-only result shape and forbidden raw-egress
blocking. The reference deployment contract proves that operators have a
repeatable deployment path for running that scanner beside the runtime API.

Production Enterprise deployments still require customer-specific network,
identity, secrets, tenant isolation, evidence storage, connector, and readiness
gate evidence.
