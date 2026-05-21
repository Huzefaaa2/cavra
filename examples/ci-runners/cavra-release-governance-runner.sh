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
runner_oidc_issuer="${CAVRA_RUNNER_OIDC_ISSUER:-}"
runner_oidc_audience="${CAVRA_RUNNER_OIDC_AUDIENCE:-}"
runner_oidc_jwks="${CAVRA_RUNNER_OIDC_JWKS:-}"
runner_oidc_jwks_url="${CAVRA_RUNNER_OIDC_JWKS_URL:-}"
runner_oidc_token_file="${CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE:-}"
runner_oidc_auto="${CAVRA_RUNNER_OIDC_AUTO:-true}"
runner_oidc_token_env="${CAVRA_RUNNER_AUTH_OIDC_TOKEN_ENV:-}"
runner_oidc_auto_token_file="${evidence_dir}/runner-oidc.jwt"

mkdir -p "${evidence_dir}"

# Optional hardening:
# - CAVRA_RUNNER_AUTH_HMAC_KEY signs runner identity claims for daemon authentication.
# - CAVRA_RUNNER_AUTH_OIDC_TOKEN or CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE sends a CI-provider OIDC JWT.
# - CAVRA_RUNNER_OIDC_AUTO=true asks GitHub Actions, GitLab CI, or Azure Pipelines for a short-lived JWT.
# - CAVRA_RUNNER_OIDC_ISSUER, CAVRA_RUNNER_OIDC_AUDIENCE, and CAVRA_RUNNER_OIDC_JWKS_URL
#   make the daemon verify GitHub Actions, GitLab CI, or Azure Pipelines JWTs directly.
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

if [ "${runner_oidc_auto}" = "true" ] && [ -z "${CAVRA_RUNNER_AUTH_OIDC_TOKEN:-}" ] && [ -z "${runner_oidc_token_file}" ] && { [ -z "${CAVRA_RUNNER_AUTH_HMAC_KEY:-}" ] || [ -n "${runner_oidc_issuer}" ] || [ -n "${runner_oidc_audience}" ]; }; then
  python3 - "${runner_oidc_auto_token_file}" "${runner_oidc_audience}" "${runner_oidc_token_env}" <<'PY'
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

output_path = pathlib.Path(sys.argv[1])
audience = sys.argv[2]
token_env_name = sys.argv[3]


def write_token(token: str) -> None:
    token = token.strip()
    if not token:
        return
    output_path.write_text(token + "\n", encoding="utf-8")
    output_path.chmod(0o600)


def request_json(url, bearer=None):
    headers = {"Accept": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


if os.environ.get("GITHUB_ACTIONS") and os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL") and os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN"):
    url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"]
    if audience:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}audience={urllib.parse.quote(audience, safe='')}"
    payload = request_json(url, os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"])
    write_token(str(payload.get("value", "")))
elif os.environ.get("GITLAB_CI"):
    candidates = [
        token_env_name,
        "CAVRA_GITLAB_OIDC_TOKEN",
        "GITLAB_OIDC_TOKEN",
        "CI_JOB_JWT_V2",
    ]
    for name in candidates:
        if name and os.environ.get(name):
            write_token(os.environ[name])
            break
elif os.environ.get("TF_BUILD"):
    if os.environ.get("CAVRA_AZURE_OIDC_TOKEN"):
        write_token(os.environ["CAVRA_AZURE_OIDC_TOKEN"])
    elif os.environ.get("SYSTEM_OIDCREQUESTURI"):
        bearer = os.environ.get("CAVRA_AZURE_OIDC_REQUEST_TOKEN") or os.environ.get("SYSTEM_ACCESSTOKEN")
        payload = request_json(os.environ["SYSTEM_OIDCREQUESTURI"], bearer)
        write_token(str(payload.get("oidcToken") or payload.get("idToken") or payload.get("value") or ""))
PY
  if [ -s "${runner_oidc_auto_token_file}" ]; then
    runner_oidc_token_file="${runner_oidc_auto_token_file}"
  fi
fi

if [ -z "${runner_oidc_issuer}" ] && { [ -n "${CAVRA_RUNNER_AUTH_OIDC_TOKEN:-}" ] || [ -n "${runner_oidc_token_file}" ]; }; then
  if [ -n "${GITHUB_ACTIONS:-}" ]; then
    runner_oidc_issuer="https://token.actions.githubusercontent.com"
  elif [ -n "${GITLAB_CI:-}" ]; then
    runner_oidc_issuer="${CI_SERVER_URL:-https://gitlab.com}"
  fi
fi
if [ -z "${runner_oidc_jwks_url}" ] && { [ -n "${CAVRA_RUNNER_AUTH_OIDC_TOKEN:-}" ] || [ -n "${runner_oidc_token_file}" ]; }; then
  if [ -n "${GITHUB_ACTIONS:-}" ]; then
    runner_oidc_jwks_url="https://token.actions.githubusercontent.com/.well-known/jwks"
  elif [ -n "${GITLAB_CI:-}" ]; then
    runner_oidc_jwks_url="${CI_SERVER_URL:-https://gitlab.com}/oauth/discovery/keys"
  fi
fi

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
if [ -n "${runner_oidc_issuer}" ]; then
  start_args+=(--runner-oidc-issuer "${runner_oidc_issuer}")
fi
if [ -n "${runner_oidc_audience}" ]; then
  start_args+=(--runner-oidc-audience "${runner_oidc_audience}")
fi
if [ -n "${runner_oidc_jwks}" ]; then
  start_args+=(--runner-oidc-jwks "${runner_oidc_jwks}")
fi
if [ -n "${runner_oidc_jwks_url}" ]; then
  start_args+=(--runner-oidc-jwks-url "${runner_oidc_jwks_url}")
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
if [ -n "${CAVRA_RUNNER_AUTH_OIDC_TOKEN:-}" ] || [ -n "${runner_oidc_token_file}" ]; then
  client_args+=(--runner-auth-claims "${runner_claims_path}")
  if [ -n "${runner_oidc_token_file}" ]; then
    client_args+=(--runner-auth-oidc-token-file "${runner_oidc_token_file}")
  fi
fi
if [ -n "${evidence_key_id}" ]; then
  client_args+=(--evidence-signing-key-id "${evidence_key_id}")
fi

"${runtime_path}" "${client_args[@]}" \
  > "${response_path}"

if [ -n "${CAVRA_DAEMON_EVIDENCE_HMAC_KEY:-}" ]; then
  verify_args=(--verify-evidence --evidence-log "${evidence_log}")
  if [ -n "${evidence_key_id}" ]; then
    verify_args+=(--evidence-signing-key-id "${evidence_key_id}")
  fi
  "${runtime_path}" "${verify_args[@]}" > "${evidence_dir}/release-governance-evidence-verification.json"
fi

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
