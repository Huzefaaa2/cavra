# CAVRA Zero-Trust Reference Deployment Quickstart

This quickstart demonstrates CAVRA API gating plus customer-side scanner
operation without raw model, prompt, source, or training-data egress.

## Docker Compose

```bash
docker compose -f examples/reference-deployments/zero-trust/docker-compose.yml up --build
```

Then validate the reference catalog:

```bash
python3 scripts/validate_zero_trust_reference_deployments.py \
  --catalog examples/reference-deployments/zero-trust-reference-deployments.json \
  --repo-root .
```

## Helm

```bash
helm template cavra examples/reference-deployments/zero-trust/helm/cavra-zero-trust
```

## Terraform

```bash
terraform -chdir=examples/reference-deployments/zero-trust/terraform/azure init
terraform -chdir=examples/reference-deployments/zero-trust/terraform/azure validate
```

## Azure What-If

```bash
az deployment group what-if \
  --resource-group <resource-group> \
  --template-file examples/reference-deployments/zero-trust/azure/container-apps.bicep \
  --parameters cavraApiImage=<image> tenantId=<tenant> workspaceId=<workspace>
```

## Readiness Gate

```bash
cavra deployment zero-trust-readiness \
  examples/reference-deployments/zero-trust-reference-deployments.live.sanitized.example.json \
  --repo-root . \
  --require-live
```

The reference completion condition is:

```text
ready_for_live_zero_trust_reference_deployments: true
blocker_count: 0
```
