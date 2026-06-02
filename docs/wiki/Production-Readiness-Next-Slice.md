# Production Readiness Next Slice

Current next slice: Trial and SaaS commercialization readiness.

## Goal

Convert CAVRA's Community adoption path into a repeatable trial, Enterprise
pilot, and future SaaS onboarding workflow without exposing Enterprise source
code, license-server logic, customer data, or SaaS secrets.

## Planned PR Sequence

1. Public trial-to-pilot intake plan.
2. Public licensing interface hardening.
3. Public SaaS Control Plane contract.
4. Private trial package readiness.
5. Private customer pilot handoff evidence.
6. Public docs/wiki sync.

## Public Boundaries

The public repository may contain trial instructions, intake templates, license
interfaces, public-safe API contracts, synthetic evidence, and documentation.

It must not contain private license validation logic, signing keys, customer
templates, private connector implementations, Enterprise source, paid policy
packs, billing secrets, or SaaS backend source.

## User Stories

- As a prospect, I can understand how to request or run a trial from the public
  repository.
- As a sales engineer, I can use a public-safe checklist to convert a trial into
  a scoped pilot.
- As a security reviewer, I can verify that commercial and customer-sensitive
  materials stay outside Community source.

## Immediate Next PR

Build the public trial-to-pilot intake plan and link it from README, roadmap,
and Enterprise trial documentation.
