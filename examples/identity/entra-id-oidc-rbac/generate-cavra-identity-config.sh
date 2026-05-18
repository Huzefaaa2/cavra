#!/usr/bin/env bash
set -euo pipefail

: "${CAVRA_ENTRA_TENANT_ID:?Set CAVRA_ENTRA_TENANT_ID to the Entra tenant ID.}"
: "${CAVRA_ENTRA_AUDIENCE:?Set CAVRA_ENTRA_AUDIENCE to the expected token audience.}"

CAVRA_IDENTITY_OUTPUT_DIR="${CAVRA_IDENTITY_OUTPUT_DIR:-.cavra/identity/entra}"
CAVRA_CONSOLE_ORIGIN="${CAVRA_CONSOLE_ORIGIN:-https://cavra-console.example.com}"
CAVRA_REPOSITORY="${CAVRA_REPOSITORY:-payments/api}"
CAVRA_APPROVER_GROUP="${CAVRA_APPROVER_GROUP:-IAM}"
CAVRA_ENTRA_IAM_GROUP_ID="${CAVRA_ENTRA_IAM_GROUP_ID:-00000000-0000-0000-0000-000000000001}"
CAVRA_ENTRA_PLATFORM_GROUP_ID="${CAVRA_ENTRA_PLATFORM_GROUP_ID:-00000000-0000-0000-0000-000000000002}"
CAVRA_ENTRA_CAB_GROUP_ID="${CAVRA_ENTRA_CAB_GROUP_ID:-00000000-0000-0000-0000-000000000003}"

mkdir -p "$CAVRA_IDENTITY_OUTPUT_DIR"

metadata_url="https://login.microsoftonline.com/${CAVRA_ENTRA_TENANT_ID}/v2.0/.well-known/openid-configuration"
metadata_file="${CAVRA_IDENTITY_OUTPUT_DIR}/openid-configuration.json"
jwks_file="${CAVRA_IDENTITY_OUTPUT_DIR}/approval-jwks.json"
oidc_file="${CAVRA_IDENTITY_OUTPUT_DIR}/approval-oidc.json"
rbac_file="${CAVRA_IDENTITY_OUTPUT_DIR}/approval-rbac.yaml"
env_file="${CAVRA_IDENTITY_OUTPUT_DIR}/cavra-identity.env"

curl --fail --silent --show-error --location "$metadata_url" --output "$metadata_file"

python3 - "$metadata_file" "$jwks_file" "$oidc_file" "$CAVRA_ENTRA_AUDIENCE" "$metadata_url" <<'PY'
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
    "provider": "entra_id",
    "metadata_url": metadata_url,
}
oidc_path.write_text(json.dumps(oidc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

cat > "$rbac_file" <<YAML
approval_rbac:
  group_mappings:
    ${CAVRA_ENTRA_IAM_GROUP_ID}: ${CAVRA_APPROVER_GROUP}
    ${CAVRA_ENTRA_PLATFORM_GROUP_ID}: Platform Security
    ${CAVRA_ENTRA_CAB_GROUP_ID}: Change Advisory Board
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

echo "Generated CAVRA Entra OIDC/RBAC files in ${CAVRA_IDENTITY_OUTPUT_DIR}"
echo "Source ${env_file} before starting the CAVRA API."
