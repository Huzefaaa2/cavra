# SaaS Control Plane Contract

CAVRA Community Edition can expose public-safe request and response contracts
for a future SaaS Control Plane. It must not include the hosted service source
code, license service implementation, tenant database logic, billing logic,
customer records, signing secrets, or paid recommendation logic.

## Contract Purpose

The public contract gives Community, Trial, Enterprise, and future SaaS
integrations a stable vocabulary for:

- entitlement status checks;
- tenant onboarding requests;
- tenant status checks;
- license validation handoff;
- policy registry readiness checks;
- policy registry lookup;
- tenant audit-store operating checks;
- customer operating dashboard checks;
- support handoff readiness checks;
- SaaS operating automation checks;
- evidence export requests.

The contract is implemented in `src/cavra/saas_control_plane.py`. It builds
schema-tagged payloads and rejects obvious secret-bearing fields before a
payload can be serialized.

## Public Request Envelope

```json
{
  "schema_version": "cavra.saas_control_plane.request.v1",
  "operation": "tenant_status",
  "tenant_id": "tenant-demo",
  "requested_by": "console",
  "correlation_id": "saas-example",
  "private_implementation_required": true,
  "payload": {}
}
```

The public request envelope is a client-side shape only. It is not a SaaS API
implementation.

## Operations

| Operation | Public request content | Private response responsibility |
| --- | --- | --- |
| `entitlement_status` | Tenant identifier and optional feature names | Subscription, license, and feature-entitlement summary |
| `tenant_onboarding` | Tenant activation metadata, deployment model, contacts, and readiness requirements | Tenant provisioning, identity onboarding, entitlement binding, audit-store readiness, and support ownership |
| `tenant_status` | Tenant identifier and requested capabilities | Entitlement, subscription, region, and service availability summary |
| `license_validation` | Local validation report and requested server checks | Signature, revocation, subscription, and feature-grant validation |
| `policy_registry_readiness` | Tenant identifier, catalog scope, policy-pack references, and readiness checks | Hosted registry availability, catalog freshness, version state, approval state, blockers, and private service handoff status |
| `policy_registry_lookup` | Policy references and public labels | Hosted policy metadata and governed artifact references |
| `tenant_audit_store_operating` | Tenant identifier, retention profile, evidence window, and operating checks | Audit-store health, retention posture, evidence freshness, export readiness, blockers, and private service handoff status |
| `customer_operating_dashboard` | Tenant identifier, dashboard scope, evidence window, and operating dashboard checks | Customer operating dashboard readiness across billing, license service, support, customer success, escalation, and release closeout |
| `support_handoff_readiness` | Tenant identifier, handoff scope, support tier, and support handoff checks | Support, customer-success, escalation, health review, dashboard, and release owner readiness |
| `saas_operating_automation` | Tenant identifier, automation scope, automation cadence, and operating automation checks | Billing monitoring, license telemetry, support follow-up, customer-success review, dashboard refresh, escalation drill, and closeout retry readiness |
| `evidence_export` | Evidence references, export format, and retention profile | Export job creation, storage, delivery, and audit status |

## Security Boundary

The public contract rejects payload keys that look like credentials, private
keys, signing material, or authorization material. It also rejects common token
formats in string values.

This repository may contain:

- dataclass request and response envelopes;
- schema version constants;
- local validation and serialization tests;
- documentation and examples using synthetic identifiers.

This repository must not contain:

- SaaS backend source code;
- production tenant records;
- customer evidence payloads;
- license signing secrets;
- billing provider secrets;
- hosted policy registry implementation;
- AI recommendation service prompts or model-routing logic.

## Expected Private Implementation

The future private SaaS repository or service should implement:

- authenticated API endpoints;
- tenant isolation;
- license service integration;
- billing and subscription status checks;
- hosted policy registry readiness checks;
- policy registry storage and artifact delivery;
- tenant audit-store health and retention checks;
- customer operating dashboard readiness checks;
- support handoff readiness checks;
- SaaS operating automation readiness checks;
- evidence export jobs;
- compliance export delivery;
- audit history persistence;
- observability, rate limits, and incident response controls.

The public contract should remain stable enough that Community clients and
Enterprise packages can call the private service without importing private
source code into this repository.

## Validation

Public tests cover:

- contract description boundaries;
- public API contract discovery;
- tenant status request serialization;
- license validation report handoff;
- hosted policy registry readiness request and response serialization;
- policy lookup validation;
- tenant audit-store operating request and response serialization;
- customer operating dashboard request and response serialization;
- support handoff readiness request and response serialization;
- SaaS operating automation request and response serialization;
- SaaS operating automation API and CLI surfaces;
- evidence export format validation;
- rejection of sensitive keys and token-like values;
- unavailable responses that direct users to private service enablement.
