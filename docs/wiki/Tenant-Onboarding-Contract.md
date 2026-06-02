# Tenant Onboarding Contract

CAVRA Community Edition now exposes a public-safe tenant onboarding contract.
It defines request and response shapes for future Enterprise and SaaS tenant
activation without implementing the private service.

## What It Enables

- Tenant activation request shape.
- Supported deployment model validation.
- Public-safe onboarding requirements.
- Public-safe owner contact metadata.
- Unavailable response messaging for Community users.

## Deployment Models

- `hosted_saas`
- `self_hosted_enterprise`
- `hybrid`

## Private Boundary

Private Enterprise or SaaS services must implement tenant database isolation,
SSO onboarding, license validation, entitlement binding, policy registry
enrollment, audit-store provisioning, billing checks, support ownership,
observability, and operational runbooks.

Public Community code must not contain tenant records, production tenant IDs,
billing secrets, license keys, private policy packs, connector credentials,
provider URLs, webhook secrets, SaaS backend source, or Enterprise
implementation details.

## User Stories

- As a sales engineer, I can produce a public-safe tenant onboarding request
  after a trial package and pilot handoff are ready.
- As a platform owner, I can see the activation requirements before a private
  SaaS or Enterprise tenant is provisioned.
- As a security reviewer, I can confirm the public repository does not expose
  tenant provisioning code or secrets.

## Next Recommendation

Implement the public entitlement status contract.
