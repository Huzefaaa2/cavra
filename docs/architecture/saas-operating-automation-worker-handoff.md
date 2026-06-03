# SaaS Operating Automation Worker Handoff

This public Community document defines how future private Enterprise/SaaS
automation worker handoff packages should connect to the public SaaS operating
automation contract. It is interface guidance only. It does not implement
automation workers, schedulers, connectors, billing checks, support workflows,
customer-success workflows, dashboard refresh jobs, closeout retry jobs, or
SaaS backend services.

## Purpose

After the public `saas_operating_automation` contract returns
`requires_private_service`, a private Enterprise or SaaS package can use the
request as the public-safe input for worker handoff. The private package owns
runtime execution, scheduler registration, connector delivery, tenant
resolution, retry policies, evidence sinks, support workflow integration, and
customer-success system integration.

Community Edition may document the handoff shape and validate public-safe
metadata. Enterprise implementation remains private.

## Public-Safe Handoff Metadata

Future public-safe handoff packages may summarize:

- tenant alias or public tenant reference;
- source operation, such as `saas_operating_automation`;
- approved required checks;
- worker target names;
- deployment environment label;
- scheduler reference label;
- evidence sink reference label;
- retry policy reference label;
- owning team or role;
- handoff status, such as `planned`, `ready`, `blocked`, or
  `requires_private_service`;
- boundary message.

## Private Responsibilities

Private Enterprise or SaaS packages must own:

- automation worker source code;
- scheduler implementation and runtime queues;
- billing-provider API calls and billing records;
- license telemetry job implementation and telemetry payloads;
- support ticket workflows and ticket contents;
- customer-success records and customer health scores;
- dashboard refresh jobs and production dashboard URLs;
- escalation drill runbooks, on-call routing, and webhooks;
- closeout retry execution;
- connector credentials, tokens, and endpoint URLs;
- customer identifiers beyond public-safe aliases;
- SaaS backend implementation and secrets.

## Public Boundary Rules

Community documentation and tests may include:

- interface names;
- public-safe field names;
- synthetic examples;
- status vocabulary;
- validation expectations;
- private-service boundary messages.

Community documentation and tests must not include:

- Enterprise source code;
- private package paths;
- SaaS backend source or deployment topology;
- worker execution algorithms;
- scheduler internals;
- connector credentials or production endpoint URLs;
- customer records, support tickets, billing records, or customer-success notes;
- compliance workpapers, executive notes, incident contents, or rollback runbooks;
- license keys, signing keys, paid policy packs, or private policy registry logic.

## Recommended Private Package Flow

1. Read the public `saas_operating_automation` request.
2. Verify the public request shape and required checks.
3. Resolve tenant and customer systems inside the private package.
4. Register or update private worker targets for each required check.
5. Attach private scheduler, retry policy, and evidence sink references.
6. Emit public-safe handoff metadata for release review.
7. Keep worker code, credentials, customer payloads, and SaaS implementation
   outside the public repository.

## User Stories

- As a platform engineer, I can build a private worker package against a stable
  public handoff vocabulary.
- As a security architect, I can verify that Community docs explain the
  integration boundary without leaking private implementation.
- As a release manager, I can understand which worker handoff metadata is safe
  to reference in public release notes.
- As a customer-success owner, I can see which operating checks need private
  worker coverage without exposing customer records.

## Enterprise Challenge Solved

Enterprises need a clean bridge between public product contracts and private
automation execution. This guidance lets CAVRA explain the product integration
model publicly while keeping all operational execution, credentials, customer
records, and commercial systems private.

## Next Recommendation

Add a public-safe worker handoff contract model to Community Edition so API,
CLI, tests, and the Evidence Console can describe the handoff metadata shape
without executing private workers or exposing Enterprise implementation.
