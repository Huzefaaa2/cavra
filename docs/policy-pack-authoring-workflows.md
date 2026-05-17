# Policy Pack Authoring and Rollout Change Workflows

CAVRA now supports safe policy authoring previews and governed rollout change workflows through the API and console.

## Policy Authoring Preview

Use `POST /policy-packs/draft` to generate and validate a policy pack draft without writing to the policy directory.

The draft response includes:

- Generated policy YAML-equivalent structure.
- JSON Schema validation status.
- Validation errors.
- Rule counts by section.
- Operator notes for repository change control.

Use `GET /policy-pack-catalog` to list installed policy packs with rule summaries.

## Rollout Change Workflow

Use `POST /policy-rollouts/change-plan` to preview a rollout transition before applying it.

Use `POST /policy-rollouts/apply-change` to persist the planned rollout transition.

Rollout plans include:

- Create or update operation.
- Before and after rollout state.
- Field-level changes.
- Risk level.
- Whether approval is required.
- Operator notes.

When OIDC or RBAC is configured, apply-change requires verified actor context through a bearer token, `actor_token`, or `actor_claims`.

## Console

The sandbox console includes Policy Authoring and Rollout Changes:

- Refresh policy catalog.
- Preview policy drafts.
- Plan rollout changes.
- Apply rollout changes.

## User Stories

- As a platform engineer, I can preview a policy pack before committing it to source control.
- As a security engineer, I can review rollout risk before moving from audit-only to enforcement.
- As an auditor, I can inspect rollout change plans and evidence before a policy mode changes.

## Enterprise Value

Policy authoring and rollout workflows keep policy changes reviewable, schema-validated, and connected to repository rollout state. This reduces unmanaged policy drift and gives platform teams a controlled path from draft to rollout.
