# AI Security Posture Dashboard Contract

CAVRA now exposes the first public-safe AI Security Posture Management
dashboard contract for Community Edition. Phase A defines the contract, and the
current Phase B hardening adds Community control coverage, near-miss visibility,
public-safe trace replay packets, public-safe approval lineage, behavior
fingerprints, policy context gaps, pre-action risk forecasts, and
intent-to-action drift, and tool-chain risk graphing without exposing Enterprise live-ingestion logic.

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
- `GET /aispm/behavior-fingerprints` returns public-safe agent behavior
  fingerprints and drift signals from normalized local activity metadata.
- `GET /aispm/policy-context-gaps` returns public-safe policy-invisible risk
  findings when a decision lacks required business context.
- `GET /aispm/pre-action-risk-forecasts` returns public-safe projected blast
  radius, likely impact, and required pre-action controls from local decision
  metadata.
- `GET /aispm/intent-action-drift` returns public-safe declared-intent versus
  observed-action drift from local decision metadata.
- `GET /aispm/tool-chain-graph` returns public-safe agent, tool, redacted
  target, policy, hotspot, and risky edge summaries from local decision
  metadata.

The public portal now includes an `AI Posture` route that renders this contract
as a static-hostable dashboard. When `window.CAVRA_API_BASE` is configured it
loads `/aispm/posture`; otherwise it falls back to deterministic sample data and
labels the view as `sample_data`. The route includes posture overview, agent
coverage, risk findings, control coverage, near-miss queue, execution timeline,
approval lineage, behavior fingerprinting, pre-action risk forecasts, intent-to-action drift, tool-chain risk graph, and the raw public-safe payload. The route also shows
policy context gaps for missing environment, ownership, data, change-window,
criticality, approval-route, or trust-tier metadata.

Community trace replay reconstructs normalized decision steps, evidence
references, risk classifications, and redaction status. It does not expose raw
prompts, model reasoning, raw tool output, private customer context, or
Enterprise replay retention logic.

Community approval lineage reconstructs "who approved what" from local approval
records using approver groups, state, timestamps, decision linkage, and evidence
references. Human actors are reduced to role labels; raw identity-provider
claims, RBAC policy context, private routing rules, and connector payloads
remain Enterprise-only.

Community behavior fingerprinting summarizes agent action profiles, decision
profiles, observed repositories, control surfaces, risk signals, drift status,
and evidence references. It does not expose prompts, reasoning traces, raw tool
output, private customer context, or organization-specific behavior baselines.

Community policy context gap detection identifies when the local decision
record lacks the business metadata needed to make a policy decision fully
explainable. It flags missing fields only; private enrichment from CMDB, data
catalogs, identity providers, cloud inventory, ticketing, and change calendars
remains Enterprise-only.

Community pre-action risk forecasts project blast radius and likely impact from
normalized local decision metadata. They do not use private asset graphs,
dependency graphs, cloud inventory, identity blast-radius context, runtime
state, or prompt-intent context; those remain Enterprise-only.

Community intent-to-action drift compares declared intent metadata with the
observed action type, target summary, control surface, and policy outcome. It
does not infer intent from raw prompts, model reasoning, conversation history,
private ticket context, full tool payloads, or semantic intent models; those
remain Enterprise-only.

Community tool-chain graphing maps agents, safe tool labels, redacted targets,
policy packs, and risk-scored execution edges from local decision metadata. It
does not expose raw tool request bodies, tool results, connector spans,
cross-system call graphs, private network targets, or Enterprise trace
correlation.

The public contract uses existing CAVRA activity metadata. It does not capture
private prompts, proprietary reasoning traces, Enterprise policy logic,
customer data, license-server state, or SaaS tenant records.

## Enterprise Boundary

Enterprise remains responsible for live, authenticated, multi-tenant AISPM:

- prompt and reasoning trace capture;
- private asset-graph and identity-aware pre-action forecasting;
- prompt-derived intent extraction and private workflow correlation;
- raw tool-call graph, cross-system execution traces, and full trace replay;
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

The packaged Community behavior fingerprint schema is available at
`src/cavra/schemas/aispm-behavior-fingerprints.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-behavior-fingerprints-sample.json`.

The packaged Community policy context gap schema is available at
`src/cavra/schemas/aispm-policy-context-gaps.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-policy-context-gaps-sample.json`.

The packaged Community pre-action risk forecast schema is available at
`src/cavra/schemas/aispm-pre-action-risk-forecasts.schema.json`. A
deterministic sample packet is available at
`examples/aispm/community-pre-action-risk-forecasts-sample.json`.

The packaged Community intent-to-action drift schema is available at
`src/cavra/schemas/aispm-intent-action-drift.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-intent-action-drift-sample.json`.

The packaged Community tool-chain graph schema is available at
`src/cavra/schemas/aispm-tool-chain-graph.schema.json`. A deterministic sample
packet is available at
`examples/aispm/community-tool-chain-graph-sample.json`.
