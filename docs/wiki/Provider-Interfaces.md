# Provider Interfaces

CAVRA separates product capability from provider readiness. Community operators
can self-host with their own providers; CAVRA Managed operates providers as a
service; Enterprise Subscription can add certified packages and implementation
help.

## Common Providers

- Identity provider for SSO/RBAC.
- Approval provider and reviewer mapping.
- Audit and evidence store.
- Object storage.
- Database.
- Report delivery provider.
- Policy registry.
- Secret store.
- Connector credentials.
- Monitoring and alerting.

## Public Boundary

The public repository can contain provider contracts, schemas, and reference
implementations. It must not contain customer secrets, production credentials,
private signing material, customer-specific templates, billing records, or
internal-only runbooks.
