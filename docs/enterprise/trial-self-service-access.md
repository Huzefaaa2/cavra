# Enterprise Trial Self-Service Access

CAVRA Enterprise Trial is moving from manually coordinated private access to
self-service approved access.

The public portal now includes an Enterprise Trial request surface. Production
deployments can connect that form to the private `CAVRA Trial Access Portal`
service in `Huzefaaa2/cavra-enterprise`.

## Availability

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

## Evaluator Flow

1. Evaluator submits the public trial request form.
2. The private portal stores the request in private deployment storage.
3. Personal email domains, missing terms acceptance, and unapproved domains can
   be rejected automatically.
4. A trial operator approves the request.
5. The private license service issues a time-limited signed trial license.
6. The portal stores only the token digest and access metadata.
7. The evaluator receives private GHCR access, license material, validation key
   material, and install instructions through an approved private channel.
8. Access can be expired or revoked.

## Public Portal Integration

The static public portal supports two modes:

- Static preview mode: stores request status locally when no private API URL is
  configured.
- Live private portal mode: posts the signup payload to
  `CAVRA_TRIAL_API_URL/trial/signup`.

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
