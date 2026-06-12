# Hosted Sandbox Operator Release Status

Status: ready

This public-safe packet gives release operators one place to decide whether the
hosted AISPM portal can be shared with external evaluators or announced more
widely.

## Portal Packet

The AISPM dashboard renders Hosted Release Operator Status and can copy or
download `cavra-hosted-sandbox-operator-status-packet.json`.

## Operator Checks

| Check | Status | Validator |
| --- | --- | --- |
| Local portal freshness | ready | `python scripts/validate-hosted-sandbox-deployment-freshness.py` |
| Live Pages freshness | requires_deploy_validation | `CAVRA_CHECK_LIVE_SANDBOX=true python scripts/validate-hosted-sandbox-deployment-freshness.py` |
| Hosted browser smoke | workflow_enforced | `npm run validate:sandbox:hosted` |
| Post-deploy evidence | workflow_enforced | `python scripts/validate-hosted-sandbox-deploy-evidence.py` |
| Announcement gate | blocked_until_live_freshness_passes | Hosted Release Operator Status |

## Validation

```bash
python scripts/validate-hosted-sandbox-operator-status.py
```

## Public Safety Boundary

This status packet includes public deployment markers, validator names, and
operator go/no-go status only. It excludes customer data, raw prompts, private
package credentials, license secrets, Enterprise source code, and tenant
telemetry.
