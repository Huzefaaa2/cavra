# Trial Access Expiry Sync

This public-safe sync records that private Enterprise PR #88 added trial access
expiry evidence for revoked, renewed, and escalated trial outcomes.

The implementation lives only in the private `Huzefaaa2/cavra-enterprise`
repository. This public Community repository contains documentation of the
boundary, not Enterprise source code, customer data, license-service logic, or
trial artifact bytes.

## What The Private Evidence Records

The private evidence consumes approved trial license/evaluator access evidence
and records references for one of three expiry outcomes:

- `revoked`: license and private artifact access were removed.
- `renewed`: the trial was extended with a renewal reference and new expiry.
- `escalated`: the trial was escalated for support, customer-success, or
  commercial follow-up.

The evidence records references only:

- approved trial license/evaluator access evidence reference;
- access approval reference;
- license reference;
- evaluator and organization references;
- original expiry timestamp;
- expiry outcome;
- license revocation reference, access revocation reference, renewal reference,
  or escalation reference as applicable;
- action owner and action timestamp;
- new expiry timestamp for renewed trials.

## Required Gates

Expiry evidence is blocked unless:

- trial license/evaluator access evidence is ready;
- trial license/evaluator access approval is approved;
- the approval package matches the access evidence package;
- the outcome is `revoked`, `renewed`, or `escalated`;
- action owner and action timestamp references are present;
- revoked trials include license and artifact access revocation references;
- renewed trials include a renewal reference and a new expiry;
- escalated trials include an escalation reference.

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

Enterprise trials must end cleanly. This sync shows that private Enterprise
evidence can prove evaluator access was revoked, renewed, or escalated at the
end of the trial window, while the public repository remains safe for Community
Edition adoption.

## Next Recommendation

Add private expired-trial notification, grace-period, and commercial handoff
automation, then sync public docs with public-safe follow-up and renewal gates.
