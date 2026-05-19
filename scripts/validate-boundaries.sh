#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
TERMS=(
  "ENTERPRISE_PRIVATE_KEY"
  "LICENSE_SIGNING_KEY"
  "STRIPE_SECRET"
  "CUSTOMER_SECRET"
  "PRIVATE_POLICY_PACK"
  "INTERNAL_ONLY"
  "proprietary"
  "confidential"
)

SCAN_PATHS=(
  "src"
  "policies"
  "plugins"
  "docker"
  ".github"
  "examples"
)

failures=0
for term in "${TERMS[@]}"; do
  for path in "${SCAN_PATHS[@]}"; do
    [[ -e "$ROOT/$path" ]] || continue
    if grep -RIn --exclude-dir=.git --exclude='*.pyc' -- "$term" "$ROOT/$path"; then
      failures=1
    fi
  done
done

if grep -RIn --exclude-dir=.git --exclude='enterprise_hooks.py' -- "cavra_enterprise/" "$ROOT/src" "$ROOT/plugins" 2>/dev/null; then
  failures=1
fi

if [[ "$failures" -ne 0 ]]; then
  echo "CAVRA public boundary validation failed. Move private material to cavra-enterprise." >&2
  exit 1
fi

echo "CAVRA public boundary validation passed."
