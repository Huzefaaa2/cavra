# CAVRA GUI UAT And CLI Parity Assessment

Date: 2026-07-15

## Scope

This assessment reviews whether the CAVRA sandbox/operator GUI exposes the
core user-facing capabilities that are available through the CAVRA CLI and API.
The goal is not to convert every release-engineering validator into a GUI
button. The goal is to ensure normal operators can install, configure, govern,
review, report, and validate CAVRA from the GUI without falling back to the CLI
for primary workflows.

## Result

| Area | CLI/API capability | GUI status | UAT finding |
| --- | --- | --- | --- |
| Version and health | `cavra version`, `/health`, `/version` | Covered | Dashboard and Settings show API connection, version, and diagnostics. |
| First-run setup | `cavra setup status/init/wizard/demo-env/validate/complete/smtp` | Covered | Setup page can create defaults, generate demo workspace, save SMTP metadata, validate, seed AISPM, and mark setup complete. |
| Policy catalog | `cavra setup policy-actions`, `/policy-action-catalog` | Covered | Policy page lists, filters, and summarizes active governed actions. |
| Policy simulation | `cavra evaluate`, `cavra policy test/explain`, `/policy-action-catalog/test` | Covered | Decision simulator evaluates risky command/file/git/MCP actions from the GUI. |
| Policy action change planning | `cavra setup policy-action-plan`, `/policy-action-catalog` POST/PATCH/DELETE | Fixed in this pass | GUI now has add/update/delete planning for policy actions. It returns a reviewable draft and does not silently write policy files. |
| Policy pack upload | `/policy-packs/upload`, `/policy-packs/draft`, `/policy-packs/publish-plan`, `/policy-packs/publish-request` | Fixed in this pass | GUI now accepts YAML/JSON policy packs, including Enterprise packs, validates draft, creates publish plan, and can request approval. |
| Policy pack publish | `/policy-packs/publish` | Partial by design | Publish remains approval-bound. GUI can request approval; final publish should require an approved request and signer context. |
| Approvals | `cavra approval create/list/approve/deny/expire/break-glass/deliver` | Covered | Approval queue supports list, filtering, selection, approve, deny, expire, break-glass, and deliver. |
| Agent registry | `cavra registry agent-register/agent-list/profiles` | Covered for local operation | GUI can seed sample agents, list/filter agents, inspect records, and load profiles. Full custom registration can be extended later. |
| MCP registry | `cavra registry mcp-register/mcp-list/mcp-check/classifications` | Covered for local operation | GUI can seed MCP records, list/filter trust registry, inspect records, run trust check, and load classifications. |
| Evidence | `cavra evidence bundle/verify/search/index/export-siem/...` | Mostly covered | GUI lists/searches evidence, inspects metadata, copies/downloads JSON, and presents AISPM evidence refs. Full trust-root/keypair generation remains CLI/admin. |
| AISPM | `cavra aispm validate-*`, AISPM API endpoints | Covered for operator review | GUI shows posture, findings, agents, timeline, report center, board pack, and guided trial links. Validator commands remain CI/admin. |
| Integrations | `cavra integration deliver`, connector API | Covered for readiness | GUI seeds integration inventory, filters health, inspects provider boundary, and tests delivery boundary. |
| Reports | Browser/API report surfaces | Covered for Community | GUI generates JSON/Markdown/CSV previews and downloads. Provider-backed scheduled delivery remains configured deployment/Managed scope. |
| Operations stores | `cavra ops stores/backup/restore/retention-plan` | Partial | Settings shows store modes and diagnostics. Backup/restore/retention execution remains CLI/operator-admin. |
| Deployment context | API/runtime environment | Fixed in this pass | Settings now reports runtime, platform, orchestrator, environment, install target, container/Kubernetes detection, namespace, and host/pod. |
| Release/runtime validators | Many `cavra release` and `cavra runtime` commands | Not GUI-primary | These are CI/release-governance commands. GUI includes relevant readiness/report surfaces but should not expose every internal validator as a daily operator control. |

## Browser UAT

Local stack:

```bash
docker compose up -d --build
```

Test target:

```text
http://127.0.0.1:5173
http://127.0.0.1:8000
```

Observed GUI routes:

- Dashboard
- First-Run Setup
- AISPM
- Architecture
- Policy Engine
- Agents & MCP Trust
- Approvals
- Evidence
- Use Cases
- Operator Paths
- Trial Access
- Integrations
- Reports
- Settings
- Compliance
- Roadmap
- Documentation

Browser-level UAT found no failed API responses and no console errors after the
Docker CORS/local config fix.

## Remaining Recommendations

1. Add final approval-aware publish action in the GUI after an approval request is approved.
2. Add custom agent and MCP registration forms, beyond sample seeding.
3. Add guarded backup/restore/retention-plan admin forms for self-hosted operators.
4. Add GUI affordances for policy signature/key management only when a secure key provider is configured.
5. Keep release and runtime closeout validators in CLI/CI unless a specific operator dashboard is required.
