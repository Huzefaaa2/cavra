# Runtime Policy Modes

CAVRA now exposes explicit public-safe runtime mode summaries for Community GA
control hardening.

## Modes

| Mode | Effective Behavior |
| --- | --- |
| `audit_only` | Records findings and evidence without blocking execution. |
| `enforce` | Preserves the policy decision from the runtime guard. |
| `strict` | Preserves blocks and approvals; converts allowed actions to approval-gated actions. |
| `break_glass` | Blocks unless an actor and reason are provided, then allows only with attestation. |

## CLI Example

```bash
cavra evaluate execute_command "terraform plan" \
  --policy-mode strict \
  --json
```

The JSON output contains:

- `schema_version`;
- requested `mode`;
- original `base_decision`;
- `effective_decision`;
- `mode_reason`;
- `evidence_required`;
- break-glass actor and reason presence when applicable.

## Break-Glass Example

```bash
cavra evaluate execute_command "terraform apply -auto-approve" \
  --policy-mode break_glass \
  --break-glass-actor incident-commander \
  --break-glass-reason "Production recovery" \
  --json
```

Break-glass does not disable CAVRA. It changes the effective decision only when
the operator supplies an actor and reason, and it still requires attestation
evidence.

## Public Boundary

The public mode summary does not include Enterprise approval-router connector
implementation, customer incidents, private approver groups, customer evidence,
or production secrets.
