# Deployment

Local CLI: install the Python package and run `cavra`.

API: run `uvicorn cavra.api:app --host 0.0.0.0 --port 8000`.

Sandbox UI: run `python -m http.server 5173 --directory apps/sandbox-ui`.

Self-hosted enterprise deployments should add persistent storage, OIDC, RBAC, SIEM export, immutable evidence storage, and approval workflow providers.
