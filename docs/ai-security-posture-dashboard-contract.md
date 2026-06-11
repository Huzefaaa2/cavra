# AI Security Posture Dashboard Contract

CAVRA now exposes the first public-safe AI Security Posture Management
dashboard contract for Community Edition. Phase A defines the contract, and the
current Phase B hardening adds Community control coverage, near-miss visibility,
public-safe trace replay packets, public-safe approval lineage, behavior
fingerprints, policy context gaps, pre-action risk forecasts, and
intent-to-action drift, tool-chain risk graphing, agent blast-radius mapping,
control coverage heatmap views, evidence confidence drilldowns, evidence
freshness SLO panels, and executive risk narratives without exposing
Enterprise live-ingestion logic.

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
- `GET /aispm/control-coverage-heatmap` returns a public-safe heatmap by agent,
  repository, and control surface from local activity metadata.
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
- `GET /aispm/agent-blast-radius` returns public-safe per-agent reach across
  repositories, redacted target classes, tools, policy packs, control surfaces,
  approval paths, and evidence references.
- `GET /aispm/evidence-confidence` returns public-safe evidence confidence
  drilldowns for decision/session evidence references, including signed,
  activity-reference, sample, metadata-only, and missing evidence classes.
- `GET /aispm/evidence-freshness` returns public-safe evidence freshness and
  retention SLO rows for local decision/session timestamps and evidence
  reference patterns.
- `GET /aispm/executive-risk-narrative` returns a deterministic public-safe
  CSO/CISO narrative from local posture metrics, top risks, evidence SLO
  status, and recommended actions.
- `GET /aispm/replay-to-policy-draft` returns a public-safe read-only policy
  draft generated from normalized local replay decisions.
- `GET /aispm/replay-to-policy-tests` returns public-safe read-only policy test
  fixtures generated from replay-derived draft controls.

The public portal now includes an `AI Posture` route that renders this contract
as a static-hostable dashboard. When `window.CAVRA_API_BASE` is configured it
loads `/aispm/posture`; otherwise it falls back to deterministic sample data and
labels the view as `sample_data`. The route includes posture overview, agent
coverage, risk findings, control coverage, near-miss queue, execution timeline,
approval lineage, behavior fingerprinting, pre-action risk forecasts,
intent-to-action drift, tool-chain risk graph, agent blast-radius map, and the
raw public-safe payload. The route also shows
policy context gaps for missing environment, ownership, data, change-window,
criticality, approval-route, or trust-tier metadata.
The route includes a control coverage heatmap so operators can compare
enforced, approval-gated, warning-only, observed, and unobserved control
surfaces per agent/repository path.
The route also includes an agent blast-radius map so CSO/CISO users can see
which agents have observed sensitive-data reach, production-infrastructure
reach, multi-repository scope, approval gaps, and required compensating
controls.
The route also includes an evidence confidence drilldown so operators can see
which policy decisions are backed by signed evidence, activity references,
sample evidence, metadata only, or missing evidence before relying on a report.
The route also includes an evidence freshness and retention SLO panel so
operators can see stale evidence, missing timestamps, retention-reference gaps,
and Enterprise archive-readiness boundaries.
The route also includes an executive risk narrative panel so CSO/CISO users can
read a Community-safe leadership summary of posture, top risks, evidence gaps,
and recommended actions.
The route also includes a replay-to-policy draft panel so platform and
security operators can see candidate controls derived from observed replay
decisions before committing reviewed policy changes.
The same panel also shows replay-to-policy test fixture exports so reviewers
can see the expected policy assertions before adding reviewed tests to CI.
The portal also offers a replay-to-policy review packet export that combines
the candidate policy draft, review-only test fixture, and reviewer checklist
into one public-safe JSON packet for PR attachment or auditor review.
The same view includes PR attachment guidance with exact packet, draft, and
fixture attachment paths plus copyable reviewer approval language.

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

Community agent blast-radius mapping rolls up normalized local activity into
per-agent reach cards. It shows repositories, target classes, safe tool labels,
policy packs, control surfaces, approval paths, blocked actions, approval-gated
actions, top risks, recommended controls, and evidence references. It does not
expose private asset graphs, identity permission graphs, cloud account
inventories, dependency graphs, secret names, customer topology, or private
criticality enrichment.

Community control coverage heatmaps pivot normalized local decisions by agent,
repository, and control surface. They show cell status, coverage score, action
counts, evidence confidence, and recommended action. They do not expose private
repository owner graphs, identity-provider claims, repository permission
matrices, environment criticality, CMDB service mappings, or live organization
baselines.

Community evidence confidence drilldowns classify local decision and session
evidence references as signed evidence, activity evidence references, sample
evidence, metadata-only records, or missing evidence. They do not inspect raw
evidence payloads, validate private artifact contents, resolve signature trust
chains, read external ticket payloads, expose customer data, or access tenant
evidence stores.

Community evidence freshness SLOs classify local decision and session
timestamps as fresh, review-soon, stale, or missing. They also classify public
evidence-reference patterns as retained references, sample references,
evidence-only references, or metadata-only records. They do not probe immutable
archives, object-lock settings, KMS key health, lifecycle policies, external
archive metadata, or auditor export manifests.

Community executive risk narratives generate deterministic, public-safe
leadership summaries from the local posture score, top-risk queue, blocked and
approval-gated decisions, and evidence freshness metrics. AI-assisted board
summaries, private tenant trends, business owner and service criticality
enrichment, customer impact analysis, scheduled executive brief delivery, and
GRC/incident packet export remain Enterprise-only.

Community replay-to-policy draft authoring converts normalized block,
require-approval, warning, high, and critical decisions into a read-only policy
pack preview. It can suggest public-safe filesystem, command, Git, MCP,
approval, evidence, and compliance controls from local metadata only. It does
not write to `policies/`, publish policy packs, inspect raw prompts, inspect
model reasoning, read raw tool payloads, enrich from tickets or asset graphs,
simulate tenant history, or automate production write-back.

Community replay-to-policy test fixture export converts the same candidate
controls into review-only JSON cases. Each case includes public-safe input
metadata, expected decision metadata, evidence references, and validation
notes. It does not run private simulation, generate tests from prompts or raw
tool payloads, open pull requests, or write CI files.

Community replay-to-policy review packet export combines the policy draft,
test fixture, checklist status, provenance, and redaction boundaries into a
single review-only JSON packet. It is intended for PR attachment and auditor
review only; it is not an automated approval, policy write-back, CI write-back,
or production rollout action.

Community replay-to-policy review packet validation is available through
`cavra aispm validate-review-packet <packet.json>` and
`POST /aispm/replay-to-policy-review-packet/validate`. It verifies the
packaged schema, fixture case counts, review checklist totals, required human
approval, and review-only export metadata without approving or mutating any
policy files. A reusable GitHub Actions gate is available at
`examples/github-actions/cavra-aispm-review-packet-validation.yml` for teams
that want replay-derived policy and fixture changes to require a valid review
packet before merge.

Community PR attachment guidance tells reviewers where to attach the review
packet, where to commit the reviewed policy draft and fixture, and what
approval wording to use. It remains advisory guidance only and does not submit,
approve, or mutate pull requests.

The public contract uses existing CAVRA activity metadata. It does not capture
private prompts, proprietary reasoning traces, Enterprise policy logic,
customer data, license-server state, or SaaS tenant records.

## Enterprise Boundary

Enterprise remains responsible for live, authenticated, multi-tenant AISPM:

- prompt and reasoning trace capture;
- private asset-graph and identity-aware pre-action forecasting;
- prompt-derived intent extraction and private workflow correlation;
- raw tool-call graph, cross-system execution traces, and full trace replay;
- private asset, identity, dependency, and customer-topology blast-radius
  enrichment;
- organization-wide control coverage heatmaps with private owner, identity,
  permission, and environment enrichment;
- immutable evidence store validation, signature trust-chain verification, and
  external evidence correlation;
- object-lock, KMS, retention lifecycle, archive restore, and auditor export
  validation;
- AI-assisted executive narratives, private trend history, tenant benchmarks,
  service criticality, customer impact, scheduled brief delivery, and
  GRC/incident packet exports;
- AI-assisted replay-to-policy authoring from prompts, reasoning traces, raw
  tool payloads, tickets, asset graphs, approval policy, tenant simulation, and
  approval-bound write-back automation;
- Enterprise replay-to-policy test generation with tenant-history regression,
  private context enrichment, and approved CI write-back;
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

The packaged Community agent blast-radius schema is available at
`src/cavra/schemas/aispm-agent-blast-radius.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-agent-blast-radius-sample.json`.

The packaged Community control coverage heatmap schema is available at
`src/cavra/schemas/aispm-control-coverage-heatmap.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-control-coverage-heatmap-sample.json`.

The packaged Community evidence confidence schema is available at
`src/cavra/schemas/aispm-evidence-confidence.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-evidence-confidence-sample.json`.

The packaged Community evidence freshness schema is available at
`src/cavra/schemas/aispm-evidence-freshness.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-evidence-freshness-sample.json`.

The packaged Community executive risk narrative schema is available at
`src/cavra/schemas/aispm-executive-risk-narrative.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-executive-risk-narrative-sample.json`.

The packaged Community replay-to-policy draft schema is available at
`src/cavra/schemas/aispm-replay-to-policy-draft.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-replay-to-policy-draft-sample.json`.

The packaged Community replay-to-policy test fixture schema is available at
`src/cavra/schemas/aispm-replay-to-policy-tests.schema.json`. A deterministic
sample packet is available at
`examples/aispm/community-replay-to-policy-tests-sample.json`.

The packaged Community replay-to-policy review packet schema is available at
`src/cavra/schemas/aispm-replay-to-policy-review-packet.schema.json`. A
deterministic sample packet is available at
`examples/aispm/community-replay-to-policy-review-packet-sample.json`.
