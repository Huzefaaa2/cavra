# AISPM Enterprise Live Ingestion

This page summarizes the public-safe Phase C design for CAVRA AI Security
Posture Management Enterprise Live Ingestion.

The implementation belongs in the private `cavra-enterprise` repository. The
public Community repository contains only contracts, schemas, examples, and
documentation.

## Goal

Phase C receives live AI-agent, MCP, CI/CD, cloud/IaC, policy-decision,
approval, and evidence events, then converts them into tenant-scoped posture
streams for the Enterprise CSO/CISO dashboard.

## Flow

```text
AI coding agent / MCP / CI runner / cloud workflow
  -> Enterprise collector
  -> Authenticated ingestion endpoint
  -> Redaction and normalization
  -> Tenant-isolated event store
  -> Streaming posture update
  -> CSO/CISO dashboard and audit replay
```

## Public Contract

Public schema:

`src/cavra/schemas/aispm-enterprise-live-ingestion-envelope.schema.json`

Public-safe example:

`examples/aispm/enterprise-live-ingestion-envelope-public-contract.example.json`

The envelope uses metadata, redacted summaries, opaque private references,
integrity metadata, and Enterprise boundary markers. It does not embed raw
prompts, model reasoning, tool output, secrets, customer records, private
policy-pack implementation, license secrets, or provider credentials.

## Private Enterprise Scope

Private implementation should include collectors for AI coding agents, MCP
servers, CI/CD runners, and cloud/IaC systems; authenticated ingestion APIs;
normalization; redaction; integrity checks; tenant event storage; streaming
updates; replay indexes; retention controls; and dashboard projections.

## Security Controls

- Tenant-scoped collector authentication.
- Event authorization by connector, repository, environment, and event type.
- Envelope schema validation plus private semantic validation.
- Idempotent event handling.
- Signed or hashed payload references.
- RBAC-controlled raw payload access.
- Tenant retention, legal hold, KMS, and object-lock enforcement.
- Ingestion health evidence for lag, rejected events, retries, and storage
  failures.

## Boundary

Community may document the design and ship the public schema/example.
Community must not ship private collectors, tenant event stores, raw prompt
capture, license enforcement, provider credentials, customer identifiers,
commercial policy packs, or SaaS backend implementation.

## Canonical Document

The canonical design is
`docs/architecture/aispm-enterprise-live-ingestion.md`.
