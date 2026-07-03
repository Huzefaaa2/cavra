# CAVRA Enterprise Identity And Access Control

Last updated: 2026-07-03

This document defines the public-safe R2.1 Enterprise identity contract for CAVRA. It covers the identity controls that CAVRA Community can validate publicly and the private Managed or Enterprise services that complete production SSO, SCIM, tenant directory, and customer-specific automation.

## Scope

CAVRA Enterprise identity uses one common claim contract across:

- OIDC and JWKS token validation for API and console mutations;
- SAML bridge deployments where a customer IdP or private Enterprise bridge normalizes SAML assertions into the same CAVRA OIDC-style claims;
- SCIM lifecycle synchronization for groups, roles, tenants, workspaces, and deprovisioning evidence;
- RBAC roles for CISO, security operators, platform security, model owners, auditors, and break-glass approvers;
- ABAC resource boundaries for tenant, workspace, repository, environment, model owner, and data classification.

The public repository validates the contract and runtime posture. Private Enterprise services own customer directory storage, SAML certificates, SCIM bearer tokens, tenant membership sync workers, and IdP-specific automation.

## Runtime Configuration

```bash
export CAVRA_APPROVAL_OIDC_CONFIG=.cavra/identity/approval-oidc.json
export CAVRA_APPROVAL_RBAC_FILE=.cavra/identity/approval-rbac.yaml
export CAVRA_ENTERPRISE_IDENTITY_POLICY=.cavra/identity/enterprise-identity-policy.yaml
export CAVRA_CORS_ORIGINS=https://cavra-console.example.com
uvicorn cavra.api:app --host 0.0.0.0 --port 8000
```

Inspect the contract and runtime readiness:

```bash
curl http://127.0.0.1:8000/identity/enterprise-contract
curl http://127.0.0.1:8000/identity/enterprise-readiness
curl http://127.0.0.1:8000/console/session \
  -H "Authorization: Bearer $CAVRA_CONSOLE_TOKEN"
```

If `CAVRA_ENTERPRISE_IDENTITY_POLICY` is not set, CAVRA exposes the default R2.1 contract. Operators can still validate the expected Enterprise shape before private IdP and SCIM integrations are attached. Without live OIDC/RBAC runtime configuration, `/identity/enterprise-readiness` reports `contract_ready`, not full runtime `ready`.

## Claim Contract

| Claim | Purpose |
| --- | --- |
| `sub` | Stable IdP subject. |
| `email` or `preferred_username` | Public actor name in approval and audit evidence. |
| `groups` | External IdP groups mapped to CAVRA roles and approval groups. |
| `roles` | Optional direct role claim. |
| `tenant_id` | Tenant boundary used by R2.2 persistence and isolation. |
| `workspace_id` | Workspace boundary inside a tenant. |
| `repository` | Repository-scoped approval boundary. |
| `environment` | Runtime or deployment environment boundary. |
| `model_owner_ref` | Model/artifact owner boundary for model governance approvals. |
| `data_classification` | Data handling and approval boundary. |

## RBAC Roles

| Role | Typical group | Responsibility |
| --- | --- | --- |
| `ciso` | `CAVRA-CISO` | Executive risk acceptance, posture review, production gate acceptance. |
| `security_operator` | `CAVRA-Security-Operations` | Runtime operations, findings, incident workflow, report operations. |
| `platform_security` | `CAVRA-Platform-Security` | CI/CD, repository, cloud, infrastructure, and policy approval paths. |
| `model_owner` | `CAVRA-Model-Owners` | Model/artifact approval, model registry risk acceptance, ownership evidence. |
| `auditor` | `CAVRA-Auditors` | Read-only audit evidence and compliance review. |
| `break_glass_approver` | `Change Advisory Board` | Emergency override approval with short TTL and retained evidence. |

## ABAC Boundaries

CAVRA treats RBAC as necessary but not sufficient for Enterprise operation. ABAC attributes bind a permitted role to a permitted resource:

- `tenant_id`;
- `workspace_id`;
- `repository`;
- `environment`;
- `model_owner_ref`;
- `data_classification`.

The public helper `actor_has_enterprise_scope` enforces tenant and workspace equality for scoped resources and role checks for runtime action approval, model/artifact approval, audit read access, and break-glass access.

## Runtime ABAC Enforcement

Approval decisions now enforce the same Enterprise scope contract at runtime. When an approval request includes Enterprise resource attributes, CAVRA checks the verified actor context before legacy approval group or repository RBAC can authorize the mutation.

| Approval type | Required role | Required boundary |
| --- | --- | --- |
| Runtime action approval | `security_operator` or `platform_security` | Matching `tenant_id` and `workspace_id` when present. |
| Model or AI artifact approval | `model_owner` or `ciso` | Matching `tenant_id` and `workspace_id` when present, plus model owner context when supplied. |
| Break-glass approval | `break_glass_approver` and `Change Advisory Board` group | Reason, external reference, TTL, and retained audit evidence. |

Scoped approvals are detected from approval or decision fields such as `tenant_id`, `workspace_id`, `repository`, `environment`, `model_owner_ref`, `data_classification`, `asset_type`, `artifact_type`, and `model_artifact_ref`. Community and local workflows that do not include Enterprise ABAC fields continue to use the existing approval group and repository RBAC behavior.

Internally, scoped approval enforcement maps requests to `approve_runtime_action`, `approve_model_artifact`, or `break_glass` before calling the Enterprise scope checker.

## SAML Bridge

CAVRA does not store SAML certificates or customer SAML metadata in this public repository. Enterprise SAML support uses one of these deployment patterns:

1. IdP emits OIDC tokens directly for CAVRA.
2. Customer identity gateway converts SAML assertions to OIDC/JWT claims.
3. Private CAVRA Enterprise bridge validates SAML and emits the CAVRA claim contract.

The required bridge output is the same OIDC-style claim contract listed above. This keeps approval, console, AISPM, and tenant-isolation logic independent from customer-specific SAML plumbing.

## SCIM Lifecycle Contract

Private Enterprise services must synchronize:

- group-to-role membership;
- tenant and workspace membership;
- create, update, disable, and delete events;
- deprovisioning within the configured SLA, defaulting to 60 minutes;
- audit evidence for directory changes that affect CAVRA access.

The public readiness endpoint validates that the contract is present. The private service validates live SCIM connectivity and deprovisioning evidence.

## Break-Glass Controls

Break-glass requires:

- `break_glass_approver` role mapped to `Change Advisory Board`;
- reason;
- external change or incident reference;
- maximum TTL of four hours;
- retained audit event.

When OIDC or RBAC is configured, CAVRA console mutation endpoints reject unauthenticated break-glass requests.

## Validation

```bash
python3 scripts/validate_enterprise_identity_readiness.py
python3 scripts/validate_enterprise_live_identity_packet.py \
  --packet .cavra/identity/enterprise-live-identity-validation.json \
  --output dist/enterprise-live-identity-validation-result.json
python3 -m pytest tests/test_enterprise_identity.py tests/test_identity_references.py -q
```

R2.1 is considered implementation-in-progress until live customer or private Enterprise IdP/SCIM integration tests produce a live packet where `ready_for_live_enterprise_identity` is `true`, but the public code now exposes and validates the Enterprise identity shape, runtime scoped approval enforcement, and public-safe live evidence packet.

See [Enterprise Live Identity Validation](enterprise-live-identity-validation.md) for the packet format and completion gate.
