# SaaS Control Plane

The SaaS Control Plane is a future private service. It must not be implemented
in this public repository.

## Future Flow

```text
Customer GitHub/GitLab/Azure DevOps Pipeline
  -> Terraform Plan / IaC Metadata / Agent Action
  -> CAVRA SaaS API
  -> Policy Evaluation
  -> Risk Score
  -> Compliance Evidence
  -> Pass / Warn / Block
```

## Future Modules

- tenant management;
- billing integration;
- license service;
- policy registry;
- audit store;
- AI recommendation engine;
- compliance export;
- organization dashboard;
- SSO and SCIM;
- enterprise reporting.

## Public Boundary

The public Community repository may contain API contracts, client stubs, and
documentation. It must not contain SaaS backend source, production
configuration, signing keys, billing secrets, customer records, or model
prompts used by paid recommendation services.

## Public Contract

The public-safe request and response contract is documented in
[SaaS Control Plane Contract](saas-control-plane-contract.md). It defines
schema-tagged shapes for tenant status, license validation handoff, policy
registry lookup, and evidence export requests. The implementation in
`src/cavra/saas_control_plane.py` is limited to client-side payload builders,
serialization, and secret-field rejection. Hosted service behavior remains a
private Enterprise/SaaS responsibility.
