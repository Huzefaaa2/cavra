import json
import sqlite3
from pathlib import Path

from cavra.operations import (
    backup_persistent_api_stores,
    build_persistent_api_retention_plan,
    export_persistent_api_retention_plan,
    persistent_api_store_status,
    restore_persistent_api_backup,
)


def _env(tmp_path: Path) -> dict[str, str]:
    return {
        "CAVRA_ACTIVITY_STORE": str(tmp_path / "activity.json"),
        "CAVRA_INVENTORY_DB": str(tmp_path / "inventory.db"),
        "CAVRA_EVIDENCE_METADATA_STORE": str(tmp_path / "evidence.json"),
        "CAVRA_APPROVAL_STORE": str(tmp_path / "approvals.json"),
        "CAVRA_REGISTRY_STORE": str(tmp_path / "registry.json"),
    }


def test_persistent_api_store_status_reports_active_modes(tmp_path: Path) -> None:
    env = _env(tmp_path)
    Path(env["CAVRA_ACTIVITY_STORE"]).write_text('{"sessions": []}\n', encoding="utf-8")

    status = persistent_api_store_status(env)

    assert status["total"] == 5
    activity = next(item for item in status["items"] if item["name"] == "activity")
    inventory = next(item for item in status["items"] if item["name"] == "inventory")
    assert activity["kind"] == "json"
    assert activity["exists"] is True
    assert inventory["kind"] == "sqlite"


def test_backup_and_restore_persistent_api_stores(tmp_path: Path) -> None:
    env = _env(tmp_path)
    Path(env["CAVRA_ACTIVITY_STORE"]).write_text('{"sessions": [{"session_id": "s1"}]}\n', encoding="utf-8")
    with sqlite3.connect(env["CAVRA_INVENTORY_DB"]) as connection:
        connection.execute("CREATE TABLE sample (id TEXT PRIMARY KEY)")
        connection.execute("INSERT INTO sample (id) VALUES (?)", ("repo",))

    backup = backup_persistent_api_stores(tmp_path / "backup", env=env)
    restored = restore_persistent_api_backup(tmp_path / "backup" / "manifest.json", env=env, target_dir=tmp_path / "restore")

    assert len(backup["stores"]) == 5
    assert restored["restored_count"] == 2
    assert json.loads((tmp_path / "restore" / "activity.json").read_text(encoding="utf-8"))["sessions"][0]["session_id"] == "s1"
    with sqlite3.connect(tmp_path / "restore" / "inventory.db") as connection:
        assert connection.execute("SELECT id FROM sample").fetchone()[0] == "repo"


def test_restore_refuses_checksum_mismatch(tmp_path: Path) -> None:
    env = _env(tmp_path)
    Path(env["CAVRA_ACTIVITY_STORE"]).write_text('{"sessions": []}\n', encoding="utf-8")
    backup_persistent_api_stores(tmp_path / "backup", env=env)
    (tmp_path / "backup" / "stores" / "activity.json").write_text("{}\n", encoding="utf-8")

    try:
        restore_persistent_api_backup(tmp_path / "backup" / "manifest.json", env=env, target_dir=tmp_path / "restore")
    except ValueError as exc:
        assert "checksum mismatch" in str(exc)
    else:
        raise AssertionError("restore accepted a modified backup")


def test_persistent_api_retention_plan_exports_json_and_markdown(tmp_path: Path) -> None:
    result = export_persistent_api_retention_plan(tmp_path / "retention", retention_days=365, legal_hold=True, env=_env(tmp_path))
    plan = build_persistent_api_retention_plan(retention_days=365, env=_env(tmp_path))

    assert plan["retention_days"] == 365
    assert result["plan"]["legal_hold"] is True
    assert (tmp_path / "retention" / "persistent-api-retention-plan.json").exists()
    assert (tmp_path / "retention" / "persistent-api-retention-plan.md").exists()
