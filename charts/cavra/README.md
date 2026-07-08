# CAVRA Helm Chart

This chart deploys the public CAVRA Community API as a Kubernetes microservice.

Community defaults to SQLite-backed stores on a persistent volume. PostgreSQL is
available as an optional dependency or external DSN scaffold for operators who
are preparing Managed/Enterprise-style persistence contracts.

## Quick Start

```bash
helm dependency build charts/cavra
helm install cavra charts/cavra --namespace cavra --create-namespace
kubectl -n cavra port-forward svc/cavra 8000:80
curl http://127.0.0.1:8000/health
```

## Optional Bundled PostgreSQL

```bash
helm install cavra charts/cavra \
  --namespace cavra \
  --create-namespace \
  --set postgresql.enabled=true \
  --set postgresql.auth.password='<change-me>' \
  --set postgresql.auth.postgresPassword='<change-me>'
```

## External PostgreSQL

```bash
helm install cavra charts/cavra \
  --namespace cavra \
  --create-namespace \
  --set externalPostgresql.enabled=true \
  --set externalPostgresql.host='postgres.example.internal' \
  --set externalPostgresql.username='cavra' \
  --set externalPostgresql.password='<secret>'
```

For production, prefer `externalPostgresql.existingSecret` instead of plaintext
`--set` values.
