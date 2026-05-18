#!/usr/bin/env bash
set -euo pipefail

: "${CAVRA_AZURE_RESOURCE_GROUP:?Set CAVRA_AZURE_RESOURCE_GROUP.}"
: "${CAVRA_AZURE_STORAGE_ACCOUNT:?Set CAVRA_AZURE_STORAGE_ACCOUNT.}"

CAVRA_AZURE_LOCATION="${CAVRA_AZURE_LOCATION:-eastus}"
CAVRA_AZURE_CONTAINER="${CAVRA_AZURE_CONTAINER:-evidence}"
CAVRA_RETENTION_DAYS="${CAVRA_RETENTION_DAYS:-2555}"
CAVRA_AZURE_LEGAL_HOLD_TAGS="${CAVRA_AZURE_LEGAL_HOLD_TAGS:-}"

az group create \
  --name "$CAVRA_AZURE_RESOURCE_GROUP" \
  --location "$CAVRA_AZURE_LOCATION"

az storage account create \
  --resource-group "$CAVRA_AZURE_RESOURCE_GROUP" \
  --name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
  --location "$CAVRA_AZURE_LOCATION" \
  --kind StorageV2 \
  --sku Standard_GRS \
  --https-only true \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false

az storage account blob-service-properties update \
  --resource-group "$CAVRA_AZURE_RESOURCE_GROUP" \
  --account-name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
  --enable-versioning true \
  --enable-change-feed true \
  --enable-delete-retention true \
  --delete-retention-days "$CAVRA_RETENTION_DAYS" \
  --enable-container-delete-retention true \
  --container-delete-retention-days "$CAVRA_RETENTION_DAYS"

az storage container create \
  --account-name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
  --name "$CAVRA_AZURE_CONTAINER" \
  --auth-mode login \
  --public-access off

policy_etag="$(az storage container immutability-policy create \
  --account-name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
  --container-name "$CAVRA_AZURE_CONTAINER" \
  --period "$CAVRA_RETENTION_DAYS" \
  --allow-protected-append-writes false \
  --auth-mode login \
  --query etag \
  --output tsv)"

az storage container immutability-policy lock \
  --account-name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
  --container-name "$CAVRA_AZURE_CONTAINER" \
  --if-match "$policy_etag" \
  --auth-mode login

if [ -n "$CAVRA_AZURE_LEGAL_HOLD_TAGS" ]; then
  az storage container legal-hold set \
    --account-name "$CAVRA_AZURE_STORAGE_ACCOUNT" \
    --container-name "$CAVRA_AZURE_CONTAINER" \
    --tags "$CAVRA_AZURE_LEGAL_HOLD_TAGS" \
    --auth-mode login
fi

echo "CAVRA immutable evidence container configured: https://${CAVRA_AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/${CAVRA_AZURE_CONTAINER}"
