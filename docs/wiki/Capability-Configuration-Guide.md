# Capability Configuration Guide

CAVRA Community includes the public product surface. Some capabilities require
operator-provided backing services before they are production-ready.

| Capability | Status before setup | Required configuration |
| --- | --- | --- |
| SSO/RBAC | Requires configuration | Identity provider, OIDC/SAML app, role mapping, reviewer groups. |
| Audit export | Requires configuration | Evidence store, export destination, retention policy. |
| Report delivery | Requires configuration | SMTP or report provider, recipient allowlist, delivery audit store. |
| Policy registry | Requires configuration | Database or object storage, versioning, approval workflow. |
| Connector framework | Available | Secret store and connector credentials for live integrations. |
| Certified connectors | Requires commercial entitlement | Enterprise Subscription or certified connector package. |
| Managed report delivery | Requires managed service | CAVRA Managed. |
| Billing and customer-success operations | Requires managed service | CAVRA Managed. |

When a provider is missing, the correct product response is
`requires_configuration`, not `Enterprise-only`.
