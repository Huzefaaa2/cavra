# Private Enterprise Repo Plan

Recommended private repository: `Huzefaaa2/cavra-enterprise`

Status: created as a private GitHub repository.

Initial private implementation status:

- Python package `cavra_enterprise`
- private pilot-intake tenant store
- encrypted-at-rest payload codec
- customer/SaaS KMS-style envelope encryption contract
- authenticated update authorization
- production SSO claim binding
- managed tenant database adapter contract
- CRM/ITSM/GRC/customer-success/tenant-management handoff workers
- provider-native Salesforce, HubSpot, Jira, ServiceNow, and Archer payload adapters
- immutable audit export and retention enforcement
- provider-specific OAuth, bearer, API-key, and basic-token auth providers
- retryable provider rate-limit handling
- audit-event persistence
- connector handoff dispatcher interfaces
- private CI workflow

Repository hardening status:

- Dependabot vulnerability alerts: enabled
- squash-only merge policy and delete-branch-on-merge: enabled
- branch protection and secret scanning: blocked by the current GitHub plan for private repositories

Suggested structure:

```text
cavra-enterprise/
  src/cavra_enterprise/
    identity/
    pilot_intake/
    sso/
    rbac/
    audit/
    dashboard/
    policy_approval/
    compliance_reports/
    ai_remediation/
    drift_monitoring/
    license_server_client/
  policy_packs/
    pci_dss/
    cis/
    azure_landing_zone/
    aws_control_tower/
    fca_emoney/
  docker/Dockerfile.enterprise
  charts/helm/
  .github/workflows/
```

The private package can plug into public CAVRA through dynamic import of
`cavra_enterprise`, Enterprise plugin manifests, private Docker images, and
private license validation.
