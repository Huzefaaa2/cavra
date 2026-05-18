# CAVRA Roadmap

## Vision

Build the industry-standard runtime governance platform for AI coding agents in regulated engineering environments.

## Phases

### Phase 0: Foundation (Completed ✓)

**Status**: Complete  
**Timeline**: May 2026

- ✓ Core policy registry and runtime guard
- ✓ AI session manager with audit recording
- ✓ File access and command interception
- ✓ GitHub PR attestation export
- ✓ Baseline policy packs
- ✓ Unit and integration tests
- ✓ CLI with `agent start`, `agent exec`, `agent attest`
- ✓ Documentation (vision, architecture, threat model)

---

### Phase 1: MVP & Market Entry (Next)

**Timeline**: Q3 2026

**Features**:
- [ ] Terraform-specific runtime controls
- [ ] Claude Code hooks integration (proof-of-concept)
- [ ] GitHub Copilot coding agent integration
- [ ] Splunk SIEM webhook export
- [ ] Jira issue linking
- [ ] Organization policy pack templates
- [ ] Development guide and examples

**Deliverables**:
- PyPI package release (`cavra`)
- Homebrew formula
- Docker image
- Quick-start documentation
- 3 enterprise reference implementations

**Success metrics**:
- 100+ GitHub stars
- 5+ enterprise pilot customers
- <5 minutes to first governance check

---

### Phase 2: MCP Governance & Tool Control

**Timeline**: Q4 2026

**Features**:
- [ ] MCP server allowlisting
- [ ] MCP capability control (read-only, execute, network)
- [ ] Tool risk scoring and categorization
- [ ] MCP session recording
- [ ] MCP-specific policy packs

**Rationale**:
MCP (Model Context Protocol) is expanding AI agent capabilities. Governance must cover tool access, not just direct commands.

**Success metrics**:
- Support for 10+ common MCP servers
- Tool allowlist adoption in 80% of customers

---

### Phase 3: Enterprise Integrations

**Timeline**: Q1 2027

**Features**:
- [ ] Datadog integration
- [ ] Azure Sentinel integration
- [ ] AWS CloudTrail integration
- [ ] ServiceNow change management sync
- [x] Okta / Azure AD SSO reference bundles
- [ ] OAuth2 API authentication
- [ ] Approval workflow orchestration

**Why now**:
Phase 2 validates the core model. Phase 3 deepens enterprise adoption through native integrations.

**Success metrics**:
- 50+ enterprise deployments
- $1M+ annual recurring revenue

---

### Phase 4: Semantic Policy & Intelligence

**Timeline**: Q2-Q3 2027

**Features**:
- [ ] Semantic diff analysis
  - Detect when agent modifies IAM, encryption, or network rules
  - Intent-based policy evaluation
- [ ] Risk scoring engine
  - Context-aware risk assessment
  - Anomaly detection on agent behavior
- [ ] Policy recommendations
  - LLM-powered policy suggestion
  - Compliance gap analysis
- [ ] Advanced approval workflows
  - Dynamic routing based on risk
  - Required reviewer selection

**Example**:
```
Instead of: "block terraform apply*"

Evaluate: "Is the agent changing IAM permissions? Is encryption enabled? Is this change review-worthy?"

Decision: "This Terraform plan creates public S3 bucket → BLOCK + notify CISO"
```

**Success metrics**:
- 90%+ accuracy on risk assessment
- 50% fewer false positives
- Policy authoring time reduced by 50%

---

### Phase 5: AI-Assisted Engineering Control Plane (2028+)

**Timeline**: 2028 and beyond

**Vision**: CAVRA becomes a control plane for all AI-assisted engineering, not just governance.

**Features**:
- [ ] Agent orchestration for complex tasks
- [ ] Multi-agent coordination
- [ ] Approval workflow automation
- [ ] Cost governance and spending limits
- [ ] Capability-based access control (CBAC) for agents
- [ ] Agent marketplace with governed tool access

**Strategic focus**:
Position CAVRA as the runtime foundation for safe, autonomous AI engineering in enterprises.

---

## Key inflection points

| Phase | Inflection point | Success criteria |
| --- | --- | --- |
| 1 | MVP market fit | Customers adopt, deploy policy packs |
| 2 | MCP becomes standard | Agents use tools, governance becomes critical |
| 3 | Enterprise baseline | 50+ deployments, revenue inflection |
| 4 | Intelligence advantage | Better than competitors at risk assessment |
| 5 | Industry standard | De facto control plane for AI engineering |

---

## Technical debt & maintenance

Ongoing (every phase):
- [ ] Security audit and penetration testing
- [ ] Performance optimization
- [ ] Compatibility with new agent frameworks
- [ ] Policy pack updates for new threats
- [ ] Documentation and examples
- [ ] Community feedback and contributions

---

## Competitive positioning

| Competitor | Advantage | CAVRA differentiation |
| --- | --- | --- |
| GitHub Code Security | GitHub native | Enterprise control + multi-tool support |
| Snyk | Code scanning | Runtime governance before commit |
| HashiCorp Sentinel | Policy-as-code | AI-agent specific, easier authoring |
| Custom solutions | Purpose-built | Reusable, market-tested policies |

---

## Investment asks

**Phase 1**: $250K (seed round)
- Engineering (2 FTE)
- Product management
- GTM and BD

**Phase 2-3**: $2M (Series A)
- Engineering (6 FTE)
- Sales and marketing
- Customer success

**Phase 4+**: $10M+ (Series B+)
- Semantic engine and ML
- Enterprise sales force
- International expansion

---

## Open questions

1. Will enterprises adopt AI agents in regulated environments?
   - **Bet**: Yes, with governance guardrails
   
2. Can policy-as-code work for non-engineers?
   - **Bet**: Yes, with templates and UI
   
3. Can runtime governance compete with post-hoc scanning?
   - **Bet**: Yes, prevents damage before Git
   
4. What's the serviceable addressable market?
   - **Estimate**: $5B+ in DevSecOps and AI governance

---

## Success = ?

We win if:
- Enterprises feel confident deploying AI coding agents
- Developers love the DX
- Competitors copy the model
- We become the standard in regulated AI engineering
