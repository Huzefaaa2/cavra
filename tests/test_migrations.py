import sqlite3
from pathlib import Path


def test_sqlite_evidence_metadata_migration(tmp_path: Path) -> None:
    migration = Path("migrations/sqlite/001_evidence_metadata.sql")
    database = tmp_path / "metadata.db"

    with sqlite3.connect(database) as connection:
        connection.executescript(migration.read_text(encoding="utf-8"))
        connection.execute(
            """
            INSERT INTO evidence_metadata (
                session_id, created_at, signer, decision_count, blocked_count, approval_required_count, payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("session", "2026-05-17T00:00:00Z", "security", 3, 1, 0, "{}"),
        )
        row = connection.execute("SELECT blocked_count FROM evidence_metadata WHERE session_id = ?", ("session",)).fetchone()

    assert row[0] == 1
