# Tenant Onboarding Contract

CAVRA Community Edition exposes a public-safe tenant onboarding contract for
future Enterprise and SaaS activation workflows. The contract defines request
and response shapes only. It does not implement the SaaS backend, tenant
database, identity provisioning, license service, billing integration, policy
registry, audit store, or support workflow automation.

## Purpose

The tenant onboarding contract lets public Community clients and private
Enterprise packages use a stable vocabulary for moving a customer from trial or
pilot approval into governed tenant activation.

The public request captures:

- tenant identifier;
- organization name;
- requested deployment model;
- region preference;
- onboarding requirements;
- public-safe owner contacts.

## Request Shape

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "tenant_onboarding",
  "tenant_id": "tenant-demo",
  "requested_by": "sales-engineering",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {
    "organization_name": "Demo Organization",
    "deployment_model": "hosted_saas",
    "region": "tenant-selected",
    "requirements": [
      "identity_provider",
      "license_validation",
      "policy_registry",
      "audit_store",
      "support_owner"
    ],
    "contacts": {
      "commercial_owner": "owner@example.invalid"
    },
    "activation_boundary": "public request shape only; tenant provisioning implementation is private"
  }
}
```

## Supported Deployment Models

- `hosted_saas`
- `self_hosted_enterprise`
- `hybrid`

## Private Responsibilities

The private SaaS or Enterprise implementation must own:

- tenant database creation and isolation;
- identity provider and SSO onboarding;
- license validation and entitlement binding;
- hosted policy registry enrollment;
- tenant audit-store provisioning;
- billing and subscription status checks;
- support and customer-success ownership;
- observability, incident response, and operational runbooks.

## Public Boundary

This repository may contain request builders, response summaries, schema
versions, validation, tests, and documentation.

This repository must not contain tenant records, production tenant IDs, billing
secrets, license keys, private policy packs, provider URLs, webhook secrets,
connector credentials, SaaS backend implementation, or Enterprise source code.

## Validation

Public tests cover:

- tenant onboarding request serialization;
- invalid deployment model rejection;
- sensitive contact-field rejection;
- unavailable response messaging that lists private modules required for tenant
  activation.

## Next Recommendation

Implement the public entitlement status contract so tenant onboarding can refer
to stable license, subscription, and feature-entitlement response shapes.
