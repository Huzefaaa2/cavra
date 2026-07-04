from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ZERO_TRUST_REFERENCE_DEPLOYMENT_SCHEMA = "cavra.zero-trust-reference-deployments.v1"
ZERO_TRUST_REFERENCE_READINESS_SCHEMA = "cavra.zero-trust-reference-deployments.readiness.v1"
ZERO_TRUST_REFERENCE_READINESS_RESULT_SCHEMA = "cavra.zero-trust-reference-deployments.readiness-result.v1"

REQUIRED_DEPLOYMENT_ARTIFACTS = {
    "docker_compose",
    "helm_chart",
    "terraform_azure",
    "azure_container_apps",
    "scanner_operation_runbook",
    "quickstart_demo",
}

REQUIRED_SECURITY_CONTROLS = {
    "fail_closed_runtime",
    "metadata_only_scanner",
    "tenant_workspace_scope",
    "private_network_mode",
    "signed_evidence_refs",
    "no_raw_model_egress",
}

REQUIRED_OPERATING_EVIDENCE = {
    "catalog_ref",
    "compose_smoke_ref",
    "helm_template_ref",
    "terraform_validate_ref",
    "azure_what_if_ref",
    "scanner_runbook_ref",
    "evidence_export_ref",
}

REFERENCE_DEPLOYMENT_FILES = {
    "docker_compose": "examples/reference-deployments/zero-trust/docker-compose.yml",
    "helm_chart": "examples/reference-deployments/zero-trust/helm/cavra-zero-trust/Chart.yaml",
    "terraform_azure": "examples/reference-deployments/zero-trust/terraform/azure/main.tf",
    "azure_container_apps": "examples/reference-deployments/zero-trust/azure/container-apps.bicep",
    "scanner_operation_runbook": "examples/reference-deployments/zero-trust/scanner-operation-runbook.md",
    "quickstart_demo": "examples/reference-deployments/zero-trust/quickstart-demo.md",
}

REQUIRED_FILE_MARKERS = {
    "docker_compose": [
        "cavra-api",
        "cavra-scanner",
        "CAVRA_FAIL_CLOSED=true",
        "CAVRA_SCANNER_MODE=metadata_only",
        "CAVRA_TENANT_ID",
    ],
    "helm_chart": [
        "cavra-zero-trust",
        "scanner",
        "failClosed",
    ],
    "terraform_azure": [
        "azurerm_container_app",
        "azurerm_container_app_environment",
        "azurerm_log_analytics_workspace",
        "zero_trust_scanner",
    ],
    "azure_container_apps": [
        "Microsoft.App/containerApps",
        "cavra-api",
        "cavra-scanner",
        "CAVRA_SCANNER_MODE",
    ],
    "scanner_operation_runbook": [
        "metadata-only",
        "no raw model",
        "customer-side",
        "evidence",
    ],
    "quickstart_demo": [
        "docker compose",
        "cavra deployment zero-trust-readiness",
        "validate_zero_trust_reference_deployments.py",
        "ready_for_live_zero_trust_reference_deployments",
    ],
}


def build_reference_deployment_catalog() -> dict[str, Any]:
    return {
        "schema_version": ZERO_TRUST_REFERENCE_DEPLOYMENT_SCHEMA,
        "product": "CAVRA",
        "catalog_id": "cavra-zero-trust-reference-deployments",
        "deployment_artifacts": [
            {
                "artifact_id": artifact_id,
                "path": REFERENCE_DEPLOYMENT_FILES[artifact_id],
                "purpose": _artifact_purpose(artifact_id),
            }
            for artifact_id in sorted(REQUIRED_DEPLOYMENT_ARTIFACTS)
        ],
        "security_controls": [
            {
                "control_id": control_id,
                "description": _control_description(control_id),
            }
            for control_id in sorted(REQUIRED_SECURITY_CONTROLS)
        ],
        "scanner_boundary": {
            "execution": "customer-side",
            "egress": "metadata-only hashes, scores, findings, and evidence references",
            "forbidden": [
                "raw model bytes",
                "training data",
                "source code",
                "prompt samples",
                "credentials",
            ],
        },
        "reference_commands": [
            "docker compose -f examples/reference-deployments/zero-trust/docker-compose.yml up --build",
            "helm template cavra examples/reference-deployments/zero-trust/helm/cavra-zero-trust",
            "terraform -chdir=examples/reference-deployments/zero-trust/terraform/azure validate",
            "az deployment group what-if --template-file examples/reference-deployments/zero-trust/azure/container-apps.bicep",
        ],
    }


def build_reference_deployment_readiness_packet(
    *,
    evidence_mode: str = "sample",
    catalog_ref: str = "examples/reference-deployments/zero-trust-reference-deployments.json",
) -> dict[str, Any]:
    return {
        "schema_version": ZERO_TRUST_REFERENCE_READINESS_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "catalog_ref": catalog_ref,
        "deployment_artifacts": sorted(REQUIRED_DEPLOYMENT_ARTIFACTS),
        "security_controls": sorted(REQUIRED_SECURITY_CONTROLS),
        "operating_evidence": {
            "catalog_ref": catalog_ref,
            "compose_smoke_ref": f"{evidence_mode}://zero-trust-reference/docker-compose-smoke",
            "helm_template_ref": f"{evidence_mode}://zero-trust-reference/helm-template",
            "terraform_validate_ref": f"{evidence_mode}://zero-trust-reference/terraform-validate",
            "azure_what_if_ref": f"{evidence_mode}://zero-trust-reference/azure-what-if",
            "scanner_runbook_ref": "examples/reference-deployments/zero-trust/scanner-operation-runbook.md",
            "evidence_export_ref": f"{evidence_mode}://zero-trust-reference/evidence-export",
        },
        "deployment_boundaries": {
            "customer_side_scanner": True,
            "metadata_only_egress": True,
            "fail_closed_default": True,
            "tenant_workspace_required": True,
            "private_network_supported": True,
        },
    }


def validate_reference_deployment_catalog(
    catalog: dict[str, Any],
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if catalog.get("schema_version") == ZERO_TRUST_REFERENCE_DEPLOYMENT_SCHEMA else "blocker",
        "Reference deployment catalog schema is valid."
        if catalog.get("schema_version") == ZERO_TRUST_REFERENCE_DEPLOYMENT_SCHEMA
        else f"Catalog must use {ZERO_TRUST_REFERENCE_DEPLOYMENT_SCHEMA}.",
    )
    artifact_ids = {str(item.get("artifact_id")) for item in catalog.get("deployment_artifacts", []) if isinstance(item, dict)}
    missing_artifacts = sorted(REQUIRED_DEPLOYMENT_ARTIFACTS - artifact_ids)
    _add_check(
        checks,
        "deployment_artifacts",
        "pass" if not missing_artifacts else "blocker",
        "All required reference deployment artifacts are listed."
        if not missing_artifacts
        else f"Missing deployment artifacts: {', '.join(missing_artifacts)}.",
    )
    control_ids = {str(item.get("control_id")) for item in catalog.get("security_controls", []) if isinstance(item, dict)}
    missing_controls = sorted(REQUIRED_SECURITY_CONTROLS - control_ids)
    _add_check(
        checks,
        "security_controls",
        "pass" if not missing_controls else "blocker",
        "All required zero-trust security controls are listed."
        if not missing_controls
        else f"Missing security controls: {', '.join(missing_controls)}.",
    )
    if repo_root is not None:
        checks.extend(validate_reference_deployment_files(repo_root)["checks"])
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.zero-trust-reference-deployments.catalog-validation.v1",
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "checks": checks,
    }


def validate_reference_deployment_files(repo_root: Path) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    for artifact_id, relative_path in sorted(REFERENCE_DEPLOYMENT_FILES.items()):
        path = repo_root / relative_path
        if not path.is_file():
            _add_check(checks, f"{artifact_id}_file", "blocker", f"Missing reference deployment file: {relative_path}.")
            continue
        content = path.read_text(encoding="utf-8")
        missing_markers = [marker for marker in REQUIRED_FILE_MARKERS[artifact_id] if marker not in content]
        _add_check(
            checks,
            f"{artifact_id}_markers",
            "pass" if not missing_markers else "blocker",
            f"{artifact_id} contains required zero-trust markers."
            if not missing_markers
            else f"{artifact_id} is missing markers: {', '.join(missing_markers)}.",
        )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.zero-trust-reference-deployments.file-validation.v1",
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "checks": checks,
    }


def validate_reference_deployment_readiness_packet(
    packet: dict[str, Any],
    *,
    repo_root: Path | None = None,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == ZERO_TRUST_REFERENCE_READINESS_SCHEMA else "blocker",
        "Reference deployment readiness packet schema is valid."
        if packet.get("schema_version") == ZERO_TRUST_REFERENCE_READINESS_SCHEMA
        else f"Packet must use {ZERO_TRUST_REFERENCE_READINESS_SCHEMA}.",
    )
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_packet_set(
        checks,
        "deployment_artifacts",
        set(str(item) for item in packet.get("deployment_artifacts", [])),
        REQUIRED_DEPLOYMENT_ARTIFACTS,
    )
    _check_packet_set(
        checks,
        "security_controls",
        set(str(item) for item in packet.get("security_controls", [])),
        REQUIRED_SECURITY_CONTROLS,
    )
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    _check_boundaries(packet.get("deployment_boundaries", {}), checks)
    if repo_root is not None:
        checks.extend(validate_reference_deployment_files(repo_root)["checks"])
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": ZERO_TRUST_REFERENCE_READINESS_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_zero_trust_reference_deployment_contract": contract_ready,
        "ready_for_live_zero_trust_reference_deployments": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_reference_deployment_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    catalog = build_reference_deployment_catalog()
    sample_packet = build_reference_deployment_readiness_packet(evidence_mode="sample")
    live_packet = build_reference_deployment_readiness_packet(evidence_mode="live")
    written = {
        "catalog": output_dir / "zero-trust-reference-deployments.json",
        "sample_readiness": output_dir / "zero-trust-reference-deployments.sample.json",
        "live_readiness_example": output_dir / "zero-trust-reference-deployments.live.sanitized.example.json",
    }
    written["catalog"].write_text(json.dumps(catalog, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_readiness"].write_text(json.dumps(sample_packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_readiness_example"].write_text(json.dumps(live_packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.zero-trust-reference-deployments.export.v1",
        "written": {key: str(path) for key, path in written.items()},
    }


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    if mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live zero-trust reference deployment evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample reference deployment packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live reference deployment validation requires evidence_mode=live.")


def _check_packet_set(
    checks: list[dict[str, str]],
    name: str,
    actual: set[str],
    required: set[str],
) -> None:
    missing = sorted(required - actual)
    _add_check(
        checks,
        name,
        "pass" if not missing else "blocker",
        f"{name} includes all required entries." if not missing else f"{name} missing: {', '.join(missing)}.",
    )


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    missing = sorted(item for item in REQUIRED_OPERATING_EVIDENCE if not evidence.get(item))
    _add_check(
        checks,
        "operating_evidence",
        "pass" if not missing else "blocker",
        "Reference deployment operating evidence references are present."
        if not missing
        else f"Operating evidence missing: {', '.join(missing)}.",
    )


def _check_boundaries(boundaries: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = {
        "customer_side_scanner": True,
        "metadata_only_egress": True,
        "fail_closed_default": True,
        "tenant_workspace_required": True,
        "private_network_supported": True,
    }
    missing = sorted(key for key, expected in required.items() if boundaries.get(key) is not expected)
    _add_check(
        checks,
        "deployment_boundaries",
        "pass" if not missing else "blocker",
        "Zero-trust deployment boundaries are explicit."
        if not missing
        else f"Deployment boundaries missing or false: {', '.join(missing)}.",
    )


def _artifact_purpose(artifact_id: str) -> str:
    purposes = {
        "docker_compose": "Local and customer-lab reference stack for API plus metadata-only scanner.",
        "helm_chart": "Kubernetes packaging baseline for private clusters and managed Kubernetes.",
        "terraform_azure": "Azure infrastructure skeleton for Container Apps, registry, logging, and storage boundaries.",
        "azure_container_apps": "Bicep reference for API and scanner sidecar-style jobs in Azure Container Apps.",
        "scanner_operation_runbook": "Customer-side operating checklist for metadata-only scanner execution.",
        "quickstart_demo": "End-to-end reproducible demo path and validation commands.",
    }
    return purposes[artifact_id]


def _control_description(control_id: str) -> str:
    descriptions = {
        "fail_closed_runtime": "Runtime gates must deny risky actions when policy, identity, or approval context is missing.",
        "metadata_only_scanner": "Scanner output is limited to hashes, risk scores, findings, and evidence references.",
        "tenant_workspace_scope": "Every deployment path requires tenant and workspace scope variables.",
        "private_network_mode": "Deployment examples support private endpoint or internal-only network operation.",
        "signed_evidence_refs": "Outputs point to signed evidence artifacts rather than raw private data.",
        "no_raw_model_egress": "Raw model weights, training data, prompts, source code, and secrets cannot leave the boundary.",
    }
    return descriptions[control_id]


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
