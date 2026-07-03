from __future__ import annotations

from copy import deepcopy
from typing import Any


ENTERPRISE_HA_CONTRACT_VERSION = "cavra.enterprise_ha.contract.v1"
ENTERPRISE_HA_EVIDENCE_VERSION = "cavra.enterprise_ha.evidence.v1"
ENTERPRISE_HA_READINESS_VERSION = "cavra.enterprise_ha.readiness.v1"

DEFAULT_RTO_MINUTES = 60
DEFAULT_RPO_MINUTES = 15
MIN_API_REPLICAS = 2
MIN_WORKER_REPLICAS = 2


def build_enterprise_ha_contract() -> dict[str, Any]:
    return {
        "schema_version": ENTERPRISE_HA_CONTRACT_VERSION,
        "product": "CAVRA",
        "purpose": "R2.3 public-safe Enterprise high availability, disaster recovery, and residency contract.",
        "targets": {
            "rto_minutes": DEFAULT_RTO_MINUTES,
            "rpo_minutes": DEFAULT_RPO_MINUTES,
            "min_api_replicas": MIN_API_REPLICAS,
            "min_worker_replicas": MIN_WORKER_REPLICAS,
        },
        "topology_components": [
            {
                "name": "api_control_plane",
                "requirement": "Stateless API/control-plane replicas behind a managed ingress or load balancer.",
                "minimum_evidence": ["api_replicas", "stateless_api", "health.endpoints"],
            },
            {
                "name": "worker_pool",
                "requirement": "At least two asynchronous workers for connector, report, posture, and evidence jobs.",
                "minimum_evidence": ["worker_replicas", "event_bus"],
            },
            {
                "name": "event_bus",
                "requirement": "Durable queue or event bus with replay and dead-letter handling.",
                "minimum_evidence": ["durable", "dead_letter_queue", "replay_supported"],
            },
            {
                "name": "database",
                "requirement": "Managed database with zone redundancy or equivalent, PITR, and tenant-scoped controls.",
                "minimum_evidence": ["multi_az", "point_in_time_restore", "rpo_minutes"],
            },
            {
                "name": "evidence_store",
                "requirement": "Immutable or append-protected evidence store with monitored writes.",
                "minimum_evidence": ["immutable_store_enabled", "evidence_write_failure alert"],
            },
            {
                "name": "observability",
                "requirement": "Health checks, SLO alerts, queue depth, replication lag, backup failure, and evidence write alerts.",
                "minimum_evidence": ["monitor_alerts"],
            },
            {
                "name": "data_residency",
                "requirement": "Observed data locations must remain inside the tenant residency policy.",
                "minimum_evidence": ["primary_region", "allowed_regions", "observed_regions"],
            },
        ],
        "required_health_endpoints": ["/health", "/version", "/console/config"],
        "required_monitor_alerts": [
            "api_availability",
            "queue_depth",
            "db_replication_lag",
            "backup_failure",
            "evidence_write_failure",
        ],
        "required_live_evidence": [
            "topology has at least two API replicas and two worker replicas",
            "API/control plane is stateless",
            "durable event bus has replay and dead-letter handling",
            "database has multi-AZ or equivalent redundancy and PITR",
            "backup restore drill completed within RTO",
            "data loss window is within RPO",
            "failover drill completed within RTO",
            "observed data regions are inside allowed residency regions",
        ],
    }


def build_enterprise_ha_readiness(
    evidence_packet: dict[str, Any] | None = None,
    *,
    require_live: bool = False,
    rto_minutes: int = DEFAULT_RTO_MINUTES,
    rpo_minutes: int = DEFAULT_RPO_MINUTES,
) -> dict[str, Any]:
    contract = build_enterprise_ha_contract()
    if evidence_packet is None:
        checks = [
            _check("contract_documented", "pass", "Enterprise HA/DR contract is documented."),
            _check("live_evidence_packet", "warn", "No live HA/DR evidence packet supplied."),
        ]
    else:
        checks = validate_enterprise_ha_evidence_packet(
            evidence_packet,
            require_live=require_live,
            rto_minutes=rto_minutes,
            rpo_minutes=rpo_minutes,
        )["checks"]
    blockers = [check for check in checks if check["status"] == "blocker"]
    warnings = [check for check in checks if check["status"] == "warn"]
    return {
        "schema_version": ENTERPRISE_HA_READINESS_VERSION,
        "product": "CAVRA",
        "ready_for_enterprise_ha_contract": not blockers,
        "ready_for_enterprise_live_ha": not blockers and not warnings,
        "status": "blocked" if blockers else "ready_with_warnings" if warnings else "ready",
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
        "contract": contract,
        "next_controls": [
            "Run the HA/DR validator with live Enterprise deployment evidence and --require-live.",
            "Attach failover, restore, queue replay, health, and residency packets to the AISPM production gate.",
            "Promote R2.3 only after live evidence has no blockers or warnings.",
        ],
    }


def validate_enterprise_ha_evidence_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
    rto_minutes: int = DEFAULT_RTO_MINUTES,
    rpo_minutes: int = DEFAULT_RPO_MINUTES,
) -> dict[str, Any]:
    payload = deepcopy(packet)
    checks = [
        _schema_check(payload),
        _live_mode_check(payload, require_live=require_live),
        _replica_check(payload),
        _stateless_api_check(payload),
        _event_bus_check(payload),
        _database_check(payload, rpo_minutes=rpo_minutes),
        _backup_restore_check(payload, rto_minutes=rto_minutes),
        _failover_check(payload, rto_minutes=rto_minutes, rpo_minutes=rpo_minutes),
        _health_check(payload),
        _monitoring_check(payload),
        _residency_check(payload),
        _evidence_store_check(payload),
    ]
    blockers = [check for check in checks if check["status"] == "blocker"]
    warnings = [check for check in checks if check["status"] == "warn"]
    return {
        "schema_version": ENTERPRISE_HA_READINESS_VERSION,
        "product": "CAVRA",
        "ready_for_enterprise_ha_contract": not blockers,
        "ready_for_enterprise_live_ha": not blockers and not warnings,
        "status": "blocked" if blockers else "ready_with_warnings" if warnings else "ready",
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "checks": checks,
        "evidence_mode": str(payload.get("evidence_mode", "")),
    }


def _schema_check(packet: dict[str, Any]) -> dict[str, str]:
    expected = ENTERPRISE_HA_EVIDENCE_VERSION
    actual = packet.get("schema_version")
    return _check(
        "schema_version",
        "pass" if actual == expected else "blocker",
        "HA/DR evidence packet schema is valid."
        if actual == expected
        else f"HA/DR evidence packet schema must be {expected}.",
    )


def _live_mode_check(packet: dict[str, Any], *, require_live: bool) -> dict[str, str]:
    mode = str(packet.get("evidence_mode", "sample"))
    if mode == "live":
        return _check("evidence_mode", "pass", "Live HA/DR evidence packet supplied.")
    return _check(
        "evidence_mode",
        "blocker" if require_live else "warn",
        "Live HA/DR evidence is required." if require_live else "Sample HA/DR evidence validates contract shape only.",
    )


def _replica_check(packet: dict[str, Any]) -> dict[str, str]:
    deployment = _section(packet, "deployment")
    api_replicas = _int(deployment.get("api_replicas"))
    worker_replicas = _int(deployment.get("worker_replicas"))
    passed = api_replicas >= MIN_API_REPLICAS and worker_replicas >= MIN_WORKER_REPLICAS
    return _check(
        "replica_floor",
        "pass" if passed else "blocker",
        f"API and worker replica floors met ({api_replicas}/{worker_replicas})."
        if passed
        else f"Expected at least {MIN_API_REPLICAS} API replicas and {MIN_WORKER_REPLICAS} worker replicas.",
    )


def _stateless_api_check(packet: dict[str, Any]) -> dict[str, str]:
    stateless = _section(packet, "deployment").get("stateless_api") is True
    return _check(
        "stateless_api",
        "pass" if stateless else "blocker",
        "API/control plane is declared stateless." if stateless else "API/control plane must be stateless.",
    )


def _event_bus_check(packet: dict[str, Any]) -> dict[str, str]:
    bus = _section(packet, "event_bus")
    passed = bus.get("durable") is True and bus.get("dead_letter_queue") is True and bus.get("replay_supported") is True
    return _check(
        "event_bus",
        "pass" if passed else "blocker",
        "Durable event bus has DLQ and replay support."
        if passed
        else "Event bus must be durable and include dead-letter plus replay support.",
    )


def _database_check(packet: dict[str, Any], *, rpo_minutes: int) -> dict[str, str]:
    database = _section(packet, "database")
    rpo = _int(database.get("rpo_minutes"))
    passed = database.get("multi_az") is True and database.get("point_in_time_restore") is True and rpo <= rpo_minutes
    return _check(
        "database_rpo",
        "pass" if passed else "blocker",
        f"Database redundancy and RPO target met ({rpo} minutes)."
        if passed
        else f"Database must be redundant, PITR-enabled, and within {rpo_minutes} minute RPO.",
    )


def _backup_restore_check(packet: dict[str, Any], *, rto_minutes: int) -> dict[str, str]:
    backup = _section(packet, "backup_restore")
    restore_duration = _int(backup.get("restore_duration_minutes"))
    passed = backup.get("restore_tested") is True and restore_duration <= rto_minutes
    return _check(
        "backup_restore",
        "pass" if passed else "blocker",
        f"Backup restore drill completed within RTO ({restore_duration} minutes)."
        if passed
        else f"Backup restore drill must complete within {rto_minutes} minute RTO.",
    )


def _failover_check(packet: dict[str, Any], *, rto_minutes: int, rpo_minutes: int) -> dict[str, str]:
    failover = _section(packet, "failover")
    failover_minutes = _int(failover.get("failover_minutes"))
    data_loss_minutes = _int(failover.get("data_loss_minutes"))
    passed = failover.get("tested") is True and failover_minutes <= rto_minutes and data_loss_minutes <= rpo_minutes
    return _check(
        "failover_drill",
        "pass" if passed else "blocker",
        f"Failover drill met RTO/RPO ({failover_minutes}/{data_loss_minutes} minutes)."
        if passed
        else f"Failover drill must be tested within {rto_minutes} minute RTO and {rpo_minutes} minute RPO.",
    )


def _health_check(packet: dict[str, Any]) -> dict[str, str]:
    endpoints = set(_section(packet, "health").get("endpoints", []))
    required = set(build_enterprise_ha_contract()["required_health_endpoints"])
    missing = sorted(required - endpoints)
    return _check(
        "health_endpoints",
        "pass" if not missing else "blocker",
        "Required health endpoints are covered." if not missing else f"Missing health endpoints: {', '.join(missing)}.",
    )


def _monitoring_check(packet: dict[str, Any]) -> dict[str, str]:
    alerts = set(_section(packet, "health").get("monitor_alerts", []))
    required = set(build_enterprise_ha_contract()["required_monitor_alerts"])
    missing = sorted(required - alerts)
    return _check(
        "monitor_alerts",
        "pass" if not missing else "blocker",
        "Required HA/DR monitor alerts are covered." if not missing else f"Missing monitor alerts: {', '.join(missing)}.",
    )


def _residency_check(packet: dict[str, Any]) -> dict[str, str]:
    residency = _section(packet, "data_residency")
    allowed = set(residency.get("allowed_regions", []))
    observed = set(residency.get("observed_regions", []))
    missing = sorted(observed - allowed)
    passed = bool(allowed) and bool(observed) and not missing
    return _check(
        "data_residency",
        "pass" if passed else "blocker",
        "Observed data regions are inside the allowed residency policy."
        if passed
        else f"Observed regions outside residency policy: {', '.join(missing) if missing else 'missing region evidence'}.",
    )


def _evidence_store_check(packet: dict[str, Any]) -> dict[str, str]:
    evidence = _section(packet, "evidence")
    immutable = evidence.get("immutable_store_enabled") is True
    return _check(
        "evidence_store",
        "pass" if immutable else "blocker",
        "Evidence store is immutable or append-protected."
        if immutable
        else "Evidence store must be immutable or append-protected.",
    )


def _section(packet: dict[str, Any], name: str) -> dict[str, Any]:
    value = packet.get(name)
    return value if isinstance(value, dict) else {}


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _check(name: str, status: str, message: str) -> dict[str, str]:
    return {"name": name, "status": status, "message": message}
