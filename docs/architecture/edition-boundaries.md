# CAVRA Edition Boundaries

CAVRA uses an open-core model. This public repository is the Community Edition
and public product landing repository. It may contain public documentation for
Enterprise, Trial, and SaaS, but it must not contain their private source code.

## Community Edition

Community belongs in this public repository:

- core runtime policy evaluation;
- local CLI and MCP integration;
- starter policy packs;
- public examples and GitHub Actions templates;
- public evidence bundle formats;
- public plugin runtime interfaces;
- public edition, licensing, and feature abstractions;
- public documentation and community Docker build.

Community must run without a license key.

## Enterprise Edition

Enterprise belongs in a private repository such as `cavra-enterprise`:

- SSO and enterprise identity connectors;
- advanced RBAC;
- central dashboards;
- paid audit exports and compliance report implementations;
- private policy packs;
- organization-wide enforcement;
- drift monitoring;
- AI remediation recommendations;
- enterprise-only plugins;
- enterprise Docker images, Helm charts, and support tooling.

The public repo may contain documentation and safe hooks only.

## Trial Edition

Trial distribution should be a private binary, private Docker image, or hosted
SaaS trial. The public repo may document installation and license activation,
but must not include trial bypass logic, signing keys, license-server code, or
enterprise source.

## SaaS Control Plane

The SaaS backend belongs in private infrastructure and private repositories:

- tenant management;
- billing integration;
- license service;
- hosted policy registry;
- hosted audit store;
- dashboards;
- compliance exports;
- AI recommendation services.

The public repo may document API boundaries and future integration contracts.

## Never Public

Do not commit:

- enterprise source code;
- proprietary algorithms;
- license validation secrets or signing keys;
- SaaS backend secrets;
- paid policy pack source;
- private customer templates;
- customer data;
- internal-only operational runbooks;
- private commercial roadmap details;
- production credentials or private keys.
