# Release Notes

## v0.1.0 - May 14, 2026

### Initial MVP Release

**CAVRA** is a runtime governance platform for AI coding agents in regulated engineering environments.

#### Features

**Core Governance**
- ✓ Policy-as-code with YAML definitions
- ✓ File access control (read/write blocking)
- ✓ Command pattern matching (allow/block/require_approval)
- ✓ Git action governance
- ✓ Session-based audit trails

**Policy Packs**
- ✓ `cavra-ai-agent-baseline`: Security for any AI agent
- ✓ `cavra-banking-baseline`: Banking/regulated compliance
- ✓ `cavra-terraform-prod`: Infrastructure-as-code safety
- ✓ `cavra-mcp-enterprise`: Tool access control

**Integrations**
- ✓ GitHub PR attestation comments
- ✓ Webhook export for SIEM (Splunk, Datadog, Sentinel)
- ✓ JSON audit artifact generation
- ✓ Markdown evidence export

**CLI**
- ✓ `cavra agent start` — Initialize session
- ✓ `cavra agent exec` — Execute under governance
- ✓ `cavra agent attest` — Generate attestation
- ✓ `cavra policy list` — Show available policies
- ✓ `cavra policy describe` — Policy details

**Quality**
- ✓ Comprehensive test suite (8/8 passing)
- ✓ GitHub Actions CI/CD workflows
- ✓ Type hints throughout codebase
- ✓ BUSL-1.1 enterprise-friendly licensing

#### Documentation

- [Vision](docs/vision.md) — Product positioning and value proposition
- [Architecture](docs/architecture.md) — Technical design and components
- [Threat Model](docs/threat-model.md) — Security threats and controls
- [Policy Authoring](docs/policy-authoring.md) — How to write custom policies
- [Implementation Guide](docs/implementation-guide.md) — Enterprise deployment steps
- [Webhook Integration](docs/webhook-integration.md) — SIEM setup
- [5-Year Roadmap](docs/roadmap.md) — Product vision and phases

#### Installation

```bash
pip install cavra
```

#### Quick Start

```bash
# Start a governed session
cavra agent start \
  --tool claude-code \
  --repo . \
  --policy-pack cavra-banking-baseline

# Execute command with governance
cavra agent exec "terraform plan"

# List available policies
cavra policy list

# Generate PR attestation
cavra agent attest <session-id> --format markdown
```

#### Known Limitations

- Phase 2 features not yet implemented (MCP server governance)
- Enterprise integrations (Jira, ServiceNow) are skeleton only
- Semantic policy engine (Phase 4) not implemented
- Web UI for policy management coming in Phase 2

#### Roadmap

See [docs/roadmap.md](docs/roadmap.md) for 5-year product vision:
- **Phase 1**: MVP & market entry (current)
- **Phase 2**: MCP governance & tool control (Q4 2026)
- **Phase 3**: Enterprise integrations (Q1 2027)
- **Phase 4**: Semantic policy & intelligence (Q2-Q3 2027)
- **Phase 5**: AI-assisted engineering control plane (2028+)

#### Support

- 📖 Documentation: https://github.com/Huzefaaa2/cavra
- 🐛 Issue tracker: https://github.com/Huzefaaa2/cavra/issues
- 💬 Discussions: https://github.com/Huzefaaa2/cavra/discussions
- 📧 Contact: huzefa@example.com

#### License

BUSL-1.1 (Business Source License 1.1)
- Unrestricted use for internal purposes
- Change deadline: May 14, 2030
- After change date: Apache 2.0
- Commercial license available

---

## Planned future releases

### v0.2.0 (Phase 1 completion)
- MCP server allowlisting
- Terraform-specific governance enhancements
- Claude Code integration (proof-of-concept)
- GitHub Copilot integration
- Splunk SIEM connector
- Organization policy pack templates

### v0.3.0 (Phase 2 preview)
- MCP capability control
- Tool risk scoring
- Advanced policy inheritance
- Policy signing and verification

### v1.0.0 (Phase 2 completion)
- MCP server marketplace integration
- Enterprise policy templates
- Advanced approval workflows
- Performance optimizations

---

## Credits

**Author**: Huzefa Husain
**Inspired by**: CAVRA V3 vision for AI agent governance in regulated environments

**Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
