# CAVRA Dual-Plane Architecture

CAVRA keeps Python as the management plane and introduces Go as an optional enforcement plane after interface parity exists.

Management plane responsibilities: policy authoring, registry, inheritance, compliance packs, risk classification, evidence, PR attestation, webhooks, SIEM/ITSM exports, FastAPI, Claude Code adapters, MCP adapters, documentation, approval routing, and SaaS/self-hosted services.

Enforcement plane responsibilities: low-latency decisions for file, command, Git, MCP, local session daemon, CI runner enforcement, audit event streaming, air-gapped deployment, and gRPC or Unix-socket interfaces.

The Python runtime remains authoritative until Go parity tests prove equivalent decisions.
