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
- CSO controls for kill switch, quarantine, policy toggle, runtime override,
  rollback, and post-event review;
- compliance and audit views for SOC 2, ISO 27001, NIST SSDF, EU AI Act, PCI
  DSS, SOX, HIPAA, and internal AI governance controls.

Community should keep a public-safe dashboard demo and local activity view,
including observed control coverage, near-miss queues, trace replay packets
derived from local decisions, approval lineage from local approval records, and
behavior fingerprints plus policy context gaps from normalized local activity
metadata.
Enterprise should own authenticated multi-tenant ingestion, streaming updates,
centralized retention, private policy context, organization controls, raw
prompt/reasoning replay, private behavior baselines, private context
enrichment, private IdP/RBAC context, and commercial compliance exports.

The detailed implementation plan is maintained in
`docs/ai-security-posture-dashboard-roadmap.md`.
