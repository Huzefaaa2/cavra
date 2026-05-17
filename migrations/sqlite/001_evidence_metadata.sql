-- CAVRA evidence metadata migration.
-- Applies to SQLite-backed pilots and self-hosted development deployments.

CREATE TABLE IF NOT EXISTS evidence_metadata (
  session_id TEXT PRIMARY KEY,
  created_at TEXT,
  signer TEXT,
  decision_count INTEGER NOT NULL DEFAULT 0,
  blocked_count INTEGER NOT NULL DEFAULT 0,
  approval_required_count INTEGER NOT NULL DEFAULT 0,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_evidence_metadata_created_at
  ON evidence_metadata (created_at);

CREATE INDEX IF NOT EXISTS idx_evidence_metadata_signer
  ON evidence_metadata (signer);

CREATE INDEX IF NOT EXISTS idx_evidence_metadata_blocked_count
  ON evidence_metadata (blocked_count);
