from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class StoreConfig:
    name: str
    kind: str
    path: Path
    configured_by: str


PERSISTENT_API_STORES = [
    {
        "name": "evidence_metadata",
        "json_env": "CAVRA_EVIDENCE_METADATA_STORE",
        "json_default": ".cavra/api/evidence-metadata.json",
        "sqlite_env": "CAVRA_EVIDENCE_METADATA_DB",
    },
    {
        "name": "approvals",
        "json_env": "CAVRA_APPROVAL_STORE",
        "json_default": ".cavra/api/approvals.json",
        "sqlite_env": "CAVRA_APPROVAL_DB",
    },
    {
        "name": "registry",
        "json_env": "CAVRA_REGISTRY_STORE",
        "json_default": ".cavra/api/registry.json",
        "sqlite_env": "CAVRA_REGISTRY_DB",
    },
    {
        "name": "activity",
        "json_env": "CAVRA_ACTIVITY_STORE",
        "json_default": ".cavra/api/activity.json",
        "sqlite_env": "CAVRA_ACTIVITY_DB",
    },
    {
        "name": "inventory",
        "json_env": "CAVRA_INVENTORY_STORE",
        "json_default": ".cavra/api/inventory.json",
        "sqlite_env": "CAVRA_INVENTORY_DB",
    },
    {
        "name": "integrations",
        "json_env": "CAVRA_INTEGRATION_STORE",
        "json_default": ".cavra/api/integrations.json",
        "sqlite_env": "CAVRA_INTEGRATION_DB",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def persistent_api_store_configs(env: Mapping[str, str] | None = None) -> list[StoreConfig]:
    source = os.environ if env is None else env
    configs: list[StoreConfig] = []
    for item in PERSISTENT_API_STORES:
        sqlite_env = str(item["sqlite_env"])
        json_env = str(item["json_env"])
        if source.get(sqlite_env):
            configs.append(StoreConfig(str(item["name"]), "sqlite", Path(source[sqlite_env]), sqlite_env))
        elif source.get(json_env):
            configs.append(StoreConfig(str(item["name"]), "json", Path(source[json_env]), json_env))
        else:
            configs.append(StoreConfig(str(item["name"]), "json", Path(str(item["json_default"])), "default"))
    return configs


def persistent_api_store_status(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    items = []
    for config in persistent_api_store_configs(env):
        exists = config.path.exists()
        items.append(
            {
                "name": config.name,
                "kind": config.kind,
                "path": str(config.path),
                "configured_by": config.configured_by,
                "exists": exists,
                "size_bytes": config.path.stat().st_size if exists else 0,
            }
        )
    return {"schema_version": "cavra.persistent_api.stores.v1", "product": "CAVRA", "items": items, "total": len(items)}


def backup_persistent_api_stores(
    output_dir: Path,
    *,
    env: Mapping[str, str] | None = None,
    include_missing: bool = False,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stores_dir = output_dir / "stores"
    stores_dir.mkdir(exist_ok=True)

    manifest: dict[str, Any] = {
        "schema_version": "cavra.persistent_api.backup.v1",
        "product": "CAVRA",
        "created_at": utc_now(),
        "stores": [],
    }
    for config in persistent_api_store_configs(env):
        exists = config.path.exists()
        if not exists and not include_missing:
            manifest["stores"].append(_backup_manifest_item(config, exists=False))
            continue
        extension = ".db" if config.kind == "sqlite" else ".json"
        destination = stores_dir / f"{config.name}{extension}"
        if exists:
            if config.kind == "sqlite":
                _backup_sqlite(config.path, destination)
            else:
                shutil.copy2(config.path, destination)
        else:
            destination.write_text("{}\n", encoding="utf-8")
        manifest["stores"].append(
            _backup_manifest_item(
                config,
                exists=exists,
                backup_path=destination.relative_to(output_dir),
                size_bytes=destination.stat().st_size,
                sha256=_sha256(destination),
            )
        )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def restore_persistent_api_backup(
    manifest_path: Path,
    *,
    env: Mapping[str, str] | None = None,
    target_dir: Path | None = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    backup_root = manifest_path.parent
    active_configs = {config.name: config for config in persistent_api_store_configs(env)}
    restored: list[dict[str, Any]] = []

    for item in manifest.get("stores", []):
        if not item.get("backup_path"):
            restored.append({"name": item.get("name"), "restored": False, "reason": "missing source backup"})
            continue
        name = str(item["name"])
        config = active_configs.get(name)
        if config is None:
            restored.append({"name": name, "restored": False, "reason": "unknown store"})
            continue
        source = _manifest_child_path(backup_root, str(item["backup_path"]))
        if _sha256(source) != item.get("sha256"):
            raise ValueError(f"backup checksum mismatch for {name}")
        destination = _restore_destination(config, target_dir)
        if destination.exists() and not overwrite:
            restored.append({"name": name, "restored": False, "reason": "target exists"})
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        restored.append({"name": name, "restored": True, "path": str(destination), "size_bytes": destination.stat().st_size})

    return {
        "schema_version": "cavra.persistent_api.restore.v1",
        "product": "CAVRA",
        "created_at": utc_now(),
        "source_manifest": str(manifest_path),
        "items": restored,
        "restored_count": sum(1 for item in restored if item.get("restored")),
    }


def build_persistent_api_retention_plan(
    *,
    retention_days: int = 2555,
    classification: str = "regulated-sdlc",
    legal_hold: bool = False,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    if retention_days < 1:
        raise ValueError("retention_days must be greater than zero")
    created = datetime.now(timezone.utc)
    retain_until = created + timedelta(days=retention_days)
    stores = persistent_api_store_status(env)["items"]
    return {
        "schema_version": "cavra.persistent_api.retention.v1",
        "product": "CAVRA",
        "created_at": created.isoformat(),
        "classification": classification,
        "retention_days": retention_days,
        "retain_until": retain_until.isoformat(),
        "legal_hold": legal_hold,
        "delete_protection": legal_hold or retention_days >= 365,
        "backup_frequency": "daily for production, before every migration, and before every release",
        "restore_test_frequency": "monthly for production pilots and before enterprise release candidates",
        "stores": [
            {
                **item,
                "minimum_retention_days": retention_days,
                "backup_required": True,
                "restore_test_required": True,
            }
            for item in stores
        ],
    }


def export_persistent_api_retention_plan(
    output_dir: Path,
    *,
    retention_days: int = 2555,
    classification: str = "regulated-sdlc",
    legal_hold: bool = False,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = build_persistent_api_retention_plan(
        retention_days=retention_days,
        classification=classification,
        legal_hold=legal_hold,
        env=env,
    )
    json_path = output_dir / "persistent-api-retention-plan.json"
    markdown_path = output_dir / "persistent-api-retention-plan.md"
    json_path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(render_persistent_api_retention_plan(plan), encoding="utf-8")
    return {"output_dir": str(output_dir), "files": [str(json_path), str(markdown_path)], "plan": plan}


def render_persistent_api_retention_plan(plan: dict[str, Any]) -> str:
    lines = [
        "# CAVRA Persistent API Retention Plan",
        "",
        f"Classification: `{plan['classification']}`",
        f"Retention days: `{plan['retention_days']}`",
        f"Retain until: `{plan['retain_until']}`",
        f"Legal hold: `{plan['legal_hold']}`",
        f"Delete protection: `{plan['delete_protection']}`",
        "",
        "## Stores",
        "",
        "| Store | Kind | Path | Exists | Minimum Retention |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in plan["stores"]:
        lines.append(
            f"| {item['name']} | {item['kind']} | `{item['path']}` | {item['exists']} | {item['minimum_retention_days']} days |"
        )
    lines.extend(
        [
            "",
            "## Controls",
            "",
            f"- Backup frequency: {plan['backup_frequency']}.",
            f"- Restore test frequency: {plan['restore_test_frequency']}.",
            "- Backups must be encrypted and stored outside the application runtime.",
            "- Restore tests must verify checksums, API startup, and representative search queries.",
            "",
        ]
    )
    return "\n".join(lines)


def _backup_manifest_item(
    config: StoreConfig,
    *,
    exists: bool,
    backup_path: Path | None = None,
    size_bytes: int = 0,
    sha256: str | None = None,
) -> dict[str, Any]:
    return {
        "name": config.name,
        "kind": config.kind,
        "source_path": str(config.path),
        "configured_by": config.configured_by,
        "exists": exists,
        "backup_path": str(backup_path) if backup_path else None,
        "size_bytes": size_bytes,
        "sha256": sha256,
    }


def _backup_sqlite(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(source) as source_connection, sqlite3.connect(destination) as destination_connection:
        source_connection.backup(destination_connection)


def _restore_destination(config: StoreConfig, target_dir: Path | None) -> Path:
    if target_dir is None:
        return config.path
    extension = ".db" if config.kind == "sqlite" else ".json"
    return target_dir / f"{config.name}{extension}"


def _manifest_child_path(root: Path, relative_path: str) -> Path:
    candidate = (root / relative_path).resolve()
    resolved_root = root.resolve()
    if resolved_root != candidate and resolved_root not in candidate.parents:
        raise ValueError("backup path escapes manifest directory")
    if not candidate.exists():
        raise FileNotFoundError(candidate)
    return candidate


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
