# Policy Pack Authoring Workflows

CAVRA supports safe policy authoring previews and governed rollout change workflows.

## API

- `GET /policy-pack-catalog`
- `POST /policy-packs/draft`
- `POST /policy-packs/publish-plan`
- `POST /policy-packs/publish-request`
- `POST /policy-packs/publish`
- `POST /policy-rollouts/change-plan`
- `POST /policy-rollouts/apply-change`

Policy drafts are read-only previews. They validate against the policy schema and include rule counts and operator notes.

Policy publishing is approval-bound and signed. CAVRA creates a publish plan with a draft digest, creates an approval request bound to that digest, and writes `policy.yaml` plus `policy.yaml.sig.json` only after the matching approval is approved or break-glass. Mismatched draft digests are rejected before write-back.

Rollout change plans include before/after state, changed fields, risk, approval requirement, and operator notes. Applying a rollout change persists the normalized rollout record. When OIDC or RBAC is configured, apply-change requires verified actor context.

## Console

The sandbox console includes Policy Authoring and Rollout Changes for catalog refresh, draft preview, publish planning, publish approval requests, signed publishing, rollout planning, and rollout apply.

## User Stories

- As a platform engineer, I can preview policy packs before committing them.
- As a platform engineer, I can publish approved policy packs with signature metadata.
- As a security engineer, I can review rollout risk before enforcement.
- As an auditor, I can inspect rollout change plans and approval-bound policy write-back evidence.
