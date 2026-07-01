# Community-First Product Model Migration

This migration replaces the old four-edition model with a Community-first model.

## Old Model

- Community Edition
- Trial Edition
- Enterprise Edition
- SaaS

## New Model

- CAVRA Community: full self-hosted public product.
- CAVRA Managed: hosted managed service.
- CAVRA Enterprise Subscription: commercial support, SLA, certified connectors, policy and compliance packs, implementation help, and private customer operations.
- CAVRA Trial: temporary evaluation access path.

## Compatibility

The code still accepts old `LicenseEdition` values and `CAVRA_EDITION` where
removing them would break users. New deployments should prefer:

```bash
CAVRA_DEPLOYMENT_MODE=community|managed|trial_access
CAVRA_COMMERCIAL_ENTITLEMENT=none|enterprise_subscription|managed
CAVRA_PROVIDER_PROFILE=local|self_hosted|managed
```

## Documentation Rule

Use "requires configuration" for self-hostable capabilities that need backing
providers. Use "requires managed service" for hosted operations. Use "requires
commercial entitlement" for certified connectors, commercial packs, SLA, and
implementation services.
