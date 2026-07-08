# CAVRA Kubernetes Deployment Guide

This guide explains how to deploy the public CAVRA Community API as a container
microservice on Kubernetes using the Helm chart in `charts/cavra`.

Main repository source:

- [Kubernetes Deployment Guide](https://github.com/Huzefaaa2/cavra/blob/main/docs/kubernetes-deployment.md)
- [CAVRA Helm Chart](https://github.com/Huzefaaa2/cavra/tree/main/charts/cavra)
- [Community API Image Workflow](https://github.com/Huzefaaa2/cavra/blob/main/.github/workflows/publish-community-api-image.yml)

## Quick Start

```bash
helm dependency build charts/cavra
helm install cavra charts/cavra --namespace cavra --create-namespace
kubectl -n cavra port-forward svc/cavra 8000:80
curl http://127.0.0.1:8000/health
```

## Deployment Modes

| Mode | Use |
| --- | --- |
| Local kind/minikube | Developer trial and chart smoke testing. |
| AKS/EKS/GKE | Managed Kubernetes deployment with cloud ingress, storage, secrets, and optional external Postgres. |
| On-prem Kubernetes | Private clusters with internal ingress, internal PKI, durable storage, and local secret management. |
| SQLite/PVC | Default Community persistence model. |
| Bundled PostgreSQL | Lab-only optional dependency for Postgres-adjacent testing. |
| External PostgreSQL | Production-style persistence planning and Enterprise tenant-isolation contracts. |

Community API persistence currently defaults to JSON/SQLite stores. PostgreSQL is
provided as an optional deployment dependency and external DSN scaffold for
operators aligning with tenant/Enterprise persistence contracts.

For the complete command set, TLS examples, external PostgreSQL mode, secrets,
and validation checklist, read the repository guide:

- [docs/kubernetes-deployment.md](https://github.com/Huzefaaa2/cavra/blob/main/docs/kubernetes-deployment.md)
