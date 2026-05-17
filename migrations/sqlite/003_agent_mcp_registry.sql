-- CAVRA agent and MCP trust registry migration.
-- Stores normalized JSON payloads with indexed columns for console and API filters.

CREATE TABLE IF NOT EXISTS registry_agents (
  agent_id TEXT PRIMARY KEY,
  status TEXT NOT NULL,
  owner TEXT,
  vendor TEXT,
  risk_tier TEXT,
  last_seen TEXT,
  updated_at TEXT NOT NULL,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_registry_agents_status
  ON registry_agents (status);

CREATE INDEX IF NOT EXISTS idx_registry_agents_owner
  ON registry_agents (owner);

CREATE INDEX IF NOT EXISTS idx_registry_agents_updated_at
  ON registry_agents (updated_at);

CREATE TABLE IF NOT EXISTS registry_mcp_servers (
  server_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  trust_tier TEXT NOT NULL,
  approval_state TEXT NOT NULL,
  owner TEXT,
  capabilities TEXT NOT NULL,
  allowed_tools TEXT NOT NULL,
  last_seen TEXT,
  updated_at TEXT NOT NULL,
  payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_registry_mcp_trust_tier
  ON registry_mcp_servers (trust_tier);

CREATE INDEX IF NOT EXISTS idx_registry_mcp_approval_state
  ON registry_mcp_servers (approval_state);

CREATE INDEX IF NOT EXISTS idx_registry_mcp_owner
  ON registry_mcp_servers (owner);
