# Trial License Evaluator Access Sync

This public-safe sync records that private Enterprise PR #87 connected approved
trial package releases to license issuance references and evaluator access
grants.

The implementation lives only in the private `Huzefaaa2/cavra-enterprise`
repository. This public Community repository contains documentation of the
boundary, not Enterprise source code or trial artifacts.

## What The Private Evidence Records

The private evidence records references only:

- approved trial package release reference;
- license reference;
- license-service issuance reference;
- entitlement reference;
- evaluator and organization references;
- private access channel;
- trial artifact reference;
- evaluator access grant reference;
- support owner;
- onboarding reference;
- revocation reference;
- issue and expiry timestamps.

Supported private access channels are:

- `private_ghcr`
- `private_binary`
- `hosted_saas`

## Required Gates

Evaluator access is blocked unless:

- the trial package release approval is approved;
- license issuance references are present;
- evaluator access references are present;
- the access channel is private or hosted;
- license expiry and evaluator access expiry match.

## Public Boundary

Do not commit any of the following to this public repository:

- license keys;
- license signing keys;
- registry tokens or image pull secrets;
- customer records;
- tenant secrets;
- SaaS license-service source code;
- Enterprise trial artifact bytes;
- paid policy packs.

## Enterprise Challenge Solved

Enterprise trial access must be auditable without exposing the commercial
implementation. This sync shows that trial packages are now followed by governed
license issuance and evaluator access evidence in the private repository, while
the public repository remains safe for Community Edition adoption.

## Next Recommendation

Add private license revocation and evaluator access expiry evidence, then sync
the public docs with a public-safe summary of access removal or renewal gates.
