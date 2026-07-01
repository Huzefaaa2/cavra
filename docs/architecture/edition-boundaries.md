# Product Boundaries

CAVRA uses a Community-first model. This public repository contains CAVRA
Community and public product documentation. It may describe CAVRA Managed,
Enterprise Subscription, and Trial access, but it must not contain private
managed-service source code, secrets, signing material, customer records, or
commercial package internals.

## Public CAVRA Community

Belongs in this repository:

- Runtime policy evaluation.
- Local CLI, API, and MCP integration.
- Approvals, evidence bundles, attestations, and public schemas.
- AISPM, report center contracts, dashboards, and public-safe samples.
- CI/CD enforcement.
- Connector SDK and reference connectors.
- Public policy packs and examples.
- Public documentation, diagrams, and deployment guides.

Community must run without a license key for local or self-hosted use.

## Provider-Configured Community

These capabilities are included but require operator configuration:

- SSO/RBAC hooks.
- Audit export.
- Report delivery.
- Policy registry.
- Object storage and database.
- Live connector credentials.
- Monitoring and retention.

The correct status for missing backing services is `requires_configuration`.

## CAVRA Managed

Belongs in private managed-service repositories and infrastructure:

- Hosted tenant onboarding.
- Managed policy registry and dashboards.
- Managed report delivery and audit storage.
- Billing, uptime, support handoff, and customer-success operations.
- Internal runbooks, service credentials, and customer records.

## Enterprise Subscription

Belongs in commercial packages or private customer operations:

- Certified connectors.
- Commercial policy packs and compliance packs.
- SLA and support workflows.
- Custom integrations and implementation help.
- Procurement, security review, and customer-specific deployment material.

## CAVRA Trial

Trial is an approved evaluator access path. It may include hosted access,
time-limited entitlement material, private package access where applicable,
guided labs, expiry, revocation, audit evidence, and closeout. Trial is not a
separate product edition.

## Never Public

Do not commit:

- Production credentials or private keys.
- License signing material or package tokens.
- CAVRA Managed secrets.
- Customer data, customer templates, or customer evidence.
- Support records, billing records, or internal-only operational runbooks.
- Private commercial roadmap details.
