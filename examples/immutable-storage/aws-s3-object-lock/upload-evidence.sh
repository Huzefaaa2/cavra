#!/usr/bin/env bash
set -euo pipefail

: "${CAVRA_AWS_BUCKET:?Set CAVRA_AWS_BUCKET to the evidence bucket name.}"
: "${CAVRA_AWS_KMS_KEY_ID:?Set CAVRA_AWS_KMS_KEY_ID to the KMS key used for evidence encryption.}"
: "${CAVRA_EVIDENCE_DIR:?Set CAVRA_EVIDENCE_DIR to a verified CAVRA evidence bundle directory.}"
: "${CAVRA_SESSION_ID:?Set CAVRA_SESSION_ID to the immutable evidence session prefix.}"

CAVRA_S3_PREFIX="${CAVRA_S3_PREFIX:-evidence/}"
destination="s3://${CAVRA_AWS_BUCKET}/${CAVRA_S3_PREFIX%/}/${CAVRA_SESSION_ID}/"

test -f "${CAVRA_EVIDENCE_DIR}/manifest.json"
test -f "${CAVRA_EVIDENCE_DIR}/retention-policy.json"

aws s3 sync "${CAVRA_EVIDENCE_DIR}/" "$destination" \
  --sse aws:kms \
  --sse-kms-key-id "$CAVRA_AWS_KMS_KEY_ID" \
  --exact-timestamps

aws s3api head-object \
  --bucket "$CAVRA_AWS_BUCKET" \
  --key "${CAVRA_S3_PREFIX%/}/${CAVRA_SESSION_ID}/manifest.json" \
  --query '{mode:ObjectLockMode, retain_until:ObjectLockRetainUntilDate, kms:SSEKMSKeyId}'

echo "CAVRA evidence uploaded to immutable S3 prefix: $destination"
