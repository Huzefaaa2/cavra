from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REQUIRED_CHECK_NAME = "cavra-required-check"
SETTINGS_ENV_VAR = "CAVRA_AGENT_ENFORCEMENT_SETTINGS"


def _load_settings(path: str | Path | None) -> dict[str, Any]:
    configured_path = path or os.environ.get(SETTINGS_ENV_VAR)
    if not configured_path:
        return {}
    settings_path = Path(configured_path)
    if not settings_path.exists():
        return {"_load_error": f"settings file not found: {settings_path}"}
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"_load_error": f"settings file is not valid JSON: {exc}"}
    return data if isinstance(data, dict) else {"_load_error": "settings file must contain a JSON object"}


def _check(
    check_id: str,
    status: str,
    message: str,
    *,
    severity: str | None = None,
    evidence: dict[str, object] | None = None,
) -> dict[str, object]:
    inferred_severity = severity or ("critical" if status == "fail" else "warning" if status == "warn" else "info")
    payload: dict[str, object] = {
        "id": check_id,
        "status": status,
        "severity": inferred_severity,
        "message": message,
    }
    if evidence is not None:
        payload["evidence"] = evidence
    return payload


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def _first_existing(paths: list[Path]) -> Path | None:
    return next((path for path in paths if path.exists()), None)


def _workflow_permissions_findings(workflow_dir: Path, root: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    if not workflow_dir.exists():
        return findings
    for path in sorted([*workflow_dir.glob("*.yml"), *workflow_dir.glob("*.yaml")]):
        text = _read_text(path).lower()
        rel = str(path.relative_to(root))
        if "permissions: write-all" in text:
            findings.append(
                _check(
                    f"workflow_permission_write_all:{path.name}",
                    "fail",
                    f"{rel} grants write-all permissions and can weaken CAVRA enforcement.",
                    evidence={"workflow": rel},
                )
            )
        elif "contents: write" in text and "pull_request" in text:
            findings.append(
                _check(
                    f"workflow_permission_contents_write:{path.name}",
                    "warn",
                    f"{rel} uses contents: write; verify it is limited to approved release or Pages workflows.",
                    evidence={"workflow": rel},
                )
            )
    return findings


def _branch_setting_confirmed(branch: dict[str, Any], *keys: str, expected: object = True) -> bool:
    for key in keys:
        if key in branch and branch[key] == expected:
            return True
    return False


def _branch_setting_disabled(branch: dict[str, Any], allowed_key: str, disabled_key: str) -> bool:
    return branch.get(allowed_key) is False or branch.get(disabled_key) is True


def _minimum_review_count(branch: dict[str, Any]) -> int:
    value = branch.get("required_reviews", 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def agent_enforcement_readiness_report(
    *,
    repo_root: str | Path = ".",
    settings_path: str | Path | None = None,
    settings: dict[str, Any] | None = None,
    required_check_name: str = DEFAULT_REQUIRED_CHECK_NAME,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    loaded_settings = settings if settings is not None else _load_settings(settings_path)
    workflow_path = root / ".github" / "workflows" / "cavra-governance.yml"
    agent_manifest_dir = root / ".github" / "agents"
    agent_manifests = sorted([*agent_manifest_dir.glob("*.yml"), *agent_manifest_dir.glob("*.yaml")])
    pr_template = _first_existing(
        [
            root / ".github" / "PULL_REQUEST_TEMPLATE.md",
            root / ".github" / "pull_request_template.md",
            root / "PULL_REQUEST_TEMPLATE.md",
            root / "pull_request_template.md",
        ]
    )
    codeowners = _first_existing([root / ".github" / "CODEOWNERS", root / "CODEOWNERS"])
    policy_pack = root / "policies" / "cavra-agentic-delivery" / "policy.yaml"
    checks: list[dict[str, object]] = []

    if loaded_settings.get("_load_error"):
        checks.append(_check("settings_file", "warn", str(loaded_settings["_load_error"])))

    if workflow_path.exists():
        workflow_text = _read_text(workflow_path)
        checks.append(
            _check(
                "required_check_workflow",
                "pass",
                "CAVRA governance workflow is present.",
                evidence={"path": str(workflow_path.relative_to(root))},
            )
        )
        checks.append(
            _check(
                "required_check_name",
                "pass" if required_check_name in workflow_text else "fail",
                f"Required check name `{required_check_name}` is {'present' if required_check_name in workflow_text else 'missing'} in the governance workflow.",
                evidence={"workflow": str(workflow_path.relative_to(root)), "required_check_name": required_check_name},
            )
        )
        checks.append(
            _check(
                "required_check_evidence_artifact",
                "pass" if "cavra-required-check-evidence" in workflow_text else "warn",
                "Required-check evidence artifact is configured."
                if "cavra-required-check-evidence" in workflow_text
                else "Required-check evidence artifact was not found in the governance workflow.",
                evidence={"workflow": str(workflow_path.relative_to(root))},
            )
        )
    else:
        checks.append(_check("required_check_workflow", "fail", "Missing .github/workflows/cavra-governance.yml."))

    checks.append(
        _check(
            "agent_manifest_coverage",
            "pass" if agent_manifests else "fail",
            f"{len(agent_manifests)} transparent agent manifest(s) found under .github/agents.",
            evidence={"manifest_count": len(agent_manifests), "directory": ".github/agents"},
        )
    )
    pr_template_text = _read_text(pr_template) if pr_template else ""
    checks.append(
        _check(
            "pull_request_template",
            "pass" if pr_template and "cavra" in pr_template_text.lower() else "warn",
            "Pull request template references CAVRA evidence."
            if pr_template and "cavra" in pr_template_text.lower()
            else "Pull request template does not reference CAVRA evidence."
            if pr_template
            else "Pull request template is missing.",
            evidence={"path": str(pr_template.relative_to(root)) if pr_template else None},
        )
    )
    checks.append(
        _check(
            "codeowners",
            "pass" if codeowners else "warn",
            "CODEOWNERS is present." if codeowners else "CODEOWNERS is missing.",
            evidence={"path": str(codeowners.relative_to(root)) if codeowners else None},
        )
    )
    checks.append(
        _check(
            "agentic_delivery_policy_pack",
            "pass" if policy_pack.exists() else "fail",
            "Agentic delivery policy pack is present."
            if policy_pack.exists()
            else "Missing policies/cavra-agentic-delivery/policy.yaml.",
            evidence={"path": str(policy_pack.relative_to(root))},
        )
    )

    branch = loaded_settings.get("branch_protection", {}) if isinstance(loaded_settings.get("branch_protection"), dict) else {}
    required_checks = loaded_settings.get("required_checks", [])
    if isinstance(required_checks, str):
        required_checks = [required_checks]
    required_checks = [str(item) for item in required_checks] if isinstance(required_checks, list) else []
    if branch:
        branch_expectations = [
            (
                "pull_request_required",
                _branch_setting_confirmed(branch, "pull_request_required", "required_pull_request_reviews"),
                "Pull requests are required before merge.",
            ),
            (
                "review_required",
                _minimum_review_count(branch) >= 1 or _branch_setting_confirmed(branch, "review_required"),
                "Non-author review is required.",
            ),
            (
                "stale_review_dismissal",
                _branch_setting_confirmed(branch, "dismiss_stale_reviews", "stale_review_dismissal"),
                "Stale approvals are dismissed on new commits.",
            ),
            (
                "conversation_resolution_required",
                _branch_setting_confirmed(branch, "conversation_resolution_required"),
                "Conversation resolution is required.",
            ),
            (
                "direct_push_restricted",
                _branch_setting_confirmed(branch, "restricted_pushes", "direct_push_restricted"),
                "Direct pushes are restricted.",
            ),
            (
                "force_push_disabled",
                _branch_setting_disabled(branch, "force_pushes_allowed", "force_push_disabled"),
                "Force pushes are disabled.",
            ),
            (
                "deletion_disabled",
                _branch_setting_disabled(branch, "deletions_allowed", "deletion_disabled"),
                "Protected branch deletion is disabled.",
            ),
            (
                "bypass_disabled",
                _branch_setting_disabled(branch, "bypass_allowed", "bypass_disabled")
                or _branch_setting_confirmed(branch, "do_not_allow_bypass"),
                "Branch protection bypass is disabled.",
            ),
        ]
        for key, passed, message in branch_expectations:
            checks.append(
                _check(
                    f"branch_{key}",
                    "pass" if passed else "fail",
                    message if passed else f"Branch protection setting `{key}` is not confirmed.",
                    evidence={"branch_protection_key": key},
                )
            )
    else:
        checks.append(
            _check(
                "branch_protection_settings",
                "warn",
                "Branch protection or ruleset settings were not supplied; verify them through GitHub/GitLab/Azure DevOps.",
            )
        )

    checks.append(
        _check(
            "required_cavra_status_check",
            "pass" if required_check_name in required_checks else "warn",
            f"`{required_check_name}` is configured as a required check."
            if required_check_name in required_checks
            else f"`{required_check_name}` was not supplied as a required check in settings.",
            evidence={"required_checks": required_checks},
        )
    )
    security_checks = loaded_settings.get("security_checks", [])
    if isinstance(security_checks, str):
        security_checks = [security_checks]
    security_checks = [str(item).lower() for item in security_checks] if isinstance(security_checks, list) else []
    checks.append(
        _check(
            "security_required_check",
            "pass" if any(item in {"codeql", "security-scan", "dependency-review"} for item in security_checks) else "warn",
            "Security required check is configured."
            if any(item in {"codeql", "security-scan", "dependency-review"} for item in security_checks)
            else "Security required check was not supplied in settings.",
            evidence={"security_checks": security_checks},
        )
    )
    checks.extend(_workflow_permissions_findings(root / ".github" / "workflows", root))

    failed = [item for item in checks if item["status"] == "fail"]
    warnings = [item for item in checks if item["status"] == "warn"]
    status = "blocked" if failed else "needs_attention" if warnings else "ready"
    return {
        "schema_version": "cavra.agent-enforcement-readiness.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "repo_root": str(root),
        "required_check_name": required_check_name,
        "summary": {
            "check_count": len(checks),
            "pass_count": len([item for item in checks if item["status"] == "pass"]),
            "warning_count": len(warnings),
            "failed_count": len(failed),
            "agent_manifest_count": len(agent_manifests),
        },
        "checks": checks,
        "recommended_actions": [
            "Require cavra-required-check on protected branches.",
            "Restrict direct pushes and disable bypass for protected branches where available.",
            "Keep AI-agent tokens out of repository administration, ruleset, workflow, secret, and environment permissions.",
            "Require PR attestation and CAVRA evidence artifacts before merge.",
            "Use governed CI runners with OIDC or signed runner claims for high-risk repositories.",
        ],
        "controls": [
            "agent-enforcement-readiness-derived-from-public-safe-repository-metadata",
            "report-contains-no-repository-secret-or-token",
            "external-branch-protection-settings-must-be-verified-through-provider-api-or-export",
        ],
    }
