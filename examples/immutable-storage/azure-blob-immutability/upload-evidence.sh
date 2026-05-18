#!/usr/bin/env bash
set -euo pipefail

: "${CAVRA_AZURE_STORAGE_ACCOUNT:?Set CAVRA_AZURE_STORAGE_ACCOUNT.}"
: "${CAVRA_AZURE_CONTAINER:?Set CAVRA_AZURE_CONTAINER.}"
: "${CAVRA_EVIDENCE_DIR:?Set CAVRA_EVIDENCE_DIR to a verified CAVRA evidence bundle directory.}"
: "${CAVRA_SESSION_ID:?Set CAVRA_SESSION_ID to the immutable evidence session prefix.}"

CAVRA_AZURE_PREFIX="${CAVRA_AZURE_PREFIX:-evidence}"
destination="${CAVRA_AZURE_PREFIX%/}/${CAVRA_SESSION_ID}"

test -f "${CAVRA_EVIDENCE_DIR}/manifest.json"
test -f "${CAVRA_EVIDENCE_DIR}/retention-policy.json"

az storage blob upload-batch \
  --account-name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
  --destination "$CAVRA_AZURE_CONTAINER" \
  --destination-path "$destination" \
  --source "$CAVRA_EVIDENCE_DIR" \
  --auth-mode login \
  --overwrite false

az storage blob show \
  --account-name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
  --container-name "$CAVRA_AZURE_CONTAINER" \
  --name "${destination}/manifest.json" \
  --auth-mode login \
  --query '{etag:properties.etag, versionId:properties.versionId, lastModified:properties.lastModified}'

echo "CAVRA evidence uploaded to immutable Azure prefix: https://${CAVRA_AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/${CAVRA_AZURE_CONTAINER}/${destination}/"
