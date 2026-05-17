-- CAVRA approval router migration.

CREATE TABLE IF NOT EXISTS approvals (
  approval_id TEXT PRIMARY KEY,
  decision_id TEXT NOT NULL,
  session_id TEXT,
  state TEXT NOT NULL,
  approver_group TEXT NOT NULL,
  requested_by TEXT,
  requested_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  decided_by TEXT,
  decided_at TEXT,
  external_ref TEXT,
  break_glass INTEGER NOT NULL DEFAULT 0,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_approvals_state
  ON approvals (state);

CREATE INDEX IF NOT EXISTS idx_approvals_group
  ON approvals (approver_group);

CREATE INDEX IF NOT EXISTS idx_approvals_requested_at
  ON approvals (requested_at);
