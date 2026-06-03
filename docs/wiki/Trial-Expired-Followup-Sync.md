# Trial Expired Follow-Up Sync

This public-safe sync records that private Enterprise PR #89 added
expired-trial follow-up automation evidence for evaluator notifications,
grace-period approvals, and commercial handoff references.

The implementation lives only in the private `Huzefaaa2/cavra-enterprise`
repository. This public Community repository contains documentation of the
boundary, not Enterprise source code, customer data, license-service logic, CRM
integration code, or trial artifact bytes.

## What The Private Evidence Records

The private evidence consumes approved trial access expiry evidence and records
references for:

- evaluator notification;
- notification channel and delivery tracking;
- grace-period approval when access is renewed or escalated;
- customer-success, sales, and support handoff ownership;
- CRM or support task tracking references;
- renewed-trial follow-up;
- revoked-trial closeout handoff.

Supported public-safe notification channel labels are:

- `email`
- `customer_success`
- `support_ticket`
- `crm_task`

## Required Gates

Expired-trial follow-up evidence is blocked unless:

- trial access expiry evidence is ready;
- trial access expiry approval is approved;
- the approval package matches the expiry evidence package;
- notification references, delivery owner, and delivery tracking references are
  present;
- renewed and escalated trials include grace-period and commercial handoff
  references;
- revoked trials include a closeout commercial handoff reference;
- handoff owners and next-action references are present.

## Public Boundary

Do not commit any of the following to this public repository:

- customer records;
- CRM payloads or CRM credentials;
- license keys;
- license signing keys;
- registry tokens or image pull secrets;
- tenant secrets;
- SaaS license-service source code;
- Enterprise trial artifact bytes;
- paid policy packs.

## Enterprise Challenge Solved

Enterprise trials must not end silently. This sync shows that private Enterprise
evidence can prove expired access led to a governed notification, grace-period
decision, and commercial or support handoff while the public repository remains
safe for Community Edition adoption.

## Next Recommendation

Add private trial conversion readiness evidence so renewed or escalated trials
can move into paid pilot or production conversion with public-safe documentation
of the gates.
