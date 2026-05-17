-- CAVRA repository inventory and policy rollout migration.

CREATE TABLE IF NOT EXISTS inventory_repositories (
  repository_id TEXT PRIMARY KEY,
  repository TEXT NOT NULL,
  provider TEXT,
  owner TEXT,
  policy_pack TEXT,
  risk_tier TEXT,
  status TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inventory_repositories_provider
  ON inventory_repositories (provider);

CREATE INDEX IF NOT EXISTS idx_inventory_repositories_owner
  ON inventory_repositories (owner);

CREATE INDEX IF NOT EXISTS idx_inventory_repositories_policy
  ON inventory_repositories (policy_pack);

CREATE INDEX IF NOT EXISTS idx_inventory_repositories_status
  ON inventory_repositories (status);

CREATE TABLE IF NOT EXISTS inventory_policy_rollouts (
  rollout_id TEXT PRIMARY KEY,
  repository TEXT NOT NULL,
  policy_pack TEXT NOT NULL,
  state TEXT NOT NULL,
  mode TEXT NOT NULL,
  owner TEXT,
  updated_at TEXT NOT NULL,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_repository
  ON inventory_policy_rollouts (repository);

CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_policy
  ON inventory_policy_rollouts (policy_pack);

CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_state
  ON inventory_policy_rollouts (state);

CREATE INDEX IF NOT EXISTS idx_inventory_rollouts_mode
  ON inventory_policy_rollouts (mode);
