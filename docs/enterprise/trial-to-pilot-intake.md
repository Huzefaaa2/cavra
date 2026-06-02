# Trial To Pilot Intake

This guide converts a successful CAVRA Community or Trial evaluation into a
scoped Enterprise pilot or SaaS onboarding motion. It is public-safe and should
be used before customer-specific details move into a private Enterprise
repository, customer-owned deployment, or SaaS tenant.

## Intake Objective

The intake should prove that CAVRA can govern AI-agent activity for a small set
of repositories while preserving approval, evidence, retention, identity, and
commercial handoff requirements.

## Intake Inputs

| Area | Public-Safe Question |
| --- | --- |
| Trial outcome | Which CAVRA scenario or workflow did the evaluator complete? |
| Repositories | Which repositories or release workflows should be in pilot scope? |
| Agents | Which AI coding agents, CI bots, or MCP tools are in scope? |
| CI/CD | Which required checks, runners, and evidence artifact paths will be used? |
| Connectors | Which non-production SIEM, ITSM, ChatOps, GRC, or webhook routes are needed? |
| Identity | Which SSO/RBAC groups own release, security, platform, and audit decisions? |
| Retention | Which evidence retention period and archive ownership model apply? |
| Commercial path | Is the customer evaluating self-hosted Enterprise, hosted SaaS, or both? |

## Pilot Scope Guardrails

- Start with one to three repositories.
- Use synthetic or non-production evidence until the private deployment is
  ready.
- Use non-production connector routes for the first handoff test.
- Keep Community mode usable without a license key.
- Keep trial license validation in private Enterprise or SaaS services.
- Do not place customer responses, license keys, connector credentials, private
  policy packs, Enterprise source, or SaaS backend details in this repository.

## Template

Use the public template:

```text
examples/demos/trial-to-pilot-intake/trial-to-pilot-intake-template.json
```

The template uses schema version `cavra.trial_to_pilot_intake.v1`. The local API
normalizes it into `cavra.pilot_intake.record.v1` and computes public-safe
readiness areas for repository/agent scope, CI/CD, connectors, SSO/RBAC,
retention, and Enterprise/SaaS handoff.

## API Usage

For local or private persistence:

```bash
curl -X POST http://127.0.0.1:8000/pilot-intakes \
  -H "Content-Type: application/json" \
  --data @examples/demos/trial-to-pilot-intake/trial-to-pilot-intake-template.json
```

Then inspect readiness:

```bash
curl http://127.0.0.1:8000/pilot-intakes/trial-to-pilot-demo/readiness
```

Private Enterprise or SaaS systems can generate a public-safe handoff plan:

```bash
curl -X POST http://127.0.0.1:8000/pilot-intakes/trial-to-pilot-demo/private-handoff-plan \
  -H "Content-Type: application/json" \
  --data '{"tenant_id":"tenant-demo","providers":["saas_tenant","security_review","customer_success"]}'
```

## Exit Criteria

- Pilot repository and release workflow scope are documented.
- Transparent agent identities and approval-required actions are documented.
- CAVRA required-check behavior is selected as audit, warn, or enforce.
- Evidence artifact path and retention requirement are documented.
- SSO/RBAC groups are mapped.
- Non-production connector routes are selected.
- Enterprise or SaaS deployment path is selected.
- Private implementation owners are assigned for customer-specific data,
  connectors, license validation, and tenant storage.

## Next Step

After this public intake is complete, continue with public licensing interface
hardening. Private trial package readiness and customer pilot handoff evidence
should remain in private repositories or SaaS systems.
