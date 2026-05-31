const scenario = [
  ["read_file", ".env", "block", "filesystem.read.block", "Secrets file cannot be exposed to AI-agent context."],
  ["write_file", "iam/admin-role.tf", "require_approval", "filesystem.write.require_approval", "IAM privilege change in regulated repository requires security approval."],
  ["execute_command", "terraform plan", "allow", "commands.allow", "Read-only infrastructure planning command is permitted."],
  ["execute_command", "terraform apply -auto-approve", "block", "commands.block", "Autonomous production-impacting infrastructure change is prohibited."],
  ["mcp_tool_call", "unknown filesystem MCP server", "block", "mcp.server.trust.block_unknown", "Untrusted MCP server with filesystem capability is not approved."],
  ["git_operation", "git push origin main", "block", "git.protected_branch.block_direct_push", "Direct push to protected branch is prohibited."],
  ["pull_request", "create PR", "allow_with_attestation", "git.pull_request.allow_with_attestation", "PR is allowed with CAVRA evidence and reviewer guidance."]
];

const evidenceCatalog = [
  {
    session_id: "demo-session",
    signer: "platform-security",
    decision_count: 7,
    blocked_count: 4,
    approval_required_count: 1,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: scenario.map(eventPayload),
    attestation_targets: scenario.map((row) => row[1]),
    artifact_count: 7
  },
  {
    session_id: "docs-agent-run",
    signer: "docs-agent",
    decision_count: 4,
    blocked_count: 0,
    approval_required_count: 0,
    retention: { retention_days: 365, retain_until: "2027-05-17T00:00:00Z" },
    decisions: scenario.slice(2, 6).map(eventPayload),
    attestation_targets: scenario.slice(2, 6).map((row) => row[1]),
    artifact_count: 7
  },
  {
    session_id: "security-review",
    signer: "security-agent",
    decision_count: 5,
    blocked_count: 2,
    approval_required_count: 1,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: scenario.slice(0, 5).map(eventPayload),
    attestation_targets: scenario.slice(0, 5).map((row) => row[1]),
    artifact_count: 7
  },
  {
    session_id: "prod-v0.2.0-rc.1-rollout",
    signer: "release-agent",
    metadata_kind: "managed-endpoint-rollout",
    rollout_status: "staged",
    rollout_ring: "pilot",
    environment: "production",
    change_record: "CHG-123",
    deployment_targets: ["github-actions-linux-amd64-runner", "linux-systemd-amd64-workstation"],
    release: { version: "v0.2.0-rc.1", commit: "sample" },
    promotion_readiness: {
      status: "ready",
      rationale: "Rollout evidence is checksum-verified and the rollout state can proceed."
    },
    decision_count: 0,
    blocked_count: 0,
    approval_required_count: 0,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: [],
    attestation_targets: [],
    artifact_count: 3
  },
  {
    session_id: "rpe-prod-v0.2.0-rc.1",
    signer: "release-manager",
    metadata_kind: "rollout-promotion-execution",
    rollout_id: "prod-v0.2.0-rc.1-rollout",
    rollout_status: "promoted",
    promotion_execution_status: "executed",
    current_ring: "pilot",
    target_ring: "production",
    approval_state: "approved",
    approval_id: "apr_sample_prod_ring",
    request_id: "rpr_sample_prod_ring",
    environment: "production",
    change_record: "CHG-123",
    deployment_targets: ["github-actions-linux-amd64-runner", "linux-systemd-amd64-workstation"],
    rollback_evidence_refs: [
      { target: "github-actions-linux-amd64-runner", ref: "rollback://prod-v0.2.0-rc.1-rollout/github-actions-linux-amd64-runner/1", step: "Restore previous signed runtime package." }
    ],
    audit_links: {
      rollout: "rollout://prod-v0.2.0-rc.1-rollout",
      promotion_request: "promotion-request://rpr_sample_prod_ring",
      approval: "approval://apr_sample_prod_ring",
      change: "change://CHG-123"
    },
    execution: {
      execution_id: "rpe-prod-v0.2.0-rc.1",
      execution_status: "executed",
      ring_advancement: { from: "pilot", to: "production", new_rollout_status: "promoted" }
    },
    decision_count: 0,
    blocked_count: 0,
    approval_required_count: 0,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: [],
    attestation_targets: [],
    artifact_count: 0
  },
  {
    session_id: "rre-prod-v0.2.0-rc.1",
    signer: "release-manager",
    metadata_kind: "rollout-rollback-execution",
    rollout_id: "prod-v0.2.0-rc.1-rollout",
    rollout_status: "rolled_back",
    rollback_execution_status: "executed",
    current_ring: "production",
    target_ring: "pilot",
    approval_state: "approved",
    approval_id: "apr_sample_prod_rollback",
    promotion_execution_id: "rpe-prod-v0.2.0-rc.1",
    environment: "production",
    change_record: "CHG-123",
    deployment_targets: ["github-actions-linux-amd64-runner", "linux-systemd-amd64-workstation"],
    rollback_evidence_refs: [
      { target: "github-actions-linux-amd64-runner", ref: "rollback://prod-v0.2.0-rc.1-rollout/github-actions-linux-amd64-runner/1", step: "Restore previous signed runtime package." }
    ],
    audit_links: {
      rollout: "rollout://prod-v0.2.0-rc.1-rollout",
      promotion_execution: "promotion-execution://rpe-prod-v0.2.0-rc.1",
      approval: "approval://apr_sample_prod_rollback",
      change: "change://CHG-123"
    },
    decision_count: 0,
    blocked_count: 0,
    approval_required_count: 0,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: [],
    attestation_targets: [],
    artifact_count: 0
  }
];

const evidenceArtifactCatalog = [
  ["manifest.json", "manifest", "application/json", "Manifest with checksums and signature metadata."],
  ["evidence.json", "evidence", "application/json", "Complete decision evidence for the session."],
  ["pr-attestation.md", "attestation", "text/markdown", "Reviewer-ready PR attestation."],
  ["compliance-mapping.md", "compliance", "text/markdown", "Audit control-objective mapping."],
  ["siem-event.json", "siem", "application/json", "SIEM-ready session event payload."],
  ["sandbox-run-summary.json", "summary", "application/json", "Compact session summary."],
  ["retention-policy.json", "retention", "application/json", "Retention, legal hold, and disposition policy."]
].map(([artifact, kind, media_type, description]) => ({
  artifact, kind, media_type, description, bytes: 1024, sha256: "sample"
}));

const rolloutArtifactCatalog = [
  ["managed-endpoint-rollout-evidence.json", "rollout-evidence", "application/json", "Verified managed endpoint rollout evidence payload."],
  ["managed-endpoint-rollout-evidence.md", "rollout-summary", "text/markdown", "Reviewer-ready managed endpoint rollout evidence summary."],
  ["checksums.txt", "rollout-checksums", "text/plain", "Checksums for managed endpoint rollout evidence files."]
].map(([artifact, kind, media_type, description]) => ({
  artifact, kind, media_type, description, bytes: 1024, sha256: "sample"
}));

const rolloutPromotionRequests = new Map();
let evidenceMetadataCache = [];

const releaseConnectorDeliveryCatalog = [
  {
    session_id: "rcd-rpe-prod-v0-2-0-rc-1-sample",
    metadata_kind: "release-connector-delivery",
    created_at: "2026-05-19T00:10:00+00:00",
    event_id: "rpe-prod-v0.2.0-rc.1",
    event_type: "cavra.rollout_promotion_execution",
    delivery_success: true,
    providers: ["splunk", "jira"],
    failed_providers: [],
    attempt_count: 2,
    max_attempt_count: 1,
    delivery_evidence: ".cavra/release/promotion-audit-deliveries/rpe-prod-v0.2.0-rc.1-connector-delivery.json"
  },
  {
    session_id: "rcd-rre-prod-v0-2-0-rc-1-sample",
    metadata_kind: "release-connector-delivery",
    created_at: "2026-05-19T00:20:00+00:00",
    event_id: "rre-prod-v0.2.0-rc.1",
    event_type: "cavra.rollout_rollback_execution",
    delivery_success: false,
    providers: ["webhook"],
    failed_providers: ["webhook"],
    attempt_count: 2,
    max_attempt_count: 2,
    delivery_evidence: ".cavra/release/rollback-deliveries/rre-prod-v0.2.0-rc.1-connector-delivery.json"
  }
];

const goRollbackDrillNotificationCatalog = [
  {
    session_id: "gordplan-go-backend-python-fallback-monthly",
    metadata_kind: "go-backend-rollback-drill-notification-plan",
    created_at: "2026-05-20T10:00:00+00:00",
    signer: "release-governance",
    plan_id: "gordplan-go-backend-python-fallback-monthly",
    schedule_id: "go_backend_python_fallback_monthly",
    alert_level: "critical",
    selected_providers: ["slack", "teams"],
    acknowledgement_required_providers: ["slack", "teams"],
    deliverable_route_count: 2,
    suppressed_route_count: 1,
    maintenance_suppressed_count: 1,
    calendar_suppressed_count: 0,
    plan: {
      schema_version: "cavra.go-backend-pilot.rollback-drill-notification-plan.v1",
      product: "CAVRA",
      plan_id: "gordplan-go-backend-python-fallback-monthly",
      schedule_id: "go_backend_python_fallback_monthly",
      generated_at: "2026-05-20T10:00:00+00:00",
      generated_by: "release-governance",
      alert_level: "critical",
      selected_providers: ["slack", "teams"],
      acknowledgement_required_providers: ["slack", "teams"],
      route_decisions: [
        { schedule_id: "go_backend_python_fallback_monthly", plan_id: "gordplan-go-backend-python-fallback-monthly", provider: "slack", owner: "release-governance", action: "deliver", acknowledgement_minutes: 45, reason: "stale rollback drill requires owner acknowledgement" },
        { schedule_id: "go_backend_python_fallback_monthly", plan_id: "gordplan-go-backend-python-fallback-monthly", provider: "teams", owner: "platform-operations", action: "deliver", acknowledgement_minutes: 60, reason: "stale rollback drill requires owner acknowledgement" },
        { schedule_id: "go_backend_python_fallback_monthly", plan_id: "gordplan-go-backend-python-fallback-monthly", provider: "webhook", owner: "release-governance", action: "suppress", category: "maintenance_window", reason: "approved maintenance window is active" }
      ],
      controls: [
        "routing-policy-derived-from-public-safe-owner-metadata",
        "notification-plan-does-not-mutate-runtime-mode"
      ]
    }
  },
  {
    session_id: "rcd-gordplan-go-backend-python-fallback-monthly",
    metadata_kind: "release-connector-delivery",
    connector_delivery_source: "go_backend_rollback_drill_notification",
    created_at: "2026-05-20T10:02:00+00:00",
    event_id: "go_backend_python_fallback_monthly",
    event_type: "cavra.go_backend.rollback_drill_notification",
    delivery_success: false,
    providers: ["slack", "teams"],
    failed_providers: ["teams"],
    attempt_count: 2,
    max_attempt_count: 2,
    delivery_evidence: ".cavra/release/go-backend-rollback-drill-notification-delivery.json"
  },
  {
    session_id: "gordack-go-backend-python-fallback-monthly-slack",
    metadata_kind: "go-backend-rollback-drill-notification-ack",
    created_at: "2026-05-20T10:20:00+00:00",
    signer: "release-manager",
    acknowledgement_id: "gordack-go-backend-python-fallback-monthly-slack",
    schedule_id: "go_backend_python_fallback_monthly",
    plan_id: "gordplan-go-backend-python-fallback-monthly",
    provider: "slack",
    acknowledgement_state: "acknowledged",
    acknowledgement: {
      schema_version: "cavra.go-backend-pilot.rollback-drill-notification-ack.v1",
      product: "CAVRA",
      acknowledgement_id: "gordack-go-backend-python-fallback-monthly-slack",
      schedule_id: "go_backend_python_fallback_monthly",
      plan_id: "gordplan-go-backend-python-fallback-monthly",
      provider: "slack",
      acknowledged_by: "release-manager",
      acknowledgement_state: "acknowledged",
      acknowledged_at: "2026-05-20T10:20:00+00:00",
      external_ref: "CHG-123",
      notes: "Rollback drill follow-up accepted by release governance."
    }
  },
  {
    session_id: "gordesc-go-backend-python-fallback-monthly",
    metadata_kind: "go-backend-rollback-drill-notification-escalation-plan",
    created_at: "2026-05-20T11:10:00+00:00",
    signer: "release-governance",
    plan_id: "gordesc-go-backend-python-fallback-monthly",
    alert_level: "critical",
    escalation_plan: {
      schema_version: "cavra.go-backend-pilot.rollback-drill-notification-escalation-plan.v1",
      product: "CAVRA",
      plan_id: "gordesc-go-backend-python-fallback-monthly",
      generated_at: "2026-05-20T11:10:00+00:00",
      generated_by: "release-governance",
      alert_level: "critical",
      acknowledgement_minutes: 60,
      route_count: 2,
      outstanding_count: 1,
      breached_count: 1,
      routes: [
        { schedule_id: "go_backend_python_fallback_monthly", plan_id: "gordplan-go-backend-python-fallback-monthly", provider: "slack", owner: "release-governance", acknowledgement_state: "acknowledged", acknowledged: true, age_minutes: 70, acknowledgement_minutes: 45, breached: false, recommended_action: "no_action" },
        { schedule_id: "go_backend_python_fallback_monthly", plan_id: "gordplan-go-backend-python-fallback-monthly", provider: "teams", owner: "platform-operations", acknowledgement_state: "outstanding", acknowledged: false, age_minutes: 70, acknowledgement_minutes: 60, breached: true, recommended_action: "escalate_missed_drill_notification" }
      ]
    }
  }
];

const releaseChannelPromotionCatalog = [
  {
    session_id: "rcp-stable-v0.2.0-rc.1",
    metadata_kind: "release-channel-promotion-request",
    created_at: "2026-05-19T00:00:00+00:00",
    request_id: "rcp-stable-v0.2.0-rc.1",
    channel: "stable",
    target_ring: "enterprise",
    approval_id: "apr_channel_stable",
    approval_state: "pending",
    deployment_targets: ["linux-systemd-amd64-workstation", "macos-jamf-arm64-workstation"],
    endpoint_management_tools: ["linux", "jamf"],
    release: { version: "v0.2.0-rc.1", commit: "sample" }
  }
];

const endpointManagementExportCatalog = [
  {
    session_id: "eme-stable-v0.2.0-rc.1",
    metadata_kind: "endpoint-management-export",
    created_at: "2026-05-19T00:05:00+00:00",
    export_id: "eme-stable-v0.2.0-rc.1",
    channel: "stable",
    provider: "all",
    providers: ["jamf", "linux"],
    approval_id: "apr_channel_stable",
    approval_state: "pending",
    request_id: "rcp-stable-v0.2.0-rc.1",
    files: ["jamf-policy.json", "linux-fleet-manifest.json", "checksums.txt"],
    release: { version: "v0.2.0-rc.1", commit: "sample" }
  }
];

const endpointPublicationDeliveryCatalog = [
  {
    session_id: "epd-emp-stable-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-management-publication-delivery",
    created_at: "2026-05-19T00:12:00+00:00",
    publication_id: "emp-stable-v0.2.0-rc.1",
    event_id: "emp-stable-v0.2.0-rc.1",
    export_id: "eme-stable-v0.2.0-rc.1",
    channel: "stable",
    delivery_success: false,
    providers: ["jamf"],
    failed_providers: ["jamf"],
    attempt_count: 1,
    max_attempt_count: 1,
    delivery_evidence: ".cavra/release/endpoint-publication-deliveries/emp-stable-v0.2.0-rc.1-connector-delivery.json"
  }
];

const endpointReconciliationCatalog = [
  {
    session_id: "mer-prod-v0-2-0-rc-1-sample",
    metadata_kind: "managed-endpoint-reconciliation",
    reconciliation_id: "mer-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T00:30:00+00:00",
    observed_at: "2026-05-19T00:25:00+00:00",
    drift_status: "drift_detected",
    alert_level: "critical",
    release: { version: "v0.2.0-rc.1", commit: "sample" },
    deployment_targets: ["linux-systemd-amd64-workstation", "macos-jamf-arm64-workstation"],
    desired_target_count: 2,
    observed_endpoint_count: 3,
    compliant_endpoint_count: 2,
    drifted_endpoint_count: 1,
    missing_target_count: 0,
    stale_endpoint_count: 0
  }
];

const endpointInventoryCatalog = [
  {
    session_id: "eii-linux-stable-sample",
    metadata_kind: "endpoint-inventory-ingestion",
    inventory_id: "eii-linux-stable-sample",
    provider: "linux",
    channel: "stable",
    created_at: "2026-05-19T00:20:00+00:00",
    observed_at: "2026-05-19T00:19:00+00:00",
    endpoint_count: 2,
    deployment_targets: ["linux-systemd-amd64-workstation"],
    missing_target_count: 0,
    version_count: 2,
    checksum_count: 2
  },
  {
    session_id: "eii-jamf-stable-sample",
    metadata_kind: "endpoint-inventory-ingestion",
    inventory_id: "eii-jamf-stable-sample",
    provider: "jamf",
    channel: "stable",
    created_at: "2026-05-19T00:24:00+00:00",
    observed_at: "2026-05-19T00:22:00+00:00",
    endpoint_count: 1,
    deployment_targets: ["macos-jamf-arm64-workstation"],
    missing_target_count: 0,
    version_count: 1,
    checksum_count: 1
  }
];

const endpointInventoryFreshnessCatalog = [
  {
    session_id: "eif-stable-sample",
    metadata_kind: "endpoint-inventory-freshness-report",
    report_id: "eif-stable-sample",
    created_at: "2026-05-20T00:00:00+00:00",
    alert_level: "warning",
    max_age_hours: 24,
    critical_age_hours: 48,
    warning_count: 1,
    critical_count: 0,
    alert_count: 1,
    latest_ingestions: [
      {
        inventory_id: "eii-linux-stable-sample",
        provider: "linux",
        channel: "stable",
        deployment_target: "linux-systemd-amd64-workstation",
        age_hours: 25,
        severity: "warning"
      }
    ],
    alerts: [
      {
        severity: "warning",
        provider: "linux",
        channel: "stable",
        deployment_target: "linux-systemd-amd64-workstation",
        message: "Latest endpoint inventory for linux/stable/linux-systemd-amd64-workstation is 25h old."
      }
    ]
  }
];

const endpointRemediationCatalog = [
  {
    session_id: "err-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-drift-remediation-request",
    request_id: "err-prod-v0-2-0-rc-1-sample",
    reconciliation_id: "mer-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T00:34:00+00:00",
    strategy: "mixed",
    action_count: 2,
    approval_id: "apr_endpoint_remediation_sample",
    approval_state: "pending",
    alert_level: "critical"
  },
  {
    session_id: "ere-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-drift-remediation-execution",
    execution_id: "ere-prod-v0-2-0-rc-1-sample",
    request_id: "err-prod-v0-2-0-rc-1-sample",
    reconciliation_id: "mer-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T00:42:00+00:00",
    strategy: "mixed",
    action_count: 2,
    approval_id: "apr_endpoint_remediation_sample",
    approval_state: "approved",
    execution_status: "recorded"
  }
];

const endpointRemediationHandoffCatalog = [
  {
    session_id: "erh-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-remediation-handoff",
    handoff_id: "erh-prod-v0-2-0-rc-1-sample",
    request_id: "err-prod-v0-2-0-rc-1-sample",
    reconciliation_id: "mer-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T00:36:00+00:00",
    providers: ["jira", "servicenow", "slack", "teams", "private_queue"],
    provider_count: 5,
    action_count: 2,
    approval_id: "apr_endpoint_remediation_sample",
    approval_state: "pending",
    delivery_mode: "manual"
  }
];

const endpointRemediationHandoffStatusCatalog = [
  {
    session_id: "erhs-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-remediation-handoff-status",
    status_id: "erhs-prod-v0-2-0-rc-1-sample",
    handoff_id: "erh-prod-v0-2-0-rc-1-sample",
    request_id: "err-prod-v0-2-0-rc-1-sample",
    reconciliation_id: "mer-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T00:48:00+00:00",
    provider: "private_queue",
    handoff_status: "completed",
    external_ref: "queue-job-123",
    approval_id: "apr_endpoint_remediation_sample",
    approval_state: "approved",
    action_count: 2
  }
];

const endpointRemediationSlaCatalog = [
  {
    session_id: "ersla-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-remediation-sla-report",
    report_id: "ersla-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T01:00:00+00:00",
    alert_level: "healthy",
    tracked_work_item_count: 1,
    completed_count: 1,
    at_risk_count: 0,
    breached_count: 0,
    completion_rate: 1,
    escalation_count: 0
  }
];

const endpointRecurrenceRetryPlanCatalog = [
  {
    session_id: "erslaescrtry-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-remediation-sla-escalation-recurrence-retry-plan",
    retry_plan_id: "erslaescrtry-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T01:25:00+00:00",
    alert_level: "critical",
    retryable_count: 1,
    waiting_count: 1,
    suppressed_count: 0,
    retry_plan: {
      schema_version: "cavra.endpoint_remediation_sla.escalation_recurrence_retry_plan.v1",
      product: "CAVRA",
      retry_plan_id: "erslaescrtry-prod-v0-2-0-rc-1-sample",
      generated_at: "2026-05-19T01:25:00+00:00",
      generated_by: "release-manager",
      alert_level: "critical",
      decision_count: 2,
      retryable_count: 1,
      waiting_count: 1,
      suppressed_count: 0,
      max_retry_attempts: 3,
      base_retry_delay_minutes: 15,
      backoff_multiplier: 2,
      retry_decisions: [
        {
          recurrence_plan_id: "erslaescr-prod-v0-2-0-rc-1-sample",
          plan_id: "erslaesc-prod-v0-2-0-rc-1-sample",
          provider: "webhook",
          action: "retry",
          reason: "failed recurrence delivery is eligible for retry",
          retry_count: 1,
          max_retry_attempts: 3,
          retry_delay_minutes: 15,
          latest_delivery_id: "rcd-prod-v0-2-0-rc-1-sample",
          latest_delivery_at: "2026-05-19T01:08:00+00:00",
          next_retry_at: "2026-05-19T01:23:00+00:00",
          route_count: 1,
          routes: [{ owner: "release-governance", provider: "webhook", route_key: "release-governance:webhook" }]
        },
        {
          recurrence_plan_id: "erslaescr-prod-v0-2-0-rc-1-sample",
          plan_id: "erslaesc-prod-v0-2-0-rc-1-sample",
          provider: "slack",
          action: "wait",
          reason: "retry delay 30 minutes has not elapsed",
          retry_count: 2,
          max_retry_attempts: 3,
          retry_delay_minutes: 30,
          latest_delivery_id: "rcd-prod-v0-2-0-rc-1-slack-sample",
          latest_delivery_at: "2026-05-19T01:18:00+00:00",
          next_retry_at: "2026-05-19T01:48:00+00:00",
          route_count: 1,
          routes: [{ owner: "release-governance", provider: "slack", route_key: "release-governance:slack" }]
        }
      ]
    }
  }
];

const endpointRecurrenceOwnerDigestCatalog = [
  {
    session_id: "erslaescdigest-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-remediation-sla-escalation-owner-digest",
    digest_id: "erslaescdigest-prod-v0-2-0-rc-1-sample",
    recurrence_plan_id: "erslaescr-prod-v0-2-0-rc-1-sample",
    retry_plan_id: "erslaescrtry-prod-v0-2-0-rc-1-sample",
    plan_id: "erslaesc-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T01:30:00+00:00",
    owner_count: 1,
    unresolved_route_count: 2,
    owner_digest: {
      schema_version: "cavra.endpoint_remediation_sla.escalation_owner_digest.v1",
      product: "CAVRA",
      event_type: "cavra.endpoint_remediation_sla.escalation_owner_digest",
      session_id: "erslaescdigest-prod-v0-2-0-rc-1-sample",
      digest_id: "erslaescdigest-prod-v0-2-0-rc-1-sample",
      recurrence_plan_id: "erslaescr-prod-v0-2-0-rc-1-sample",
      retry_plan_id: "erslaescrtry-prod-v0-2-0-rc-1-sample",
      plan_id: "erslaesc-prod-v0-2-0-rc-1-sample",
      generated_at: "2026-05-19T01:30:00+00:00",
      generated_by: "release-manager",
      alert_level: "critical",
      summary: {
        owner_count: 1,
        unresolved_route_count: 2,
        retryable_count: 1,
        waiting_retry_count: 1
      },
      owners: [
        {
          owner: "release-governance",
          route_count: 1,
          retry_count: 1,
          providers: { slack: 1, webhook: 1 },
          routes: [{ owner: "release-governance", provider: "slack", action: "wait", route_key: "release-governance:slack" }]
        }
      ]
    }
  }
];

const endpointRecurrenceSuppressionTrendCatalog = [
  {
    session_id: "erslaesctrend-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-remediation-sla-escalation-suppression-trend",
    trend_id: "erslaesctrend-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T01:35:00+00:00",
    alert_level: "warning",
    suppression_event_count: 3,
    category_counts: {
      maintenance_window: 1,
      owner_calendar: 1,
      recurrence_interval_wait: 1
    },
    suppression_trend: {
      schema_version: "cavra.endpoint_remediation_sla.escalation_suppression_trend.v1",
      product: "CAVRA",
      trend_id: "erslaesctrend-prod-v0-2-0-rc-1-sample",
      generated_at: "2026-05-19T01:35:00+00:00",
      generated_by: "release-manager",
      alert_level: "warning",
      suppression_event_count: 3,
      category_counts: {
        maintenance_window: 1,
        owner_calendar: 1,
        recurrence_interval_wait: 1
      },
      owner_counts: { "release-governance": 3 },
      provider_counts: { slack: 1, teams: 1, webhook: 1 },
      latest_events: [
        { created_at: "2026-05-19T01:32:00+00:00", category: "maintenance_window", owner: "release-governance", provider: "teams", action: "suppress", reason: "owner maintenance window is active" },
        { created_at: "2026-05-19T01:20:00+00:00", category: "owner_calendar", owner: "release-governance", provider: "slack", action: "wait", reason: "owner calendar is unavailable" },
        { created_at: "2026-05-19T01:10:00+00:00", category: "recurrence_interval_wait", owner: "release-governance", provider: "webhook", action: "wait", reason: "recurrence interval has not elapsed" }
      ]
    }
  }
];

const endpointRecurrenceAutomationCatalog = [
  {
    session_id: "erslaescauto-prod-v0-2-0-rc-1-sample",
    metadata_kind: "endpoint-remediation-sla-escalation-recurrence-automation-run",
    run_id: "erslaescauto-prod-v0-2-0-rc-1-sample",
    created_at: "2026-05-19T01:40:00+00:00",
    dry_run: true,
    retryable_count: 1,
    owner_digest_count: 1,
    suppression_event_count: 3,
    automation_run: {
      schema_version: "cavra.endpoint_remediation_sla.escalation_recurrence_automation_run.v1",
      product: "CAVRA",
      run_id: "erslaescauto-prod-v0-2-0-rc-1-sample",
      generated_at: "2026-05-19T01:40:00+00:00",
      generated_by: "release-manager",
      dry_run: true,
      schedule: {
        enabled: true,
        interval_minutes: 30,
        window_start: "2026-05-19T01:30:00+00:00",
        window_end: "2026-05-19T02:00:00+00:00"
      },
      summary: {
        recurrence_plan_count: 1,
        retry_plan_count: 1,
        retryable_count: 1,
        waiting_retry_count: 1,
        suppressed_retry_count: 0,
        owner_digest_count: 1,
        owner_digest_route_count: 2,
        suppression_event_count: 3,
        follow_up_action_count: 6
      },
      retry_plan: endpointRecurrenceRetryPlanCatalog[0].retry_plan,
      owner_digest_events: [endpointRecurrenceOwnerDigestCatalog[0].owner_digest],
      suppression_trend: endpointRecurrenceSuppressionTrendCatalog[0].suppression_trend,
      follow_up_actions: [
        { owner: "release-governance", provider: "webhook", action: "retry", category: "maximum_retry", outcome: "planned", reason: "failed recurrence delivery is eligible for retry" },
        { owner: "release-governance", provider: "slack", action: "wait", category: "recurrence_interval_wait", outcome: "skipped", reason: "retry delay has not elapsed" },
        { owner: "release-governance", provider: "teams", action: "suppress", category: "maintenance_window", outcome: "skipped", reason: "owner maintenance window is active" },
        { owner: "release-governance", provider: "slack", action: "wait", category: "owner_calendar", outcome: "skipped", reason: "owner calendar is unavailable" },
        { owner: "release-governance", provider: "webhook", action: "wait", category: "recurrence_interval_wait", outcome: "skipped", reason: "recurrence interval has not elapsed" },
        { owner: "release-governance", provider: "private_queue", action: "deliver", category: "owner_review", outcome: "planned", reason: "owner digest prepared for release governance review" }
      ]
    }
  }
];

const endpointRecurrenceDetailPayloads = new Map();
const goDrillNotificationDetailPayloads = new Map();
let consoleSessionCache = null;
let currentGoDrillEscalationRoutes = [];

const endpointManagementExportArtifactCatalog = {
  "eme-stable-v0.2.0-rc.1": {
    schema_version: "cavra.evidence.artifacts.v1",
    product: "CAVRA",
    session_id: "eme-stable-v0.2.0-rc.1",
    metadata_kind: "endpoint-management-export",
    artifact_root_configured: false,
    artifact_count: 4,
    endpoint_management_export_integrity: {
      status: "verified",
      verified_artifacts: ["endpoint-management-export-manifest.json", "jamf-policy.json", "linux-fleet-manifest.json"],
      missing_artifacts: [],
      unchecked_artifacts: [],
      checksum_mismatches: [],
      checksum_errors: []
    },
    download_readiness: {
      status: "ready",
      rationale: "Sample endpoint-management export artifacts are checksum-verified and ready for review."
    },
    artifacts: [
      ["endpoint-management-export-manifest.json", "endpoint-export-manifest", "application/json", "Endpoint export manifest with release and approval metadata."],
      ["jamf-policy.json", "jamf-policy", "application/json", "Jamf import policy for managed runtime rollout."],
      ["linux-fleet-manifest.json", "linux-fleet-manifest", "application/json", "Linux fleet manifest for managed runtime rollout."],
      ["checksums.txt", "endpoint-export-checksums", "text/plain", "Checksums for endpoint-management export files."]
    ].map(([artifact, kind, media_type, description]) => ({
      artifact, kind, media_type, description, bytes: 1024, sha256: "sample", download_url: ""
    })),
    bundle_download_url: ""
  }
};

const releaseNoteCatalog = [
  {
    title: "Backend-Driven Sandbox Runs",
    date: "2026-05-18",
    summary: "The public sandbox can now call a deployed CAVRA API, run the flagship scenario with backend policy decisions, and refresh evidence and activity records.",
    links: [
      ["PR #12", "https://github.com/Huzefaaa2/cavra/pull/12"],
      ["Sandbox docs", "https://github.com/Huzefaaa2/cavra/blob/main/docs/sandbox.md"]
    ]
  },
  {
    title: "Release Integrity",
    date: "2026-05-18",
    summary: "Go runtime release packages now include checksums, SBOM metadata, SLSA provenance, detached signatures, and local verifier support.",
    links: [
      ["Go release packaging", "https://github.com/Huzefaaa2/cavra/blob/main/docs/go-release-packaging.md"],
      ["Release security", "https://github.com/Huzefaaa2/cavra/blob/main/docs/release-security-advisories.md"]
    ]
  },
  {
    title: "Public Evidence Console",
    date: "2026-05-18",
    summary: "The hosted demo includes evidence search, PR attestation checks, approval views, registry views, production readiness, and release documentation links.",
    links: [
      ["Hosted sandbox", "https://huzefaaa2.github.io/cavra/"],
      ["Roadmap", "https://github.com/Huzefaaa2/cavra/blob/main/docs/production-roadmap.md"]
    ]
  }
];

const activitySessions = evidenceCatalog.map((item) => ({
  schema_version: "cavra.session.v1",
  session_id: item.session_id,
  agent_id: item.session_id === "docs-agent-run" ? "docs-agent" : "codex-agent",
  actor: item.signer,
  repository: item.session_id === "security-review" ? "platform/security" : "payments/api",
  policy_pack: "cavra-ai-agent-baseline",
  state: "active",
  started_at: "2026-05-18T00:00:00+00:00",
  updated_at: "2026-05-18T00:10:00+00:00",
  decision_count: item.decision_count,
  blocked_count: item.blocked_count,
  approval_required_count: item.approval_required_count,
  evidence_refs: [`evidence://${item.session_id}`]
}));

const activityDecisions = evidenceCatalog.flatMap((item) =>
  item.decisions.map((decision, index) => ({
    schema_version: "cavra.decision.v1",
    decision_id: `dec_${item.session_id}_${index + 1}`,
    session_id: item.session_id,
    agent_id: item.session_id === "docs-agent-run" ? "docs-agent" : "codex-agent",
    actor: item.signer,
    repository: item.session_id === "security-review" ? "platform/security" : "payments/api",
    policy_pack: decision.policy_pack,
    policy_id: decision.policy_id,
    action_type: decision.action_type,
    target: decision.target,
    requested_operation: decision.action_type,
    rule_id: decision.rule_id,
    decision: decision.decision,
    severity: decision.severity,
    reason: decision.reason,
    timestamp: decision.timestamp,
    correlation_id: `corr_${item.session_id}_${index + 1}`,
    evidence_refs: decision.evidence_generated || []
  }))
);

const repositoryCatalog = [
  {
    repository_id: "payments/api",
    repository: "payments/api",
    provider: "github",
    owner: "Payments Platform",
    business_unit: "payments",
    environment: "production",
    policy_pack: "cavra-banking",
    risk_tier: "high",
    status: "active",
    protected_branches: ["main", "release/*"],
    required_checks: ["cavra", "CodeQL"]
  },
  {
    repository_id: "platform/security",
    repository: "platform/security",
    provider: "github",
    owner: "Platform Security",
    business_unit: "platform",
    environment: "production",
    policy_pack: "cavra-ai-agent-baseline",
    risk_tier: "medium",
    status: "active",
    protected_branches: ["main"],
    required_checks: ["cavra"]
  },
  {
    repository_id: "docs/site",
    repository: "docs/site",
    provider: "github",
    owner: "Documentation",
    business_unit: "engineering",
    environment: "development",
    policy_pack: "cavra-ai-agent-baseline",
    risk_tier: "low",
    status: "active",
    protected_branches: ["main"],
    required_checks: []
  }
];

const rolloutCatalog = [
  {
    rollout_id: "payments-api-banking",
    repository: "payments/api",
    policy_pack: "cavra-banking",
    policy_version: "2026.05",
    mode: "strict",
    state: "active",
    owner: "Platform Security",
    coverage_percent: 95,
    evidence_refs: ["evidence://demo-session", "attestation://payments/api"]
  },
  {
    rollout_id: "platform-security-baseline",
    repository: "platform/security",
    policy_pack: "cavra-ai-agent-baseline",
    policy_version: "latest",
    mode: "enforce",
    state: "active",
    owner: "Platform Security",
    coverage_percent: 88,
    evidence_refs: ["evidence://security-review"]
  },
  {
    rollout_id: "docs-site-baseline",
    repository: "docs/site",
    policy_pack: "cavra-ai-agent-baseline",
    policy_version: "latest",
    mode: "audit_only",
    state: "planned",
    owner: "Documentation",
    coverage_percent: 20,
    evidence_refs: []
  }
];

const policyCatalog = [
  {
    id: "cavra-ai-agent-baseline",
    title: "AI Agent Baseline",
    description: "Default CAVRA controls for AI coding agents.",
    version: "latest",
    summary: { rule_counts: { filesystem: 8, commands: 6, git: 4, mcp: 5, approvals: 2, evidence: 3, compliance: 1 } }
  },
  {
    id: "cavra-banking",
    title: "Banking Baseline",
    description: "Regulated banking SDLC policy overlay.",
    version: "2026.05",
    summary: { rule_counts: { filesystem: 12, commands: 8, git: 5, mcp: 6, approvals: 4, evidence: 5, compliance: 6 } }
  }
];

const integrationCatalog = [
  {
    integration_id: "github-enterprise",
    provider: "github",
    name: "GitHub Enterprise",
    category: "source_control",
    status: "active",
    health_status: "healthy",
    owner: "Developer Platform",
    environment: "production",
    auth_mode: "github_app",
    capabilities: ["required_check", "pull_request", "branch_protection"]
  },
  {
    integration_id: "splunk-soc",
    provider: "splunk",
    name: "Splunk SOC",
    category: "siem",
    status: "configured",
    health_status: "not_checked",
    owner: "SOC",
    environment: "production",
    auth_mode: "hec_token",
    capabilities: ["decision_events", "blocked_action_alerts"]
  },
  {
    integration_id: "jira-change",
    provider: "jira",
    name: "Jira Change",
    category: "itsm",
    status: "planned",
    health_status: "unknown",
    owner: "Change Management",
    environment: "production",
    auth_mode: "oauth",
    capabilities: ["approval_ticket", "change_reference"]
  }
];

const approvalCatalog = [
  {
    approval_id: "apr_demo_iam",
    decision_id: "dec_demo_iam",
    session_id: "demo-session",
    state: "pending",
    approver_group: "IAM",
    requested_by: "developer",
    requested_at: new Date().toISOString(),
    expires_at: "2026-05-18T00:00:00Z",
    external_ref: "CHG-100",
    decision: { target: "iam/admin-role.tf", rule_id: "filesystem.write.require_approval", reason: "IAM privilege change requires review." },
    evidence_refs: ["approval://apr_demo_iam", "evidence://demo-session/dec_demo_iam"],
    history: [
      { event: "requested", actor: "developer", timestamp: new Date().toISOString(), reason: "IAM privilege change requires review." }
    ]
  },
  {
    approval_id: "apr_break_glass",
    decision_id: "dec_incident",
    session_id: "incident-session",
    state: "break_glass",
    approver_group: "Change Advisory Board",
    requested_by: "incident-commander",
    requested_at: new Date().toISOString(),
    expires_at: "2026-05-17T20:00:00Z",
    external_ref: "INC-777",
    break_glass: true,
    break_glass_reason: "Production recovery for active incident.",
    decision: { target: "terraform apply", rule_id: "commands.block", reason: "Autonomous production-impacting infrastructure change is prohibited." },
    evidence_refs: ["approval://apr_break_glass", "incident://INC-777"],
    history: [
      { event: "break_glass", actor: "incident-commander", timestamp: new Date().toISOString(), reason: "Production recovery for active incident." }
    ]
  }
];

const agentCatalog = [
  {
    agent_id: "claude-code",
    vendor: "Anthropic",
    owner: "AI Platform",
    status: "active",
    capabilities: ["code_edit", "test", "mcp_tool_call"],
    risk_tier: "high"
  },
  {
    agent_id: "codex-agent",
    vendor: "OpenAI",
    owner: "Developer Platform",
    status: "active",
    capabilities: ["code_edit", "test", "git_operation"],
    risk_tier: "high"
  },
  {
    agent_id: "docs-agent",
    vendor: "CAVRA",
    owner: "Documentation",
    status: "active",
    capabilities: ["documentation", "diagram_update"],
    risk_tier: "low"
  }
];

const mcpCatalog = [
  {
    server_id: "github-mcp",
    name: "GitHub MCP",
    trust_tier: "approved",
    approval_state: "approved",
    capabilities: ["repository", "saas"],
    allowed_tools: ["create_pull_request", "create_issue"]
  },
  {
    server_id: "filesystem-mcp",
    name: "Filesystem MCP",
    trust_tier: "experimental",
    approval_state: "pending",
    capabilities: ["filesystem"],
    allowed_tools: ["read_file"]
  },
  {
    server_id: "unknown-filesystem",
    name: "Unknown Filesystem",
    trust_tier: "blocked",
    approval_state: "denied",
    capabilities: ["filesystem"],
    allowed_tools: []
  }
];

const agentProfiles = [
  ["claude-code", "Claude Code", "Anthropic", "high", ["code_edit", "test", "shell", "mcp_tool_call"]],
  ["codex", "OpenAI Codex", "OpenAI", "high", ["code_edit", "test", "shell", "git_operation"]],
  ["github-copilot", "GitHub Copilot Agent", "GitHub", "medium", ["code_edit", "test", "pull_request"]],
  ["cursor", "Cursor Agent", "Cursor", "medium", ["code_edit", "test", "repository_search"]],
  ["gemini-cli", "Gemini CLI", "Google", "high", ["code_edit", "test", "cloud_assistance"]],
  ["aws-q-developer", "AWS Q Developer", "AWS", "high", ["code_edit", "iam_review", "cloud_assistance"]]
].map(([profile_id, display_name, vendor, risk_tier, default_capabilities]) => ({
  profile_id, display_name, vendor, risk_tier, default_capabilities
}));

const mcpClassifications = [
  ["filesystem", "local_resource", "high", "Prevent unapproved file and secret access."],
  ["shell", "execution", "critical", "Route command execution through policy and approval gates."],
  ["network", "egress", "medium", "Control data egress and supply-chain downloads."],
  ["database", "data_access", "high", "Protect regulated data stores from autonomous reads and writes."],
  ["saas", "enterprise_workflow", "medium", "Keep workflow automation scoped to approved tools."],
  ["cloud", "infrastructure", "critical", "Prevent unapproved IAM and production changes."],
  ["repository", "source_control", "medium", "Govern source-control automation and workflow changes."]
].map(([capability, category, risk_tier, control_objective]) => ({
  capability, category, risk_tier, control_objective
}));

let consoleConfig = null;
let consoleAuthToken = window.sessionStorage?.getItem("cavraConsoleToken") || "";
let lastPolicyPublishApprovalId = "";
let lastSandboxRun = null;

function eventPayload(row, index) {
  const [action_type, target, decision, rule_id, reason] = row;
  return {
    event_id: `evt_${index + 1}`,
    timestamp: new Date().toISOString(),
    agent: "Simulated AI-agent scenario using real CAVRA policy decisions.",
    action_type, target, decision, rule_id, reason,
    policy_pack: "cavra-ai-agent-baseline",
    policy_id: "cavra-ai-agent-baseline",
    severity: decision === "allow" ? "low" : "high",
    business_impact: "Pre-action runtime governance with audit evidence.",
    evidence_generated: [`evidence://sandbox/evt_${index + 1}`],
    remediation: decision === "block" ? "Use an approved workflow or request a policy exception." : "Continue with recorded evidence."
  };
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  })[char]);
}

function formatMetricNumber(value) {
  return Number(value || 0).toLocaleString("en-US");
}

function formatMetricDate(value) {
  if (!value) return "None yet";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return String(value).slice(0, 16);
  return parsed.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function apiUrl(path, params = {}) {
  const configuredBase = window.CAVRA_API_BASE || consoleConfig?.api_base_url || "";
  const base = configuredBase || window.location.origin;
  const url = new URL(path, base);
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  }
  return url.toString();
}

function apiHeaders(json = false) {
  const headers = {};
  if (json) headers["content-type"] = "application/json";
  if (consoleAuthToken) headers.authorization = `Bearer ${consoleAuthToken}`;
  return headers;
}

async function loadConsoleConfig() {
  if (consoleConfig) return consoleConfig;
  try {
    const response = await fetch(apiUrl("/console/config"));
    if (!response.ok) throw new Error("config unavailable");
    consoleConfig = await response.json();
  } catch {
    consoleConfig = {
      product: "CAVRA",
      api_base_url: window.CAVRA_API_BASE || "",
      metadata_mode: "sample",
      cors_origins: []
    };
  }
  const status = document.querySelector("#apiStatus");
  if (status) {
    const mode = consoleConfig.metadata_mode || "sample";
    status.textContent = `API: ${mode}`;
  }
  return consoleConfig;
}

async function runScenario() {
  const actions = document.querySelector("#actions");
  const decisions = document.querySelector("#decisions");
  const evidence = document.querySelector("#evidence");
  const status = document.querySelector("#scenarioStatus");
  actions.innerHTML = "";
  decisions.innerHTML = "";
  if (status) {
    status.textContent = "Scenario source: running";
    status.className = "status-line";
  }
  evidence.textContent = "Running...";
  const run = await loadSandboxRun();
  lastSandboxRun = run;
  const events = Array.isArray(run.events) ? run.events : [];
  for (const event of events) {
    await new Promise((resolve) => setTimeout(resolve, 280));
    actions.insertAdjacentHTML("beforeend", `<li><strong>${event.action_type}</strong><br>${event.target}</li>`);
    decisions.insertAdjacentHTML("beforeend", `<li class="${event.decision}"><strong>${event.decision}</strong><br>${event.reason}<br><small>${event.rule_id}</small></li>`);
  }
  evidence.textContent = JSON.stringify(run, null, 2);
  updateScenarioDownloads(run);
  if (status) {
    status.textContent = `Scenario source: ${run.source === "cavra-api" ? "CAVRA API" : "local sample"} · ${run.run_id || "sample"}`;
    status.className = `status-line ${run.source === "cavra-api" ? "ok" : "warn"}`;
  }
  if (run.source === "cavra-api") {
    await Promise.all([refreshEvidence(), refreshActivity()]);
  }
}

async function loadSandboxRun() {
  await loadConsoleConfig();
  const persona = document.querySelector("#persona")?.value || "Developer";
  const policyMode = document.querySelector("#policyMode")?.value || "Enforce";
  try {
    const response = await fetch(apiUrl(consoleConfig?.endpoints?.sandbox_run || "/api/sandbox/run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        scenario: "before-the-agent-acts",
        persona,
        policy_mode: policyMode
      })
    });
    if (!response.ok) throw new Error("sandbox API unavailable");
    return await response.json();
  } catch {
    const events = scenario.map(eventPayload);
    const blocked = events.filter((event) => event.decision === "block").length;
    const approvals = events.filter((event) => event.decision === "require_approval").length;
    return {
      schema_version: "cavra.sandbox.run.v1",
      product: "CAVRA",
      run_id: `local_${Date.now()}`,
      scenario: "before-the-agent-acts",
      persona,
      policy_mode: policyMode.toLowerCase().replaceAll(" ", "_"),
      policy_pack: "cavra-ai-agent-baseline",
      source: "local-sample",
      tagline: "Before the agent acts, CAVRA decides.",
      decision_count: events.length,
      blocked_count: blocked,
      approval_required_count: approvals,
      events,
      artifacts: [
        { artifact: "evidence.json", kind: "evidence", media_type: "application/json", download_url: "./evidence/before-the-agent-acts/evidence.json" }
      ]
    };
  }
}

function updateScenarioDownloads(run) {
  const evidenceLink = document.querySelector("#downloadEvidence");
  if (!evidenceLink) return;
  const evidenceArtifact = (run.artifacts || []).find((item) => item.artifact === "evidence.json" || item.kind === "evidence");
  const downloadUrl = evidenceArtifact?.download_url || "./evidence/before-the-agent-acts/evidence.json";
  evidenceLink.href = downloadUrl.startsWith(".") || downloadUrl.startsWith("http") ? downloadUrl : apiUrl(downloadUrl);
}

async function loadEvidenceMetadata() {
  await loadConsoleConfig();
  try {
    const params = {
      signer: document.querySelector("#filterSigner")?.value.trim(),
      metadata_kind: document.querySelector("#filterMetadataKind")?.value,
      rollout_status: document.querySelector("#filterRolloutStatus")?.value,
      environment: document.querySelector("#filterEnvironment")?.value.trim(),
      deployment_target: document.querySelector("#filterDeploymentTarget")?.value.trim(),
      min_blocked: document.querySelector("#filterBlocked")?.value || 0,
      has_approvals: document.querySelector("#filterApprovals")?.value,
      limit: document.querySelector("#filterLimit")?.value || 10
    };
    const response = await fetch(apiUrl("/evidence", params));
    if (!response.ok) throw new Error("API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return evidenceCatalog;
  }
}

async function loadEvidenceArtifacts(sessionId) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl(`/evidence/${encodeURIComponent(sessionId)}/artifacts`));
    if (!response.ok) throw new Error("Evidence artifact API unavailable");
    return await response.json();
  } catch {
    const metadata = evidenceCatalog.find((item) => item.session_id === sessionId) || {};
    const isRollout = metadata.metadata_kind === "managed-endpoint-rollout";
    const artifacts = isRollout ? rolloutArtifactCatalog : evidenceArtifactCatalog;
    return {
      schema_version: "cavra.evidence.artifacts.v1",
      product: "CAVRA",
      session_id: sessionId,
      metadata_kind: metadata.metadata_kind || "session",
      artifact_root_configured: false,
      artifact_count: artifacts.length,
      artifacts: artifacts.map((item) => ({ ...item, download_url: "" })),
      ...(isRollout ? {
        rollout_artifact_integrity: {
          status: "verified",
          verified_artifacts: ["managed-endpoint-rollout-evidence.json", "managed-endpoint-rollout-evidence.md"],
          missing_artifacts: [],
          unchecked_artifacts: [],
          checksum_mismatches: [],
          checksum_errors: []
        },
        promotion_readiness: metadata.promotion_readiness || {
          status: "ready",
          rationale: "Sample rollout evidence is checksum-verified and ready for promotion review."
        }
      } : {}),
      bundle_download_url: ""
    };
  }
}

async function loadReleaseConnectorDeliveries() {
  await loadConsoleConfig();
  try {
    const params = {
      provider: document.querySelector("#filterReleaseDeliveryProvider")?.value.trim(),
      event_type: document.querySelector("#filterReleaseDeliveryEvent")?.value,
      success: document.querySelector("#filterReleaseDeliverySuccess")?.value,
      limit: 25
    };
    const response = await fetch(apiUrl("/release-connector-deliveries", params));
    if (!response.ok) throw new Error("Release connector delivery API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return filterReleaseConnectorDeliveries(releaseConnectorDeliveryCatalog);
  }
}

async function loadReleaseConnectorDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/release-connector-deliveries/dashboard"));
    if (!response.ok) throw new Error("Release connector delivery dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleReleaseConnectorDashboard(filterReleaseConnectorDeliveries(releaseConnectorDeliveryCatalog));
  }
}

async function loadReleaseChannelPromotions() {
  await loadConsoleConfig();
  try {
    const params = {
      channel: document.querySelector("#filterReleaseChannel")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/release-channel-promotions", params));
    if (!response.ok) throw new Error("Release channel promotion API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return filterReleaseChannelPromotions(releaseChannelPromotionCatalog);
  }
}

async function loadEndpointManagementExports() {
  await loadConsoleConfig();
  try {
    const params = {
      channel: document.querySelector("#filterReleaseChannel")?.value.trim(),
      provider: document.querySelector("#filterEndpointExportProvider")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-management-exports", params));
    if (!response.ok) throw new Error("Endpoint management export API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return filterEndpointManagementExports(endpointManagementExportCatalog);
  }
}

async function loadEndpointManagementExportDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-management-exports/dashboard"));
    if (!response.ok) throw new Error("Endpoint management export dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointManagementExportDashboard(filterEndpointManagementExports(endpointManagementExportCatalog));
  }
}

async function loadEndpointPublicationDeliveries() {
  await loadConsoleConfig();
  try {
    const params = {
      provider: document.querySelector("#filterEndpointPublicationProvider")?.value.trim(),
      channel: document.querySelector("#filterEndpointPublicationChannel")?.value.trim(),
      success: document.querySelector("#filterEndpointPublicationSuccess")?.value,
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-management-publications", params));
    if (!response.ok) throw new Error("Endpoint publication delivery API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return filterEndpointPublicationDeliveries(endpointPublicationDeliveryCatalog);
  }
}

async function loadEndpointPublicationDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-management-publications/dashboard"));
    if (!response.ok) throw new Error("Endpoint publication dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointPublicationDashboard(filterEndpointPublicationDeliveries(endpointPublicationDeliveryCatalog));
  }
}

async function loadEndpointReconciliations() {
  await loadConsoleConfig();
  try {
    const params = {
      drift_status: document.querySelector("#filterEndpointReconciliationStatus")?.value,
      alert_level: document.querySelector("#filterEndpointReconciliationAlert")?.value,
      deployment_target: document.querySelector("#filterEndpointReconciliationTarget")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-reconciliations", params));
    if (!response.ok) throw new Error("Endpoint reconciliation API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return filterEndpointReconciliations(endpointReconciliationCatalog);
  }
}

async function loadEndpointReconciliationDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-reconciliations/dashboard"));
    if (!response.ok) throw new Error("Endpoint reconciliation dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointReconciliationDashboard(filterEndpointReconciliations(endpointReconciliationCatalog));
  }
}

async function loadEndpointInventoryIngestions() {
  await loadConsoleConfig();
  try {
    const params = {
      provider: document.querySelector("#filterEndpointInventoryProvider")?.value,
      channel: document.querySelector("#filterEndpointInventoryChannel")?.value.trim(),
      deployment_target: document.querySelector("#filterEndpointInventoryTarget")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-inventory-ingestions", params));
    if (!response.ok) throw new Error("Endpoint inventory ingestion API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return endpointInventoryCatalog.filter((item) => {
      const provider = document.querySelector("#filterEndpointInventoryProvider")?.value;
      const channel = document.querySelector("#filterEndpointInventoryChannel")?.value.trim();
      const target = document.querySelector("#filterEndpointInventoryTarget")?.value.trim();
      if (provider && item.provider !== provider) return false;
      if (channel && item.channel !== channel) return false;
      if (target && !(item.deployment_targets || []).includes(target)) return false;
      return true;
    });
  }
}

async function loadEndpointInventoryDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-inventory-ingestions/dashboard"));
    if (!response.ok) throw new Error("Endpoint inventory dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointInventoryDashboard(endpointInventoryCatalog);
  }
}

async function loadEndpointInventoryFreshness() {
  await loadConsoleConfig();
  try {
    const params = {
      alert_level: document.querySelector("#filterEndpointInventoryFreshnessAlert")?.value,
      provider: document.querySelector("#filterEndpointInventoryFreshnessProvider")?.value,
      channel: document.querySelector("#filterEndpointInventoryFreshnessChannel")?.value.trim(),
      deployment_target: document.querySelector("#filterEndpointInventoryFreshnessTarget")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-inventory-freshness", params));
    if (!response.ok) throw new Error("Endpoint inventory freshness API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return endpointInventoryFreshnessCatalog.filter((item) => {
      const alert = document.querySelector("#filterEndpointInventoryFreshnessAlert")?.value;
      const provider = document.querySelector("#filterEndpointInventoryFreshnessProvider")?.value;
      const channel = document.querySelector("#filterEndpointInventoryFreshnessChannel")?.value.trim();
      const target = document.querySelector("#filterEndpointInventoryFreshnessTarget")?.value.trim();
      const latest = item.latest_ingestions || [];
      if (alert && item.alert_level !== alert) return false;
      if (provider && !latest.some((entry) => entry.provider === provider)) return false;
      if (channel && !latest.some((entry) => entry.channel === channel)) return false;
      if (target && !latest.some((entry) => entry.deployment_target === target)) return false;
      return true;
    });
  }
}

async function loadEndpointInventoryFreshnessDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-inventory-freshness/dashboard"));
    if (!response.ok) throw new Error("Endpoint inventory freshness dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointInventoryFreshnessDashboard(endpointInventoryFreshnessCatalog);
  }
}

async function loadEndpointRemediations() {
  await loadConsoleConfig();
  try {
    const params = {
      metadata_kind: document.querySelector("#filterEndpointRemediationKind")?.value,
      approval_state: document.querySelector("#filterEndpointRemediationApproval")?.value,
      reconciliation_id: document.querySelector("#filterEndpointRemediationReconciliation")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-remediations", params));
    if (!response.ok) throw new Error("Endpoint remediation API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return endpointRemediationCatalog.filter((item) => {
      const kind = document.querySelector("#filterEndpointRemediationKind")?.value;
      const approval = document.querySelector("#filterEndpointRemediationApproval")?.value;
      const reconciliation = document.querySelector("#filterEndpointRemediationReconciliation")?.value.trim();
      if (kind && item.metadata_kind !== kind) return false;
      if (approval && item.approval_state !== approval) return false;
      if (reconciliation && item.reconciliation_id !== reconciliation) return false;
      return true;
    });
  }
}

async function loadEndpointRemediationDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediations/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointRemediationDashboard(endpointRemediationCatalog);
  }
}

async function loadEndpointRemediationHandoffs() {
  await loadConsoleConfig();
  try {
    const params = {
      provider: document.querySelector("#filterEndpointRemediationHandoffProvider")?.value,
      approval_state: document.querySelector("#filterEndpointRemediationHandoffApproval")?.value,
      request_id: document.querySelector("#filterEndpointRemediationHandoffRequest")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-remediation-handoffs", params));
    if (!response.ok) throw new Error("Endpoint remediation handoff API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return endpointRemediationHandoffCatalog.filter((item) => {
      const provider = document.querySelector("#filterEndpointRemediationHandoffProvider")?.value;
      const approval = document.querySelector("#filterEndpointRemediationHandoffApproval")?.value;
      const request = document.querySelector("#filterEndpointRemediationHandoffRequest")?.value.trim();
      if (provider && !(item.providers || []).includes(provider)) return false;
      if (approval && item.approval_state !== approval) return false;
      if (request && item.request_id !== request) return false;
      return true;
    });
  }
}

async function loadEndpointRemediationHandoffDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-handoffs/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation handoff dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointRemediationHandoffDashboard(endpointRemediationHandoffCatalog);
  }
}

async function loadEndpointRemediationHandoffStatuses() {
  await loadConsoleConfig();
  try {
    const params = {
      provider: document.querySelector("#filterEndpointRemediationHandoffStatusProvider")?.value,
      handoff_status: document.querySelector("#filterEndpointRemediationHandoffStatusState")?.value,
      handoff_id: document.querySelector("#filterEndpointRemediationHandoffStatusId")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-remediation-handoff-statuses", params));
    if (!response.ok) throw new Error("Endpoint remediation handoff status API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return endpointRemediationHandoffStatusCatalog.filter((item) => {
      const provider = document.querySelector("#filterEndpointRemediationHandoffStatusProvider")?.value;
      const status = document.querySelector("#filterEndpointRemediationHandoffStatusState")?.value;
      const handoff = document.querySelector("#filterEndpointRemediationHandoffStatusId")?.value.trim();
      if (provider && item.provider !== provider) return false;
      if (status && item.handoff_status !== status) return false;
      if (handoff && item.handoff_id !== handoff) return false;
      return true;
    });
  }
}

async function loadEndpointRemediationHandoffStatusDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-handoff-statuses/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation handoff status dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointRemediationHandoffStatusDashboard(endpointRemediationHandoffStatusCatalog);
  }
}

async function loadEndpointRemediationSlaReports() {
  await loadConsoleConfig();
  try {
    const params = {
      alert_level: document.querySelector("#filterEndpointRemediationSlaAlert")?.value,
      min_breached: document.querySelector("#filterEndpointRemediationSlaBreached")?.value,
      limit: 25
    };
    const response = await fetch(apiUrl("/endpoint-remediation-sla-reports", params));
    if (!response.ok) throw new Error("Endpoint remediation SLA report API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return endpointRemediationSlaCatalog.filter((item) => {
      const alert = document.querySelector("#filterEndpointRemediationSlaAlert")?.value;
      const minBreached = Number(document.querySelector("#filterEndpointRemediationSlaBreached")?.value || 0);
      if (alert && item.alert_level !== alert) return false;
      if (Number(item.breached_count || 0) < minBreached) return false;
      return true;
    });
  }
}

async function loadEndpointRemediationSlaDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-reports/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation SLA dashboard API unavailable");
    return await response.json();
  } catch {
    return sampleEndpointRemediationSlaDashboard(endpointRemediationSlaCatalog);
  }
}

async function loadEndpointRemediationSlaNotificationDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-notifications/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation SLA notification dashboard API unavailable");
    return await response.json();
  } catch {
    return {
      alert_level: "healthy",
      plan_count: 0,
      delivery_count: 0,
      acknowledgement_count: 0,
      outstanding_acknowledgement_count: 0,
      suppressed_provider_count: 0
    };
  }
}

async function loadEndpointRemediationSlaEscalationDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalations/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation SLA escalation dashboard API unavailable");
    return await response.json();
  } catch {
    return {
      alert_level: "healthy",
      plan_count: 0,
      active_escalation_count: 0,
      acknowledgement_breach_count: 0,
      resolution_breach_count: 0,
      owner_count: 0
    };
  }
}

async function loadEndpointRemediationSlaEscalationActionDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-actions/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation SLA escalation action dashboard API unavailable");
    return await response.json();
  } catch {
    return {
      alert_level: "healthy",
      delivery_count: 0,
      failed_delivery_count: 0,
      owner_review_count: 0,
      unresolved_review_count: 0
    };
  }
}

async function loadEndpointRemediationSlaEscalationRecurrenceDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-recurrences/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation SLA escalation recurrence dashboard API unavailable");
    return await response.json();
  } catch {
    return {
      alert_level: "healthy",
      deliverable_route_count: 0,
      waiting_route_count: 0,
      suppressed_route_count: 0,
      maintenance_suppressed_count: 0,
      calendar_suppressed_count: 0
    };
  }
}

async function loadEndpointRecurrenceAutomationDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-recurrence-automations/dashboard"));
    if (!response.ok) throw new Error("Endpoint remediation SLA escalation recurrence automation dashboard API unavailable");
    return await response.json();
  } catch {
    return {
      alert_level: "critical",
      run_count: endpointRecurrenceAutomationCatalog.length,
      dry_run_count: endpointRecurrenceAutomationCatalog.filter((item) => endpointRecurrenceAutomationPayload(item).dry_run !== false).length,
      executed_count: endpointRecurrenceAutomationCatalog.filter((item) => endpointRecurrenceAutomationPayload(item).dry_run === false).length,
      retryable_count: 1,
      owner_digest_count: 1,
      suppression_event_count: 3
    };
  }
}

async function loadEndpointRecurrenceAutomationHealth() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-recurrence-automations/health", {
      expected_interval_minutes: 30,
      stale_metadata_minutes: 120
    }));
    if (!response.ok) throw new Error("Endpoint remediation SLA escalation recurrence automation health API unavailable");
    return await response.json();
  } catch {
    return {
      alert_level: "warning",
      missed_run_count: 0,
      failed_job_count: 0,
      stale_metadata_count: 1,
      connector_delivery_failure_count: 0,
      latest_run_age_minutes: 45,
      alerts: [
        {
          severity: "warning",
          category: "stale_metadata",
          message: "Sample recurrence metadata is ready for refresh."
        }
      ]
    };
  }
}

async function loadEndpointRecurrenceAutomationHealthAlerts() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts", { limit: 50 }));
    if (!response.ok) throw new Error("Endpoint recurrence automation health alert API unavailable");
    return (await response.json()).items || [];
  } catch {
    return [
      {
        metadata_kind: "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan",
        session_id: "erslahalert-sample",
        created_at: "2026-05-20T15:00:00+00:00",
        alert_level: "warning",
        selected_providers: ["webhook"],
        acknowledgement_required_providers: ["webhook"],
        health_alert_plan: {
          health_id: "erslah-sample",
          alert_level: "warning",
          summary: { stale_metadata_count: 1, alert_count: 1 }
        }
      }
    ];
  }
}

async function loadEndpointRecurrenceAutomationHealthAlertDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/dashboard"));
    if (!response.ok) throw new Error("Endpoint recurrence automation health alert dashboard API unavailable");
    return await response.json();
  } catch {
    return {
      alert_level: "warning",
      plan_count: 1,
      delivery_count: 0,
      failed_delivery_count: 0,
      acknowledgement_count: 0,
      outstanding_acknowledgement_count: 1,
      suppressed_provider_count: 0
    };
  }
}

function selectedEndpointRecurrenceFilters() {
  return {
    owner: document.querySelector("#filterEndpointRecurrenceOwner")?.value.trim().toLowerCase() || "",
    provider: document.querySelector("#filterEndpointRecurrenceProvider")?.value || "",
    action: document.querySelector("#filterEndpointRecurrenceAction")?.value || "",
    category: document.querySelector("#filterEndpointRecurrenceCategory")?.value || "",
    workerMode: document.querySelector("#filterEndpointRecurrenceWorkerMode")?.value || ""
  };
}

function endpointRecurrenceRetryPlanPayload(item) {
  return item?.retry_plan && typeof item.retry_plan === "object" ? item.retry_plan : item;
}

function endpointRecurrenceOwnerDigestPayload(item) {
  return item?.owner_digest && typeof item.owner_digest === "object" ? item.owner_digest : item;
}

function endpointRecurrenceSuppressionTrendPayload(item) {
  return item?.suppression_trend && typeof item.suppression_trend === "object" ? item.suppression_trend : item;
}

function endpointRecurrenceAutomationPayload(item) {
  return item?.automation_run && typeof item.automation_run === "object" ? item.automation_run : item;
}

function endpointRecurrenceRetryDecisions(item) {
  const plan = endpointRecurrenceRetryPlanPayload(item);
  return Array.isArray(plan.retry_decisions) ? plan.retry_decisions : [];
}

function endpointRecurrenceOwnerRows(item) {
  const digest = endpointRecurrenceOwnerDigestPayload(item);
  return Array.isArray(digest.owners) ? digest.owners : [];
}

function endpointRecurrenceTrendRows(item) {
  const trend = endpointRecurrenceSuppressionTrendPayload(item);
  return Array.isArray(trend.latest_events) ? trend.latest_events : [];
}

function endpointRecurrenceAutomationActions(item) {
  const run = endpointRecurrenceAutomationPayload(item);
  return Array.isArray(run.follow_up_actions) ? run.follow_up_actions : [];
}

function endpointRecurrenceAutomationRows(item) {
  const run = endpointRecurrenceAutomationPayload(item);
  const rows = [...endpointRecurrenceAutomationActions(item)];
  const retryPlan = run.retry_plan && typeof run.retry_plan === "object" ? run.retry_plan : {};
  const ownerDigests = Array.isArray(run.owner_digest_events) ? run.owner_digest_events : [];
  const suppressionTrend = run.suppression_trend && typeof run.suppression_trend === "object" ? run.suppression_trend : {};
  for (const decision of endpointRecurrenceRetryDecisions(retryPlan)) {
    rows.push(decision, ...(decision.routes || []));
  }
  for (const digest of ownerDigests) {
    rows.push(...endpointRecurrenceOwnerRows(digest));
  }
  rows.push(...endpointRecurrenceTrendRows(suppressionTrend));
  return rows;
}

function matchesEndpointRecurrenceOwner(owner, rows) {
  if (!owner) return true;
  return rows.some((row) => String(row.owner || "").toLowerCase().includes(owner));
}

function matchesEndpointRecurrenceProvider(provider, rows) {
  if (!provider) return true;
  return rows.some((row) => {
    if (String(row.provider || "") === provider) return true;
    if (Array.isArray(row.routes) && row.routes.some((route) => String(route.provider || "") === provider)) return true;
    return row.providers && Object.prototype.hasOwnProperty.call(row.providers, provider);
  });
}

function filterEndpointRecurrenceRetryPlans(items) {
  const filters = selectedEndpointRecurrenceFilters();
  return items.filter((item) => {
    const decisions = endpointRecurrenceRetryDecisions(item);
    if (!matchesEndpointRecurrenceOwner(filters.owner, decisions.flatMap((decision) => decision.routes || []))) return false;
    if (!matchesEndpointRecurrenceProvider(filters.provider, decisions)) return false;
    if (filters.action && !decisions.some((decision) => decision.action === filters.action)) return false;
    if (filters.category && filters.category !== "maximum_retry") return false;
    return true;
  });
}

function filterEndpointRecurrenceOwnerDigests(items) {
  const filters = selectedEndpointRecurrenceFilters();
  return items.filter((item) => {
    const owners = endpointRecurrenceOwnerRows(item);
    if (!matchesEndpointRecurrenceOwner(filters.owner, owners)) return false;
    if (!matchesEndpointRecurrenceProvider(filters.provider, owners)) return false;
    if (filters.action && !owners.some((owner) => {
      if (filters.action === "retry") return Number(owner.retry_count || 0) > 0;
      return (owner.routes || []).some((route) => route.action === filters.action);
    })) return false;
    if (filters.category) return false;
    return true;
  });
}

function filterEndpointRecurrenceSuppressionTrends(items) {
  const filters = selectedEndpointRecurrenceFilters();
  return items.filter((item) => {
    const rows = endpointRecurrenceTrendRows(item);
    if (!matchesEndpointRecurrenceOwner(filters.owner, rows)) return false;
    if (!matchesEndpointRecurrenceProvider(filters.provider, rows)) return false;
    if (filters.action && !rows.some((row) => row.action === filters.action)) return false;
    if (filters.category && !rows.some((row) => row.category === filters.category)) return false;
    return true;
  });
}

function filterEndpointRecurrenceAutomations(items) {
  const filters = selectedEndpointRecurrenceFilters();
  return items.filter((item) => {
    const run = endpointRecurrenceAutomationPayload(item);
    const rows = endpointRecurrenceAutomationRows(item);
    const isDryRun = run.dry_run !== false && item.dry_run !== false;
    if (filters.workerMode === "dry_run" && !isDryRun) return false;
    if (filters.workerMode === "executed" && isDryRun) return false;
    if (!matchesEndpointRecurrenceOwner(filters.owner, rows)) return false;
    if (!matchesEndpointRecurrenceProvider(filters.provider, rows)) return false;
    if (filters.action && !rows.some((row) => row.action === filters.action)) return false;
    if (filters.category && !rows.some((row) => row.category === filters.category)) return false;
    return true;
  });
}

async function loadEndpointRecurrenceActionItems(metadataKind, sampleItems) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-actions", {
      metadata_kind: metadataKind,
      limit: 50
    }));
    if (!response.ok) throw new Error("Endpoint recurrence operations API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return sampleItems;
  }
}

async function loadEndpointRecurrenceAutomations() {
  await loadConsoleConfig();
  const filters = selectedEndpointRecurrenceFilters();
  const params = { limit: 50 };
  if (filters.workerMode === "dry_run") params.dry_run = true;
  if (filters.workerMode === "executed") params.dry_run = false;
  try {
    const response = await fetch(apiUrl("/endpoint-remediation-sla-escalation-recurrence-automations", params));
    if (!response.ok) throw new Error("Endpoint recurrence automation API unavailable");
    const payload = await response.json();
    const items = Array.isArray(payload) ? payload : payload.items || [];
    return filterEndpointRecurrenceAutomations(items);
  } catch {
    return filterEndpointRecurrenceAutomations(endpointRecurrenceAutomationCatalog);
  }
}

async function loadEndpointRecurrenceRetryPlans() {
  const items = await loadEndpointRecurrenceActionItems(
    "endpoint-remediation-sla-escalation-recurrence-retry-plan",
    endpointRecurrenceRetryPlanCatalog
  );
  return filterEndpointRecurrenceRetryPlans(items);
}

async function loadEndpointRecurrenceOwnerDigests() {
  const items = await loadEndpointRecurrenceActionItems(
    "endpoint-remediation-sla-escalation-owner-digest",
    endpointRecurrenceOwnerDigestCatalog
  );
  return filterEndpointRecurrenceOwnerDigests(items);
}

async function loadEndpointRecurrenceSuppressionTrends() {
  const items = await loadEndpointRecurrenceActionItems(
    "endpoint-remediation-sla-escalation-suppression-trend",
    endpointRecurrenceSuppressionTrendCatalog
  );
  return filterEndpointRecurrenceSuppressionTrends(items);
}

function selectedGoDrillNotificationFilters() {
  return {
    owner: document.querySelector("#filterGoDrillNotificationOwner")?.value.trim().toLowerCase() || "",
    provider: document.querySelector("#filterGoDrillNotificationProvider")?.value || "",
    state: document.querySelector("#filterGoDrillNotificationState")?.value || "",
    kind: document.querySelector("#filterGoDrillNotificationKind")?.value || "",
    deliverySource: document.querySelector("#filterGoDrillDeliverySource")?.value || "",
    action: document.querySelector("#filterGoDrillNotificationAction")?.value || "",
    category: document.querySelector("#filterGoDrillNotificationCategory")?.value || ""
  };
}

function goDrillNotificationPayload(item) {
  if (item?.plan && typeof item.plan === "object") return item.plan;
  if (item?.acknowledgement && typeof item.acknowledgement === "object") return item.acknowledgement;
  if (item?.escalation_plan && typeof item.escalation_plan === "object") return item.escalation_plan;
  if (item?.acknowledgement_audit_package && typeof item.acknowledgement_audit_package === "object") return item.acknowledgement_audit_package;
  if (item?.acknowledgement_audit_delivery_plan && typeof item.acknowledgement_audit_delivery_plan === "object") return item.acknowledgement_audit_delivery_plan;
  if (item?.acknowledgement_audit_delivery_retry_plan && typeof item.acknowledgement_audit_delivery_retry_plan === "object") return item.acknowledgement_audit_delivery_retry_plan;
  if (item?.retry_execution_approval_plan && typeof item.retry_execution_approval_plan === "object") return item.retry_execution_approval_plan;
  if (item?.retry_execution_approval_decision && typeof item.retry_execution_approval_decision === "object") return item.retry_execution_approval_decision;
  if (item?.retry_execution_record && typeof item.retry_execution_record === "object") return item.retry_execution_record;
  if (item?.connector_recovery_playbook && typeof item.connector_recovery_playbook === "object") return item.connector_recovery_playbook;
  if (item?.connector_recovery_closure && typeof item.connector_recovery_closure === "object") return item.connector_recovery_closure;
  if (item?.retry_recovery_report && typeof item.retry_recovery_report === "object") return item.retry_recovery_report;
  if (item?.recovery_escalation_plan && typeof item.recovery_escalation_plan === "object") return item.recovery_escalation_plan;
  if (item?.recovery_escalation_acknowledgement && typeof item.recovery_escalation_acknowledgement === "object") return item.recovery_escalation_acknowledgement;
  if (item?.recovery_escalation_delivery_retry_plan && typeof item.recovery_escalation_delivery_retry_plan === "object") return item.recovery_escalation_delivery_retry_plan;
  if (item?.recovery_escalation_retry_worker_run && typeof item.recovery_escalation_retry_worker_run === "object") return item.recovery_escalation_retry_worker_run;
  if (item?.recovery_escalation_retry_execution_record && typeof item.recovery_escalation_retry_execution_record === "object") return item.recovery_escalation_retry_execution_record;
  if (item?.recovery_escalation_retry_health && typeof item.recovery_escalation_retry_health === "object") return item.recovery_escalation_retry_health;
  if (item?.recovery_escalation_retry_health_alert_plan && typeof item.recovery_escalation_retry_health_alert_plan === "object") return item.recovery_escalation_retry_health_alert_plan;
  if (item?.recovery_escalation_retry_health_alert_delivery_retry_plan && typeof item.recovery_escalation_retry_health_alert_delivery_retry_plan === "object") return item.recovery_escalation_retry_health_alert_delivery_retry_plan;
  if (item?.recovery_escalation_retry_health_alert_delivery_retry_worker_run && typeof item.recovery_escalation_retry_health_alert_delivery_retry_worker_run === "object") return item.recovery_escalation_retry_health_alert_delivery_retry_worker_run;
  if (item?.recovery_escalation_retry_health_alert_delivery_retry_execution_record && typeof item.recovery_escalation_retry_health_alert_delivery_retry_execution_record === "object") return item.recovery_escalation_retry_health_alert_delivery_retry_execution_record;
  if (item?.recovery_executive_report && typeof item.recovery_executive_report === "object") return item.recovery_executive_report;
  if (item?.recovery_executive_report_schedule_run && typeof item.recovery_executive_report_schedule_run === "object") return item.recovery_executive_report_schedule_run;
  if (item?.recovery_executive_report_delivery_retry_plan && typeof item.recovery_executive_report_delivery_retry_plan === "object") return item.recovery_executive_report_delivery_retry_plan;
  if (item?.recovery_executive_report_delivery_retry_worker_run && typeof item.recovery_executive_report_delivery_retry_worker_run === "object") return item.recovery_executive_report_delivery_retry_worker_run;
  if (item?.recovery_executive_report_delivery_retry_execution_record && typeof item.recovery_executive_report_delivery_retry_execution_record === "object") return item.recovery_executive_report_delivery_retry_execution_record;
  if (item?.recovery_executive_report_delivery_retry_health && typeof item.recovery_executive_report_delivery_retry_health === "object") return item.recovery_executive_report_delivery_retry_health;
  if (item?.recovery_executive_report_delivery_retry_health_alert_plan && typeof item.recovery_executive_report_delivery_retry_health_alert_plan === "object") return item.recovery_executive_report_delivery_retry_health_alert_plan;
  if (item?.recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan && typeof item.recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan === "object") return item.recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan;
  if (item?.recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run && typeof item.recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run === "object") return item.recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run;
  if (item?.recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record && typeof item.recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record === "object") return item.recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record;
  if (item?.acknowledgement_audit_delivery_worker_run && typeof item.acknowledgement_audit_delivery_worker_run === "object") return item.acknowledgement_audit_delivery_worker_run;
  if (item?.worker_health_alert_plan && typeof item.worker_health_alert_plan === "object") return item.worker_health_alert_plan;
  return item || {};
}

function goDrillNotificationProviders(item) {
  const escalationRoutes = item?.escalation_plan && typeof item.escalation_plan === "object" && Array.isArray(item.escalation_plan.routes)
    ? item.escalation_plan.routes
    : [];
  const auditRoutes = item?.acknowledgement_audit_package && typeof item.acknowledgement_audit_package === "object" && Array.isArray(item.acknowledgement_audit_package.routes)
    ? item.acknowledgement_audit_package.routes
    : [];
  const recoveryRoutes = item?.recovery_escalation_plan && typeof item.recovery_escalation_plan === "object" && Array.isArray(item.recovery_escalation_plan.escalation_routes)
    ? item.recovery_escalation_plan.escalation_routes
    : [];
  const providers = [
    item?.provider,
    ...(Array.isArray(item?.selected_providers) ? item.selected_providers : []),
    ...(Array.isArray(item?.acknowledgement_required_providers) ? item.acknowledgement_required_providers : []),
    ...(Array.isArray(item?.providers) ? item.providers : []),
    ...(Array.isArray(item?.failed_providers) ? item.failed_providers : []),
    ...escalationRoutes.map((route) => route.provider),
    ...auditRoutes.map((route) => route.provider),
    ...recoveryRoutes.map((route) => route.provider)
  ].filter(Boolean);
  return [...new Set(providers.map(String))];
}

function goDrillDeliverySource(item) {
  if (item?.connector_delivery_source) return String(item.connector_delivery_source);
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-package") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-plan") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-ack") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-plan") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-closure") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-ack") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-delivery-retry-plan") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-worker-run") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-execution-record") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-plan") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-ack") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-plan") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-worker-run") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-execution-record") return "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-plan") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-worker-run") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-execution-record") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-plan") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-ack") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-plan") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-worker-run") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-execution-record") return "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run") return "go_backend_rollback_drill_acknowledgement_audit";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan") return "go_backend_rollback_drill_acknowledgement_audit_worker_health_alert";
  if (item?.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-ack") return "go_backend_rollback_drill_acknowledgement_audit_worker_health_alert";
  return "go_backend_rollback_drill_notification";
}

function goDrillNotificationStatus(item) {
  if (item?.acknowledgement_state) return String(item.acknowledgement_state);
  if (item?.delivery_success === false) return "delivery_failed";
  if (item?.delivery_success === true) return "delivered";
  if (item?.alert_level) return String(item.alert_level);
  return "indexed";
}

function filterGoDrillNotificationHistory(items) {
  const filters = selectedGoDrillNotificationFilters();
  return items.filter((item) => {
    if (filters.kind && item.metadata_kind !== filters.kind) return false;
    if (filters.deliverySource && goDrillDeliverySource(item) !== filters.deliverySource) return false;
    if (filters.provider && !goDrillNotificationProviders(item).includes(filters.provider)) return false;
    if (filters.state) {
      const status = goDrillNotificationStatus(item);
      if (filters.state === "outstanding") {
        const payload = goDrillNotificationPayload(item);
        if (!payload.routes?.some((route) => route.acknowledgement_state === "outstanding" || route.acknowledged === false)) return false;
      } else if (status !== filters.state) {
        return false;
      }
    }
    return true;
  });
}

function buildSampleGoDrillNotificationDashboard(items) {
  const plans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-notification-plan");
  const deliveries = items.filter((item) => item.metadata_kind === "release-connector-delivery");
  const auditPackages = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-package");
  const auditDeliveryPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-plan");
  const auditRetryPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan");
  const auditRetryAcks = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-ack");
  const auditRetryApprovalPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-plan");
  const auditRetryApprovalDecisions = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision");
  const auditRetryExecutionRecords = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record");
  const auditRecoveryPlaybooks = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook");
  const auditRecoveryClosures = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-closure");
  const auditRecoveryEscalationPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan");
  const auditRecoveryEscalationAcks = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-ack");
  const auditRecoveryEscalationRetryPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-delivery-retry-plan");
  const auditRecoveryEscalationRetryWorkerRuns = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-worker-run");
  const auditRecoveryEscalationRetryExecutionRecords = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-execution-record");
  const auditRecoveryEscalationRetryHealthReports = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health");
  const auditRecoveryEscalationRetryHealthAlerts = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-plan");
  const auditRecoveryEscalationRetryHealthAcks = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-ack");
  const auditRecoveryEscalationRetryHealthAlertRetryPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-plan");
  const auditRecoveryEscalationRetryHealthAlertRetryWorkerRuns = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-worker-run");
  const auditRecoveryEscalationRetryHealthAlertRetryExecutions = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-execution-record");
  const auditRecoveryExecutiveReports = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report");
  const auditRecoveryExecutiveScheduleRuns = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run");
  const auditRecoveryExecutiveDeliveries = deliveries.filter((item) => item.connector_delivery_source === "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report");
  const auditRecoveryExecutiveDeliveryRetryPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-plan");
  const auditRecoveryExecutiveDeliveryRetryWorkerRuns = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-worker-run");
  const auditRecoveryExecutiveDeliveryRetryExecutionRecords = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-execution-record");
  const auditRecoveryExecutiveDeliveryRetryHealthReports = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health");
  const auditRecoveryExecutiveDeliveryRetryHealthAlerts = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-plan");
  const auditRecoveryExecutiveDeliveryRetryHealthAcks = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-ack");
  const auditRecoveryExecutiveDeliveryRetryHealthAlertDeliveries = deliveries.filter((item) => item.connector_delivery_source === "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert");
  const auditRecoveryExecutiveDeliveryRetryHealthAlertRetryPlans = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-plan");
  const auditRecoveryExecutiveDeliveryRetryHealthAlertRetryWorkerRuns = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-worker-run");
  const auditRecoveryExecutiveDeliveryRetryHealthAlertRetryExecutions = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-execution-record");
  const auditWorkerRuns = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run");
  const auditWorkerHealthAlerts = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan");
  const auditWorkerHealthAcks = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-ack");
  const auditDeliveries = deliveries.filter((item) => item.connector_delivery_source === "go_backend_rollback_drill_acknowledgement_audit");
  const acknowledgements = items.filter((item) => item.metadata_kind === "go-backend-rollback-drill-notification-ack");
  const escalationRoutes = items.flatMap((item) => {
    const plan = item.escalation_plan && typeof item.escalation_plan === "object" ? item.escalation_plan : {};
    return Array.isArray(plan.routes) ? plan.routes : [];
  });
  const outstanding = escalationRoutes.filter((route) => route.acknowledged === false || route.acknowledgement_state === "outstanding");
  const failedDeliveries = deliveries.filter((item) => item.delivery_success === false);
  const failedAuditDeliveries = auditDeliveries.filter((item) => item.delivery_success === false);
  const auditDeliverySuccessCount = auditDeliveries.filter((item) => item.delivery_success === true).length;
  return {
    alert_level: failedDeliveries.length || outstanding.length ? "critical" : "healthy",
    plan_count: plans.length,
    delivery_count: deliveries.length,
    failed_delivery_count: failedDeliveries.length,
    acknowledgement_count: acknowledgements.length,
    acknowledgement_audit_package_count: auditPackages.length,
    acknowledgement_audit_delivery_plan_count: auditDeliveryPlans.length,
    acknowledgement_audit_delivery_count: auditDeliveries.length,
    failed_acknowledgement_audit_delivery_count: failedAuditDeliveries.length,
    acknowledgement_audit_delivery_success_count: auditDeliverySuccessCount,
    acknowledgement_audit_delivery_success_rate: auditDeliveries.length ? auditDeliverySuccessCount / auditDeliveries.length : null,
    acknowledgement_audit_delivery_health: failedAuditDeliveries.length ? "critical" : "healthy",
    acknowledgement_audit_delivery_retry_plan_count: auditRetryPlans.length,
    acknowledgement_audit_delivery_retryable_count: auditRetryPlans.reduce((total, item) => total + Number(item.retryable_count || 0), 0),
    acknowledgement_audit_delivery_retry_ack_count: auditRetryAcks.length,
    acknowledgement_audit_delivery_retry_execution_approval_plan_count: auditRetryApprovalPlans.length,
    acknowledgement_audit_delivery_retry_execution_approval_decision_count: auditRetryApprovalDecisions.length,
    acknowledgement_audit_delivery_retry_execution_approved_count: auditRetryApprovalDecisions.filter((item) => item.approval_state === "approved").length,
    acknowledgement_audit_delivery_retry_execution_record_count: auditRetryExecutionRecords.length,
    acknowledgement_audit_delivery_retry_execution_success_count: auditRetryExecutionRecords.filter((item) => item.execution_status === "delivered").length,
    acknowledgement_audit_delivery_retry_execution_failed_count: auditRetryExecutionRecords.filter((item) => ["failed", "skipped"].includes(item.execution_status)).length,
    acknowledgement_audit_delivery_connector_recovery_playbook_count: auditRecoveryPlaybooks.length,
    acknowledgement_audit_delivery_connector_recovery_closure_count: auditRecoveryClosures.length,
    acknowledgement_audit_delivery_connector_recovery_closed_count: auditRecoveryClosures.filter((item) => ["resolved", "mitigated"].includes(item.closure_state)).length,
    acknowledgement_audit_delivery_recovery_escalation_plan_count: auditRecoveryEscalationPlans.length,
    acknowledgement_audit_delivery_recovery_escalation_route_count: auditRecoveryEscalationPlans.reduce((total, item) => total + Number(item.escalation_count || 0), 0),
    acknowledgement_audit_delivery_recovery_escalation_ack_count: auditRecoveryEscalationAcks.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_plan_count: auditRecoveryEscalationRetryPlans.length,
    acknowledgement_audit_delivery_recovery_escalation_retryable_count: auditRecoveryEscalationRetryPlans.reduce((total, item) => total + Number(item.retryable_count || 0), 0),
    acknowledgement_audit_delivery_recovery_escalation_retry_worker_run_count: auditRecoveryEscalationRetryWorkerRuns.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_count: auditRecoveryEscalationRetryExecutionRecords.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_execution_success_count: auditRecoveryEscalationRetryExecutionRecords.filter((item) => item.execution_status === "delivered").length,
    acknowledgement_audit_delivery_recovery_escalation_retry_execution_failed_count: auditRecoveryEscalationRetryExecutionRecords.filter((item) => ["failed", "skipped"].includes(item.execution_status)).length,
    acknowledgement_audit_delivery_recovery_escalation_retry_health_count: auditRecoveryEscalationRetryHealthReports.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_count: auditRecoveryEscalationRetryHealthReports.reduce((total, item) => total + Number(item.alert_count || 0), 0),
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_count: auditRecoveryEscalationRetryHealthAlerts.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_ack_count: auditRecoveryEscalationRetryHealthAcks.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_count: auditRecoveryEscalationRetryHealthAlertRetryPlans.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retryable_count: auditRecoveryEscalationRetryHealthAlertRetryPlans.reduce((total, item) => total + Number(item.retryable_count || 0), 0),
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_count: auditRecoveryEscalationRetryHealthAlertRetryWorkerRuns.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record_count: auditRecoveryEscalationRetryHealthAlertRetryExecutions.length,
    acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_failed_count: auditRecoveryEscalationRetryHealthAlertRetryExecutions.filter((item) => ["failed", "skipped"].includes(item.execution_status)).length,
    acknowledgement_audit_delivery_recovery_executive_report_count: auditRecoveryExecutiveReports.length,
    acknowledgement_audit_delivery_recovery_executive_report_schedule_run_count: auditRecoveryExecutiveScheduleRuns.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_count: auditRecoveryExecutiveDeliveries.length,
    failed_acknowledgement_audit_delivery_recovery_executive_report_delivery_count: auditRecoveryExecutiveDeliveries.filter((item) => item.delivery_success === false).length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan_count: auditRecoveryExecutiveDeliveryRetryPlans.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retryable_count: auditRecoveryExecutiveDeliveryRetryPlans.reduce((total, item) => total + Number(item.retryable_count || 0), 0),
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run_count: auditRecoveryExecutiveDeliveryRetryWorkerRuns.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record_count: auditRecoveryExecutiveDeliveryRetryExecutionRecords.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_success_count: auditRecoveryExecutiveDeliveryRetryExecutionRecords.filter((item) => item.execution_status === "delivered").length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_failed_count: auditRecoveryExecutiveDeliveryRetryExecutionRecords.filter((item) => ["failed", "skipped"].includes(item.execution_status)).length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_count: auditRecoveryExecutiveDeliveryRetryHealthReports.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_count: auditRecoveryExecutiveDeliveryRetryHealthReports.reduce((total, item) => total + Number(item.alert_count || 0), 0),
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_count: auditRecoveryExecutiveDeliveryRetryHealthAlerts.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_ack_count: auditRecoveryExecutiveDeliveryRetryHealthAcks.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_count: auditRecoveryExecutiveDeliveryRetryHealthAlertDeliveries.length,
    failed_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_count: auditRecoveryExecutiveDeliveryRetryHealthAlertDeliveries.filter((item) => item.delivery_success === false).length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_count: auditRecoveryExecutiveDeliveryRetryHealthAlertRetryPlans.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retryable_count: auditRecoveryExecutiveDeliveryRetryHealthAlertRetryPlans.reduce((total, item) => total + Number(item.retryable_count || 0), 0),
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_count: auditRecoveryExecutiveDeliveryRetryHealthAlertRetryWorkerRuns.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record_count: auditRecoveryExecutiveDeliveryRetryHealthAlertRetryExecutions.length,
    acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_failed_count: auditRecoveryExecutiveDeliveryRetryHealthAlertRetryExecutions.filter((item) => ["failed", "skipped"].includes(item.execution_status)).length,
    acknowledgement_audit_delivery_worker_run_count: auditWorkerRuns.length,
    acknowledgement_audit_delivery_worker_dry_run_count: auditWorkerRuns.filter((item) => item.dry_run !== false).length,
    acknowledgement_audit_delivery_worker_executed_count: auditWorkerRuns.filter((item) => item.dry_run === false).length,
    acknowledgement_audit_delivery_worker_health_alert_count: auditWorkerHealthAlerts.length,
    acknowledgement_audit_delivery_worker_health_alert_ack_count: auditWorkerHealthAcks.length,
    outstanding_acknowledgement_count: outstanding.length,
    outstanding_acknowledgements: outstanding.map((route) => ({
      schedule_id: route.schedule_id,
      provider: route.provider,
      plan_id: route.plan_id
    })),
    latest: items.slice(0, 10)
  };
}

function goDrillEscalationRoutes(historyItems, dashboard = {}) {
  const filters = selectedGoDrillNotificationFilters();
  let routes = historyItems.flatMap((item) => {
    const plan = item.escalation_plan && typeof item.escalation_plan === "object" ? item.escalation_plan : {};
    return Array.isArray(plan.routes)
      ? plan.routes.map((route) => ({ ...route, escalation_plan_id: item.plan_id || plan.plan_id }))
      : [];
  });
  if (!routes.length) {
    routes = (dashboard.outstanding_acknowledgements || []).map((route) => ({
      schedule_id: route.schedule_id,
      plan_id: route.plan_id,
      provider: route.provider,
      owner: "release-governance",
      acknowledgement_state: "outstanding",
      acknowledged: false,
      age_minutes: null,
      acknowledgement_minutes: null,
      breached: false,
      recommended_action: "wait_for_acknowledgement"
    }));
  }
  return routes.filter((route) => {
    if (filters.provider && route.provider !== filters.provider) return false;
    if (filters.state && filters.state !== (route.acknowledgement_state || (route.acknowledged ? "acknowledged" : "outstanding"))) return false;
    return true;
  });
}

function goDrillRouteCategory(route) {
  if (route.action !== "suppress") return route.action || "deliver";
  if (route.maintenance_window) return "maintenance_window";
  if (route.owner_availability && route.owner_availability.available === false) return "owner_calendar";
  if (String(route.reason || "").toLowerCase().includes("healthy")) return "healthy_schedule";
  return route.category || "other";
}

function sampleGoDrillRoutingRows(items) {
  return items.flatMap((item) => {
    const plan = item?.plan && typeof item.plan === "object" ? item.plan : {};
    const routeDecisions = Array.isArray(plan.route_decisions) ? plan.route_decisions : [];
    return routeDecisions.map((route, index) => ({
      route_id: `sample-go-drill-route-${index}`,
      created_at: item.created_at || plan.generated_at || "",
      plan_id: plan.plan_id || item.plan_id || "",
      schedule_id: plan.schedule_id || item.schedule_id || route.schedule_id || "",
      alert_level: plan.alert_level || item.alert_level || "unknown",
      provider: route.provider || "",
      owner: route.owner || "release-governance",
      escalation_owner: route.escalation_owner || route.owner || "release-governance",
      action: route.action || "deliver",
      category: goDrillRouteCategory(route),
      reason: route.reason || "",
      acknowledgement_minutes: route.acknowledgement_minutes,
      maintenance_window_id: route.maintenance_window?.window_id || "",
      maintenance_window_reason: route.maintenance_window?.reason || "",
      owner_available: route.owner_availability?.available !== false,
      owner_availability_reason: route.owner_availability?.reason || "",
      next_due_at: plan.next_due_at || "",
      route
    }));
  });
}

function filterGoDrillRoutingRows(rows) {
  const filters = selectedGoDrillNotificationFilters();
  return rows.filter((route) => {
    if (filters.owner && !String(`${route.owner} ${route.escalation_owner}`).toLowerCase().includes(filters.owner)) return false;
    if (filters.provider && route.provider !== filters.provider) return false;
    if (filters.action && route.action !== filters.action) return false;
    if (filters.category && route.category !== filters.category) return false;
    return true;
  });
}

function buildSampleGoDrillSuppressionTrend(rows) {
  const suppressed = rows.filter((route) => route.action === "suppress");
  const countBy = (key) => suppressed.reduce((counts, route) => {
    const value = route[key] || "unknown";
    counts[value] = Number(counts[value] || 0) + 1;
    return counts;
  }, {});
  const categoryCounts = countBy("category");
  return {
    schema_version: "cavra.go-backend-pilot.rollback-drill-routing-suppression-trend.v1",
    product: "CAVRA",
    trend_id: "sample-go-drill-routing-suppression-trend",
    generated_at: "2026-05-20T11:15:00+00:00",
    generated_by: "console",
    alert_level: suppressed.length ? "warning" : "healthy",
    suppression_event_count: suppressed.length,
    category_counts: categoryCounts,
    owner_counts: countBy("owner"),
    provider_counts: countBy("provider"),
    maintenance_suppressed_count: Number(categoryCounts.maintenance_window || 0),
    calendar_suppressed_count: Number(categoryCounts.owner_calendar || 0),
    healthy_schedule_suppressed_count: Number(categoryCounts.healthy_schedule || 0),
    latest_events: suppressed.slice(0, 20)
  };
}

async function loadGoRollbackDrillNotificationHistory() {
  await loadConsoleConfig();
  const filters = selectedGoDrillNotificationFilters();
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications", {
      provider: filters.provider,
      metadata_kind: filters.kind,
      connector_delivery_source: filters.deliverySource,
      acknowledgement_state: filters.state && filters.state !== "outstanding" ? filters.state : "",
      limit: 50
    }));
    if (!response.ok) throw new Error("Go rollback drill notification history API unavailable");
    const payload = await response.json();
    return filterGoDrillNotificationHistory(Array.isArray(payload) ? payload : payload.items || []);
  } catch {
    return filterGoDrillNotificationHistory(goRollbackDrillNotificationCatalog);
  }
}

async function loadGoRollbackDrillRoutingHistory() {
  await loadConsoleConfig();
  const filters = selectedGoDrillNotificationFilters();
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/routes", {
      owner: filters.owner,
      provider: filters.provider,
      action: filters.action,
      category: filters.category,
      limit: 50
    }));
    if (!response.ok) throw new Error("Go rollback drill routing history API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return filterGoDrillRoutingRows(sampleGoDrillRoutingRows(goRollbackDrillNotificationCatalog));
  }
}

async function loadGoRollbackDrillSuppressionTrend() {
  await loadConsoleConfig();
  const filters = selectedGoDrillNotificationFilters();
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/suppression-trends", {
      owner: filters.owner,
      provider: filters.provider
    }));
    if (!response.ok) throw new Error("Go rollback drill suppression trend API unavailable");
    const payload = await response.json();
    return payload.trend || payload;
  } catch {
    return buildSampleGoDrillSuppressionTrend(filterGoDrillRoutingRows(sampleGoDrillRoutingRows(goRollbackDrillNotificationCatalog)));
  }
}

async function loadGoRollbackDrillNotificationDashboard() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/dashboard"));
    if (!response.ok) throw new Error("Go rollback drill notification dashboard API unavailable");
    return await response.json();
  } catch {
    return buildSampleGoDrillNotificationDashboard(goRollbackDrillNotificationCatalog);
  }
}

async function loadGoRollbackDrillRetryRecoveryReport() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report", {
      recovery_slo_minutes: 240,
      generated_by: "console"
    }));
    if (!response.ok) throw new Error("Go rollback drill retry recovery report API unavailable");
    const payload = await response.json();
    return payload.report || payload;
  } catch {
    return buildSampleGoDrillRetryRecoveryReport(goRollbackDrillNotificationCatalog);
  }
}

async function loadEndpointManagementExportArtifacts(exportId) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl(`/endpoint-management-exports/${encodeURIComponent(exportId)}/artifacts`));
    if (!response.ok) throw new Error("Endpoint management export artifact API unavailable");
    return await response.json();
  } catch {
    return endpointManagementExportArtifactCatalog[exportId] || {
      schema_version: "cavra.evidence.artifacts.v1",
      product: "CAVRA",
      session_id: exportId,
      metadata_kind: "endpoint-management-export",
      artifact_root_configured: false,
      artifact_count: 0,
      artifacts: [],
      bundle_download_url: "",
      endpoint_management_export_integrity: { status: "incomplete" },
      download_readiness: { status: "blocked", rationale: "Endpoint export artifacts are not available from sample data." }
    };
  }
}

async function loadSessions() {
  await loadConsoleConfig();
  try {
    const params = {
      repository: document.querySelector("#filterActivityRepository")?.value.trim(),
      agent_id: document.querySelector("#filterActivityAgent")?.value.trim(),
      policy_pack: document.querySelector("#filterActivityPolicy")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/sessions", params));
    if (!response.ok) throw new Error("Session API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return activitySessions;
  }
}

async function loadDecisions() {
  await loadConsoleConfig();
  try {
    const params = {
      repository: document.querySelector("#filterActivityRepository")?.value.trim(),
      agent_id: document.querySelector("#filterActivityAgent")?.value.trim(),
      policy_pack: document.querySelector("#filterActivityPolicy")?.value.trim(),
      decision: document.querySelector("#filterDecisionState")?.value,
      severity: document.querySelector("#filterDecisionSeverity")?.value,
      limit: 25
    };
    const response = await fetch(apiUrl("/decisions", params));
    if (!response.ok) throw new Error("Decision API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return activityDecisions;
  }
}

async function loadRepositories() {
  await loadConsoleConfig();
  try {
    const params = {
      owner: document.querySelector("#filterRepositoryOwner")?.value.trim(),
      policy_pack: document.querySelector("#filterRepositoryPolicy")?.value.trim(),
      risk_tier: document.querySelector("#filterRepositoryRisk")?.value
    };
    const response = await fetch(apiUrl("/repositories", params));
    if (!response.ok) throw new Error("Repository API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return repositoryCatalog;
  }
}

async function loadPolicyRollouts() {
  await loadConsoleConfig();
  try {
    const params = {
      policy_pack: document.querySelector("#filterRepositoryPolicy")?.value.trim(),
      state: document.querySelector("#filterRolloutState")?.value,
      mode: document.querySelector("#filterRolloutMode")?.value
    };
    const response = await fetch(apiUrl("/policy-rollouts", params));
    if (!response.ok) throw new Error("Policy rollout API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return rolloutCatalog;
  }
}

async function loadPolicyRolloutDetail(rolloutId) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl(`/policy-rollout-details/${encodeURIComponent(rolloutId)}`));
    if (!response.ok) throw new Error("Policy rollout detail API unavailable");
    return await response.json();
  } catch {
    const rollout = rolloutCatalog.find((item) => item.rollout_id === rolloutId);
    if (!rollout) return null;
    const repository = repositoryCatalog.find((item) => item.repository === rollout.repository);
    const decisions = activityDecisions.filter((item) => item.repository === rollout.repository && item.policy_pack === rollout.policy_pack);
    return {
      schema_version: "cavra.policy_rollout.detail.v1",
      product: "CAVRA",
      rollout,
      repository,
      policy_pack: {
        id: rollout.policy_pack,
        title: rollout.policy_pack,
        version: rollout.policy_version,
        rule_summary: { filesystem: 8, commands: 6, git: 2, mcp: 3, approvals: 2, evidence: 3 }
      },
      activity_summary: {
        total: decisions.length,
        outcomes: decisions.reduce((acc, item) => ({ ...acc, [item.decision]: (acc[item.decision] || 0) + 1 }), {}),
        severities: decisions.reduce((acc, item) => ({ ...acc, [item.severity]: (acc[item.severity] || 0) + 1 }), {}),
        recent_decisions: decisions.slice(0, 5)
      },
      integration_summary: {
        total: integrationCatalog.length,
        by_category: integrationCatalog.reduce((acc, item) => ({ ...acc, [item.category]: (acc[item.category] || 0) + 1 }), {}),
        by_health: integrationCatalog.reduce((acc, item) => ({ ...acc, [item.health_status]: (acc[item.health_status] || 0) + 1 }), {})
      },
      readiness: {
        status: Number(rollout.coverage_percent || 0) >= 80 ? "ready" : "needs_attention",
        checks: [
          { id: "repository_registered", status: repository ? "pass" : "warn", message: repository ? "Repository inventory record is present." : "Repository inventory record is missing." },
          { id: "policy_coverage", status: Number(rollout.coverage_percent || 0) >= 80 ? "pass" : "warn", message: `Coverage is ${Number(rollout.coverage_percent || 0)}%.` }
        ]
      }
    };
  }
}

async function loadPolicyCatalog() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/policy-pack-catalog"));
    if (!response.ok) throw new Error("Policy catalog API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return policyCatalog;
  }
}

function draftPolicyPayload() {
  return {
    id: document.querySelector("#draftPolicyId").value.trim(),
    title: document.querySelector("#draftPolicyTitle").value.trim(),
    description: "Platform-authored policy draft from the CAVRA console.",
    version: document.querySelector("#draftPolicyVersion").value.trim(),
    inherits: document.querySelector("#draftPolicyInherits").value.trim(),
    commands: { block: ["terraform apply -auto-approve", "kubectl delete namespace"] },
    filesystem: { block_read: [".env", "secrets/"], require_approval_write: ["iam/"] },
    git: { require_ai_attestation: true, require_pull_request: true }
  };
}

function rolloutChangePayload() {
  return {
    rollout_id: document.querySelector("#changeRolloutId").value.trim(),
    repository: document.querySelector("#changeRepository").value.trim(),
    policy_pack: document.querySelector("#changePolicyPack").value.trim(),
    mode: document.querySelector("#changeMode").value,
    state: document.querySelector("#changeState").value,
    coverage_percent: Number(document.querySelector("#changeCoverage").value || 0)
  };
}

async function previewPolicyDraft() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/policy-packs/draft"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(draftPolicyPayload())
    });
    if (!response.ok) throw new Error("Policy draft API unavailable");
    renderPolicyDraft(await response.json());
  } catch {
    const payload = draftPolicyPayload();
    renderPolicyDraft({
      schema_version: "cavra.policy_pack.draft.v1",
      product: "CAVRA",
      valid: payload.id.startsWith("cavra-"),
      errors: payload.id.startsWith("cavra-") ? [] : ["metadata.id must start with cavra-"],
      policy_pack: { metadata: { id: payload.id, title: payload.title, version: payload.version, inherits: payload.inherits } },
      summary: { policy_id: payload.id, title: payload.title, version: payload.version, inherits: payload.inherits, rule_counts: { filesystem: 3, commands: 2, git: 2 } },
      operator_notes: ["Sample draft preview; connect the API for schema validation."]
    });
  }
}

async function planPolicyPublish() {
  await loadConsoleConfig();
  const payload = draftPolicyPayload();
  try {
    const response = await fetch(apiUrl("/policy-packs/publish-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Policy publish plan API unavailable");
    renderPolicyPublishPlan(await response.json(), null);
  } catch {
    renderPolicyPublishPlan(samplePolicyPublishPlan(payload), null);
  }
}

async function requestPolicyPublishApproval() {
  await loadConsoleConfig();
  const payload = draftPolicyPayload();
  try {
    const response = await fetch(apiUrl("/policy-packs/publish-request"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({ draft: payload, requested_by: "platform-security", approver_group: "Platform Security" })
    });
    if (!response.ok) throw new Error("Policy publish request API unavailable");
    const result = await response.json();
    lastPolicyPublishApprovalId = result.approval?.approval_id || "";
    document.querySelector("#policyPublishApprovalId").value = lastPolicyPublishApprovalId;
    renderPolicyPublishPlan(result.plan, result.approval);
    await refreshApprovals();
  } catch {
    lastPolicyPublishApprovalId = `apr_policy_${Date.now()}`;
    document.querySelector("#policyPublishApprovalId").value = lastPolicyPublishApprovalId;
    renderPolicyPublishPlan(samplePolicyPublishPlan(payload), {
      approval_id: lastPolicyPublishApprovalId,
      state: "pending",
      approver_group: "Platform Security",
      requested_by: "platform-security"
    });
  }
}

async function publishPolicyPack() {
  await loadConsoleConfig();
  const approvalId = document.querySelector("#policyPublishApprovalId").value.trim() || lastPolicyPublishApprovalId;
  const payload = draftPolicyPayload();
  try {
    const response = await fetch(apiUrl("/policy-packs/publish"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({ draft: payload, approval_id: approvalId, signer: "platform-security" })
    });
    if (!response.ok) throw new Error("Policy publish API unavailable");
    renderPolicyPublishResult(await response.json());
    await refreshPolicyCatalog();
  } catch {
    renderPolicyPublishResult({
      schema_version: "cavra.policy_pack.publish_result.v1",
      product: "CAVRA",
      status: approvalId ? "waiting_for_approval" : "approval_required",
      policy_id: payload.id,
      policy_digest: "sample-digest",
      approval: { approval_id: approvalId || "n/a", state: approvalId ? "pending" : "missing" },
      operator_notes: ["Approve the policy publish request before signed write-back."]
    });
  }
}

function samplePolicyPublishPlan(payload) {
  return {
    schema_version: "cavra.policy_pack.publish_plan.v1",
    product: "CAVRA",
    operation: "create",
    valid: payload.id.startsWith("cavra-"),
    errors: payload.id.startsWith("cavra-") ? [] : ["metadata.id must start with cavra-"],
    approval_required: true,
    risk: "high",
    policy_id: payload.id,
    policy_digest: "sample-digest",
    target_path: `policies/${payload.id}/policy.yaml`,
    summary: { policy_id: payload.id, title: payload.title, version: payload.version, rule_counts: { filesystem: 3, commands: 2, git: 2 } },
    diff: { added: ["metadata", "filesystem", "commands", "git"], removed: [], changed: [] },
    operator_notes: ["Sample publish plan; connect the API for approval-bound signed write-back."]
  };
}

async function planRolloutChange() {
  await loadConsoleConfig();
  const payload = rolloutChangePayload();
  try {
    const response = await fetch(apiUrl("/policy-rollouts/change-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Rollout plan API unavailable");
    renderRolloutChangePlan(await response.json(), false);
  } catch {
    const before = rolloutCatalog.find((item) => item.rollout_id === payload.rollout_id);
    renderRolloutChangePlan({
      schema_version: "cavra.policy_rollout.change_plan.v1",
      product: "CAVRA",
      operation: before ? "update" : "create",
      risk: payload.mode === "strict" ? "high" : "medium",
      approval_required: payload.mode === "strict" || payload.mode === "break_glass",
      before,
      after: { ...(before || {}), ...payload },
      changes: Object.entries(payload).map(([field, value]) => ({ field, before: before?.[field], after: value })),
      operator_notes: ["Sample rollout plan; connect the API to persist changes."]
    }, false);
  }
}

async function applyRolloutChange() {
  await loadConsoleConfig();
  const payload = rolloutChangePayload();
  try {
    const response = await fetch(apiUrl("/policy-rollouts/apply-change"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Rollout apply API unavailable");
    const result = await response.json();
    renderRolloutChangePlan(result.plan, true);
    await refreshInventory();
  } catch {
    const index = rolloutCatalog.findIndex((item) => item.rollout_id === payload.rollout_id);
    if (index >= 0) rolloutCatalog[index] = { ...rolloutCatalog[index], ...payload };
    else rolloutCatalog.push({ owner: "platform-security", policy_version: "latest", evidence_refs: [], ...payload });
    renderRolloutChangePlan({
      schema_version: "cavra.policy_rollout.change_plan.v1",
      product: "CAVRA",
      operation: index >= 0 ? "update" : "create",
      risk: payload.mode === "strict" ? "high" : "medium",
      approval_required: payload.mode === "strict",
      before: null,
      after: payload,
      changes: Object.entries(payload).map(([field, value]) => ({ field, before: null, after: value })),
      operator_notes: ["Applied locally because the API was unavailable."]
    }, true);
    await refreshInventory();
  }
}

async function loadDeploymentReadiness() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/deployment/production-readiness"));
    if (!response.ok) throw new Error("Deployment readiness API unavailable");
    return await response.json();
  } catch {
    return {
      schema_version: "cavra.deployment.production_readiness.v1",
      product: "CAVRA",
      status: "needs_attention",
      checks: [
        { id: "oidc_configured", status: consoleConfig?.approval_oidc === "configured" ? "pass" : "warn", message: "Console and approval actions validate signed OIDC tokens." },
        { id: "rbac_configured", status: consoleConfig?.approval_rbac === "configured" ? "pass" : "warn", message: "Repository-scoped RBAC policy is configured." },
        { id: "cors_restricted", status: (consoleConfig?.cors_origins || []).length ? "pass" : "warn", message: "Allowed console origins are explicit." },
        { id: "go_backend_pilot", status: "pass", message: "Optional Go backend pilot is disabled or ready with Python fallback and parity gate evidence." },
        { id: "go_backend_deployment_paths", status: "pass", message: "Go backend CI runner and workstation deployment paths are ready when the pilot is enabled." },
        { id: "go_backend_promotion_gate", status: "pass", message: "Promoted Go backend mode requires runtime, deployment, and audited parity evidence." },
        { id: "go_backend_rollback_controls", status: "pass", message: "Promoted Go backend mode requires an approved rollback plan back to Python-only mode." },
        { id: "go_backend_rollback_rehearsal", status: "pass", message: "Promoted Go backend mode requires rollback rehearsal evidence and dashboard visibility." },
        { id: "go_backend_rollback_drill_history", status: "pass", message: "Promoted Go backend mode requires fresh operational drill history for returning to Python-only mode." },
        { id: "go_backend_rollback_drill_schedule", status: "pass", message: "Promoted Go backend mode requires recurring rollback drill scheduling and stale-drill notification routes." }
      ],
      go_backend_pilot: { schema_version: "cavra.go-backend-pilot.readiness.v1", mode: "disabled", status: "disabled", checks: [] },
      go_backend_deployment: { schema_version: "cavra.go-backend-pilot.deployment-readiness.v1", mode: "disabled", status: "not_configured", checks: [], ci_runner_targets: [], workstation_targets: [], channels: [] },
      go_backend_promotion: { schema_version: "cavra.go-backend-pilot.promotion-readiness.v1", mode: "disabled", status: "not_requested", checks: [] },
      go_backend_rollback: { schema_version: "cavra.go-backend-pilot.rollback-readiness.v1", mode: "disabled", status: "not_requested", checks: [] },
      go_backend_rollback_rehearsal: { schema_version: "cavra.go-backend-pilot.rollback-rehearsal.v1", mode: "disabled", status: "not_requested", checks: [], rehearsal: {} },
      go_backend_rollback_drill_history: { schema_version: "cavra.go-backend-pilot.rollback-drill-history.v1", mode: "disabled", status: "not_requested", checks: [], history: {} },
      go_backend_rollback_drill_schedule: { schema_version: "cavra.go-backend-pilot.rollback-drill-schedule.v1", mode: "disabled", status: "not_requested", checks: [], schedule: {} },
      operator_notes: ["Connect to the API for full persistent-store and evidence-artifact readiness checks."]
    };
  }
}

async function loadSecurityBoundary() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/console/security-boundary"));
    if (!response.ok) throw new Error("Security boundary API unavailable");
    return await response.json();
  } catch {
    return {
      schema_version: "cavra.console.security_boundary.v1",
      product: "CAVRA",
      mode: "local_or_demo",
      oidc: { configured: false, config_env: "CAVRA_APPROVAL_OIDC_CONFIG", supported_algorithms: ["RS256"], validated_claims: ["iss", "aud", "exp", "nbf", "groups", "roles"] },
      rbac: { configured: false, config_env: "CAVRA_APPROVAL_RBAC_FILE", boundaries: ["approval_group", "repository_permissions", "group_mappings"] },
      cors: { configured: Array.isArray(consoleConfig?.cors_origins) && consoleConfig.cors_origins.length > 0, origins: consoleConfig?.cors_origins || [] },
      console_permissions: ["read_activity", "read_inventory", "read_integrations", "read_evidence_metadata", "approval_decision_requires_actor_claims_or_token_when_configured"],
      operator_notes: ["Host the console behind enterprise identity before production use."]
    };
  }
}

async function loadConsoleSession() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/console/session"), { headers: apiHeaders() });
    if (!response.ok) throw new Error("Console session API unavailable");
    return await response.json();
  } catch {
    return {
      schema_version: "cavra.console.session.v1",
      product: "CAVRA",
      mode: consoleAuthToken ? "token_not_verified" : "local_or_demo",
      authenticated: false,
      auth_required: consoleConfig?.approval_oidc === "configured",
      actor: null,
      repository_permissions: [],
      permissions: {
        read_activity: true,
        read_inventory: true,
        read_integrations: true,
        read_evidence_metadata: true,
        decide_approvals: false,
        create_break_glass: false
      },
      operator_notes: ["Connect to the API to validate signed console tokens."]
    };
  }
}

async function loadIntegrations() {
  await loadConsoleConfig();
  try {
    const params = {
      category: document.querySelector("#filterIntegrationCategory")?.value,
      status: document.querySelector("#filterIntegrationStatus")?.value,
      health_status: document.querySelector("#filterIntegrationHealth")?.value,
      owner: document.querySelector("#filterIntegrationOwner")?.value.trim()
    };
    const response = await fetch(apiUrl("/integrations", params));
    if (!response.ok) throw new Error("Integration API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return integrationCatalog;
  }
}

async function loadApprovals() {
  await loadConsoleConfig();
  try {
    const params = {
      state: document.querySelector("#filterApprovalState")?.value,
      approver_group: document.querySelector("#filterApprovalGroup")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/approvals", params));
    if (!response.ok) throw new Error("Approval API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return approvalCatalog;
  }
}

async function loadAgents() {
  await loadConsoleConfig();
  try {
    const params = {
      status: document.querySelector("#filterAgentStatus")?.value,
      owner: document.querySelector("#filterAgentOwner")?.value.trim()
    };
    const response = await fetch(apiUrl("/agents", params));
    if (!response.ok) throw new Error("Agent registry API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return agentCatalog;
  }
}

async function loadMcpServers() {
  await loadConsoleConfig();
  try {
    const params = {
      trust_tier: document.querySelector("#filterMcpTrust")?.value,
      capability: document.querySelector("#filterMcpCapability")?.value
    };
    const response = await fetch(apiUrl("/mcp/servers", params));
    if (!response.ok) throw new Error("MCP registry API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return mcpCatalog;
  }
}

async function loadAgentProfiles() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/agents/profiles"));
    if (!response.ok) throw new Error("Agent profile API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return agentProfiles;
  }
}

async function loadMcpClassifications() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/mcp/tool-classifications"));
    if (!response.ok) throw new Error("MCP classification API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return mcpClassifications;
  }
}

function filterEvidence(items) {
  const metadataKind = document.querySelector("#filterMetadataKind")?.value;
  const rolloutStatus = document.querySelector("#filterRolloutStatus")?.value;
  const environment = document.querySelector("#filterEnvironment")?.value.trim().toLowerCase();
  const deploymentTarget = document.querySelector("#filterDeploymentTarget")?.value.trim().toLowerCase();
  const signer = document.querySelector("#filterSigner").value.trim().toLowerCase();
  const minBlocked = Number(document.querySelector("#filterBlocked").value || 0);
  const approvalValue = document.querySelector("#filterApprovals").value;
  const limit = Number(document.querySelector("#filterLimit").value || 10);
  return items
    .filter((item) => !metadataKind || item.metadata_kind === metadataKind)
    .filter((item) => !rolloutStatus || item.rollout_status === rolloutStatus)
    .filter((item) => !environment || String(item.environment || "").toLowerCase().includes(environment))
    .filter((item) => !deploymentTarget || (item.deployment_targets || []).some((target) => String(target).toLowerCase().includes(deploymentTarget)))
    .filter((item) => !signer || String(item.signer || "").toLowerCase().includes(signer))
    .filter((item) => Number(item.blocked_count || 0) >= minBlocked)
    .filter((item) => approvalValue === "" || (Number(item.approval_required_count || 0) > 0) === (approvalValue === "true"))
    .slice(0, limit);
}

function filterReleaseConnectorDeliveries(items) {
  const provider = document.querySelector("#filterReleaseDeliveryProvider")?.value.trim().toLowerCase();
  const eventType = document.querySelector("#filterReleaseDeliveryEvent")?.value;
  const success = document.querySelector("#filterReleaseDeliverySuccess")?.value;
  return items
    .filter((item) => !provider || (item.providers || []).some((value) => String(value).toLowerCase().includes(provider)))
    .filter((item) => !eventType || item.event_type === eventType)
    .filter((item) => success === "" || Boolean(item.delivery_success) === (success === "true"));
}

function filterReleaseChannelPromotions(items) {
  const channel = document.querySelector("#filterReleaseChannel")?.value.trim().toLowerCase();
  return items.filter((item) => !channel || String(item.channel || "").toLowerCase().includes(channel));
}

function filterEndpointManagementExports(items) {
  const channel = document.querySelector("#filterReleaseChannel")?.value.trim().toLowerCase();
  const provider = document.querySelector("#filterEndpointExportProvider")?.value.trim().toLowerCase();
  return items
    .filter((item) => !channel || String(item.channel || "").toLowerCase().includes(channel))
    .filter((item) => !provider || (item.providers || []).some((value) => String(value).toLowerCase().includes(provider)));
}

function filterEndpointPublicationDeliveries(items) {
  const provider = document.querySelector("#filterEndpointPublicationProvider")?.value.trim().toLowerCase();
  const channel = document.querySelector("#filterEndpointPublicationChannel")?.value.trim().toLowerCase();
  const success = document.querySelector("#filterEndpointPublicationSuccess")?.value;
  return items
    .filter((item) => !provider || (item.providers || []).some((value) => String(value).toLowerCase().includes(provider)))
    .filter((item) => !channel || String(item.channel || "").toLowerCase().includes(channel))
    .filter((item) => success === "" || Boolean(item.delivery_success) === (success === "true"));
}

function filterEndpointReconciliations(items) {
  const status = document.querySelector("#filterEndpointReconciliationStatus")?.value;
  const alert = document.querySelector("#filterEndpointReconciliationAlert")?.value;
  const target = document.querySelector("#filterEndpointReconciliationTarget")?.value.trim().toLowerCase();
  return items
    .filter((item) => !status || item.drift_status === status)
    .filter((item) => !alert || item.alert_level === alert)
    .filter((item) => !target || (item.deployment_targets || []).some((value) => String(value).toLowerCase().includes(target)));
}

function filterSessions(items) {
  const repository = document.querySelector("#filterActivityRepository").value.trim().toLowerCase();
  const agent = document.querySelector("#filterActivityAgent").value.trim().toLowerCase();
  const policy = document.querySelector("#filterActivityPolicy").value.trim().toLowerCase();
  return items
    .filter((item) => !repository || String(item.repository || "").toLowerCase().includes(repository))
    .filter((item) => !agent || String(item.agent_id || "").toLowerCase().includes(agent))
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy));
}

function filterDecisions(items) {
  const repository = document.querySelector("#filterActivityRepository").value.trim().toLowerCase();
  const agent = document.querySelector("#filterActivityAgent").value.trim().toLowerCase();
  const policy = document.querySelector("#filterActivityPolicy").value.trim().toLowerCase();
  const decision = document.querySelector("#filterDecisionState").value;
  const severity = document.querySelector("#filterDecisionSeverity").value;
  return items
    .filter((item) => !repository || String(item.repository || "").toLowerCase().includes(repository))
    .filter((item) => !agent || String(item.agent_id || "").toLowerCase().includes(agent))
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy))
    .filter((item) => !decision || item.decision === decision)
    .filter((item) => !severity || item.severity === severity);
}

function filterRepositories(items) {
  const owner = document.querySelector("#filterRepositoryOwner").value.trim().toLowerCase();
  const policy = document.querySelector("#filterRepositoryPolicy").value.trim().toLowerCase();
  const risk = document.querySelector("#filterRepositoryRisk").value;
  return items
    .filter((item) => !owner || String(item.owner || "").toLowerCase().includes(owner))
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy))
    .filter((item) => !risk || item.risk_tier === risk);
}

function filterPolicyRollouts(items) {
  const policy = document.querySelector("#filterRepositoryPolicy").value.trim().toLowerCase();
  const state = document.querySelector("#filterRolloutState").value;
  const mode = document.querySelector("#filterRolloutMode").value;
  return items
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy))
    .filter((item) => !state || item.state === state)
    .filter((item) => !mode || item.mode === mode);
}

function filterIntegrations(items) {
  const category = document.querySelector("#filterIntegrationCategory").value;
  const status = document.querySelector("#filterIntegrationStatus").value;
  const health = document.querySelector("#filterIntegrationHealth").value;
  const owner = document.querySelector("#filterIntegrationOwner").value.trim().toLowerCase();
  return items
    .filter((item) => !category || item.category === category)
    .filter((item) => !status || item.status === status)
    .filter((item) => !health || item.health_status === health)
    .filter((item) => !owner || String(item.owner || "").toLowerCase().includes(owner));
}

function filterApprovals(items) {
  const state = document.querySelector("#filterApprovalState").value;
  const group = document.querySelector("#filterApprovalGroup").value.trim().toLowerCase();
  return items
    .filter((item) => !state || item.state === state)
    .filter((item) => !group || String(item.approver_group || "").toLowerCase().includes(group));
}

function filterAgents(items) {
  const status = document.querySelector("#filterAgentStatus").value;
  const owner = document.querySelector("#filterAgentOwner").value.trim().toLowerCase();
  return items
    .filter((item) => !status || item.status === status)
    .filter((item) => !owner || String(item.owner || "").toLowerCase().includes(owner));
}

function filterMcpServers(items) {
  const trust = document.querySelector("#filterMcpTrust").value;
  const capability = document.querySelector("#filterMcpCapability").value;
  return items
    .filter((item) => !trust || item.trust_tier === trust)
    .filter((item) => !capability || (item.capabilities || []).includes(capability));
}

function renderEvidenceRows(items) {
  const rows = document.querySelector("#evidenceRows");
  const sessionSelect = document.querySelector("#attestationSession");
  rows.innerHTML = "";
  sessionSelect.innerHTML = "";
  for (const item of items) {
    const kind = evidenceKindLabel(item);
    const rollout = item.metadata_kind === "managed-endpoint-rollout" || item.metadata_kind === "rollout-promotion-execution" || item.metadata_kind === "rollout-rollback-execution"
      ? `${item.environment || "environment"} / ${item.rollout_status || item.promotion_execution_status || item.rollback_execution_status || "unknown"}`
      : "n/a";
    const readiness = evidenceReadiness(item);
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.session_id || "unknown")}</td>
        <td>${escapeHtml(kind)}</td>
        <td>${escapeHtml(item.signer || "local")}</td>
        <td>${escapeHtml(rollout)}</td>
        <td>${item.decision_count || 0}</td>
        <td class="${Number(item.blocked_count || 0) > 0 ? "block" : "allow"}">${item.blocked_count || 0}</td>
        <td class="${Number(item.approval_required_count || 0) > 0 ? "require_approval" : "allow"}">${item.approval_required_count || 0}</td>
        <td>${item.retention?.retention_days || "n/a"} days</td>
        <td class="${escapeHtml(readiness.className)}">${escapeHtml(readiness.label)}</td>
        <td><button class="evidenceArtifactAction secondary" data-session="${escapeHtml(item.session_id || "")}">${item.metadata_kind === "rollout-promotion-execution" || item.metadata_kind === "rollout-rollback-execution" ? "Audit" : "Artifacts"}</button></td>
      </tr>
    `);
    sessionSelect.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(item.session_id)}">${escapeHtml(item.session_id)}</option>`);
  }
}

function evidenceKindLabel(item) {
  if (item.metadata_kind === "managed-endpoint-rollout") return "Endpoint rollout";
  if (item.metadata_kind === "rollout-promotion-execution") return "Promotion execution";
  if (item.metadata_kind === "rollout-rollback-execution") return "Rollback execution";
  return "Session";
}

function renderEvidenceArtifacts(payload) {
  const panel = document.querySelector("#evidenceArtifacts");
  const artifacts = Array.isArray(payload.artifacts) ? payload.artifacts : [];
  const bundleHref = payload.bundle_download_url ? apiUrl(payload.bundle_download_url) : "";
  const readiness = payload.promotion_readiness || {};
  const integrity = payload.rollout_artifact_integrity || {};
  const isRollout = payload.metadata_kind === "managed-endpoint-rollout";
  panel.innerHTML = `
    <dl>
      <dt>Session</dt><dd>${escapeHtml(payload.session_id || "unknown")}</dd>
      <dt>Artifact root</dt><dd class="${payload.artifact_root_configured ? "allow" : "require_approval"}">${payload.artifact_root_configured ? "configured" : "sample or disabled"}</dd>
      <dt>Artifacts</dt><dd>${Number(payload.artifact_count || artifacts.length || 0)}</dd>
      <dt>Bundle</dt><dd>${bundleHref ? `<a href="${escapeHtml(bundleHref)}">Download bundle</a>` : "not available from sample data"}</dd>
      ${isRollout ? `
        <dt>Integrity</dt><dd class="${escapeHtml(statusClass(integrity.status))}">${escapeHtml(integrity.status || "unknown")}</dd>
        <dt>Readiness</dt><dd class="${escapeHtml(statusClass(readiness.status))}">${escapeHtml(readiness.status || "review")}</dd>
        <dt>Rationale</dt><dd>${escapeHtml(readiness.rationale || "Review rollout artifact integrity before promotion.")}</dd>
      ` : ""}
    </dl>
    ${isRollout ? `
      <h3>Rollout Controls</h3>
      <ul>
        <li>Verified: ${escapeHtml(formatList(integrity.verified_artifacts))}</li>
        <li>Missing: ${escapeHtml(formatList(integrity.missing_artifacts))}</li>
        <li>Unchecked: ${escapeHtml(formatList(integrity.unchecked_artifacts))}</li>
        <li>Mismatched: ${escapeHtml(formatList(integrity.checksum_mismatches))}</li>
      </ul>
      <div class="artifact-actions">
        <button class="rolloutPromotionRequestAction" data-session="${escapeHtml(payload.session_id || "")}">Request Promotion Approval</button>
        <button class="rolloutPromotionExecutionAction" data-session="${escapeHtml(payload.session_id || "")}">Record Promotion Execution</button>
        <span id="rolloutPromotionStatus" class="status-line"></span>
      </div>
    ` : ""}
    <h3>Bundle Files</h3>
    <ul>${artifacts.map((item) => {
      const href = item.download_url ? apiUrl(item.download_url) : "";
      const label = `${item.artifact} (${item.kind || item.media_type || "artifact"})`;
      const suffix = item.bytes ? ` - ${Number(item.bytes)} bytes` : "";
      return `<li>${href ? `<a href="${escapeHtml(href)}">${escapeHtml(label)}</a>` : escapeHtml(label)}${escapeHtml(suffix)}<br><small>${escapeHtml(item.description || "")}</small></li>`;
    }).join("") || "<li>n/a</li>"}</ul>
  `;
}

function evidenceReadiness(item) {
  if (item.metadata_kind !== "managed-endpoint-rollout") {
    return { label: "n/a", className: "" };
  }
  const status = item.promotion_readiness?.status || (
    ["failed", "rolled_back"].includes(item.rollout_status) ? "blocked" : item.rollout_status === "planned" ? "review" : "review"
  );
  return { label: status, className: statusClass(status) };
}

function statusClass(status) {
  if (["ready", "verified", "succeeded"].includes(status)) return "allow";
  if (["blocked", "failed"].includes(status)) return "block";
  return "require_approval";
}

function formatList(items) {
  return Array.isArray(items) && items.length ? items.join(", ") : "none";
}

function renderReleaseNotes() {
  const panel = document.querySelector("#releaseNotes");
  if (!panel) return;
  panel.innerHTML = releaseNoteCatalog.map((item) => `
    <article class="release-note">
      <div>
        <strong>${escapeHtml(item.title)}</strong>
        <span>${escapeHtml(item.date)}</span>
      </div>
      <p>${escapeHtml(item.summary)}</p>
      <div class="release-note-links">
        ${item.links.map(([label, href]) => `<a href="${escapeHtml(href)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`).join("")}
      </div>
    </article>
  `).join("");
}

function renderDemoMetrics(metrics) {
  const panel = document.querySelector("#demoMetrics");
  if (!panel) return;
  const items = [
    ["Runs", metrics.total_runs],
    ["Decisions", metrics.total_decisions],
    ["Blocked", metrics.blocked_actions],
    ["Approvals", metrics.approval_required_actions]
  ];
  const sourceLabel = metrics.source === "activity_store" ? "Persisted backend metadata" : "Local sample mode";
  panel.innerHTML = `
    <div class="metric-source">
      <strong>${escapeHtml(sourceLabel)}</strong>
      <span>${escapeHtml(metrics.telemetry === "disabled" ? "Telemetry-free" : "Telemetry status unknown")}</span>
    </div>
    ${items.map(([label, value]) => `
      <div class="metric-card">
        <span>${escapeHtml(label)}</span>
        <strong>${formatMetricNumber(value)}</strong>
      </div>
    `).join("")}
    <div class="metric-card metric-wide">
      <span>Latest</span>
      <strong>${escapeHtml(formatMetricDate(metrics.latest_run_at))}</strong>
    </div>
  `;
}

function renderReleaseConnectorDeliveries(items, dashboard) {
  const rows = document.querySelector("#releaseDeliveryRows");
  const panel = document.querySelector("#releaseDeliveryDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  const alerts = Array.isArray(dashboard.alerts) ? dashboard.alerts : [];
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Deliveries</span>
      <strong>${formatMetricNumber(dashboard.total_deliveries)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Failed</span>
      <strong class="${Number(dashboard.failed_deliveries || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.failed_deliveries)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Success Rate</span>
      <strong>${Math.round(Number(dashboard.success_rate || 0) * 100)}%</strong>
    </div>
    <div class="release-delivery-alerts">
      <strong>Alerts</strong>
      <ul>${alerts.map((item) => `<li><span class="${riskClass(item.severity)}">${escapeHtml(item.severity)}</span> ${escapeHtml(item.message || item.event_id || "delivery alert")}</li>`).join("") || "<li class=\"allow\">No active release connector delivery alerts.</li>"}</ul>
    </div>
  `;
  for (const item of items) {
    const providerText = formatList(item.providers);
    const status = item.delivery_success ? "success" : "failed";
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.session_id || "delivery")}</td>
        <td>${escapeHtml(item.event_id || "unknown")}</td>
        <td>${escapeHtml(item.event_type || "cavra.connector.event")}</td>
        <td>${escapeHtml(providerText)}</td>
        <td class="${item.delivery_success ? "allow" : "block"}">${escapeHtml(status)}</td>
        <td>${Number(item.attempt_count || 0)}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointPublicationDeliveries(items, dashboard) {
  const rows = document.querySelector("#endpointPublicationRows");
  const panel = document.querySelector("#endpointPublicationDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  const alerts = Array.isArray(dashboard.alerts) ? dashboard.alerts : [];
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Publications</span>
      <strong>${formatMetricNumber(dashboard.total_publications)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Failed</span>
      <strong class="${Number(dashboard.failed_publications || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.failed_publications)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Success Rate</span>
      <strong>${Math.round(Number(dashboard.success_rate || 0) * 100)}%</strong>
    </div>
    <div class="release-delivery-alerts">
      <strong>Alerts</strong>
      <ul>${alerts.map((item) => `<li><span class="${riskClass(item.severity)}">${escapeHtml(item.severity)}</span> ${escapeHtml(item.message || item.export_id || "publication alert")}</li>`).join("") || "<li class=\"allow\">No active endpoint publication alerts.</li>"}</ul>
    </div>
  `;
  for (const item of items) {
    const status = item.delivery_success ? "success" : "failed";
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.publication_id || item.event_id || item.session_id || "publication")}</td>
        <td>${escapeHtml(item.export_id || "unknown")}</td>
        <td>${escapeHtml(item.channel || "unknown")}</td>
        <td>${escapeHtml(formatList(item.providers))}</td>
        <td class="${item.delivery_success ? "allow" : "block"}">${escapeHtml(status)}</td>
        <td>${Number(item.attempt_count || 0)}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointInventoryIngestions(items, dashboard) {
  const rows = document.querySelector("#endpointInventoryRows");
  const panel = document.querySelector("#endpointInventoryDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Ingestions</span>
      <strong>${formatMetricNumber(dashboard.total_ingestions)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Endpoints</span>
      <strong>${formatMetricNumber(dashboard.endpoint_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Missing Targets</span>
      <strong class="${Number(dashboard.missing_target_count || 0) ? "warn" : "allow"}">${formatMetricNumber(dashboard.missing_target_count)}</strong>
    </div>
  `;
  for (const item of items) {
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.inventory_id || item.session_id || "inventory")}</td>
        <td>${escapeHtml(item.provider || "unknown")}</td>
        <td>${escapeHtml(item.channel || "unknown")}</td>
        <td>${Number(item.endpoint_count || 0)}</td>
        <td>${escapeHtml(formatList(item.deployment_targets))}</td>
        <td class="${Number(item.missing_target_count || 0) ? "warn" : "allow"}">${Number(item.missing_target_count || 0)}</td>
        <td>${escapeHtml(String(item.observed_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointInventoryFreshness(items, dashboard) {
  const rows = document.querySelector("#endpointInventoryFreshnessRows");
  const panel = document.querySelector("#endpointInventoryFreshnessDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  const alerts = Array.isArray(dashboard.alerts) ? dashboard.alerts : [];
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Reports</span>
      <strong>${formatMetricNumber(dashboard.report_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Warnings</span>
      <strong class="${Number(dashboard.warning_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.warning_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Critical</span>
      <strong class="${Number(dashboard.critical_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.critical_count)}</strong>
    </div>
    <div class="release-delivery-alerts">
      <strong>Freshness Alerts</strong>
      <ul>${alerts.map((item) => `<li><span class="${riskClass(item.severity)}">${escapeHtml(item.severity)}</span> ${escapeHtml(item.message || "inventory freshness alert")}</li>`).join("") || "<li class=\"allow\">No endpoint inventory freshness alerts.</li>"}</ul>
    </div>
  `;
  for (const item of items) {
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.report_id || item.session_id || "freshness-report")}</td>
        <td class="${riskClass(item.alert_level)}">${escapeHtml(item.alert_level || "unknown")}</td>
        <td>${Number(item.warning_count || 0)}</td>
        <td>${Number(item.critical_count || 0)}</td>
        <td>${Number(item.alert_count || (item.alerts || []).length || 0)}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointReconciliations(items, dashboard) {
  const rows = document.querySelector("#endpointReconciliationRows");
  const panel = document.querySelector("#endpointReconciliationDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  const alerts = Array.isArray(dashboard.alerts) ? dashboard.alerts : [];
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Reports</span>
      <strong>${formatMetricNumber(dashboard.total_reconciliations)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Drifted</span>
      <strong class="${Number(dashboard.drifted_endpoint_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.drifted_endpoint_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Missing</span>
      <strong class="${Number(dashboard.missing_target_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.missing_target_count)}</strong>
    </div>
    <div class="release-delivery-alerts">
      <strong>Alerts</strong>
      <ul>${alerts.map((item) => `<li><span class="${riskClass(item.severity)}">${escapeHtml(item.severity)}</span> ${escapeHtml(item.message || item.reconciliation_id || "drift alert")}</li>`).join("") || "<li class=\"allow\">No active endpoint drift alerts.</li>"}</ul>
    </div>
  `;
  for (const item of items) {
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.reconciliation_id || item.session_id || "reconciliation")}</td>
        <td class="${item.drift_status === "aligned" ? "allow" : "block"}">${escapeHtml(item.drift_status || "unknown")}</td>
        <td class="${riskClass(item.alert_level)}">${escapeHtml(item.alert_level || "unknown")}</td>
        <td>${Number(item.observed_endpoint_count || 0)}</td>
        <td>${Number(item.compliant_endpoint_count || 0)}</td>
        <td>${Number(item.drifted_endpoint_count || 0)}</td>
        <td>${Number(item.missing_target_count || 0)}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointRemediations(items, dashboard) {
  const rows = document.querySelector("#endpointRemediationRows");
  const panel = document.querySelector("#endpointRemediationDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Requests</span>
      <strong>${formatMetricNumber(dashboard.request_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Executions</span>
      <strong>${formatMetricNumber(dashboard.execution_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Pending</span>
      <strong class="${Number(dashboard.pending_approval_count || 0) ? "warn" : "allow"}">${formatMetricNumber(dashboard.pending_approval_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Actions</span>
      <strong>${formatMetricNumber(dashboard.planned_action_count)}</strong>
    </div>
  `;
  for (const item of items) {
    const id = item.request_id || item.execution_id || item.session_id || "remediation";
    const state = item.execution_status || item.approval_state || "unknown";
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(id)}</td>
        <td>${escapeHtml(item.reconciliation_id || "unknown")}</td>
        <td>${escapeHtml(item.metadata_kind === "endpoint-drift-remediation-execution" ? "execution" : "request")}</td>
        <td>${escapeHtml(item.strategy || "mixed")}</td>
        <td>${Number(item.action_count || 0)}</td>
        <td class="${state === "approved" || state === "recorded" ? "allow" : "warn"}">${escapeHtml(state)}</td>
        <td>${escapeHtml(item.approval_id || "unknown")}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointRemediationHandoffs(items, dashboard) {
  const rows = document.querySelector("#endpointRemediationHandoffRows");
  const panel = document.querySelector("#endpointRemediationHandoffDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Handoffs</span>
      <strong>${formatMetricNumber(dashboard.handoff_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Providers</span>
      <strong>${formatMetricNumber(dashboard.provider_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Pending</span>
      <strong class="${Number(dashboard.pending_approval_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.pending_approval_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Actions</span>
      <strong>${formatMetricNumber(dashboard.action_count)}</strong>
    </div>
  `;
  for (const item of items) {
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.handoff_id || item.session_id || "handoff")}</td>
        <td>${escapeHtml(item.request_id || "unknown")}</td>
        <td>${escapeHtml(formatList(item.providers))}</td>
        <td>${Number(item.action_count || 0)}</td>
        <td class="${item.approval_state === "approved" ? "allow" : "require_approval"}">${escapeHtml(item.approval_state || "unknown")}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointRemediationHandoffStatuses(items, dashboard) {
  const rows = document.querySelector("#endpointRemediationHandoffStatusRows");
  const panel = document.querySelector("#endpointRemediationHandoffStatusDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Events</span>
      <strong>${formatMetricNumber(dashboard.status_event_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Tracked</span>
      <strong>${formatMetricNumber(dashboard.tracked_handoff_provider_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Completed</span>
      <strong class="allow">${formatMetricNumber(dashboard.completed_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Blocked</span>
      <strong class="${Number(dashboard.blocked_count || 0) || Number(dashboard.failed_count || 0) ? "block" : "allow"}">${formatMetricNumber(Number(dashboard.blocked_count || 0) + Number(dashboard.failed_count || 0))}</strong>
    </div>
  `;
  for (const item of items) {
    const state = item.handoff_status || "unknown";
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.status_id || item.session_id || "status")}</td>
        <td>${escapeHtml(item.handoff_id || "unknown")}</td>
        <td>${escapeHtml(item.provider || "unknown")}</td>
        <td class="${state === "completed" ? "allow" : state === "blocked" || state === "failed" ? "block" : "warn"}">${escapeHtml(state)}</td>
        <td>${escapeHtml(item.external_ref || "n/a")}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function renderEndpointRemediationSlaReports(items, dashboard, notificationDashboard = {}, escalationDashboard = {}, escalationActionDashboard = {}, escalationRecurrenceDashboard = {}) {
  const rows = document.querySelector("#endpointRemediationSlaRows");
  const panel = document.querySelector("#endpointRemediationSlaDashboard");
  if (!rows || !panel) return;
  rows.innerHTML = "";
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Reports</span>
      <strong>${formatMetricNumber(dashboard.report_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Tracked</span>
      <strong>${formatMetricNumber(dashboard.tracked_work_item_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>At Risk</span>
      <strong class="${Number(dashboard.at_risk_count || 0) ? "warn" : "allow"}">${formatMetricNumber(dashboard.at_risk_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Breached</span>
      <strong class="${Number(dashboard.breached_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.breached_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Notifications</span>
      <strong>${formatMetricNumber(notificationDashboard.delivery_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Outstanding Ack</span>
      <strong class="${Number(notificationDashboard.outstanding_acknowledgement_count || 0) ? "block" : "allow"}">${formatMetricNumber(notificationDashboard.outstanding_acknowledgement_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Suppressed</span>
      <strong class="${Number(notificationDashboard.suppressed_provider_count || 0) ? "warn" : "allow"}">${formatMetricNumber(notificationDashboard.suppressed_provider_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Active Escalations</span>
      <strong class="${Number(escalationDashboard.active_escalation_count || 0) ? "block" : "allow"}">${formatMetricNumber(escalationDashboard.active_escalation_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>SLO Owners</span>
      <strong>${formatMetricNumber(escalationDashboard.owner_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Esc Deliveries</span>
      <strong class="${Number(escalationActionDashboard.failed_delivery_count || 0) ? "block" : "allow"}">${formatMetricNumber(escalationActionDashboard.delivery_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Owner Reviews</span>
      <strong class="${Number(escalationActionDashboard.unresolved_review_count || 0) ? "warn" : "allow"}">${formatMetricNumber(escalationActionDashboard.owner_review_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Recurrence Ready</span>
      <strong class="${Number(escalationRecurrenceDashboard.deliverable_route_count || 0) ? "block" : "allow"}">${formatMetricNumber(escalationRecurrenceDashboard.deliverable_route_count)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Suppressed Routes</span>
      <strong class="${Number(escalationRecurrenceDashboard.suppressed_route_count || 0) ? "warn" : "allow"}">${formatMetricNumber(escalationRecurrenceDashboard.suppressed_route_count)}</strong>
    </div>
  `;
  for (const item of items) {
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.report_id || item.session_id || "report")}</td>
        <td class="${riskClass(item.alert_level)}">${escapeHtml(item.alert_level || "unknown")}</td>
        <td>${formatMetricNumber(item.tracked_work_item_count)}</td>
        <td>${formatMetricNumber(item.completed_count)}</td>
        <td>${formatMetricNumber(item.at_risk_count)}</td>
        <td>${formatMetricNumber(item.breached_count)}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
}

function topEndpointRecurrenceTrendCategory(trends) {
  const counts = {};
  for (const item of trends) {
    const trend = endpointRecurrenceSuppressionTrendPayload(item);
    for (const [category, count] of Object.entries(trend.category_counts || {})) {
      counts[category] = Number(counts[category] || 0) + Number(count || 0);
    }
  }
  const [category] = Object.entries(counts).sort((left, right) => Number(right[1]) - Number(left[1]))[0] || [];
  return category || "none";
}

function endpointRecurrencePayloadId(kind, index) {
  return `${kind}:${index}`;
}

function endpointRecurrenceActionButtons(payloadId) {
  return `
    <div class="row-actions">
      <button class="endpointRecurrenceDetailAction secondary" data-payload="${escapeHtml(payloadId)}">Details</button>
      <button class="endpointRecurrenceExportAction secondary" data-payload="${escapeHtml(payloadId)}">Export</button>
    </div>
  `;
}

function renderEndpointRecurrenceOperations(
  retryPlans,
  ownerDigests,
  suppressionTrends,
  automationRuns,
  dashboard = {},
  automationDashboard = {},
  automationHealth = {},
  healthAlerts = [],
  healthAlertDashboard = {}
) {
  const panel = document.querySelector("#endpointRecurrenceOperationsDashboard");
  const retryRows = document.querySelector("#endpointRecurrenceRetryRows");
  const digestRows = document.querySelector("#endpointRecurrenceDigestRows");
  const trendRows = document.querySelector("#endpointRecurrenceTrendRows");
  const automationRows = document.querySelector("#endpointRecurrenceAutomationRows");
  const healthAlertRows = document.querySelector("#endpointRecurrenceHealthAlertRows");
  if (!panel || !retryRows || !digestRows || !trendRows || !automationRows || !healthAlertRows) return;

  endpointRecurrenceDetailPayloads.clear();
  retryRows.innerHTML = "";
  digestRows.innerHTML = "";
  trendRows.innerHTML = "";
  automationRows.innerHTML = "";
  healthAlertRows.innerHTML = "";

  const retryableCount = retryPlans.reduce((total, item) => total + Number(endpointRecurrenceRetryPlanPayload(item).retryable_count || item.retryable_count || 0), 0);
  const waitingCount = retryPlans.reduce((total, item) => total + Number(endpointRecurrenceRetryPlanPayload(item).waiting_count || item.waiting_count || 0), 0);
  const suppressedCount = retryPlans.reduce((total, item) => total + Number(endpointRecurrenceRetryPlanPayload(item).suppressed_count || item.suppressed_count || 0), 0);
  const unresolvedCount = ownerDigests.reduce((total, item) => {
    const digest = endpointRecurrenceOwnerDigestPayload(item);
    return total + Number(digest.summary?.unresolved_route_count || item.unresolved_route_count || 0);
  }, 0);
  const ownerCount = ownerDigests.reduce((owners, item) => {
    for (const row of endpointRecurrenceOwnerRows(item)) {
      if (row.owner) owners.add(row.owner);
    }
    return owners;
  }, new Set()).size;
  const trendEventCount = suppressionTrends.reduce((total, item) => total + Number(endpointRecurrenceSuppressionTrendPayload(item).suppression_event_count || item.suppression_event_count || 0), 0);
  const automationDryRunCount = automationRuns.filter((item) => endpointRecurrenceAutomationPayload(item).dry_run !== false && item.dry_run !== false).length;
  const automationExecutedCount = automationRuns.length - automationDryRunCount;
  const automationRetryableCount = automationRuns.reduce((total, item) => {
    const run = endpointRecurrenceAutomationPayload(item);
    return total + Number(run.summary?.retryable_count || item.retryable_count || 0);
  }, 0);
  const automationDigestCount = automationRuns.reduce((total, item) => {
    const run = endpointRecurrenceAutomationPayload(item);
    return total + Number(run.summary?.owner_digest_count || item.owner_digest_count || 0);
  }, 0);
  const automationTrendEventCount = automationRuns.reduce((total, item) => {
    const run = endpointRecurrenceAutomationPayload(item);
    return total + Number(run.summary?.suppression_event_count || item.suppression_event_count || 0);
  }, 0);
  const status = automationHealth.alert_level || automationDashboard.alert_level || dashboard.alert_level || (retryableCount || trendEventCount || automationRetryableCount ? "warning" : "healthy");

  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(status)}">${escapeHtml(status)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Retry Plans</span>
      <strong>${formatMetricNumber(dashboard.recurrence_retry_plan_count || retryPlans.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Retryable</span>
      <strong class="${retryableCount ? "block" : "allow"}">${formatMetricNumber(retryableCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Waiting</span>
      <strong class="${waitingCount ? "require_approval" : "allow"}">${formatMetricNumber(waitingCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Suppressed</span>
      <strong class="${suppressedCount ? "require_approval" : "allow"}">${formatMetricNumber(suppressedCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Owner Digests</span>
      <strong>${formatMetricNumber(dashboard.owner_digest_count || ownerDigests.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Owners</span>
      <strong>${formatMetricNumber(ownerCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Unresolved</span>
      <strong class="${unresolvedCount ? "block" : "allow"}">${formatMetricNumber(unresolvedCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Trend Reports</span>
      <strong>${formatMetricNumber(dashboard.suppression_trend_count || suppressionTrends.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Trend Events</span>
      <strong class="${trendEventCount ? "require_approval" : "allow"}">${formatMetricNumber(trendEventCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Top Category</span>
      <strong>${escapeHtml(topEndpointRecurrenceTrendCategory(suppressionTrends))}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Failed Deliveries</span>
      <strong class="${Number(dashboard.failed_delivery_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.failed_delivery_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Worker Runs</span>
      <strong>${formatMetricNumber(automationDashboard.run_count || automationRuns.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Dry Runs</span>
      <strong>${formatMetricNumber(automationDashboard.dry_run_count ?? automationDryRunCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Executed Runs</span>
      <strong class="${automationExecutedCount ? "require_approval" : "allow"}">${formatMetricNumber(automationDashboard.executed_count ?? automationExecutedCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Worker Retryable</span>
      <strong class="${automationRetryableCount ? "block" : "allow"}">${formatMetricNumber(automationDashboard.retryable_count ?? automationRetryableCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Worker Digests</span>
      <strong>${formatMetricNumber(automationDashboard.owner_digest_count ?? automationDigestCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Worker Trend Events</span>
      <strong class="${automationTrendEventCount ? "require_approval" : "allow"}">${formatMetricNumber(automationDashboard.suppression_event_count ?? automationTrendEventCount)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Health</span>
      <strong class="${riskClass(automationHealth.alert_level)}">${escapeHtml(automationHealth.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Missed Runs</span>
      <strong class="${Number(automationHealth.missed_run_count || 0) ? "block" : "allow"}">${formatMetricNumber(automationHealth.missed_run_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Failed Jobs</span>
      <strong class="${Number(automationHealth.failed_job_count || 0) ? "block" : "allow"}">${formatMetricNumber(automationHealth.failed_job_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Stale Metadata</span>
      <strong class="${Number(automationHealth.stale_metadata_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(automationHealth.stale_metadata_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Connector Failures</span>
      <strong class="${Number(automationHealth.connector_delivery_failure_count || 0) ? "block" : "allow"}">${formatMetricNumber(automationHealth.connector_delivery_failure_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Latest Age</span>
      <strong>${automationHealth.latest_run_age_minutes === null || automationHealth.latest_run_age_minutes === undefined ? "none" : `${formatMetricNumber(automationHealth.latest_run_age_minutes)}m`}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Alert Plans</span>
      <strong>${formatMetricNumber(healthAlertDashboard.plan_count || healthAlerts.filter((item) => item.metadata_kind === "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Alert Deliveries</span>
      <strong class="${Number(healthAlertDashboard.failed_delivery_count || 0) ? "block" : "allow"}">${formatMetricNumber(healthAlertDashboard.delivery_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Alert Acks</span>
      <strong>${formatMetricNumber(healthAlertDashboard.acknowledgement_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Outstanding Acks</span>
      <strong class="${Number(healthAlertDashboard.outstanding_acknowledgement_count || 0) ? "block" : "allow"}">${formatMetricNumber(healthAlertDashboard.outstanding_acknowledgement_count || 0)}</strong>
    </div>
  `;

  retryPlans.forEach((item, index) => {
    const plan = endpointRecurrenceRetryPlanPayload(item);
    const payloadId = endpointRecurrencePayloadId("retry", index);
    endpointRecurrenceDetailPayloads.set(payloadId, { label: plan.retry_plan_id || item.retry_plan_id || "retry-plan", payload: plan });
    retryRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(plan.retry_plan_id || item.retry_plan_id || item.session_id || "retry-plan")}</td>
        <td class="${riskClass(plan.alert_level || item.alert_level)}">${escapeHtml(plan.alert_level || item.alert_level || "unknown")}</td>
        <td>${formatMetricNumber(plan.retryable_count || item.retryable_count)}</td>
        <td>${formatMetricNumber(plan.waiting_count || item.waiting_count)}</td>
        <td>${formatMetricNumber(plan.suppressed_count || item.suppressed_count)}</td>
        <td>${escapeHtml(String(plan.generated_at || item.created_at || "").slice(0, 19))}</td>
        <td>${endpointRecurrenceActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!retryPlans.length) retryRows.insertAdjacentHTML("beforeend", `<tr><td colspan="7">No retry plans match the current filters.</td></tr>`);

  ownerDigests.forEach((item, index) => {
    const digest = endpointRecurrenceOwnerDigestPayload(item);
    const summary = digest.summary || {};
    const payloadId = endpointRecurrencePayloadId("digest", index);
    endpointRecurrenceDetailPayloads.set(payloadId, { label: digest.digest_id || item.digest_id || "owner-digest", payload: digest });
    digestRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(digest.digest_id || item.digest_id || item.session_id || "owner-digest")}</td>
        <td>${formatMetricNumber(summary.owner_count || item.owner_count)}</td>
        <td class="${Number(summary.unresolved_route_count || item.unresolved_route_count || 0) ? "block" : "allow"}">${formatMetricNumber(summary.unresolved_route_count || item.unresolved_route_count)}</td>
        <td>${formatMetricNumber(summary.retryable_count || item.retryable_count)}</td>
        <td>${escapeHtml(String(digest.generated_at || item.created_at || "").slice(0, 19))}</td>
        <td>${endpointRecurrenceActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!ownerDigests.length) digestRows.insertAdjacentHTML("beforeend", `<tr><td colspan="6">No owner digests match the current filters.</td></tr>`);

  suppressionTrends.forEach((item, index) => {
    const trend = endpointRecurrenceSuppressionTrendPayload(item);
    const payloadId = endpointRecurrencePayloadId("trend", index);
    endpointRecurrenceDetailPayloads.set(payloadId, { label: trend.trend_id || item.trend_id || "suppression-trend", payload: trend });
    const [topCategory] = Object.entries(trend.category_counts || item.category_counts || {}).sort((left, right) => Number(right[1]) - Number(left[1]))[0] || [];
    trendRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(trend.trend_id || item.trend_id || item.session_id || "suppression-trend")}</td>
        <td class="${riskClass(trend.alert_level || item.alert_level)}">${escapeHtml(trend.alert_level || item.alert_level || "unknown")}</td>
        <td>${formatMetricNumber(trend.suppression_event_count || item.suppression_event_count)}</td>
        <td>${escapeHtml(topCategory || "none")}</td>
        <td>${escapeHtml(String(trend.generated_at || item.created_at || "").slice(0, 19))}</td>
        <td>${endpointRecurrenceActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!suppressionTrends.length) trendRows.insertAdjacentHTML("beforeend", `<tr><td colspan="6">No suppression trends match the current filters.</td></tr>`);

  automationRuns.forEach((item, index) => {
    const run = endpointRecurrenceAutomationPayload(item);
    const summary = run.summary || {};
    const payloadId = endpointRecurrencePayloadId("automation", index);
    const isDryRun = run.dry_run !== false && item.dry_run !== false;
    endpointRecurrenceDetailPayloads.set(payloadId, { label: run.run_id || item.run_id || "automation-run", payload: run });
    automationRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(run.run_id || item.run_id || item.session_id || "automation-run")}</td>
        <td class="${isDryRun ? "require_approval" : "allow"}">${isDryRun ? "dry_run" : "executed"}</td>
        <td class="${Number(summary.retryable_count || item.retryable_count || 0) ? "block" : "allow"}">${formatMetricNumber(summary.retryable_count || item.retryable_count)}</td>
        <td>${formatMetricNumber(summary.owner_digest_count || item.owner_digest_count)}</td>
        <td>${formatMetricNumber(summary.suppression_event_count || item.suppression_event_count)}</td>
        <td>${escapeHtml(String(run.generated_at || item.created_at || "").slice(0, 19))}</td>
        <td>${endpointRecurrenceActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!automationRuns.length) automationRows.insertAdjacentHTML("beforeend", `<tr><td colspan="7">No worker runs match the current filters.</td></tr>`);

  healthAlerts.forEach((item, index) => {
    const payload = item.health_alert_plan || item.acknowledgement || item.delivery || item;
    const payloadId = endpointRecurrencePayloadId("health-alert", index);
    const provider = item.provider || (item.providers || item.selected_providers || [])[0] || "n/a";
    const ackState = item.acknowledgement_state || (item.acknowledgement_required_providers || []).join(", ") || "n/a";
    const kind = String(item.metadata_kind || "health-alert").replace("endpoint-remediation-sla-escalation-recurrence-automation-", "");
    endpointRecurrenceDetailPayloads.set(payloadId, { label: item.session_id || item.plan_id || item.health_id || "health-alert", payload });
    healthAlertRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.session_id || item.plan_id || item.health_id || item.event_id || "health-alert")}</td>
        <td>${escapeHtml(kind)}</td>
        <td class="${riskClass(item.alert_level || (item.delivery_success === false ? "critical" : "healthy"))}">${escapeHtml(item.alert_level || (item.delivery_success === false ? "failed" : item.acknowledgement_state || "indexed"))}</td>
        <td>${escapeHtml(provider)}</td>
        <td>${escapeHtml(ackState)}</td>
        <td>${escapeHtml(String(item.created_at || payload.generated_at || "").slice(0, 19))}</td>
        <td>${endpointRecurrenceActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!healthAlerts.length) healthAlertRows.insertAdjacentHTML("beforeend", `<tr><td colspan="7">No health alert delivery or acknowledgement records indexed.</td></tr>`);
}

function showEndpointRecurrenceDetail(payloadId) {
  const panel = document.querySelector("#endpointRecurrenceDetail");
  const entry = endpointRecurrenceDetailPayloads.get(payloadId);
  if (!panel || !entry) return;
  panel.innerHTML = `
    <dl>
      <dt>Artifact</dt><dd>${escapeHtml(entry.label)}</dd>
      <dt>Type</dt><dd>${escapeHtml(payloadId.split(":")[0])}</dd>
    </dl>
    <pre>${escapeHtml(JSON.stringify(entry.payload, null, 2))}</pre>
  `;
}

function exportEndpointRecurrencePayload(payloadId) {
  const entry = endpointRecurrenceDetailPayloads.get(payloadId);
  if (!entry) return;
  const fileName = `${String(entry.label || "cavra-recurrence-artifact").replace(/[^a-zA-Z0-9_.-]+/g, "-")}.json`;
  const blob = new Blob([JSON.stringify(entry.payload, null, 2)], { type: "application/json" });
  const href = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = href;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(href);
}

function goDrillPayloadId(kind, index) {
  return `go-drill-${kind}:${index}`;
}

function goDrillNotificationActionButtons(payloadId) {
  return `
    <div class="row-actions">
      <button class="goDrillNotificationDetailAction secondary" data-payload="${escapeHtml(payloadId)}">Details</button>
      <button class="goDrillNotificationExportAction secondary" data-payload="${escapeHtml(payloadId)}">Export</button>
    </div>
  `;
}

function goDrillNotificationMutationButtons(payloadId, route) {
  if (!route?.schedule_id || !route?.provider || route.action === "suppress") return goDrillNotificationActionButtons(payloadId);
  const state = route.acknowledgement_state || (route.acknowledged ? "acknowledged" : "outstanding");
  return `
    <div class="row-actions">
      <button class="goDrillNotificationDetailAction secondary" data-payload="${escapeHtml(payloadId)}">Details</button>
      <button class="goDrillNotificationExportAction secondary" data-payload="${escapeHtml(payloadId)}">Export</button>
      <button class="goDrillAckAction" data-payload="${escapeHtml(payloadId)}" data-state="acknowledged" ${state === "acknowledged" ? "disabled" : ""}>Ack</button>
      <button class="goDrillAckAction secondary" data-payload="${escapeHtml(payloadId)}" data-state="escalated">Escalate</button>
      <button class="goDrillAckAction secondary" data-payload="${escapeHtml(payloadId)}" data-state="resolved">Resolve</button>
    </div>
  `;
}

function goDrillNotificationKindLabel(kind) {
  return String(kind || "record")
    .replace("go-backend-rollback-drill-notification-", "")
    .replace("release-connector-delivery", "connector-delivery");
}

function topCountLabel(counts) {
  const [label, count] = Object.entries(counts || {}).sort((left, right) => Number(right[1]) - Number(left[1]))[0] || [];
  return label ? `${label} (${count})` : "none";
}

function buildSampleGoDrillRetryRecoveryReport(historyItems) {
  const executionRecords = historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record");
  const recoveryClosures = historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-closure");
  const recoveryPlaybooks = historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook");
  const providers = new Map();
  const ensureProvider = (provider) => {
    const key = provider || "unknown";
    if (!providers.has(key)) {
      providers.set(key, {
        provider: key,
        execution_count: 0,
        execution_delivered_count: 0,
        execution_failed_count: 0,
        execution_skipped_count: 0,
        recovery_playbook_count: 0,
        recovery_closure_count: 0,
        open_recovery_count: 0,
        slo_breached_count: 0,
        latest_closure_at: ""
      });
    }
    return providers.get(key);
  };
  executionRecords.forEach((item) => {
    const payload = goDrillNotificationPayload(item);
    const summary = ensureProvider(payload.provider || item.provider);
    const status = payload.execution_status || item.execution_status || "unknown";
    summary.execution_count += 1;
    if (status === "delivered") summary.execution_delivered_count += 1;
    if (status === "failed") summary.execution_failed_count += 1;
    if (status === "skipped") summary.execution_skipped_count += 1;
  });
  recoveryPlaybooks.forEach((item) => {
    const payload = goDrillNotificationPayload(item);
    (payload.provider_playbooks || []).forEach((playbook) => {
      const summary = ensureProvider(playbook.provider);
      summary.recovery_playbook_count += 1;
    });
  });
  recoveryClosures.forEach((item) => {
    const payload = goDrillNotificationPayload(item);
    const summary = ensureProvider(payload.provider || item.provider);
    summary.recovery_closure_count += 1;
    summary.latest_closure_at = [summary.latest_closure_at, payload.closed_at || item.created_at || ""].sort().pop() || "";
  });
  providers.forEach((summary) => {
    summary.open_recovery_count = Math.max(0, summary.recovery_playbook_count - summary.recovery_closure_count);
  });
  return {
    schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-retry-recovery-report.v1",
    alert_level: executionRecords.some((item) => ["failed", "skipped"].includes(item.execution_status)) ? "critical" : "healthy",
    execution_count: executionRecords.length,
    execution_failed_count: executionRecords.filter((item) => ["failed", "skipped"].includes(item.execution_status)).length,
    recovery_playbook_provider_count: recoveryPlaybooks.length,
    recovery_closed_count: recoveryClosures.filter((item) => ["resolved", "mitigated"].includes(item.closure_state)).length,
    recovery_open_count: Array.from(providers.values()).reduce((total, item) => total + Number(item.open_recovery_count || 0), 0),
    recovery_slo_breached_count: 0,
    provider_summary: Array.from(providers.values()).sort((left, right) => left.provider.localeCompare(right.provider)),
    closure_trends: []
  };
}

function buildSampleGoDrillRecoveryEscalationPlan(historyItems) {
  const report = buildSampleGoDrillRetryRecoveryReport(historyItems);
  const routes = [];
  (report.provider_summary || []).forEach((summary) => {
    const failed = Number(summary.execution_failed_count || 0) + Number(summary.execution_skipped_count || 0);
    if (failed) {
      routes.push({
        provider: summary.provider,
        category: "retry-execution",
        severity: "critical",
        reason: "failed or skipped retry execution",
        recommended_action: "notify release owner and verify connector recovery closure evidence",
        failure_count: failed,
        closure_state: "review_required",
        slo_status: "review_required"
      });
    }
    if (Number(summary.open_recovery_count || 0)) {
      routes.push({
        provider: summary.provider,
        category: "connector-recovery",
        severity: Number(summary.slo_breached_count || 0) ? "critical" : "warning",
        reason: Number(summary.slo_breached_count || 0) ? "recovery SLO breached" : "connector recovery remains open",
        recommended_action: "notify release owner for recovery follow-up",
        failure_count: Number(summary.open_recovery_count || 0),
        closure_state: "open",
        slo_status: Number(summary.slo_breached_count || 0) ? "breached" : "open"
      });
    }
  });
  return {
    schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan.v1",
    product: "CAVRA",
    plan_id: `sample-go-drill-recovery-escalation-${Date.now()}`,
    generated_at: new Date().toISOString(),
    generated_by: goDrillAckActor(),
    alert_level: routes.some((route) => route.severity === "critical") ? "critical" : routes.length ? "warning" : "healthy",
    escalation_count: routes.length,
    critical_escalation_count: routes.filter((route) => route.severity === "critical").length,
    failed_execution_count: Number(report.execution_failed_count || 0),
    open_recovery_count: Number(report.recovery_open_count || 0),
    slo_breached_count: Number(report.recovery_slo_breached_count || 0),
    selected_providers: [...new Set(routes.map((route) => route.provider).filter(Boolean))],
    escalation_routes: routes,
    executive_summary: {
      status: routes.length ? "warning" : "healthy",
      execution_count: Number(report.execution_count || 0),
      failed_execution_count: Number(report.execution_failed_count || 0),
      open_recovery_count: Number(report.recovery_open_count || 0),
      slo_breached_count: Number(report.recovery_slo_breached_count || 0)
    }
  };
}

function renderGoRollbackDrillNotifications(historyItems, dashboard = {}, routingRows = [], suppressionTrend = {}, retryRecoveryReport = {}) {
  const panel = document.querySelector("#goRollbackDrillNotificationDashboard");
  const historyRows = document.querySelector("#goDrillNotificationRows");
  const escalationRows = document.querySelector("#goDrillEscalationRows");
  const routeRows = document.querySelector("#goDrillRouteRows");
  const suppressionRows = document.querySelector("#goDrillSuppressionTrendRows");
  const retryRecoveryRows = document.querySelector("#goDrillRetryRecoveryRows");
  if (!panel || !historyRows || !escalationRows || !routeRows || !suppressionRows || !retryRecoveryRows) return;

  goDrillNotificationDetailPayloads.clear();
  historyRows.innerHTML = "";
  escalationRows.innerHTML = "";
  routeRows.innerHTML = "";
  suppressionRows.innerHTML = "";
  retryRecoveryRows.innerHTML = "";
  const routes = goDrillEscalationRoutes(historyItems, dashboard);
  currentGoDrillEscalationRoutes = routes;
  const breachedRoutes = routes.filter((route) => route.breached);
  const outstandingRoutes = routes.filter((route) => route.acknowledged === false || route.acknowledgement_state === "outstanding");
  const suppressedRoutes = routingRows.filter((route) => route.action === "suppress");
  const status = dashboard.alert_level || (breachedRoutes.length ? "critical" : outstandingRoutes.length ? "warning" : "healthy");

  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(status)}">${escapeHtml(status)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Plans</span>
      <strong>${formatMetricNumber(dashboard.plan_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-notification-plan").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Deliveries</span>
      <strong>${formatMetricNumber(dashboard.delivery_count || historyItems.filter((item) => item.metadata_kind === "release-connector-delivery").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Delivery Health</span>
      <strong class="${dashboard.acknowledgement_audit_delivery_health === "critical" ? "block" : "allow"}">${escapeHtml(dashboard.acknowledgement_audit_delivery_health || "healthy")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Plans</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_plan_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-plan").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Sends</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_count || historyItems.filter((item) => item.connector_delivery_source === "go_backend_rollback_drill_acknowledgement_audit").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Failed</span>
      <strong class="${Number(dashboard.failed_acknowledgement_audit_delivery_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.failed_acknowledgement_audit_delivery_count || historyItems.filter((item) => item.connector_delivery_source === "go_backend_rollback_drill_acknowledgement_audit" && item.delivery_success === false).length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Success</span>
      <strong>${dashboard.acknowledgement_audit_delivery_success_rate == null ? "n/a" : `${Math.round(Number(dashboard.acknowledgement_audit_delivery_success_rate) * 100)}%`}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Retry Plans</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_retry_plan_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Retryable</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_retryable_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_retryable_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Audit Workers</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_worker_run_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Worker Dry Runs</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_worker_dry_run_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Worker Alerts</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_worker_health_alert_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_worker_health_alert_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Retry Acks</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_retry_ack_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-ack").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Retry Approvals</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_retry_execution_approval_decision_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Approved Retries</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_retry_execution_approved_count || 0) ? "allow" : "require_approval"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_retry_execution_approved_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision" && item.approval_state === "approved").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Retry Executions</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_retry_execution_record_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Execution Failed</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_retry_execution_failed_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_retry_execution_failed_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record" && ["failed", "skipped"].includes(item.execution_status)).length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Recovery Playbooks</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_connector_recovery_playbook_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Recovery Closed</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_connector_recovery_closed_count || 0) ? "allow" : "require_approval"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_connector_recovery_closed_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-closure" && ["resolved", "mitigated"].includes(item.closure_state)).length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Recovery Open</span>
      <strong class="${Number(retryRecoveryReport.recovery_open_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(retryRecoveryReport.recovery_open_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Recovery SLO Breached</span>
      <strong class="${Number(retryRecoveryReport.recovery_slo_breached_count || 0) ? "block" : "allow"}">${formatMetricNumber(retryRecoveryReport.recovery_slo_breached_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Recovery Escalations</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_escalation_route_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_route_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Recovery Esc Ack</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_ack_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-ack").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Esc Retryable</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_escalation_retryable_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_retryable_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Esc Retry Runs</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_worker_run_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-worker-run").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Esc Retry Executions</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-execution-record").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Retry Health Alerts</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Retry Health Sends</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-plan").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Health Alert Retryable</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retryable_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retryable_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Health Alert Retry Runs</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-worker-run").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Executive Reports</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Executive Schedules</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_schedule_run_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Executive Sends</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_count || historyItems.filter((item) => item.connector_delivery_source === "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Retryable</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retryable_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retryable_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Retry Runs</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-worker-run").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Retry Failed</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_failed_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_failed_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-execution-record" && ["failed", "skipped"].includes(item.execution_status)).length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Retry Health</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Health Alerts</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-plan").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Alert Retryable</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retryable_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retryable_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Alert Retry Runs</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-worker-run").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exec Alert Retry Failed</span>
      <strong class="${Number(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_failed_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_failed_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Failed Delivery</span>
      <strong class="${Number(dashboard.failed_delivery_count || 0) ? "block" : "allow"}">${formatMetricNumber(dashboard.failed_delivery_count || historyItems.filter((item) => item.delivery_success === false).length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Acknowledgements</span>
      <strong>${formatMetricNumber(dashboard.acknowledgement_count || historyItems.filter((item) => item.metadata_kind === "go-backend-rollback-drill-notification-ack").length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Outstanding</span>
      <strong class="${Number(dashboard.outstanding_acknowledgement_count || outstandingRoutes.length) ? "block" : "allow"}">${formatMetricNumber(dashboard.outstanding_acknowledgement_count || outstandingRoutes.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Escalation Routes</span>
      <strong>${formatMetricNumber(routes.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Breached</span>
      <strong class="${breachedRoutes.length ? "block" : "allow"}">${formatMetricNumber(breachedRoutes.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Route Rows</span>
      <strong>${formatMetricNumber(routingRows.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Suppressed</span>
      <strong class="${suppressedRoutes.length ? "require_approval" : "allow"}">${formatMetricNumber(suppressedRoutes.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Maintenance</span>
      <strong>${formatMetricNumber(suppressionTrend.maintenance_suppressed_count || 0)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Calendar</span>
      <strong>${formatMetricNumber(suppressionTrend.calendar_suppressed_count || 0)}</strong>
    </div>
  `;

  historyItems.forEach((item, index) => {
    const payload = goDrillNotificationPayload(item);
    const payloadId = goDrillPayloadId("history", index);
    const providers = goDrillNotificationProviders(item);
    const statusText = goDrillNotificationStatus(item);
    goDrillNotificationDetailPayloads.set(payloadId, {
      label: item.session_id || item.plan_id || item.acknowledgement_id || item.event_id || "go-drill-notification",
      payload: item
    });
    historyRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.session_id || item.plan_id || item.acknowledgement_id || item.event_id || "notification")}</td>
        <td>${escapeHtml(goDrillNotificationKindLabel(item.metadata_kind))}</td>
        <td>${escapeHtml(providers.join(", ") || "n/a")}</td>
        <td class="${statusText === "delivery_failed" || statusText === "critical" ? "block" : statusText === "warning" || statusText === "escalated" ? "require_approval" : "allow"}">${escapeHtml(statusText)}</td>
        <td>${escapeHtml(item.schedule_id || item.event_id || payload.schedule_id || "n/a")}</td>
        <td>${escapeHtml(String(item.created_at || payload.generated_at || payload.acknowledged_at || "").slice(0, 19))}</td>
        <td>${goDrillNotificationActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!historyItems.length) historyRows.insertAdjacentHTML("beforeend", `<tr><td colspan="7">No rollback drill notification records match the current filters.</td></tr>`);

  routes.forEach((route, index) => {
    const payloadId = goDrillPayloadId("route", index);
    const state = route.acknowledgement_state || (route.acknowledged ? "acknowledged" : "outstanding");
    goDrillNotificationDetailPayloads.set(payloadId, {
      label: `${route.schedule_id || "schedule"}-${route.provider || "provider"}`,
      payload: route
    });
    const age = route.age_minutes === null || route.age_minutes === undefined ? "n/a" : `${formatMetricNumber(route.age_minutes)}m`;
    const slo = route.acknowledgement_minutes === null || route.acknowledgement_minutes === undefined ? "n/a" : `${formatMetricNumber(route.acknowledgement_minutes)}m`;
    escalationRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(route.schedule_id || "unknown")}</td>
        <td>${escapeHtml(route.provider || "unknown")}</td>
        <td>${escapeHtml(route.owner || "release-governance")}</td>
        <td class="${route.breached ? "block" : state === "outstanding" ? "require_approval" : "allow"}">${escapeHtml(state)}</td>
        <td>${escapeHtml(`${age} / ${slo}`)}</td>
        <td>${escapeHtml(route.recommended_action || "n/a")}</td>
        <td>${goDrillNotificationMutationButtons(payloadId, route)}</td>
      </tr>
    `);
  });
  if (!routes.length) escalationRows.insertAdjacentHTML("beforeend", `<tr><td colspan="7">No escalation routes are currently indexed.</td></tr>`);

  routingRows.forEach((route, index) => {
    const payloadId = goDrillPayloadId("routing", index);
    goDrillNotificationDetailPayloads.set(payloadId, {
      label: route.route_id || `${route.schedule_id || "schedule"}-${route.provider || "provider"}-${route.action || "route"}`,
      payload: route
    });
    routeRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(route.route_id || route.plan_id || "route")}</td>
        <td>${escapeHtml(route.owner || "release-governance")}</td>
        <td>${escapeHtml(route.provider || "unknown")}</td>
        <td class="${route.action === "suppress" ? "require_approval" : "allow"}">${escapeHtml(route.action || "unknown")}</td>
        <td>${escapeHtml(route.category || "none")}</td>
        <td>${escapeHtml(route.reason || "n/a")}</td>
        <td>${goDrillNotificationActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!routingRows.length) routeRows.insertAdjacentHTML("beforeend", `<tr><td colspan="7">No routing history rows match the current filters.</td></tr>`);

  const trendPayloadId = goDrillPayloadId("suppression-trend", 0);
  goDrillNotificationDetailPayloads.set(trendPayloadId, {
    label: suppressionTrend.trend_id || "go-drill-routing-suppression-trend",
    payload: suppressionTrend
  });
  const categories = Object.entries(suppressionTrend.category_counts || {});
  if (categories.length) {
    categories.forEach(([category, count], index) => {
      const payloadId = index === 0 ? trendPayloadId : goDrillPayloadId("suppression-trend", index);
      goDrillNotificationDetailPayloads.set(payloadId, {
        label: `${suppressionTrend.trend_id || "suppression-trend"}-${category}`,
        payload: { category, count, trend: suppressionTrend }
      });
      suppressionRows.insertAdjacentHTML("beforeend", `
        <tr>
          <td>${escapeHtml(category)}</td>
          <td class="${Number(count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(count)}</td>
          <td>${escapeHtml(topCountLabel(suppressionTrend.owner_counts))}</td>
          <td>${escapeHtml(topCountLabel(suppressionTrend.provider_counts))}</td>
          <td>${escapeHtml(String(suppressionTrend.generated_at || "").slice(0, 19))}</td>
          <td>${goDrillNotificationActionButtons(payloadId)}</td>
        </tr>
      `);
    });
  } else {
    suppressionRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>none</td>
        <td class="allow">0</td>
        <td>${escapeHtml(topCountLabel(suppressionTrend.owner_counts))}</td>
        <td>${escapeHtml(topCountLabel(suppressionTrend.provider_counts))}</td>
        <td>${escapeHtml(String(suppressionTrend.generated_at || "").slice(0, 19))}</td>
        <td>${goDrillNotificationActionButtons(trendPayloadId)}</td>
      </tr>
    `);
  }

  (retryRecoveryReport.provider_summary || []).forEach((summary, index) => {
    const payloadId = goDrillPayloadId("retry-recovery", index);
    goDrillNotificationDetailPayloads.set(payloadId, {
      label: `${summary.provider || "provider"}-retry-recovery`,
      payload: summary
    });
    retryRecoveryRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(summary.provider || "unknown")}</td>
        <td>${formatMetricNumber(summary.execution_count || 0)}</td>
        <td class="${Number(summary.execution_failed_count || 0) || Number(summary.execution_skipped_count || 0) ? "block" : "allow"}">${formatMetricNumber(Number(summary.execution_failed_count || 0) + Number(summary.execution_skipped_count || 0))}</td>
        <td class="${Number(summary.open_recovery_count || 0) ? "require_approval" : "allow"}">${formatMetricNumber(summary.open_recovery_count || 0)}</td>
        <td class="${Number(summary.slo_breached_count || 0) ? "block" : "allow"}">${formatMetricNumber(summary.slo_breached_count || 0)}</td>
        <td>${escapeHtml(String(summary.latest_closure_at || "").slice(0, 19) || "n/a")}</td>
        <td>${goDrillNotificationActionButtons(payloadId)}</td>
      </tr>
    `);
  });
  if (!(retryRecoveryReport.provider_summary || []).length) {
    retryRecoveryRows.insertAdjacentHTML("beforeend", `<tr><td colspan="7">No retry recovery SLO rows are currently indexed.</td></tr>`);
  }
}

function showGoDrillNotificationDetail(payloadId) {
  const panel = document.querySelector("#goDrillNotificationDetail");
  const entry = goDrillNotificationDetailPayloads.get(payloadId);
  if (!panel || !entry) return;
  panel.innerHTML = `
    <dl>
      <dt>Artifact</dt><dd>${escapeHtml(entry.label)}</dd>
      <dt>Type</dt><dd>${escapeHtml(payloadId.split(":")[0].replace("go-drill-", ""))}</dd>
    </dl>
    <pre>${escapeHtml(JSON.stringify(entry.payload, null, 2))}</pre>
  `;
}

function exportGoDrillNotificationPayload(payloadId) {
  const entry = goDrillNotificationDetailPayloads.get(payloadId);
  if (!entry) return;
  const fileName = `${String(entry.label || "cavra-go-drill-notification").replace(/[^a-zA-Z0-9_.-]+/g, "-")}.json`;
  const blob = new Blob([JSON.stringify(entry.payload, null, 2)], { type: "application/json" });
  const href = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = href;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(href);
}

function goDrillAckActor() {
  const configured = document.querySelector("#goDrillAckActor")?.value.trim();
  const sessionActor = consoleSessionCache?.actor?.actor;
  return configured || sessionActor || "console-user";
}

function addSampleGoDrillAcknowledgement(route, acknowledgementState, payload) {
  const acknowledgedAt = new Date().toISOString();
  const acknowledgementId = `gordack-${route.schedule_id}-${route.provider}-${acknowledgementState}-${Date.now()}`;
  const acknowledgement = {
    schema_version: "cavra.go-backend-pilot.rollback-drill-notification-ack.v1",
    product: "CAVRA",
    acknowledgement_id: acknowledgementId,
    schedule_id: route.schedule_id,
    plan_id: route.plan_id || "",
    provider: route.provider,
    acknowledged_by: payload.acknowledged_by,
    acknowledgement_state: acknowledgementState,
    acknowledged_at: acknowledgedAt,
    external_ref: payload.external_ref || "",
    notes: payload.notes || ""
  };
  goRollbackDrillNotificationCatalog.unshift({
    session_id: acknowledgementId,
    metadata_kind: "go-backend-rollback-drill-notification-ack",
    created_at: acknowledgedAt,
    signer: payload.acknowledged_by,
    acknowledgement_id: acknowledgementId,
    schedule_id: route.schedule_id,
    plan_id: route.plan_id || "",
    provider: route.provider,
    acknowledgement_state: acknowledgementState,
    acknowledgement
  });
  for (const item of goRollbackDrillNotificationCatalog) {
    const routes = item?.escalation_plan?.routes;
    if (!Array.isArray(routes)) continue;
    for (const escalationRoute of routes) {
      if (escalationRoute.schedule_id === route.schedule_id && escalationRoute.provider === route.provider) {
        escalationRoute.acknowledgement_state = acknowledgementState;
        escalationRoute.acknowledged = ["acknowledged", "resolved"].includes(acknowledgementState);
        escalationRoute.breached = acknowledgementState === "escalated";
        escalationRoute.recommended_action = acknowledgementState === "escalated" ? "follow_escalation_runbook" : "no_action";
      }
    }
  }
}

async function recordGoDrillAcknowledgement(payloadId, acknowledgementState) {
  const status = document.querySelector("#goDrillAckStatus");
  const entry = goDrillNotificationDetailPayloads.get(payloadId);
  const route = entry?.payload || {};
  if (!route.schedule_id || !route.provider) {
    if (status) status.textContent = "Select a deliverable drill route before recording an acknowledgement.";
    return;
  }
  const payload = {
    provider: route.provider,
    plan_id: route.plan_id || "",
    acknowledged_by: goDrillAckActor(),
    acknowledgement_state: acknowledgementState,
    external_ref: document.querySelector("#goDrillAckExternalRef")?.value.trim() || "",
    notes: document.querySelector("#goDrillAckNotes")?.value.trim() || `Console marked route ${acknowledgementState}.`
  };
  if (status) status.textContent = `Recording ${acknowledgementState} for ${route.provider}...`;
  try {
    const response = await fetch(apiUrl(`/runtime/go-pilot/rollback-drill-notifications/${encodeURIComponent(route.schedule_id)}/acknowledgements`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
      const detail = await response.text();
      if ([401, 403].includes(response.status)) {
        if (status) status.textContent = `Acknowledgement requires an authorized console session: ${detail || response.statusText}`;
        return;
      }
      throw new Error(detail || "acknowledgement API unavailable");
    }
    const result = await response.json();
    if (status) {
      const actor = result.actor?.actor || result.acknowledgement?.acknowledged_by || payload.acknowledged_by;
      status.textContent = `Recorded ${acknowledgementState} for ${route.provider} as ${actor}.`;
    }
  } catch (error) {
    addSampleGoDrillAcknowledgement(route, acknowledgementState, payload);
    if (status) status.textContent = `Using local sample acknowledgement: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

function goDrillBulkRouteCandidates(acknowledgementState) {
  return currentGoDrillEscalationRoutes.filter((route) => {
    if (!route.schedule_id || !route.provider) return false;
    if (acknowledgementState === "escalated") return Boolean(route.breached);
    const state = route.acknowledgement_state || (route.acknowledged ? "acknowledged" : "outstanding");
    return state === "outstanding" || route.acknowledged === false;
  });
}

function goDrillAcknowledgementPayload(acknowledgementState, routes) {
  return {
    acknowledged_by: goDrillAckActor(),
    acknowledgement_state: acknowledgementState,
    external_ref: document.querySelector("#goDrillAckExternalRef")?.value.trim() || "",
    notes: document.querySelector("#goDrillAckNotes")?.value.trim() || `Console bulk marked routes ${acknowledgementState}.`,
    routes: routes.map((route) => ({
      schedule_id: route.schedule_id,
      provider: route.provider,
      plan_id: route.plan_id || "",
      external_ref: route.external_ref || "",
      notes: route.notes || ""
    }))
  };
}

async function recordGoDrillBulkAcknowledgements(acknowledgementState) {
  const status = document.querySelector("#goDrillAckStatus");
  const routes = goDrillBulkRouteCandidates(acknowledgementState);
  if (!routes.length) {
    if (status) status.textContent = `No ${acknowledgementState === "escalated" ? "breached" : "outstanding"} drill routes match the current filters.`;
    return;
  }
  const payload = goDrillAcknowledgementPayload(acknowledgementState, routes);
  if (status) status.textContent = `Recording ${acknowledgementState} for ${routes.length} route(s)...`;
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) {
      const detail = await response.text();
      if ([401, 403].includes(response.status)) {
        if (status) status.textContent = `Bulk acknowledgement requires an authorized console session: ${detail || response.statusText}`;
        return;
      }
      throw new Error(detail || "bulk acknowledgement API unavailable");
    }
    const result = await response.json();
    if (status) status.textContent = `Recorded ${result.acknowledgement_count || routes.length} ${acknowledgementState} acknowledgement(s).`;
  } catch (error) {
    for (const route of routes) addSampleGoDrillAcknowledgement(route, acknowledgementState, payload);
    if (status) status.textContent = `Using local sample bulk acknowledgement: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

function latestGoDrillAckByRoute() {
  const acknowledgements = goRollbackDrillNotificationCatalog
    .filter((item) => item.metadata_kind === "go-backend-rollback-drill-notification-ack")
    .sort((left, right) => String(right.created_at || "").localeCompare(String(left.created_at || "")));
  const latest = new Map();
  for (const item of acknowledgements) {
    const ack = item.acknowledgement && typeof item.acknowledgement === "object" ? item.acknowledgement : item;
    const key = `${ack.schedule_id || item.schedule_id || ""}:${ack.provider || item.provider || ""}`;
    if (key !== ":" && !latest.has(key)) latest.set(key, ack);
  }
  return latest;
}

function buildSampleGoDrillAckAuditPackage() {
  const filters = selectedGoDrillNotificationFilters();
  const latestAck = latestGoDrillAckByRoute();
  const routes = currentGoDrillEscalationRoutes.map((route) => {
    const ack = latestAck.get(`${route.schedule_id || ""}:${route.provider || ""}`) || {};
    const state = ack.acknowledgement_state || route.acknowledgement_state || (route.acknowledged ? "acknowledged" : "outstanding");
    return {
      route_id: route.route_id || "",
      schedule_id: route.schedule_id || "",
      plan_id: route.plan_id || "",
      provider: route.provider || "",
      owner: route.owner || "release-governance",
      acknowledgement_state: state,
      acknowledged: ["acknowledged", "resolved"].includes(state),
      acknowledged_by: ack.acknowledged_by || "",
      acknowledged_at: ack.acknowledged_at || "",
      external_ref: ack.external_ref || "",
      notes: ack.notes || ""
    };
  });
  const countState = (state) => routes.filter((route) => route.acknowledgement_state === state).length;
  return {
    schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-package.v1",
    product: "CAVRA",
    audit_id: `sample-go-drill-ack-audit-${Date.now()}`,
    generated_at: new Date().toISOString(),
    generated_by: goDrillAckActor(),
    filters: { owner: filters.owner, provider: filters.provider, schedule_id: "" },
    route_count: routes.length,
    acknowledgement_count: routes.filter((route) => route.acknowledged_by).length,
    acknowledged_count: countState("acknowledged"),
    resolved_count: countState("resolved"),
    escalated_count: countState("escalated"),
    dismissed_count: countState("dismissed"),
    outstanding_count: routes.filter((route) => !route.acknowledged).length,
    alert_level: routes.some((route) => !route.acknowledged) ? "critical" : "healthy",
    routes,
    controls: ["sample-public-safe-acknowledgement-audit-package"]
  };
}

async function exportGoDrillAckAuditPackage() {
  const status = document.querySelector("#goDrillAckStatus");
  const filters = selectedGoDrillNotificationFilters();
  let auditPackage = null;
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        owner: filters.owner,
        provider: filters.provider,
        generated_by: goDrillAckActor()
      })
    });
    if (!response.ok) {
      const detail = await response.text();
      if ([401, 403].includes(response.status)) {
        if (status) status.textContent = `Audit export requires an authorized console session: ${detail || response.statusText}`;
        return;
      }
      throw new Error(detail || "acknowledgement audit API unavailable");
    }
    const result = await response.json();
    auditPackage = result.audit_package || result;
    if (status) status.textContent = `Exported acknowledgement audit package ${auditPackage.audit_id || ""}.`;
  } catch (error) {
    auditPackage = buildSampleGoDrillAckAuditPackage();
    if (status) status.textContent = `Using local sample acknowledgement audit package: ${error.message || "API unavailable"}.`;
  }
  const fileName = `${String(auditPackage.audit_id || "cavra-go-drill-ack-audit").replace(/[^a-zA-Z0-9_.-]+/g, "-")}.json`;
  const blob = new Blob([JSON.stringify(auditPackage, null, 2)], { type: "application/json" });
  const href = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = href;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(href);
}

function addSampleGoDrillAckAuditDelivery(auditPackage, provider) {
  const deliveredAt = new Date().toISOString();
  const deliveryId = `sample-go-drill-ack-delivery-${Date.now()}`;
  const deliveryPlan = {
    schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-plan.v1",
    product: "CAVRA",
    delivery_id: deliveryId,
    audit_id: auditPackage.audit_id || "",
    generated_at: deliveredAt,
    generated_by: goDrillAckActor(),
    cadence: "on_demand",
    schedule_ref: "console-sample",
    requested_provider: provider,
    selected_providers: [provider],
    destination_count: 1,
    route_count: auditPackage.route_count || 0,
    outstanding_count: auditPackage.outstanding_count || 0,
    alert_level: auditPackage.alert_level || "healthy",
    controls: ["sample-public-safe-acknowledgement-audit-delivery"]
  };
  goRollbackDrillNotificationCatalog.unshift({
    session_id: deliveryId,
    metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-plan",
    created_at: deliveredAt,
    signer: deliveryPlan.generated_by,
    delivery_id: deliveryId,
    audit_id: deliveryPlan.audit_id,
    selected_providers: [provider],
    acknowledgement_audit_delivery_plan: deliveryPlan
  });
  goRollbackDrillNotificationCatalog.unshift({
    session_id: `${deliveryId}-connector`,
    metadata_kind: "release-connector-delivery",
    connector_delivery_source: "go_backend_rollback_drill_acknowledgement_audit",
    created_at: deliveredAt,
    signer: "sample-connector",
    event_id: deliveryId,
    delivery_id: deliveryId,
    audit_id: deliveryPlan.audit_id,
    event_type: "cavra.go_backend.rollback_drill.acknowledgement_audit_delivery",
    delivery_success: false,
    providers: [provider],
    failed_providers: [provider],
    delivery: { success: false, provider, mode: "sample" }
  });
}

async function deliverGoDrillAckAuditPackage() {
  const status = document.querySelector("#goDrillAckStatus");
  const filters = selectedGoDrillNotificationFilters();
  const deliveryProvider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = `Delivering acknowledgement audit package to ${deliveryProvider}...`;
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        owner: filters.owner,
        provider: filters.provider,
        delivery_provider: deliveryProvider,
        generated_by: goDrillAckActor(),
        cadence: "on_demand",
        schedule_ref: "evidence-console"
      })
    });
    if (!response.ok) {
      const detail = await response.text();
      if ([401, 403].includes(response.status)) {
        if (status) status.textContent = `Audit delivery requires an authorized console session: ${detail || response.statusText}`;
        return;
      }
      throw new Error(detail || "acknowledgement audit delivery API unavailable");
    }
    const result = await response.json();
    if (status) {
      const selected = result.delivery_plan?.selected_providers?.join(", ") || deliveryProvider;
      status.textContent = `Delivered acknowledgement audit package ${result.audit_package?.audit_id || ""} to ${selected}.`;
    }
  } catch (error) {
    const auditPackage = buildSampleGoDrillAckAuditPackage();
    addSampleGoDrillAckAuditDelivery(auditPackage, deliveryProvider);
    if (status) status.textContent = `Using local sample audit delivery: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

function addSampleGoDrillAckAuditRetryPlan() {
  const generatedAt = new Date().toISOString();
  const failedDelivery = goRollbackDrillNotificationCatalog.find(
    (item) => item.connector_delivery_source === "go_backend_rollback_drill_acknowledgement_audit" && item.delivery_success === false
  );
  const retryPlanId = `sample-go-drill-ack-retry-${Date.now()}`;
  const retryDecision = failedDelivery
    ? {
        delivery_id: failedDelivery.delivery_id || failedDelivery.event_id || failedDelivery.session_id,
        audit_id: failedDelivery.audit_id || "",
        provider: (failedDelivery.failed_providers || failedDelivery.providers || ["webhook"])[0],
        action: "retry",
        reason: "sample failed acknowledgement audit delivery is eligible for retry",
        retry_count: 1,
        max_retry_attempts: 3,
        retry_delay_minutes: 15,
        latest_delivery_id: failedDelivery.session_id,
        latest_delivery_at: failedDelivery.created_at,
        next_retry_at: generatedAt,
        failed_status_codes: failedDelivery.status_codes || []
      }
    : null;
  const retryPlan = {
    schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-retry-plan.v1",
    product: "CAVRA",
    retry_plan_id: retryPlanId,
    generated_at: generatedAt,
    generated_by: goDrillAckActor(),
    alert_level: retryDecision ? "critical" : "healthy",
    decision_count: retryDecision ? 1 : 0,
    retryable_count: retryDecision ? 1 : 0,
    waiting_count: 0,
    suppressed_count: 0,
    max_retry_attempts: 3,
    base_retry_delay_minutes: 15,
    backoff_multiplier: 2,
    retry_decisions: retryDecision ? [retryDecision] : [],
    controls: ["sample-public-safe-acknowledgement-audit-delivery-retry-plan"]
  };
  goRollbackDrillNotificationCatalog.unshift({
    session_id: retryPlanId,
    created_at: generatedAt,
    signer: retryPlan.generated_by,
    metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan",
    retry_plan_id: retryPlanId,
    alert_level: retryPlan.alert_level,
    retryable_count: retryPlan.retryable_count,
    waiting_count: retryPlan.waiting_count,
    suppressed_count: retryPlan.suppressed_count,
    acknowledgement_audit_delivery_retry_plan: retryPlan
  });
  return retryPlan;
}

async function planGoDrillAckAuditRetry() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Planning acknowledgement audit delivery retries...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 15, backoff_multiplier: 2 }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "acknowledgement audit retry plan API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Planned ${formatMetricNumber(result.plan?.retryable_count || 0)} retryable audit deliveries.`;
  } catch (error) {
    const retryPlan = addSampleGoDrillAckAuditRetryPlan();
    if (status) status.textContent = `Using local sample retry plan with ${formatMetricNumber(retryPlan.retryable_count || 0)} retryable deliveries: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function runGoDrillAckAuditWorker() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Running acknowledgement audit delivery worker dry-run...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        dry_run: true,
        max_retry_deliveries: 5,
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 },
        schedule: { interval_minutes: 30, cadence: "every_30_minutes", enabled: true }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "acknowledgement audit worker API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Worker dry-run selected ${formatMetricNumber(result.run?.summary?.selected_retry_count || 0)} retry deliveries.`;
  } catch (error) {
    const retryPlan = addSampleGoDrillAckAuditRetryPlan();
    const generatedAt = new Date().toISOString();
    const runId = `sample-go-drill-ack-worker-${Date.now()}`;
    const workerRun = {
      schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-worker-run.v1",
      product: "CAVRA",
      run_id: runId,
      generated_at: generatedAt,
      generated_by: goDrillAckActor(),
      dry_run: true,
      schedule: { interval_minutes: 30, window_start: generatedAt, window_end: generatedAt, enabled: true, cadence: "every_30_minutes" },
      summary: {
        retry_plan_count: 1,
        retryable_count: retryPlan.retryable_count || 0,
        waiting_retry_count: retryPlan.waiting_count || 0,
        suppressed_retry_count: retryPlan.suppressed_count || 0,
        selected_retry_count: retryPlan.retryable_count || 0,
        follow_up_action_count: retryPlan.decision_count || 0
      },
      retry_plan: retryPlan,
      selected_retries: retryPlan.retry_decisions || [],
      follow_up_actions: retryPlan.retry_decisions || [],
      controls: ["sample-public-safe-acknowledgement-audit-delivery-worker-run"]
    };
    goRollbackDrillNotificationCatalog.unshift({
      session_id: runId,
      created_at: generatedAt,
      signer: workerRun.generated_by,
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run",
      run_id: runId,
      dry_run: true,
      retryable_count: workerRun.summary.retryable_count,
      selected_retry_count: workerRun.summary.selected_retry_count,
      acknowledgement_audit_delivery_worker_run: workerRun
    });
    if (status) status.textContent = `Using local sample worker dry-run: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

function latestGoDrillRetryPlan() {
  return goRollbackDrillNotificationCatalog.find(
    (item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan"
  )?.acknowledgement_audit_delivery_retry_plan;
}

function latestGoDrillRetryApprovalPlan() {
  return goRollbackDrillNotificationCatalog.find(
    (item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-plan"
  )?.retry_execution_approval_plan;
}

function addSampleGoDrillRetryExecutionApprovalPlan() {
  const generatedAt = new Date().toISOString();
  const retryPlan = latestGoDrillRetryPlan() || addSampleGoDrillAckAuditRetryPlan();
  const retryDecision = (retryPlan.retry_decisions || [])[0] || {};
  const approvalPlanId = `sample-go-drill-retry-approval-${Date.now()}`;
  const approvalDecision = {
    retry_plan_id: retryPlan.retry_plan_id,
    provider: retryDecision.provider || "webhook",
    delivery_id: retryDecision.delivery_id || "",
    audit_id: retryDecision.audit_id || "",
    action: "request_approval",
    reason: "retry execution is acknowledged and ready for governed approval",
    approval_required: true
  };
  const plan = {
    schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-plan.v1",
    product: "CAVRA",
    approval_plan_id: approvalPlanId,
    generated_at: generatedAt,
    generated_by: goDrillAckActor(),
    alert_level: "critical",
    decision_count: 1,
    approval_required_count: 1,
    approved_count: 0,
    waiting_count: 0,
    approval_decisions: [approvalDecision],
    controls: ["sample-public-safe-retry-execution-approval-plan"]
  };
  goRollbackDrillNotificationCatalog.unshift({
    session_id: approvalPlanId,
    created_at: generatedAt,
    signer: plan.generated_by,
    metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-plan",
    approval_plan_id: approvalPlanId,
    alert_level: plan.alert_level,
    approval_required_count: 1,
    retry_execution_approval_plan: plan
  });
  return plan;
}

async function planGoDrillRetryExecutionApproval() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Planning acknowledgement audit retry execution approvals...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        approval_policy: { require_retry_ack: true }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "retry execution approval API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Planned ${formatMetricNumber(result.plan?.approval_required_count || 0)} retry execution approvals.`;
  } catch (error) {
    const plan = addSampleGoDrillRetryExecutionApprovalPlan();
    if (status) status.textContent = `Using local sample retry approval plan ${plan.approval_plan_id}: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function approveGoDrillRetryExecution() {
  const status = document.querySelector("#goDrillAckStatus");
  const approvalPlan = latestGoDrillRetryApprovalPlan() || addSampleGoDrillRetryExecutionApprovalPlan();
  const decision = (approvalPlan.approval_decisions || []).find((item) => item.action === "request_approval") || (approvalPlan.approval_decisions || [])[0] || {};
  const provider = decision.provider || document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Approving acknowledgement audit retry execution...";
  try {
    const response = await fetch(apiUrl(`/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plans/${encodeURIComponent(approvalPlan.approval_plan_id)}/decisions`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        provider,
        decided_by: goDrillAckActor(),
        approval_state: "approved",
        retry_plan_id: decision.retry_plan_id || "",
        delivery_id: decision.delivery_id || "",
        audit_id: decision.audit_id || "",
        external_ref: document.querySelector("#goDrillAckExternalRef")?.value || "",
        notes: document.querySelector("#goDrillAckNotes")?.value || ""
      })
    });
    if (!response.ok) throw new Error(await response.text() || "retry execution approval decision API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Approved retry execution ${result.decision?.decision_id || ""}.`;
  } catch (error) {
    const decidedAt = new Date().toISOString();
    const decisionId = `sample-go-drill-retry-approval-decision-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: decisionId,
      created_at: decidedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision",
      decision_id: decisionId,
      approval_plan_id: approvalPlan.approval_plan_id,
      retry_plan_id: decision.retry_plan_id || "",
      delivery_id: decision.delivery_id || "",
      audit_id: decision.audit_id || "",
      provider,
      approval_state: "approved",
      retry_execution_approval_decision: {
        decision_id: decisionId,
        approval_plan_id: approvalPlan.approval_plan_id,
        provider,
        approval_state: "approved",
        decided_by: goDrillAckActor(),
        decided_at: decidedAt
      }
    });
    if (status) status.textContent = `Using local sample retry approval: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function executeGoDrillApprovedRetry() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Executing approved acknowledgement audit retry...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        execute: true,
        max_retry_deliveries: 5,
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 15, backoff_multiplier: 2 },
        schedule: { interval_minutes: 30, cadence: "manual_retry", enabled: true },
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "approved retry execution API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Executed ${formatMetricNumber(result.retry_results?.filter((item) => item.execution_record).length || 0)} approved retry records.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const executionId = `sample-go-drill-retry-execution-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: executionId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record",
      execution_id: executionId,
      execution_status: "skipped",
      provider: document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook",
      delivery_success: false,
      retry_execution_record: {
        execution_id: executionId,
        execution_status: "skipped",
        executed_at: generatedAt,
        executed_by: goDrillAckActor(),
        controls: ["sample-public-safe-live-retry-execution-record"]
      }
    });
    if (status) status.textContent = `Using local sample retry execution record: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

function latestGoDrillConnectorRecoveryPlaybook() {
  return goRollbackDrillNotificationCatalog.find(
    (item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook"
  )?.connector_recovery_playbook;
}

async function buildGoDrillConnectorRecoveryPlaybook() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Building acknowledgement audit connector recovery playbook...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        min_failure_count: 1,
        lookback_hours: 24
      })
    });
    if (!response.ok) throw new Error(await response.text() || "connector recovery playbook API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Built ${formatMetricNumber(result.playbook?.provider_count || 0)} connector recovery playbooks.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const playbookId = `sample-go-drill-connector-recovery-${Date.now()}`;
    const playbook = {
      playbook_id: playbookId,
      generated_at: generatedAt,
      generated_by: goDrillAckActor(),
      alert_level: "critical",
      provider_count: 1,
      failure_count: 1,
      provider_playbooks: [{ provider: "webhook", category: "webhook", failure_count: 1 }],
      controls: ["sample-public-safe-connector-recovery-playbook"]
    };
    goRollbackDrillNotificationCatalog.unshift({
      session_id: playbookId,
      created_at: generatedAt,
      signer: playbook.generated_by,
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook",
      playbook_id: playbookId,
      alert_level: "critical",
      provider_count: 1,
      failure_count: 1,
      connector_recovery_playbook: playbook
    });
    if (status) status.textContent = `Using local sample recovery playbook: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function closeGoDrillConnectorRecovery() {
  const status = document.querySelector("#goDrillAckStatus");
  const playbook = latestGoDrillConnectorRecoveryPlaybook();
  const provider = playbook?.provider_playbooks?.[0]?.provider || document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Closing connector recovery playbook...";
  try {
    if (!playbook?.playbook_id) throw new Error("connector recovery playbook is not available");
    const response = await fetch(apiUrl(`/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbooks/${encodeURIComponent(playbook.playbook_id)}/closures`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        provider,
        closed_by: goDrillAckActor(),
        closure_state: "resolved",
        external_ref: document.querySelector("#goDrillAckExternalRef")?.value || "",
        notes: document.querySelector("#goDrillAckNotes")?.value || "",
        verification_refs: goRollbackDrillNotificationCatalog
          .filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record")
          .slice(0, 3)
          .map((item) => item.execution_id)
          .filter(Boolean)
      })
    });
    if (!response.ok) throw new Error(await response.text() || "connector recovery closure API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Closed recovery ${result.closure?.closure_id || ""}.`;
  } catch (error) {
    const closedAt = new Date().toISOString();
    const closureId = `sample-go-drill-recovery-closure-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: closureId,
      created_at: closedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-closure",
      closure_id: closureId,
      playbook_id: playbook?.playbook_id || "",
      provider,
      closure_state: "resolved",
      connector_recovery_closure: {
        closure_id: closureId,
        playbook_id: playbook?.playbook_id || "",
        provider,
        closure_state: "resolved",
        closed_by: goDrillAckActor(),
        closed_at: closedAt
      }
    });
    if (status) status.textContent = `Using local sample recovery closure: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

function latestGoDrillRecoveryEscalationPlan() {
  return goRollbackDrillNotificationCatalog.find(
    (item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan"
  )?.recovery_escalation_plan;
}

async function planGoDrillRecoveryEscalation() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Planning recovery escalation notifications...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        recovery_slo_minutes: 240
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery escalation plan API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Planned ${formatMetricNumber(result.plan?.escalation_count || 0)} recovery escalations.`;
  } catch (error) {
    const plan = buildSampleGoDrillRecoveryEscalationPlan(goRollbackDrillNotificationCatalog);
    goRollbackDrillNotificationCatalog.unshift({
      session_id: plan.plan_id,
      created_at: plan.generated_at,
      signer: plan.generated_by,
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan",
      plan_id: plan.plan_id,
      alert_level: plan.alert_level,
      escalation_count: plan.escalation_count,
      selected_providers: plan.selected_providers,
      recovery_escalation_plan: plan
    });
    if (status) status.textContent = `Using local sample recovery escalation plan: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function deliverGoDrillRecoveryEscalation() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  const plan = latestGoDrillRecoveryEscalationPlan();
  if (status) status.textContent = "Delivering recovery escalation notification...";
  try {
    if (!plan?.plan_id) throw new Error("recovery escalation plan is not available");
    const response = await fetch(apiUrl(`/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/${encodeURIComponent(plan.plan_id)}/deliver`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        provider,
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery escalation delivery API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Delivered recovery escalation ${result.event_id || plan.plan_id}.`;
  } catch (error) {
    const createdAt = new Date().toISOString();
    const deliveryId = `sample-go-drill-recovery-escalation-delivery-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: deliveryId,
      metadata_kind: "release-connector-delivery",
      connector_delivery_source: "go_backend_rollback_drill_acknowledgement_audit_recovery_escalation",
      created_at: createdAt,
      event_id: plan?.plan_id || deliveryId,
      event_type: "cavra.go_backend.rollback_drill.acknowledgement_audit_delivery.recovery_escalation",
      delivery_success: false,
      providers: [provider],
      failed_providers: [provider],
      plan_id: plan?.plan_id || "",
      attempt_count: 1,
      max_attempt_count: 1
    });
    if (status) status.textContent = `Using local sample recovery escalation delivery: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function buildGoDrillRecoveryExecutiveReport() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Building recovery executive report...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report", {
      recovery_slo_minutes: 240,
      generated_by: goDrillAckActor()
    }));
    if (!response.ok) throw new Error(await response.text() || "recovery executive report API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Built executive report ${result.report?.executive_report_id || ""}.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const plan = latestGoDrillRecoveryEscalationPlan() || buildSampleGoDrillRecoveryEscalationPlan(goRollbackDrillNotificationCatalog);
    const executiveReport = {
      schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-recovery-executive-report.v1",
      product: "CAVRA",
      executive_report_id: `sample-go-drill-recovery-executive-${Date.now()}`,
      generated_at: generatedAt,
      generated_by: goDrillAckActor(),
      alert_level: plan.alert_level || "healthy",
      executive_summary: {
        status: plan.alert_level || "healthy",
        failed_execution_count: Number(plan.failed_execution_count || 0),
        open_recovery_count: Number(plan.open_recovery_count || 0),
        slo_breached_count: Number(plan.slo_breached_count || 0),
        escalation_count: Number(plan.escalation_count || 0)
      },
      key_risks: plan.escalation_routes || [],
      recommended_actions: ["deliver recovery escalation notifications to operations channels"]
    };
    goRollbackDrillNotificationCatalog.unshift({
      session_id: executiveReport.executive_report_id,
      created_at: generatedAt,
      signer: executiveReport.generated_by,
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report",
      executive_report_id: executiveReport.executive_report_id,
      alert_level: executiveReport.alert_level,
      escalation_count: executiveReport.executive_summary.escalation_count,
      recovery_executive_report: executiveReport
    });
    if (status) status.textContent = `Using local sample executive report: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function acknowledgeGoDrillRecoveryEscalation() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  const plan = latestGoDrillRecoveryEscalationPlan();
  if (status) status.textContent = "Acknowledging recovery escalation...";
  try {
    if (!plan?.plan_id) throw new Error("recovery escalation plan is not available");
    const response = await fetch(apiUrl(`/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/${encodeURIComponent(plan.plan_id)}/acknowledgements`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        provider,
        acknowledged_by: goDrillAckActor(),
        acknowledgement_state: "accepted",
        external_ref: document.querySelector("#goDrillAckExternalRef")?.value || "",
        notes: document.querySelector("#goDrillAckNotes")?.value || "",
        escalation_reason: plan.escalation_routes?.[0]?.reason || ""
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery escalation acknowledgement API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Acknowledged recovery escalation ${result.acknowledgement?.acknowledgement_id || ""}.`;
  } catch (error) {
    const acknowledgedAt = new Date().toISOString();
    const acknowledgementId = `sample-go-drill-recovery-escalation-ack-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: acknowledgementId,
      created_at: acknowledgedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-ack",
      acknowledgement_id: acknowledgementId,
      plan_id: plan?.plan_id || "",
      provider,
      acknowledgement_state: "accepted",
      recovery_escalation_acknowledgement: {
        acknowledgement_id: acknowledgementId,
        plan_id: plan?.plan_id || "",
        provider,
        acknowledged_by: goDrillAckActor(),
        acknowledgement_state: "accepted",
        acknowledged_at: acknowledgedAt
      }
    });
    if (status) status.textContent = `Using local sample recovery escalation acknowledgement: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function planGoDrillRecoveryEscalationRetry() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Planning recovery escalation delivery retry...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery escalation retry plan API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Planned ${formatMetricNumber(result.plan?.retryable_count || 0)} recovery escalation retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const retryPlanId = `sample-go-drill-recovery-escalation-retry-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: retryPlanId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-delivery-retry-plan",
      retry_plan_id: retryPlanId,
      alert_level: "warning",
      retryable_count: 1,
      recovery_escalation_delivery_retry_plan: {
        retry_plan_id: retryPlanId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        retryable_count: 1,
        retry_decisions: [{ provider: "webhook", action: "retry", reason: "sample recovery escalation delivery retry" }]
      }
    });
    if (status) status.textContent = `Using local sample recovery escalation retry plan: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function scheduleGoDrillRecoveryExecutiveReport() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Running scheduled recovery executive report...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        recovery_slo_minutes: 240,
        schedule: { interval_minutes: 60, cadence: "hourly", enabled: true }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery executive report schedule API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Scheduled executive report run ${result.run?.run_id || ""}.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const runId = `sample-go-drill-recovery-executive-schedule-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: runId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run",
      run_id: runId,
      alert_level: "warning",
      recovery_executive_report_schedule_run: {
        run_id: runId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        schedule: { interval_minutes: 60, cadence: "hourly", enabled: true },
        summary: { executive_report_count: 1, escalation_count: 1 }
      }
    });
    if (status) status.textContent = `Using local sample scheduled executive report: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function runGoDrillRecoveryEscalationRetryWorker() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Running recovery escalation retry worker...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-worker-run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        dry_run: true,
        max_retry_deliveries: 5,
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 },
        schedule: { interval_minutes: 30, cadence: "half_hourly", enabled: true }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery escalation retry worker API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Recovery escalation retry worker selected ${formatMetricNumber(result.run?.summary?.selected_retry_count || 0)} retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const runId = `sample-go-drill-recovery-escalation-retry-worker-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: runId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-worker-run",
      run_id: runId,
      dry_run: true,
      retryable_count: 1,
      selected_retry_count: 1,
      recovery_escalation_retry_worker_run: {
        run_id: runId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        dry_run: true,
        summary: { retryable_count: 1, selected_retry_count: 1, acknowledgement_pending_count: 0 }
      }
    });
    if (status) status.textContent = `Using local sample recovery retry worker: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function buildGoDrillRecoveryEscalationRetryHealth() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Building recovery escalation retry health report...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health", {
      expected_interval_minutes: 30,
      stale_metadata_minutes: 120,
      generated_by: goDrillAckActor()
    }));
    if (!response.ok) throw new Error(await response.text() || "recovery escalation retry health API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Recovery retry health ${result.health?.alert_level || "indexed"} with ${formatMetricNumber(result.health?.alert_count || 0)} alerts.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const healthId = `sample-go-drill-recovery-retry-health-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: healthId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health",
      health_id: healthId,
      alert_level: "warning",
      alert_count: 1,
      recovery_escalation_retry_health: {
        health_id: healthId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        alert_level: "warning",
        alert_count: 1,
        retry_plan_count: 1,
        worker_run_count: 1,
        execution_record_count: 1,
        alerts: [{ severity: "warning", category: "sample_recovery_retry_health", message: "Sample recovery retry health report." }]
      }
    });
    if (status) status.textContent = `Using local sample recovery retry health: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function sendGoDrillRecoveryRetryHealthAlert() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Sending recovery escalation retry health alert...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/deliver"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        provider,
        force: true,
        expected_interval_minutes: 30,
        stale_metadata_minutes: 120,
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery retry health alert API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Recovery retry health alert ${result.plan?.plan_id || ""} selected ${formatMetricNumber(result.plan?.selected_providers?.length || 0)} destinations.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const healthId = `sample-go-drill-recovery-retry-health-${Date.now()}`;
    const planId = `sample-go-drill-recovery-retry-health-alert-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: planId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-plan",
      plan_id: planId,
      health_id: healthId,
      alert_level: "warning",
      selected_providers: [provider],
      acknowledgement_required_providers: [provider],
      recovery_escalation_retry_health_alert_plan: {
        plan_id: planId,
        health_id: healthId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        alert_level: "warning",
        selected_providers: [provider],
        acknowledgement_required_providers: [provider],
        summary: { alert_count: 1, retryable_count: 1 }
      }
    });
    if (status) status.textContent = `Using local sample recovery retry health alert: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function planGoDrillRecoveryRetryHealthAlertRetry() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Planning recovery retry health alert redelivery...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery retry health alert retry plan API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Planned ${formatMetricNumber(result.plan?.retryable_count || 0)} recovery health alert retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const retryPlanId = `sample-go-drill-recovery-health-alert-retry-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: retryPlanId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-plan",
      retry_plan_id: retryPlanId,
      alert_level: "warning",
      retryable_count: 1,
      recovery_escalation_retry_health_alert_delivery_retry_plan: {
        retry_plan_id: retryPlanId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        retryable_count: 1,
        waiting_count: 0,
        suppressed_count: 0,
        retry_decisions: [{ provider: "webhook", action: "retry", reason: "sample recovery health alert retry" }]
      }
    });
    if (status) status.textContent = `Using local sample health alert retry plan: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function runGoDrillRecoveryRetryHealthAlertRetryWorker() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Running recovery retry health alert retry worker...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-worker-run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        execute: true,
        provider,
        max_retry_deliveries: 2,
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 },
        schedule: { interval_minutes: 30, cadence: "manual_recovery_health_alert_retry", enabled: true },
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "recovery health alert retry worker API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Recovery health alert retry worker selected ${formatMetricNumber(result.run?.summary?.selected_retry_count || 0)} retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const runId = `sample-go-drill-recovery-health-alert-retry-worker-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: runId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-worker-run",
      run_id: runId,
      dry_run: false,
      retryable_count: 1,
      selected_retry_count: 1,
      recovery_escalation_retry_health_alert_delivery_retry_worker_run: {
        run_id: runId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        dry_run: false,
        summary: { retryable_count: 1, selected_retry_count: 1, follow_up_action_count: 1 },
        selected_retries: [{ provider, action: "retry", reason: "sample recovery health alert retry" }]
      }
    });
    if (status) status.textContent = `Using local sample recovery health alert retry worker: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function deliverGoDrillRecoveryExecutiveReport() {
  const status = document.querySelector("#goDrillAckStatus");
  const scheduleRun = goRollbackDrillNotificationCatalog.find(
    (item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run"
  );
  const runId = scheduleRun?.run_id || scheduleRun?.session_id || "latest";
  if (status) status.textContent = "Delivering scheduled recovery executive report...";
  try {
    const response = await fetch(apiUrl(`/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-runs/${encodeURIComponent(runId)}/deliver`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        provider: document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook",
        retries: 1,
        timeout_seconds: 10,
        schedule: { interval_minutes: 60, cadence: "hourly", enabled: true }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "executive report delivery API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Executive report delivery ${result.success ? "succeeded" : "recorded with failures"}.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const deliveryId = `sample-go-drill-recovery-executive-delivery-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: deliveryId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "release-connector-delivery",
      connector_delivery_source: "go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report",
      run_id: runId,
      delivery_success: false,
      providers: ["webhook"],
      failed_providers: ["webhook"]
    });
    if (status) status.textContent = `Using local sample executive delivery: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function planGoDrillRecoveryExecutiveDeliveryRetry() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Planning executive report delivery retry...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "executive report delivery retry plan API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Planned ${formatMetricNumber(result.plan?.retryable_count || 0)} executive delivery retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const retryPlanId = `sample-go-drill-executive-delivery-retry-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: retryPlanId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-plan",
      retry_plan_id: retryPlanId,
      alert_level: "warning",
      retryable_count: 1,
      recovery_executive_report_delivery_retry_plan: {
        retry_plan_id: retryPlanId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        retryable_count: 1,
        waiting_count: 0,
        suppressed_count: 0,
        retry_decisions: [{ provider: "webhook", action: "retry", reason: "sample executive delivery retry" }]
      }
    });
    if (status) status.textContent = `Using local sample executive delivery retry plan: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function runGoDrillRecoveryExecutiveDeliveryRetryWorker() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Running executive report delivery retry worker...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-worker-run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        execute: true,
        provider,
        max_retry_deliveries: 2,
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 },
        schedule: { interval_minutes: 30, cadence: "manual_executive_delivery_retry", enabled: true },
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "executive report delivery retry worker API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Executive delivery retry worker selected ${formatMetricNumber(result.run?.summary?.selected_retry_count || 0)} retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const runId = `sample-go-drill-executive-delivery-retry-worker-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: runId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-worker-run",
      run_id: runId,
      dry_run: false,
      retryable_count: 1,
      selected_retry_count: 1,
      recovery_executive_report_delivery_retry_worker_run: {
        run_id: runId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        dry_run: false,
        summary: { retryable_count: 1, selected_retry_count: 1, follow_up_action_count: 1 },
        selected_retries: [{ provider, action: "retry", reason: "sample executive delivery retry" }]
      }
    });
    if (status) status.textContent = `Using local sample executive delivery retry worker: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function buildGoDrillExecutiveDeliveryRetryHealth() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Building executive delivery retry health report...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health", {
      expected_interval_minutes: 60,
      stale_metadata_minutes: 180,
      generated_by: goDrillAckActor()
    }));
    if (!response.ok) throw new Error(await response.text() || "executive delivery retry health API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Executive retry health ${result.health?.alert_level || "indexed"} with ${formatMetricNumber(result.health?.alert_count || 0)} alerts.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const healthId = `sample-go-drill-executive-delivery-retry-health-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: healthId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health",
      health_id: healthId,
      alert_level: "warning",
      alert_count: 1,
      recovery_executive_report_delivery_retry_health: {
        health_id: healthId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        alert_level: "warning",
        alert_count: 1,
        retry_plan_count: 1,
        worker_run_count: 1,
        execution_record_count: 1,
        alerts: [{ severity: "warning", category: "sample_executive_retry_health", message: "Sample executive delivery retry health report." }]
      }
    });
    if (status) status.textContent = `Using local sample executive retry health: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function sendGoDrillExecutiveDeliveryRetryHealthAlert() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Sending executive delivery retry health alert...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/deliver"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        provider,
        force: true,
        expected_interval_minutes: 60,
        stale_metadata_minutes: 180,
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "executive delivery retry health alert API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Executive retry health alert ${result.plan?.plan_id || ""} selected ${formatMetricNumber(result.plan?.selected_providers?.length || 0)} destinations.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const healthId = `sample-go-drill-executive-delivery-retry-health-${Date.now()}`;
    const planId = `sample-go-drill-executive-delivery-retry-health-alert-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: planId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-plan",
      plan_id: planId,
      health_id: healthId,
      alert_level: "warning",
      selected_providers: [provider],
      acknowledgement_required_providers: [provider],
      recovery_executive_report_delivery_retry_health_alert_plan: {
        plan_id: planId,
        health_id: healthId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        alert_level: "warning",
        selected_providers: [provider],
        acknowledgement_required_providers: [provider],
        summary: { alert_count: 1, retryable_count: 1, failed_execution_count: 1 }
      }
    });
    if (status) status.textContent = `Using local sample executive retry health alert: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function planGoDrillExecutiveRetryHealthAlertRetry() {
  const status = document.querySelector("#goDrillAckStatus");
  if (status) status.textContent = "Planning executive retry health alert redelivery...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 }
      })
    });
    if (!response.ok) throw new Error(await response.text() || "executive retry health alert retry plan API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Planned ${formatMetricNumber(result.plan?.retryable_count || 0)} executive health alert retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const retryPlanId = `sample-go-drill-executive-health-alert-retry-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: retryPlanId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-plan",
      retry_plan_id: retryPlanId,
      alert_level: "warning",
      retryable_count: 1,
      recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan: {
        retry_plan_id: retryPlanId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        retryable_count: 1,
        waiting_count: 0,
        suppressed_count: 0,
        retry_decisions: [{ provider: "webhook", action: "retry", reason: "sample executive health alert retry" }]
      }
    });
    if (status) status.textContent = `Using local sample executive health alert retry plan: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function runGoDrillExecutiveRetryHealthAlertRetryWorker() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Running executive retry health alert retry worker...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-worker-run"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        execute: true,
        provider,
        max_retry_deliveries: 2,
        retry_policy: { max_retry_attempts: 3, retry_delay_minutes: 0, allow_immediate_retry: true, backoff_multiplier: 2 },
        schedule: { interval_minutes: 30, cadence: "manual_executive_health_alert_retry", enabled: true },
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "executive health alert retry worker API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Executive health alert retry worker selected ${formatMetricNumber(result.run?.summary?.selected_retry_count || 0)} retries.`;
  } catch (error) {
    const generatedAt = new Date().toISOString();
    const runId = `sample-go-drill-executive-health-alert-retry-worker-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: runId,
      created_at: generatedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health-alert-delivery-retry-worker-run",
      run_id: runId,
      dry_run: false,
      retryable_count: 1,
      selected_retry_count: 1,
      recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run: {
        run_id: runId,
        generated_at: generatedAt,
        generated_by: goDrillAckActor(),
        dry_run: false,
        summary: { retryable_count: 1, selected_retry_count: 1, follow_up_action_count: 1 },
        selected_retries: [{ provider, action: "retry", reason: "sample executive health alert retry" }]
      }
    });
    if (status) status.textContent = `Using local sample executive health alert retry worker: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function showGoDrillFinalReportingClosureDashboard() {
  const status = document.querySelector("#goDrillAckStatus");
  const panel = document.querySelector("#goDrillNotificationDetail");
  if (status) status.textContent = "Loading final reporting closure dashboard...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closure-dashboard"));
    if (!response.ok) throw new Error(await response.text() || "final reporting closure dashboard API unavailable");
    const dashboard = await response.json();
    if (panel) {
      panel.innerHTML = `
        <dl>
          <dt>Closure</dt><dd class="${dashboard.closure_state === "closed" ? "allow" : "block"}">${escapeHtml(dashboard.closure_state || "unknown")}</dd>
          <dt>Open Items</dt><dd>${formatMetricNumber(dashboard.open_item_count || 0)}</dd>
          <dt>Alert Level</dt><dd class="${escapeHtml(statusClass(dashboard.alert_level))}">${escapeHtml(dashboard.alert_level || "unknown")}</dd>
        </dl>
        <pre>${escapeHtml(JSON.stringify(dashboard, null, 2))}</pre>
      `;
    }
    if (status) status.textContent = `Final reporting closure is ${dashboard.closure_state || "unknown"} with ${formatMetricNumber(dashboard.open_item_count || 0)} open items.`;
  } catch (error) {
    const dashboard = {
      schema_version: "cavra.go-backend-pilot.rollback-drill-final-reporting-closure-dashboard.sample.v1",
      product: "CAVRA",
      generated_at: new Date().toISOString(),
      closure_state: "open",
      alert_level: "warning",
      open_item_count: 1,
      open_items: ["sample_final_reporting_closure_pending"],
      summary: buildSampleGoDrillNotificationDashboard(goRollbackDrillNotificationCatalog)
    };
    if (panel) {
      panel.innerHTML = `
        <dl>
          <dt>Closure</dt><dd class="require_approval">${escapeHtml(dashboard.closure_state)}</dd>
          <dt>Open Items</dt><dd>${formatMetricNumber(dashboard.open_item_count)}</dd>
          <dt>Source</dt><dd>local sample</dd>
        </dl>
        <pre>${escapeHtml(JSON.stringify(dashboard, null, 2))}</pre>
      `;
    }
    if (status) status.textContent = `Using local sample final closure dashboard: ${error.message || "API unavailable"}.`;
  }
}

function addSampleGoDrillAckAuditWorkerHealthAlert() {
  const generatedAt = new Date().toISOString();
  const retryPlan = latestGoDrillRetryPlan() || addSampleGoDrillAckAuditRetryPlan();
  const healthId = `sample-go-drill-ack-health-${Date.now()}`;
  const planId = `sample-go-drill-ack-health-alert-${Date.now()}`;
  const healthAlertPlan = {
    schema_version: "cavra.go-backend-pilot.rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan.v1",
    product: "CAVRA",
    plan_id: planId,
    health_id: healthId,
    generated_at: generatedAt,
    generated_by: goDrillAckActor(),
    alert_level: Number(retryPlan.retryable_count || 0) ? "warning" : "healthy",
    summary: {
      run_count: goRollbackDrillNotificationCatalog.filter((item) => item.metadata_kind === "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run").length,
      retryable_count: retryPlan.retryable_count || 0,
      missed_run_count: 0,
      failed_job_count: 0,
      alert_count: Number(retryPlan.retryable_count || 0) ? 1 : 0
    },
    requested_provider: "webhook",
    eligible_providers: ["webhook"],
    selected_providers: Number(retryPlan.retryable_count || 0) ? ["webhook"] : [],
    suppressed_providers: [],
    acknowledgement_required_providers: Number(retryPlan.retryable_count || 0) ? ["webhook"] : [],
    controls: ["sample-public-safe-acknowledgement-audit-worker-health-alert"]
  };
  goRollbackDrillNotificationCatalog.unshift({
    session_id: planId,
    created_at: generatedAt,
    signer: healthAlertPlan.generated_by,
    metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan",
    plan_id: planId,
    health_id: healthId,
    alert_level: healthAlertPlan.alert_level,
    selected_providers: healthAlertPlan.selected_providers,
    acknowledgement_required_providers: healthAlertPlan.acknowledgement_required_providers,
    worker_health_alert_plan: healthAlertPlan
  });
  return healthAlertPlan;
}

async function sendGoDrillAckAuditWorkerHealthAlert() {
  const status = document.querySelector("#goDrillAckStatus");
  const provider = document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Sending acknowledgement audit worker health alert...";
  try {
    const response = await fetch(apiUrl("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        generated_by: goDrillAckActor(),
        provider,
        force: true,
        expected_interval_minutes: 30,
        stale_metadata_minutes: 120,
        retries: 0,
        timeout_seconds: 0.1
      })
    });
    if (!response.ok) throw new Error(await response.text() || "acknowledgement audit worker health alert API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Worker health alert ${result.plan?.plan_id || ""} selected ${formatMetricNumber(result.plan?.selected_providers?.length || 0)} destinations.`;
  } catch (error) {
    const plan = addSampleGoDrillAckAuditWorkerHealthAlert();
    if (status) status.textContent = `Using local sample worker health alert ${plan.plan_id}: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

async function acknowledgeGoDrillAckAuditRetry() {
  const status = document.querySelector("#goDrillAckStatus");
  const retryPlan = latestGoDrillRetryPlan() || addSampleGoDrillAckAuditRetryPlan();
  const decision = (retryPlan.retry_decisions || [])[0] || {};
  const provider = decision.provider || document.querySelector("#goDrillAckAuditDeliveryProvider")?.value || "webhook";
  if (status) status.textContent = "Acknowledging acknowledgement audit retry decision...";
  try {
    const response = await fetch(apiUrl(`/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plans/${encodeURIComponent(retryPlan.retry_plan_id)}/acknowledgements`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        provider,
        acknowledged_by: goDrillAckActor(),
        acknowledgement_state: "accepted",
        delivery_id: decision.delivery_id || "",
        audit_id: decision.audit_id || "",
        external_ref: document.querySelector("#goDrillAckExternalRef")?.value || "",
        notes: document.querySelector("#goDrillAckNotes")?.value || ""
      })
    });
    if (!response.ok) throw new Error(await response.text() || "acknowledgement audit retry acknowledgement API unavailable");
    const result = await response.json();
    if (status) status.textContent = `Acknowledged retry decision ${result.acknowledgement?.acknowledgement_id || ""}.`;
  } catch (error) {
    const acknowledgedAt = new Date().toISOString();
    const acknowledgementId = `sample-go-drill-ack-retry-ack-${Date.now()}`;
    goRollbackDrillNotificationCatalog.unshift({
      session_id: acknowledgementId,
      created_at: acknowledgedAt,
      signer: goDrillAckActor(),
      metadata_kind: "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-ack",
      acknowledgement_id: acknowledgementId,
      retry_plan_id: retryPlan.retry_plan_id,
      delivery_id: decision.delivery_id || "",
      audit_id: decision.audit_id || "",
      provider,
      acknowledgement_state: "accepted",
      acknowledgement: {
        acknowledgement_id: acknowledgementId,
        retry_plan_id: retryPlan.retry_plan_id,
        provider,
        acknowledgement_state: "accepted",
        acknowledged_by: goDrillAckActor(),
        acknowledged_at: acknowledgedAt
      }
    });
    if (status) status.textContent = `Using local sample retry acknowledgement: ${error.message || "API unavailable"}.`;
  }
  await refreshGoRollbackDrillNotifications();
}

function renderReleaseChannelPublishing(promotions, exports, dashboard) {
  const promotionRows = document.querySelector("#releaseChannelRows");
  const exportRows = document.querySelector("#endpointExportRows");
  const panel = document.querySelector("#releaseChannelDashboard");
  if (!promotionRows || !exportRows || !panel) return;
  promotionRows.innerHTML = "";
  exportRows.innerHTML = "";
  panel.innerHTML = `
    <div class="release-delivery-metric">
      <span>Status</span>
      <strong class="${riskClass(dashboard.alert_level)}">${escapeHtml(dashboard.alert_level || "unknown")}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Promotions</span>
      <strong>${formatMetricNumber(promotions.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Exports</span>
      <strong>${formatMetricNumber(dashboard.total_exports || exports.length)}</strong>
    </div>
    <div class="release-delivery-metric">
      <span>Pending</span>
      <strong class="${Number(dashboard.pending_approval_exports || 0) ? "require_approval" : "allow"}">${formatMetricNumber(dashboard.pending_approval_exports)}</strong>
    </div>
    <div class="release-delivery-alerts">
      <strong>Providers</strong>
      <ul>${Object.entries(dashboard.providers || {}).map(([provider, count]) => `<li>${escapeHtml(provider)}: ${formatMetricNumber(count)}</li>`).join("") || "<li>No endpoint exports indexed yet.</li>"}</ul>
    </div>
  `;
  for (const item of promotions) {
    promotionRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.request_id || item.session_id || "request")}</td>
        <td>${escapeHtml(item.channel || "unknown")}</td>
        <td>${escapeHtml(item.target_ring || "unknown")}</td>
        <td class="${item.approval_state === "approved" ? "allow" : "require_approval"}">${escapeHtml(item.approval_id || "required")} / ${escapeHtml(item.approval_state || "pending")}</td>
        <td>${escapeHtml(formatList(item.deployment_targets))}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
  for (const item of exports) {
    exportRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.export_id || item.session_id || "export")}</td>
        <td>${escapeHtml(item.channel || "unknown")}</td>
        <td>${escapeHtml(formatList(item.providers))}</td>
        <td class="${item.approval_state === "approved" ? "allow" : "require_approval"}">${escapeHtml(item.approval_id || "required")} / ${escapeHtml(item.approval_state || "pending")}</td>
        <td>${Number((item.files || []).length)}</td>
        <td>${escapeHtml(String(item.created_at || "").slice(0, 19))}</td>
        <td><button class="endpointExportArtifactAction secondary" data-export="${escapeHtml(item.export_id || item.session_id || "")}">Artifacts</button></td>
      </tr>
    `);
  }
}

function renderEndpointExportArtifacts(payload) {
  const panel = document.querySelector("#endpointExportArtifacts");
  if (!panel) return;
  const artifacts = Array.isArray(payload.artifacts) ? payload.artifacts : [];
  const integrity = payload.endpoint_management_export_integrity || {};
  const readiness = payload.download_readiness || {};
  const bundleHref = payload.bundle_download_url ? apiUrl(payload.bundle_download_url) : "";
  panel.innerHTML = `
    <dl>
      <dt>Export</dt><dd>${escapeHtml(payload.session_id || "unknown")}</dd>
      <dt>Artifact root</dt><dd class="${payload.artifact_root_configured ? "allow" : "require_approval"}">${payload.artifact_root_configured ? "configured" : "sample or disabled"}</dd>
      <dt>Integrity</dt><dd class="${escapeHtml(statusClass(integrity.status))}">${escapeHtml(integrity.status || "unknown")}</dd>
      <dt>Readiness</dt><dd class="${escapeHtml(statusClass(readiness.status))}">${escapeHtml(readiness.status || "blocked")}</dd>
      <dt>Bundle</dt><dd>${bundleHref ? `<a href="${escapeHtml(bundleHref)}">Download bundle</a>` : "not available from sample data"}</dd>
      <dt>Rationale</dt><dd>${escapeHtml(readiness.rationale || "Verify endpoint-management export checksums before download.")}</dd>
    </dl>
    <h3>Integrity</h3>
    <ul>
      <li>Verified: ${escapeHtml(formatList(integrity.verified_artifacts))}</li>
      <li>Missing: ${escapeHtml(formatList(integrity.missing_artifacts))}</li>
      <li>Unchecked: ${escapeHtml(formatList(integrity.unchecked_artifacts))}</li>
      <li>Mismatched: ${escapeHtml(formatList(integrity.checksum_mismatches))}</li>
    </ul>
    <h3>Bundle Files</h3>
    <ul>${artifacts.map((item) => {
      const href = item.download_url ? apiUrl(item.download_url) : "";
      const label = `${item.artifact} (${item.kind || item.media_type || "artifact"})`;
      const suffix = item.bytes ? ` - ${Number(item.bytes)} bytes` : "";
      return `<li>${href ? `<a href="${escapeHtml(href)}">${escapeHtml(label)}</a>` : escapeHtml(label)}${escapeHtml(suffix)}<br><small>${escapeHtml(item.description || "")}</small></li>`;
    }).join("") || "<li>No endpoint export artifacts available.</li>"}</ul>
  `;
}

function sampleEndpointManagementExportDashboard(items) {
  const providers = {};
  const channels = {};
  let pending = 0;
  let files = 0;
  for (const item of items) {
    for (const provider of item.providers || []) providers[provider] = Number(providers[provider] || 0) + 1;
    channels[item.channel || "unknown"] = Number(channels[item.channel || "unknown"] || 0) + 1;
    files += (item.files || []).length;
    if (item.approval_state !== "approved") pending += 1;
  }
  return {
    schema_version: "cavra.endpoint_management.export_dashboard.v1",
    product: "CAVRA",
    total_exports: items.length,
    pending_approval_exports: pending,
    total_files: files,
    providers,
    channels,
    alert_level: pending ? "warning" : "healthy",
    latest: items.slice(0, 10)
  };
}

function sampleEndpointPublicationDashboard(items) {
  const failed = items.filter((item) => !item.delivery_success);
  return {
    schema_version: "cavra.endpoint_management.publication_dashboard.v1",
    product: "CAVRA",
    alert_level: failed.length ? "warning" : "healthy",
    total_publications: items.length,
    successful_publications: items.length - failed.length,
    failed_publications: failed.length,
    success_rate: items.length ? (items.length - failed.length) / items.length : 0,
    providers: [],
    alerts: failed.map((item) => ({
      severity: "warning",
      event_id: item.event_id,
      export_id: item.export_id,
      failed_providers: item.failed_providers || [],
      message: `Endpoint publication failed for ${item.export_id}.`
    })),
    latest: items.slice(0, 10)
  };
}

function sampleEndpointReconciliationDashboard(items) {
  const drifted = items.reduce((total, item) => total + Number(item.drifted_endpoint_count || 0), 0);
  const missing = items.reduce((total, item) => total + Number(item.missing_target_count || 0), 0);
  const stale = items.reduce((total, item) => total + Number(item.stale_endpoint_count || 0), 0);
  const compliant = items.reduce((total, item) => total + Number(item.compliant_endpoint_count || 0), 0);
  const alerts = items
    .filter((item) => item.alert_level === "critical" || item.alert_level === "warning")
    .map((item) => ({
      severity: item.alert_level,
      reconciliation_id: item.reconciliation_id,
      message: `Endpoint reconciliation found ${Number(item.drifted_endpoint_count || 0)} drifted endpoints and ${Number(item.missing_target_count || 0)} missing targets.`
    }));
  return {
    schema_version: "cavra.endpoint_reconciliation.dashboard.v1",
    product: "CAVRA",
    alert_level: alerts.some((item) => item.severity === "critical") ? "critical" : alerts.length ? "warning" : "healthy",
    total_reconciliations: items.length,
    compliant_endpoint_count: compliant,
    drifted_endpoint_count: drifted,
    missing_target_count: missing,
    stale_endpoint_count: stale,
    alerts,
    latest: items.slice(0, 10)
  };
}

function sampleEndpointInventoryDashboard(items) {
  const providerMap = new Map();
  for (const item of items) {
    const provider = item.provider || "unknown";
    const current = providerMap.get(provider) || { provider, ingestions: 0, endpoint_count: 0, missing_target_count: 0 };
    current.ingestions += 1;
    current.endpoint_count += Number(item.endpoint_count || 0);
    current.missing_target_count += Number(item.missing_target_count || 0);
    providerMap.set(provider, current);
  }
  const missing = items.reduce((total, item) => total + Number(item.missing_target_count || 0), 0);
  return {
    schema_version: "cavra.endpoint_inventory_ingestion.dashboard.v1",
    product: "CAVRA",
    alert_level: missing ? "warning" : "healthy",
    total_ingestions: items.length,
    endpoint_count: items.reduce((total, item) => total + Number(item.endpoint_count || 0), 0),
    missing_target_count: missing,
    providers: Array.from(providerMap.values()).sort((a, b) => a.provider.localeCompare(b.provider)),
    latest: items.slice(0, 10)
  };
}

function sampleEndpointInventoryFreshnessDashboard(items) {
  const alerts = items.flatMap((item) => Array.isArray(item.alerts) ? item.alerts : []);
  const critical = items.reduce((total, item) => total + Number(item.critical_count || 0), 0);
  const warning = items.reduce((total, item) => total + Number(item.warning_count || 0), 0);
  return {
    schema_version: "cavra.endpoint_inventory_freshness.dashboard.v1",
    product: "CAVRA",
    alert_level: critical ? "critical" : warning ? "warning" : "healthy",
    report_count: items.length,
    warning_count: warning,
    critical_count: critical,
    alert_count: alerts.length,
    alerts,
    latest: items.slice(0, 10)
  };
}

function sampleEndpointRemediationDashboard(items) {
  const requests = items.filter((item) => item.metadata_kind === "endpoint-drift-remediation-request");
  const executions = items.filter((item) => item.metadata_kind === "endpoint-drift-remediation-execution");
  const pending = requests.filter((item) => item.approval_state === "pending");
  return {
    schema_version: "cavra.endpoint_drift_remediation.dashboard.v1",
    product: "CAVRA",
    alert_level: pending.length ? "critical" : requests.length && !executions.length ? "warning" : "healthy",
    request_count: requests.length,
    execution_count: executions.length,
    pending_approval_count: pending.length,
    approved_execution_count: executions.filter((item) => item.approval_state === "approved").length,
    planned_action_count: requests.reduce((total, item) => total + Number(item.action_count || 0), 0),
    latest: items.slice(0, 10)
  };
}

function sampleEndpointRemediationHandoffDashboard(items) {
  const providers = {};
  for (const item of items) {
    for (const provider of item.providers || []) {
      providers[provider] = (providers[provider] || 0) + 1;
    }
  }
  const pending = items.filter((item) => item.approval_state === "pending");
  return {
    schema_version: "cavra.endpoint_remediation_handoff.dashboard.v1",
    product: "CAVRA",
    alert_level: pending.length ? "warning" : "healthy",
    handoff_count: items.length,
    pending_approval_count: pending.length,
    provider_count: Object.keys(providers).length,
    action_count: items.reduce((total, item) => total + Number(item.action_count || 0), 0),
    providers,
    latest: items.slice(0, 10)
  };
}

function sampleEndpointRemediationHandoffStatusDashboard(items) {
  const providers = {};
  const statuses = {};
  const latest = {};
  for (const item of items) {
    providers[item.provider] = (providers[item.provider] || 0) + 1;
    statuses[item.handoff_status] = (statuses[item.handoff_status] || 0) + 1;
    latest[`${item.handoff_id}:${item.provider}`] = item;
  }
  const latestItems = Object.values(latest);
  const blocked = latestItems.filter((item) => item.handoff_status === "blocked");
  const failed = latestItems.filter((item) => item.handoff_status === "failed");
  const inProgress = latestItems.filter((item) => ["queued", "delivered", "acknowledged", "in_progress"].includes(item.handoff_status));
  return {
    schema_version: "cavra.endpoint_remediation_handoff_status.dashboard.v1",
    product: "CAVRA",
    alert_level: blocked.length || failed.length ? "critical" : inProgress.length ? "warning" : "healthy",
    status_event_count: items.length,
    tracked_handoff_provider_count: latestItems.length,
    completed_count: latestItems.filter((item) => item.handoff_status === "completed").length,
    in_progress_count: inProgress.length,
    blocked_count: blocked.length,
    failed_count: failed.length,
    provider_count: Object.keys(providers).length,
    providers,
    statuses,
    latest: items.slice(0, 10)
  };
}

function sampleEndpointRemediationSlaDashboard(items) {
  const latest = items[0] || {};
  return {
    schema_version: "cavra.endpoint_remediation_sla_report.dashboard.v1",
    product: "CAVRA",
    alert_level: latest.alert_level || "healthy",
    report_count: items.length,
    critical_report_count: items.filter((item) => item.alert_level === "critical").length,
    warning_report_count: items.filter((item) => item.alert_level === "warning").length,
    latest_report_id: latest.report_id,
    tracked_work_item_count: latest.tracked_work_item_count || 0,
    completed_count: latest.completed_count || 0,
    at_risk_count: latest.at_risk_count || 0,
    breached_count: latest.breached_count || 0,
    completion_rate: latest.completion_rate || 0,
    escalation_count: latest.escalation_count || 0,
    latest: items.slice(0, 10)
  };
}

function sampleReleaseConnectorDashboard(items) {
  const failed = items.filter((item) => !item.delivery_success);
  const alerts = failed.map((item) => ({
    severity: item.event_type === "cavra.rollout_rollback_execution" ? "critical" : "warning",
    event_id: item.event_id,
    event_type: item.event_type,
    failed_providers: item.failed_providers || [],
    message: `Release connector delivery failed for ${item.event_id}.`
  }));
  return {
    schema_version: "cavra.release.connector_delivery_dashboard.v1",
    product: "CAVRA",
    alert_level: alerts.some((item) => item.severity === "critical") ? "critical" : alerts.length ? "warning" : "healthy",
    total_deliveries: items.length,
    successful_deliveries: items.length - failed.length,
    failed_deliveries: failed.length,
    success_rate: items.length ? (items.length - failed.length) / items.length : 0,
    alerts
  };
}

function renderActivityRows(sessions, decisions) {
  const sessionRows = document.querySelector("#sessionRows");
  const decisionRows = document.querySelector("#decisionRows");
  sessionRows.innerHTML = "";
  decisionRows.innerHTML = "";
  for (const item of sessions) {
    sessionRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.session_id || "unknown")}</td>
        <td>${escapeHtml(item.repository || "local")}</td>
        <td>${escapeHtml(item.agent_id || "unknown-agent")}</td>
        <td>${item.decision_count || 0}</td>
        <td class="${Number(item.blocked_count || 0) > 0 ? "block" : "allow"}">${item.blocked_count || 0}</td>
        <td class="${Number(item.approval_required_count || 0) > 0 ? "require_approval" : "allow"}">${item.approval_required_count || 0}</td>
        <td>${escapeHtml(String(item.updated_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
  for (const item of decisions) {
    decisionRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.decision_id || "unknown")}</td>
        <td class="${riskClass(item.decision)}">${escapeHtml(item.decision || "audit_only")}</td>
        <td>${escapeHtml(item.action_type || "unknown")}</td>
        <td>${escapeHtml(item.target || "n/a")}</td>
        <td>${escapeHtml(item.rule_id || "runtime.default")}</td>
        <td class="${riskClass(item.severity)}">${escapeHtml(item.severity || "low")}</td>
      </tr>
    `);
  }
}

function renderInventoryRows(repositories, rollouts) {
  const repositoryRows = document.querySelector("#repositoryRows");
  const rolloutRows = document.querySelector("#rolloutRows");
  repositoryRows.innerHTML = "";
  rolloutRows.innerHTML = "";
  for (const item of repositories) {
    const checks = Array.isArray(item.required_checks) && item.required_checks.length ? item.required_checks.join(", ") : "not configured";
    repositoryRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.repository || item.repository_id || "unknown")}</td>
        <td>${escapeHtml(item.owner || "unassigned")}</td>
        <td>${escapeHtml(item.policy_pack || "cavra-ai-agent-baseline")}</td>
        <td class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier || "medium")}</td>
        <td class="${riskClass(item.status)}">${escapeHtml(item.status || "active")}</td>
        <td>${escapeHtml(checks)}</td>
      </tr>
    `);
  }
  for (const item of rollouts) {
    rolloutRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.repository || "unknown")}</td>
        <td>${escapeHtml(item.policy_pack || "n/a")}</td>
        <td class="${riskClass(item.mode)}">${escapeHtml(item.mode || "enforce")}</td>
        <td class="${riskClass(item.state)}">${escapeHtml(item.state || "planned")}</td>
        <td>${Number(item.coverage_percent || 0)}%</td>
        <td>${escapeHtml(item.owner || "platform-security")}</td>
        <td><button class="rolloutDetailAction secondary" data-id="${escapeHtml(item.rollout_id || "")}">Details</button></td>
      </tr>
    `);
  }
}

function renderPolicyRolloutDetail(detail) {
  const panel = document.querySelector("#rolloutDetail");
  if (!detail) {
    panel.textContent = "Policy rollout detail is not available.";
    return;
  }
  const rollout = detail.rollout || {};
  const repository = detail.repository || {};
  const policy = detail.policy_pack || {};
  const activity = detail.activity_summary || {};
  const integrations = detail.integration_summary || {};
  const readiness = detail.readiness || {};
  const checks = Array.isArray(readiness.checks) ? readiness.checks : [];
  const recent = Array.isArray(activity.recent_decisions) ? activity.recent_decisions : [];
  panel.innerHTML = `
    <dl>
      <dt>Rollout</dt><dd>${escapeHtml(rollout.rollout_id || "unknown")}</dd>
      <dt>Repository</dt><dd>${escapeHtml(rollout.repository || repository.repository || "unknown")}</dd>
      <dt>Policy</dt><dd>${escapeHtml(policy.title || rollout.policy_pack || "unknown")} ${escapeHtml(policy.version || rollout.policy_version || "")}</dd>
      <dt>Mode</dt><dd class="${riskClass(rollout.mode)}">${escapeHtml(rollout.mode || "enforce")}</dd>
      <dt>State</dt><dd class="${riskClass(rollout.state)}">${escapeHtml(rollout.state || "planned")}</dd>
      <dt>Coverage</dt><dd>${Number(rollout.coverage_percent || 0)}%</dd>
      <dt>Repository owner</dt><dd>${escapeHtml(repository.owner || rollout.owner || "unassigned")}</dd>
      <dt>Activity</dt><dd>${Number(activity.total || 0)} matching decisions</dd>
      <dt>Integrations</dt><dd>${Number(integrations.total || 0)} inventoried</dd>
      <dt>Readiness</dt><dd class="${readiness.status === "ready" ? "allow" : "require_approval"}">${escapeHtml(readiness.status || "needs_attention")}</dd>
    </dl>
    <h3>Rule Summary</h3>
    <ul>${Object.entries(policy.rule_summary || {}).map(([key, value]) => `<li>${escapeHtml(key)}: ${Number(value || 0)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Readiness Checks</h3>
    <ul>${checks.map((item) => `<li><strong class="${item.status === "pass" ? "allow" : "require_approval"}">${escapeHtml(item.status)}</strong> ${escapeHtml(item.message || item.id)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Recent Decisions</h3>
    <ul>${recent.map((item) => `<li><strong class="${riskClass(item.decision)}">${escapeHtml(item.decision)}</strong> ${escapeHtml(item.target || item.decision_id || "unknown")}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderPolicyCatalog(items) {
  const panel = document.querySelector("#policyCatalog");
  panel.innerHTML = `
    <h3>Policy Catalog</h3>
    <ul>${items.map((item) => `<li><strong>${escapeHtml(item.id)}</strong> ${escapeHtml(item.version || "latest")}<br><small>${escapeHtml(item.title || item.description || "")}</small></li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderPolicyDraft(draft) {
  const panel = document.querySelector("#policyDraft");
  const counts = draft.summary?.rule_counts || {};
  const errors = Array.isArray(draft.errors) ? draft.errors : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${draft.valid ? "allow" : "block"}">${draft.valid ? "valid" : "invalid"}</dd>
      <dt>Policy</dt><dd>${escapeHtml(draft.summary?.policy_id || draft.policy_pack?.metadata?.id || "unknown")}</dd>
      <dt>Version</dt><dd>${escapeHtml(draft.summary?.version || "n/a")}</dd>
      <dt>Inherits</dt><dd>${escapeHtml(draft.summary?.inherits || "none")}</dd>
    </dl>
    <h3>Rule Counts</h3>
    <ul>${Object.entries(counts).map(([key, value]) => `<li>${escapeHtml(key)}: ${Number(value || 0)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Validation</h3>
    <ul>${errors.map((item) => `<li class="block">${escapeHtml(item)}</li>`).join("") || "<li class=\"allow\">No schema errors</li>"}</ul>
  `;
}

function renderPolicyPublishPlan(plan, approval) {
  const panel = document.querySelector("#policyPublishPlan");
  const diff = plan.diff || {};
  const notes = Array.isArray(plan.operator_notes) ? plan.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${plan.valid ? "allow" : "block"}">${plan.valid ? "ready for approval" : "invalid"}</dd>
      <dt>Operation</dt><dd>${escapeHtml(plan.operation || "create")}</dd>
      <dt>Risk</dt><dd class="${riskClass(plan.risk)}">${escapeHtml(plan.risk || "high")}</dd>
      <dt>Approval</dt><dd class="require_approval">${approval ? escapeHtml(`${approval.state || "pending"} ${approval.approval_id || ""}`) : "required"}</dd>
      <dt>Policy</dt><dd>${escapeHtml(plan.policy_id || "unknown")}</dd>
      <dt>Digest</dt><dd>${escapeHtml(plan.policy_digest || "n/a")}</dd>
      <dt>Target</dt><dd>${escapeHtml(plan.target_path || "policies/.../policy.yaml")}</dd>
    </dl>
    <h3>Policy Diff</h3>
    <ul>
      <li>Added: ${Number(diff.added?.length || 0)}</li>
      <li>Changed: ${Number(diff.changed?.length || 0)}</li>
      <li>Removed: ${Number(diff.removed?.length || 0)}</li>
    </ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderPolicyPublishResult(result) {
  const panel = document.querySelector("#policyPublishPlan");
  const notes = Array.isArray(result.operator_notes) ? result.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${result.status === "published" ? "allow" : "require_approval"}">${escapeHtml(result.status || "approval_required")}</dd>
      <dt>Policy</dt><dd>${escapeHtml(result.policy_id || "unknown")}</dd>
      <dt>Digest</dt><dd>${escapeHtml(result.policy_digest || "n/a")}</dd>
      <dt>Approval</dt><dd>${escapeHtml(result.approval?.approval_id || "n/a")} ${escapeHtml(result.approval?.state || "")}</dd>
      <dt>Signature</dt><dd class="${result.signature_verified ? "allow" : "require_approval"}">${result.signature_verified ? "verified" : "pending"}</dd>
      <dt>Policy path</dt><dd>${escapeHtml(result.policy_path || "not written")}</dd>
    </dl>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderRolloutChangePlan(plan, applied) {
  const panel = document.querySelector("#rolloutChangePlan");
  const changes = Array.isArray(plan.changes) ? plan.changes : [];
  const notes = Array.isArray(plan.operator_notes) ? plan.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${applied ? "allow" : "require_approval"}">${applied ? "applied" : "planned"}</dd>
      <dt>Operation</dt><dd>${escapeHtml(plan.operation || "update")}</dd>
      <dt>Risk</dt><dd class="${riskClass(plan.risk)}">${escapeHtml(plan.risk || "medium")}</dd>
      <dt>Approval</dt><dd class="${plan.approval_required ? "require_approval" : "allow"}">${plan.approval_required ? "required" : "not required"}</dd>
      <dt>Repository</dt><dd>${escapeHtml(plan.after?.repository || "unknown")}</dd>
      <dt>Policy</dt><dd>${escapeHtml(plan.after?.policy_pack || "unknown")}</dd>
    </dl>
    <h3>Changes</h3>
    <ul>${changes.map((item) => `<li>${escapeHtml(item.field)}: ${escapeHtml(item.before ?? "n/a")} -> ${escapeHtml(item.after ?? "n/a")}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderIntegrationRows(integrations) {
  const integrationRows = document.querySelector("#integrationRows");
  integrationRows.innerHTML = "";
  for (const item of integrations) {
    const capabilities = Array.isArray(item.capabilities) && item.capabilities.length ? item.capabilities.join(", ") : "not configured";
    integrationRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.name || item.integration_id || item.provider || "unknown")}</td>
        <td>${escapeHtml(item.category || "security")}</td>
        <td class="${riskClass(item.status)}">${escapeHtml(item.status || "planned")}</td>
        <td class="${riskClass(item.health_status)}">${escapeHtml(item.health_status || "not_checked")}</td>
        <td>${escapeHtml(item.owner || "platform-security")}</td>
        <td>${escapeHtml(item.environment || "global")}</td>
        <td>${escapeHtml(capabilities)}</td>
      </tr>
    `);
  }
}

function riskClass(value) {
  if (value === "critical" || value === "high" || value === "blocked" || value === "denied" || value === "strict" || value === "failed" || value === "disabled") return "block";
  if (value === "medium" || value === "warning" || value === "experimental" || value === "pending" || value === "planned" || value === "audit_only" || value === "degraded" || value === "not_checked" || value === "configured") return "require_approval";
  return "allow";
}

function renderRegistryRows(agents, mcpServers, profiles, classifications) {
  const agentRows = document.querySelector("#agentRows");
  const mcpRows = document.querySelector("#mcpRows");
  const profileRows = document.querySelector("#agentProfileRows");
  const classificationRows = document.querySelector("#mcpClassificationRows");
  agentRows.innerHTML = "";
  mcpRows.innerHTML = "";
  profileRows.innerHTML = "";
  classificationRows.innerHTML = "";
  for (const item of agents) {
    const capabilities = Array.isArray(item.capabilities) ? item.capabilities.join(", ") : "";
    agentRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.agent_id || "unknown")}</td>
        <td>${escapeHtml(item.vendor || "unknown")}</td>
        <td>${escapeHtml(item.owner || "unassigned")}</td>
        <td class="${riskClass(item.status)}">${escapeHtml(item.status || "active")}</td>
        <td>${escapeHtml(capabilities || "n/a")}</td>
        <td class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier || "medium")}</td>
      </tr>
    `);
  }
  for (const item of mcpServers) {
    const capabilities = Array.isArray(item.capabilities) ? item.capabilities.join(", ") : "";
    const tools = Array.isArray(item.allowed_tools) && item.allowed_tools.length ? item.allowed_tools.join(", ") : "approval required";
    mcpRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.name || item.server_id || "unknown")}</td>
        <td class="${riskClass(item.trust_tier)}">${escapeHtml(item.trust_tier || "unknown")}</td>
        <td class="${riskClass(item.approval_state)}">${escapeHtml(item.approval_state || "pending")}</td>
        <td>${escapeHtml(capabilities || "n/a")}</td>
        <td>${escapeHtml(tools)}</td>
      </tr>
    `);
  }
  for (const item of profiles.slice(0, 6)) {
    const capabilities = item.default_capabilities || [];
    profileRows.insertAdjacentHTML("beforeend", `
      <article class="profile-item">
        <strong>${escapeHtml(item.display_name || item.profile_id)}</strong>
        <span>${escapeHtml(item.vendor || "unknown")} · <span class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier || "medium")}</span></span>
        <small>${escapeHtml(capabilities.slice(0, 4).join(", "))}</small>
      </article>
    `);
  }
  for (const item of classifications) {
    classificationRows.insertAdjacentHTML("beforeend", `
      <article class="profile-item">
        <strong>${escapeHtml(item.capability)}</strong>
        <span>${escapeHtml(item.category || "tool")} · <span class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier)}</span></span>
        <small>${escapeHtml(item.control_objective || "")}</small>
      </article>
    `);
  }
}

function renderSecurityBoundary(boundary) {
  const panel = document.querySelector("#securityBoundary");
  const oidc = boundary.oidc || {};
  const rbac = boundary.rbac || {};
  const cors = boundary.cors || {};
  const permissions = Array.isArray(boundary.console_permissions) ? boundary.console_permissions : [];
  const notes = Array.isArray(boundary.operator_notes) ? boundary.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Mode</dt><dd class="${boundary.mode === "oidc_rbac_ready" ? "allow" : "require_approval"}">${escapeHtml(boundary.mode || "local_or_demo")}</dd>
      <dt>OIDC</dt><dd class="${oidc.configured ? "allow" : "require_approval"}">${oidc.configured ? "configured" : "disabled"}</dd>
      <dt>RBAC</dt><dd class="${rbac.configured ? "allow" : "require_approval"}">${rbac.configured ? "configured" : "disabled"}</dd>
      <dt>CORS</dt><dd>${cors.configured ? escapeHtml((cors.origins || []).join(", ")) : "same-origin or local demo"}</dd>
      <dt>OIDC env</dt><dd>${escapeHtml(oidc.config_env || "CAVRA_APPROVAL_OIDC_CONFIG")}</dd>
      <dt>RBAC env</dt><dd>${escapeHtml(rbac.config_env || "CAVRA_APPROVAL_RBAC_FILE")}</dd>
    </dl>
    <h3>Console Permissions</h3>
    <ul>${permissions.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderConsoleSession(session) {
  consoleSessionCache = session;
  const panel = document.querySelector("#consoleSession");
  const actor = session.actor || {};
  const permissions = session.permissions || {};
  const repositoryPermissions = Array.isArray(session.repository_permissions) ? session.repository_permissions : [];
  const notes = Array.isArray(session.operator_notes) ? session.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Mode</dt><dd class="${session.authenticated ? "allow" : "require_approval"}">${escapeHtml(session.mode || "local_or_demo")}</dd>
      <dt>Authenticated</dt><dd class="${session.authenticated ? "allow" : "require_approval"}">${session.authenticated ? "yes" : "no"}</dd>
      <dt>Actor</dt><dd>${escapeHtml(actor.actor || "not verified")}</dd>
      <dt>Issuer</dt><dd>${escapeHtml(actor.issuer || "n/a")}</dd>
      <dt>Groups</dt><dd>${escapeHtml((actor.groups || []).join(", ") || "n/a")}</dd>
    </dl>
    <h3>Permissions</h3>
    <ul>${Object.entries(permissions).map(([key, value]) => `<li><strong class="${value ? "allow" : "require_approval"}">${escapeHtml(value ? "allow" : "not allowed")}</strong> ${escapeHtml(key)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Repository Scope</h3>
    <ul>${repositoryPermissions.map((item) => `<li>${escapeHtml(item.repository || "*")} / ${escapeHtml(item.approver_group || "*")} / ${escapeHtml((item.actions || []).join(", "))}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderDeploymentReadiness(report) {
  const panel = document.querySelector("#deploymentReadiness");
  const checks = Array.isArray(report.checks) ? report.checks : [];
  const notes = Array.isArray(report.operator_notes) ? report.operator_notes : [];
  const goPilot = report.go_backend_pilot || {};
  const goDeployment = report.go_backend_deployment || {};
  const goPromotion = report.go_backend_promotion || {};
  const goRollback = report.go_backend_rollback || {};
  const goRehearsal = report.go_backend_rollback_rehearsal || {};
  const goDrills = report.go_backend_rollback_drill_history || {};
  const goDrillSchedule = report.go_backend_rollback_drill_schedule || {};
  const rehearsalEvidence = Array.isArray(goRehearsal.rehearsal?.evidence_refs) ? goRehearsal.rehearsal.evidence_refs : [];
  const drillEvidence = Array.isArray(goDrills.history?.evidence_refs) ? goDrills.history.evidence_refs : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${report.status === "ready" ? "allow" : "require_approval"}">${escapeHtml(report.status || "needs_attention")}</dd>
      <dt>Stores</dt><dd>${Number(report.store_summary?.total || 0)} checked</dd>
      <dt>Missing stores</dt><dd>${escapeHtml((report.store_summary?.missing || []).join(", ") || "none")}</dd>
      <dt>Go pilot</dt><dd class="${goPilot.status === "ready" || goPilot.status === "disabled" ? "allow" : "require_approval"}">${escapeHtml(goPilot.status || "disabled")} (${escapeHtml(goPilot.mode || "disabled")})</dd>
      <dt>Go deployment</dt><dd class="${goDeployment.status === "ready" || goDeployment.status === "not_configured" ? "allow" : "require_approval"}">${escapeHtml(goDeployment.status || "not_configured")}</dd>
      <dt>Go promotion</dt><dd class="${goPromotion.status === "ready" || goPromotion.status === "not_requested" ? "allow" : "require_approval"}">${escapeHtml(goPromotion.status || "not_requested")}</dd>
      <dt>Go rollback</dt><dd class="${goRollback.status === "ready" || goRollback.status === "not_requested" ? "allow" : "require_approval"}">${escapeHtml(goRollback.status || "not_requested")}</dd>
      <dt>Rollback rehearsal</dt><dd class="${goRehearsal.status === "ready" || goRehearsal.status === "not_requested" ? "allow" : "require_approval"}">${escapeHtml(goRehearsal.status || "not_requested")}</dd>
      <dt>Recovery target</dt><dd>${escapeHtml(goRehearsal.rehearsal?.recovery_minutes ? `${goRehearsal.rehearsal.recovery_minutes}m / ${goRehearsal.rehearsal.max_recovery_minutes || "n/a"}m` : "n/a")}</dd>
      <dt>Rehearsal evidence</dt><dd>${escapeHtml(rehearsalEvidence.join(", ") || "n/a")}</dd>
      <dt>Rollback drills</dt><dd class="${goDrills.status === "ready" || goDrills.status === "not_requested" ? "allow" : "require_approval"}">${escapeHtml(goDrills.status || "not_requested")}</dd>
      <dt>Latest drill</dt><dd>${escapeHtml(goDrills.history?.latest_drill_id ? `${goDrills.history.latest_drill_id} / ${goDrills.history.latest_executed_at || "n/a"}` : "n/a")}</dd>
      <dt>Drill evidence</dt><dd>${escapeHtml(drillEvidence.join(", ") || "n/a")}</dd>
      <dt>Drill schedule</dt><dd class="${["ready", "due_soon", "not_requested"].includes(goDrillSchedule.status) ? "allow" : "require_approval"}">${escapeHtml(goDrillSchedule.status || "not_requested")}</dd>
      <dt>Next drill</dt><dd>${escapeHtml(goDrillSchedule.schedule?.next_due_at || "n/a")}</dd>
      <dt>Notify</dt><dd>${escapeHtml((goDrillSchedule.schedule?.notification_providers || []).join(", ") || "n/a")}</dd>
    </dl>
    <h3>Checks</h3>
    <ul>${checks.map((item) => `<li><strong class="${item.status === "pass" ? "allow" : "require_approval"}">${escapeHtml(item.status)}</strong> ${escapeHtml(item.id)}<br><small>${escapeHtml(item.message || "")}</small></li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderApprovalRows(items) {
  const rows = document.querySelector("#approvalRows");
  rows.innerHTML = "";
  for (const item of items) {
    const stateClass = item.state === "break_glass" ? "warn" : item.state === "denied" ? "block" : "allow";
    const detailAction = `<button class="approvalDetailAction secondary" data-id="${escapeHtml(item.approval_id)}">Details</button>`;
    const actions = item.state === "pending"
      ? `<button class="approvalAction" data-action="approve" data-id="${escapeHtml(item.approval_id)}">Approve</button>
         <button class="approvalAction secondary" data-action="deny" data-id="${escapeHtml(item.approval_id)}">Deny</button>
         <button class="approvalAction secondary" data-action="expire" data-id="${escapeHtml(item.approval_id)}">Expire</button>
         ${detailAction}`
      : detailAction;
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.approval_id || "unknown")}</td>
        <td class="${stateClass}">${escapeHtml(item.state || "pending")}</td>
        <td>${escapeHtml(item.approver_group || "Repository Owners")}</td>
        <td>${escapeHtml(item.requested_by || "ai-agent")}</td>
        <td>${escapeHtml(item.decision?.target || item.decision_id || "unknown")}</td>
        <td>${escapeHtml(item.external_ref || "n/a")}</td>
        <td class="row-actions">${actions}</td>
      </tr>
    `);
  }
}

function renderApprovalDetail(item) {
  const panel = document.querySelector("#approvalDetail");
  if (!item) {
    panel.textContent = "Approval record not found.";
    return;
  }
  const history = Array.isArray(item.history) ? item.history : [];
  const evidenceRefs = Array.isArray(item.evidence_refs) ? item.evidence_refs : [];
  panel.innerHTML = `
    <dl>
      <dt>Approval</dt><dd>${escapeHtml(item.approval_id || "unknown")}</dd>
      <dt>State</dt><dd>${escapeHtml(item.state || "pending")}</dd>
      <dt>Approver group</dt><dd>${escapeHtml(item.approver_group || "Repository Owners")}</dd>
      <dt>Requested by</dt><dd>${escapeHtml(item.requested_by || "ai-agent")}</dd>
      <dt>Decided by</dt><dd>${escapeHtml(item.decided_by || "n/a")}</dd>
      <dt>External ref</dt><dd>${escapeHtml(item.external_ref || "n/a")}</dd>
      <dt>Decision target</dt><dd>${escapeHtml(item.decision?.target || item.decision_id || "unknown")}</dd>
      <dt>Rule</dt><dd>${escapeHtml(item.decision?.rule_id || "n/a")}</dd>
      <dt>Reason</dt><dd>${escapeHtml(item.decision_reason || item.break_glass_reason || item.decision?.reason || "n/a")}</dd>
    </dl>
    <h3>Evidence</h3>
    <ul>${evidenceRefs.length ? evidenceRefs.map((ref) => `<li>${escapeHtml(ref)}</li>`).join("") : "<li>n/a</li>"}</ul>
    <h3>History</h3>
    <ul>${history.length ? history.map((event) => `<li><strong>${escapeHtml(event.event || "event")}</strong> ${escapeHtml(event.actor || "unknown")}<br><small>${escapeHtml(event.timestamp || "")}</small><br>${escapeHtml(event.reason || "")}</li>`).join("") : "<li>n/a</li>"}</ul>
  `;
}

async function refreshEvidence() {
  const items = filterEvidence(await loadEvidenceMetadata());
  evidenceMetadataCache = items;
  renderEvidenceRows(items);
}

async function refreshReleaseDelivery() {
  const [items, dashboard] = await Promise.all([loadReleaseConnectorDeliveries(), loadReleaseConnectorDashboard()]);
  renderReleaseConnectorDeliveries(items, dashboard);
}

async function refreshEndpointPublicationDelivery() {
  const [items, dashboard] = await Promise.all([loadEndpointPublicationDeliveries(), loadEndpointPublicationDashboard()]);
  renderEndpointPublicationDeliveries(items, dashboard);
}

async function refreshEndpointInventory() {
  const [items, dashboard] = await Promise.all([loadEndpointInventoryIngestions(), loadEndpointInventoryDashboard()]);
  renderEndpointInventoryIngestions(items, dashboard);
}

async function refreshEndpointInventoryFreshness() {
  const [items, dashboard] = await Promise.all([
    loadEndpointInventoryFreshness(),
    loadEndpointInventoryFreshnessDashboard()
  ]);
  renderEndpointInventoryFreshness(items, dashboard);
}

async function refreshEndpointReconciliation() {
  const [items, dashboard] = await Promise.all([loadEndpointReconciliations(), loadEndpointReconciliationDashboard()]);
  renderEndpointReconciliations(items, dashboard);
}

async function refreshEndpointRemediation() {
  const [items, dashboard] = await Promise.all([loadEndpointRemediations(), loadEndpointRemediationDashboard()]);
  renderEndpointRemediations(items, dashboard);
}

async function refreshEndpointRemediationHandoff() {
  const [items, dashboard] = await Promise.all([
    loadEndpointRemediationHandoffs(),
    loadEndpointRemediationHandoffDashboard()
  ]);
  renderEndpointRemediationHandoffs(items, dashboard);
}

async function refreshEndpointRemediationHandoffStatus() {
  const [items, dashboard] = await Promise.all([
    loadEndpointRemediationHandoffStatuses(),
    loadEndpointRemediationHandoffStatusDashboard()
  ]);
  renderEndpointRemediationHandoffStatuses(items, dashboard);
}

async function refreshEndpointRemediationSla() {
  const [items, dashboard, notificationDashboard, escalationDashboard, escalationActionDashboard, escalationRecurrenceDashboard] = await Promise.all([
    loadEndpointRemediationSlaReports(),
    loadEndpointRemediationSlaDashboard(),
    loadEndpointRemediationSlaNotificationDashboard(),
    loadEndpointRemediationSlaEscalationDashboard(),
    loadEndpointRemediationSlaEscalationActionDashboard(),
    loadEndpointRemediationSlaEscalationRecurrenceDashboard()
  ]);
  renderEndpointRemediationSlaReports(items, dashboard, notificationDashboard, escalationDashboard, escalationActionDashboard, escalationRecurrenceDashboard);
}

async function refreshEndpointRecurrenceOperations() {
  const [
    retryPlans,
    ownerDigests,
    suppressionTrends,
    automationRuns,
    dashboard,
    automationDashboard,
    automationHealth,
    healthAlerts,
    healthAlertDashboard
  ] = await Promise.all([
    loadEndpointRecurrenceRetryPlans(),
    loadEndpointRecurrenceOwnerDigests(),
    loadEndpointRecurrenceSuppressionTrends(),
    loadEndpointRecurrenceAutomations(),
    loadEndpointRemediationSlaEscalationActionDashboard(),
    loadEndpointRecurrenceAutomationDashboard(),
    loadEndpointRecurrenceAutomationHealth(),
    loadEndpointRecurrenceAutomationHealthAlerts(),
    loadEndpointRecurrenceAutomationHealthAlertDashboard()
  ]);
  renderEndpointRecurrenceOperations(
    retryPlans,
    ownerDigests,
    suppressionTrends,
    automationRuns,
    dashboard,
    automationDashboard,
    automationHealth,
    healthAlerts,
    healthAlertDashboard
  );
}

async function refreshGoRollbackDrillNotifications() {
  const [historyItems, dashboard, routingRows, suppressionTrend, retryRecoveryReport] = await Promise.all([
    loadGoRollbackDrillNotificationHistory(),
    loadGoRollbackDrillNotificationDashboard(),
    loadGoRollbackDrillRoutingHistory(),
    loadGoRollbackDrillSuppressionTrend(),
    loadGoRollbackDrillRetryRecoveryReport()
  ]);
  renderGoRollbackDrillNotifications(historyItems, dashboard, routingRows, suppressionTrend, retryRecoveryReport);
}

async function deliverEndpointRemediationSlaNotification() {
  const status = document.querySelector("#endpointRemediationSlaDeliveryStatus");
  if (status) {
    status.textContent = "Delivering SLA notification...";
    status.className = "status-line require_approval";
  }
  const reports = await loadEndpointRemediationSlaReports();
  const report = reports[0];
  if (!report) {
    if (status) {
      status.textContent = "No SLA report is available to notify.";
      status.className = "status-line warn";
    }
    return;
  }
  const reportId = report.report_id || report.session_id;
  try {
    const response = await fetch(apiUrl(`/endpoint-remediation-sla-reports/${encodeURIComponent(reportId)}/deliver`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({ provider: "all", retries: 1, generated_by: "console" })
    });
    if (!response.ok) throw new Error("Endpoint remediation SLA notification API unavailable");
    const result = await response.json();
    if (status) {
      status.textContent = `Notification ${result.success ? "delivered" : "recorded with failures"}: ${result.event_id || reportId}`;
      status.className = `status-line ${result.success ? "ok" : "warn"}`;
    }
    await refreshReleaseDelivery();
  } catch {
    if (status) {
      status.textContent = `Sample notification ready for ${reportId}; configure connectors to deliver.`;
      status.className = "status-line warn";
    }
  }
}

async function refreshReleaseChannels() {
  const [promotions, exports, dashboard] = await Promise.all([
    loadReleaseChannelPromotions(),
    loadEndpointManagementExports(),
    loadEndpointManagementExportDashboard()
  ]);
  renderReleaseChannelPublishing(promotions, exports, dashboard);
}

async function showEndpointExportArtifacts(exportId) {
  renderEndpointExportArtifacts(await loadEndpointManagementExportArtifacts(exportId));
}

async function showEvidenceArtifacts(sessionId) {
  renderEvidenceArtifacts(await loadEvidenceArtifacts(sessionId));
}

async function showPromotionExecutionDetail(executionId) {
  const panel = document.querySelector("#evidenceArtifacts");
  let item = evidenceMetadataCache.find((entry) => entry.session_id === executionId) || evidenceCatalog.find((entry) => entry.session_id === executionId);
  try {
    const response = await fetch(apiUrl(`/promotion-executions/${encodeURIComponent(executionId)}`));
    if (response.ok) item = await response.json();
  } catch {
    // sample metadata is rendered below
  }
  const rollbackRefs = Array.isArray(item?.rollback_evidence_refs) ? item.rollback_evidence_refs : [];
  const auditLinks = item?.audit_links || {};
  let exportEvent = null;
  try {
    const response = await fetch(apiUrl(`/promotion-executions/${encodeURIComponent(executionId)}/audit-export`));
    if (response.ok) exportEvent = (await response.json()).event;
  } catch {
    exportEvent = null;
  }
  panel.innerHTML = `
    <dl>
      <dt>Execution</dt><dd>${escapeHtml(item?.session_id || executionId)}</dd>
      <dt>Rollout</dt><dd>${escapeHtml(item?.rollout_id || "unknown")}</dd>
      <dt>Ring</dt><dd>${escapeHtml(item?.current_ring || "unknown")} -> ${escapeHtml(item?.target_ring || "unknown")}</dd>
      <dt>Status</dt><dd class="ok">${escapeHtml(item?.promotion_execution_status || item?.rollout_status || "executed")}</dd>
      <dt>Approval</dt><dd>${escapeHtml(item?.approval_id || "unknown")} (${escapeHtml(item?.approval_state || "unknown")})</dd>
      <dt>Export</dt><dd>${escapeHtml(exportEvent ? `${exportEvent.event_type} / ${exportEvent.rollback_reference_count} rollback refs` : "SIEM and ITSM payloads available from API/CLI")}</dd>
    </dl>
    <h3>Audit Links</h3>
    <ul>${Object.entries(auditLinks).map(([key, value]) => `<li><strong>${escapeHtml(key)}</strong>: ${escapeHtml(value)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Rollback Evidence</h3>
    <ul>${rollbackRefs.map((ref) => `<li>${escapeHtml(ref.target || "target")}: ${escapeHtml(ref.ref || "")}<br><small>${escapeHtml(ref.step || "")}</small></li>`).join("") || "<li>No rollback evidence links recorded.</li>"}</ul>
  `;
}

async function showRollbackExecutionDetail(rollbackId) {
  const panel = document.querySelector("#evidenceArtifacts");
  let item = evidenceMetadataCache.find((entry) => entry.session_id === rollbackId) || evidenceCatalog.find((entry) => entry.session_id === rollbackId);
  try {
    const response = await fetch(apiUrl(`/rollback-executions/${encodeURIComponent(rollbackId)}`));
    if (response.ok) item = await response.json();
  } catch {
    // sample metadata is rendered below
  }
  const rollbackRefs = Array.isArray(item?.rollback_evidence_refs) ? item.rollback_evidence_refs : [];
  const auditLinks = item?.audit_links || {};
  panel.innerHTML = `
    <dl>
      <dt>Rollback</dt><dd>${escapeHtml(item?.session_id || rollbackId)}</dd>
      <dt>Promotion execution</dt><dd>${escapeHtml(item?.promotion_execution_id || "unknown")}</dd>
      <dt>Rollout</dt><dd>${escapeHtml(item?.rollout_id || "unknown")}</dd>
      <dt>Ring</dt><dd>${escapeHtml(item?.current_ring || "unknown")} -> ${escapeHtml(item?.target_ring || "unknown")}</dd>
      <dt>Status</dt><dd class="ok">${escapeHtml(item?.rollback_execution_status || item?.rollout_status || "executed")}</dd>
      <dt>Approval</dt><dd>${escapeHtml(item?.approval_id || "unknown")} (${escapeHtml(item?.approval_state || "unknown")})</dd>
    </dl>
    <h3>Audit Links</h3>
    <ul>${Object.entries(auditLinks).map(([key, value]) => `<li><strong>${escapeHtml(key)}</strong>: ${escapeHtml(value)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Rollback Evidence</h3>
    <ul>${rollbackRefs.map((ref) => `<li>${escapeHtml(ref.target || "target")}: ${escapeHtml(ref.ref || "")}<br><small>${escapeHtml(ref.step || "")}</small></li>`).join("") || "<li>No rollback evidence links recorded.</li>"}</ul>
  `;
}

async function requestRolloutPromotionApproval(sessionId) {
  const status = document.querySelector("#rolloutPromotionStatus");
  if (status) {
    status.textContent = "Requesting signed promotion approval...";
    status.className = "status-line require_approval";
  }
  try {
    const response = await fetch(apiUrl(`/evidence/${encodeURIComponent(sessionId)}/promotion-request`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        target_ring: "production",
        requested_by: "console",
        approver_group: "Change Advisory Board"
      })
    });
    if (!response.ok) throw new Error("Promotion approval API unavailable");
    const result = await response.json();
    if (result.request) rolloutPromotionRequests.set(sessionId, result.request);
    if (status) {
      status.textContent = `Signed promotion approval requested: ${result.approval?.approval_id || "pending"}`;
      status.className = "status-line ok";
    }
    if (result.approval) renderApprovalDetail(result.approval);
  } catch {
    const approval = {
      schema_version: "cavra.approval.v1",
      product: "CAVRA",
      approval_id: `apr_rollout_${Date.now()}`,
      decision_id: `rpr_${Date.now()}:decision`,
      session_id: sessionId,
      state: "pending",
      approver_group: "Change Advisory Board",
      requested_by: "console",
      requested_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      decision: {
        action_type: "release_promote_endpoint_rollout",
        target: `${sessionId}->production`,
        decision: "require_approval",
        rule_id: "release.rollout.promotion.require_approval",
        reason: "Managed endpoint rollout promotion requires signed approval."
      },
      evidence_refs: [`approval://rollout/${Date.now()}`, `evidence://${sessionId}/managed-endpoint-rollout-evidence.json`],
      history: [{ event: "requested", actor: "console", timestamp: new Date().toISOString(), reason: "Sample signed promotion request." }]
    };
    rolloutPromotionRequests.set(sessionId, {
      schema_version: "cavra.go-runtime.endpoint-rollout-promotion-request.v1",
      request_id: approval.decision_id.replace(":decision", ""),
      rollout_id: sessionId,
      current_ring: "pilot",
      target_ring: "production",
      rollout_status: "staged",
      change_record: "CHG-123",
      release: { version: "v0.2.0-rc.1" },
      deployment_targets: ["github-actions-linux-amd64-runner"],
      approval
    });
    approvalCatalog.unshift(approval);
    if (status) {
      status.textContent = `Sample promotion approval requested: ${approval.approval_id}`;
      status.className = "status-line ok";
    }
    renderApprovalDetail(approval);
  }
  await refreshApprovals();
}

async function recordRolloutPromotionExecution(sessionId) {
  const status = document.querySelector("#rolloutPromotionStatus");
  const request = rolloutPromotionRequests.get(sessionId);
  if (status) {
    status.textContent = "Recording approved promotion execution...";
    status.className = "status-line require_approval";
  }
  try {
    if (!request) throw new Error("Promotion request is required before execution");
    const response = await fetch(apiUrl(`/evidence/${encodeURIComponent(sessionId)}/promotion-execution`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({
        request,
        approval_id: request.approval?.approval_id,
        executed_by: "console"
      })
    });
    if (!response.ok) throw new Error("Promotion execution API unavailable");
    const result = await response.json();
    if (status) {
      status.textContent = `Promotion execution recorded: ${result.execution?.execution_id || "recorded"}`;
      status.className = "status-line ok";
    }
  } catch {
    if (status) {
      status.textContent = `Sample promotion execution recorded for ${sessionId}`;
      status.className = "status-line ok";
    }
  }
}

async function refreshActivity() {
  const [sessions, decisions] = await Promise.all([loadSessions(), loadDecisions()]);
  renderActivityRows(filterSessions(sessions), filterDecisions(decisions));
}

async function refreshDemoMetrics() {
  renderDemoMetrics(await loadDemoMetrics());
}

async function refreshInventory() {
  const [repositories, rollouts] = await Promise.all([loadRepositories(), loadPolicyRollouts()]);
  renderInventoryRows(filterRepositories(repositories), filterPolicyRollouts(rollouts));
}

async function refreshPolicyCatalog() {
  renderPolicyCatalog(await loadPolicyCatalog());
}

async function showPolicyRolloutDetail(rolloutId) {
  renderPolicyRolloutDetail(await loadPolicyRolloutDetail(rolloutId));
}

async function refreshIntegrations() {
  const items = filterIntegrations(await loadIntegrations());
  renderIntegrationRows(items);
}

async function refreshSecurityBoundary() {
  renderSecurityBoundary(await loadSecurityBoundary());
}

async function refreshDeploymentReadiness() {
  renderDeploymentReadiness(await loadDeploymentReadiness());
}

async function refreshConsoleSession() {
  renderConsoleSession(await loadConsoleSession());
}

async function refreshApprovals() {
  const items = filterApprovals(await loadApprovals());
  renderApprovalRows(items);
}

async function refreshRegistry() {
  const [agents, mcpServers, profiles, classifications] = await Promise.all([
    loadAgents(),
    loadMcpServers(),
    loadAgentProfiles(),
    loadMcpClassifications()
  ]);
  renderRegistryRows(filterAgents(agents), filterMcpServers(mcpServers), profiles, classifications);
}

async function submitApprovalAction(approvalId, action) {
  const reason = action === "expire" ? "approval expired from console" : window.prompt(`${action} reason`);
  if (!reason) return;
  try {
    const response = await fetch(apiUrl(`/approvals/${approvalId}/${action}`), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify({ actor: "console-user", reason })
    });
    if (!response.ok) throw new Error("Approval API unavailable");
  } catch {
    const item = approvalCatalog.find((approval) => approval.approval_id === approvalId);
    if (item) {
      item.state = action === "approve" ? "approved" : action === "deny" ? "denied" : "expired";
      item.decided_by = "console-user";
      item.decision_reason = reason;
      item.history = [
        ...(Array.isArray(item.history) ? item.history : []),
        { event: item.state, actor: "console-user", timestamp: new Date().toISOString(), reason }
      ];
    }
  }
  await refreshApprovals();
}

async function showApprovalDetail(approvalId) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl(`/approvals/${approvalId}`));
    if (!response.ok) throw new Error("Approval API unavailable");
    renderApprovalDetail(await response.json());
  } catch {
    renderApprovalDetail(approvalCatalog.find((approval) => approval.approval_id === approvalId));
  }
}

async function createBreakGlassApproval() {
  const target = document.querySelector("#breakGlassTarget").value.trim();
  const rule = document.querySelector("#breakGlassRule").value.trim();
  const actor = document.querySelector("#breakGlassActor").value.trim();
  const group = document.querySelector("#breakGlassGroup").value.trim();
  const externalRef = document.querySelector("#breakGlassRef").value.trim();
  const reason = document.querySelector("#breakGlassReason").value.trim();
  const ttlHours = Number(document.querySelector("#breakGlassTtl").value || 4);
  const status = document.querySelector("#breakGlassStatus");
  if (!target || !actor || !group || !reason) {
    status.textContent = "Target, actor, group, and reason are required.";
    status.className = "status-line warn";
    return;
  }
  const payload = {
    decision: {
      decision_id: `dec_console_${Date.now()}`,
      session_id: "console-break-glass",
      action_type: "execute_command",
      target,
      rule_id: rule || "commands.block",
      decision: "block",
      severity: "critical",
      reason: "Emergency override requested from console.",
      evidence_refs: [`console://break-glass/${Date.now()}`]
    },
    actor,
    reason,
    approver_group: group,
    external_ref: externalRef || undefined,
    ttl_hours: ttlHours
  };
  try {
    const response = await fetch(apiUrl("/approvals/break-glass"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Approval API unavailable");
    const created = await response.json();
    status.textContent = `Break-glass approval created: ${created.approval_id}`;
    status.className = "status-line ok";
    renderApprovalDetail(created);
  } catch {
    const created = {
      schema_version: "cavra.approval.v1",
      product: "CAVRA",
      approval_id: `apr_console_${Date.now()}`,
      decision_id: payload.decision.decision_id,
      session_id: payload.decision.session_id,
      state: "break_glass",
      approver_group: group,
      requested_by: actor,
      requested_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + ttlHours * 60 * 60 * 1000).toISOString(),
      external_ref: externalRef || undefined,
      break_glass: true,
      break_glass_reason: reason,
      decision: payload.decision,
      evidence_refs: [`approval://console/${Date.now()}`, ...payload.decision.evidence_refs],
      history: [{ event: "break_glass", actor, timestamp: new Date().toISOString(), reason }]
    };
    approvalCatalog.unshift(created);
    status.textContent = `Break-glass approval created locally: ${created.approval_id}`;
    status.className = "status-line ok";
    renderApprovalDetail(created);
  }
  await refreshApprovals();
}

async function verifyAttestation() {
  const selected = document.querySelector("#attestationSession").value;
  const result = document.querySelector("#attestationResult");
  const items = await loadEvidenceMetadata();
  const item = items.find((entry) => entry.session_id === selected) || evidenceCatalog.find((entry) => entry.session_id === selected);
  const decisions = item?.decisions || evidenceCatalog[0].decisions;
  const targets = item?.attestation_targets || decisions.map((decision) => decision.target);
  const missing = targets.filter((target) => !JSON.stringify(decisions).includes(target));
  result.innerHTML = "";
  result.insertAdjacentHTML("beforeend", `<li class="${missing.length ? "warn" : "ok"}">${missing.length ? "Verification needs review" : "Attestation coverage verified"}</li>`);
  result.insertAdjacentHTML("beforeend", `<li>Session: ${selected}</li>`);
  result.insertAdjacentHTML("beforeend", `<li>Decision targets checked: ${targets.length}</li>`);
  result.insertAdjacentHTML("beforeend", `<li>Missing targets: ${missing.length}</li>`);
}

document.querySelector("#runScenario").addEventListener("click", runScenario);
document.querySelector("#refreshEvidence").addEventListener("click", refreshEvidence);
document.querySelector("#refreshReleaseDelivery").addEventListener("click", refreshReleaseDelivery);
document.querySelector("#refreshEndpointPublicationDelivery").addEventListener("click", refreshEndpointPublicationDelivery);
document.querySelector("#refreshEndpointInventory").addEventListener("click", refreshEndpointInventory);
document.querySelector("#refreshEndpointInventoryFreshness").addEventListener("click", refreshEndpointInventoryFreshness);
document.querySelector("#refreshEndpointReconciliation").addEventListener("click", refreshEndpointReconciliation);
document.querySelector("#refreshEndpointRemediation").addEventListener("click", refreshEndpointRemediation);
document.querySelector("#refreshEndpointRemediationHandoff").addEventListener("click", refreshEndpointRemediationHandoff);
document.querySelector("#refreshEndpointRemediationHandoffStatus").addEventListener("click", refreshEndpointRemediationHandoffStatus);
document.querySelector("#refreshEndpointRemediationSla").addEventListener("click", refreshEndpointRemediationSla);
document.querySelector("#refreshEndpointRecurrenceOperations").addEventListener("click", refreshEndpointRecurrenceOperations);
document.querySelector("#refreshGoRollbackDrillNotifications").addEventListener("click", refreshGoRollbackDrillNotifications);
document.querySelector("#goDrillBulkAckOutstanding").addEventListener("click", () => recordGoDrillBulkAcknowledgements("acknowledged"));
document.querySelector("#goDrillBulkEscalateBreached").addEventListener("click", () => recordGoDrillBulkAcknowledgements("escalated"));
document.querySelector("#goDrillExportAckAudit").addEventListener("click", exportGoDrillAckAuditPackage);
document.querySelector("#goDrillDeliverAckAudit").addEventListener("click", deliverGoDrillAckAuditPackage);
document.querySelector("#goDrillPlanAckAuditRetry").addEventListener("click", planGoDrillAckAuditRetry);
document.querySelector("#goDrillRunAckAuditWorker").addEventListener("click", runGoDrillAckAuditWorker);
document.querySelector("#goDrillSendAckAuditWorkerAlert").addEventListener("click", sendGoDrillAckAuditWorkerHealthAlert);
document.querySelector("#goDrillAckAuditRetryAck").addEventListener("click", acknowledgeGoDrillAckAuditRetry);
document.querySelector("#goDrillPlanRetryExecutionApproval").addEventListener("click", planGoDrillRetryExecutionApproval);
document.querySelector("#goDrillApproveRetryExecution").addEventListener("click", approveGoDrillRetryExecution);
document.querySelector("#goDrillBuildConnectorRecovery").addEventListener("click", buildGoDrillConnectorRecoveryPlaybook);
document.querySelector("#goDrillExecuteApprovedRetry").addEventListener("click", executeGoDrillApprovedRetry);
document.querySelector("#goDrillCloseConnectorRecovery").addEventListener("click", closeGoDrillConnectorRecovery);
document.querySelector("#goDrillPlanRecoveryEscalation").addEventListener("click", planGoDrillRecoveryEscalation);
document.querySelector("#goDrillDeliverRecoveryEscalation").addEventListener("click", deliverGoDrillRecoveryEscalation);
document.querySelector("#goDrillBuildRecoveryExecutiveReport").addEventListener("click", buildGoDrillRecoveryExecutiveReport);
document.querySelector("#goDrillAckRecoveryEscalation").addEventListener("click", acknowledgeGoDrillRecoveryEscalation);
document.querySelector("#goDrillPlanRecoveryEscalationRetry").addEventListener("click", planGoDrillRecoveryEscalationRetry);
document.querySelector("#goDrillRunRecoveryEscalationRetry").addEventListener("click", runGoDrillRecoveryEscalationRetryWorker);
document.querySelector("#goDrillBuildRecoveryEscalationRetryHealth").addEventListener("click", buildGoDrillRecoveryEscalationRetryHealth);
document.querySelector("#goDrillSendRecoveryRetryHealthAlert").addEventListener("click", sendGoDrillRecoveryRetryHealthAlert);
document.querySelector("#goDrillPlanRecoveryRetryHealthAlertRetry").addEventListener("click", planGoDrillRecoveryRetryHealthAlertRetry);
document.querySelector("#goDrillRunRecoveryRetryHealthAlertRetry").addEventListener("click", runGoDrillRecoveryRetryHealthAlertRetryWorker);
document.querySelector("#goDrillScheduleRecoveryExecutiveReport").addEventListener("click", scheduleGoDrillRecoveryExecutiveReport);
document.querySelector("#goDrillDeliverRecoveryExecutiveReport").addEventListener("click", deliverGoDrillRecoveryExecutiveReport);
document.querySelector("#goDrillPlanExecutiveDeliveryRetry").addEventListener("click", planGoDrillRecoveryExecutiveDeliveryRetry);
document.querySelector("#goDrillRunExecutiveDeliveryRetry").addEventListener("click", runGoDrillRecoveryExecutiveDeliveryRetryWorker);
document.querySelector("#goDrillBuildExecutiveDeliveryRetryHealth").addEventListener("click", buildGoDrillExecutiveDeliveryRetryHealth);
document.querySelector("#goDrillSendExecutiveDeliveryRetryHealthAlert").addEventListener("click", sendGoDrillExecutiveDeliveryRetryHealthAlert);
document.querySelector("#goDrillPlanExecutiveRetryHealthAlertRetry").addEventListener("click", planGoDrillExecutiveRetryHealthAlertRetry);
document.querySelector("#goDrillRunExecutiveRetryHealthAlertRetry").addEventListener("click", runGoDrillExecutiveRetryHealthAlertRetryWorker);
document.querySelector("#goDrillShowFinalReportingClosure").addEventListener("click", showGoDrillFinalReportingClosureDashboard);
document.querySelector("#deliverEndpointRemediationSla").addEventListener("click", deliverEndpointRemediationSlaNotification);
document.querySelectorAll("#filterEndpointRecurrenceOwner, #filterEndpointRecurrenceProvider, #filterEndpointRecurrenceAction, #filterEndpointRecurrenceCategory, #filterEndpointRecurrenceWorkerMode").forEach((control) => {
  control.addEventListener("input", refreshEndpointRecurrenceOperations);
  control.addEventListener("change", refreshEndpointRecurrenceOperations);
});
document.querySelectorAll("#filterGoDrillNotificationOwner, #filterGoDrillNotificationProvider, #filterGoDrillNotificationState, #filterGoDrillNotificationKind, #filterGoDrillDeliverySource, #filterGoDrillNotificationAction, #filterGoDrillNotificationCategory").forEach((control) => {
  control.addEventListener("input", refreshGoRollbackDrillNotifications);
  control.addEventListener("change", refreshGoRollbackDrillNotifications);
});
document.querySelector("#refreshActivity").addEventListener("click", refreshActivity);
document.querySelector("#refreshInventory").addEventListener("click", refreshInventory);
document.querySelector("#refreshPolicyCatalog").addEventListener("click", refreshPolicyCatalog);
document.querySelector("#previewPolicyDraft").addEventListener("click", previewPolicyDraft);
document.querySelector("#planPolicyPublish").addEventListener("click", planPolicyPublish);
document.querySelector("#requestPolicyPublishApproval").addEventListener("click", requestPolicyPublishApproval);
document.querySelector("#publishPolicyPack").addEventListener("click", publishPolicyPack);
document.querySelector("#planRolloutChange").addEventListener("click", planRolloutChange);
document.querySelector("#applyRolloutChange").addEventListener("click", applyRolloutChange);
document.querySelector("#refreshReleaseChannels").addEventListener("click", refreshReleaseChannels);
document.querySelector("#refreshIntegrations").addEventListener("click", refreshIntegrations);
document.querySelector("#refreshSecurityBoundary").addEventListener("click", refreshSecurityBoundary);
document.querySelector("#refreshDeploymentReadiness").addEventListener("click", refreshDeploymentReadiness);
document.querySelector("#refreshConsoleSession").addEventListener("click", refreshConsoleSession);
document.querySelector("#saveConsoleToken").addEventListener("click", async () => {
  consoleAuthToken = document.querySelector("#consoleToken").value.trim();
  window.sessionStorage?.setItem("cavraConsoleToken", consoleAuthToken);
  await refreshConsoleSession();
});
document.querySelector("#clearConsoleToken").addEventListener("click", async () => {
  consoleAuthToken = "";
  document.querySelector("#consoleToken").value = "";
  window.sessionStorage?.removeItem("cavraConsoleToken");
  await refreshConsoleSession();
});
document.querySelector("#refreshApprovals").addEventListener("click", refreshApprovals);
document.querySelector("#refreshRegistry").addEventListener("click", refreshRegistry);
document.querySelector("#createBreakGlass").addEventListener("click", createBreakGlassApproval);
document.querySelector("#evidenceRows").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const artifactButton = event.target.closest(".evidenceArtifactAction");
  if (!artifactButton) return;
  const item = evidenceMetadataCache.find((entry) => entry.session_id === artifactButton.dataset.session);
  if (item?.metadata_kind === "rollout-promotion-execution") {
    await showPromotionExecutionDetail(artifactButton.dataset.session);
    return;
  }
  if (item?.metadata_kind === "rollout-rollback-execution") {
    await showRollbackExecutionDetail(artifactButton.dataset.session);
    return;
  }
  await showEvidenceArtifacts(artifactButton.dataset.session);
});
document.querySelector("#evidenceArtifacts").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const promotionButton = event.target.closest(".rolloutPromotionRequestAction");
  const executionButton = event.target.closest(".rolloutPromotionExecutionAction");
  if (promotionButton) await requestRolloutPromotionApproval(promotionButton.dataset.session);
  if (executionButton) await recordRolloutPromotionExecution(executionButton.dataset.session);
});
document.querySelector("#rolloutRows").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const detailButton = event.target.closest(".rolloutDetailAction");
  if (!detailButton) return;
  await showPolicyRolloutDetail(detailButton.dataset.id);
});
document.querySelector("#endpointExportRows").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const artifactButton = event.target.closest(".endpointExportArtifactAction");
  if (!artifactButton) return;
  await showEndpointExportArtifacts(artifactButton.dataset.export);
});
document.addEventListener("click", (event) => {
  if (!(event.target instanceof Element)) return;
  const detailButton = event.target.closest(".endpointRecurrenceDetailAction");
  if (detailButton) {
    showEndpointRecurrenceDetail(detailButton.dataset.payload);
    return;
  }
  const exportButton = event.target.closest(".endpointRecurrenceExportAction");
  if (exportButton) exportEndpointRecurrencePayload(exportButton.dataset.payload);
  const goDrillDetailButton = event.target.closest(".goDrillNotificationDetailAction");
  if (goDrillDetailButton) {
    showGoDrillNotificationDetail(goDrillDetailButton.dataset.payload);
    return;
  }
  const goDrillExportButton = event.target.closest(".goDrillNotificationExportAction");
  if (goDrillExportButton) {
    exportGoDrillNotificationPayload(goDrillExportButton.dataset.payload);
    return;
  }
  const goDrillAckButton = event.target.closest(".goDrillAckAction");
  if (goDrillAckButton) {
    recordGoDrillAcknowledgement(goDrillAckButton.dataset.payload, goDrillAckButton.dataset.state || "acknowledged");
  }
});
document.querySelector("#approvalRows").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const detailButton = event.target.closest(".approvalDetailAction");
  if (detailButton) {
    await showApprovalDetail(detailButton.dataset.id);
    return;
  }
  const actionButton = event.target.closest(".approvalAction");
  if (!actionButton) return;
  await submitApprovalAction(actionButton.dataset.id, actionButton.dataset.action);
});
document.querySelector("#verifyAttestation").addEventListener("click", verifyAttestation);
document.querySelector("#copyInstall").addEventListener("click", async () => {
  await navigator.clipboard.writeText("claude mcp add cavra -- cavra-mcp-server");
});
refreshEvidence();
renderReleaseNotes();
refreshReleaseChannels();
refreshReleaseDelivery();
refreshEndpointPublicationDelivery();
refreshEndpointInventory();
refreshEndpointInventoryFreshness();
refreshEndpointReconciliation();
refreshEndpointRemediation();
refreshEndpointRemediationHandoff();
refreshEndpointRemediationHandoffStatus();
refreshEndpointRemediationSla();
refreshEndpointRecurrenceOperations();
refreshGoRollbackDrillNotifications();
refreshDemoMetrics();
refreshActivity();
refreshInventory();
refreshPolicyCatalog();
refreshIntegrations();
refreshSecurityBoundary();
refreshDeploymentReadiness();
document.querySelector("#consoleToken").value = consoleAuthToken;
refreshConsoleSession();
refreshApprovals();
refreshRegistry();
