-- CAVRA enterprise integrations inventory migration.

CREATE TABLE IF NOT EXISTS integrations (
  integration_id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  category TEXT NOT NULL,
  status TEXT NOT NULL,
  owner TEXT,
  environment TEXT,
  health_status TEXT,
  updated_at TEXT NOT NULL,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_integrations_provider
  ON integrations (provider);

CREATE INDEX IF NOT EXISTS idx_integrations_category
  ON integrations (category);

CREATE INDEX IF NOT EXISTS idx_integrations_status
  ON integrations (status);

CREATE INDEX IF NOT EXISTS idx_integrations_owner
  ON integrations (owner);

CREATE INDEX IF NOT EXISTS idx_integrations_health
  ON integrations (health_status);
