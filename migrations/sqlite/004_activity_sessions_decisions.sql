-- CAVRA activity persistence migration.
-- Stores runtime sessions and decisions for API and console browsing.

CREATE TABLE IF NOT EXISTS activity_sessions (
  session_id TEXT PRIMARY KEY,
  agent_id TEXT,
  actor TEXT,
  repository TEXT,
  policy_pack TEXT,
  state TEXT NOT NULL,
  started_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  decision_count INTEGER NOT NULL DEFAULT 0,
  blocked_count INTEGER NOT NULL DEFAULT 0,
  approval_required_count INTEGER NOT NULL DEFAULT 0,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_activity_sessions_agent
  ON activity_sessions (agent_id);

CREATE INDEX IF NOT EXISTS idx_activity_sessions_repository
  ON activity_sessions (repository);

CREATE INDEX IF NOT EXISTS idx_activity_sessions_policy
  ON activity_sessions (policy_pack);

CREATE INDEX IF NOT EXISTS idx_activity_sessions_updated
  ON activity_sessions (updated_at);

CREATE TABLE IF NOT EXISTS activity_decisions (
  decision_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  agent_id TEXT,
  actor TEXT,
  repository TEXT,
  policy_pack TEXT,
  action_type TEXT,
  target TEXT,
  rule_id TEXT,
  decision TEXT NOT NULL,
  severity TEXT,
  timestamp TEXT NOT NULL,
  correlation_id TEXT,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_activity_decisions_session
  ON activity_decisions (session_id);

CREATE INDEX IF NOT EXISTS idx_activity_decisions_agent
  ON activity_decisions (agent_id);

CREATE INDEX IF NOT EXISTS idx_activity_decisions_repository
  ON activity_decisions (repository);

CREATE INDEX IF NOT EXISTS idx_activity_decisions_policy
  ON activity_decisions (policy_pack);

CREATE INDEX IF NOT EXISTS idx_activity_decisions_decision
  ON activity_decisions (decision);

CREATE INDEX IF NOT EXISTS idx_activity_decisions_timestamp
  ON activity_decisions (timestamp);
