-- CAVRA R2.2 public-safe Postgres tenant/workspace RLS contract.
-- Private Managed and Enterprise deployments should apply the same predicates
-- with runtime roles that do not own these tables and do not have BYPASSRLS.

CREATE SCHEMA IF NOT EXISTS cavra;

CREATE TABLE IF NOT EXISTS cavra.tenants (
    tenant_id TEXT PRIMARY KEY,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cavra.workspaces (
    tenant_id TEXT NOT NULL REFERENCES cavra.tenants (tenant_id) ON DELETE CASCADE,
    workspace_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id)
);

CREATE TABLE IF NOT EXISTS cavra.evidence_metadata (
    tenant_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id, session_id),
    FOREIGN KEY (tenant_id, workspace_id) REFERENCES cavra.workspaces (tenant_id, workspace_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cavra.approvals (
    tenant_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    approval_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id, approval_id),
    FOREIGN KEY (tenant_id, workspace_id) REFERENCES cavra.workspaces (tenant_id, workspace_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cavra.activity_sessions (
    tenant_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id, session_id),
    FOREIGN KEY (tenant_id, workspace_id) REFERENCES cavra.workspaces (tenant_id, workspace_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cavra.activity_decisions (
    tenant_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    decision_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id, decision_id),
    FOREIGN KEY (tenant_id, workspace_id) REFERENCES cavra.workspaces (tenant_id, workspace_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cavra.inventory_repositories (
    tenant_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    repository_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id, repository_id),
    FOREIGN KEY (tenant_id, workspace_id) REFERENCES cavra.workspaces (tenant_id, workspace_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cavra.inventory_policy_rollouts (
    tenant_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    rollout_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id, rollout_id),
    FOREIGN KEY (tenant_id, workspace_id) REFERENCES cavra.workspaces (tenant_id, workspace_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cavra.integrations (
    tenant_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    integration_id TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, workspace_id, integration_id),
    FOREIGN KEY (tenant_id, workspace_id) REFERENCES cavra.workspaces (tenant_id, workspace_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_workspaces_tenant_workspace ON cavra.workspaces (tenant_id, workspace_id);
CREATE INDEX IF NOT EXISTS idx_evidence_metadata_tenant_workspace ON cavra.evidence_metadata (tenant_id, workspace_id);
CREATE INDEX IF NOT EXISTS idx_approvals_tenant_workspace ON cavra.approvals (tenant_id, workspace_id);
CREATE INDEX IF NOT EXISTS idx_activity_sessions_tenant_workspace ON cavra.activity_sessions (tenant_id, workspace_id);
CREATE INDEX IF NOT EXISTS idx_activity_decisions_tenant_workspace ON cavra.activity_decisions (tenant_id, workspace_id);
CREATE INDEX IF NOT EXISTS idx_inventory_repositories_tenant_workspace ON cavra.inventory_repositories (tenant_id, workspace_id);
CREATE INDEX IF NOT EXISTS idx_inventory_policy_rollouts_tenant_workspace ON cavra.inventory_policy_rollouts (tenant_id, workspace_id);
CREATE INDEX IF NOT EXISTS idx_integrations_tenant_workspace ON cavra.integrations (tenant_id, workspace_id);

ALTER TABLE cavra.tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.tenants FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation_tenants ON cavra.tenants
    USING (tenant_id = current_setting('cavra.tenant_id', true))
    WITH CHECK (tenant_id = current_setting('cavra.tenant_id', true));

ALTER TABLE cavra.workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.workspaces FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_workspaces ON cavra.workspaces
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );

ALTER TABLE cavra.evidence_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.evidence_metadata FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_evidence_metadata ON cavra.evidence_metadata
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );

ALTER TABLE cavra.approvals ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.approvals FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_approvals ON cavra.approvals
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );

ALTER TABLE cavra.activity_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.activity_sessions FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_activity_sessions ON cavra.activity_sessions
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );

ALTER TABLE cavra.activity_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.activity_decisions FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_activity_decisions ON cavra.activity_decisions
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );

ALTER TABLE cavra.inventory_repositories ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.inventory_repositories FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_inventory_repositories ON cavra.inventory_repositories
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );

ALTER TABLE cavra.inventory_policy_rollouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.inventory_policy_rollouts FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_inventory_policy_rollouts ON cavra.inventory_policy_rollouts
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );

ALTER TABLE cavra.integrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE cavra.integrations FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_workspace_isolation_integrations ON cavra.integrations
    USING (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    )
    WITH CHECK (
        tenant_id = current_setting('cavra.tenant_id', true)
        AND workspace_id = current_setting('cavra.workspace_id', true)
    );
