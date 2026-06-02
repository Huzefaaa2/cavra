# Enterprise Licensing

Future license types:

- community;
- trial;
- business;
- enterprise;
- saas.

The public repository provides safe license objects and local placeholder
validation only. Enterprise license signing, revocation, billing status,
customer entitlements, and SaaS validation belong in private services.

## Public Validation Behavior

The Community client can load local JSON-shaped license payloads and return a
public-safe validation report. It supports:

- valid Community licenses without a key;
- trial, business, enterprise, and SaaS placeholder license shapes;
- expired license detection from `expires_at`;
- invalid payload detection for unknown editions or statuses;
- revoked and suspended status preservation;
- unsupported Community signatures because the public client does not verify
  private signing material.

The validation report includes status, edition, license ID, enabled features,
locked features, and whether private validation is required.

## Private Validation Boundary

The public client does not verify signatures, revocation lists, billing state,
tenant entitlements, subscription status, customer contracts, or SaaS tenant
ownership. Those checks must be delegated to private Enterprise or SaaS license
services.

## Next Step

Continue with the public SaaS Control Plane contract. That contract should
define public-safe tenant status, license validation boundary, policy registry,
and evidence export shapes without implementing the private SaaS backend.
