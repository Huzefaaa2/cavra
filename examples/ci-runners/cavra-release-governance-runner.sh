#!/usr/bin/env bash
set -euo pipefail

runtime_path="${CAVRA_RUNTIME_PATH:-cavra-runtime}"
request_path="${CAVRA_RELEASE_GOVERNANCE_REQUEST:?CAVRA_RELEASE_GOVERNANCE_REQUEST is required}"
expected_decision="${CAVRA_EXPECTED_DECISION:-allow}"
expected_rule_id="${CAVRA_EXPECTED_RULE_ID:-}"
allow_blocking_decision="${CAVRA_ALLOW_BLOCKING_DECISION:-false}"
evidence_dir="${CAVRA_RELEASE_GOVERNANCE_EVIDENCE_DIR:-.cavra/go-daemon}"
socket_path="${CAVRA_RUNTIME_SOCKET:-${evidence_dir}/cavra-runtime.sock}"
evidence_log="${CAVRA_RUNTIME_EVIDENCE_LOG:-${evidence_dir}/release-governance-evidence.jsonl}"
response_path="${CAVRA_RELEASE_GOVERNANCE_RESPONSE:-${evidence_dir}/release-governance-response.json}"

mkdir -p "${evidence_dir}"

"${runtime_path}" \
  --lifecycle start \
  --socket "${socket_path}" \
  --evidence-log "${evidence_log}"
trap '"${runtime_path}" --lifecycle stop --socket "${socket_path}" || true' EXIT

"${runtime_path}" \
  --daemon \
  --socket "${socket_path}" \
  --input "${request_path}" \
  > "${response_path}"

python3 - "${response_path}" "${expected_decision}" "${expected_rule_id}" "${allow_blocking_decision}" <<'PY'
import json
import pathlib
import sys

response_path = pathlib.Path(sys.argv[1])
expected_decision = sys.argv[2]
expected_rule = sys.argv[3]
allow_block = sys.argv[4].lower() == "true"

response = json.loads(response_path.read_text(encoding="utf-8"))
actual_decision = response.get("decision")
actual_rule = response.get("rule_id")

if actual_decision != expected_decision:
    raise SystemExit(f"unexpected CAVRA decision: {actual_decision} != {expected_decision}")
if expected_rule and actual_rule != expected_rule:
    raise SystemExit(f"unexpected CAVRA rule_id: {actual_rule} != {expected_rule}")
if actual_decision == "block" and not allow_block:
    raise SystemExit(response.get("reason", "CAVRA blocked release governance request"))
PY
