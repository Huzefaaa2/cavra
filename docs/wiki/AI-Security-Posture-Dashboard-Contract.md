# AI Security Posture Dashboard Contract

CAVRA now exposes the first public-safe AI Security Posture Management
dashboard contract for Community Edition. The current public implementation
includes Phase A contract fields plus Phase B control coverage, near-miss
visibility, public-safe trace replay packets, public-safe approval lineage,
public-safe behavior fingerprints, public-safe policy context gaps, and
public-safe pre-action risk forecasts, public-safe intent-to-action drift, and
public-safe tool-chain risk graphing, public-safe agent blast-radius mapping,
and public-safe control coverage heatmap views.

Community Edition provides:

- `GET /aispm/dashboard/contract`
- `GET /aispm/dashboard/sample`
- `GET /aispm/posture`
- `GET /aispm/agents`
- `GET /aispm/findings`
- `GET /aispm/timeline`
- `GET /aispm/control-coverage`
- `GET /aispm/control-coverage-heatmap`
- `GET /aispm/near-misses`
- `GET /aispm/trace-replay/{session_id}`
- `GET /aispm/approval-lineage`
- `GET /aispm/behavior-fingerprints`
- `GET /aispm/policy-context-gaps`
- `GET /aispm/pre-action-risk-forecasts`
- `GET /aispm/intent-action-drift`
- `GET /aispm/tool-chain-graph`
- `GET /aispm/agent-blast-radius`

The public portal now includes an `AI Posture` route that renders the contract
with sample data by default and reads `/aispm/posture` when
`window.CAVRA_API_BASE` is configured. The route shows posture overview, agent
coverage, risk findings, control coverage, near misses, execution timeline, and
approval lineage, behavior fingerprinting, pre-action risk forecasts, and the
intent-to-action drift queue, tool-chain risk graph, agent blast-radius map, and
the raw public-safe payload. It also shows
policy context gaps for missing
environment, ownership, data, change-window, criticality, approval-route, or
trust-tier metadata.
It also includes an agent blast-radius map for observed repository, target,
tool, policy, approval, and control-surface reach per agent.
It includes a control coverage heatmap for enforced, approval-gated,
warning-only, observed, and unobserved control surfaces per agent/repository
path.

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
and evidence references. Raw prompts, reasoning traces, tool output, private
customer context, and organization-specific behavior baselines remain
Enterprise-only.

Community policy context gap detection identifies when local decision metadata
is missing business context required for explainable governance. Private
enrichment from CMDB, data catalogs, identity providers, cloud inventory,
ticketing, and change calendars remains Enterprise-only.

Community pre-action risk forecasts project blast radius and likely impact from
normalized local decision metadata. Private asset graphs, dependency graphs,
identity blast radius, cloud inventory, runtime state, and prompt-intent context
remain Enterprise-only.

Community intent-to-action drift compares declared intent metadata with
observed action type, target summary, control surface, and policy outcome.
Raw prompt intent extraction, reasoning analysis, conversation history, private
ticket context, full tool payloads, and semantic intent models remain
Enterprise-only.

Community tool-chain graphing maps agents, safe tool labels, redacted targets, policy packs, hotspots, and risk-scored execution edges from local decision metadata. Raw tool requests, tool results, connector spans, cross-system call graphs, private network targets, and Enterprise trace correlation remain Enterprise-only.

Community agent blast-radius mapping rolls normalized local activity into
per-agent reach cards. It shows repositories, target classes, safe tool labels,
policy packs, control surfaces, approval paths, top risks, recommended
controls, and evidence references. Private asset graphs, identity permission
graphs, cloud inventory, dependency graphs, secret names, and customer topology
remain Enterprise-only.

Community control coverage heatmaps pivot normalized local decisions by agent,
repository, and control surface. They show cell status, coverage score, action
counts, evidence confidence, and recommended action. Private repository owner
graphs, identity-provider claims, repository permission matrices, environment
criticality, CMDB service mapping, and live organization baselines remain
Enterprise-only.

These endpoints derive posture from local activity metadata or sample data.
They do not expose private prompts, proprietary reasoning traces, Enterprise
policy logic, customer data, license-server state, or SaaS tenant records.

Enterprise remains responsible for live authenticated multi-tenant posture,
prompt/reasoning traces, private asset-graph forecasting, prompt-derived
intent extraction, private workflow correlation, raw tool-call graphs, cross-system execution traces, full trace
replay, private blast-radius enrichment, organization-wide heatmaps,
organization controls, kill switch, runtime overrides, centralized
retention, immutable audit exports, and compliance reporting.

The packaged dashboard schema is `src/cavra/schemas/aispm-dashboard.schema.json`.
The packaged Community trace replay schema is
`src/cavra/schemas/aispm-trace-replay.schema.json`, with a deterministic sample
packet at `examples/aispm/community-trace-replay-sample.json`.
The packaged Community approval lineage schema is
`src/cavra/schemas/aispm-approval-lineage.schema.json`, with a deterministic
sample packet at `examples/aispm/community-approval-lineage-sample.json`.
The packaged Community behavior fingerprint schema is
`src/cavra/schemas/aispm-behavior-fingerprints.schema.json`, with a
deterministic sample packet at
`examples/aispm/community-behavior-fingerprints-sample.json`.
The packaged Community policy context gap schema is
`src/cavra/schemas/aispm-policy-context-gaps.schema.json`, with a deterministic
sample packet at `examples/aispm/community-policy-context-gaps-sample.json`.
The packaged Community pre-action risk forecast schema is
`src/cavra/schemas/aispm-pre-action-risk-forecasts.schema.json`, with a
deterministic sample packet at
`examples/aispm/community-pre-action-risk-forecasts-sample.json`.
The packaged Community intent-to-action drift schema is
`src/cavra/schemas/aispm-intent-action-drift.schema.json`, with a
deterministic sample packet at
`examples/aispm/community-intent-action-drift-sample.json`.
The packaged Community tool-chain graph schema is
`src/cavra/schemas/aispm-tool-chain-graph.schema.json`, with a deterministic
sample packet at `examples/aispm/community-tool-chain-graph-sample.json`.
The packaged Community agent blast-radius schema is
`src/cavra/schemas/aispm-agent-blast-radius.schema.json`, with a deterministic
sample packet at `examples/aispm/community-agent-blast-radius-sample.json`.
The packaged Community control coverage heatmap schema is
`src/cavra/schemas/aispm-control-coverage-heatmap.schema.json`, with a
deterministic sample packet at
`examples/aispm/community-control-coverage-heatmap-sample.json`.
