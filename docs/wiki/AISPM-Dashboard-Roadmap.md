# AISPM Dashboard Roadmap

CAVRA's public Evidence Console demonstrates the control model and supports
local or sample evidence views. The product roadmap now separates that public
surface from the future Enterprise AI Security Posture Management dashboard.

Enterprise should provide the live CSO/CISO operating surface:

- live agent activity across prompts, responses, reasoning traces, tool calls,
  file actions, shell commands, Git operations, MCP calls, CI runner activity,
  and cloud/IaC actions;
- policy decision streams for allow, warn, block, require approval, audit-only,
  and allow with attestation outcomes;
- risk and violation queues grouped by repository, agent, severity, control
  family, policy pack, data class, and environment;
- execution timelines and full trace replay for each governed session;
- approval lineage showing who approved what, when, why, under which policy,
  and with which evidence bundle;
- control coverage heatmaps for repositories, agent tools, CI gates, MCP
  servers, runtime modes, and enforcement backends;
- evidence confidence drilldowns for signed, activity-reference, sample,
  metadata-only, and missing evidence;
- evidence freshness and retention SLO panels for stale evidence, missing
  timestamps, retention gaps, and archive-readiness boundaries;
- executive risk narratives for CSO/CISO users that summarize posture, top
  risks, evidence gaps, and recommended actions;
- replay-to-policy authoring that converts governed traces into reviewed
  candidate controls, policy tests, and approval-bound policy changes;
- CSO controls for kill switch, quarantine, policy toggle, runtime override,
  rollback, and post-event review;
- compliance and audit views for SOC 2, ISO 27001, NIST SSDF, EU AI Act, PCI
  DSS, SOX, HIPAA, and internal AI governance controls.

Community should keep a public-safe dashboard demo and local activity view,
including observed control coverage, near-miss queues, trace replay packets
derived from local decisions, approval lineage from local approval records, and
behavior fingerprints, policy context gaps, pre-action risk forecasts,
evidence confidence drilldowns, evidence freshness SLO panels, and
deterministic executive risk narratives, plus read-only replay-to-policy draft
and test fixture previews, from normalized local activity
metadata, plus
intent-to-action drift and tool-chain risk graphing from declared intent, safe
tool labels, redacted targets, and observed action metadata.
Enterprise should own authenticated multi-tenant ingestion, streaming updates,
centralized retention, private policy context, organization controls, raw
prompt/reasoning replay, private behavior baselines, private context
enrichment, private asset/dependency/identity forecast enrichment,
prompt-derived semantic intent extraction, private workflow correlation, raw tool payload graphing, immutable evidence validation, cross-system execution traces,
private IdP/RBAC context, AI-assisted board summaries, private trend history,
tenant benchmarks, service criticality, customer-impact enrichment, private
prompt/reasoning/tool-payload policy authoring, tenant-history policy
simulation, approval-bound write-back automation, and commercial compliance
exports.

After all AISPM phases reach production-ready status, the GitHub Wiki must
include a public-safe trial-user lab notebook and product textbook. It should
walk users through CAVRA end to end with screenshots, diagrams, flow charts,
expected outputs, troubleshooting notes, and role-specific labs for developers,
platform teams, auditors, security engineers, and CSO/CISO users. The notebook
must not expose Enterprise source code, license secrets, private keys, customer
data, or private policy-pack implementation details.

The detailed implementation plan is maintained in
`docs/ai-security-posture-dashboard-roadmap.md`.
