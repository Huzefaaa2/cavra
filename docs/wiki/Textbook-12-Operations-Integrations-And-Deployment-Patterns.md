# Operations, Integrations, And Deployment Patterns

CAVRA can run locally, inside CI/CD, next to a hosted API, or as part of an Enterprise control plane. The right pattern depends on scope.

## Local Pattern

Use local mode for learning, policy authoring, demos, and repository-specific workflows.

```bash
cavra evaluate write_file src/example.py --json
cavra evidence bundle --output .cavra/evidence/latest
```

## CI/CD Pattern

Use CI/CD when CAVRA decisions should become required checks. The workflow normally:

1. Evaluates proposed changes.
2. Generates evidence.
3. Verifies evidence or PR attestation.
4. Blocks merge or deployment if the gate fails.

## API Pattern

Use the API when multiple clients need a shared decision or evidence surface. The sandbox UI can query the API for backend-driven scenario runs, session history, decision records, approvals, registry data, and evidence metadata.

## Enterprise Connector Pattern

Use live connectors for production operations:

- SIEM export.
- ITSM ticketing.
- ChatOps notifications.
- SMTP or report provider delivery.
- Cloud and endpoint inventory ingestion.
- Private queue handoff.
- Managed release and rollback evidence.

All connector outputs should redact credentials and record delivery evidence.

## Tenant Pattern

Enterprise tenant isolation requires separate identity context, entitlement status, policy assignment, audit stores, and report delivery records. Tenant boundaries must be tested with live validation before production.

## Runtime Workflow Pattern

Runtime workflow validation should test actual agent and tool behavior, not only synthetic payloads. Production readiness requires proving that real workflows pass through CAVRA and that bypass paths are blocked or detected.

## Operating Review Pattern

Post-GA operations should include:

- Publication validation.
- First-wave activation readiness.
- Customer-success operating review.
- Security advisory drill closeout.
- GA operating archive closeout.
- Final docs and status sync.

Historical records for these operating chains are stored in [Development And Testing Artifacts](Development-And-Testing-Artifacts/Index).
