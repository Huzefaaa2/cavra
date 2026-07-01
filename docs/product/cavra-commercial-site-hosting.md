# CAVRA Commercial Site Hosting

`cavra.mind-ops.cloud` is the commercial product front door for CAVRA Managed,
CAVRA Enterprise Subscription, Trial Access, AISPM, trust, resources, and
customer contact paths.

The website source is intentionally not stored in this public CAVRA repository.
The public repository remains the Community source, public sandbox, README, wiki
textbook, and public documentation home.

## Hosting Decision

The commercial site is hosted through Replit, matching the operating model
already used for `cavra-trial.mind-ops.cloud`.

Recommended surface map:

| Surface | Role |
| --- | --- |
| `cavra.mind-ops.cloud` | Commercial product front door hosted on Replit. |
| `cavra-trial.mind-ops.cloud` | Trial intake and evaluator workflow hosted on Replit. |
| `huzefaaa2.github.io/cavra` | Public sandbox, demo console, and documentation bridge. |
| GitHub Wiki | Public CAVRA technical textbook and field documentation. |
| Public CAVRA repo | Community source, public contracts, public docs, and release evidence. |

## DNS Notes

Replit generates the exact DNS records from the Publishing area after the custom
domain is attached. For a Spaceship-managed subdomain, add the records that
Replit provides for `cavra.mind-ops.cloud`.

Expected record types:

- `A` record for the `cavra` hostname pointing to the Replit-provided IP address.
- `TXT` record for the `cavra` hostname containing the Replit verification value.

Keep the Replit verification `TXT` record in place permanently so Replit can
renew the SSL/TLS certificate.

DNS propagation can take several minutes and may take up to 48 hours depending
on registrar and resolver caches.

## Public Repository Boundary

Do not add commercial website source, private buyer copy, private analytics
configuration, private deployment secrets, or managed-service implementation
details to this repository.
