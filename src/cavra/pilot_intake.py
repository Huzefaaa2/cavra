from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PILOT_INTAKE_SCHEMA_VERSION = "cavra.final_closeout_pilot_intake.v1"
PILOT_INTAKE_RECORD_SCHEMA_VERSION = "cavra.pilot_intake.record.v1"
PILOT_INTAKE_STORE_SCHEMA_VERSION = "cavra.pilot_intake.store.v1"
READY = "ready"
PLANNED = "planned"
NEEDS_INPUT = "needs_input"
BLOCKED = "blocked"
RISKY_KEY_PARTS = {
    "api_key",
    "client_secret",
    "password",
    "private_key",
    "secret",
    "signing_key",
    "token",
    "webhook_secret",
}
RISKY_VALUE_PATTERNS = (
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_pilot_intake(payload: dict[str, Any], *, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    """Normalize a public-safe pilot intake record for local/private persistence."""

    if not isinstance(payload, dict):
        raise ValueError("pilot intake payload must be a JSON object")
    _reject_sensitive_material(payload)
    source_schema = str(payload.get("schema_version", PILOT_INTAKE_SCHEMA_VERSION))
    if source_schema != PILOT_INTAKE_SCHEMA_VERSION:
        raise ValueError(f"pilot intake schema_version must be {PILOT_INTAKE_SCHEMA_VERSION}")

    now = utc_now()
    intake_id = str(payload.get("intake_id") or existing.get("intake_id") if existing else payload.get("intake_id") or "")
    if not intake_id:
        intake_id = f"pilot-{uuid.uuid4().hex[:12]}"
    created_at = str((existing or {}).get("created_at") or payload.get("created_at") or now)
    record = {
        "schema_version": PILOT_INTAKE_RECORD_SCHEMA_VERSION,
        "intake_id": intake_id,
        "source_schema_version": source_schema,
        "generated_for": str(payload.get("generated_for", "customer-owned-private-record")),
        "pilot_objective": str(payload.get("pilot_objective", "")),
        "created_at": created_at,
        "updated_at": now,
        "created_by": str(payload.get("created_by", "console")),
        "storage_boundary": {
            "community_repo": "sample templates and API contracts only",
            "private_records": "store customer pilot responses in self-hosted Enterprise or SaaS storage",
            "sensitive_material_rejected": True,
        },
        "repositories": _list_of_dicts(payload.get("repositories", [])),
        "agents": _list_of_dicts(payload.get("agents", [])),
        "ci_cd": _dict(payload.get("ci_cd", {})),
        "connectors": _list_of_dicts(payload.get("connectors", [])),
        "identity_and_rbac": _dict(payload.get("identity_and_rbac", {})),
        "retention": _dict(payload.get("retention", {})),
        "enterprise_or_saas_handoff": _dict(payload.get("enterprise_or_saas_handoff", {})),
        "success_criteria": _string_list(payload.get("success_criteria", [])),
        "evidence_refs": _string_list(payload.get("evidence_refs", [])),
        "notes": str(payload.get("notes", "")),
    }
    record["readiness"] = build_pilot_readiness(record)
    return record


def build_pilot_readiness(record: dict[str, Any]) -> dict[str, Any]:
    repositories = _list_of_dicts(record.get("repositories", []))
    agents = _list_of_dicts(record.get("agents", []))
    ci_cd = _dict(record.get("ci_cd", {}))
    connectors = _list_of_dicts(record.get("connectors", []))
    identity = _dict(record.get("identity_and_rbac", {}))
    retention = _dict(record.get("retention", {}))
    handoff = _dict(record.get("enterprise_or_saas_handoff", {}))
    areas = [
        _area(
            "repository_agent",
            READY if repositories and agents and _has_required_check(repositories) else NEEDS_INPUT,
            "Repository scope and transparent agent inventory are ready."
            if repositories and agents and _has_required_check(repositories)
            else "Add scoped repositories, protected branches, required checks, and transparent agent identities.",
        ),
        _area(
            "ci_cd",
            READY if _present(ci_cd.get("platform")) and _present(ci_cd.get("required_check")) else NEEDS_INPUT,
            "CI/CD enforcement path is mapped."
            if _present(ci_cd.get("platform")) and _present(ci_cd.get("required_check"))
            else "Add CI/CD platform, required check, evidence path, and failure behavior.",
        ),
        _area("connectors", _connector_status(connectors), _connector_message(connectors)),
        _area(
            "sso_rbac",
            READY if _present(identity.get("identity_provider")) and _has_group(identity) else NEEDS_INPUT,
            "Identity provider and approver groups are mapped."
            if _present(identity.get("identity_provider")) and _has_group(identity)
            else "Map identity provider and approver groups before paid pilot enablement.",
        ),
        _area(
            "retention_audit",
            READY if int(retention.get("retention_days", 0) or 0) > 0 and _present(retention.get("archive_destination")) else PLANNED,
            "Retention window and archive destination are ready."
            if int(retention.get("retention_days", 0) or 0) > 0 and _present(retention.get("archive_destination"))
            else "Confirm retention window, archive destination, and exception owner.",
        ),
        _area(
            "enterprise_saas_handoff",
            READY
            if _present(handoff.get("preferred_deployment"))
            and _present(handoff.get("commercial_owner"))
            and _present(handoff.get("target_pilot_start"))
            else NEEDS_INPUT,
            "Deployment path, commercial owner, and pilot start date are ready."
            if _present(handoff.get("preferred_deployment"))
            and _present(handoff.get("commercial_owner"))
            and _present(handoff.get("target_pilot_start"))
            else "Select Enterprise or SaaS deployment path and assign commercial owner.",
        ),
    ]
    status_values = [str(item["status"]) for item in areas]
    if BLOCKED in status_values:
        overall = BLOCKED
    elif NEEDS_INPUT in status_values:
        overall = NEEDS_INPUT
    elif PLANNED in status_values:
        overall = PLANNED
    else:
        overall = READY
    return {
        "schema_version": "cavra.pilot_intake.readiness.v1",
        "overall_status": overall,
        "area_count": len(areas),
        "ready_count": sum(1 for item in areas if item["status"] == READY),
        "needs_input_count": sum(1 for item in areas if item["status"] == NEEDS_INPUT),
        "planned_count": sum(1 for item in areas if item["status"] == PLANNED),
        "areas": areas,
    }


class PilotIntakeStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list(
        self,
        *,
        overall_status: str | None = None,
        repository: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        items = self._load()["pilot_intakes"]
        if overall_status:
            items = [item for item in items if item.get("readiness", {}).get("overall_status") == overall_status]
        if repository:
            items = [
                item
                for item in items
                if repository in [str(repo.get("repository", "")) for repo in _list_of_dicts(item.get("repositories", []))]
            ]
        items = sorted(items, key=lambda item: (str(item.get("updated_at", "")), str(item.get("intake_id", ""))), reverse=True)
        return {"items": items[offset : offset + limit], "total": len(items), "limit": limit, "offset": offset}

    def upsert(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = self._load()
        existing = None
        intake_id = payload.get("intake_id")
        if intake_id:
            existing = next((item for item in data["pilot_intakes"] if item.get("intake_id") == intake_id), None)
        record = normalize_pilot_intake(payload, existing=existing)
        data["pilot_intakes"] = [item for item in data["pilot_intakes"] if item.get("intake_id") != record["intake_id"]]
        data["pilot_intakes"].append(record)
        self._save(data)
        return record

    def get(self, intake_id: str) -> dict[str, Any] | None:
        return next((item for item in self._load()["pilot_intakes"] if item.get("intake_id") == intake_id), None)

    def _load(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists():
            return {"pilot_intakes": []}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return {"pilot_intakes": list(payload.get("pilot_intakes", []))}

    def _save(self, payload: dict[str, list[dict[str, Any]]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"schema_version": PILOT_INTAKE_STORE_SCHEMA_VERSION, **payload}, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )


def _area(area: str, status: str, message: str) -> dict[str, str]:
    return {"area": area, "status": status, "message": message}


def _connector_status(connectors: list[dict[str, Any]]) -> str:
    if not connectors:
        return NEEDS_INPUT
    statuses = {str(item.get("status", "")).lower().replace("-", "_") for item in connectors}
    if statuses & {"blocked", "failed"}:
        return BLOCKED
    if statuses & {"ready", "tested", "active", "configured"}:
        return READY
    return PLANNED


def _connector_message(connectors: list[dict[str, Any]]) -> str:
    if not connectors:
        return "Add at least one non-production connector or audit handoff route."
    if _connector_status(connectors) == READY:
        return "Connector route is ready for pilot validation."
    if _connector_status(connectors) == BLOCKED:
        return "Connector route is blocked and needs owner action."
    return "Connector route is planned and needs test evidence."


def _has_required_check(repositories: list[dict[str, Any]]) -> bool:
    return any(_string_list(item.get("required_checks", [])) for item in repositories)


def _has_group(identity: dict[str, Any]) -> bool:
    return any(str(key).endswith("_group") and _present(value) for key, value in identity.items())


def _present(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return bool(text) and text not in {"to-be-confirmed", "tbd", "none", "missing"}


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _reject_sensitive_material(payload: Any, *, path: str = "$") -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key).lower()
            if any(part in key_text for part in RISKY_KEY_PARTS):
                raise ValueError(f"pilot intake contains sensitive field at {path}.{key}")
            _reject_sensitive_material(value, path=f"{path}.{key}")
        return
    if isinstance(payload, list):
        for index, value in enumerate(payload):
            _reject_sensitive_material(value, path=f"{path}[{index}]")
        return
    if isinstance(payload, str):
        for pattern in RISKY_VALUE_PATTERNS:
            if pattern.search(payload):
                raise ValueError(f"pilot intake contains sensitive value at {path}")
