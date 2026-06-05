# Enterprise Trial Self-Service Access

CAVRA Enterprise Trial is moving from manually coordinated private access to
self-service approved access.

The public portal now includes an Enterprise Trial request surface. Production
deployments can connect that form to the private `CAVRA Trial Access Portal`
service in `Huzefaaa2/cavra-enterprise`.

## Availability

Live request landing page and portal:

```text
https://cavra-trial.mind-ops.cloud
```

The CAVRA Trial domain is the canonical evaluator-facing landing page. It hosts
the branded request form and submits directly to the private Trial Access
service.

Current approved trial package:

```text
ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05
```

Public-safe digest:

```text
sha256:2d5f0d338a5528205f11674917d1526db7aa9732ef2af6ca3bd957b6230b4b47
```

Enterprise Trial is not an anonymous public download. It is available through
self-service request and approved private access.

Latest public-safe validation: on 2026-06-05, the hosted portal health check,
PostgreSQL storage health check, public portal configuration, synthetic signup,
operator approval, license validation, and revocation flow were validated using
a synthetic evaluator request. No license token, signing key, operator token, or
Enterprise source code is stored in the public repository.

## Evaluator Flow

1. Evaluator submits the public trial request form.
2. The evaluator receives a professional request-submitted email at the work
   email used in the form.
3. The private portal stores the request in private deployment storage.
4. Personal email domains, missing terms acceptance, and unapproved domains can
   be rejected automatically.
5. The trial operator receives an approval alert and reviews the request in the
   private operator dashboard.
6. A trial operator approves the request.
7. The private license service issues a time-limited signed trial license.
8. The portal stores only the token digest and access metadata.
9. The evaluator receives private GHCR access, license material, validation key
   material, and install instructions through the submitted work email and any
   additional approved private handoff channel.
10. Access can be expired or revoked.

Approval emails contain license material for the named evaluator only. Do not
forward approval emails to public channels, issue trackers, or shared documents.

## Public Portal Integration

The public GitHub Pages portal links users to the dedicated Trial domain. It no
longer acts as the primary request form.

For GitHub Pages, keep repository variable `CAVRA_PUBLIC_TRIAL_API_URL` pointed
at the private HTTPS Trial Access Portal origin for compatibility with older
static builds. New evaluator requests should start at the Trial domain.

Current production value:

```text
CAVRA_PUBLIC_TRIAL_API_URL=https://cavra-trial.mind-ops.cloud
```

## GitHub Pages and Jekyll Fit

GitHub Pages is suitable for the public CAVRA landing portal, documentation,
trial request form, and static evaluator instructions. Jekyll can be used later
if the docs move to a generated documentation site, but it is not required for
the current HTML portal.

GitHub Pages must not host the private Trial Access Portal service, license
service, signing keys, evaluator records, revocation state, GHCR pull secrets,
or Enterprise source. The public page should only submit requests to a separate
HTTPS API endpoint controlled by the private Enterprise deployment.

Recommended split:

- GitHub Pages: public CAVRA portal, docs, and static trial overview.
- Replit custom domain: branded Enterprise Trial landing page and request form.
- Private HTTPS service: `/trial/signup`, `/trial/approve`, `/trial/revoke`,
  `/trial/status/{request_id}`, license issuance, expiry, revocation, and
  operator workflows.
- Private email delivery: request acknowledgement, operator alert, and approved
  evaluator handoff through the configured CAVRA trial mailbox.
- GHCR: private Enterprise Trial package, gated by approved evaluator access.

The private API must be hosted behind HTTPS, bot protection, rate limits, audit
logging, and operator approval controls before public launch.

## Private Boundaries

Do not publish:

- Enterprise source code;
- license tokens;
- license signing keys;
- registry pull secrets;
- customer records;
- revocation state;
- paid policy packs;
- private approval notes;
- SaaS backend internals.

The public repository only documents the evaluator path and public-safe package
status.
