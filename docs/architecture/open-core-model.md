# Open-Core Model

CAVRA Community Edition remains publicly available in `Huzefaaa2/cavra`.
Enterprise Edition, Trial delivery logic, paid policy packs, license service,
and SaaS backend should live outside this public repository.

## Public Repository

The public repository contains:

- Community source code;
- public documentation;
- Enterprise feature documentation;
- trial installation instructions;
- references to trial binaries or private container images;
- extension interfaces for private packages.

## Private Repositories

Recommended private repository:

- `Huzefaaa2/cavra-enterprise`

Future private repositories may include:

- `cavra-saas-control-plane`;
- `cavra-commercial-policy-packs`;
- `cavra-enterprise-deployments`.

## Licensing Options

Possible licensing options:

- AGPL for strong open-source reciprocity;
- Business Source License for delayed open conversion;
- dual commercial license for Enterprise customers;
- proprietary Enterprise license for private modules.

Final license choice requires legal review.

## Commercial Packaging

Community should be easy to install and useful on its own. Enterprise should be
installed as a private package, private container image, Helm chart, or hosted
SaaS connection. Trial should use a time-limited license key or hosted license
validation flow implemented outside this repository.
