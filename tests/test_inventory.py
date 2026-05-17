from pathlib import Path

from cavra.inventory import InventoryStore, SQLiteInventoryStore


def _repository() -> dict[str, object]:
    return {
        "repository": "payments/api",
        "provider": "github",
        "owner": "Payments Platform",
        "business_unit": "payments",
        "environment": "production",
        "policy_pack": "cavra-banking",
        "risk_tier": "high",
        "protected_branches": ["main", "release/*"],
        "required_checks": ["cavra", "CodeQL"],
    }


def _rollout() -> dict[str, object]:
    return {
        "rollout_id": "payments-api-banking",
        "repository": "payments/api",
        "policy_pack": "cavra-banking",
        "policy_version": "2026.05",
        "mode": "strict",
        "state": "active",
        "owner": "Platform Security",
        "coverage_percent": 95,
    }


def test_inventory_store_persists_repository_and_rollout(tmp_path: Path) -> None:
    store = InventoryStore(tmp_path / "inventory.json")

    repo = store.upsert_repository(_repository())
    rollout = store.upsert_policy_rollout(_rollout())

    assert repo["repository_id"] == "payments/api"
    assert rollout["mode"] == "strict"
    assert store.list_repositories(owner="Payments Platform")["total"] == 1
    assert store.list_policy_rollouts(repository="payments/api", state="active")["total"] == 1
    assert store.get_repository("payments/api")["risk_tier"] == "high"
    assert store.get_policy_rollout("payments-api-banking")["coverage_percent"] == 95


def test_sqlite_inventory_store_filters_records(tmp_path: Path) -> None:
    store = SQLiteInventoryStore(tmp_path / "inventory.db")

    store.upsert_repository(_repository())
    store.upsert_policy_rollout(_rollout())
    store.upsert_repository({**_repository(), "repository": "docs/site", "owner": "Docs", "policy_pack": "cavra-ai-agent-baseline", "risk_tier": "low"})

    assert store.list_repositories(policy_pack="cavra-banking")["total"] == 1
    assert store.list_repositories(risk_tier="low")["items"][0]["repository"] == "docs/site"
    assert store.list_policy_rollouts(mode="strict")["total"] == 1
