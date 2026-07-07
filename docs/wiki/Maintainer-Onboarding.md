# CAVRA Maintainer Onboarding

Last updated: 2026-07-07

This playbook turns CAVRA maintainer onboarding into a repeatable, auditable process. It is the operating companion to [Maintainer Governance](maintainer-governance.md) and [RFC Process](rfc-process.md).

The repository can be marked ready for multi-maintainer governance when this playbook, CODEOWNERS, RFC rules, release cadence, PR review expectations, and Phase 1 governance tests are present. Assigning additional named maintainers remains a repository administration action.

## Onboarding Stages

| Stage | Outcome | Evidence |
| --- | --- | --- |
| Candidate | Candidate is nominated for a bounded ownership area. | Issue or maintainer note referencing the area. |
| Shadow reviewer | Candidate reviews low-risk docs, tests, or examples without merge authority. | Review links and maintainer feedback. |
| Area reviewer | Candidate reviews one CODEOWNERS area with maintainer approval. | CODEOWNERS update proposal and successful review history. |
| Area maintainer | Candidate can approve bounded changes in the assigned area. | CODEOWNERS entry and governance acknowledgement. |
| Release/security maintainer | Candidate can approve release, security, or evidence-sensitive changes. | Release rehearsal, security walkthrough, and explicit maintainer approval. |

## Required Reading

Before receiving a CODEOWNERS assignment, a candidate must read:

- `SECURITY.md`;
- `docs/vulnerability-disclosure.md`;
- `docs/release-security-advisories.md`;
- `docs/release-trust-checklist.md`;
- `docs/api-versioning-and-openapi.md`;
- `docs/governance/maintainer-governance.md`;
- `docs/governance/rfc-process.md`;
- `docs/governance/release-cadence.md`;
- `docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md`.

## Required Validation

The candidate or sponsoring maintainer must run:

```bash
python3 scripts/validate_release_security.py
python3 scripts/validate_openapi_contract.py
python3 scripts/validate_release_trust_gate.py
python3 -m pytest tests/test_phase1_trust_governance.py -q
```

For area-specific assignments, also run the tests for that area.

## Public-Safety Rules

Maintainers must not approve public changes that include:

- private customer names or identifiers;
- production secrets, tokens, private keys, SMTP credentials, or connector credentials;
- raw customer evidence, raw model artifacts, private runtime traces, or proprietary prompts;
- Enterprise-private source code in the public Community repository;
- unsupported compliance, legal, pricing, or SLA claims.

## CODEOWNERS Update Rules

CODEOWNERS updates must:

1. limit the maintainer to a bounded area at first;
2. include the candidate's completed onboarding evidence;
3. keep security-sensitive paths covered by a Project Maintainer and Security Maintainer;
4. be reviewed by the current Project Maintainer;
5. be linked from the relevant roadmap or governance issue.

## Graduation Criteria

A candidate can graduate from reviewer to area maintainer when:

- the required reading is acknowledged;
- the required validation passes;
- at least two successful reviews are completed in the target area;
- no public-safety violations were introduced;
- the sponsoring maintainer approves the bounded CODEOWNERS assignment.

## R1.2 Completion Boundary

R1.2 is complete when CAVRA has:

- CODEOWNERS coverage for public source, docs, workflows, scripts, and product surfaces;
- documented maintainer roles and security-sensitive review classes;
- this onboarding playbook;
- documented RFC process;
- documented release cadence;
- PR template prompts for validation, docs, risk, rollback, and follow-up;
- Phase 1 governance tests covering the public artifacts.

Adding more named maintainers is an operating action that uses this process. It does not block the public roadmap item once the process and enforcement hooks are present.

