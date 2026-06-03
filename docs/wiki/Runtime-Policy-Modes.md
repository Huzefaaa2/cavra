# Runtime Policy Modes

CAVRA now exposes explicit public-safe runtime mode summaries for Community GA
control hardening.

| Mode | Effective Behavior |
| --- | --- |
| `audit_only` | Records findings and evidence without blocking execution. |
| `enforce` | Preserves the policy decision from the runtime guard. |
| `strict` | Preserves blocks and approvals; converts allowed actions to approval-gated actions. |
| `break_glass` | Blocks unless an actor and reason are provided, then allows only with attestation. |

```bash
cavra evaluate execute_command "terraform plan" --policy-mode strict --json
```

Break-glass does not disable CAVRA. It changes the effective decision only when
the operator supplies an actor and reason, and it still requires attestation
evidence.
