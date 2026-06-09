# AI Security Posture Dashboard Contract

CAVRA now exposes the first public-safe AI Security Posture Management
dashboard contract for Community Edition. Phase A defines the contract, and the
current Phase B hardening adds Community control coverage, near-miss visibility,
public-safe trace replay packets, and public-safe approval lineage without
exposing Enterprise live-ingestion logic.

## Community Boundary

Community Edition provides local and sample posture views only:

- `GET /aispm/dashboard/contract` describes Community and Enterprise
  boundaries.
- `GET /aispm/dashboard/sample` returns deterministic sample dashboard data for
  the static portal and demos.
- `GET /aispm/posture` derives posture from the local activity store.
- `GET /aispm/agents` returns agent coverage summaries.
- `GET /aispm/findings` returns public-safe risk findings from policy
  decisions.
- `GET /aispm/timeline` returns a local execution timeline from sessions and
  decisions.
- `GET /aispm/control-coverage` returns observed Community coverage by
  sensitive-data, infrastructure, MCP/tool, source-control, runtime-command, and
  general-policy surfaces.
- `GET /aispm/near-misses` returns warned, approval-gated, or attested risky
  actions that should be reviewed before they become incidents.
- `GET /aispm/trace-replay/{session_id}` returns a public-safe replay packet
  from local session decisions with sensitive targets summarized.
- `GET /aispm/approval-lineage` returns public-safe approval lineage from the
  local approval store with role-labelled actors and private IdP/RBAC context
  locked to Enterprise.

The public portal now includes an `AI Posture` route that renders this contract
as a static-hostable dashboard. When `window.CAVRA_API_BASE` is configured it
loads `/aispm/posture`; otherwise it falls back to deterministic sample data and
labels the view as `sample_data`. The route includes posture overview, agent
coverage, risk findings, control coverage, near-miss queue, execution timeline,
approval lineage, and the raw public-safe payload.

Community trace replay reconstructs normalized decision steps, evidence
references, risk classifications, and redaction status. It does not expose raw
prompts, model reasoning, raw tool output, private customer context, or
Enterprise replay retention logic.

Community approval lineage reconstructs "who approved what" from local approval
records using approver groups, state, timestamps, decision linkage, and evidence
references. Human actors are reduced to role labels; raw identity-provider
claims, RBAC policy context, private routing rules, and connector payloads
remain Enterprise-only.

The public contract uses existing CAVRA activity metadata. It does not capture
private prompts, proprietary reasoning traces, Enterprise policy logic,
customer data, license-server state, or SaaS tenant records.

## Enterprise Boundary

Enterprise remains responsible for live, authenticated, multi-tenant AISPM:

- prompt and reasoning trace capture;
- tool-call graph and full trace replay;
- organization-wide control coverage;
- live policy distribution status;
- kill switch, quarantine, policy toggles, and runtime overrides;
- centralized retention, immutable audit exports, and compliance reports.

The public API marks those capabilities as `requires_cavra_enterprise`.

## Data Provenance

Every dashboard response includes provenance fields so operators can distinguish
between sample data, local activity metadata, and future Enterprise live
ingestion.

| Provenance | Meaning |
| --- | --- |
| `sample_data` | Public-safe deterministic demo data. |
| `local_activity_store` | Derived from Community JSON or SQLite activity persistence. |
| `enterprise_live_ingestion` | Reserved for private Enterprise live ingestion. |

## Schema

The packaged dashboard schema is available at
`src/cavra/schemas/aispm-dashboard.schema.json`.

The packaged Community trace replay schema is available at
`src/cavra/schemas/aispm-trace-replay.schema.json`. A deterministic sample
packet is available at `examples/aispm/community-trace-replay-sample.json`.

The packaged Community approval lineage schema is available at
`src/cavra/schemas/aispm-approval-lineage.schema.json`. A deterministic sample
packet is available at `examples/aispm/community-approval-lineage-sample.json`.
