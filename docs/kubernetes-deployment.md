# CAVRA Kubernetes Deployment Guide

This guide explains how to deploy the public CAVRA Community API as a container
microservice on Kubernetes using the Helm chart in `charts/cavra`.

## What The Chart Deploys

The chart deploys:

- CAVRA Community FastAPI/Uvicorn API.
- Kubernetes `Deployment`, `Service`, optional `Ingress`, optional TLS, optional
  HPA, optional PDB, optional NetworkPolicy, and a Helm test pod.
- Persistent volume backed SQLite stores by default.
- Optional PostgreSQL dependency or external PostgreSQL DSN scaffold.

Community API persistence currently defaults to JSON/SQLite stores. PostgreSQL
is provided as an optional deployment dependency and external DSN scaffold for
operators aligning with tenant/Enterprise persistence contracts. Do not assume
every public Community store automatically migrates to PostgreSQL unless the
operator has configured the corresponding adapter path.

## Container Image

The Community API image is built from:

- `docker/Dockerfile.azure-api`

The GitHub Container Registry publish workflow is:

- `.github/workflows/publish-community-api-image.yml`

Default image:

```text
ghcr.io/huzefaaa2/cavra-community-api:1.0.0
```

Build locally:

```bash
docker build -f docker/Dockerfile.azure-api -t cavra-community-api:local .
docker run --rm -p 8000:8000 cavra-community-api:local
curl http://127.0.0.1:8000/health
```

## Local kind Or minikube

Create a local cluster:

```bash
kind create cluster --name cavra
# or
minikube start
```

Install the chart with default SQLite-on-PVC persistence:

```bash
helm dependency build charts/cavra
helm install cavra charts/cavra --namespace cavra --create-namespace
kubectl -n cavra rollout status deployment/cavra
kubectl -n cavra port-forward svc/cavra 8000:80
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
```

Run the Helm test:

```bash
helm test cavra --namespace cavra
```

For kind with a locally built image:

```bash
docker build -f docker/Dockerfile.azure-api -t cavra-community-api:local .
kind load docker-image cavra-community-api:local --name cavra
helm upgrade --install cavra charts/cavra \
  --namespace cavra \
  --create-namespace \
  --set image.repository=cavra-community-api \
  --set image.tag=local \
  --set image.pullPolicy=Never
```

## Cloud AKS, EKS, Or GKE

The same chart can run on managed Kubernetes.

General flow:

```bash
kubectl create namespace cavra
helm dependency build charts/cavra
helm upgrade --install cavra charts/cavra \
  --namespace cavra \
  --set replicaCount=2 \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=5 \
  --set podDisruptionBudget.enabled=true \
  --set ingress.enabled=true \
  --set ingress.className=nginx \
  --set 'ingress.hosts[0].host=cavra.example.com' \
  --set 'ingress.hosts[0].paths[0].path=/' \
  --set 'ingress.tls[0].secretName=cavra-tls' \
  --set 'ingress.tls[0].hosts[0]=cavra.example.com'
```

Cloud notes:

- **AKS:** use Azure Key Vault CSI or External Secrets for connector, SMTP, and
  database secrets. Use Azure Database for PostgreSQL if enabling external
  Postgres.
- **EKS:** use AWS Load Balancer Controller, External Secrets Operator, and RDS
  for PostgreSQL where required.
- **GKE:** use GKE Ingress or Gateway, Secret Manager CSI or External Secrets,
  and Cloud SQL for PostgreSQL where required.

## On-Premises Kubernetes

For on-prem clusters, decide these platform dependencies first:

- Ingress controller: NGINX, HAProxy, Traefik, or Gateway API implementation.
- Storage class: backed by vSphere CSI, Ceph/Rook, Longhorn, NetApp, or another
  durable storage provider.
- Secret manager: Kubernetes Secrets, External Secrets, Vault, or a platform
  provider.
- TLS issuer: cert-manager with an internal CA, public ACME issuer, or manually
  managed certificate secrets.

Example:

```bash
helm upgrade --install cavra charts/cavra \
  --namespace cavra \
  --create-namespace \
  --set persistence.storageClass=longhorn \
  --set ingress.enabled=true \
  --set ingress.className=nginx \
  --set 'ingress.hosts[0].host=cavra.internal.example' \
  --set 'ingress.hosts[0].paths[0].path=/' \
  --set 'ingress.tls[0].secretName=cavra-internal-tls' \
  --set 'ingress.tls[0].hosts[0]=cavra.internal.example'
```

## Optional Bundled PostgreSQL

Use this mode for local trials or isolated lab environments, not for long-lived
production operations.

```bash
helm upgrade --install cavra charts/cavra \
  --namespace cavra \
  --create-namespace \
  --set postgresql.enabled=true \
  --set postgresql.auth.password='<replace-me>' \
  --set postgresql.auth.postgresPassword='<replace-me>'
```

The chart injects:

```text
CAVRA_DATABASE_URL
CAVRA_ENTERPRISE_POSTGRES_DSN
```

The public Community API still uses SQLite store variables unless you configure
or extend the appropriate persistence adapters.

## External PostgreSQL Mode

Use an external managed PostgreSQL service for production-style deployments.

Create a secret:

```bash
kubectl -n cavra create secret generic cavra-postgres \
  --from-literal=password='<postgres-password>'
```

Install:

```bash
helm upgrade --install cavra charts/cavra \
  --namespace cavra \
  --create-namespace \
  --set externalPostgresql.enabled=true \
  --set externalPostgresql.host=postgres.example.internal \
  --set externalPostgresql.database=cavra \
  --set externalPostgresql.username=cavra \
  --set externalPostgresql.existingSecret=cavra-postgres
```

## Secrets

Use `existingSecret` for production-sensitive values:

```bash
kubectl -n cavra create secret generic cavra-secrets \
  --from-literal=CAVRA_POLICY_SIGNING_KEY='<pem-or-secret-ref>' \
  --from-literal=CAVRA_GO_RELEASE_SIGNING_KEY='<pem-or-secret-ref>'

helm upgrade --install cavra charts/cavra \
  --namespace cavra \
  --set existingSecret=cavra-secrets
```

Do not commit SMTP passwords, connector tokens, tenant secrets, signing keys, or
private policy packs into Helm values files.

## TLS

With cert-manager:

```yaml
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: cavra.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: cavra-tls
      hosts:
        - cavra.example.com
```

For internal PKI, create the TLS secret yourself:

```bash
kubectl -n cavra create secret tls cavra-tls \
  --cert=tls.crt \
  --key=tls.key
```

## Validation

Run chart validation locally:

```bash
helm dependency build charts/cavra
helm lint charts/cavra
helm template cavra charts/cavra --namespace cavra > /tmp/cavra.yaml
helm template cavra charts/cavra --namespace cavra --set postgresql.enabled=true > /tmp/cavra-postgres.yaml
```

Runtime validation:

```bash
kubectl -n cavra rollout status deployment/cavra
kubectl -n cavra get pods,svc,ingress,pvc
kubectl -n cavra port-forward svc/cavra 8000:80
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/console/config
helm test cavra --namespace cavra
```

## Production Checklist

- Use at least two replicas with HPA/PDB where your storage and workload model
  allow it.
- Use an external managed PostgreSQL service for production persistence planning
  where Enterprise tenant isolation contracts require it.
- Use a real ingress controller, TLS, and DNS.
- Use secret management instead of plaintext values.
- Enable NetworkPolicy if your cluster CNI enforces it.
- Configure observability with your platform logging, metrics, and tracing.
- Validate `/health`, `/version`, and `/console/config` before exposing the API
  to users.
