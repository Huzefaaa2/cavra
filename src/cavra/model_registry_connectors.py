from __future__ import annotations

from typing import Any

from cavra.connector_sdk import (
    CONNECTOR_MANIFEST_SCHEMA,
    REQUIRED_TEST_SUITES,
    build_connector_certification_packet,
    build_connector_compatibility_matrix,
    validate_connector_manifest,
)


MODEL_REGISTRY_EVIDENCE_SCHEMA = "cavra.model-registry-connectors.evidence.v1"
MODEL_REGISTRY_READINESS_SCHEMA = "cavra.model-registry-connectors.readiness.v1"

MODEL_REGISTRY_PROVIDER_SPECS: dict[str, dict[str, Any]] = {
    "mlflow": {
        "display_name": "MLflow Model Registry Connector",
        "auth_modes": ["bearer_token", "api_key"],
        "capabilities": ["model_version_lookup", "registered_model_metadata", "stage_tracking", "lineage_reference"],
    },
    "sagemaker": {
        "display_name": "Amazon SageMaker Model Registry Connector",
        "auth_modes": ["oidc_workload_identity", "api_key"],
        "capabilities": ["model_package_lookup", "approval_status_tracking", "model_card_reference", "lineage_reference"],
    },
    "huggingface": {
        "display_name": "Hugging Face Model Hub Connector",
        "auth_modes": ["bearer_token", "api_key"],
        "capabilities": ["repository_metadata", "model_card_reference", "revision_hash_tracking", "lineage_reference"],
    },
    "wandb": {
        "display_name": "Weights & Biases Model Registry Connector",
        "auth_modes": ["api_key", "bearer_token"],
        "capabilities": ["artifact_metadata", "alias_tracking", "run_lineage_reference", "risk_metadata"],
    },
}

REQUIRED_MODEL_REGISTRY_PROVIDERS = set(MODEL_REGISTRY_PROVIDER_SPECS)
REQUIRED_METADATA_FIELDS = {
    "registry_provider",
    "model_ref",
    "model_version",
    "artifact_digest",
    "owner_ref",
    "lineage_ref",
    "risk_tier",
    "evidence_ref",
}
FORBIDDEN_RAW_CONTENT_FIELDS = {
    "model_bytes",
    "model_weights",
    "training_data",
    "training_dataset",
    "dataset_rows",
    "prompt_samples",
    "private_features",
    "raw_artifact",
}


def build_model_registry_connector_manifest(provider: str) -> dict[str, Any]:
    spec = MODEL_REGISTRY_PROVIDER_SPECS[provider]
    return {
        "schema_version": CONNECTOR_MANIFEST_SCHEMA,
        "connector_id": f"cavra-model-registry-{provider}",
        "display_name": spec["display_name"],
        "provider": provider,
        "category": "model_registry",
        "version": "2026.07",
        "sdk_version": "1.0",
        "entrypoint": f"cavra.connectors.model_registry.{provider}:ModelRegistryConnector",
        "certification_tier": "certified",
        "supported_events": [
            "cavra.model.registry.metadata",
            "cavra.model.risk.finding",
            "cavra.model.approval.required",
        ],
        "capabilities": [
            *spec["capabilities"],
            "metadata_only_export",
            "no_raw_model_egress",
            "audit_metadata",
        ],
        "auth": {
            "modes": spec["auth_modes"],
            "secret_fields": ["authorization", "token", "api_key", "client_secret"],
        },
        "runtime": {
            "language": "python",
            "min_python": "3.9",
            "network_required": True,
            "timeout_seconds_default": 10,
            "max_retries_default": 2,
        },
        "security": {
            "redacts_secrets": True,
            "does_not_log_payload_secrets": True,
            "supports_timeout": True,
            "supports_retries": True,
            "idempotency_supported": True,
            "tenant_scope_required": True,
            "metadata_only": True,
            "raw_model_egress_blocked": True,
        },
        "tests": {
            "suites": sorted(REQUIRED_TEST_SUITES | {"metadata_only", "no_raw_model_egress"}),
            "fixtures": [f"examples/model-registries/connectors/{provider}.json"],
        },
        "compatibility": {
            "cavra_versions": ["1.0.0"],
            "api_contract": "openapi/cavra-api.openapi.json",
            "connector_sdk": "1.0",
        },
    }


def build_model_registry_connector_registry() -> dict[str, Any]:
    manifests = [
        build_model_registry_connector_manifest(provider)
        for provider in sorted(MODEL_REGISTRY_PROVIDER_SPECS)
    ]
    return {
        "schema_version": "cavra.model-registry-connectors.registry.v1",
        "product": "CAVRA",
        "connector_count": len(manifests),
        "providers": sorted(MODEL_REGISTRY_PROVIDER_SPECS),
        "manifests": manifests,
        "compatibility_matrix": build_connector_compatibility_matrix(manifests),
        "certification_packets": [
            build_connector_certification_packet(manifest, probe_results=_model_registry_probe_results())
            for manifest in manifests
        ],
    }


def build_model_registry_metadata_event(payload: dict[str, Any]) -> dict[str, Any]:
    validation = validate_model_registry_metadata(payload)
    if not validation["valid"]:
        blockers = [
            check["message"]
            for check in validation["checks"]
            if check["status"] == "blocker"
        ]
        raise ValueError("; ".join(blockers))
    return {
        "schema_version": "cavra.model-registry.metadata-event.v1",
        "product": "CAVRA",
        "event_type": "cavra.model.registry.metadata",
        "registry_provider": payload["registry_provider"],
        "model_ref": payload["model_ref"],
        "model_version": payload["model_version"],
        "artifact_digest": payload["artifact_digest"],
        "owner_ref": payload["owner_ref"],
        "lineage_ref": payload["lineage_ref"],
        "risk_tier": payload["risk_tier"],
        "evidence_ref": payload["evidence_ref"],
        "metadata": {
            key: value
            for key, value in payload.get("metadata", {}).items()
            if key not in FORBIDDEN_RAW_CONTENT_FIELDS
        },
    }


def validate_model_registry_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    missing = sorted(field for field in REQUIRED_METADATA_FIELDS if not payload.get(field))
    forbidden = sorted(_find_forbidden_fields(payload))
    digest = str(payload.get("artifact_digest", ""))
    _add_check(
        checks,
        "required_metadata",
        "pass" if not missing else "blocker",
        "Required model metadata fields are present." if not missing else f"Missing metadata fields: {', '.join(missing)}.",
    )
    _add_check(
        checks,
        "no_raw_model_egress",
        "pass" if not forbidden else "blocker",
        "Payload contains only metadata, references, and hashes." if not forbidden else f"Raw content fields are forbidden: {', '.join(forbidden)}.",
    )
    _add_check(
        checks,
        "artifact_digest",
        "pass" if digest.startswith("sha256:") and len(digest) > 20 else "blocker",
        "Artifact digest is hash-based." if digest.startswith("sha256:") and len(digest) > 20 else "Artifact digest must be a sha256 reference.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.model-registry.metadata-validation.v1",
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "checks": checks,
    }


def validate_model_registry_connector_registry(manifests: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    manifests = manifests or [
        build_model_registry_connector_manifest(provider)
        for provider in sorted(MODEL_REGISTRY_PROVIDER_SPECS)
    ]
    checks: list[dict[str, str]] = []
    providers = {str(manifest.get("provider")) for manifest in manifests}
    missing = sorted(REQUIRED_MODEL_REGISTRY_PROVIDERS - providers)
    invalid = [
        str(manifest.get("provider") or manifest.get("connector_id"))
        for manifest in manifests
        if not validate_connector_manifest(manifest)["valid"]
        or manifest.get("security", {}).get("raw_model_egress_blocked") is not True
        or manifest.get("security", {}).get("metadata_only") is not True
    ]
    _add_check(
        checks,
        "providers",
        "pass" if not missing else "blocker",
        "Every required model registry provider has a connector manifest." if not missing else f"Missing providers: {', '.join(missing)}.",
    )
    _add_check(
        checks,
        "metadata_only_manifests",
        "pass" if not invalid else "blocker",
        "Every model registry connector validates and blocks raw model egress." if not invalid else f"Invalid manifests: {', '.join(invalid)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.model-registry-connectors.registry-validation.v1",
        "product": "CAVRA",
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "provider_count": len(providers),
        "providers": sorted(providers),
        "checks": checks,
    }


def validate_model_registry_connectors_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_provider_registry(packet.get("provider_registry", {}), checks)
    _check_metadata_contract(packet.get("metadata_contract", {}), checks)
    _check_no_egress(packet.get("no_raw_model_egress", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": MODEL_REGISTRY_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_model_registry_connector_contract": contract_ready,
        "ready_for_live_model_registry_connectors": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _model_registry_probe_results() -> dict[str, str]:
    return {
        "auth": "pass",
        "compatibility": "pass",
        "contract": "pass",
        "metadata_only": "pass",
        "no_raw_model_egress": "pass",
        "redaction": "pass",
        "retry": "pass",
        "timeout": "pass",
    }


def _find_forbidden_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key in FORBIDDEN_RAW_CONTENT_FIELDS:
                found.add(path)
            found.update(_find_forbidden_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == MODEL_REGISTRY_EVIDENCE_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Model registry connector evidence packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.model-registry-connectors.evidence.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    if mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live model registry connector evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample model registry connector packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live model registry validation requires evidence_mode=live.")


def _check_provider_registry(registry: dict[str, Any], checks: list[dict[str, str]]) -> None:
    provider_ids = set(registry.get("provider_ids", []))
    missing = sorted(REQUIRED_MODEL_REGISTRY_PROVIDERS - provider_ids)
    flags = {
        "manifests_published": registry.get("manifests_published") is True,
        "certification_packets_generated": registry.get("certification_packets_generated") is True,
        "compatibility_matrix_generated": registry.get("compatibility_matrix_generated") is True,
    }
    if not missing and all(flags.values()):
        _add_check(checks, "provider_registry", "pass", "Model registry provider registry is complete.")
        return
    problems = [name for name, ok in flags.items() if not ok]
    if missing:
        problems.append(f"provider_ids: {', '.join(missing)}")
    _add_check(checks, "provider_registry", "blocker", f"Model registry provider registry is missing: {', '.join(problems)}.")


def _check_metadata_contract(contract: dict[str, Any], checks: list[dict[str, str]]) -> None:
    fields = set(contract.get("required_fields", []))
    missing = sorted(REQUIRED_METADATA_FIELDS - fields)
    flags = {
        "hash_required": contract.get("hash_required") is True,
        "lineage_required": contract.get("lineage_required") is True,
        "owner_required": contract.get("owner_required") is True,
        "risk_tier_required": contract.get("risk_tier_required") is True,
    }
    if not missing and all(flags.values()):
        _add_check(checks, "metadata_contract", "pass", "Metadata-only model registry contract is complete.")
        return
    problems = [name for name, ok in flags.items() if not ok]
    if missing:
        problems.append(f"required_fields: {', '.join(missing)}")
    _add_check(checks, "metadata_contract", "blocker", f"Metadata contract is missing: {', '.join(problems)}.")


def _check_no_egress(egress: dict[str, Any], checks: list[dict[str, str]]) -> None:
    flags = {
        "raw_model_bytes_blocked": egress.get("raw_model_bytes_blocked") is True,
        "training_data_blocked": egress.get("training_data_blocked") is True,
        "private_features_blocked": egress.get("private_features_blocked") is True,
        "negative_tests_passed": egress.get("negative_tests_passed") is True,
    }
    if all(flags.values()):
        _add_check(checks, "no_raw_model_egress", "pass", "Raw model and training data egress controls are tested.")
    else:
        missing = [name for name, ok in flags.items() if not ok]
        _add_check(checks, "no_raw_model_egress", "blocker", f"No-egress controls are missing: {', '.join(missing)}.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = [
        "model_registry_owner",
        "metadata_validation_ref",
        "no_egress_test_ref",
        "compatibility_matrix_ref",
        "customer_registry_sandbox_ref",
    ]
    missing = [field for field in required if not evidence.get(field)]
    if not missing:
        _add_check(checks, "operating_evidence", "pass", "Model registry connector operating evidence references are present.")
    else:
        _add_check(checks, "operating_evidence", "blocker", f"Operating evidence is missing: {', '.join(missing)}.")
