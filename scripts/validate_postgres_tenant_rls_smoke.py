#!/usr/bin/env python3
"""Run a public-safe Postgres tenant RLS smoke check when private credentials exist."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cavra.postgres_tenancy import (  # noqa: E402
    POSTGRES_TENANT_RLS_SMOKE_VERSION,
    apply_postgres_tenant_scope,
    build_postgres_rls_smoke_plan,
)


DEFAULT_DSN_ENV = "CAVRA_ENTERPRISE_POSTGRES_DSN"
MIGRATION_PATH = ROOT / "migrations/postgres/001_tenant_scoped_operational_stores.sql"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dsn-env", default=DEFAULT_DSN_ENV, help="Environment variable containing the private DSN.")
    parser.add_argument("--tenant-a", default="tenant-smoke-a")
    parser.add_argument("--workspace-a", default="workspace-smoke-a")
    parser.add_argument("--tenant-b", default="tenant-smoke-b")
    parser.add_argument("--workspace-b", default="workspace-smoke-b")
    parser.add_argument("--smoke-id", default="cavra-rls-smoke")
    parser.add_argument("--apply-migration", action="store_true", help="Apply the public migration SQL before smoke checks.")
    parser.add_argument("--require-live", action="store_true", help="Fail instead of skipping when DSN or psycopg is missing.")
    parser.add_argument("--output", type=Path, help="Optional path for the sanitized smoke packet.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dsn = os.getenv(args.dsn_env)
    if not dsn:
        packet = _packet(
            status="skipped",
            live_rls_smoke_tested=False,
            message=f"missing DSN environment variable: {args.dsn_env}",
            args=args,
        )
        _write_packet(packet, args.output)
        print(json.dumps(packet, indent=2, sort_keys=True))
        return 1 if args.require_live else 0

    try:
        import psycopg
    except ImportError:
        packet = _packet(
            status="skipped",
            live_rls_smoke_tested=False,
            message="psycopg is not installed in this environment",
            args=args,
        )
        _write_packet(packet, args.output)
        print(json.dumps(packet, indent=2, sort_keys=True))
        return 1 if args.require_live else 0

    try:
        with psycopg.connect(dsn) as connection:
            packet = run_live_smoke(connection, args=args)
    except Exception as exc:
        packet = _packet(
            status="failed",
            live_rls_smoke_tested=False,
            message=str(exc),
            args=args,
        )
        _write_packet(packet, args.output)
        print(json.dumps(packet, indent=2, sort_keys=True))
        return 1

    _write_packet(packet, args.output)
    print(json.dumps(packet, indent=2, sort_keys=True))
    return 0 if packet["live_rls_smoke_tested"] else 1


def run_live_smoke(connection: Any, *, args: argparse.Namespace) -> dict[str, Any]:
    if args.apply_migration:
        connection.execute(MIGRATION_PATH.read_text(encoding="utf-8"))
        connection.commit()

    smoke_id = args.smoke_id
    payload = json.dumps({"source": "cavra-postgres-rls-smoke", "smoke_id": smoke_id})

    apply_postgres_tenant_scope(connection, tenant_id=args.tenant_a, workspace_id=args.workspace_a)
    connection.execute(
        """
        INSERT INTO cavra.tenants (tenant_id, payload)
        VALUES (%s, %s::jsonb)
        ON CONFLICT (tenant_id) DO UPDATE SET payload = excluded.payload, updated_at = now()
        """,
        (args.tenant_a, payload),
    )
    connection.execute(
        """
        INSERT INTO cavra.workspaces (tenant_id, workspace_id, payload)
        VALUES (%s, %s, %s::jsonb)
        ON CONFLICT (tenant_id, workspace_id) DO UPDATE SET payload = excluded.payload, updated_at = now()
        """,
        (args.tenant_a, args.workspace_a, payload),
    )
    connection.execute(
        """
        INSERT INTO cavra.integrations (tenant_id, workspace_id, integration_id, payload)
        VALUES (%s, %s, %s, %s::jsonb)
        ON CONFLICT (tenant_id, workspace_id, integration_id) DO UPDATE SET payload = excluded.payload, updated_at = now()
        """,
        (args.tenant_a, args.workspace_a, smoke_id, payload),
    )
    positive_count = _count(
        connection.execute(
            """
            SELECT COUNT(*) FROM cavra.integrations
            WHERE tenant_id = %s AND workspace_id = %s AND integration_id = %s
            """,
            (args.tenant_a, args.workspace_a, smoke_id),
        )
    )
    connection.commit()

    apply_postgres_tenant_scope(connection, tenant_id=args.tenant_b, workspace_id=args.workspace_b)
    negative_count = _count(
        connection.execute(
            """
            SELECT COUNT(*) FROM cavra.integrations
            WHERE tenant_id = %s AND workspace_id = %s AND integration_id = %s
            """,
            (args.tenant_a, args.workspace_a, smoke_id),
        )
    )
    connection.commit()

    apply_postgres_tenant_scope(connection, tenant_id=args.tenant_a, workspace_id=args.workspace_a)
    connection.execute(
        "DELETE FROM cavra.integrations WHERE tenant_id = %s AND workspace_id = %s AND integration_id = %s",
        (args.tenant_a, args.workspace_a, smoke_id),
    )
    connection.commit()

    passed = positive_count == 1 and negative_count == 0
    return _packet(
        status="pass" if passed else "failed",
        live_rls_smoke_tested=passed,
        message="Postgres tenant RLS smoke passed." if passed else "Postgres tenant RLS smoke failed.",
        args=args,
        positive_count=positive_count,
        negative_count=negative_count,
    )


def _count(cursor: Any) -> int:
    row = cursor.fetchone()
    if row is None:
        return 0
    if isinstance(row, dict):
        return int(next(iter(row.values())))
    return int(row[0])


def _packet(
    *,
    status: str,
    live_rls_smoke_tested: bool,
    message: str,
    args: argparse.Namespace,
    positive_count: int | None = None,
    negative_count: int | None = None,
) -> dict[str, Any]:
    plan = build_postgres_rls_smoke_plan(
        tenant_a=args.tenant_a,
        workspace_a=args.workspace_a,
        tenant_b=args.tenant_b,
        workspace_b=args.workspace_b,
    )
    return {
        "schema_version": POSTGRES_TENANT_RLS_SMOKE_VERSION,
        "product": "CAVRA",
        "status": status,
        "live_rls_smoke_tested": live_rls_smoke_tested,
        "message": message,
        "dsn_env": args.dsn_env,
        "dsn_value_included": False,
        "migration_applied": bool(args.apply_migration),
        "positive_count": positive_count,
        "negative_count": negative_count,
        "plan": plan,
    }


def _write_packet(packet: dict[str, Any], output: Path | None) -> None:
    if output is None:
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
