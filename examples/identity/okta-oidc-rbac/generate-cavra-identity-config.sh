#!/usr/bin/env bash
set -euo pipefail

: "${CAVRA_OKTA_ISSUER:?Set CAVRA_OKTA_ISSUER to the Okta issuer URL.}"
: "${CAVRA_OKTA_AUDIENCE:?Set CAVRA_OKTA_AUDIENCE to the expected token audience.}"

CAVRA_IDENTITY_OUTPUT_DIR="${CAVRA_IDENTITY_OUTPUT_DIR:-.cavra/identity/okta}"
CAVRA_CONSOLE_ORIGIN="${CAVRA_CONSOLE_ORIGIN:-https://cavra-console.example.com}"
CAVRA_REPOSITORY="${CAVRA_REPOSITORY:-payments/api}"
CAVRA_APPROVER_GROUP="${CAVRA_APPROVER_GROUP:-IAM}"
CAVRA_OKTA_IAM_GROUP="${CAVRA_OKTA_IAM_GROUP:-CAVRA-IAM-Approvers}"
CAVRA_OKTA_PLATFORM_GROUP="${CAVRA_OKTA_PLATFORM_GROUP:-CAVRA-Platform-Security}"
CAVRA_OKTA_CAB_GROUP="${CAVRA_OKTA_CAB_GROUP:-CAVRA-Change-Advisory-Board}"

mkdir -p "$CAVRA_IDENTITY_OUTPUT_DIR"

issuer="${CAVRA_OKTA_ISSUER%/}"
metadata_url="${issuer}/.well-known/openid-configuration"
metadata_file="${CAVRA_IDENTITY_OUTPUT_DIR}/openid-configuration.json"
jwks_file="${CAVRA_IDENTITY_OUTPUT_DIR}/approval-jwks.json"
oidc_file="${CAVRA_IDENTITY_OUTPUT_DIR}/approval-oidc.json"
rbac_file="${CAVRA_IDENTITY_OUTPUT_DIR}/approval-rbac.yaml"
env_file="${CAVRA_IDENTITY_OUTPUT_DIR}/cavra-identity.env"

curl --fail --silent --show-error --location "$metadata_url" --output "$metadata_file"

python3 - "$metadata_file" "$jwks_file" "$oidc_file" "$CAVRA_OKTA_AUDIENCE" "$metadata_url" <<'PY'
import json
import sys
from pathlib import Path
from urllib.request import urlopen

metadata_path = Path(sys.argv[1])
jwks_path = Path(sys.argv[2])
oidc_path = Path(sys.argv[3])
audience = sys.argv[4]
metadata_url = sys.argv[5]

metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
jwks_uri = metadata["jwks_uri"]
with urlopen(jwks_uri, timeout=30) as response:
    jwks = json.loads(response.read().decode("utf-8"))
jwks_path.write_text(json.dumps(jwks, indent=2, sort_keys=True) + "\n", encoding="utf-8")
oidc = {
    "issuer": metadata["issuer"],
    "audience": audience,
    "jwks_path": jwks_path.name,
    "leeway_seconds": 60,
    "provider": "okta",
    "metadata_url": metadata_url,
}
oidc_path.write_text(json.dumps(oidc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

cat > "$rbac_file" <<YAML
approval_rbac:
  group_mappings:
    ${CAVRA_OKTA_IAM_GROUP}: ${CAVRA_APPROVER_GROUP}
    ${CAVRA_OKTA_PLATFORM_GROUP}: Platform Security
    ${CAVRA_OKTA_CAB_GROUP}: Change Advisory Board
  repository_permissions:
    - repository: ${CAVRA_REPOSITORY}
      approver_group: ${CAVRA_APPROVER_GROUP}
      groups:
        - ${CAVRA_APPROVER_GROUP}
      actions:
        - approved
        - denied
    - repository: ${CAVRA_REPOSITORY}
      approver_group: Platform Security
      groups:
        - Platform Security
      actions:
        - approved
        - denied
        - expired
YAML

cat > "$env_file" <<ENV
export CAVRA_APPROVAL_OIDC_CONFIG=${oidc_file}
export CAVRA_APPROVAL_RBAC_FILE=${rbac_file}
export CAVRA_CORS_ORIGINS=${CAVRA_CONSOLE_ORIGIN}
ENV

echo "Generated CAVRA Okta OIDC/RBAC files in ${CAVRA_IDENTITY_OUTPUT_DIR}"
echo "Source ${env_file} before starting the CAVRA API."
