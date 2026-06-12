# AISPM Enterprise Live Ingestion

This document defines the public-safe Phase C design for CAVRA AI Security
Posture Management Enterprise Live Ingestion.

The implementation belongs in the private `cavra-enterprise` repository. The
public Community repository may contain this contract, schemas, examples, and
documentation only.

## Goal

Phase C turns the Community AISPM dashboard model into a live Enterprise
ingestion plane that can receive, normalize, secure, persist, and stream
AI-agent activity for authenticated CSO/CISO, security, platform, and auditor
views.

## Target Flow

```text
AI coding agent / MCP / CI runner / cloud workflow
  -> Enterprise collector
  -> Authenticated ingestion endpoint
  -> Redaction and normalization
  -> Policy decision and evidence linkage
  -> Tenant-isolated event store
  -> Streaming posture update
  -> CSO/CISO dashboard, audit replay, and compliance evidence
```

## Event Sources

Enterprise collectors should support these source classes:

| Source | Example events |
| --- | --- |
| AI coding agents | prompts, responses, tool requests, file actions, shell commands, Git operations |
| MCP servers | tool registrations, tool calls, trust decisions, denied calls |
| CI/CD runners | workflow jobs, required checks, PR attestations, artifact links |
| Cloud and IaC | plan metadata, drift events, deployment attempts, approval gates |
| CAVRA runtime | policy decisions, approvals, evidence refs, runtime modes |
| Identity and governance | actor refs, approver refs, RBAC scopes, policy versions |

Raw prompts, model reasoning, tool output, customer payloads, and private
connector responses must be stored only in private Enterprise storage when the
tenant has explicitly enabled that collection mode.

## Public Envelope Contract

The public envelope schema is:

`src/cavra/schemas/aispm-enterprise-live-ingestion-envelope.schema.json`

The public-safe example is:

`examples/aispm/enterprise-live-ingestion-envelope-public-contract.example.json`

The envelope intentionally contains metadata, redacted summaries, opaque
private references, integrity metadata, and Enterprise boundary markers. It
does not embed raw prompts, model reasoning, tool output, secrets, customer
records, private policy-pack implementation, license secrets, or provider
credentials.

## Private Enterprise Components

The private implementation should add these modules to `cavra-enterprise`:

```text
src/cavra_enterprise/
  aispm_ingestion/
    collectors/
      codex.py
      claude_code.py
      github_copilot.py
      cursor.py
      gemini_cli.py
      mcp.py
      ci.py
      cloud_iac.py
    api.py
    normalizer.py
    redaction.py
    integrity.py
    tenant_store.py
    stream.py
    retention.py
    replay_index.py
    dashboard_projection.py
```

## Ingestion API Shape

The private API should expose authenticated endpoints similar to:

| Endpoint | Purpose |
| --- | --- |
| `POST /enterprise/aispm/events` | Receive one normalized event envelope. |
| `POST /enterprise/aispm/events/batch` | Receive a bounded batch of envelopes. |
| `GET /enterprise/aispm/stream` | Stream tenant-scoped posture updates through SSE or WebSocket. |
| `GET /enterprise/aispm/events/{event_id}` | Retrieve tenant-authorized event metadata. |
| `GET /enterprise/aispm/replay/{session_id}` | Build authorized replay from normalized events and private payload refs. |
| `GET /enterprise/aispm/ingestion/health` | Report collector lag, rejected events, retry counts, and storage status. |

These endpoints must not be implemented in the public repository.

## Security Requirements

- Authenticate every collector with tenant-scoped credentials, workload
  identity, signed runner claims, or mTLS.
- Authorize ingestion by tenant, repository, connector, environment, and
  allowed event type.
- Validate every envelope against the public contract and private semantic
  rules before persistence.
- Enforce idempotency through `event_id` and `transport.idempotency_key`.
- Sign or hash private payloads before storage.
- Preserve hash-chain or append-only audit metadata for policy decisions,
  approvals, overrides, and evidence access.
- Redact or tokenize sensitive fields before dashboard projection.
- Separate raw private payload storage from dashboard projection storage.
- Apply tenant-specific retention, legal hold, object-lock, and KMS policies.
- Emit ingestion health evidence for failed validation, dropped events, stale
  collectors, queue lag, and storage failures.

## Tenant Data Model

Enterprise storage should separate:

| Store | Data |
| --- | --- |
| Event envelope store | Validated metadata, event IDs, timestamps, source refs, policy refs |
| Private payload store | Raw prompts, reasoning, tool output, connector payloads when enabled |
| Projection store | Dashboard-ready posture summaries and indexes |
| Evidence store | Signed evidence refs, immutable audit packets, retention metadata |
| Replay index | Session timelines, step order, related approvals, related evidence |

## Streaming Model

Phase C should support near-real-time dashboard updates without making the
public Community portal a live Enterprise service.

Recommended model:

1. Collectors submit events over authenticated HTTPS.
2. Normalizer writes accepted envelopes to the tenant event store.
3. Projection worker updates posture views.
4. Stream service emits tenant-scoped SSE or WebSocket deltas.
5. Dashboard receives only authorized projections for the logged-in user role.

## Public Community Boundary

Community may contain:

- this design document;
- the public envelope schema;
- a redacted example envelope;
- dashboard contracts and sample data;
- upgrade messages that mark live ingestion as Enterprise-only.

Community must not contain:

- collector implementations for private platforms;
- tenant database code for live ingestion;
- raw prompt or reasoning capture;
- license enforcement code;
- private signing keys;
- customer identifiers;
- provider credentials;
- commercial policy packs;
- SaaS backend implementation.

## Acceptance Criteria

Phase C is ready for Enterprise trial when:

- authenticated collectors can submit valid envelopes;
- invalid, unsigned, or unauthorized envelopes are rejected;
- duplicate event IDs are idempotent;
- accepted events appear in tenant-scoped posture projections;
- SSE or WebSocket streams update the Enterprise dashboard;
- raw payload access is RBAC-controlled and audited;
- retention and KMS/object-lock readiness are enforced;
- ingestion health shows lag, failures, and collector status;
- replay can reconstruct a session from normalized events and private payload
  refs;
- public documentation remains free of private code and secrets.

## Next Step

Implement the private `cavra_enterprise.aispm_ingestion` package against this
contract, then add a private Enterprise Trial validation run that demonstrates
one live collector, one policy decision stream, one dashboard update, and one
auditor replay packet.
