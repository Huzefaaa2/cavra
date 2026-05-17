# Console Authenticated Sessions

CAVRA now exposes a read-only console session endpoint and uses the same OIDC/JWKS and repository RBAC model for console mutations that approval decisions already use.

## Endpoint

- `GET /console/session`

Pass a signed OIDC JWT in the `Authorization` header:

```bash
curl http://127.0.0.1:8000/console/session \
  -H "Authorization: Bearer $CAVRA_CONSOLE_TOKEN"
```

The response reports authentication mode, verified actor, groups, repository-scoped permissions, and console permission flags.

## Configuration

Use the existing approval identity configuration:

```bash
export CAVRA_APPROVAL_OIDC_CONFIG=.cavra/approval-oidc.json
export CAVRA_APPROVAL_RBAC_FILE=.cavra/approval-rbac.yaml
uvicorn cavra.api:app --reload
```

The OIDC config validates issuer, audience, expiry, not-before, JWKS key ID, and RS256 signature. The RBAC file maps external identity groups to CAVRA approval groups and repository permissions.

## Enforced Console Mutations

When OIDC or RBAC is configured, the following API actions require verified actor context from an `Authorization: Bearer` token, `actor_token`, or `actor_claims`:

- `POST /approvals/{approval_id}/approve`
- `POST /approvals/{approval_id}/deny`
- `POST /approvals/{approval_id}/expire`
- `POST /approvals/break-glass`

Approval decisions use repository-scoped RBAC. Break-glass actions require an actor in the `Change Advisory Board` group.

## Console UI

The sandbox console includes a Console Session panel. Operators can paste a bearer token for local validation; approval and break-glass actions then send that token automatically.

## User Stories

- As a platform engineer, I can confirm which OIDC actor the console is using.
- As an IAM owner, I can approve repository-scoped actions from the console without global approval authority.
- As a security architect, I can require verified actor context for browser-visible console mutations.

## Enterprise Value

Authenticated console sessions close the gap between a useful operational console and production identity requirements. CAVRA can now show read-oriented operational data while requiring signed, repository-scoped identity context before console users approve, deny, expire, or break-glass controlled actions.
