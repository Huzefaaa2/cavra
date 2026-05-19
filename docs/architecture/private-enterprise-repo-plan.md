# Private Enterprise Repository Plan

Recommended private repository name: `cavra-enterprise`

If I cannot create the private repository from the current environment, prepare
it manually in GitHub under `Huzefaaa2` as a private repository with branch
protection, secret scanning, CodeQL, Dependabot, and required reviews.

## Suggested Structure

```text
cavra-enterprise/
  src/
    cavra_enterprise/
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
  docker/
    Dockerfile.enterprise
  charts/
    helm/
  .github/
    workflows/
      enterprise-ci.yml
      enterprise-release.yml
```

## Integration With Public CAVRA

Enterprise can plug into Community through:

- Python package `cavra_enterprise`;
- plugin manifests with `edition_required=enterprise`;
- private Docker image layers;
- private license validation client;
- hosted SaaS Control Plane APIs.

The public package should never import Enterprise modules directly except
through dynamic hooks such as `cavra.edition.enterprise_hooks`.
