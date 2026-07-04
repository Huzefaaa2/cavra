# Zero-Trust Reference Deployments

CAVRA zero-trust reference deployments package the public Community runtime,
metadata-only scanner operation, and deployment smoke gates into reproducible
operator examples.

This page covers the R6.4 public reference layer: Docker Compose, Helm,
Terraform, Azure Container Apps, scanner operation, and readiness evidence.

## Reference Artifacts

| Artifact | Path | Purpose |
| --- | --- | --- |
| Docker Compose | `examples/reference-deployments/zero-trust/docker-compose.yml` | Runs CAVRA API plus a metadata-only customer-side scanner job. |
| Helm chart | `examples/reference-deployments/zero-trust/helm/cavra-zero-trust` | Kubernetes packaging baseline for private clusters and managed Kubernetes. |
| Terraform Azure | `examples/reference-deployments/zero-trust/terraform/azure` | Azure Container Apps, environment, logging, and scanner app skeleton. |
| Azure Bicep | `examples/reference-deployments/zero-trust/azure/container-apps.bicep` | Direct Azure Container Apps reference deployment. |
| Scanner runbook | `examples/reference-deployments/zero-trust/scanner-operation-runbook.md` | Customer-side metadata-only scanner operating checklist. |
| Quickstart demo | `examples/reference-deployments/zero-trust/quickstart-demo.md` | End-to-end validation commands and completion condition. |

## Required Controls

- Fail-closed runtime behavior.
- Metadata-only scanner output.
- Tenant and workspace scope.
- Private network mode support.
- Signed evidence references.
- No raw model, training data, prompt, source code, or secret egress.

## Validation

```bash
python3 scripts/validate_zero_trust_reference_deployments.py \
  --catalog examples/reference-deployments/zero-trust-reference-deployments.json \
  --repo-root .
```

```bash
python3 scripts/validate_zero_trust_reference_deployments.py \
  --packet examples/reference-deployments/zero-trust-reference-deployments.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

CLI equivalent:

```bash
cavra deployment zero-trust-catalog --repo-root .
cavra deployment zero-trust-readiness \
  examples/reference-deployments/zero-trust-reference-deployments.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

Live completion condition:

```text
ready_for_live_zero_trust_reference_deployments: true
blocker_count: 0
```

## Production Boundary

The public reference deployment validates packaging and contract shape. A real
Enterprise deployment must replace sanitized example refs with customer live
evidence from Docker Compose smoke tests, Helm rendering, Terraform validation,
Azure what-if review, scanner operation, evidence export, tenant/workspace
ownership, identity controls, private networking, and audit storage.

Use this page with [Zero-Trust Scanner Agent](Zero-Trust-Scanner-Agent.md),
[Azure Community Deployment](Azure-Community-SaaS-Deployment.md), and
[Azure Trial And Enterprise Deployment](Azure-Trial-And-Enterprise-Deployment.md).
