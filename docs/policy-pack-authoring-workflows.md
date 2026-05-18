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

## Approval-Bound Signed Publishing

Publishing is no longer a direct write. Use:

- `POST /policy-packs/publish-plan` to preview create/update operation, policy digest, diff summary, target path, and risk.
- `POST /policy-packs/publish-request` to create an approval request bound to that exact draft digest.
- `POST /policy-packs/publish` with `approval_id` to write `policy.yaml` and `policy.yaml.sig.json` only after approval.

The publish endpoint rejects:

- Invalid drafts.
- Pending, denied, or expired approvals.
- Approvals created for a different policy ID or draft digest.
- Unsafe policy IDs that would escape the policy directory.

Set `CAVRA_POLICY_DIR` for the policy write-back root. Set `CAVRA_POLICY_SIGNING_KEY` to create HMAC-backed signatures; otherwise CAVRA writes digest-backed signature metadata for local workflows.

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
- Plan signed policy publishing.
- Request policy publish approval.
- Publish approved policy packs with signature metadata.
- Plan rollout changes.
- Apply rollout changes.

## User Stories

- As a platform engineer, I can preview a policy pack before committing it to source control.
- As a platform engineer, I can publish policy packs only after approval and signature generation.
- As a security engineer, I can review rollout risk before moving from audit-only to enforcement.
- As a security engineer, I can reject write-back when the approved draft digest does not match the submitted draft.
- As an auditor, I can inspect rollout change plans and evidence before a policy mode changes.

## Enterprise Value

Policy authoring and rollout workflows keep policy changes reviewable, schema-validated, approval-bound, signed, and connected to repository rollout state. This reduces unmanaged policy drift and gives platform teams a controlled path from draft to publish to rollout.
