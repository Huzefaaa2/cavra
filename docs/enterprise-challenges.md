# Enterprise Challenges CAVRA Solves

## Secret Exposure

Challenge: AI agents can read sensitive files and copy secrets into model context or logs.

CAVRA control: File Guard blocks `.env`, key files, kubeconfig, Terraform state, tfvars, and regulated data paths before read.

## Unsafe Infrastructure Changes

Challenge: Agents can run `terraform apply`, `kubectl delete`, or cloud IAM commands directly.

CAVRA control: Command Guard allows planning and read-only commands while blocking or routing production-impacting commands for approval.

## Direct Git Push

Challenge: Agents can bypass review with direct protected-branch pushes or force pushes.

CAVRA control: Git Guard blocks direct pushes to protected branches and generates PR attestation.

## MCP Tool Sprawl

Challenge: MCP servers can expose filesystem, shell, network, database, and SaaS capabilities without enterprise approval.

CAVRA control: MCP Guard blocks unknown servers, classifies capabilities, and creates the foundation for an MCP Trust Registry.

## Audit Gaps

Challenge: Existing controls often record outcomes after changes happen, not decisions before actions.

CAVRA control: Evidence Hub records every attempted action, policy decision, rule, reason, timestamp, and correlation ID.

## Identity Ambiguity

Challenge: Enterprises cannot consistently answer which agent acted, on whose behalf, and with what scope.

CAVRA control: Agent Registry roadmap tracks agent ID, vendor, version, capabilities, owner, risk tier, active sessions, and evidence history.

## Approval Bypass

Challenge: AI agents can perform high-risk work outside change management.

CAVRA control: Approval Router roadmap maps risky actions to Platform Security, IAM, AppSec, CAB, AI Governance, Data Protection, PCI, HIPAA, and repository owner groups.

## Regulated SDLC Evidence

Challenge: Banks, healthcare, public sector, and SaaS companies need evidence, not promises.

CAVRA control: Compliance packs, PR attestations, evidence bundles, SIEM exports, and immutable evidence storage roadmap create audit-ready artifacts.
