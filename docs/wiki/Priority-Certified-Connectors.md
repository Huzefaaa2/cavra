# Priority Certified Connectors

CAVRA R4.2 adds a public-safe certified connector registry for the first priority provider wave. It builds on the R4.1 connector SDK and covers SCM, CI/CD, SIEM, ITSM, and ChatOps providers.

## Certified Provider Set

| Group | Providers |
| --- | --- |
| SCM | GitHub, GitLab, Azure Repos |
| CI/CD | GitHub Actions, Jenkins |
| SIEM | Splunk, Microsoft Sentinel |
| ITSM | ServiceNow, Jira |
| ChatOps | Slack, Microsoft Teams |

## What Is Implemented

- Versioned certified connector manifests under `examples/connectors/priority-certified/`.
- Built-in registry and compatibility matrix in `src/cavra/certified_connectors.py`.
- Readiness packet validator in `scripts/validate_priority_connectors.py`.
- Delivery request-spec support for GitHub, GitLab, Azure Repos, GitHub Actions, and Jenkins in addition to the existing Splunk, Sentinel, ServiceNow, Jira, Slack, and Teams paths.
- Sample and sanitized live evidence packets.
- Strict CI workflow and tests.

## Validation Commands

```bash
python3 scripts/validate_priority_connectors.py --registry
python3 scripts/validate_priority_connectors.py --manifest-dir examples/connectors/priority-certified
python3 scripts/validate_priority_connectors.py --packet examples/connectors/enterprise-priority-connectors.sample.json
python3 scripts/validate_priority_connectors.py --packet examples/connectors/enterprise-priority-connectors.live.sanitized.example.json --require-live
python3 -m pytest tests/test_certified_connectors.py -q
```

## Operating Boundary

The public repository now certifies the manifest contract, provider coverage, compatibility matrix, request-spec generation, credential redaction behavior, and readiness packet shape. Customer production use still requires tenant-specific credential custody, provider sandbox evidence, firewall allowlisting, webhook or token rotation, and support ownership records.
