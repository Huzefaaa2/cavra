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
runner_claims_path="${CAVRA_RUNNER_AUTH_CLAIMS:-${evidence_dir}/runner-auth-claims.json}"
runner_auth_key_id="${CAVRA_RUNNER_AUTH_KEY_ID:-}"
evidence_key_id="${CAVRA_DAEMON_EVIDENCE_KEY_ID:-}"

mkdir -p "${evidence_dir}"

# Optional hardening:
# - CAVRA_RUNNER_AUTH_HMAC_KEY signs runner identity claims for daemon authentication.
# - CAVRA_DAEMON_EVIDENCE_HMAC_KEY signs the chained daemon evidence JSONL stream.

python3 - "${runner_claims_path}" <<'PY'
import json
import os
import pathlib
import sys

provider = os.environ.get("CAVRA_RUNNER_PROVIDER", "")
if not provider:
    if os.environ.get("GITHUB_ACTIONS"):
        provider = "github-actions"
    elif os.environ.get("GITLAB_CI"):
        provider = "gitlab-ci"
    elif os.environ.get("TF_BUILD"):
        provider = "azure-pipelines"
    else:
        provider = "local"

claims = {
    "provider": provider,
    "repository": (
        os.environ.get("CAVRA_RUNNER_REPOSITORY")
        or os.environ.get("GITHUB_REPOSITORY")
        or os.environ.get("CI_PROJECT_PATH")
        or os.environ.get("BUILD_REPOSITORY_NAME")
        or "local"
    ),
    "workflow": (
        os.environ.get("CAVRA_RUNNER_WORKFLOW")
        or os.environ.get("GITHUB_WORKFLOW")
        or os.environ.get("CI_PIPELINE_SOURCE")
        or os.environ.get("BUILD_DEFINITIONNAME")
        or "local"
    ),
    "run_id": (
        os.environ.get("CAVRA_RUNNER_RUN_ID")
        or os.environ.get("GITHUB_RUN_ID")
        or os.environ.get("CI_PIPELINE_ID")
        or os.environ.get("BUILD_BUILDID")
        or ""
    ),
    "run_attempt": (
        os.environ.get("CAVRA_RUNNER_RUN_ATTEMPT")
        or os.environ.get("GITHUB_RUN_ATTEMPT")
        or os.environ.get("CI_JOB_ID")
        or os.environ.get("SYSTEM_JOBATTEMPT")
        or ""
    ),
    "ref": (
        os.environ.get("CAVRA_RUNNER_REF")
        or os.environ.get("GITHUB_REF")
        or os.environ.get("CI_COMMIT_REF_NAME")
        or os.environ.get("BUILD_SOURCEBRANCH")
        or ""
    ),
    "sha": (
        os.environ.get("CAVRA_RUNNER_SHA")
        or os.environ.get("GITHUB_SHA")
        or os.environ.get("CI_COMMIT_SHA")
        or os.environ.get("BUILD_SOURCEVERSION")
        or ""
    ),
    "actor": (
        os.environ.get("CAVRA_RUNNER_ACTOR")
        or os.environ.get("GITHUB_ACTOR")
        or os.environ.get("GITLAB_USER_LOGIN")
        or os.environ.get("BUILD_REQUESTEDFOR")
        or ""
    ),
    "job": (
        os.environ.get("CAVRA_RUNNER_JOB")
        or os.environ.get("GITHUB_JOB")
        or os.environ.get("CI_JOB_NAME")
        or os.environ.get("SYSTEM_JOBDISPLAYNAME")
        or ""
    ),
    "runner_name": (
        os.environ.get("CAVRA_RUNNER_NAME")
        or os.environ.get("RUNNER_NAME")
        or os.environ.get("CI_RUNNER_DESCRIPTION")
        or os.environ.get("AGENT_NAME")
        or ""
    ),
}
pathlib.Path(sys.argv[1]).write_text(json.dumps(claims, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

start_args=(
  --lifecycle start
  --socket "${socket_path}"
  --evidence-log "${evidence_log}"
)
if [ -n "${evidence_key_id}" ]; then
  start_args+=(--evidence-signing-key-id "${evidence_key_id}")
fi
if [ -n "${runner_auth_key_id}" ]; then
  start_args+=(--runner-auth-key-id "${runner_auth_key_id}")
fi

"${runtime_path}" "${start_args[@]}"
trap '"${runtime_path}" --lifecycle stop --socket "${socket_path}" || true' EXIT

client_args=(
  --daemon
  --socket "${socket_path}"
  --input "${request_path}"
)
if [ -n "${CAVRA_RUNNER_AUTH_HMAC_KEY:-}" ]; then
  client_args+=(--runner-auth-claims "${runner_claims_path}")
  if [ -n "${runner_auth_key_id}" ]; then
    client_args+=(--runner-auth-key-id "${runner_auth_key_id}")
  fi
fi
if [ -n "${evidence_key_id}" ]; then
  client_args+=(--evidence-signing-key-id "${evidence_key_id}")
fi

"${runtime_path}" "${client_args[@]}" \
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
