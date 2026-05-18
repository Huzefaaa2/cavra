# CAVRA Immutable Evidence Store: Azure Blob Storage

This reference deploys an Azure Blob container for CAVRA evidence bundles using blob versioning, HTTPS-only access, public-access blocking, and a locked time-based immutability policy.

Use it for regulated evidence archives where CAVRA evidence bundles must be retained in a WORM posture.

## Files

- `variables.example.env`: environment variables for the deployment scripts.
- `deploy.sh`: creates or configures the storage account, container, and immutability policy.
- `upload-evidence.sh`: uploads a CAVRA evidence bundle into a session-scoped prefix.

## Deploy

```bash
cp variables.example.env .env
source .env
bash deploy.sh
```

The script creates a storage account, enables blob versioning, creates the evidence container, creates a time-based immutability policy, and locks the policy. Test with a non-production resource group before locking a production retention policy.

## Upload Evidence

```bash
source .env
export CAVRA_EVIDENCE_DIR=.cavra/evidence/latest
export CAVRA_SESSION_ID=release-2026-05-18
bash upload-evidence.sh
```

Run CAVRA verification before upload:

```bash
cavra evidence verify "$CAVRA_EVIDENCE_DIR" \
  --trust-root .cavra/keys/evidence-trust-roots.json \
  --key-id prod-evidence \
  --minimum-retention-days "$CAVRA_RETENTION_DAYS"
```

## Enterprise Controls

- Container immutability policy is locked after creation.
- Blob versioning is enabled.
- Public blob access is disabled.
- HTTPS-only access and minimum TLS 1.2 are enforced.
- Uploaded evidence is organized by immutable session prefix.
- Optional legal hold tags can be applied with `CAVRA_AZURE_LEGAL_HOLD_TAGS`.

## Operator Notes

Locked Azure time-based immutability policies protect data from overwrite and deletion until the retention period expires. Do not lock production policies until retention requirements have been reviewed by security, legal, and records management.
