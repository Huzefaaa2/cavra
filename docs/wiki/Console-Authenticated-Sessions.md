# Console Authenticated Sessions

CAVRA now exposes `GET /console/session` and enforces verified actor context for console mutations when OIDC or RBAC is configured.

## How It Works

The console session endpoint accepts `Authorization: Bearer <OIDC JWT>`. The API validates the token with `CAVRA_APPROVAL_OIDC_CONFIG`, maps groups with `CAVRA_APPROVAL_RBAC_FILE`, and returns actor, groups, repository permissions, and console permission flags.

## Enforced Actions

- `POST /approvals/{approval_id}/approve`
- `POST /approvals/{approval_id}/deny`
- `POST /approvals/{approval_id}/expire`
- `POST /approvals/break-glass`

Approval decisions use repository-scoped RBAC. Break-glass actions require `Change Advisory Board` group membership.

## Console UI

The sandbox console includes a Console Session panel for bearer-token validation. Once a token is active, approval and break-glass actions include it automatically.

## User Stories

- As a platform engineer, I can verify the console actor before approving controlled actions.
- As a repository owner, I can receive repository-scoped approval rights without global authority.
- As an auditor, I can confirm that browser-visible mutations require signed identity context.
