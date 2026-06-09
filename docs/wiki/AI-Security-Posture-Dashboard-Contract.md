# AI Security Posture Dashboard Contract

CAVRA now exposes the first public-safe AI Security Posture Management
dashboard contract for Community Edition. The current public implementation
includes Phase A contract fields plus Phase B control coverage, near-miss
visibility, and public-safe trace replay packets.

Community Edition provides:

- `GET /aispm/dashboard/contract`
- `GET /aispm/dashboard/sample`
- `GET /aispm/posture`
- `GET /aispm/agents`
- `GET /aispm/findings`
- `GET /aispm/timeline`
- `GET /aispm/control-coverage`
- `GET /aispm/near-misses`
- `GET /aispm/trace-replay/{session_id}`

The public portal now includes an `AI Posture` route that renders the contract
with sample data by default and reads `/aispm/posture` when
`window.CAVRA_API_BASE` is configured. The route shows posture overview, agent
coverage, risk findings, control coverage, near misses, execution timeline, and
the raw public-safe payload.

Community trace replay reconstructs normalized decision steps, evidence
references, risk classifications, and redaction status. It does not expose raw
prompts, model reasoning, raw tool output, private customer context, or
Enterprise replay retention logic.

These endpoints derive posture from local activity metadata or sample data.
They do not expose private prompts, proprietary reasoning traces, Enterprise
policy logic, customer data, license-server state, or SaaS tenant records.

Enterprise remains responsible for live authenticated multi-tenant posture,
prompt/reasoning traces, tool-call graphs, full trace replay, organization
controls, kill switch, runtime overrides, centralized retention, immutable audit
exports, and compliance reporting.

The packaged dashboard schema is `src/cavra/schemas/aispm-dashboard.schema.json`.
The packaged Community trace replay schema is
`src/cavra/schemas/aispm-trace-replay.schema.json`, with a deterministic sample
packet at `examples/aispm/community-trace-replay-sample.json`.
