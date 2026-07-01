# CAVRA Product Model

CAVRA uses a Community-first model:

- **CAVRA Community:** the full public self-hosted product and default codebase.
- **CAVRA Managed:** hosted CAVRA operated as a managed service.
- **CAVRA Enterprise Subscription:** commercial support, SLA, certified connectors, policy and compliance packs, implementation help, and private customer operations.
- **CAVRA Trial:** temporary evaluator access for Managed or Enterprise Subscription capabilities. Trial is not a separate edition.

![CAVRA product model map](assets/textbook/cavra-edition-map.svg)

## Capability Language

Do not describe a self-hostable Community capability as "Enterprise-only" just
because a backing provider is missing. Use these statuses:

| Status | Use when |
| --- | --- |
| Available | The capability is included and ready. |
| Requires configuration | The capability is included, but needs identity, audit storage, report delivery, database, object storage, policy registry, or connector credentials. |
| Requires managed service | The capability depends on hosted operations provided by CAVRA Managed. |
| Requires commercial entitlement | The capability depends on Enterprise Subscription, certified connectors, commercial policy packs, compliance packs, or implementation services. |

## Migration Map

| Old phrase | New phrase |
| --- | --- |
| Community Edition | CAVRA Community |
| Enterprise Edition | CAVRA Enterprise Subscription or supported deployment |
| SaaS | CAVRA Managed |
| Trial Edition | CAVRA Trial access |
| Enterprise-only feature | Requires configuration, managed service, or commercial entitlement |
| Locked feature | Not configured or requires entitlement |

Historical release notes may retain old labels when clearly archived.
