"""Public-safe AISPM report delivery contracts.

The real Enterprise renderer, scheduler, tenant store, and email delivery
implementation live outside this Community repository. This module exposes the
stable public contract that Community docs, tests, and private Enterprise
packages can agree on without shipping commercial source code or secrets.
"""

from __future__ import annotations

from typing import Any


AISPM_REPORT_DELIVERY_CONTRACT_SCHEMA_VERSION = "cavra.aispm.report_delivery_contract.v1"
AISPM_REPORT_SETUP_WIZARD_CONTRACT_SCHEMA_VERSION = "cavra.aispm.report_setup_wizard_contract.v1"
AISPM_REPORT_DELIVERY_AUDIT_EVENT_SCHEMA_VERSION = "cavra.aispm.report_delivery_audit_event.v1"
AISPM_REPORT_OPERATIONS_DASHBOARD_SCHEMA_VERSION = "cavra.aispm.report_operations_dashboard.v1"
AISPM_REPORT_RETENTION_LIFECYCLE_SCHEMA_VERSION = "cavra.aispm.report_retention_lifecycle.v1"
AISPM_REPORT_SEARCH_RETRIEVAL_SCHEMA_VERSION = "cavra.aispm.report_search_retrieval.v1"
AISPM_REPORT_EXPORT_PACKAGE_MANIFEST_SCHEMA_VERSION = "cavra.aispm.report_export_package_manifest.v1"
AISPM_REPORT_SCHEDULE_POLICY_SCHEMA_VERSION = "cavra.aispm.report_schedule_policy.v1"
AISPM_REPORT_RECIPIENT_POLICY_SCHEMA_VERSION = "cavra.aispm.report_recipient_policy.v1"
AISPM_REPORT_APPROVAL_DECISION_SCHEMA_VERSION = "cavra.aispm.report_approval_decision.v1"
AISPM_REPORT_EXCEPTION_LIFECYCLE_SCHEMA_VERSION = "cavra.aispm.report_exception_lifecycle.v1"
AISPM_REPORT_EVIDENCE_ROOM_SCHEMA_VERSION = "cavra.aispm.report_evidence_room.v1"
AISPM_REPORT_EVIDENCE_ROOM_ACCESS_EVENT_SCHEMA_VERSION = (
    "cavra.aispm.report_evidence_room_access_event.v1"
)
AISPM_REPORT_INCIDENT_PACKET_SCHEMA_VERSION = "cavra.aispm.report_incident_packet.v1"
AISPM_REPORT_INCIDENT_CLOSURE_SCHEMA_VERSION = "cavra.aispm.report_incident_closure.v1"
AISPM_REPORT_KPI_METRICS_SCHEMA_VERSION = "cavra.aispm.report_kpi_metrics.v1"
AISPM_REPORT_ALERT_ESCALATION_SCHEMA_VERSION = "cavra.aispm.report_alert_escalation.v1"
AISPM_REPORT_ALERT_OPERATIONS_DASHBOARD_SCHEMA_VERSION = (
    "cavra.aispm.report_alert_operations_dashboard.v1"
)
AISPM_REPORT_ALERT_DRILLDOWN_SCHEMA_VERSION = "cavra.aispm.report_alert_drilldown.v1"
AISPM_REPORT_ALERT_REMEDIATION_PLAN_SCHEMA_VERSION = (
    "cavra.aispm.report_alert_remediation_plan.v1"
)
AISPM_REPORT_ALERT_REMEDIATION_CLOSURE_SCHEMA_VERSION = (
    "cavra.aispm.report_alert_remediation_closure.v1"
)
AISPM_REPORT_REMEDIATION_CLOSURE_OPERATIONS_DASHBOARD_SCHEMA_VERSION = (
    "cavra.aispm.report_remediation_closure_operations_dashboard.v1"
)
AISPM_REPORT_REMEDIATION_CLOSURE_EXECUTIVE_DIGEST_SCHEMA_VERSION = (
    "cavra.aispm.report_remediation_closure_executive_digest.v1"
)
AISPM_REPORT_REMEDIATION_CLOSURE_DIGEST_DISTRIBUTION_SCHEMA_VERSION = (
    "cavra.aispm.report_remediation_closure_digest_distribution.v1"
)
AISPM_REPORT_CENTER_TRIAL_VALIDATION_PACKET_SCHEMA_VERSION = (
    "cavra.aispm.report_center_trial_validation_packet.v1"
)
AISPM_REPORT_CENTER_TRIAL_OPERATOR_DASHBOARD_SCHEMA_VERSION = (
    "cavra.aispm.report_center_trial_operator_dashboard_readiness.v1"
)
AISPM_REPORT_CENTER_TRIAL_OPERATOR_API_VIEW_MODEL_SCHEMA_VERSION = (
    "cavra.aispm.report_center_trial_operator_api_view_model.v1"
)
AISPM_REPORT_CENTER_TRIAL_EVALUATOR_HANDOFF_SCHEMA_VERSION = (
    "cavra.aispm.report_center_trial_evaluator_handoff_packet.v1"
)
AISPM_REPORT_CENTER_TRIAL_REVOCATION_EXPIRY_SCHEMA_VERSION = (
    "cavra.aispm.report_center_trial_revocation_expiry_evidence.v1"
)
AISPM_REPORT_CENTER_TRIAL_LAB_NOTEBOOK_SCHEMA_VERSION = (
    "cavra.aispm.report_center_trial_lab_notebook_outline.v1"
)
AISPM_REPORT_CENTER_TRIAL_LAB_NOTEBOOK_PUBLICATION_READINESS_SCHEMA_VERSION = (
    "cavra.aispm.report_center_trial_lab_notebook_publication_readiness.v1"
)


COMMUNITY_REPORTS: list[dict[str, Any]] = [
    {
        "report_id": "executive_risk_brief",
        "title": "Executive Risk Brief",
        "formats": ["markdown"],
        "audiences": ["cso", "ciso"],
        "availability": "community",
    },
    {
        "report_id": "board_kpi_pack",
        "title": "Board KPI Pack",
        "formats": ["json"],
        "audiences": ["board", "leadership"],
        "availability": "community",
    },
    {
        "report_id": "soc2_audit_summary",
        "title": "SOC 2-Style Audit Summary",
        "formats": ["markdown"],
        "audiences": ["audit", "grc"],
        "availability": "community",
    },
    {
        "report_id": "control_coverage_export",
        "title": "Control Coverage Export",
        "formats": ["csv"],
        "audiences": ["security_engineering"],
        "availability": "community",
    },
    {
        "report_id": "evidence_freshness_export",
        "title": "Evidence Freshness Export",
        "formats": ["csv"],
        "audiences": ["audit", "grc"],
        "availability": "community",
    },
    {
        "report_id": "agent_risk_register",
        "title": "Agent Risk Register",
        "formats": ["csv"],
        "audiences": ["platform_security"],
        "availability": "community",
    },
]


ENTERPRISE_REPORTS: list[dict[str, Any]] = [
    {
        "report_id": "pdf_board_pack",
        "title": "PDF Board Pack",
        "formats": ["pdf"],
        "audiences": ["board", "cso", "ciso"],
        "availability": "requires_cavra_enterprise",
    },
    {
        "report_id": "xlsx_evidence_workbook",
        "title": "XLSX Evidence Workbook",
        "formats": ["xlsx"],
        "audiences": ["audit", "grc", "security_engineering"],
        "availability": "requires_cavra_enterprise",
    },
    {
        "report_id": "docx_audit_narrative",
        "title": "DOCX Audit Narrative",
        "formats": ["docx"],
        "audiences": ["audit", "risk_committee"],
        "availability": "requires_cavra_enterprise",
    },
    {
        "report_id": "signed_json_evidence_packet",
        "title": "Signed JSON Evidence Packet",
        "formats": ["json"],
        "audiences": ["audit", "security_engineering"],
        "availability": "requires_cavra_enterprise",
    },
    {
        "report_id": "siem_jsonl_export",
        "title": "SIEM JSONL Export",
        "formats": ["jsonl"],
        "audiences": ["soc", "security_operations"],
        "availability": "requires_cavra_enterprise",
    },
    {
        "report_id": "grc_upload_package",
        "title": "GRC Upload Package",
        "formats": ["zip"],
        "audiences": ["grc", "audit"],
        "availability": "requires_cavra_enterprise",
    },
]


REPORT_SETUP_WIZARD_STEPS: list[dict[str, Any]] = [
    {
        "step_id": "organization_profile",
        "title": "Organization Profile",
        "description": "Collect public report identity, timezone, retention, and branding references.",
        "fields": [
            "CAVRA_REPORT_FROM_ADDRESS",
            "CAVRA_REPORT_REPLY_TO",
            "CAVRA_REPORT_DEFAULT_TIMEZONE",
            "CAVRA_REPORT_RETENTION_DAYS",
            "CAVRA_REPORT_BRAND_PROFILE",
        ],
        "availability": "requires_cavra_enterprise",
    },
    {
        "step_id": "delivery_provider",
        "title": "Delivery Provider",
        "description": "Select SMTP, Microsoft 365, Google Workspace, AWS SES, SendGrid, webhook, or disabled mode.",
        "fields": [
            "CAVRA_REPORT_DELIVERY_MODE",
            "CAVRA_REPORT_SMTP_HOST",
            "CAVRA_REPORT_SMTP_PORT",
            "CAVRA_REPORT_SMTP_USERNAME_REF",
            "CAVRA_REPORT_SMTP_PASSWORD_REF",
            "CAVRA_REPORT_PROVIDER_TOKEN_REF",
        ],
        "availability": "requires_cavra_enterprise",
    },
    {
        "step_id": "recipient_governance",
        "title": "Recipient Governance",
        "description": "Define recipient domain allowlists, approval requirements, and RBAC scopes.",
        "fields": [
            "CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS",
            "CAVRA_REPORT_EXTERNAL_APPROVAL_REQUIRED",
            "CAVRA_REPORT_ALLOWED_RBAC_ROLES",
        ],
        "availability": "requires_cavra_enterprise",
    },
    {
        "step_id": "schedule_and_audit",
        "title": "Schedule And Audit",
        "description": "Configure schedule presets, delivery retry policy, evidence retention, and audit export references.",
        "fields": [
            "CAVRA_REPORT_DEFAULT_SCHEDULE",
            "CAVRA_REPORT_RETRY_POLICY",
            "CAVRA_REPORT_DELIVERY_AUDIT_RETENTION_DAYS",
            "CAVRA_REPORT_AUDIT_EXPORT_REF",
        ],
        "availability": "requires_cavra_enterprise",
    },
]


def build_aispm_report_delivery_contract() -> dict[str, Any]:
    """Return the public-safe Enterprise report delivery integration contract."""

    return {
        "schema_version": AISPM_REPORT_DELIVERY_CONTRACT_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "community_reports": COMMUNITY_REPORTS,
        "enterprise_reports": ENTERPRISE_REPORTS,
        "api": {
            "catalog_endpoint": "GET /enterprise/aispm/reports/catalog",
            "render_endpoint": "POST /enterprise/aispm/reports/render",
            "send_endpoint": "POST /enterprise/aispm/reports/send",
            "deliveries_endpoint": "GET /enterprise/aispm/reports/deliveries",
            "schedules_endpoint": "POST /enterprise/aispm/reports/schedules",
            "implementation": "requires_cavra_enterprise",
        },
        "delivery": {
            "supported_modes": [
                "disabled",
                "smtp",
                "microsoft365",
                "google_workspace",
                "ses",
                "sendgrid",
                "webhook",
            ],
            "recipient_controls": [
                "domain_allowlist",
                "rbac",
                "approval_gate",
                "delivery_audit",
            ],
            "implementation": "requires_cavra_enterprise",
        },
        "setup": {
            "required_settings": [
                "CAVRA_REPORT_DELIVERY_MODE",
                "CAVRA_REPORT_FROM_ADDRESS",
                "CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS",
                "CAVRA_REPORT_DEFAULT_TIMEZONE",
                "CAVRA_REPORT_RETENTION_DAYS",
            ],
            "secret_reference_settings": [
                "CAVRA_REPORT_SMTP_USERNAME_REF",
                "CAVRA_REPORT_SMTP_PASSWORD_REF",
                "CAVRA_REPORT_PROVIDER_TOKEN_REF",
            ],
            "secret_values_allowed_in_public_repo": False,
        },
        "security_controls": [
            "tenant_scoped_rendering",
            "recipient_domain_allowlist",
            "rbac_authorization",
            "optional_external_delivery_approval",
            "immutable_delivery_audit",
            "secret_manager_references_only",
            "raw_prompt_and_reasoning_redaction",
        ],
        "enterprise_boundaries": {
            "renderer": "requires_cavra_enterprise",
            "scheduler": "requires_cavra_enterprise",
            "email_delivery": "requires_cavra_enterprise",
            "tenant_persistence": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_setup_wizard_contract() -> dict[str, Any]:
    """Return the public-safe Enterprise setup wizard contract for reports."""

    return {
        "schema_version": AISPM_REPORT_SETUP_WIZARD_CONTRACT_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "wizard": {
            "wizard_id": "aispm_report_delivery_setup",
            "title": "AISPM Report Delivery Setup",
            "purpose": "Collect tenant-specific report delivery settings without storing secret values in public files.",
            "implementation": "requires_cavra_enterprise",
        },
        "steps": REPORT_SETUP_WIZARD_STEPS,
        "delivery_modes": [
            "disabled",
            "smtp",
            "microsoft365",
            "google_workspace",
            "ses",
            "sendgrid",
            "webhook",
        ],
        "validation_rules": [
            {
                "rule_id": "sender-address-required",
                "field": "CAVRA_REPORT_FROM_ADDRESS",
                "requirement": "must be a verified sender address for enabled delivery modes",
                "enforcement": "requires_cavra_enterprise",
            },
            {
                "rule_id": "recipient-domain-allowlist-required",
                "field": "CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS",
                "requirement": "must contain at least one approved domain before external delivery is enabled",
                "enforcement": "requires_cavra_enterprise",
            },
            {
                "rule_id": "secret-values-not-accepted",
                "field": "*_REF",
                "requirement": "wizard accepts secret-manager references only, never raw credential values",
                "enforcement": "requires_cavra_enterprise",
            },
            {
                "rule_id": "external-delivery-approval",
                "field": "CAVRA_REPORT_EXTERNAL_APPROVAL_REQUIRED",
                "requirement": "high-risk or external-domain report delivery may require an approval gate",
                "enforcement": "requires_cavra_enterprise",
            },
        ],
        "admin_settings": {
            "required_public_settings": [
                "CAVRA_REPORT_DELIVERY_MODE",
                "CAVRA_REPORT_FROM_ADDRESS",
                "CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS",
                "CAVRA_REPORT_DEFAULT_TIMEZONE",
                "CAVRA_REPORT_RETENTION_DAYS",
            ],
            "optional_public_settings": [
                "CAVRA_REPORT_REPLY_TO",
                "CAVRA_REPORT_BRAND_PROFILE",
                "CAVRA_REPORT_DEFAULT_SCHEDULE",
                "CAVRA_REPORT_EXTERNAL_APPROVAL_REQUIRED",
                "CAVRA_REPORT_ALLOWED_RBAC_ROLES",
            ],
            "secret_reference_settings": [
                "CAVRA_REPORT_SMTP_USERNAME_REF",
                "CAVRA_REPORT_SMTP_PASSWORD_REF",
                "CAVRA_REPORT_PROVIDER_TOKEN_REF",
            ],
            "secret_values_allowed": False,
        },
        "enterprise_boundaries": {
            "wizard_ui": "requires_cavra_enterprise",
            "settings_persistence": "requires_cavra_enterprise",
            "secret_resolution": "requires_cavra_enterprise",
            "provider_validation": "requires_cavra_enterprise",
            "test_delivery": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_delivery_audit_event_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report delivery audit events."""

    return {
        "schema_version": AISPM_REPORT_DELIVERY_AUDIT_EVENT_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "audit_event": {
            "audit_event_id": "audit_report_delivery_public_contract_sample",
            "action": "send",
            "occurred_at": "2026-06-11T08:00:00Z",
            "tenant_ref": "tenant:opaque-public-contract-sample",
            "actor_ref": "role:ciso",
            "report_id": "pdf_board_pack",
            "requested_format": "pdf",
            "delivery_mode": "smtp",
            "status": "sent",
        },
        "recipient_summary": {
            "recipient_count": 2,
            "allowed_domains": ["example.com"],
            "external_domain_count": 0,
            "recipient_addresses_redacted": True,
        },
        "approval": {
            "approval_required": True,
            "approval_ref": "approval:opaque-public-contract-sample",
            "decision": "approved",
        },
        "retry": {
            "attempt": 1,
            "max_attempts": 3,
            "next_retry_at": None,
            "terminal": True,
        },
        "evidence": {
            "evidence_refs": ["cavra://evidence/redacted/report-delivery-sample"],
            "report_digest_ref": "sha256:redacted-public-contract-digest",
            "delivery_audit_ref": "enterprise-private://delivery-audit/opaque-ref",
            "immutable_store_ref": "enterprise-private://immutable-store/opaque-ref",
        },
        "redaction": {
            "raw_report_content_included": False,
            "provider_response_included": False,
            "recipient_addresses_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "audit_store": "requires_cavra_enterprise",
            "provider_response_storage": "requires_cavra_enterprise",
            "retry_worker": "requires_cavra_enterprise",
            "immutable_evidence_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_operations_dashboard_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report operations views."""

    return {
        "schema_version": AISPM_REPORT_OPERATIONS_DASHBOARD_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:05:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "summary": {
            "delivery_health": "degraded",
            "scheduled_reports": 8,
            "pending_approvals": 2,
            "retry_queue_depth": 3,
            "failed_deliveries": 1,
            "immutable_audit_coverage_percent": 96.5,
        },
        "queues": [
            {
                "queue": "delivery",
                "depth": 3,
                "oldest_age_minutes": 12,
                "status": "action_required",
            },
            {
                "queue": "audit_export",
                "depth": 0,
                "oldest_age_minutes": 0,
                "status": "healthy",
            },
        ],
        "scheduled_reports": [
            {
                "schedule_id": "schedule:opaque-board-pack",
                "report_id": "pdf_board_pack",
                "cadence": "weekly",
                "next_run_at": "2026-06-15T09:00:00Z",
                "status": "active",
            }
        ],
        "approval_bottlenecks": [
            {
                "approval_ref": "approval:opaque-pending-external-delivery",
                "report_id": "pdf_board_pack",
                "pending_minutes": 42,
                "approver_group": "security-leadership",
                "status": "pending",
            }
        ],
        "failed_deliveries": [
            {
                "delivery_ref": "delivery:opaque-failed-send",
                "report_id": "xlsx_evidence_workbook",
                "delivery_mode": "smtp",
                "failure_class": "provider_auth",
                "retry_status": "queued",
                "last_attempt_at": "2026-06-11T07:58:00Z",
            }
        ],
        "audit_coverage": {
            "events_expected": 124,
            "events_persisted": 120,
            "immutable_refs_missing": 4,
            "coverage_status": "partial",
        },
        "redaction": {
            "recipient_addresses_included": False,
            "provider_responses_included": False,
            "raw_report_content_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "dashboard_persistence": "requires_cavra_enterprise",
            "live_queue_inspection": "requires_cavra_enterprise",
            "provider_health_probe": "requires_cavra_enterprise",
            "retry_control": "requires_cavra_enterprise",
            "audit_search": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_retention_lifecycle_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report retention lifecycle."""

    return {
        "schema_version": AISPM_REPORT_RETENTION_LIFECYCLE_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:10:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "policy": {
            "policy_id": "report-retention-standard",
            "default_retention_days": 365,
            "audit_event_retention_days": 2555,
            "immutable_storage_required": True,
            "legal_hold_supported": True,
            "deletion_requires_approval": True,
        },
        "report_lifecycle": [
            {
                "report_ref": "report:opaque-board-pack",
                "report_id": "pdf_board_pack",
                "created_at": "2026-06-11T08:00:00Z",
                "expires_at": "2027-06-11T08:00:00Z",
                "lifecycle_state": "retained",
                "immutable_store_ref": "enterprise-private://immutable-store/report/opaque-ref",
                "legal_hold_ref": None,
            },
            {
                "report_ref": "report:opaque-audit-workbook",
                "report_id": "xlsx_evidence_workbook",
                "created_at": "2026-06-11T08:00:00Z",
                "expires_at": "2033-06-09T08:00:00Z",
                "lifecycle_state": "legal_hold",
                "immutable_store_ref": "enterprise-private://immutable-store/report/opaque-audit-ref",
                "legal_hold_ref": "legal-hold:opaque-public-contract-sample",
            },
        ],
        "audit_export_lifecycle": {
            "export_ref": "audit-export:opaque-report-delivery",
            "created_at": "2026-06-11T08:05:00Z",
            "expires_at": "2033-06-09T08:05:00Z",
            "archive_state": "archived",
            "object_lock": "enabled",
            "kms_key_ref": "enterprise-private://kms/opaque-key-ref",
        },
        "deletion_policy": {
            "allowed_states": ["expired", "archived"],
            "blocked_states": ["retained", "legal_hold", "pending_approval"],
            "approval_required": True,
            "tombstone_required": True,
        },
        "evidence": {
            "retention_evidence_refs": ["cavra://evidence/redacted/report-retention-sample"],
            "archive_manifest_ref": "enterprise-private://archive-manifest/opaque-ref",
            "chain_ref": "enterprise-private://evidence-chain/opaque-ref",
        },
        "redaction": {
            "raw_report_content_included": False,
            "recipient_addresses_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "retention_worker": "requires_cavra_enterprise",
            "legal_hold_store": "requires_cavra_enterprise",
            "immutable_archive": "requires_cavra_enterprise",
            "kms_integration": "requires_cavra_enterprise",
            "deletion_approval_workflow": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_search_retrieval_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report search and retrieval."""

    return {
        "schema_version": AISPM_REPORT_SEARCH_RETRIEVAL_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:15:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "query": {
            "query_id": "query:opaque-report-search",
            "actor_ref": "role:auditor",
            "filters": {
                "report_ids": ["pdf_board_pack", "xlsx_evidence_workbook"],
                "formats": ["pdf", "xlsx"],
                "lifecycle_states": ["retained", "legal_hold"],
                "from": "2026-06-01T00:00:00Z",
                "to": "2026-06-11T23:59:59Z",
            },
            "rbac_scope": "audit:read",
            "retention_mode": "retention_aware",
        },
        "results": [
            {
                "report_ref": "report:opaque-board-pack",
                "report_id": "pdf_board_pack",
                "format": "pdf",
                "created_at": "2026-06-11T08:00:00Z",
                "lifecycle_state": "retained",
                "download_allowed": True,
                "evidence_ref": "cavra://evidence/redacted/report-delivery-sample",
                "immutable_store_ref": "enterprise-private://immutable-store/report/opaque-ref",
            }
        ],
        "retrieval": {
            "retrieval_ref": "retrieval:opaque-report-download",
            "requested_report_ref": "report:opaque-board-pack",
            "access_decision": "allow",
            "download_url_ref": "enterprise-private://download-url/opaque-ref",
            "expires_at": "2026-06-11T08:30:00Z",
            "watermark_required": True,
        },
        "access_controls": {
            "rbac_enforced": True,
            "retention_checked": True,
            "legal_hold_checked": True,
            "download_audit_required": True,
            "approval_required": False,
        },
        "audit": {
            "audit_event_ref": "audit:opaque-report-retrieval",
            "logged_at": "2026-06-11T08:15:01Z",
            "evidence_refs": ["cavra://evidence/redacted/report-retrieval-sample"],
        },
        "redaction": {
            "raw_report_content_included": False,
            "download_url_included": False,
            "recipient_addresses_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "search_index": "requires_cavra_enterprise",
            "rbac_authorization": "requires_cavra_enterprise",
            "immutable_ref_resolution": "requires_cavra_enterprise",
            "signed_download_urls": "requires_cavra_enterprise",
            "retrieval_audit_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_export_package_manifest_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report export packages."""

    return {
        "schema_version": AISPM_REPORT_EXPORT_PACKAGE_MANIFEST_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:20:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "package": {
            "package_ref": "export-package:opaque-board-and-audit-pack",
            "package_type": "board_and_audit_bundle",
            "requested_by": "role:ciso",
            "created_at": "2026-06-11T08:20:00Z",
            "retention_class": "governance_record",
            "watermark_required": True,
            "signed_manifest_required": True,
        },
        "artifacts": [
            {
                "artifact_ref": "artifact:opaque-board-pdf",
                "report_id": "pdf_board_pack",
                "format": "pdf",
                "content_ref": "enterprise-private://report-artifact/opaque-board-pdf",
                "digest_ref": "sha256:redacted-public-contract-board-pdf",
                "size_bytes": 245760,
            },
            {
                "artifact_ref": "artifact:opaque-evidence-workbook",
                "report_id": "xlsx_evidence_workbook",
                "format": "xlsx",
                "content_ref": "enterprise-private://report-artifact/opaque-evidence-workbook",
                "digest_ref": "sha256:redacted-public-contract-evidence-workbook",
                "size_bytes": 196608,
            },
        ],
        "delivery_targets": [
            {
                "target_ref": "target:opaque-grc-upload",
                "target_type": "grc_upload",
                "recipient_scope": "approved_internal_domain",
                "delivery_mode": "webhook",
                "approval_required": True,
            }
        ],
        "integrity": {
            "manifest_digest_ref": "sha256:redacted-public-contract-manifest",
            "signature_ref": "enterprise-private://signature/opaque-manifest-signature",
            "chain_ref": "enterprise-private://evidence-chain/opaque-export-package",
            "checksums_required": True,
        },
        "evidence": {
            "source_evidence_refs": [
                "cavra://evidence/redacted/report-delivery-sample",
                "cavra://evidence/redacted/report-retrieval-sample",
            ],
            "export_audit_ref": "audit:opaque-export-package",
            "immutable_store_ref": "enterprise-private://immutable-store/export-package/opaque-ref",
        },
        "redaction": {
            "raw_report_content_included": False,
            "recipient_addresses_included": False,
            "download_urls_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "package_renderer": "requires_cavra_enterprise",
            "artifact_storage": "requires_cavra_enterprise",
            "manifest_signing": "requires_cavra_enterprise",
            "grc_connector": "requires_cavra_enterprise",
            "siem_exporter": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_schedule_policy_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report schedules."""

    return {
        "schema_version": AISPM_REPORT_SCHEDULE_POLICY_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:25:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "schedule": {
            "schedule_ref": "schedule:opaque-ciso-weekly-board-pack",
            "name": "Weekly CISO Board And Audit Pack",
            "status": "active",
            "report_ids": ["pdf_board_pack", "xlsx_evidence_workbook"],
            "formats": ["pdf", "xlsx"],
            "cadence": "weekly",
            "timezone": "UTC",
            "next_run_at": "2026-06-15T09:00:00Z",
            "created_by": "role:ciso",
        },
        "recipient_governance": {
            "recipient_scope": "approved_internal_domain",
            "allowed_domains": ["example.com"],
            "rbac_scope": "reports:schedule",
            "external_delivery_allowed": False,
            "recipient_addresses_redacted": True,
        },
        "delivery": {
            "delivery_mode": "smtp",
            "target_ref": "delivery-target:opaque-internal-leadership-list",
            "package_manifest_required": True,
            "watermark_required": True,
            "encrypted_attachment_required": True,
        },
        "approval_policy": {
            "approval_required": True,
            "approver_group": "security-leadership",
            "approval_ref": "approval-policy:opaque-weekly-board-pack",
            "change_requires_approval": True,
            "external_recipient_requires_approval": True,
        },
        "blackout_windows": [
            {
                "window_ref": "blackout:opaque-quarter-close",
                "starts_at": "2026-06-30T00:00:00Z",
                "ends_at": "2026-07-02T23:59:59Z",
                "behavior": "defer",
            }
        ],
        "retry_policy": {
            "max_attempts": 3,
            "backoff": "exponential",
            "retry_window_minutes": 120,
            "dead_letter_required": True,
        },
        "run_evidence": {
            "last_run_ref": "report-run:opaque-weekly-board-pack",
            "last_run_status": "sent",
            "last_run_at": "2026-06-08T09:00:00Z",
            "evidence_refs": ["cavra://evidence/redacted/report-schedule-run-sample"],
            "audit_event_ref": "audit:opaque-report-schedule-run",
        },
        "redaction": {
            "recipient_addresses_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "scheduler_worker": "requires_cavra_enterprise",
            "calendar_blackout_engine": "requires_cavra_enterprise",
            "recipient_resolution": "requires_cavra_enterprise",
            "provider_delivery": "requires_cavra_enterprise",
            "schedule_persistence": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_recipient_policy_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report recipient policy."""

    return {
        "schema_version": AISPM_REPORT_RECIPIENT_POLICY_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:30:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "policy": {
            "policy_ref": "recipient-policy:opaque-report-delivery-standard",
            "name": "Report Delivery Recipient Policy",
            "status": "active",
            "owner_ref": "role:security-admin",
            "default_action": "deny",
            "external_delivery_default": "require_approval",
        },
        "domain_rules": [
            {
                "domain": "example.com",
                "classification": "internal",
                "allowed": True,
                "approval_required": False,
                "encryption_required": True,
            },
            {
                "domain": "auditor.example",
                "classification": "external_auditor",
                "allowed": True,
                "approval_required": True,
                "encryption_required": True,
            },
        ],
        "recipient_groups": [
            {
                "group_ref": "recipient-group:opaque-security-leadership",
                "display_name": "Security Leadership",
                "role_scope": "ciso",
                "member_count": 3,
                "source": "idp_group",
                "addresses_redacted": True,
            }
        ],
        "delivery_channel_eligibility": [
            {
                "channel": "smtp",
                "allowed": True,
                "requires_verified_sender": True,
                "requires_encryption": True,
            },
            {
                "channel": "webhook",
                "allowed": True,
                "requires_verified_sender": False,
                "requires_encryption": True,
            },
            {
                "channel": "download",
                "allowed": True,
                "requires_verified_sender": False,
                "requires_encryption": False,
            },
        ],
        "approval_policy": {
            "external_recipient_approval_required": True,
            "new_domain_approval_required": True,
            "recipient_group_change_approval_required": True,
            "approver_group": "security-leadership",
            "approval_evidence_required": True,
        },
        "encryption_policy": {
            "attachment_encryption_required": True,
            "minimum_transport": "tls_1_2",
            "kms_key_ref_required": True,
            "customer_managed_key_supported": True,
        },
        "audit": {
            "policy_change_audit_ref": "audit:opaque-recipient-policy-change",
            "last_reviewed_at": "2026-06-10T12:00:00Z",
            "review_evidence_refs": ["cavra://evidence/redacted/recipient-policy-review-sample"],
        },
        "redaction": {
            "recipient_addresses_included": False,
            "idp_group_members_included": False,
            "provider_tokens_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "recipient_directory_sync": "requires_cavra_enterprise",
            "idp_group_resolution": "requires_cavra_enterprise",
            "domain_verification": "requires_cavra_enterprise",
            "encryption_key_resolution": "requires_cavra_enterprise",
            "approval_workflow": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_approval_decision_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report approval decisions."""

    return {
        "schema_version": AISPM_REPORT_APPROVAL_DECISION_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:35:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "approval_request": {
            "approval_ref": "approval:opaque-external-report-delivery",
            "request_type": "external_delivery_exception",
            "requested_by": "role:ciso",
            "requested_at": "2026-06-11T08:32:00Z",
            "resource_ref": "schedule:opaque-ciso-weekly-board-pack",
            "risk_level": "high",
            "reason_code": "external_auditor_delivery",
        },
        "decision": {
            "decision_ref": "approval-decision:opaque-external-report-delivery",
            "decision": "approved",
            "decided_by": "role:security-leadership",
            "decided_at": "2026-06-11T08:34:00Z",
            "expires_at": "2026-06-18T08:34:00Z",
            "conditions": [
                "recipient_domain_must_match_auditor_allowlist",
                "encrypted_attachment_required",
                "signed_export_manifest_required",
            ],
        },
        "subject": {
            "report_ids": ["pdf_board_pack", "xlsx_evidence_workbook"],
            "formats": ["pdf", "xlsx"],
            "delivery_mode": "smtp",
            "recipient_scope": "approved_external_domain",
            "recipient_addresses_redacted": True,
        },
        "policy_context": {
            "recipient_policy_ref": "recipient-policy:opaque-report-delivery-standard",
            "schedule_ref": "schedule:opaque-ciso-weekly-board-pack",
            "domain_rule_ref": "domain-rule:opaque-auditor-domain",
            "approval_policy_ref": "approval-policy:opaque-weekly-board-pack",
        },
        "evidence": {
            "approval_evidence_refs": ["cavra://evidence/redacted/report-approval-decision-sample"],
            "request_digest_ref": "sha256:redacted-public-contract-approval-request",
            "decision_digest_ref": "sha256:redacted-public-contract-approval-decision",
            "immutable_store_ref": "enterprise-private://immutable-store/report-approval/opaque-ref",
        },
        "audit": {
            "audit_event_ref": "audit:opaque-report-approval-decision",
            "logged_at": "2026-06-11T08:35:01Z",
            "review_required_by": "2026-06-18T08:34:00Z",
        },
        "redaction": {
            "approver_identity_included": False,
            "recipient_addresses_included": False,
            "raw_report_content_included": False,
            "private_justification_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "approval_workflow": "requires_cavra_enterprise",
            "approver_identity_resolution": "requires_cavra_enterprise",
            "policy_exception_store": "requires_cavra_enterprise",
            "immutable_decision_audit": "requires_cavra_enterprise",
            "notification_delivery": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_exception_lifecycle_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report exception lifecycle."""

    return {
        "schema_version": AISPM_REPORT_EXCEPTION_LIFECYCLE_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:40:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "exception": {
            "exception_ref": "exception:opaque-external-auditor-delivery",
            "exception_type": "external_delivery_exception",
            "status": "active",
            "opened_at": "2026-06-11T08:34:00Z",
            "expires_at": "2026-06-18T08:34:00Z",
            "owner_ref": "role:security-leadership",
            "linked_approval_ref": "approval-decision:opaque-external-report-delivery",
        },
        "scope": {
            "report_ids": ["pdf_board_pack", "xlsx_evidence_workbook"],
            "recipient_scope": "approved_external_domain",
            "domain_rule_ref": "domain-rule:opaque-auditor-domain",
            "schedule_ref": "schedule:opaque-ciso-weekly-board-pack",
            "delivery_modes": ["smtp"],
        },
        "lifecycle_events": [
            {
                "event_ref": "exception-event:opaque-opened",
                "event_type": "opened",
                "occurred_at": "2026-06-11T08:34:00Z",
                "actor_ref": "role:security-leadership",
                "evidence_ref": "cavra://evidence/redacted/report-exception-opened",
            },
            {
                "event_ref": "exception-event:opaque-review-scheduled",
                "event_type": "review_scheduled",
                "occurred_at": "2026-06-11T08:36:00Z",
                "actor_ref": "system:cavra",
                "evidence_ref": "cavra://evidence/redacted/report-exception-review-scheduled",
            },
        ],
        "review_policy": {
            "review_required": True,
            "review_due_at": "2026-06-17T08:34:00Z",
            "renewal_requires_approval": True,
            "revocation_requires_reason": True,
            "closure_requires_evidence": True,
        },
        "renewal": {
            "renewal_allowed": True,
            "max_renewals": 1,
            "renewal_window_starts_at": "2026-06-16T08:34:00Z",
            "renewal_approval_ref": "approval-policy:opaque-exception-renewal",
        },
        "closure": {
            "closure_state": "not_closed",
            "closed_at": None,
            "closure_reason": None,
            "closure_evidence_refs": [],
        },
        "evidence": {
            "exception_digest_ref": "sha256:redacted-public-contract-exception",
            "lifecycle_audit_ref": "audit:opaque-report-exception-lifecycle",
            "immutable_store_ref": "enterprise-private://immutable-store/report-exception/opaque-ref",
            "evidence_refs": ["cavra://evidence/redacted/report-exception-lifecycle-sample"],
        },
        "redaction": {
            "recipient_addresses_included": False,
            "approver_identity_included": False,
            "private_justification_included": False,
            "raw_report_content_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "exception_store": "requires_cavra_enterprise",
            "renewal_workflow": "requires_cavra_enterprise",
            "revocation_workflow": "requires_cavra_enterprise",
            "review_notification_delivery": "requires_cavra_enterprise",
            "immutable_lifecycle_audit": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_evidence_room_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report evidence rooms."""

    return {
        "schema_version": AISPM_REPORT_EVIDENCE_ROOM_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:45:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "room": {
            "room_ref": "evidence-room:opaque-auditor-review",
            "title": "External Auditor Report Evidence Room",
            "purpose": "Scoped auditor access to curated CAVRA report packages.",
            "status": "active",
            "created_by": "role:grc-admin",
            "created_at": "2026-06-11T08:45:00Z",
            "expires_at": "2026-06-25T08:45:00Z",
        },
        "access_scope": {
            "audience": "external_auditor",
            "recipient_scope": "approved_external_domain",
            "allowed_domain_refs": ["domain-rule:opaque-auditor-domain"],
            "rbac_scope": "evidence_room:read",
            "mfa_required": True,
            "download_allowed": True,
        },
        "artifacts": [
            {
                "artifact_ref": "artifact:opaque-board-pdf",
                "report_id": "pdf_board_pack",
                "format": "pdf",
                "manifest_ref": "export-package:opaque-board-and-audit-pack",
                "digest_ref": "sha256:redacted-public-contract-board-pdf",
                "watermark_required": True,
            },
            {
                "artifact_ref": "artifact:opaque-evidence-workbook",
                "report_id": "xlsx_evidence_workbook",
                "format": "xlsx",
                "manifest_ref": "export-package:opaque-board-and-audit-pack",
                "digest_ref": "sha256:redacted-public-contract-evidence-workbook",
                "watermark_required": True,
            },
        ],
        "controls": {
            "signed_manifest_required": True,
            "time_limited_links": True,
            "access_log_required": True,
            "download_watermark_required": True,
            "revocation_supported": True,
        },
        "access_log": {
            "access_log_ref": "audit:opaque-evidence-room-access-log",
            "last_accessed_at": None,
            "access_count": 0,
            "immutable_store_ref": "enterprise-private://immutable-store/evidence-room-access/opaque-ref",
            "evidence_refs": ["cavra://evidence/redacted/evidence-room-created"],
        },
        "redaction": {
            "recipient_addresses_included": False,
            "auditor_identity_included": False,
            "raw_report_content_included": False,
            "download_urls_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "evidence_room_portal": "requires_cavra_enterprise",
            "auditor_identity_resolution": "requires_cavra_enterprise",
            "signed_download_links": "requires_cavra_enterprise",
            "watermarking_service": "requires_cavra_enterprise",
            "immutable_access_log": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_evidence_room_access_event_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise evidence room access events."""

    return {
        "schema_version": AISPM_REPORT_EVIDENCE_ROOM_ACCESS_EVENT_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T08:51:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "event": {
            "event_ref": "evidence-room-event:opaque-download-approved",
            "room_ref": "evidence-room:opaque-auditor-review",
            "event_type": "download",
            "outcome": "allowed",
            "occurred_at": "2026-06-11T08:50:00Z",
            "source": "evidence_room_portal",
            "correlation_ref": "correlation:opaque-evidence-room-session",
        },
        "actor": {
            "actor_ref": "principal:opaque-external-auditor",
            "actor_type": "external_auditor",
            "identity_redacted": True,
            "organization_ref": "organization:opaque-audit-firm",
            "mfa_verified": True,
            "ip_address_redacted": True,
        },
        "access_decision": {
            "decision": "allow",
            "reason": "approved_domain_mfa_and_active_room",
            "policy_refs": [
                "recipient-policy:opaque-approved-auditor-domain",
                "retention-policy:opaque-report-retention",
            ],
            "expires_at": "2026-06-11T09:05:00Z",
            "revocation_ref": None,
        },
        "artifacts": [
            {
                "artifact_ref": "artifact:opaque-board-pdf",
                "report_id": "pdf_board_pack",
                "format": "pdf",
                "digest_ref": "sha256:redacted-public-contract-board-pdf",
                "watermark_applied": True,
            }
        ],
        "controls": {
            "signed_link_used": True,
            "watermark_required": True,
            "access_logged": True,
            "immutable_audit_required": True,
            "retention_checked": True,
            "license_checked": True,
        },
        "integrity": {
            "event_digest_ref": "sha256:redacted-public-contract-access-event",
            "previous_event_digest_ref": "sha256:redacted-public-contract-room-created",
            "manifest_ref": "export-package:opaque-board-and-audit-pack",
            "audit_store_ref": "enterprise-private://immutable-store/evidence-room-events/opaque-ref",
            "evidence_refs": ["cavra://evidence/redacted/evidence-room-download-approved"],
        },
        "redaction": {
            "recipient_addresses_included": False,
            "auditor_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "identity_resolution": "requires_cavra_enterprise",
            "signed_download_links": "requires_cavra_enterprise",
            "watermarking_service": "requires_cavra_enterprise",
            "immutable_access_event_store": "requires_cavra_enterprise",
            "revocation_workflow": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_incident_packet_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report incident packets."""

    return {
        "schema_version": AISPM_REPORT_INCIDENT_PACKET_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T09:03:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "incident": {
            "incident_ref": "report-incident:opaque-external-access-review",
            "title": "External Report Access Review Packet",
            "incident_type": "evidence_room_access_review",
            "severity": "medium",
            "status": "under_review",
            "opened_at": "2026-06-11T09:00:00Z",
            "detected_by": "evidence_room_monitor",
        },
        "scope": {
            "room_refs": ["evidence-room:opaque-auditor-review"],
            "report_ids": ["pdf_board_pack", "xlsx_evidence_workbook"],
            "artifact_refs": ["artifact:opaque-board-pdf"],
            "policy_refs": [
                "recipient-policy:opaque-approved-auditor-domain",
                "retention-policy:opaque-report-retention",
            ],
        },
        "related_records": {
            "exception_refs": ["report-exception:opaque-external-auditor-domain"],
            "approval_decision_refs": ["approval-decision:opaque-external-send"],
            "access_event_refs": ["evidence-room-event:opaque-download-approved"],
            "delivery_audit_refs": ["delivery-audit:opaque-report-send"],
            "export_package_refs": ["export-package:opaque-board-and-audit-pack"],
        },
        "evidence": {
            "packet_digest_ref": "sha256:redacted-public-contract-incident-packet",
            "manifest_ref": "incident-packet:opaque-manifest",
            "timeline_ref": "incident-timeline:opaque-access-review",
            "immutable_store_ref": "enterprise-private://immutable-store/report-incidents/opaque-ref",
            "evidence_refs": [
                "cavra://evidence/redacted/report-incident-opened",
                "cavra://evidence/redacted/evidence-room-download-approved",
            ],
        },
        "review": {
            "owner_ref": "role:security-leadership",
            "due_at": "2026-06-13T09:00:00Z",
            "approval_required": True,
            "closure_requires_evidence": True,
            "recommended_actions": [
                "verify_auditor_access_scope",
                "confirm_watermarked_artifact_download",
                "review_exception_expiry",
            ],
        },
        "controls": {
            "signed_packet_required": True,
            "immutable_audit_required": True,
            "chain_of_custody_required": True,
            "redaction_review_required": True,
            "post_incident_review_required": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "private_justification_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "incident_packet_builder": "requires_cavra_enterprise",
            "timeline_correlation": "requires_cavra_enterprise",
            "identity_resolution": "requires_cavra_enterprise",
            "signed_packet_generation": "requires_cavra_enterprise",
            "immutable_incident_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_incident_closure_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report incident closure."""

    return {
        "schema_version": AISPM_REPORT_INCIDENT_CLOSURE_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T09:18:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "incident": {
            "incident_ref": "report-incident:opaque-external-access-review",
            "incident_type": "evidence_room_access_review",
            "severity": "medium",
            "final_status": "closed",
            "opened_at": "2026-06-11T09:00:00Z",
            "closed_at": "2026-06-11T09:18:00Z",
        },
        "remediation": {
            "summary": "Verified auditor access scope, watermarking, exception expiry, and packet integrity.",
            "actions": [
                {
                    "action_ref": "remediation:opaque-access-scope-review",
                    "action_type": "access_scope_review",
                    "status": "completed",
                    "evidence_ref": "cavra://evidence/redacted/access-scope-reviewed",
                },
                {
                    "action_ref": "remediation:opaque-exception-expiry-confirmed",
                    "action_type": "exception_expiry_confirmed",
                    "status": "completed",
                    "evidence_ref": "cavra://evidence/redacted/exception-expiry-confirmed",
                },
            ],
        },
        "closure_approval": {
            "approval_ref": "closure-approval:opaque-security-leadership",
            "decision": "approved",
            "approver_role": "security-leadership",
            "decided_at": "2026-06-11T09:16:00Z",
            "conditions": ["retain_packet_for_audit_window", "review_recipient_policy_next_cycle"],
        },
        "lessons_learned": {
            "summary": "External auditor access should stay time-boxed and tied to explicit recipient policy refs.",
            "control_updates": [
                "tighten_external_auditor_room_expiry",
                "require_post_download_exception_review",
            ],
            "runbook_refs": ["runbook:opaque-evidence-room-access-review"],
        },
        "follow_up_tasks": [
            {
                "task_ref": "followup:opaque-recipient-policy-review",
                "owner_ref": "role:grc-admin",
                "due_at": "2026-06-18T09:18:00Z",
                "status": "open",
                "evidence_required": True,
            }
        ],
        "evidence": {
            "closure_digest_ref": "sha256:redacted-public-contract-incident-closure",
            "incident_packet_ref": "incident-packet:opaque-manifest",
            "closure_manifest_ref": "incident-closure:opaque-manifest",
            "immutable_store_ref": "enterprise-private://immutable-store/report-incident-closures/opaque-ref",
            "evidence_refs": [
                "cavra://evidence/redacted/report-incident-closure-approved",
                "cavra://evidence/redacted/access-scope-reviewed",
            ],
        },
        "controls": {
            "closure_approval_required": True,
            "remediation_evidence_required": True,
            "lessons_learned_required": True,
            "follow_up_tracking_required": True,
            "immutable_closure_required": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "private_justification_included": False,
            "customer_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_only",
        },
        "enterprise_boundaries": {
            "closure_workflow": "requires_cavra_enterprise",
            "remediation_tracking": "requires_cavra_enterprise",
            "approval_identity_resolution": "requires_cavra_enterprise",
            "lessons_learned_workflow": "requires_cavra_enterprise",
            "immutable_closure_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_kpi_metrics_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report-center KPI metrics."""

    return {
        "schema_version": AISPM_REPORT_KPI_METRICS_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T09:31:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "window": {
            "window_ref": "metrics-window:opaque-weekly-board-pack",
            "starts_at": "2026-06-04T00:00:00Z",
            "ends_at": "2026-06-11T00:00:00Z",
            "timezone": "UTC",
            "grain": "weekly",
        },
        "summary": {
            "reports_generated": 42,
            "reports_delivered": 39,
            "delivery_success_rate": 0.9286,
            "open_exceptions": 3,
            "open_incidents": 1,
            "audit_readiness_score": 0.91,
        },
        "report_volume": [
            {"report_id": "pdf_board_pack", "generated": 4, "delivered": 4},
            {"report_id": "xlsx_evidence_workbook", "generated": 8, "delivered": 7},
            {"report_id": "signed_json_evidence_packet", "generated": 30, "delivered": 28},
        ],
        "delivery_health": {
            "successful_deliveries": 39,
            "failed_deliveries": 3,
            "retryable_failures": 2,
            "dead_lettered": 1,
            "median_delivery_seconds": 18,
            "p95_delivery_seconds": 94,
        },
        "approval_latency": {
            "approval_required_count": 9,
            "approved_count": 8,
            "pending_count": 1,
            "median_minutes": 34,
            "p95_minutes": 210,
            "breached_slo_count": 1,
        },
        "exception_aging": {
            "active_exceptions": 3,
            "expiring_soon": 1,
            "expired": 0,
            "median_age_hours": 26,
            "oldest_age_hours": 94,
        },
        "evidence_room_access": {
            "active_rooms": 2,
            "access_events": 17,
            "downloads": 6,
            "failed_access_attempts": 1,
            "revocations": 1,
            "watermarked_downloads": 6,
        },
        "incident_closure_slo": {
            "opened": 2,
            "closed": 1,
            "within_slo": 1,
            "breached_slo": 0,
            "median_closure_hours": 4,
        },
        "audit_readiness_trend": [
            {"period": "2026-W22", "score": 0.86, "evidence_gap_count": 7},
            {"period": "2026-W23", "score": 0.91, "evidence_gap_count": 4},
        ],
        "controls": {
            "derived_from_immutable_events": True,
            "retention_aware": True,
            "rbac_scoped": True,
            "tenant_aggregated": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "customer_records_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "aggregate_metrics_only",
        },
        "enterprise_boundaries": {
            "metrics_aggregation_worker": "requires_cavra_enterprise",
            "tenant_metrics_store": "requires_cavra_enterprise",
            "dashboard_projection": "requires_cavra_enterprise",
            "private_trend_history": "requires_cavra_enterprise",
            "rbac_filtering": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_alert_escalation_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report alert escalation."""

    return {
        "schema_version": AISPM_REPORT_ALERT_ESCALATION_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T10:02:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "window": {
            "window_ref": "alert-window:opaque-weekly-board-pack",
            "starts_at": "2026-06-04T00:00:00Z",
            "ends_at": "2026-06-11T00:00:00Z",
            "timezone": "UTC",
        },
        "alert_policy": {
            "policy_ref": "report-alert-policy:opaque-cso-default",
            "status": "active",
            "owner_role": "security_operations",
            "evaluation_cadence": "5m",
            "suppression_window_minutes": 30,
            "requires_acknowledgement": True,
        },
        "trigger_rules": [
            {
                "rule_id": "failed-delivery-spike",
                "metric": "delivery_health.failed_deliveries",
                "operator": ">=",
                "threshold": 3,
                "severity": "high",
                "owner_role": "platform_security",
                "route_ref": "route:opaque-platform-security",
            },
            {
                "rule_id": "evidence-room-suspicious-access",
                "metric": "evidence_room_access.failed_access_attempts",
                "operator": ">=",
                "threshold": 1,
                "severity": "critical",
                "owner_role": "security_operations",
                "route_ref": "route:opaque-soc",
            },
            {
                "rule_id": "aging-exception-breach",
                "metric": "exception_aging.oldest_age_hours",
                "operator": ">",
                "threshold": 72,
                "severity": "medium",
                "owner_role": "grc",
                "route_ref": "route:opaque-grc",
            },
            {
                "rule_id": "approval-latency-slo-breach",
                "metric": "approval_latency.breached_slo_count",
                "operator": ">=",
                "threshold": 1,
                "severity": "medium",
                "owner_role": "security_leadership",
                "route_ref": "route:opaque-security-leadership",
            },
        ],
        "evaluations": [
            {
                "evaluation_ref": "alert-eval:opaque-failed-delivery-spike",
                "rule_id": "failed-delivery-spike",
                "status": "triggered",
                "observed_value": 3,
                "severity": "high",
                "triggered_at": "2026-06-11T09:45:00Z",
                "correlation_ref": "metric-window:opaque-weekly-board-pack",
            },
            {
                "evaluation_ref": "alert-eval:opaque-evidence-room-access",
                "rule_id": "evidence-room-suspicious-access",
                "status": "triggered",
                "observed_value": 1,
                "severity": "critical",
                "triggered_at": "2026-06-11T09:48:00Z",
                "correlation_ref": "access-event:opaque-failed-policy",
            },
            {
                "evaluation_ref": "alert-eval:opaque-aging-exception",
                "rule_id": "aging-exception-breach",
                "status": "suppressed",
                "observed_value": 94,
                "severity": "medium",
                "triggered_at": "2026-06-11T09:50:00Z",
                "correlation_ref": "exception:opaque-expiring-report-send",
            },
        ],
        "routing": {
            "primary_channel": "security_operations_queue",
            "secondary_channel": "email_digest",
            "integration_refs": [
                "integration:opaque-siem",
                "integration:opaque-itsm",
            ],
            "recipient_addresses_redacted": True,
            "external_delivery_requires_approval": True,
        },
        "escalation": {
            "current_level": 2,
            "max_level": 3,
            "next_escalation_at": "2026-06-11T10:15:00Z",
            "levels": [
                {
                    "level": 1,
                    "owner_role": "platform_security",
                    "timeout_minutes": 15,
                    "action": "notify",
                },
                {
                    "level": 2,
                    "owner_role": "security_operations",
                    "timeout_minutes": 30,
                    "action": "page_and_create_incident",
                },
                {
                    "level": 3,
                    "owner_role": "ciso",
                    "timeout_minutes": 60,
                    "action": "executive_escalation",
                },
            ],
        },
        "acknowledgement": {
            "ack_required": True,
            "ack_status": "pending",
            "ack_due_at": "2026-06-11T10:20:00Z",
            "ack_owner_role": "security_operations",
            "ack_evidence_ref": "cavra://evidence/redacted/report-alert-ack-required",
        },
        "incident_linkage": {
            "incident_required": True,
            "incident_ref": "incident:opaque-report-delivery-and-access-review",
            "incident_packet_ref": "incident-packet:opaque-report-alert",
            "closure_required": True,
        },
        "evidence": {
            "metrics_ref": "metrics:opaque-weekly-board-pack",
            "alert_digest_ref": "digest:opaque-report-alert",
            "routing_audit_ref": "audit:opaque-report-alert-routing",
            "immutable_store_ref": "immutable:opaque-report-alert",
            "evidence_refs": [
                "cavra://evidence/redacted/report-alert-triggered",
                "cavra://evidence/redacted/report-alert-routed",
            ],
        },
        "controls": {
            "derived_from_kpi_metrics": True,
            "immutable_alert_required": True,
            "acknowledgement_required": True,
            "escalation_policy_required": True,
            "suppression_audited": True,
            "recipient_policy_enforced": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "metadata_and_aggregate_metrics_only",
        },
        "enterprise_boundaries": {
            "alert_evaluator": "requires_cavra_enterprise",
            "routing_engine": "requires_cavra_enterprise",
            "escalation_worker": "requires_cavra_enterprise",
            "notification_delivery": "requires_cavra_enterprise",
            "incident_creation": "requires_cavra_enterprise",
            "acknowledgement_store": "requires_cavra_enterprise",
            "suppression_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_alert_operations_dashboard_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report alert operations."""

    return {
        "schema_version": AISPM_REPORT_ALERT_OPERATIONS_DASHBOARD_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T10:26:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "dashboard": {
            "dashboard_ref": "report-alert-dashboard:opaque-cso-operations",
            "status": "degraded",
            "open_alerts": 5,
            "critical_open": 1,
            "high_open": 2,
            "overdue_acknowledgements": 2,
            "suppressed_alerts": 3,
            "linked_incidents": 2,
            "unlinked_incidents": 1,
            "mean_time_to_ack_minutes": 22,
        },
        "queues": [
            {
                "queue": "alert_evaluation",
                "depth": 7,
                "oldest_age_minutes": 4,
                "status": "healthy",
            },
            {
                "queue": "routing",
                "depth": 3,
                "oldest_age_minutes": 9,
                "status": "degraded",
            },
            {
                "queue": "escalation",
                "depth": 2,
                "oldest_age_minutes": 18,
                "status": "degraded",
            },
            {
                "queue": "acknowledgement",
                "depth": 5,
                "oldest_age_minutes": 42,
                "status": "breached",
            },
            {
                "queue": "incident_creation",
                "depth": 1,
                "oldest_age_minutes": 11,
                "status": "healthy",
            },
        ],
        "active_alerts": [
            {
                "alert_ref": "alert:opaque-evidence-room-access",
                "rule_id": "evidence-room-suspicious-access",
                "severity": "critical",
                "status": "escalated",
                "owner_role": "security_operations",
                "route_ref": "route:opaque-soc",
                "opened_at": "2026-06-11T09:48:00Z",
                "age_minutes": 38,
                "ack_due_at": "2026-06-11T10:20:00Z",
                "incident_ref": "incident:opaque-report-delivery-and-access-review",
            },
            {
                "alert_ref": "alert:opaque-failed-delivery-spike",
                "rule_id": "failed-delivery-spike",
                "severity": "high",
                "status": "ack_overdue",
                "owner_role": "platform_security",
                "route_ref": "route:opaque-platform-security",
                "opened_at": "2026-06-11T09:45:00Z",
                "age_minutes": 41,
                "ack_due_at": "2026-06-11T10:15:00Z",
                "incident_ref": "incident:opaque-report-delivery-and-access-review",
            },
        ],
        "escalation_health": {
            "level_1_active": 2,
            "level_2_active": 2,
            "level_3_active": 1,
            "next_escalation_due_at": "2026-06-11T10:30:00Z",
            "breached_escalations": 1,
        },
        "acknowledgement_slos": {
            "required_count": 5,
            "pending_count": 3,
            "overdue_count": 2,
            "acknowledged_count": 2,
            "median_ack_minutes": 22,
            "p95_ack_minutes": 64,
        },
        "suppression_summary": {
            "active_suppressions": 3,
            "expired_suppressions": 1,
            "requires_review": 1,
            "suppression_audit_coverage": 1.0,
        },
        "incident_linkage_health": {
            "linked_alerts": 4,
            "unlinked_alerts": 1,
            "open_incidents": 2,
            "closure_required": 2,
            "stale_incident_count": 0,
        },
        "routing_health": [
            {
                "channel": "security_operations_queue",
                "status": "healthy",
                "pending_routes": 1,
                "failed_routes": 0,
            },
            {
                "channel": "email_digest",
                "status": "degraded",
                "pending_routes": 2,
                "failed_routes": 1,
            },
            {
                "channel": "itsm",
                "status": "healthy",
                "pending_routes": 0,
                "failed_routes": 0,
            },
        ],
        "evidence": {
            "dashboard_digest_ref": "digest:opaque-report-alert-dashboard",
            "latest_alert_ref": "alert:opaque-evidence-room-access",
            "latest_routing_audit_ref": "audit:opaque-report-alert-routing",
            "immutable_store_ref": "immutable:opaque-report-alert-dashboard",
            "evidence_refs": [
                "cavra://evidence/redacted/report-alert-dashboard-rendered",
                "cavra://evidence/redacted/report-alert-queue-health",
            ],
        },
        "controls": {
            "derived_from_alert_events": True,
            "rbac_scoped": True,
            "retention_aware": True,
            "immutable_dashboard_required": True,
            "recipient_policy_enforced": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "alert_operations_metadata_only",
        },
        "enterprise_boundaries": {
            "dashboard_projection": "requires_cavra_enterprise",
            "queue_persistence": "requires_cavra_enterprise",
            "alert_event_store": "requires_cavra_enterprise",
            "routing_health_checks": "requires_cavra_enterprise",
            "acknowledgement_store": "requires_cavra_enterprise",
            "incident_linkage_store": "requires_cavra_enterprise",
            "suppression_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_alert_drilldown_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report alert drilldowns."""

    return {
        "schema_version": AISPM_REPORT_ALERT_DRILLDOWN_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T10:52:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "alert": {
            "alert_ref": "alert:opaque-evidence-room-access",
            "rule_id": "evidence-room-suspicious-access",
            "title": "Suspicious Evidence Room Access",
            "severity": "critical",
            "status": "escalated",
            "opened_at": "2026-06-11T09:48:00Z",
            "age_minutes": 64,
            "owner_role": "security_operations",
            "source_metric": "evidence_room_access.failed_access_attempts",
            "observed_value": 1,
            "threshold": 1,
        },
        "timeline": [
            {
                "event_ref": "alert-event:opaque-detected",
                "event_type": "detected",
                "occurred_at": "2026-06-11T09:48:00Z",
                "actor_role": "system",
                "status": "completed",
                "summary": "Alert rule evaluated from aggregate evidence-room access metrics.",
                "evidence_ref": "cavra://evidence/redacted/report-alert-triggered",
            },
            {
                "event_ref": "alert-event:opaque-routed",
                "event_type": "routed",
                "occurred_at": "2026-06-11T09:49:00Z",
                "actor_role": "routing_engine",
                "status": "completed",
                "summary": "Alert routed to security operations and incident queue.",
                "evidence_ref": "cavra://evidence/redacted/report-alert-routed",
            },
            {
                "event_ref": "alert-event:opaque-escalated",
                "event_type": "escalated",
                "occurred_at": "2026-06-11T10:18:00Z",
                "actor_role": "escalation_worker",
                "status": "completed",
                "summary": "Acknowledgement SLO breached and alert moved to level 2.",
                "evidence_ref": "cavra://evidence/redacted/report-alert-escalated",
            },
        ],
        "routing": [
            {
                "route_ref": "route:opaque-soc",
                "channel": "security_operations_queue",
                "owner_role": "security_operations",
                "status": "delivered",
                "delivered_at": "2026-06-11T09:49:00Z",
            },
            {
                "route_ref": "route:opaque-itsm",
                "channel": "itsm",
                "owner_role": "platform_security",
                "status": "created",
                "delivered_at": "2026-06-11T09:50:00Z",
            },
        ],
        "acknowledgement_history": [
            {
                "ack_ref": "ack:opaque-alert-required",
                "status": "pending",
                "owner_role": "security_operations",
                "due_at": "2026-06-11T10:20:00Z",
                "decision_ref": "decision:opaque-ack-pending",
                "evidence_ref": "cavra://evidence/redacted/report-alert-ack-required",
            },
            {
                "ack_ref": "ack:opaque-alert-overdue",
                "status": "overdue",
                "owner_role": "security_operations",
                "due_at": "2026-06-11T10:20:00Z",
                "decision_ref": "decision:opaque-ack-overdue",
                "evidence_ref": "cavra://evidence/redacted/report-alert-ack-overdue",
            },
        ],
        "suppression_history": [
            {
                "suppression_ref": "suppression:opaque-related-aging-exception",
                "status": "active",
                "reason_code": "duplicate_signal",
                "owner_role": "grc",
                "expires_at": "2026-06-11T12:00:00Z",
                "audit_ref": "audit:opaque-alert-suppression",
            }
        ],
        "escalation_path": {
            "current_level": 2,
            "next_level": 3,
            "next_escalation_at": "2026-06-11T11:18:00Z",
            "levels": [
                {"level": 1, "owner_role": "platform_security", "status": "completed"},
                {"level": 2, "owner_role": "security_operations", "status": "active"},
                {"level": 3, "owner_role": "ciso", "status": "pending"},
            ],
        },
        "linked_incident": {
            "incident_required": True,
            "incident_ref": "incident:opaque-report-delivery-and-access-review",
            "incident_packet_ref": "incident-packet:opaque-report-alert",
            "closure_ref": "incident-closure:opaque-pending",
            "closure_required": True,
            "status": "under_review",
        },
        "evidence_chain": {
            "metrics_ref": "metrics:opaque-weekly-board-pack",
            "alert_digest_ref": "digest:opaque-report-alert",
            "routing_audit_ref": "audit:opaque-report-alert-routing",
            "timeline_digest_ref": "digest:opaque-alert-timeline",
            "immutable_store_ref": "immutable:opaque-report-alert-drilldown",
            "evidence_refs": [
                "cavra://evidence/redacted/report-alert-triggered",
                "cavra://evidence/redacted/report-alert-routed",
                "cavra://evidence/redacted/report-alert-escalated",
            ],
        },
        "controls": {
            "derived_from_alert_events": True,
            "timeline_ordered": True,
            "rbac_scoped": True,
            "retention_aware": True,
            "immutable_drilldown_required": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "single_alert_metadata_only",
        },
        "enterprise_boundaries": {
            "drilldown_projection": "requires_cavra_enterprise",
            "timeline_event_store": "requires_cavra_enterprise",
            "routing_detail_store": "requires_cavra_enterprise",
            "acknowledgement_store": "requires_cavra_enterprise",
            "suppression_store": "requires_cavra_enterprise",
            "incident_linkage_store": "requires_cavra_enterprise",
            "evidence_chain_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_alert_remediation_plan_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise report alert remediation plans."""

    return {
        "schema_version": AISPM_REPORT_ALERT_REMEDIATION_PLAN_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T11:18:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "plan": {
            "plan_ref": "remediation-plan:opaque-report-alert",
            "status": "in_progress",
            "priority": "critical",
            "owner_role": "security_operations",
            "opened_at": "2026-06-11T10:22:00Z",
            "due_at": "2026-06-12T10:22:00Z",
            "source_alert_ref": "alert:opaque-evidence-room-access",
            "source_incident_ref": "incident:opaque-report-delivery-and-access-review",
        },
        "scope": {
            "finding_type": "evidence_room_access_review",
            "affected_report_refs": ["report:opaque-board-pack"],
            "affected_evidence_room_refs": ["evidence-room:opaque-auditor-room"],
            "affected_integration_refs": ["integration:opaque-itsm"],
            "customer_records_redacted": True,
        },
        "tasks": [
            {
                "task_ref": "task:opaque-revoke-access",
                "title": "Revoke stale evidence-room access",
                "owner_role": "security_operations",
                "status": "completed",
                "due_at": "2026-06-11T12:00:00Z",
                "approval_required": False,
                "evidence_required": True,
                "evidence_ref": "cavra://evidence/redacted/evidence-room-access-revoked",
            },
            {
                "task_ref": "task:opaque-review-recipient-policy",
                "title": "Review recipient and evidence-room policy",
                "owner_role": "grc",
                "status": "in_progress",
                "due_at": "2026-06-12T09:00:00Z",
                "approval_required": True,
                "evidence_required": True,
                "evidence_ref": "cavra://evidence/redacted/recipient-policy-review",
            },
            {
                "task_ref": "task:opaque-update-alert-threshold",
                "title": "Tune suspicious access alert threshold",
                "owner_role": "platform_security",
                "status": "pending",
                "due_at": "2026-06-12T10:00:00Z",
                "approval_required": True,
                "evidence_required": True,
                "evidence_ref": "cavra://evidence/redacted/alert-threshold-update",
            },
        ],
        "approval_requirements": [
            {
                "approval_ref": "approval:opaque-recipient-policy-review",
                "approval_type": "policy_change",
                "approver_role": "security_leadership",
                "status": "pending",
                "due_at": "2026-06-12T08:00:00Z",
            },
            {
                "approval_ref": "approval:opaque-closure",
                "approval_type": "plan_closure",
                "approver_role": "ciso",
                "status": "not_requested",
                "due_at": "2026-06-12T10:22:00Z",
            },
        ],
        "closure_criteria": {
            "all_tasks_complete": True,
            "required_approvals_complete": True,
            "evidence_chain_complete": True,
            "incident_closure_required": True,
            "post_incident_review_required": True,
        },
        "control_updates": [
            {
                "control_ref": "control:opaque-evidence-room-access",
                "update_type": "policy_threshold",
                "owner_role": "platform_security",
                "status": "planned",
                "evidence_ref": "cavra://evidence/redacted/control-threshold-update",
            },
            {
                "control_ref": "control:opaque-recipient-governance",
                "update_type": "recipient_policy",
                "owner_role": "grc",
                "status": "in_progress",
                "evidence_ref": "cavra://evidence/redacted/recipient-policy-control-update",
            },
        ],
        "communications": {
            "internal_update_required": True,
            "executive_update_required": True,
            "customer_notification_required": False,
            "external_message_ref": "message-template:opaque-not-required",
        },
        "evidence": {
            "plan_digest_ref": "digest:opaque-remediation-plan",
            "alert_drilldown_ref": "alert-drilldown:opaque-evidence-room-access",
            "incident_packet_ref": "incident-packet:opaque-report-alert",
            "closure_manifest_ref": "closure-manifest:opaque-pending",
            "immutable_store_ref": "immutable:opaque-remediation-plan",
            "evidence_refs": [
                "cavra://evidence/redacted/remediation-plan-created",
                "cavra://evidence/redacted/evidence-room-access-revoked",
                "cavra://evidence/redacted/recipient-policy-review",
            ],
        },
        "controls": {
            "task_owners_required": True,
            "approval_gates_enforced": True,
            "closure_criteria_required": True,
            "post_incident_control_updates_required": True,
            "immutable_plan_required": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "remediation_metadata_only",
        },
        "enterprise_boundaries": {
            "remediation_workflow": "requires_cavra_enterprise",
            "task_store": "requires_cavra_enterprise",
            "approval_workflow": "requires_cavra_enterprise",
            "owner_resolution": "requires_cavra_enterprise",
            "control_update_workflow": "requires_cavra_enterprise",
            "notification_workflow": "requires_cavra_enterprise",
            "immutable_plan_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_alert_remediation_closure_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise alert remediation closure."""

    return {
        "schema_version": AISPM_REPORT_ALERT_REMEDIATION_CLOSURE_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T11:42:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "closure": {
            "closure_ref": "remediation-closure:opaque-report-alert",
            "plan_ref": "remediation-plan:opaque-report-alert",
            "source_alert_ref": "alert:opaque-evidence-room-access",
            "source_incident_ref": "incident:opaque-report-delivery-and-access-review",
            "final_status": "closed",
            "closed_at": "2026-06-12T10:12:00Z",
            "owner_role": "security_operations",
            "residual_risk_level": "low",
        },
        "completed_tasks": [
            {
                "task_ref": "task:opaque-revoke-access",
                "title": "Revoke stale evidence-room access",
                "owner_role": "security_operations",
                "completed_at": "2026-06-11T11:36:00Z",
                "evidence_ref": "cavra://evidence/redacted/evidence-room-access-revoked",
                "approval_ref": "approval:opaque-not-required",
            },
            {
                "task_ref": "task:opaque-review-recipient-policy",
                "title": "Review recipient and evidence-room policy",
                "owner_role": "grc",
                "completed_at": "2026-06-12T08:35:00Z",
                "evidence_ref": "cavra://evidence/redacted/recipient-policy-reviewed",
                "approval_ref": "approval:opaque-recipient-policy-review",
            },
        ],
        "final_approvals": [
            {
                "approval_ref": "approval:opaque-closure",
                "approval_type": "plan_closure",
                "approver_role": "ciso",
                "decision": "approved",
                "decided_at": "2026-06-12T09:45:00Z",
                "evidence_ref": "cavra://evidence/redacted/remediation-closure-approved",
            }
        ],
        "control_updates": [
            {
                "control_ref": "control:opaque-evidence-room-access",
                "update_type": "policy_threshold",
                "owner_role": "platform_security",
                "final_status": "completed",
                "evidence_ref": "cavra://evidence/redacted/control-threshold-updated",
            },
            {
                "control_ref": "control:opaque-recipient-governance",
                "update_type": "recipient_policy",
                "owner_role": "grc",
                "final_status": "completed",
                "evidence_ref": "cavra://evidence/redacted/recipient-policy-control-updated",
            },
        ],
        "residual_risk": {
            "risk_level": "low",
            "accepted": True,
            "accepted_by_role": "ciso",
            "acceptance_ref": "risk-acceptance:opaque-remediation-closure",
            "review_due_at": "2026-07-12T10:12:00Z",
            "rationale_summary": "Compensating controls and revised evidence-room policy reduce residual risk.",
        },
        "post_incident_review": {
            "review_ref": "post-incident-review:opaque-report-alert",
            "completed": True,
            "completed_at": "2026-06-12T10:00:00Z",
            "facilitator_role": "security_leadership",
            "lessons_learned_refs": ["lesson:opaque-evidence-room-review-window"],
            "follow_up_required": True,
        },
        "communications": {
            "internal_update_sent": True,
            "executive_update_sent": True,
            "customer_notification_required": False,
            "customer_notification_sent": False,
            "communication_ref": "communication:opaque-remediation-closure-summary",
        },
        "evidence": {
            "closure_digest_ref": "digest:opaque-remediation-closure",
            "remediation_plan_ref": "remediation-plan:opaque-report-alert",
            "alert_drilldown_ref": "alert-drilldown:opaque-evidence-room-access",
            "incident_packet_ref": "incident-packet:opaque-report-alert",
            "closure_manifest_ref": "closure-manifest:opaque-remediation-complete",
            "immutable_store_ref": "immutable:opaque-remediation-closure",
            "evidence_refs": [
                "cavra://evidence/redacted/remediation-plan-completed",
                "cavra://evidence/redacted/remediation-closure-approved",
                "cavra://evidence/redacted/post-incident-review-completed",
            ],
        },
        "controls": {
            "all_tasks_completed": True,
            "final_approval_required": True,
            "residual_risk_recorded": True,
            "post_incident_review_recorded": True,
            "immutable_closure_required": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "remediation_closure_metadata_only",
        },
        "enterprise_boundaries": {
            "closure_workflow": "requires_cavra_enterprise",
            "approval_identity_resolution": "requires_cavra_enterprise",
            "residual_risk_store": "requires_cavra_enterprise",
            "post_incident_review_store": "requires_cavra_enterprise",
            "communication_delivery": "requires_cavra_enterprise",
            "immutable_closure_store": "requires_cavra_enterprise",
            "evidence_chain_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_remediation_closure_operations_dashboard_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise remediation closure operations."""

    return {
        "schema_version": AISPM_REPORT_REMEDIATION_CLOSURE_OPERATIONS_DASHBOARD_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T12:04:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "dashboard": {
            "dashboard_ref": "dashboard:opaque-remediation-closure-ops",
            "status": "degraded",
            "closure_readiness": "attention_required",
            "closed_plans": 42,
            "open_plans": 9,
            "overdue_tasks": 3,
            "overdue_closures": 2,
            "closures_due_soon": 4,
            "mean_time_to_close_hours": 18.4,
            "p95_time_to_close_hours": 46.2,
        },
        "throughput": {
            "period": "last_30_days",
            "opened": 51,
            "closed": 42,
            "reopened": 2,
            "closure_rate": 0.82,
            "sla_met_count": 37,
            "sla_breached_count": 5,
        },
        "queues": [
            {
                "queue": "closure_approval",
                "depth": 4,
                "oldest_age_hours": 18.5,
                "status": "degraded",
            },
            {
                "queue": "residual_risk_review",
                "depth": 2,
                "oldest_age_hours": 12.0,
                "status": "healthy",
            },
            {
                "queue": "post_incident_review",
                "depth": 3,
                "oldest_age_hours": 30.0,
                "status": "degraded",
            },
            {
                "queue": "evidence_finalization",
                "depth": 1,
                "oldest_age_hours": 8.0,
                "status": "healthy",
            },
        ],
        "residual_risk_aging": {
            "total_acceptances": 11,
            "low": 7,
            "medium": 3,
            "high": 1,
            "critical": 0,
            "overdue_reviews": 1,
            "next_review_due_at": "2026-06-18T09:00:00Z",
        },
        "approval_bottlenecks": [
            {
                "approver_role": "ciso",
                "pending_count": 2,
                "oldest_age_hours": 18.5,
                "p95_age_hours": 20.0,
                "status": "degraded",
            },
            {
                "approver_role": "security_leadership",
                "pending_count": 2,
                "oldest_age_hours": 9.0,
                "p95_age_hours": 11.5,
                "status": "healthy",
            },
        ],
        "post_incident_review_health": {
            "required": 18,
            "completed": 15,
            "overdue": 2,
            "completion_rate": 0.83,
            "follow_up_required": 6,
        },
        "closure_slo": {
            "target_hours": 24,
            "met_count": 37,
            "breached_count": 5,
            "at_risk_count": 4,
            "status": "degraded",
        },
        "recent_closures": [
            {
                "closure_ref": "remediation-closure:opaque-report-alert",
                "plan_ref": "remediation-plan:opaque-report-alert",
                "source_alert_ref": "alert:opaque-evidence-room-access",
                "final_status": "closed",
                "owner_role": "security_operations",
                "residual_risk_level": "low",
                "closed_at": "2026-06-12T10:12:00Z",
                "evidence_ref": "cavra://evidence/redacted/remediation-closure-approved",
            }
        ],
        "evidence": {
            "dashboard_digest_ref": "digest:opaque-remediation-closure-ops",
            "latest_closure_ref": "remediation-closure:opaque-report-alert",
            "latest_plan_ref": "remediation-plan:opaque-report-alert",
            "immutable_store_ref": "immutable:opaque-remediation-closure-ops",
            "evidence_refs": [
                "cavra://evidence/redacted/remediation-closure-dashboard-generated",
                "cavra://evidence/redacted/remediation-closure-slo-evaluated",
                "cavra://evidence/redacted/residual-risk-review-aging-evaluated",
            ],
        },
        "controls": {
            "derived_from_closure_events": True,
            "rbac_scoped": True,
            "retention_aware": True,
            "immutable_dashboard_required": True,
            "slo_policy_enforced": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "remediation_closure_operations_metadata_only",
        },
        "enterprise_boundaries": {
            "closure_operations_projection": "requires_cavra_enterprise",
            "closure_event_store": "requires_cavra_enterprise",
            "slo_evaluator": "requires_cavra_enterprise",
            "residual_risk_review_store": "requires_cavra_enterprise",
            "approval_queue_store": "requires_cavra_enterprise",
            "post_incident_review_store": "requires_cavra_enterprise",
            "immutable_dashboard_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_remediation_closure_executive_digest_contract() -> dict[str, Any]:
    """Return a public-safe sample contract for Enterprise remediation closure executive digests."""

    return {
        "schema_version": AISPM_REPORT_REMEDIATION_CLOSURE_EXECUTIVE_DIGEST_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T12:26:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "digest": {
            "digest_ref": "digest:opaque-remediation-closure-executive",
            "title": "Remediation Closure Executive Digest",
            "period": "last_30_days",
            "audiences": ["cso", "ciso", "board", "audit"],
            "status": "attention_required",
            "prepared_at": "2026-06-11T12:26:00Z",
            "visibility": "public_safe_metadata",
        },
        "executive_summary": {
            "headline": "Most remediation plans closed within SLO; residual-risk review needs attention.",
            "closure_readiness": "attention_required",
            "key_message": "Closure throughput is healthy, but overdue closure approvals and one residual-risk review require CSO follow-up.",
            "material_risk": "Residual-risk review aging could weaken audit readiness if not cleared before the next board pack.",
            "recommended_action": "Clear CISO closure approvals and complete overdue residual-risk review within the next governance window.",
        },
        "metrics": {
            "closed_plans": 42,
            "open_plans": 9,
            "overdue_closures": 2,
            "overdue_tasks": 3,
            "closure_rate": 0.82,
            "sla_breached_count": 5,
            "residual_risk_acceptances": 11,
            "overdue_residual_risk_reviews": 1,
            "post_incident_review_completion_rate": 0.83,
        },
        "risk_summary": {
            "residual_risk_level": "medium",
            "high_or_critical_residual_risk_count": 1,
            "top_risk_themes": [
                "closure approval latency",
                "residual-risk review aging",
                "post-incident follow-up backlog",
            ],
            "accepted_risk_review_due_at": "2026-06-18T09:00:00Z",
        },
        "remediation_status": {
            "closure_approval_queue": "degraded",
            "residual_risk_review_queue": "healthy",
            "post_incident_review_queue": "degraded",
            "evidence_finalization_queue": "healthy",
            "closure_slo_status": "degraded",
        },
        "board_talking_points": [
            "CAVRA closed 42 remediation plans in the reporting period.",
            "Five closure SLO breaches require governance review.",
            "One accepted residual-risk item is overdue for review.",
            "Post-incident review completion is 83 percent for the reporting period.",
        ],
        "audit_readiness": {
            "auditor_ready": False,
            "immutable_evidence_available": True,
            "exceptions_count": 2,
            "report_package_refs": [
                "report-package:opaque-board-pack",
                "report-package:opaque-audit-summary",
            ],
            "evidence_refs": [
                "cavra://evidence/redacted/remediation-closure-dashboard-generated",
                "cavra://evidence/redacted/remediation-closure-slo-evaluated",
                "cavra://evidence/redacted/residual-risk-review-aging-evaluated",
            ],
        },
        "distribution": {
            "formats": ["pdf", "docx", "html", "signed_json"],
            "delivery_modes": ["portal", "email", "grc_upload"],
            "approval_required": True,
            "recipient_policy_ref": "recipient-policy:opaque-executive-digest",
        },
        "evidence": {
            "digest_ref": "digest:opaque-remediation-closure-executive",
            "operations_dashboard_ref": "dashboard:opaque-remediation-closure-ops",
            "latest_closure_ref": "remediation-closure:opaque-report-alert",
            "immutable_store_ref": "immutable:opaque-remediation-closure-executive",
            "evidence_refs": [
                "cavra://evidence/redacted/remediation-closure-executive-digest-generated",
                "cavra://evidence/redacted/remediation-closure-dashboard-generated",
                "cavra://evidence/redacted/board-digest-approval-required",
            ],
        },
        "controls": {
            "derived_from_closure_operations": True,
            "rbac_scoped": True,
            "executive_approval_required": True,
            "immutable_digest_required": True,
            "recipient_policy_enforced": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "board_member_identity_included": False,
            "secrets_included": False,
            "payload_handling": "remediation_closure_executive_digest_metadata_only",
        },
        "enterprise_boundaries": {
            "digest_renderer": "requires_cavra_enterprise",
            "board_pack_renderer": "requires_cavra_enterprise",
            "tenant_metrics_store": "requires_cavra_enterprise",
            "report_delivery": "requires_cavra_enterprise",
            "approval_workflow": "requires_cavra_enterprise",
            "evidence_package_builder": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_remediation_closure_digest_distribution_contract() -> dict[str, Any]:
    """Return a public-safe contract for Enterprise closure digest distribution."""

    return {
        "schema_version": AISPM_REPORT_REMEDIATION_CLOSURE_DIGEST_DISTRIBUTION_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-11T12:44:00Z",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "distribution": {
            "distribution_ref": "distribution:opaque-remediation-closure-executive",
            "digest_ref": "digest:opaque-remediation-closure-executive",
            "status": "approval_pending",
            "delivery_window": "board_pack_cycle",
            "prepared_at": "2026-06-11T12:44:00Z",
            "send_after": "2026-06-11T14:00:00Z",
            "expires_at": "2026-06-18T14:00:00Z",
        },
        "approval": {
            "approval_ref": "approval:opaque-board-digest-send",
            "approval_type": "executive_digest_distribution",
            "approver_role": "ciso",
            "status": "pending",
            "required_before_send": True,
            "due_at": "2026-06-11T13:30:00Z",
            "evidence_ref": "cavra://evidence/redacted/board-digest-approval-requested",
        },
        "recipient_governance": {
            "recipient_policy_ref": "recipient-policy:opaque-executive-digest",
            "allowed_audiences": ["cso", "ciso", "board", "audit"],
            "external_recipients_allowed": False,
            "domain_allowlist_required": True,
            "rbac_scope_required": True,
            "recipient_addresses_redacted": True,
        },
        "delivery_plan": {
            "formats": ["pdf", "docx", "html", "signed_json"],
            "delivery_modes": ["portal", "email", "grc_upload"],
            "provider_refs": ["provider:opaque-email", "provider:opaque-grc"],
            "retry_policy_ref": "retry-policy:opaque-executive-digest",
            "watermark_required": True,
            "signed_manifest_required": True,
        },
        "delivery_status": [
            {
                "channel": "portal",
                "status": "ready",
                "attempt_count": 0,
                "last_attempt_at": "2026-06-11T12:44:00Z",
                "delivery_evidence_ref": "cavra://evidence/redacted/portal-package-prepared",
            },
            {
                "channel": "email",
                "status": "blocked_pending_approval",
                "attempt_count": 0,
                "last_attempt_at": "2026-06-11T12:44:00Z",
                "delivery_evidence_ref": (
                    "cavra://evidence/redacted/email-send-blocked-pending-approval"
                ),
            },
            {
                "channel": "grc_upload",
                "status": "ready",
                "attempt_count": 0,
                "last_attempt_at": "2026-06-11T12:44:00Z",
                "delivery_evidence_ref": "cavra://evidence/redacted/grc-package-prepared",
            },
        ],
        "send_evidence": {
            "distribution_digest_ref": "digest:opaque-remediation-closure-distribution",
            "executive_digest_ref": "digest:opaque-remediation-closure-executive",
            "manifest_ref": "manifest:opaque-executive-digest-distribution",
            "immutable_store_ref": "immutable:opaque-remediation-closure-distribution",
            "evidence_refs": [
                "cavra://evidence/redacted/board-digest-approval-requested",
                "cavra://evidence/redacted/portal-package-prepared",
                "cavra://evidence/redacted/email-send-blocked-pending-approval",
            ],
        },
        "controls": {
            "approval_before_send_required": True,
            "recipient_policy_enforced": True,
            "domain_allowlist_enforced": True,
            "rbac_scoped": True,
            "immutable_send_evidence_required": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "payload_handling": "remediation_closure_digest_distribution_metadata_only",
        },
        "enterprise_boundaries": {
            "approval_workflow": "requires_cavra_enterprise",
            "recipient_directory": "requires_cavra_enterprise",
            "delivery_provider": "requires_cavra_enterprise",
            "signed_package_builder": "requires_cavra_enterprise",
            "send_worker": "requires_cavra_enterprise",
            "delivery_audit_store": "requires_cavra_enterprise",
            "license_enforcement": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_center_trial_validation_packet_contract() -> dict[str, Any]:
    """Return a public-safe Enterprise Trial validation packet for Report Center."""

    return {
        "schema_version": AISPM_REPORT_CENTER_TRIAL_VALIDATION_PACKET_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-12T09:30:00Z",
        "trial_ref": "trial:opaque-report-center-evaluator",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "validation_summary": {
            "status": "ready_for_evaluator_review",
            "passed_paths": 10,
            "warning_paths": 0,
            "blocked_paths": 0,
            "failed_paths": 0,
            "evidence_packet_ref": "evidence-packet:opaque-report-center-trial",
            "validated_at": "2026-06-12T09:30:00Z",
        },
        "package_under_test": {
            "package_ref": "package:opaque-cavra-enterprise-trial",
            "version": "2026.06.12",
            "image_ref": "ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.12",
            "license_status": "trial_active",
            "license_validation_mode": "hosted_validation",
            "source_included": False,
        },
        "validation_paths": [
            {
                "path_id": "setup_wizard",
                "title": "Setup wizard saves tenant report settings",
                "status": "passed",
                "assertions": [
                    "provider references saved",
                    "raw credential values excluded",
                    "tenant report settings persisted",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-setup-settings-saved",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-setup-wizard-contract",
                ],
            },
            {
                "path_id": "render_report",
                "title": "Report rendering produces artifact metadata",
                "status": "passed",
                "assertions": [
                    "pdf metadata produced",
                    "docx metadata produced",
                    "html metadata produced",
                    "signed json metadata produced",
                    "artifact digests available",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-render-metadata-produced",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-export-package-manifest",
                ],
            },
            {
                "path_id": "send_blocked_by_policy",
                "title": "Send blocks when approval or recipient policy is missing",
                "status": "passed",
                "assertions": [
                    "external recipient blocked",
                    "missing approval blocked",
                    "delivery audit event written",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-send-blocked-by-policy",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-recipient-policy",
                    "schema:aispm-report-delivery-audit-event",
                ],
            },
            {
                "path_id": "send_after_approval",
                "title": "Approved send creates immutable delivery evidence",
                "status": "passed",
                "assertions": [
                    "approval decision accepted",
                    "recipient policy passed",
                    "immutable send evidence recorded",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-send-approved",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-approval-decision",
                    "schema:aispm-report-delivery-contract",
                ],
            },
            {
                "path_id": "schedule_run",
                "title": "Scheduled report run respects governance policy",
                "status": "passed",
                "assertions": [
                    "schedule policy evaluated",
                    "blackout window checked",
                    "retry policy available",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-schedule-run-evaluated",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-schedule-policy",
                ],
            },
            {
                "path_id": "evidence_room",
                "title": "Evidence room grants scoped and expiring access",
                "status": "passed",
                "assertions": [
                    "room access scoped",
                    "watermark evidence available",
                    "view and download events logged",
                    "revocation path verified",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/evidence-room-access-validated",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-evidence-room",
                    "schema:aispm-report-evidence-room-access-event",
                ],
            },
            {
                "path_id": "alert_escalation",
                "title": "Delivery or approval SLO breach routes an alert",
                "status": "passed",
                "assertions": [
                    "alert rule evaluated",
                    "routing policy applied",
                    "acknowledgement due time recorded",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-alert-escalation-validated",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-alert-escalation",
                    "schema:aispm-report-alert-operations-dashboard",
                ],
            },
            {
                "path_id": "remediation_closure",
                "title": "Alert remediation closes only after required evidence",
                "status": "passed",
                "assertions": [
                    "tasks completed",
                    "final approval recorded",
                    "residual risk state captured",
                    "closure evidence recorded",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-remediation-closure-validated",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-alert-remediation-plan",
                    "schema:aispm-report-alert-remediation-closure",
                ],
            },
            {
                "path_id": "executive_digest_distribution",
                "title": "Executive digest distribution waits for approval",
                "status": "passed",
                "assertions": [
                    "email delivery blocked before approval",
                    "portal package ready",
                    "grc package ready",
                    "signed manifest required",
                    "immutable send evidence available",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/executive-digest-distribution-validated",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-remediation-closure-executive-digest",
                    "schema:aispm-report-remediation-closure-digest-distribution",
                ],
            },
            {
                "path_id": "revocation_and_retention",
                "title": "Revoked or expired artifacts cannot be retrieved",
                "status": "passed",
                "assertions": [
                    "revoked artifact blocked",
                    "expired artifact blocked",
                    "retention policy evaluated",
                    "retrieval audit event written",
                ],
                "evidence_refs": [
                    "cavra://evidence/redacted/report-revocation-retention-validated",
                ],
                "public_artifact_refs": [
                    "schema:aispm-report-retention-lifecycle",
                    "schema:aispm-report-search-retrieval",
                ],
            },
        ],
        "artifacts": {
            "schemas_validated": [
                "aispm-report-delivery-contract.schema.json",
                "aispm-report-setup-wizard-contract.schema.json",
                "aispm-report-delivery-audit-event.schema.json",
                "aispm-report-operations-dashboard.schema.json",
                "aispm-report-retention-lifecycle.schema.json",
                "aispm-report-search-retrieval.schema.json",
                "aispm-report-export-package-manifest.schema.json",
                "aispm-report-schedule-policy.schema.json",
                "aispm-report-recipient-policy.schema.json",
                "aispm-report-approval-decision.schema.json",
                "aispm-report-evidence-room.schema.json",
                "aispm-report-evidence-room-access-event.schema.json",
                "aispm-report-alert-escalation.schema.json",
                "aispm-report-alert-remediation-closure.schema.json",
                "aispm-report-remediation-closure-digest-distribution.schema.json",
            ],
            "packet_digest_ref": "digest:opaque-report-center-trial-validation",
            "immutable_store_ref": "immutable:opaque-report-center-trial-validation",
            "operator_dashboard_ref": "dashboard:opaque-report-center-trial",
        },
        "controls": {
            "license_validated": True,
            "tenant_scoped": True,
            "approval_before_send_verified": True,
            "recipient_policy_verified": True,
            "retention_policy_verified": True,
            "revocation_verified": True,
            "immutable_evidence_required": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_prompt_included": False,
            "model_reasoning_included": False,
            "raw_tool_output_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "source_code_included": False,
            "payload_handling": "report_center_trial_validation_metadata_only",
        },
        "enterprise_boundaries": {
            "trial_license_service": "requires_cavra_enterprise",
            "report_renderer": "requires_cavra_enterprise",
            "delivery_worker": "requires_cavra_enterprise",
            "scheduler": "requires_cavra_enterprise",
            "evidence_room_worker": "requires_cavra_enterprise",
            "alert_evaluator": "requires_cavra_enterprise",
            "remediation_workflow": "requires_cavra_enterprise",
            "digest_distribution_worker": "requires_cavra_enterprise",
            "tenant_store": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_center_trial_operator_dashboard_readiness_contract() -> dict[str, Any]:
    """Return a public-safe Enterprise Trial operator dashboard readiness contract."""

    return {
        "schema_version": AISPM_REPORT_CENTER_TRIAL_OPERATOR_DASHBOARD_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-12T10:15:00Z",
        "trial_ref": "trial:opaque-report-center-evaluator",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "dashboard": {
            "dashboard_ref": "dashboard:opaque-report-center-trial-operator",
            "status": "ready_for_operator_review",
            "operator_review_required": True,
            "last_validation_packet_ref": "evidence-packet:opaque-report-center-trial",
            "last_refresh_at": "2026-06-12T10:15:00Z",
            "next_review_due_at": "2026-06-12T12:00:00Z",
        },
        "validation_rollup": {
            "total_paths": 10,
            "passed_paths": 10,
            "warning_paths": 0,
            "blocked_paths": 0,
            "failed_paths": 0,
            "critical_blockers": 0,
            "handoff_ready": True,
            "trial_validation_packet_ref": "packet:opaque-report-center-validation",
        },
        "path_status": [
            {
                "path_id": "setup_wizard",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-setup-settings-saved",
            },
            {
                "path_id": "render_report",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-render-metadata-produced",
            },
            {
                "path_id": "send_blocked_by_policy",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-send-blocked-by-policy",
            },
            {
                "path_id": "send_after_approval",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-send-approved",
            },
            {
                "path_id": "schedule_run",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-schedule-run-evaluated",
            },
            {
                "path_id": "evidence_room",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/evidence-room-access-validated",
            },
            {
                "path_id": "alert_escalation",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-alert-escalation-validated",
            },
            {
                "path_id": "remediation_closure",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-remediation-closure-validated",
            },
            {
                "path_id": "executive_digest_distribution",
                "status": "passed",
                "operator_state": "review_recommended",
                "evidence_ref": "cavra://evidence/redacted/executive-digest-distribution-validated",
            },
            {
                "path_id": "revocation_and_retention",
                "status": "passed",
                "operator_state": "no_action_required",
                "evidence_ref": "cavra://evidence/redacted/report-revocation-retention-validated",
            },
        ],
        "approval_blockers": [],
        "evidence_links": [
            {
                "label": "Trial validation packet",
                "evidence_ref": "cavra://evidence/redacted/report-center-trial-validation-packet",
                "artifact_ref": "packet:opaque-report-center-validation",
                "status": "available",
            },
            {
                "label": "Digest distribution evidence",
                "evidence_ref": "cavra://evidence/redacted/executive-digest-distribution-validated",
                "artifact_ref": "distribution:opaque-remediation-closure-executive",
                "status": "available",
            },
            {
                "label": "Retention verification evidence",
                "evidence_ref": "cavra://evidence/redacted/report-revocation-retention-validated",
                "artifact_ref": "retention:opaque-report-center-trial",
                "status": "available",
            },
        ],
        "operator_actions": [
            {
                "action_id": "review-trial-validation",
                "label": "Review trial validation packet",
                "state": "recommended",
                "requires_approval": False,
                "evidence_ref": "cavra://evidence/redacted/operator-review-requested",
            },
            {
                "action_id": "approve-evaluator-handoff",
                "label": "Approve evaluator handoff",
                "state": "available",
                "requires_approval": True,
                "evidence_ref": "cavra://evidence/redacted/evaluator-handoff-ready",
            },
            {
                "action_id": "request-rerun",
                "label": "Request validation rerun",
                "state": "available",
                "requires_approval": False,
                "evidence_ref": "cavra://evidence/redacted/validation-rerun-available",
            },
        ],
        "evaluator_handoff": {
            "handoff_state": "ready",
            "handoff_packet_ref": "handoff:opaque-report-center-evaluator",
            "instructions_ref": "docs:enterprise-trial-report-center",
            "package_access_state": "ready",
            "license_state": "trial_active",
            "support_state": "operator_review_pending",
            "expires_at": "2026-06-19T10:15:00Z",
        },
        "controls": {
            "operator_review_required": True,
            "approval_before_handoff_required": True,
            "license_status_visible": True,
            "package_access_status_visible": True,
            "evidence_refs_only": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "evaluator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_prompt_included": False,
            "model_reasoning_included": False,
            "raw_tool_output_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "source_code_included": False,
            "payload_handling": "report_center_trial_operator_dashboard_metadata_only",
        },
        "enterprise_boundaries": {
            "operator_dashboard_api": "requires_cavra_enterprise",
            "trial_validation_store": "requires_cavra_enterprise",
            "handoff_workflow": "requires_cavra_enterprise",
            "package_access_service": "requires_cavra_enterprise",
            "license_service": "requires_cavra_enterprise",
            "support_queue": "requires_cavra_enterprise",
            "audit_store": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_center_trial_operator_api_view_model_contract() -> dict[str, Any]:
    """Return a public-safe Enterprise Trial operator dashboard API/view-model contract."""

    return {
        "schema_version": AISPM_REPORT_CENTER_TRIAL_OPERATOR_API_VIEW_MODEL_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-12T10:45:00Z",
        "source_contract_ref": (
            "src/cavra/schemas/"
            "aispm-report-center-trial-operator-dashboard-readiness.schema.json"
        ),
        "api_surface": {
            "base_path": "/enterprise/trial/operator/report-center",
            "auth_required": True,
            "auth_modes": ["github_operator_session", "enterprise_operator_sso"],
            "content_type": "application/json",
            "endpoints": [
                {
                    "endpoint_id": "get-dashboard",
                    "method": "GET",
                    "path": "/dashboard",
                    "purpose": "Return redacted readiness rollup and handoff state.",
                    "response_model": "trial_operator_dashboard_view",
                    "audit_event_required": True,
                },
                {
                    "endpoint_id": "get-validation-packet",
                    "method": "GET",
                    "path": "/validation-packet/{packet_ref}",
                    "purpose": "Return redacted validation packet metadata for operator review.",
                    "response_model": "trial_validation_packet_summary",
                    "audit_event_required": True,
                },
                {
                    "endpoint_id": "approve-handoff",
                    "method": "POST",
                    "path": "/handoffs/{handoff_ref}/approve",
                    "purpose": "Approve evaluator handoff after validation review.",
                    "response_model": "trial_operator_action_result",
                    "audit_event_required": True,
                },
                {
                    "endpoint_id": "request-rerun",
                    "method": "POST",
                    "path": "/validation-runs/{run_ref}/rerun",
                    "purpose": "Request a new validation run before evaluator handoff.",
                    "response_model": "trial_operator_action_result",
                    "audit_event_required": True,
                },
            ],
        },
        "view_model": {
            "view_id": "trial_operator_dashboard_view",
            "route": "/operator/report-center/trial",
            "title": "Enterprise Trial Operator Review",
            "refresh_interval_seconds": 60,
            "sections": [
                {
                    "section_id": "validation_rollup",
                    "title": "Validation Rollup",
                    "data_source": "GET /dashboard",
                    "fields": [
                        "total_paths",
                        "passed_paths",
                        "warning_paths",
                        "blocked_paths",
                        "failed_paths",
                        "critical_blockers",
                        "handoff_ready",
                    ],
                },
                {
                    "section_id": "path_status",
                    "title": "Evaluator Path Status",
                    "data_source": "GET /dashboard",
                    "fields": ["path_id", "status", "operator_state", "evidence_ref"],
                },
                {
                    "section_id": "approval_blockers",
                    "title": "Approval Blockers",
                    "data_source": "GET /dashboard",
                    "fields": ["blocker_ref", "severity", "reason_code", "evidence_ref"],
                },
                {
                    "section_id": "evidence_links",
                    "title": "Evidence Links",
                    "data_source": "GET /dashboard",
                    "fields": ["label", "evidence_ref", "artifact_ref", "status"],
                },
                {
                    "section_id": "evaluator_handoff",
                    "title": "Evaluator Handoff",
                    "data_source": "GET /dashboard",
                    "fields": [
                        "handoff_state",
                        "package_access_state",
                        "license_state",
                        "support_state",
                        "expires_at",
                    ],
                },
            ],
            "primary_actions": [
                {
                    "action_id": "review-trial-validation",
                    "label": "Review validation packet",
                    "method": "GET",
                    "endpoint_id": "get-validation-packet",
                    "enabled_when": "validation_packet_available",
                },
                {
                    "action_id": "approve-evaluator-handoff",
                    "label": "Approve evaluator handoff",
                    "method": "POST",
                    "endpoint_id": "approve-handoff",
                    "enabled_when": "handoff_ready_and_no_blockers",
                },
                {
                    "action_id": "request-rerun",
                    "label": "Request validation rerun",
                    "method": "POST",
                    "endpoint_id": "request-rerun",
                    "enabled_when": "operator_review_required",
                },
            ],
            "filters": [
                {"filter_id": "path_status", "values": ["passed", "warning", "blocked", "failed"]},
                {
                    "filter_id": "operator_state",
                    "values": ["no_action_required", "review_recommended", "action_required"],
                },
            ],
            "empty_states": [
                {
                    "state_id": "no_validation_packet",
                    "message": "No trial validation packet is available yet.",
                },
                {
                    "state_id": "no_blockers",
                    "message": "No approval blockers are currently open.",
                },
            ],
        },
        "action_state_machine": {
            "states": [
                "pending_validation",
                "ready_for_operator_review",
                "handoff_approved",
                "rerun_requested",
                "blocked",
            ],
            "transitions": [
                {
                    "from": "pending_validation",
                    "to": "ready_for_operator_review",
                    "trigger": "validation_packet_passed",
                },
                {
                    "from": "ready_for_operator_review",
                    "to": "handoff_approved",
                    "trigger": "approve_evaluator_handoff",
                },
                {
                    "from": "ready_for_operator_review",
                    "to": "rerun_requested",
                    "trigger": "request_validation_rerun",
                },
                {
                    "from": "ready_for_operator_review",
                    "to": "blocked",
                    "trigger": "critical_blocker_opened",
                },
            ],
        },
        "audit_events": [
            {
                "event_type": "operator_dashboard_viewed",
                "required_fields": ["operator_ref", "tenant_ref", "trial_ref", "viewed_at"],
            },
            {
                "event_type": "validation_packet_reviewed",
                "required_fields": ["operator_ref", "packet_ref", "reviewed_at"],
            },
            {
                "event_type": "evaluator_handoff_approved",
                "required_fields": ["operator_ref", "handoff_ref", "approved_at"],
            },
            {
                "event_type": "validation_rerun_requested",
                "required_fields": ["operator_ref", "run_ref", "requested_at"],
            },
        ],
        "controls": {
            "operator_auth_required": True,
            "rbac_required": True,
            "csrf_protection_required": True,
            "immutable_audit_required": True,
            "approval_before_handoff_required": True,
            "rate_limit_required": True,
            "evidence_refs_only": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "evaluator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "raw_prompt_included": False,
            "model_reasoning_included": False,
            "raw_tool_output_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "source_code_included": False,
            "payload_handling": "report_center_trial_operator_api_metadata_only",
        },
        "enterprise_boundaries": {
            "operator_dashboard_api": "requires_cavra_enterprise",
            "operator_session_store": "requires_cavra_enterprise",
            "trial_validation_store": "requires_cavra_enterprise",
            "handoff_workflow": "requires_cavra_enterprise",
            "package_access_service": "requires_cavra_enterprise",
            "license_service": "requires_cavra_enterprise",
            "support_queue": "requires_cavra_enterprise",
            "audit_store": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_center_trial_evaluator_handoff_packet_contract() -> dict[str, Any]:
    """Return a public-safe Enterprise Trial evaluator handoff packet contract."""

    return {
        "schema_version": AISPM_REPORT_CENTER_TRIAL_EVALUATOR_HANDOFF_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-12T11:15:00Z",
        "handoff_ref": "handoff:opaque-report-center-evaluator",
        "trial_ref": "trial:opaque-report-center-evaluator",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "source_contract_refs": [
            "src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json",
            "src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json",
            "src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json",
        ],
        "evaluator_experience": {
            "state": "ready_for_evaluator",
            "welcome_title": "CAVRA Enterprise Trial",
            "audience": ["security_leader", "platform_engineer", "ai_governance_reviewer"],
            "estimated_setup_minutes": 20,
            "instructions_ref": "docs:enterprise-trial-report-center",
            "steps": [
                {
                    "step_id": "confirm-approval",
                    "title": "Confirm approved trial access",
                    "status": "ready",
                    "requires_operator": False,
                    "evidence_ref": "cavra://evidence/redacted/trial-access-approved",
                },
                {
                    "step_id": "authenticate-package-registry",
                    "title": "Authenticate to the package registry",
                    "status": "ready",
                    "requires_operator": False,
                    "evidence_ref": "cavra://evidence/redacted/package-registry-access-ready",
                },
                {
                    "step_id": "pull-trial-package",
                    "title": "Pull the Enterprise Trial package",
                    "status": "ready",
                    "requires_operator": False,
                    "evidence_ref": "cavra://evidence/redacted/trial-package-access-ready",
                },
                {
                    "step_id": "configure-license",
                    "title": "Configure trial license",
                    "status": "ready",
                    "requires_operator": False,
                    "evidence_ref": "cavra://evidence/redacted/trial-license-active",
                },
                {
                    "step_id": "run-first-validation",
                    "title": "Run the first validation scenario",
                    "status": "ready",
                    "requires_operator": False,
                    "evidence_ref": "cavra://evidence/redacted/report-center-validation-ready",
                },
            ],
        },
        "package_access": {
            "provider": "ghcr",
            "package_ref": "package:opaque-cavra-enterprise-trial",
            "access_status": "ready",
            "permissions_required": ["read:packages"],
            "image_ref_redacted": True,
            "download_urls_included": False,
            "package_token_included": False,
            "access_expires_at": "2026-06-19T10:15:00Z",
        },
        "license_status": {
            "license_ref": "license:opaque-enterprise-trial",
            "status": "active",
            "license_type": "trial",
            "issued_at": "2026-06-12T10:15:00Z",
            "expires_at": "2026-06-19T10:15:00Z",
            "revocation_state": "not_revoked",
            "license_key_included": False,
        },
        "support": {
            "support_state": "operator_review_pending",
            "channels": [
                {
                    "channel_id": "trial-portal",
                    "label": "Trial portal",
                    "status": "available",
                    "contact_detail_included": False,
                },
                {
                    "channel_id": "email",
                    "label": "Email support",
                    "status": "available",
                    "contact_detail_included": False,
                },
            ],
            "response_slo": "next_business_day",
            "support_ticket_ref": "support:opaque-trial-handoff",
        },
        "revocation": {
            "revocation_supported": True,
            "current_state": "not_revoked",
            "revocation_ref": "revocation:opaque-report-center-trial",
            "blocked_after_revocation": True,
            "audit_event_required": True,
        },
        "onboarding_checks": [
            {
                "check_id": "operator_approved",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/operator-handoff-approved",
            },
            {
                "check_id": "package_access_ready",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/package-access-ready",
            },
            {
                "check_id": "license_active",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/license-active",
            },
            {
                "check_id": "validation_packet_available",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/validation-packet-available",
            },
        ],
        "controls": {
            "operator_approval_required": True,
            "trial_license_required": True,
            "package_access_gated": True,
            "revocation_enforced": True,
            "support_handoff_audited": True,
            "evidence_refs_only": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "evaluator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "package_tokens_included": False,
            "license_key_included": False,
            "raw_prompt_included": False,
            "model_reasoning_included": False,
            "raw_tool_output_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "source_code_included": False,
            "payload_handling": "report_center_trial_evaluator_handoff_metadata_only",
        },
        "enterprise_boundaries": {
            "trial_portal": "requires_cavra_enterprise",
            "package_access_service": "requires_cavra_enterprise",
            "license_service": "requires_cavra_enterprise",
            "revocation_service": "requires_cavra_enterprise",
            "support_queue": "requires_cavra_enterprise",
            "audit_store": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_center_trial_revocation_expiry_evidence_contract() -> dict[str, Any]:
    """Return a public-safe Enterprise Trial revocation and expiry evidence contract."""

    return {
        "schema_version": AISPM_REPORT_CENTER_TRIAL_REVOCATION_EXPIRY_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-12T11:45:00Z",
        "trial_ref": "trial:opaque-report-center-evaluator",
        "tenant_ref": "tenant:opaque-public-contract-sample",
        "evidence_packet_ref": "evidence-packet:opaque-trial-revocation-expiry",
        "source_contract_refs": [
            "src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json",
            "src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json",
        ],
        "revocation_expiry": {
            "trigger": "operator_revocation",
            "state": "revoked",
            "revoked_at": "2026-06-12T11:30:00Z",
            "expired_at": "2026-06-19T10:15:00Z",
            "reason_code": "trial_completed",
            "operator_approval_ref": "approval:opaque-trial-revocation",
            "audit_ref": "audit:opaque-trial-revocation-expiry",
        },
        "blocked_access_checks": [
            {
                "check_id": "license_validation",
                "surface": "license_service",
                "attempted_action": "validate_trial_license",
                "expected_result": "blocked",
                "actual_result": "blocked",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/license-validation-blocked",
            },
            {
                "check_id": "package_pull",
                "surface": "package_registry",
                "attempted_action": "pull_trial_package",
                "expected_result": "blocked",
                "actual_result": "blocked",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/package-pull-blocked",
            },
            {
                "check_id": "trial_portal_access",
                "surface": "trial_portal",
                "attempted_action": "open_trial_dashboard",
                "expected_result": "blocked",
                "actual_result": "blocked",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/trial-portal-access-blocked",
            },
            {
                "check_id": "report_render",
                "surface": "report_center",
                "attempted_action": "render_enterprise_report",
                "expected_result": "blocked",
                "actual_result": "blocked",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/report-render-blocked",
            },
            {
                "check_id": "support_handoff",
                "surface": "support_queue",
                "attempted_action": "open_trial_support_channel",
                "expected_result": "blocked",
                "actual_result": "blocked",
                "status": "passed",
                "evidence_ref": "cavra://evidence/redacted/support-channel-blocked",
            },
        ],
        "access_state": {
            "license_state": "revoked",
            "package_access_state": "revoked",
            "portal_access_state": "revoked",
            "support_state": "closed",
            "handoff_state": "closed",
            "revocation_enforced": True,
            "expiry_enforced": True,
        },
        "audit_chain": [
            {
                "event_type": "trial_revocation_requested",
                "event_ref": "audit:opaque-revocation-requested",
                "occurred_at": "2026-06-12T11:25:00Z",
                "immutable": True,
            },
            {
                "event_type": "trial_access_revoked",
                "event_ref": "audit:opaque-access-revoked",
                "occurred_at": "2026-06-12T11:30:00Z",
                "immutable": True,
            },
            {
                "event_type": "blocked_access_verified",
                "event_ref": "audit:opaque-blocked-access-verified",
                "occurred_at": "2026-06-12T11:45:00Z",
                "immutable": True,
            },
        ],
        "operator_summary": {
            "summary_state": "revocation_verified",
            "blocked_checks": 5,
            "failed_checks": 0,
            "follow_up_required": False,
            "evidence_ready": True,
        },
        "controls": {
            "operator_approval_required": True,
            "revocation_enforced": True,
            "expiry_enforced": True,
            "license_block_verified": True,
            "package_block_verified": True,
            "portal_block_verified": True,
            "support_block_verified": True,
            "immutable_audit_required": True,
            "evidence_refs_only": True,
            "raw_payloads_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "evaluator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "package_tokens_included": False,
            "license_key_included": False,
            "raw_prompt_included": False,
            "model_reasoning_included": False,
            "raw_tool_output_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "source_code_included": False,
            "payload_handling": "report_center_trial_revocation_expiry_metadata_only",
        },
        "enterprise_boundaries": {
            "trial_portal": "requires_cavra_enterprise",
            "package_access_service": "requires_cavra_enterprise",
            "license_service": "requires_cavra_enterprise",
            "revocation_service": "requires_cavra_enterprise",
            "support_queue": "requires_cavra_enterprise",
            "audit_store": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_center_trial_lab_notebook_outline_contract() -> dict[str, Any]:
    """Return a public-safe Enterprise Trial lab notebook outline contract."""

    return {
        "schema_version": AISPM_REPORT_CENTER_TRIAL_LAB_NOTEBOOK_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-12T12:15:00Z",
        "notebook_ref": "wiki:aispm-enterprise-trial-lab-notebook",
        "source_contract_refs": [
            "src/cavra/schemas/aispm-dashboard.schema.json",
            "src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json",
            "src/cavra/schemas/aispm-report-center-trial-evaluator-handoff-packet.schema.json",
            "src/cavra/schemas/aispm-report-center-trial-revocation-expiry-evidence.schema.json",
        ],
        "notebook": {
            "title": "CAVRA Enterprise Trial Lab Notebook",
            "audiences": [
                "developer",
                "platform_engineer",
                "security_engineer",
                "auditor",
                "cso_ciso",
            ],
            "publication_target": "github_wiki",
            "status": "outline_ready",
            "estimated_duration_minutes": 180,
            "requires_enterprise_trial": True,
            "public_safe": True,
        },
        "chapters": [
            {
                "chapter_id": "orientation",
                "title": "Product Orientation",
                "objective": "Understand CAVRA editions, AI-agent governance, and evidence boundaries.",
                "labs": ["lab-product-tour", "lab-community-vs-enterprise"],
                "required_assets": ["diagram-open-core-model", "screenshot-dashboard-home"],
            },
            {
                "chapter_id": "trial-access",
                "title": "Trial Access And Setup",
                "objective": "Request, approve, and prepare a governed Enterprise Trial evaluation.",
                "labs": ["lab-request-trial", "lab-operator-approval", "lab-evaluator-handoff"],
                "required_assets": ["flow-trial-access", "screenshot-trial-portal"],
            },
            {
                "chapter_id": "agent-enforcement",
                "title": "AI-Agent Enforcement",
                "objective": "Run controlled agent actions and inspect allow, warn, block, and approval decisions.",
                "labs": ["lab-run-agent-scenario", "lab-review-policy-decisions"],
                "required_assets": ["diagram-enforcement-flow", "screenshot-policy-decision"],
            },
            {
                "chapter_id": "aispm-dashboard",
                "title": "AISPM Dashboard",
                "objective": "Review posture, live activity, risk, timelines, and evidence confidence.",
                "labs": ["lab-cso-dashboard", "lab-risk-drilldown", "lab-evidence-freshness"],
                "required_assets": ["screenshot-aispm-dashboard", "diagram-posture-data-flow"],
            },
            {
                "chapter_id": "report-center",
                "title": "CSO Report Center",
                "objective": "Download Community reports and review Enterprise report-delivery governance.",
                "labs": ["lab-download-community-reports", "lab-enterprise-report-governance"],
                "required_assets": ["screenshot-report-center", "flow-report-approval"],
            },
            {
                "chapter_id": "closeout",
                "title": "Trial Closeout",
                "objective": "Verify revocation, expiry, and public-safe closeout evidence.",
                "labs": ["lab-revocation-expiry", "lab-closeout-evidence"],
                "required_assets": ["flow-revocation-expiry", "screenshot-closeout-summary"],
            },
        ],
        "labs": [
            {
                "lab_id": "lab-product-tour",
                "title": "Navigate the CAVRA product surfaces",
                "role": "developer",
                "phase": "orientation",
                "expected_minutes": 15,
                "verification_checkpoint": "checkpoint-product-surfaces",
                "evidence_ref": "cavra://evidence/redacted/lab-product-tour",
            },
            {
                "lab_id": "lab-request-trial",
                "title": "Request Enterprise Trial access",
                "role": "platform_engineer",
                "phase": "trial-access",
                "expected_minutes": 20,
                "verification_checkpoint": "checkpoint-trial-request",
                "evidence_ref": "cavra://evidence/redacted/lab-request-trial",
            },
            {
                "lab_id": "lab-operator-approval",
                "title": "Review and approve a trial request",
                "role": "security_engineer",
                "phase": "trial-access",
                "expected_minutes": 20,
                "verification_checkpoint": "checkpoint-operator-approval",
                "evidence_ref": "cavra://evidence/redacted/lab-operator-approval",
            },
            {
                "lab_id": "lab-run-agent-scenario",
                "title": "Run a governed AI-agent scenario",
                "role": "developer",
                "phase": "agent-enforcement",
                "expected_minutes": 25,
                "verification_checkpoint": "checkpoint-agent-decision",
                "evidence_ref": "cavra://evidence/redacted/lab-agent-scenario",
            },
            {
                "lab_id": "lab-cso-dashboard",
                "title": "Review the CSO/CISO posture view",
                "role": "cso_ciso",
                "phase": "aispm-dashboard",
                "expected_minutes": 25,
                "verification_checkpoint": "checkpoint-cso-dashboard",
                "evidence_ref": "cavra://evidence/redacted/lab-cso-dashboard",
            },
            {
                "lab_id": "lab-download-community-reports",
                "title": "Download public-safe Community reports",
                "role": "auditor",
                "phase": "report-center",
                "expected_minutes": 20,
                "verification_checkpoint": "checkpoint-community-reports",
                "evidence_ref": "cavra://evidence/redacted/lab-community-reports",
            },
            {
                "lab_id": "lab-revocation-expiry",
                "title": "Verify trial revocation and expiry enforcement",
                "role": "security_engineer",
                "phase": "closeout",
                "expected_minutes": 25,
                "verification_checkpoint": "checkpoint-revocation-expiry",
                "evidence_ref": "cavra://evidence/redacted/lab-revocation-expiry",
            },
        ],
        "visual_assets": [
            {
                "asset_id": "diagram-open-core-model",
                "asset_type": "diagram",
                "format": "png",
                "status": "required",
                "public_safe": True,
            },
            {
                "asset_id": "screenshot-aispm-dashboard",
                "asset_type": "screenshot",
                "format": "png",
                "status": "required",
                "public_safe": True,
            },
            {
                "asset_id": "flow-revocation-expiry",
                "asset_type": "flow_chart",
                "format": "png",
                "status": "required",
                "public_safe": True,
            },
        ],
        "verification_checkpoints": [
            {
                "checkpoint_id": "checkpoint-trial-request",
                "expected_result": "trial_request_pending_or_approved",
                "evidence_ref": "cavra://evidence/redacted/checkpoint-trial-request",
            },
            {
                "checkpoint_id": "checkpoint-agent-decision",
                "expected_result": "policy_decision_recorded",
                "evidence_ref": "cavra://evidence/redacted/checkpoint-agent-decision",
            },
            {
                "checkpoint_id": "checkpoint-revocation-expiry",
                "expected_result": "trial_access_blocked_after_revocation",
                "evidence_ref": "cavra://evidence/redacted/checkpoint-revocation-expiry",
            },
        ],
        "role_paths": [
            {
                "role": "developer",
                "recommended_labs": ["lab-product-tour", "lab-run-agent-scenario"],
            },
            {
                "role": "auditor",
                "recommended_labs": ["lab-download-community-reports", "lab-revocation-expiry"],
            },
            {
                "role": "cso_ciso",
                "recommended_labs": ["lab-cso-dashboard", "lab-download-community-reports"],
            },
        ],
        "publishing": {
            "target": "github_wiki",
            "page_title": "CAVRA Enterprise Trial Lab Notebook",
            "requires_screenshots": True,
            "requires_diagrams": True,
            "requires_flow_charts": True,
            "requires_checkpoint_evidence": True,
            "update_after_phase_completion": True,
        },
        "controls": {
            "public_safe_required": True,
            "screenshots_redacted": True,
            "diagram_sources_public_safe": True,
            "checkpoint_evidence_required": True,
            "enterprise_source_excluded": True,
            "license_secret_excluded": True,
            "customer_data_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "evaluator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "package_tokens_included": False,
            "license_key_included": False,
            "raw_prompt_included": False,
            "model_reasoning_included": False,
            "raw_tool_output_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "source_code_included": False,
            "payload_handling": "report_center_trial_lab_notebook_outline_metadata_only",
        },
        "enterprise_boundaries": {
            "wiki_publication_workflow": "public_docs_only",
            "trial_portal": "requires_cavra_enterprise",
            "license_service": "requires_cavra_enterprise",
            "package_access_service": "requires_cavra_enterprise",
            "private_lab_fixtures": "requires_cavra_enterprise",
        },
    }


def build_aispm_report_center_trial_lab_notebook_publication_readiness_contract() -> dict[str, Any]:
    """Return the public-safe readiness packet for publishing the trial lab notebook."""

    return {
        "schema_version": AISPM_REPORT_CENTER_TRIAL_LAB_NOTEBOOK_PUBLICATION_READINESS_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "enterprise_trial",
        "contract_visibility": "public_contract",
        "generated_at": "2026-06-12T13:00:00Z",
        "notebook_ref": "wiki:aispm-enterprise-trial-lab-notebook",
        "outline_contract_ref": (
            "src/cavra/schemas/aispm-report-center-trial-lab-notebook-outline.schema.json"
        ),
        "publication_readiness": {
            "status": "ready_for_publication_review",
            "target": "github_wiki",
            "release_gate": "enterprise_trial_public_docs_ready",
            "required_reviews": ["docs_owner", "security_owner", "product_owner"],
            "requires_no_private_artifacts": True,
        },
        "wiki_pages": [
            {
                "page_id": "trial-lab-overview",
                "title": "CAVRA Enterprise Trial Lab Notebook",
                "source_ref": "docs/wiki/AISPM-Enterprise-Trial-Lab-Notebook.md",
                "nav_entry_required": True,
                "link_health_required": True,
                "screenshot_refs": ["screenshot-dashboard-home"],
                "diagram_refs": ["diagram-open-core-model"],
                "checkpoint_refs": ["checkpoint-product-surfaces"],
            },
            {
                "page_id": "trial-access-flow",
                "title": "Trial Access And Operator Approval",
                "source_ref": "docs/wiki/AISPM-Trial-Access-And-Operator-Approval.md",
                "nav_entry_required": True,
                "link_health_required": True,
                "screenshot_refs": ["screenshot-trial-portal"],
                "diagram_refs": ["flow-trial-access"],
                "checkpoint_refs": ["checkpoint-trial-request", "checkpoint-operator-approval"],
            },
            {
                "page_id": "trial-closeout",
                "title": "Trial Revocation, Expiry, And Closeout",
                "source_ref": "docs/wiki/AISPM-Trial-Revocation-Expiry-And-Closeout.md",
                "nav_entry_required": True,
                "link_health_required": True,
                "screenshot_refs": ["screenshot-closeout-summary"],
                "diagram_refs": ["flow-revocation-expiry"],
                "checkpoint_refs": ["checkpoint-revocation-expiry"],
            },
        ],
        "visual_assets": [
            {
                "asset_id": "screenshot-dashboard-home",
                "asset_type": "screenshot",
                "source_route": "https://huzefaaa2.github.io/cavra/#dashboard",
                "format": "png",
                "redaction_status": "public_safe",
                "alt_text_required": True,
                "required": True,
            },
            {
                "asset_id": "screenshot-trial-portal",
                "asset_type": "screenshot",
                "source_route": "https://cavra-trial.mind-ops.cloud/",
                "format": "png",
                "redaction_status": "public_safe",
                "alt_text_required": True,
                "required": True,
            },
            {
                "asset_id": "diagram-open-core-model",
                "asset_type": "diagram",
                "source_route": "docs/architecture/open-core-model.md",
                "format": "png",
                "redaction_status": "public_safe",
                "alt_text_required": True,
                "required": True,
            },
            {
                "asset_id": "flow-revocation-expiry",
                "asset_type": "flow_chart",
                "source_route": "docs/architecture/aispm-report-center.md",
                "format": "png",
                "redaction_status": "public_safe",
                "alt_text_required": True,
                "required": True,
            },
        ],
        "link_checks": [
            {
                "target_label": "Community dashboard",
                "url_kind": "public_docs_or_portal",
                "expected_status": "reachable",
                "owner": "docs_owner",
            },
            {
                "target_label": "Enterprise Trial portal",
                "url_kind": "trial_portal",
                "expected_status": "reachable",
                "owner": "trial_operator",
            },
            {
                "target_label": "Public README",
                "url_kind": "repository_page",
                "expected_status": "reachable",
                "owner": "docs_owner",
            },
        ],
        "navigation_checks": [
            {
                "nav_id": "wiki-home-trial-lab-entry",
                "location": "docs/wiki/Home.md",
                "required_page_ids": [
                    "trial-lab-overview",
                    "trial-access-flow",
                    "trial-closeout",
                ],
            }
        ],
        "checkpoint_evidence": [
            {
                "checkpoint_id": "checkpoint-product-surfaces",
                "evidence_ref": "cavra://evidence/redacted/checkpoint-product-surfaces",
                "source_packet_ref": "trial_lab_notebook_outline",
                "public_safe": True,
            },
            {
                "checkpoint_id": "checkpoint-trial-request",
                "evidence_ref": "cavra://evidence/redacted/checkpoint-trial-request",
                "source_packet_ref": "trial_validation_packet",
                "public_safe": True,
            },
            {
                "checkpoint_id": "checkpoint-revocation-expiry",
                "evidence_ref": "cavra://evidence/redacted/checkpoint-revocation-expiry",
                "source_packet_ref": "trial_revocation_expiry_evidence",
                "public_safe": True,
            },
        ],
        "acceptance_criteria": [
            {
                "criterion_id": "wiki_nav_complete",
                "description": "Wiki navigation includes every required lab notebook page.",
                "required": True,
            },
            {
                "criterion_id": "assets_redacted",
                "description": "Screenshots, diagrams, and flow charts contain only public-safe data.",
                "required": True,
            },
            {
                "criterion_id": "links_verified",
                "description": "Public links and portal links are checked before publication.",
                "required": True,
            },
            {
                "criterion_id": "checkpoint_evidence_ready",
                "description": "Each lab checkpoint has a public-safe evidence reference.",
                "required": True,
            },
        ],
        "controls": {
            "public_safe_required": True,
            "screenshots_redacted": True,
            "diagrams_redacted": True,
            "wiki_nav_required": True,
            "link_health_required": True,
            "checkpoint_evidence_required": True,
            "enterprise_source_excluded": True,
            "license_secret_excluded": True,
            "customer_data_excluded": True,
        },
        "redaction": {
            "recipient_addresses_included": False,
            "operator_identity_included": False,
            "evaluator_identity_included": False,
            "auditor_identity_included": False,
            "approver_identity_included": False,
            "board_member_identity_included": False,
            "ip_address_included": False,
            "download_urls_included": False,
            "package_tokens_included": False,
            "license_key_included": False,
            "raw_prompt_included": False,
            "model_reasoning_included": False,
            "raw_tool_output_included": False,
            "raw_report_content_included": False,
            "provider_response_included": False,
            "customer_records_included": False,
            "private_remediation_details_included": False,
            "tenant_drilldown_records_included": False,
            "secrets_included": False,
            "source_code_included": False,
            "payload_handling": "report_center_trial_lab_notebook_publication_readiness_metadata_only",
        },
        "enterprise_boundaries": {
            "wiki_publication_workflow": "public_docs_only",
            "trial_portal": "requires_cavra_enterprise",
            "license_service": "requires_cavra_enterprise",
            "package_access_service": "requires_cavra_enterprise",
            "private_screenshot_capture": "requires_cavra_enterprise",
            "private_lab_fixtures": "requires_cavra_enterprise",
        },
    }
