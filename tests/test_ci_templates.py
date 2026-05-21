from pathlib import Path

import yaml


def _load_yaml(path: str) -> dict[str, object]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_live_github_governance_workflow_is_required_check_candidate() -> None:
    workflow_path = ".github/workflows/cavra-governance.yml"
    workflow = _load_yaml(workflow_path)
    text = Path(workflow_path).read_text(encoding="utf-8")

    assert workflow["jobs"]["cavra"]["name"] == "cavra-required-check"
    assert "cavra policy validate" in text
    assert "ruff check src/ tests/" in text
    assert "actions/setup-go@v6" in text
    assert "go test ./..." in text
    assert "pytest -q" in text
    assert "cavra evidence verify .cavra/evidence/required-check" in text
    assert "cavra evidence verify-attestation" in text
    assert "cavra-required-check-evidence" in text
    assert "Go enforcement-plane parity scaffold tested." in text


def test_go_runtime_ci_job_runs_with_setup_go() -> None:
    workflow_path = ".github/workflows/test.yml"
    workflow = _load_yaml(workflow_path)
    text = Path(workflow_path).read_text(encoding="utf-8")

    assert workflow["jobs"]["go-runtime"]["name"] == "go-runtime-parity"
    assert "actions/setup-go@v6" in text
    assert "go-version-file: go/cavra-runtime/go.mod" in text
    assert "go test ./..." in text
    assert "working-directory: go/cavra-runtime" in text


def test_sandbox_pages_workflow_builds_static_artifact() -> None:
    workflow_path = ".github/workflows/deploy-sandbox.yml"
    workflow = _load_yaml(workflow_path)
    text = Path(workflow_path).read_text(encoding="utf-8")

    assert workflow["permissions"]["pages"] == "write"
    assert workflow["permissions"]["id-token"] == "write"
    assert workflow["env"]["FORCE_JAVASCRIPT_ACTIONS_TO_NODE24"] == "true"
    assert workflow["jobs"]["build"]["name"] == "build-sandbox"
    assert workflow["jobs"]["deploy"]["name"] == "deploy-sandbox"
    assert "assets/brand/**" in text
    assert "node --check apps/sandbox-ui/config.js" in text
    assert "node --check apps/sandbox-ui/sandbox.js" in text
    assert "CAVRA_PUBLIC_API_BASE_URL" in text
    assert "public/config.js" in text
    assert "cp -R assets/brand public/assets/" in text
    assert "actions/configure-pages@v6" in text
    assert "actions/upload-pages-artifact@v3" in text
    assert "actions/deploy-pages@v4" in text


def test_go_release_workflow_packages_signed_release_artifacts() -> None:
    workflow_path = ".github/workflows/go-release.yml"
    workflow = _load_yaml(workflow_path)
    text = Path(workflow_path).read_text(encoding="utf-8")

    assert workflow["permissions"]["id-token"] == "write"
    assert workflow["permissions"]["attestations"] == "write"
    assert workflow["permissions"]["artifact-metadata"] == "write"
    assert workflow["jobs"]["package"]["name"] == "package-go-runtime"
    assert "actions/setup-go@v6" in text
    assert "actions/attest@v4" in text
    assert "github-keyless-attestation.json" in text
    assert "gh attestation verify" in text
    assert "go-version-file: go/cavra-runtime/go.mod" in text
    assert "GOOS=" in text
    assert "go list -m -json all" in text
    assert "scripts/package_go_release.py" in text
    assert "CAVRA_GO_RELEASE_SIGNING_KEY" in text
    assert "--signing-required" in text
    assert "cavra-go-runtime-release-package" in text


def test_github_required_check_templates_parse_and_verify_evidence() -> None:
    for workflow_path in [
        "examples/github-actions/cavra-required-check.yml",
        "examples/github-actions/cavra-enterprise-enforcement.yml",
    ]:
        workflow = _load_yaml(workflow_path)
        text = Path(workflow_path).read_text(encoding="utf-8")

        assert workflow["jobs"]["cavra"]["name"].startswith("cavra-")
        assert "cavra policy validate" in text
        assert "cavra evidence verify" in text
        assert "cavra evidence verify-attestation" in text


def test_github_release_governance_go_runtime_template_uses_typed_daemon_request() -> None:
    workflow_path = "examples/github-actions/cavra-release-governance-go-runtime.yml"
    workflow = _load_yaml(workflow_path)
    text = Path(workflow_path).read_text(encoding="utf-8")

    job = workflow["jobs"]["cavra-release-governance"]
    assert job["name"] == "cavra-release-governance-go-runtime"
    assert "actions/setup-go@v6" in text
    assert "go-version-file: go/cavra-runtime/go.mod" in text
    assert "CAVRA_RELEASE_GOVERNANCE_REQUEST" in text
    assert "examples/go-runtime/typed-release-governance/approved-promotion.json" in text
    assert "--lifecycle start" in text
    assert "--daemon" in text
    assert "release-governance-evidence.jsonl" in text
    assert "release-governance-response.json" in text
    assert "release_governance.approval.approved" in text
    assert "cavra-release-governance-go-runtime" in text


def test_github_release_governance_composite_action_uses_packaged_runner_wrapper() -> None:
    action_path = "examples/github-actions/actions/cavra-release-governance-go-runtime/action.yml"
    action = _load_yaml(action_path)
    text = Path(action_path).read_text(encoding="utf-8")

    assert action["runs"]["using"] == "composite"
    assert "runtime-path" in action["inputs"]
    assert "request-path" in action["inputs"]
    assert "expected-decision" in action["inputs"]
    assert "runner-auth-key-id" in action["inputs"]
    assert "evidence-signing-key-id" in action["inputs"]
    assert "runner-oidc-issuer" in action["inputs"]
    assert "runner-oidc-audience" in action["inputs"]
    assert "runner-oidc-jwks-url" in action["inputs"]
    assert "runner-oidc-token-file" in action["inputs"]
    assert "CAVRA_RELEASE_GOVERNANCE_REQUEST" in text
    assert "CAVRA_RUNNER_AUTH_KEY_ID" in text
    assert "CAVRA_DAEMON_EVIDENCE_KEY_ID" in text
    assert "CAVRA_RUNNER_OIDC_ISSUER" in text
    assert "CAVRA_RUNNER_AUTH_OIDC_TOKEN_FILE" in text
    assert "cavra-release-governance-runner.sh" in text


def test_release_governance_runner_wrapper_runs_daemon_and_fails_closed() -> None:
    script_path = "examples/ci-runners/cavra-release-governance-runner.sh"
    text = Path(script_path).read_text(encoding="utf-8")

    assert "CAVRA_RUNTIME_PATH" in text
    assert "CAVRA_RELEASE_GOVERNANCE_REQUEST" in text
    assert "--lifecycle start" in text
    assert "--daemon" in text
    assert "--runner-auth-claims" in text
    assert "--runner-auth-key-id" in text
    assert "--runner-auth-oidc-token-file" in text
    assert "--runner-oidc-issuer" in text
    assert "--runner-oidc-audience" in text
    assert "--runner-oidc-jwks-url" in text
    assert "--evidence-signing-key-id" in text
    assert "--verify-evidence" in text
    assert "CAVRA_RUNNER_AUTH_HMAC_KEY" in text
    assert "CAVRA_RUNNER_AUTH_OIDC_TOKEN" in text
    assert "CAVRA_RUNNER_OIDC_JWKS_URL" in text
    assert "CAVRA_DAEMON_EVIDENCE_HMAC_KEY" in text
    assert "runner-auth-claims.json" in text
    assert "release-governance-evidence-verification.json" in text
    assert "release-governance-evidence.jsonl" in text
    assert "release-governance-response.json" in text
    assert "CAVRA blocked release governance request" in text


def test_gitlab_required_check_template_parses_and_exports_artifacts() -> None:
    pipeline_path = "examples/gitlab-ci/cavra-required-check.gitlab-ci.yml"
    pipeline = _load_yaml(pipeline_path)
    text = Path(pipeline_path).read_text(encoding="utf-8")

    job = pipeline["cavra-required-check"]
    assert job["stage"] == "governance"
    assert "cavra evidence verify" in text
    assert "cavra evidence verify-attestation" in text
    assert ".cavra/evidence/attestation/" in job["artifacts"]["paths"]


def test_gitlab_release_governance_go_runtime_template_uses_typed_daemon_request() -> None:
    pipeline_path = "examples/gitlab-ci/cavra-release-governance-go-runtime.gitlab-ci.yml"
    pipeline = _load_yaml(pipeline_path)
    text = Path(pipeline_path).read_text(encoding="utf-8")

    job = pipeline["cavra-release-governance-go-runtime"]
    assert job["stage"] == "release-governance"
    assert job["image"] == "golang:1.26"
    assert "CAVRA_RELEASE_GOVERNANCE_REQUEST" in text
    assert "examples/go-runtime/typed-release-governance/approved-promotion.json" in text
    assert "--lifecycle start" in text
    assert "--daemon" in text
    assert "release-governance-evidence.jsonl" in text
    assert "release_governance.approval.approved" in text
    assert "go/cavra-runtime/.cavra/go-daemon/" in job["artifacts"]["paths"]


def test_azure_pipelines_required_check_template_parses_and_exports_artifacts() -> None:
    pipeline_path = "examples/azure-pipelines/cavra-required-check.azure-pipelines.yml"
    pipeline = _load_yaml(pipeline_path)
    text = Path(pipeline_path).read_text(encoding="utf-8")

    job = pipeline["stages"][0]["jobs"][0]
    artifact_step = job["steps"][-1]
    assert pipeline["trigger"] == "none"
    assert pipeline["pr"] == "none"
    assert job["displayName"] == "cavra-required-check"
    assert "cavra policy validate" in text
    assert "cavra evidence verify" in text
    assert "cavra evidence verify-attestation" in text
    assert artifact_step["task"] == "PublishPipelineArtifact@1"
    assert artifact_step["inputs"]["artifact"] == "cavra-required-check-evidence"


def test_azure_release_governance_go_runtime_template_uses_typed_daemon_request() -> None:
    pipeline_path = "examples/azure-pipelines/cavra-release-governance-go-runtime.azure-pipelines.yml"
    pipeline = _load_yaml(pipeline_path)
    text = Path(pipeline_path).read_text(encoding="utf-8")

    job = pipeline["stages"][0]["jobs"][0]
    artifact_step = job["steps"][-1]
    assert pipeline["trigger"] == "none"
    assert pipeline["pr"] == "none"
    assert job["displayName"] == "cavra-release-governance-go-runtime"
    assert "GoTool@0" in text
    assert "CAVRA_RELEASE_GOVERNANCE_REQUEST" in text
    assert "examples/go-runtime/typed-release-governance/approved-promotion.json" in text
    assert "--lifecycle start" in text
    assert "--daemon" in text
    assert "release-governance-evidence.jsonl" in text
    assert "release_governance.approval.approved" in text
    assert artifact_step["task"] == "PublishPipelineArtifact@1"
    assert artifact_step["inputs"]["artifact"] == "cavra-release-governance-go-runtime"
