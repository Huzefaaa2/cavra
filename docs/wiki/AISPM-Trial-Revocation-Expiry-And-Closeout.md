# AISPM Trial Revocation, Expiry, And Closeout

This public-safe lab defines how CAVRA Enterprise Trial closeout should be
verified. It focuses on the evaluator experience, operator evidence, and
blocked-access expectations after trial expiry or revocation.

The private Enterprise implementation owns real license validation, package
registry revocation, trial portal enforcement, support queue closure, and
immutable audit storage.

## Closeout Scenarios

| Scenario | Expected Result |
| --- | --- |
| Natural expiry | The trial license stops validating after the approved evaluation window. |
| Operator revocation | Package access, portal access, and license validation are blocked after revocation. |
| Support closeout | Support handoff moves to closed or follow-up state. |
| Evidence closeout | Redacted closeout evidence is available for operator and customer-success review. |

## Blocked-Access Checks

- License validation rejects expired or revoked trials.
- Private package pull fails after access is removed.
- Trial portal access no longer exposes evaluator-specific package guidance.
- Enterprise report rendering is disabled for the revoked or expired trial.
- Support handoff is closed or marked for follow-up.

## Evidence Expectations

| Evidence | Public-Safe Requirement |
| --- | --- |
| Revocation event | Include timestamp and opaque event ref only. |
| License block | Include blocked state and evidence ref, not the license key. |
| Package block | Include blocked state, not package token or private URL. |
| Portal block | Include status only, not evaluator identity or IP address. |
| Support closeout | Include closeout state, not private support transcript. |
| Audit archive | Include immutable archive status and evidence ref only. |
| Release validator | Include blocked/ready status, not private workflow logs or package credentials. |

## Operator Closeout Checklist

1. Confirm the trial access state is expired or revoked.
2. Confirm the license service blocks validation.
3. Confirm package access is removed.
4. Confirm trial portal access is blocked or downgraded.
5. Confirm support handoff is closed or assigned for follow-up.
6. Confirm operator audit archive retention evidence remains available.
7. Confirm release validators would block any stale or incomplete readiness
   packet before a new trial package is announced.
8. Export a redacted closeout evidence packet.

## Verification Checkpoints

| Checkpoint | Expected Result |
| --- | --- |
| `checkpoint-revocation-expiry` | Trial license validation, package pull, portal access, report rendering, and support handoff are blocked after revocation or expiry. |

## Public Safety Rules

Do not publish license keys, package URLs, package tokens, evaluator identity,
operator identity, IP addresses, private support records, provider responses,
raw prompts, model reasoning, raw tool output, customer records, or Enterprise
source code.

## Related Contracts

- `src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json`
- `src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json`
- `src/cavra/schemas/aispm-report-center-trial-lab-notebook-publication-readiness.schema.json`

## Related Pages

- [CAVRA Trial Field Guide](CAVRA-Trial-Field-Guide)
- [Trial Access And Operator Approval](AISPM-Trial-Access-And-Operator-Approval)
- [AISPM Report Center Enterprise Readiness](AISPM-Report-Center-Enterprise-Readiness)
