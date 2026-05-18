# CAVRA Immutable Evidence Store: AWS S3 Object Lock

This reference deploys an S3 bucket for CAVRA evidence bundles using Object Lock, versioning, KMS encryption, public-access blocking, and default retention.

Use it for regulated evidence archives where CAVRA evidence bundles must be retained in a WORM posture.

## Files

- `variables.example.env`: environment variables for the deployment scripts.
- `deploy.sh`: creates or configures the Object Lock bucket.
- `upload-evidence.sh`: uploads a CAVRA evidence bundle into a session-scoped prefix.

## Deploy

```bash
cp variables.example.env .env
source .env
bash deploy.sh
```

Object Lock must be enabled when the bucket is created. For production archives, create a new bucket rather than reusing a mutable bucket.

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

- S3 Object Lock default retention mode is `COMPLIANCE` by default.
- Bucket versioning is enabled.
- KMS encryption is required for uploads.
- Public access is blocked.
- Non-TLS requests are denied.
- Uploaded evidence is organized by immutable session prefix.

## Operator Notes

Compliance-mode Object Lock retention cannot be shortened or removed by normal users, including the root user, during the retention period. Test with `GOVERNANCE` mode in a non-production account before creating a production `COMPLIANCE` archive.
