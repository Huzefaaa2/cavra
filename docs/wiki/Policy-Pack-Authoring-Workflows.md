# Policy Pack Authoring Workflows

CAVRA supports safe policy authoring previews and governed rollout change workflows.

## API

- `GET /policy-pack-catalog`
- `POST /policy-packs/draft`
- `POST /policy-rollouts/change-plan`
- `POST /policy-rollouts/apply-change`

Policy drafts are read-only previews. They validate against the policy schema and include rule counts and operator notes.

Rollout change plans include before/after state, changed fields, risk, approval requirement, and operator notes. Applying a rollout change persists the normalized rollout record. When OIDC or RBAC is configured, apply-change requires verified actor context.

## Console

The sandbox console includes Policy Authoring and Rollout Changes for catalog refresh, draft preview, rollout planning, and rollout apply.

## User Stories

- As a platform engineer, I can preview policy packs before committing them.
- As a security engineer, I can review rollout risk before enforcement.
- As an auditor, I can inspect rollout change plans.
