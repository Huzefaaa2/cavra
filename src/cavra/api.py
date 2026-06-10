from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from cavra.activity import ActivityStore, SQLiteActivityStore, utc_now
from cavra.agent_enforcement import agent_enforcement_readiness_report
from cavra.aispm import (
    build_aispm_approval_lineage,
    build_aispm_agent_blast_radius,
    build_aispm_behavior_fingerprints,
    build_aispm_control_coverage_heatmap,
    build_aispm_dashboard_contract,
    build_aispm_evidence_confidence_drilldown,
    build_aispm_intent_action_drift,
    build_aispm_policy_context_gaps,
    build_aispm_posture,
    build_aispm_pre_action_risk_forecasts,
    build_aispm_trace_replay_packet,
    build_aispm_tool_chain_graph,
    build_sample_aispm_dashboard,
)
from cavra.approvals import (
    ApprovalStore,
    SQLiteApprovalStore,
    actor_context_from_claims,
    actor_context_from_oidc_token,
    actor_can_decide,
    attach_approval_to_decision,
    deliver_provider_requests,
    load_oidc_config,
    load_provider_config,
    load_rbac_rules,
    load_routing_rules,
    repository_permissions_for_actor,
)
from cavra.evidence import (
    EvidenceArtifactError,
    EvidenceMetadataStore,
    SQLiteEvidenceMetadataStore,
    build_evidence_artifact_archive,
    list_evidence_artifacts,
    load_evidence_artifact,
)
from cavra.go_backend import (
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_retry,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert,
    acknowledge_go_rollback_drill_notification,
    build_go_rollback_drill_acknowledgement_audit_delivery_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_closure_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook,
    build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closure_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health,
    acknowledge_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_immutable_archive_reference,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_immutable_archive_reference_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_artifact_bundle,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_artifact_bundle_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_decision_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_request,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_request_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_readiness_bundle,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_readiness_bundle_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_approval_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_record_attachment,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_record_attachment_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_signed_archive_manifest,
    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_signed_archive_manifest_metadata,
    decide_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review,
    filter_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_history,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_decision_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report,
    build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_ack_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_dashboard,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan_metadata,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_run,
    build_go_rollback_drill_acknowledgement_audit_delivery_worker_run_metadata,
    build_go_rollback_drill_acknowledgement_audit_package,
    build_go_rollback_drill_acknowledgement_audit_package_metadata,
    build_go_rollback_drill_notification_ack_metadata,
    build_go_rollback_drill_notification_event,
    build_go_rollback_drill_notification_dashboard,
    build_go_rollback_drill_notification_escalation_plan,
    build_go_rollback_drill_notification_escalation_plan_metadata,
    build_go_rollback_drill_notification_plan,
    build_go_rollback_drill_notification_plan_metadata,
    build_go_rollback_drill_routing_suppression_trend,
    build_go_rollback_drill_routing_suppression_trend_metadata,
    close_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery,
    decide_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_approval,
    decide_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval,
    evaluate_with_go_pilot,
    filter_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_history,
    filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_history,
    filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_history,
    filter_go_rollback_drill_acknowledgement_audit_delivery_worker_history,
    filter_go_rollback_drill_notification_history,
    filter_go_rollback_drill_routing_history,
    go_backend_readiness_report,
    go_deployment_readiness_report,
    go_promotion_readiness_report,
    go_rollback_readiness_report,
    go_rollback_drill_history_report,
    go_rollback_drill_schedule_report,
    go_rollback_rehearsal_report,
)
from cavra.integrations import (
    IntegrationStore,
    SQLiteIntegrationStore,
    build_connector_delivery_dashboard,
    build_connector_delivery_metadata,
    deliver_connector_event,
    filter_connector_delivery_history,
    load_connector_config,
)
from cavra.inventory import InventoryStore, SQLiteInventoryStore
from cavra.operations import build_persistent_api_retention_plan, persistent_api_store_status
from cavra.policy_authoring import (
    build_policy_pack_draft,
    build_policy_pack_publish_plan,
    build_policy_publish_decision,
    build_rollout_change_plan,
    production_readiness_report,
    publish_policy_pack,
    summarize_policy,
)
from cavra.pilot_intake import PilotIntakeStore, build_private_persistence_handoff_plan
from cavra.policy_registry import PolicyRegistry, PolicyRegistryError
from cavra.registry import (
    RegistryStore,
    SQLiteRegistryStore,
    classify_mcp_capability,
    default_agent_profiles,
    default_mcp_tool_classifications,
)
from cavra.saas_control_plane import (
    SAAS_OPERATING_AUTOMATION_CHECKS,
    SaaSContractError,
    SaaSOperatingAutomationSummary,
    SaaSOperatingAutomationWorkerHandoffSummary,
    build_saas_operating_automation_request,
    build_saas_operating_automation_response,
    build_saas_operating_automation_worker_handoff_request,
    build_saas_operating_automation_worker_handoff_response,
    describe_public_contract,
)
from cavra.release import (
    automate_endpoint_reconciliation_from_ingestion,
    build_endpoint_management_export_dashboard,
    build_endpoint_management_publication_dashboard,
    build_endpoint_management_publication_event,
    build_endpoint_management_publication_metadata,
    build_endpoint_drift_remediation_dashboard,
    build_endpoint_drift_remediation_execution_metadata,
    build_endpoint_drift_remediation_request_metadata,
    build_endpoint_remediation_handoff,
    build_endpoint_remediation_handoff_dashboard,
    build_endpoint_remediation_handoff_metadata,
    build_endpoint_remediation_handoff_status_dashboard,
    build_endpoint_remediation_handoff_status_metadata,
    build_endpoint_remediation_sla_dashboard,
    build_endpoint_remediation_sla_escalation_action_dashboard,
    build_endpoint_remediation_sla_escalation_delivery_event,
    build_endpoint_remediation_sla_escalation_dashboard,
    build_endpoint_remediation_sla_escalation_owner_digest_event,
    build_endpoint_remediation_sla_escalation_owner_digest_metadata,
    build_endpoint_remediation_sla_escalation_plan,
    build_endpoint_remediation_sla_escalation_plan_metadata,
    build_endpoint_remediation_sla_escalation_recurrence_dashboard,
    build_endpoint_remediation_sla_escalation_recurrence_automation_dashboard,
    build_endpoint_remediation_sla_escalation_recurrence_automation_health,
    build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_ack_metadata,
    build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard,
    build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_event,
    build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan,
    build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan_metadata,
    build_endpoint_remediation_sla_escalation_recurrence_automation_run,
    build_endpoint_remediation_sla_escalation_recurrence_automation_run_metadata,
    build_endpoint_remediation_sla_escalation_recurrence_delivery_event,
    build_endpoint_remediation_sla_escalation_recurrence_plan,
    build_endpoint_remediation_sla_escalation_recurrence_plan_metadata,
    build_endpoint_remediation_sla_escalation_recurrence_retry_plan,
    build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata,
    build_endpoint_remediation_sla_escalation_review_metadata,
    build_endpoint_remediation_sla_escalation_suppression_audit,
    build_endpoint_remediation_sla_escalation_suppression_audit_metadata,
    build_endpoint_remediation_sla_escalation_suppression_trends,
    build_endpoint_remediation_sla_escalation_suppression_trend_metadata,
    build_endpoint_remediation_sla_notification_ack_metadata,
    build_endpoint_remediation_sla_notification_dashboard,
    build_endpoint_remediation_sla_notification_event,
    build_endpoint_remediation_sla_notification_plan,
    build_endpoint_remediation_sla_notification_plan_metadata,
    build_endpoint_remediation_sla_report,
    build_endpoint_remediation_sla_report_metadata,
    build_endpoint_inventory_freshness_dashboard,
    build_endpoint_inventory_freshness_metadata,
    build_endpoint_inventory_ingestion_dashboard,
    build_endpoint_inventory_ingestion_metadata,
    build_endpoint_reconciliation_automation_dashboard,
    build_endpoint_reconciliation_automation_metadata,
    build_managed_endpoint_reconciliation_dashboard,
    build_managed_endpoint_reconciliation_metadata,
    build_managed_endpoint_rollout_rollback_execution_metadata,
    build_managed_endpoint_rollout_promotion_execution_metadata,
    build_rollout_promotion_execution_audit_event,
    build_rollout_rollback_execution_audit_event,
    acknowledge_endpoint_remediation_sla_escalation_recurrence_automation_health_alert,
    acknowledge_endpoint_remediation_sla_notification,
    create_endpoint_drift_remediation_request,
    create_managed_endpoint_rollout_rollback_execution,
    create_managed_endpoint_rollout_promotion_execution,
    create_managed_endpoint_rollout_promotion_request,
    execute_endpoint_drift_remediation,
    filter_endpoint_drift_remediation_history,
    filter_endpoint_remediation_handoff_history,
    filter_endpoint_remediation_handoff_status_history,
    filter_endpoint_remediation_sla_escalation_history,
    filter_endpoint_remediation_sla_escalation_action_history,
    filter_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_history,
    filter_endpoint_remediation_sla_escalation_recurrence_automation_history,
    filter_endpoint_remediation_sla_escalation_recurrence_history,
    filter_endpoint_remediation_sla_notification_history,
    filter_endpoint_remediation_sla_report_history,
    filter_endpoint_inventory_freshness_history,
    filter_endpoint_inventory_ingestion_history,
    filter_endpoint_management_publication_history,
    filter_endpoint_reconciliation_automation_history,
    filter_managed_endpoint_reconciliation_history,
    evaluate_endpoint_inventory_freshness,
    ingest_endpoint_inventory,
    reconcile_managed_endpoint_deployment,
    review_endpoint_remediation_sla_escalation,
    record_endpoint_remediation_handoff_status,
)
from cavra.runtime import RuntimeGuard
from cavra.sandbox import (
    compliance_mapping,
    create_sandbox_run,
    evidence_json,
    pr_attestation,
    sandbox_activity_session,
    sandbox_evidence_metadata,
    sandbox_scenarios as available_sandbox_scenarios,
)

try:
    from fastapi import FastAPI, Header, HTTPException, Response
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:  # pragma: no cover
    FastAPI = None
    Header = None
    HTTPException = None
    Response = None
    CORSMiddleware = None


def create_app():
    if FastAPI is None:
        raise RuntimeError("Install fastapi and uvicorn to run the CAVRA API.")
    app = FastAPI(
        title="CAVRA API",
        description="Controlled Agentic Verification & Runtime Authority API for AI-agent runtime governance.",
        version="0.1.0",
    )
    cors_origins = _csv_env("CAVRA_CORS_ORIGINS")
    if cors_origins and CORSMiddleware is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
        )
    runs: dict[str, dict] = {}
    evidence_store = (
        SQLiteEvidenceMetadataStore(Path(os.environ["CAVRA_EVIDENCE_METADATA_DB"]))
        if os.environ.get("CAVRA_EVIDENCE_METADATA_DB")
        else EvidenceMetadataStore(Path(os.environ.get("CAVRA_EVIDENCE_METADATA_STORE", ".cavra/api/evidence-metadata.json")))
    )
    evidence_artifact_root = Path(os.environ["CAVRA_EVIDENCE_ARTIFACT_ROOT"]) if os.environ.get("CAVRA_EVIDENCE_ARTIFACT_ROOT") else None
    approval_store = (
        SQLiteApprovalStore(Path(os.environ["CAVRA_APPROVAL_DB"]))
        if os.environ.get("CAVRA_APPROVAL_DB")
        else ApprovalStore(Path(os.environ.get("CAVRA_APPROVAL_STORE", ".cavra/api/approvals.json")))
    )
    routing_rules = load_routing_rules(Path(os.environ["CAVRA_APPROVAL_ROUTING_FILE"])) if os.environ.get("CAVRA_APPROVAL_ROUTING_FILE") else None
    provider_config = load_provider_config(Path(os.environ["CAVRA_APPROVAL_PROVIDER_CONFIG"])) if os.environ.get("CAVRA_APPROVAL_PROVIDER_CONFIG") else None
    connector_config = load_connector_config(Path(os.environ["CAVRA_CONNECTOR_CONFIG"])) if os.environ.get("CAVRA_CONNECTOR_CONFIG") else None
    rbac_rules = load_rbac_rules(Path(os.environ["CAVRA_APPROVAL_RBAC_FILE"])) if os.environ.get("CAVRA_APPROVAL_RBAC_FILE") else {}
    oidc_config = load_oidc_config(Path(os.environ["CAVRA_APPROVAL_OIDC_CONFIG"])) if os.environ.get("CAVRA_APPROVAL_OIDC_CONFIG") else {}
    registry_store = (
        SQLiteRegistryStore(Path(os.environ["CAVRA_REGISTRY_DB"]))
        if os.environ.get("CAVRA_REGISTRY_DB")
        else RegistryStore(Path(os.environ.get("CAVRA_REGISTRY_STORE", ".cavra/api/registry.json")))
    )
    activity_store = (
        SQLiteActivityStore(Path(os.environ["CAVRA_ACTIVITY_DB"]))
        if os.environ.get("CAVRA_ACTIVITY_DB")
        else ActivityStore(Path(os.environ.get("CAVRA_ACTIVITY_STORE", ".cavra/api/activity.json")))
    )
    inventory_store = (
        SQLiteInventoryStore(Path(os.environ["CAVRA_INVENTORY_DB"]))
        if os.environ.get("CAVRA_INVENTORY_DB")
        else InventoryStore(Path(os.environ.get("CAVRA_INVENTORY_STORE", ".cavra/api/inventory.json")))
    )
    integration_store = (
        SQLiteIntegrationStore(Path(os.environ["CAVRA_INTEGRATION_DB"]))
        if os.environ.get("CAVRA_INTEGRATION_DB")
        else IntegrationStore(Path(os.environ.get("CAVRA_INTEGRATION_STORE", ".cavra/api/integrations.json")))
    )
    pilot_intake_store = PilotIntakeStore(Path(os.environ.get("CAVRA_PILOT_INTAKE_STORE", ".cavra/api/pilot-intakes.json")))

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "product": "CAVRA"}

    @app.get("/version")
    def version() -> dict[str, str]:
        return {"version": "0.1.0", "name": "CAVRA Runtime Server"}

    @app.get("/console/config")
    def console_config() -> dict[str, object]:
        metadata_mode = "sqlite" if isinstance(evidence_store, SQLiteEvidenceMetadataStore) else "json"
        approval_mode = "sqlite" if isinstance(approval_store, SQLiteApprovalStore) else "json"
        registry_mode = "sqlite" if isinstance(registry_store, SQLiteRegistryStore) else "json"
        activity_mode = "sqlite" if isinstance(activity_store, SQLiteActivityStore) else "json"
        inventory_mode = "sqlite" if isinstance(inventory_store, SQLiteInventoryStore) else "json"
        integration_mode = "sqlite" if isinstance(integration_store, SQLiteIntegrationStore) else "json"
        return {
            "product": "CAVRA",
            "api_base_url": os.environ.get("CAVRA_PUBLIC_API_BASE_URL", ""),
            "metadata_mode": metadata_mode,
            "approval_mode": approval_mode,
            "registry_mode": registry_mode,
            "activity_mode": activity_mode,
            "inventory_mode": inventory_mode,
            "integration_mode": integration_mode,
            "pilot_intake_mode": "json",
            "approval_provider_delivery": "configured" if provider_config is not None else "disabled",
            "connector_delivery": "configured" if connector_config is not None else "disabled",
            "approval_oidc": "configured" if oidc_config else "disabled",
            "approval_rbac": "configured" if rbac_rules else "disabled",
            "evidence_artifacts": "configured" if evidence_artifact_root else "disabled",
            "registry_store": str(registry_store.path),
            "cors_origins": cors_origins,
            "endpoints": {
                "saas_control_plane_contract": "/saas/control-plane/contract",
                "saas_operating_automation": "/saas/operating-automation",
                "saas_operating_automation_worker_handoff": "/saas/operating-automation/worker-handoff",
                "evidence": "/evidence",
                "evidence_item": "/evidence/{session_id}",
                "evidence_artifacts": "/evidence/{session_id}/artifacts",
                "evidence_artifact": "/evidence/{session_id}/artifacts/{artifact_name}",
                "evidence_artifact_bundle": "/evidence/{session_id}/artifact-bundle",
                "evidence_rollout_promotion_request": "/evidence/{session_id}/promotion-request",
                "evidence_rollout_promotion_execution": "/evidence/{session_id}/promotion-execution",
                "promotion_executions": "/promotion-executions",
                "promotion_execution": "/promotion-executions/{execution_id}",
                "promotion_execution_audit_export": "/promotion-executions/{execution_id}/audit-export",
                "promotion_execution_audit_deliver": "/promotion-executions/{execution_id}/audit-export/deliver",
                "promotion_execution_rollback": "/promotion-executions/{execution_id}/rollback-execution",
                "rollback_execution": "/rollback-executions/{rollback_id}",
                "rollback_execution_deliver": "/rollback-executions/{rollback_id}/deliver",
                "release_connector_deliveries": "/release-connector-deliveries",
                "release_connector_delivery_dashboard": "/release-connector-deliveries/dashboard",
                "release_channel_promotions": "/release-channel-promotions",
                "release_channel_promotion": "/release-channel-promotions/{request_id}",
                "endpoint_management_exports": "/endpoint-management-exports",
                "endpoint_management_export": "/endpoint-management-exports/{export_id}",
                "endpoint_management_export_dashboard": "/endpoint-management-exports/dashboard",
                "endpoint_management_export_artifacts": "/endpoint-management-exports/{export_id}/artifacts",
                "endpoint_management_export_artifact": "/endpoint-management-exports/{export_id}/artifacts/{artifact_name}",
                "endpoint_management_export_artifact_bundle": "/endpoint-management-exports/{export_id}/artifact-bundle",
                "endpoint_management_export_publish": "/endpoint-management-exports/{export_id}/publish",
                "endpoint_management_publications": "/endpoint-management-publications",
                "endpoint_management_publication_dashboard": "/endpoint-management-publications/dashboard",
                "endpoint_inventory_ingest": "/endpoint-inventory/ingest",
                "endpoint_inventory_ingestions": "/endpoint-inventory-ingestions",
                "endpoint_inventory_dashboard": "/endpoint-inventory-ingestions/dashboard",
                "endpoint_inventory_freshness_report": "/endpoint-inventory/freshness-report",
                "endpoint_inventory_freshness": "/endpoint-inventory-freshness",
                "endpoint_inventory_freshness_dashboard": "/endpoint-inventory-freshness/dashboard",
                "endpoint_deployment_reconcile": "/endpoint-deployment/reconcile",
                "endpoint_reconciliations": "/endpoint-reconciliations",
                "endpoint_reconciliation_dashboard": "/endpoint-reconciliations/dashboard",
                "endpoint_inventory_reconcile": "/endpoint-inventory-ingestions/{inventory_id}/reconcile",
                "endpoint_reconciliation_automations": "/endpoint-reconciliation-automations",
                "endpoint_reconciliation_automation_dashboard": "/endpoint-reconciliation-automations/dashboard",
                "endpoint_remediation_request": "/endpoint-reconciliations/{reconciliation_id}/remediation-request",
                "endpoint_remediation_execute": "/endpoint-remediations/{request_id}/execute",
                "endpoint_remediations": "/endpoint-remediations",
                "endpoint_remediation_dashboard": "/endpoint-remediations/dashboard",
                "endpoint_remediation_handoff": "/endpoint-remediations/{request_id}/handoff",
                "endpoint_remediation_handoffs": "/endpoint-remediation-handoffs",
                "endpoint_remediation_handoff_dashboard": "/endpoint-remediation-handoffs/dashboard",
                "endpoint_remediation_handoff_status": "/endpoint-remediation-handoffs/{handoff_id}/status",
                "endpoint_remediation_handoff_statuses": "/endpoint-remediation-handoff-statuses",
                "endpoint_remediation_handoff_status_dashboard": "/endpoint-remediation-handoff-statuses/dashboard",
                "endpoint_remediation_sla_report": "/endpoint-remediation-sla/report",
                "endpoint_remediation_sla_deliver": "/endpoint-remediation-sla-reports/{report_id}/deliver",
                "endpoint_remediation_sla_acknowledge": "/endpoint-remediation-sla-reports/{report_id}/acknowledgements",
                "endpoint_remediation_sla_notifications": "/endpoint-remediation-sla-notifications",
                "endpoint_remediation_sla_notification_dashboard": "/endpoint-remediation-sla-notifications/dashboard",
                "endpoint_remediation_sla_escalation_plan": "/endpoint-remediation-sla-notifications/escalation-plan",
                "endpoint_remediation_sla_escalation_deliver": "/endpoint-remediation-sla-escalations/{plan_id}/deliver",
                "endpoint_remediation_sla_escalation_review": "/endpoint-remediation-sla-escalations/{plan_id}/reviews",
                "endpoint_remediation_sla_escalations": "/endpoint-remediation-sla-escalations",
                "endpoint_remediation_sla_escalation_dashboard": "/endpoint-remediation-sla-escalations/dashboard",
                "endpoint_remediation_sla_escalation_actions": "/endpoint-remediation-sla-escalation-actions",
                "endpoint_remediation_sla_escalation_action_dashboard": "/endpoint-remediation-sla-escalation-actions/dashboard",
                "endpoint_remediation_sla_escalation_recurrence_plan": "/endpoint-remediation-sla-escalations/recurrence-plan",
                "endpoint_remediation_sla_escalation_recurrence_deliver": "/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/deliver",
                "endpoint_remediation_sla_escalation_suppression_audit": "/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/suppression-audit",
                "endpoint_remediation_sla_escalation_recurrence_retry_plan": "/endpoint-remediation-sla-escalation-recurrences/retry-plan",
                "endpoint_remediation_sla_escalation_owner_digest": "/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/owner-digest",
                "endpoint_remediation_sla_escalation_suppression_trends": "/endpoint-remediation-sla-escalation-recurrences/suppression-trends",
                "endpoint_remediation_sla_escalation_recurrence_automation": "/endpoint-remediation-sla-escalation-recurrences/automation-run",
                "endpoint_remediation_sla_escalation_recurrence_automations": "/endpoint-remediation-sla-escalation-recurrence-automations",
                "endpoint_remediation_sla_escalation_recurrence_automation_dashboard": "/endpoint-remediation-sla-escalation-recurrence-automations/dashboard",
                "endpoint_remediation_sla_escalation_recurrence_automation_health": "/endpoint-remediation-sla-escalation-recurrence-automations/health",
                "endpoint_remediation_sla_escalation_recurrence_automation_health_alert_deliver": "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/deliver",
                "endpoint_remediation_sla_escalation_recurrence_automation_health_alert_acknowledge": "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/{health_id}/acknowledgements",
                "endpoint_remediation_sla_escalation_recurrence_automation_health_alerts": "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts",
                "endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard": "/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/dashboard",
                "endpoint_remediation_sla_escalation_recurrences": "/endpoint-remediation-sla-escalation-recurrences",
                "endpoint_remediation_sla_escalation_recurrence_dashboard": "/endpoint-remediation-sla-escalation-recurrences/dashboard",
                "endpoint_remediation_sla_reports": "/endpoint-remediation-sla-reports",
                "endpoint_remediation_sla_dashboard": "/endpoint-remediation-sla-reports/dashboard",
                "console_session": "/console/session",
                "deployment_readiness": "/deployment/production-readiness",
                "go_backend_readiness": "/runtime/go-pilot/readiness",
                "go_deployment_readiness": "/runtime/go-pilot/deployment-readiness",
                "go_promotion_readiness": "/runtime/go-pilot/promotion-readiness",
                "go_rollback_readiness": "/runtime/go-pilot/rollback-readiness",
                "go_rollback_rehearsal": "/runtime/go-pilot/rollback-rehearsal",
                "go_rollback_drills": "/runtime/go-pilot/rollback-drills",
                "go_rollback_drill_schedule": "/runtime/go-pilot/rollback-drill-schedule",
                "go_rollback_drill_notifications": "/runtime/go-pilot/rollback-drill-notifications/deliver",
                "go_rollback_drill_notification_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/{schedule_id}/acknowledgements",
                "go_rollback_drill_notification_bulk_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk",
                "go_rollback_drill_notification_acknowledgement_audit": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package",
                "go_rollback_drill_notification_acknowledgement_audit_delivery": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_retry_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_worker": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_workers": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-runs",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_worker_dashboard": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-dashboard",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/{health_id}/acknowledgements",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alerts": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_dashboard": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alert-dashboard",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_retry_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plans/{retry_plan_id}/acknowledgements",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_retry_execution_approval_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_retry_execution_approval_decide": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plans/{approval_plan_id}/decisions",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_connector_recovery_playbook": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_connector_recovery_close": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbooks/{playbook_id}/closures",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_retry_recovery_report": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/acknowledgements",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_worker": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-worker-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/{health_id}/acknowledgements",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alerts": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_dashboard": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alert-dashboard",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_retry_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_retry_worker": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-worker-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_schedule_run": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-runs/{run_id}/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-worker-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/{health_id}/acknowledgements",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alerts": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_dashboard": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alert-dashboard",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_retry_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_retry_worker": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-worker-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closure_dashboard": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closure-dashboard",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_readiness": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_operator_runbook_export": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-operator-runbook-export",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_readiness_approval": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness/{summary_id}/approval-decisions",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_record_attachment": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-record-attachment",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closure-packet-verification",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_worker": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-worker-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_immutable_archive_reference": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-immutable-archive-reference",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_acknowledge": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/{health_id}/acknowledgements",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alerts": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_dashboard": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alert-dashboard",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_readiness_bundle": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-readiness-bundle",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_signed_archive_manifest": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-signed-archive-manifest",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_summary": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_health": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-health",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_deliver": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-health-alerts/deliver",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_plan": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary/delivery-retry-plan",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_worker": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary/delivery-retry-worker-run",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_review": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-review",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_decision": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-review/{review_id}/decisions",
                "go_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_artifact_bundle": "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-artifact-bundle",
                "go_rollback_drill_notification_history": "/runtime/go-pilot/rollback-drill-notifications",
                "go_rollback_drill_notification_dashboard": "/runtime/go-pilot/rollback-drill-notifications/dashboard",
                "go_rollback_drill_notification_escalation_plan": "/runtime/go-pilot/rollback-drill-notifications/escalation-plan",
                "go_rollback_drill_notification_routes": "/runtime/go-pilot/rollback-drill-notifications/routes",
                "go_rollback_drill_notification_suppression_trends": "/runtime/go-pilot/rollback-drill-notifications/suppression-trends",
                "go_backend_evaluate": "/runtime/go-pilot/evaluate",
                "policy_pack_catalog": "/policy-pack-catalog",
                "policy_pack_draft": "/policy-packs/draft",
                "policy_pack_publish_plan": "/policy-packs/publish-plan",
                "policy_pack_publish_request": "/policy-packs/publish-request",
                "policy_pack_publish": "/policy-packs/publish",
                "approvals": "/approvals",
                "sessions": "/sessions",
                "decisions": "/decisions",
                "aispm_dashboard_contract": "/aispm/dashboard/contract",
                "aispm_sample": "/aispm/dashboard/sample",
                "aispm_posture": "/aispm/posture",
                "aispm_agents": "/aispm/agents",
                "aispm_findings": "/aispm/findings",
                "aispm_timeline": "/aispm/timeline",
                "aispm_control_coverage": "/aispm/control-coverage",
                "aispm_control_coverage_heatmap": "/aispm/control-coverage-heatmap",
                "aispm_near_misses": "/aispm/near-misses",
                "aispm_trace_replay": "/aispm/trace-replay/{session_id}",
                "aispm_approval_lineage": "/aispm/approval-lineage",
                "aispm_behavior_fingerprints": "/aispm/behavior-fingerprints",
                "aispm_policy_context_gaps": "/aispm/policy-context-gaps",
                "aispm_pre_action_risk_forecasts": "/aispm/pre-action-risk-forecasts",
                "aispm_intent_action_drift": "/aispm/intent-action-drift",
                "aispm_tool_chain_graph": "/aispm/tool-chain-graph",
                "aispm_agent_blast_radius": "/aispm/agent-blast-radius",
                "aispm_evidence_confidence": "/aispm/evidence-confidence",
                "repositories": "/repositories",
                "policy_rollouts": "/policy-rollouts",
                "policy_rollout_change_plan": "/policy-rollouts/change-plan",
                "policy_rollout_apply_change": "/policy-rollouts/apply-change",
                "policy_rollout_detail": "/policy-rollouts/{rollout_id}/detail",
                "console_security_boundary": "/console/security-boundary",
                "operations_stores": "/operations/stores",
                "operations_retention_plan": "/operations/retention-plan",
                "integrations": "/integrations",
                "integration_deliver": "/integrations/{integration_id}/deliver",
                "pilot_intakes": "/pilot-intakes",
                "pilot_intake": "/pilot-intakes/{intake_id}",
                "pilot_intake_readiness": "/pilot-intakes/{intake_id}/readiness",
                "pilot_intake_private_handoff_plan": "/pilot-intakes/{intake_id}/private-handoff-plan",
                "agents": "/agents",
                "agent_enforcement_readiness": "/agents/enforcement-readiness",
                "mcp_servers": "/mcp/servers",
                "mcp_trust": "/mcp/trust",
                "sandbox_scenarios": "/api/sandbox/scenarios",
                "sandbox_metrics": "/api/sandbox/metrics",
                "sandbox_run": "/api/sandbox/run",
                "sandbox_run_item": "/api/sandbox/runs/{run_id}",
                "sandbox_run_events": "/api/sandbox/runs/{run_id}/events",
                "sandbox_run_evidence": "/api/sandbox/runs/{run_id}/evidence",
                "sandbox_run_attestation": "/api/sandbox/runs/{run_id}/attestation",
                "sandbox_run_compliance": "/api/sandbox/runs/{run_id}/compliance",
            },
        }

    @app.get("/saas/control-plane/contract")
    def saas_control_plane_contract() -> dict[str, object]:
        return describe_public_contract()

    @app.post("/saas/operating-automation")
    def saas_operating_automation(payload: dict) -> dict[str, object]:
        try:
            request = build_saas_operating_automation_request(
                str(payload.get("tenant_id", "")),
                requested_by=str(payload.get("requested_by", "community")),
                automation_scope=str(payload.get("automation_scope", "trial-to-paid-customer-scale")),
                automation_cadence=str(payload.get("automation_cadence", "daily")),
                required_checks=tuple(payload.get("required_checks", SAAS_OPERATING_AUTOMATION_CHECKS)),
            )
            summary = SaaSOperatingAutomationSummary(
                tenant_id=request.tenant_id,
                automation_status=str(payload.get("automation_status", "unknown")),
                billing_monitoring_status=str(payload.get("billing_monitoring_status", "unknown")),
                license_telemetry_status=str(payload.get("license_telemetry_status", "unknown")),
                support_followup_status=str(payload.get("support_followup_status", "unknown")),
                customer_success_review_status=str(payload.get("customer_success_review_status", "unknown")),
                dashboard_refresh_status=str(payload.get("dashboard_refresh_status", "unknown")),
                escalation_drill_status=str(payload.get("escalation_drill_status", "unknown")),
                closeout_retry_status=str(payload.get("closeout_retry_status", "unknown")),
                automation_scope=str(payload.get("automation_scope", "trial-to-paid-customer-scale")),
                automation_cadence=str(payload.get("automation_cadence", "daily")),
                blockers=tuple(payload.get("blockers") or ()),
            )
            response = build_saas_operating_automation_response(request, summary)
        except SaaSContractError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "request": request.to_dict(),
            "response": response.to_dict(),
        }

    @app.post("/saas/operating-automation/worker-handoff")
    def saas_operating_automation_worker_handoff(payload: dict) -> dict[str, object]:
        try:
            required_checks = tuple(payload.get("required_checks", SAAS_OPERATING_AUTOMATION_CHECKS))
            worker_targets = tuple(payload.get("worker_targets", SAAS_OPERATING_AUTOMATION_CHECKS))
            request = build_saas_operating_automation_worker_handoff_request(
                str(payload.get("tenant_id", "")),
                requested_by=str(payload.get("requested_by", "community")),
                deployment_environment=str(payload.get("deployment_environment", "production")),
                worker_mode=str(payload.get("worker_mode", "dry_run")),
                required_checks=required_checks,
                worker_targets=worker_targets,
            )
            summary = SaaSOperatingAutomationWorkerHandoffSummary(
                tenant_id=request.tenant_id,
                handoff_status=str(payload.get("handoff_status", "requires_private_service")),
                deployment_environment=str(payload.get("deployment_environment", "production")),
                scheduler_ref=str(payload.get("scheduler_ref", "scheduler-pending")),
                evidence_sink_ref=str(payload.get("evidence_sink_ref", "evidence-sink-pending")),
                retry_policy_ref=str(payload.get("retry_policy_ref", "retry-policy-pending")),
                worker_owner=str(payload.get("worker_owner", "operations-owner")),
                worker_mode=str(payload.get("worker_mode", "dry_run")),
                required_checks=required_checks,
                worker_targets=worker_targets,
                blockers=tuple(payload.get("blockers") or ()),
            )
            response = build_saas_operating_automation_worker_handoff_response(request, summary)
        except SaaSContractError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "request": request.to_dict(),
            "response": response.to_dict(),
        }

    @app.get("/policies")
    @app.get("/policy-packs")
    def policies() -> list[dict]:
        return PolicyRegistry().list_policy_packs()

    @app.get("/policy-pack-catalog")
    def policy_pack_catalog() -> dict[str, object]:
        packs = PolicyRegistry().list_policy_packs()
        return {
            "schema_version": "cavra.policy_pack.catalog.v1",
            "product": "CAVRA",
            "total": len(packs),
            "items": [
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "version": item.get("version"),
                    "summary": summarize_policy(item.get("policy", {})),
                }
                for item in packs
            ],
        }

    @app.post("/policy-packs/draft")
    def policy_pack_draft(payload: dict) -> dict:
        try:
            return build_policy_pack_draft(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/policy-packs/publish-plan")
    def policy_pack_publish_plan(payload: dict) -> dict:
        draft_payload = payload.get("draft") if isinstance(payload.get("draft"), dict) else payload
        try:
            return build_policy_pack_publish_plan(draft_payload, _current_policy_for_draft(draft_payload))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/policy-packs/publish-request")
    def policy_pack_publish_request(payload: dict, authorization: Optional[str] = Header(default=None)) -> dict:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        draft_payload = payload.get("draft") if isinstance(payload.get("draft"), dict) else payload
        try:
            plan = build_policy_pack_publish_plan(draft_payload, _current_policy_for_draft(draft_payload))
            requested_by = actor_context.get("actor") if actor_context else payload.get("requested_by", "policy-authoring-console")
            decision = build_policy_publish_decision(
                plan,
                requested_by=str(requested_by),
                approver_group=payload.get("approver_group", "Platform Security"),
                repository=payload.get("repository"),
            )
            approval = approval_store.create_request(
                decision,
                approver_group=payload.get("approver_group", "Platform Security"),
                requested_by=str(requested_by),
                ttl_hours=int(payload.get("ttl_hours", 24)),
                routing_rules=routing_rules,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "schema_version": "cavra.policy_pack.publish_request.v1",
            "product": "CAVRA",
            "plan": plan,
            "approval": approval,
        }

    @app.post("/policy-packs/publish")
    def policy_pack_publish(payload: dict, authorization: Optional[str] = Header(default=None)) -> dict:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        draft_payload = payload.get("draft") if isinstance(payload.get("draft"), dict) else payload
        approval_id = payload.get("approval_id")
        if not approval_id:
            raise HTTPException(status_code=400, detail="approval_id is required")
        approval = approval_store.get(str(approval_id))
        if approval is None:
            raise HTTPException(status_code=404, detail="approval not found")
        if actor_context and not actor_can_decide(actor_context, approval, action="approved", rbac_rules=rbac_rules):
            raise HTTPException(status_code=403, detail="actor is not authorized to publish this policy")
        try:
            return publish_policy_pack(
                draft_payload,
                approval,
                signer=payload.get("signer") or (actor_context.get("actor") if actor_context else "policy-authoring-api"),
                key=os.environ.get("CAVRA_POLICY_SIGNING_KEY"),
                actor=actor_context.get("actor") if actor_context else payload.get("actor", "policy-authoring-api"),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/decisions")
    def decision_index(
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        decision: Optional[str] = None,
        severity: Optional[str] = None,
        action_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return activity_store.list_decisions(
            session_id=session_id,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            decision=decision,
            severity=severity,
            action_type=action_type,
            limit=limit,
            offset=offset,
        )

    @app.post("/decisions")
    def decisions(payload: dict) -> dict:
        guard = RuntimeGuard(
            policy_pack=payload.get("policy_pack") or "cavra-ai-agent-baseline",
            session_id=payload.get("session_id", "local"),
            agent_id=payload.get("agent_id", "unknown-agent"),
            actor=payload.get("actor", "ai-agent"),
            registry_store=registry_store,
        )
        action_type = payload.get("action_type")
        target = payload.get("target", "")
        if action_type == "read_file":
            result = guard.evaluate_file_access(Path(target), "read").to_dict()
        elif action_type == "write_file":
            result = guard.evaluate_file_access(Path(target), "write").to_dict()
        elif action_type == "execute_command":
            result = guard.evaluate_command(target).to_dict()
        elif action_type == "git_operation":
            result = guard.evaluate_git_action(payload.get("operation", "push"), target).to_dict()
        else:
            result = guard.evaluate_mcp_tool_call(payload.get("server", "unknown"), payload.get("tool", "unknown"), payload.get("capability")).to_dict()
        if payload.get("repository"):
            result["repository"] = payload["repository"]
        return activity_store.upsert_decision(result)

    @app.get("/decisions/{decision_id}")
    def decision_item(decision_id: str) -> dict:
        item = activity_store.get_decision(decision_id)
        if item is None:
            raise HTTPException(status_code=404, detail="decision not found")
        return item

    @app.get("/sessions")
    def session_index(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return activity_store.list_sessions(
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            state=state,
            limit=limit,
            offset=offset,
        )

    @app.post("/sessions")
    def upsert_session(payload: dict) -> dict:
        try:
            return activity_store.upsert_session(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid session record") from exc

    @app.get("/sessions/{session_id}")
    def session_item(session_id: str) -> dict:
        item = activity_store.get_session(session_id)
        if item is None:
            raise HTTPException(status_code=404, detail="session not found")
        return item

    @app.get("/aispm/dashboard/contract")
    def aispm_dashboard_contract() -> dict:
        return build_aispm_dashboard_contract()

    @app.get("/aispm/dashboard/sample")
    def aispm_dashboard_sample() -> dict:
        return build_sample_aispm_dashboard()

    @app.get("/aispm/posture")
    def aispm_posture(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_posture(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/agents")
    def aispm_agents(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        posture = build_aispm_posture(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )
        return {
            "schema_version": "cavra.aispm.agents.v1",
            "data_provenance": posture["data_provenance"],
            "items": posture["agents"],
            "total": len(posture["agents"]),
        }

    @app.get("/aispm/findings")
    def aispm_findings(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        posture = build_aispm_posture(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )
        return {
            "schema_version": "cavra.aispm.findings.v1",
            "data_provenance": posture["data_provenance"],
            "items": posture["findings"],
            "total": len(posture["findings"]),
        }

    @app.get("/aispm/timeline")
    def aispm_timeline(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        posture = build_aispm_posture(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )
        return {
            "schema_version": "cavra.aispm.timeline.v1",
            "data_provenance": posture["data_provenance"],
            "items": posture["timeline"],
            "total": len(posture["timeline"]),
        }

    @app.get("/aispm/control-coverage")
    def aispm_control_coverage(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        posture = build_aispm_posture(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )
        return {
            "schema_version": "cavra.aispm.control_coverage.v1",
            "data_provenance": posture["data_provenance"],
            "items": posture["control_coverage"],
            "total": len(posture["control_coverage"]),
        }

    @app.get("/aispm/control-coverage-heatmap")
    def aispm_control_coverage_heatmap(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_control_coverage_heatmap(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/evidence-confidence")
    def aispm_evidence_confidence(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_evidence_confidence_drilldown(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/near-misses")
    def aispm_near_misses(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        posture = build_aispm_posture(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )
        return {
            "schema_version": "cavra.aispm.near_misses.v1",
            "data_provenance": posture["data_provenance"],
            "items": posture["near_misses"],
            "total": len(posture["near_misses"]),
        }

    @app.get("/aispm/behavior-fingerprints")
    def aispm_behavior_fingerprints(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_behavior_fingerprints(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/policy-context-gaps")
    def aispm_policy_context_gaps(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_policy_context_gaps(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/pre-action-risk-forecasts")
    def aispm_pre_action_risk_forecasts(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_pre_action_risk_forecasts(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/intent-action-drift")
    def aispm_intent_action_drift(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_intent_action_drift(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/tool-chain-graph")
    def aispm_tool_chain_graph(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_tool_chain_graph(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/agent-blast-radius")
    def aispm_agent_blast_radius(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_agent_blast_radius(
            activity_store,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            limit=limit,
        )

    @app.get("/aispm/trace-replay/{session_id}")
    def aispm_trace_replay(session_id: str, limit: int = 200) -> dict:
        packet = build_aispm_trace_replay_packet(activity_store, session_id=session_id, limit=limit)
        if packet is None:
            raise HTTPException(status_code=404, detail="trace replay session not found")
        return packet

    @app.get("/aispm/approval-lineage")
    def aispm_approval_lineage(
        state: Optional[str] = None,
        approver_group: Optional[str] = None,
        session_id: Optional[str] = None,
        limit: int = 200,
    ) -> dict:
        return build_aispm_approval_lineage(
            approval_store,
            activity_store,
            state=state,
            approver_group=approver_group,
            session_id=session_id,
            limit=limit,
        )

    @app.get("/operations/stores")
    def operations_store_index() -> dict:
        return persistent_api_store_status()

    @app.get("/console/security-boundary")
    def console_security_boundary() -> dict[str, object]:
        return _console_security_boundary(
            oidc_configured=bool(oidc_config),
            rbac_configured=bool(rbac_rules),
            cors_origins=cors_origins,
        )

    @app.get("/console/session")
    def console_session(authorization: Optional[str] = Header(default=None)) -> dict[str, object]:
        return _console_session_context(
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )

    @app.get("/operations/retention-plan")
    def operations_retention_plan(
        retention_days: int = 2555,
        classification: str = "regulated-sdlc",
        legal_hold: bool = False,
    ) -> dict:
        try:
            return build_persistent_api_retention_plan(
                retention_days=retention_days,
                classification=classification,
                legal_hold=legal_hold,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid retention plan request") from exc

    @app.get("/deployment/production-readiness")
    def deployment_production_readiness() -> dict[str, object]:
        return production_readiness_report(
            oidc_configured=bool(oidc_config),
            rbac_configured=bool(rbac_rules),
            cors_origins=cors_origins,
            evidence_artifact_root_configured=bool(evidence_artifact_root),
            policy_pack_count=len(PolicyRegistry().list_policy_packs()),
            store_status=persistent_api_store_status(),
            go_backend_readiness=go_backend_readiness_report(),
            go_deployment_readiness=go_deployment_readiness_report(),
            go_promotion_readiness=go_promotion_readiness_report(),
            go_rollback_readiness=go_rollback_readiness_report(),
            go_rollback_rehearsal=go_rollback_rehearsal_report(),
            go_rollback_drill_history=go_rollback_drill_history_report(),
            go_rollback_drill_schedule=go_rollback_drill_schedule_report(),
        )

    @app.get("/runtime/go-pilot/readiness")
    def runtime_go_pilot_readiness() -> dict[str, object]:
        return go_backend_readiness_report()

    @app.get("/runtime/go-pilot/deployment-readiness")
    def runtime_go_pilot_deployment_readiness() -> dict[str, object]:
        return go_deployment_readiness_report()

    @app.get("/runtime/go-pilot/promotion-readiness")
    def runtime_go_pilot_promotion_readiness() -> dict[str, object]:
        return go_promotion_readiness_report()

    @app.get("/runtime/go-pilot/rollback-readiness")
    def runtime_go_pilot_rollback_readiness() -> dict[str, object]:
        return go_rollback_readiness_report()

    @app.get("/runtime/go-pilot/rollback-rehearsal")
    def runtime_go_pilot_rollback_rehearsal() -> dict[str, object]:
        return go_rollback_rehearsal_report()

    @app.get("/runtime/go-pilot/rollback-drills")
    def runtime_go_pilot_rollback_drills() -> dict[str, object]:
        return go_rollback_drill_history_report()

    @app.get("/runtime/go-pilot/rollback-drill-schedule")
    def runtime_go_pilot_rollback_drill_schedule() -> dict[str, object]:
        return go_rollback_drill_schedule_report()

    @app.post("/runtime/go-pilot/rollback-drill-notifications/deliver")
    def runtime_go_pilot_rollback_drill_notification_deliver(payload: dict) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        try:
            report = go_rollback_drill_schedule_report()
            plan = build_go_rollback_drill_notification_plan(
                report,
                requested_provider=payload.get("provider", "all"),
                available_providers=_configured_connector_providers(connector_config),
                generated_by=payload.get("generated_by", "console"),
                force=bool(payload.get("force", False)),
                routing_policy=payload.get("routing_policy") if isinstance(payload.get("routing_policy"), dict) else None,
            )
            event = build_go_rollback_drill_notification_event(
                report,
                generated_by=payload.get("generated_by", "console"),
                routing_policy=payload.get("routing_policy") if isinstance(payload.get("routing_policy"), dict) else None,
            )
            event["notification_plan"] = plan
            plan_metadata = evidence_store.upsert(build_go_rollback_drill_notification_plan_metadata(plan))
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="go_backend_rollback_drill_notification",
                    )
                )
            return {
                "schedule": report,
                "plan": plan,
                "delivery": result,
                "plan_metadata": plan_metadata,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": plan.get("schedule_id") or plan.get("plan_id"),
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/runtime/go-pilot/rollback-drill-notifications/{schedule_id}/acknowledgements")
    def runtime_go_pilot_rollback_drill_notification_acknowledge(
        schedule_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_go_rollback_drill_notification(
                schedule_id,
                provider=payload["provider"],
                acknowledged_by=str(acknowledged_by),
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                plan_id=payload.get("plan_id"),
            )
            metadata = evidence_store.upsert(build_go_rollback_drill_notification_ack_metadata(acknowledgement))
            return {
                "acknowledgement": acknowledgement,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/bulk")
    def runtime_go_pilot_rollback_drill_notification_bulk_acknowledge(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        routes = payload.get("routes")
        if not isinstance(routes, list) or not routes:
            raise HTTPException(status_code=400, detail="routes are required")
        if len(routes) > 100:
            raise HTTPException(status_code=400, detail="bulk acknowledgement is limited to 100 routes")
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        acknowledgements = []
        metadata_items = []
        try:
            for route in routes:
                if not isinstance(route, dict):
                    raise ValueError("each route must be an object")
                schedule_id = str(route.get("schedule_id") or "").strip()
                provider = str(route.get("provider") or "").strip()
                if not schedule_id or not provider:
                    raise ValueError("each route requires schedule_id and provider")
                acknowledgement = acknowledge_go_rollback_drill_notification(
                    schedule_id,
                    provider=provider,
                    acknowledged_by=str(acknowledged_by),
                    acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                    external_ref=route.get("external_ref") or payload.get("external_ref"),
                    notes=route.get("notes") or payload.get("notes"),
                    plan_id=route.get("plan_id") or payload.get("plan_id"),
                )
                acknowledgements.append(acknowledgement)
                metadata_items.append(evidence_store.upsert(build_go_rollback_drill_notification_ack_metadata(acknowledgement)))
            return {
                "schema_version": "cavra.go-backend-pilot.rollback-drill-bulk-acknowledgement.v1",
                "product": "CAVRA",
                "bulk_id": f"gordbulkack-{len(acknowledgements)}-{acknowledgements[0]['acknowledgement_id']}",
                "acknowledgement_state": payload.get("acknowledgement_state", "acknowledged"),
                "acknowledgement_count": len(acknowledgements),
                "acknowledgements": acknowledgements,
                "metadata": metadata_items,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-package")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        package = build_go_rollback_drill_acknowledgement_audit_package(
            _go_rollback_drill_notification_items(evidence_store),
            schedule_id=payload.get("schedule_id"),
            provider=payload.get("provider"),
            owner=payload.get("owner"),
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(build_go_rollback_drill_acknowledgement_audit_package_metadata(package))
        return {
            "audit_package": package,
            "metadata": metadata,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        package = build_go_rollback_drill_acknowledgement_audit_package(
            _go_rollback_drill_notification_items(evidence_store),
            schedule_id=payload.get("schedule_id"),
            provider=payload.get("provider"),
            owner=payload.get("owner"),
            generated_by=str(generated_by),
        )
        audit_metadata = evidence_store.upsert(build_go_rollback_drill_acknowledgement_audit_package_metadata(package))
        try:
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_plan(
                package,
                requested_provider=payload.get("delivery_provider", payload.get("provider", "all")),
                available_providers=_configured_connector_providers(connector_config),
                generated_by=str(generated_by),
                cadence=str(payload.get("cadence") or "on_demand"),
                schedule_ref=payload.get("schedule_ref"),
                next_delivery_at=payload.get("next_delivery_at"),
            )
            plan_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata(plan)
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_event(
                package,
                plan,
                generated_by=str(generated_by),
            )
            result = None
            delivery_metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="go_backend_rollback_drill_acknowledgement_audit",
                    )
                    | {
                        "audit_id": package.get("audit_id"),
                        "delivery_id": plan.get("delivery_id"),
                    }
                )
            return {
                "audit_package": package,
                "audit_metadata": audit_metadata,
                "delivery_plan": plan,
                "plan_metadata": plan_metadata,
                "delivery": result,
                "metadata": delivery_metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else bool(plan["selected_providers"]),
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plan")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_retry_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan(
                _go_rollback_drill_notification_items(evidence_store),
                policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
                generated_by=str(generated_by),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan_metadata(plan)
            )
            return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-run")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        dry_run = bool(payload.get("dry_run", not bool(payload.get("execute", False))))
        items = _go_rollback_drill_notification_items(evidence_store)
        run = build_go_rollback_drill_acknowledgement_audit_delivery_worker_run(
            items,
            retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
            generated_by=str(generated_by),
            dry_run=dry_run,
            max_retry_deliveries=int(payload.get("max_retry_deliveries", 5)),
        )
        retry_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_retry_plan_metadata(run["retry_plan"])
        )
        packages = {
            str(item.get("audit_id") or ""): item.get("acknowledgement_audit_package")
            for item in items
            if item.get("metadata_kind") == "go-backend-rollback-drill-acknowledgement-audit-package"
            and isinstance(item.get("acknowledgement_audit_package"), dict)
        }
        approved_retry_execution_decisions = {}
        for item in items:
            if (
                item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision"
                and item.get("approval_state") == "approved"
            ):
                approved_retry_execution_decisions[
                    (
                        str(item.get("provider") or ""),
                        str(item.get("delivery_id") or ""),
                        str(item.get("audit_id") or ""),
                    )
                ] = (
                    item.get("retry_execution_approval_decision")
                    if isinstance(item.get("retry_execution_approval_decision"), dict)
                    else item
                )
        retry_results = []
        for decision in run.get("selected_retries", []):
            if not isinstance(decision, dict):
                continue
            audit_id = str(decision.get("audit_id") or "")
            package = packages.get(audit_id)
            skipped = None
            plan = None
            plan_metadata = None
            delivery = None
            delivery_metadata = None
            execution_record = None
            execution_metadata = None
            approval_decision = approved_retry_execution_decisions.get(
                (
                    str(decision.get("provider") or ""),
                    str(decision.get("delivery_id") or ""),
                    str(decision.get("audit_id") or ""),
                )
            )
            if package is None:
                skipped = "audit_package_not_found"
            else:
                plan = build_go_rollback_drill_acknowledgement_audit_delivery_plan(
                    package,
                    requested_provider=str(decision.get("provider") or payload.get("provider", "all")),
                    available_providers=_configured_connector_providers(connector_config) if connector_config else [],
                    generated_by=str(generated_by),
                    cadence="retry",
                    schedule_ref=f"retry:{run['run_id']}",
                )
                plan_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata(plan)
                )
                if dry_run:
                    skipped = "dry_run"
                elif connector_config is None:
                    skipped = "connector_config_not_configured"
                elif plan["selected_providers"]:
                    event = build_go_rollback_drill_acknowledgement_audit_delivery_event(
                        package,
                        plan,
                        generated_by=str(generated_by),
                    )
                    delivery = deliver_connector_event(
                        event,
                        connector_config,
                        provider=",".join(plan["selected_providers"]),
                        retries=int(payload.get("retries", 2)),
                        timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                    )
                    delivery_metadata = evidence_store.upsert(
                        build_connector_delivery_metadata(
                            delivery,
                            source="go_backend_rollback_drill_acknowledgement_audit",
                        )
                        | {
                            "audit_id": package.get("audit_id"),
                            "delivery_id": plan.get("delivery_id"),
                            "retry_plan_id": run["retry_plan"].get("retry_plan_id"),
                            "worker_run_id": run.get("run_id"),
                        }
                    )
            if not dry_run and approval_decision is not None:
                execution_record = build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record(
                    run,
                    decision,
                    approval_decision=approval_decision,
                    delivery_plan=plan,
                    delivery=delivery,
                    delivery_metadata=delivery_metadata,
                    skipped=skipped,
                    executed_by=str(generated_by),
                )
                execution_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_record_metadata(
                        execution_record
                    )
                )
            retry_results.append(
                {
                    "decision": decision,
                    "delivery_plan": plan,
                    "plan_metadata": plan_metadata,
                    "delivery": delivery,
                    "delivery_metadata": delivery_metadata,
                    "execution_record": execution_record,
                    "execution_metadata": execution_metadata,
                    "skipped": skipped,
                }
            )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_worker_run_metadata(run)
        )
        return {
            "run": run,
            "metadata": metadata,
            "retry_metadata": retry_metadata,
            "retry_results": retry_results,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.get("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-runs")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_runs(
        dry_run: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_acknowledgement_audit_delivery_worker_history(
            _go_rollback_drill_notification_items(evidence_store),
            dry_run=dry_run,
            limit=limit,
            offset=offset,
        )

    @app.get("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-dashboard")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_dashboard() -> dict[str, object]:
        return build_go_rollback_drill_acknowledgement_audit_delivery_worker_dashboard(
            _go_rollback_drill_notification_items(evidence_store)
        )

    @app.get("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-recovery-report")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_retry_recovery_report(
        recovery_slo_minutes: int = 240,
        generated_by: str = "console",
    ) -> dict[str, object]:
        report = build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report(
            _go_rollback_drill_notification_items(evidence_store),
            recovery_slo_minutes=recovery_slo_minutes,
            generated_by=generated_by,
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_retry_recovery_report_metadata(report)
        )
        return {"report": report, "metadata": metadata}

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalation-plan")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan(
            _go_rollback_drill_notification_items(evidence_store),
            recovery_slo_minutes=int(payload.get("recovery_slo_minutes", 240)),
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan_metadata(plan)
        )
        return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_deliver_route(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        return runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_deliver(
            payload,
            authorization,
        )

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/{health_id}/acknowledgements"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_acknowledge_route(
        health_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        return runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_acknowledge(
            health_id,
            payload,
            authorization,
        )

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_deliver(
        plan_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        items = _go_rollback_drill_notification_items(evidence_store)
        plan_metadata = next(
            (
                item
                for item in items
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan"
                and item.get("plan_id") == plan_id
                and isinstance(item.get("recovery_escalation_plan"), dict)
            ),
            None,
        )
        plan = plan_metadata["recovery_escalation_plan"] if plan_metadata else None
        if plan is None and plan_id == "latest":
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan(
                items,
                recovery_slo_minutes=int(payload.get("recovery_slo_minutes", 240)),
                generated_by=str(generated_by),
            )
            plan_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_plan_metadata(plan)
            )
        if plan is None:
            raise HTTPException(status_code=404, detail="recovery escalation plan not found")
        event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_event(
            plan,
            generated_by=str(generated_by),
            max_routes=int(payload.get("max_routes", 20)),
        )
        requested_provider = str(payload.get("provider") or ",".join(plan.get("selected_providers") or []) or "webhook")
        result = deliver_connector_event(
            event,
            connector_config,
            provider=requested_provider,
            retries=int(payload.get("retries", 2)),
            timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
        )
        metadata = evidence_store.upsert(
            build_connector_delivery_metadata(
                result,
                source="go_backend_rollback_drill_acknowledgement_audit_recovery_escalation",
            )
            | {"plan_id": plan.get("plan_id"), "selected_providers": result.get("providers", [])}
        )
        return {
            "plan": plan,
            "delivery": result,
            "plan_metadata": plan_metadata,
            "metadata": metadata,
            "success": bool(result.get("success")),
            "event_id": plan.get("plan_id"),
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/{plan_id}/acknowledgements"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_acknowledge(
        plan_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation(
                plan_id,
                provider=payload["provider"],
                acknowledged_by=str(acknowledged_by),
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                escalation_reason=payload.get("escalation_reason"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_ack_metadata(
                    acknowledgement
                )
            )
            return {
                "acknowledgement": acknowledgement,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-plan"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan(
            _go_rollback_drill_notification_items(evidence_store),
            policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan_metadata(
                plan
            )
        )
        return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-worker-run"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        dry_run = bool(payload.get("dry_run", not bool(payload.get("execute", False))))
        items = _go_rollback_drill_notification_items(evidence_store)
        run = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run(
            items,
            retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
            generated_by=str(generated_by),
            dry_run=dry_run,
            max_retry_deliveries=int(payload.get("max_retry_deliveries", 5)),
        )
        retry_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_delivery_retry_plan_metadata(
                run["retry_plan"]
            )
        )
        escalation_plans = {
            str(item.get("plan_id") or ""): item.get("recovery_escalation_plan")
            for item in items
            if item.get("metadata_kind")
            == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan"
            and isinstance(item.get("recovery_escalation_plan"), dict)
        }
        retry_results = []
        for decision in run.get("selected_retries", []):
            if not isinstance(decision, dict):
                continue
            plan = escalation_plans.get(str(decision.get("plan_id") or ""))
            delivery = None
            delivery_metadata = None
            execution_record = None
            execution_metadata = None
            skipped = None
            if plan is None:
                skipped = "recovery_escalation_plan_not_found"
            elif dry_run:
                skipped = "dry_run"
            elif connector_config is None:
                skipped = "connector_config_not_configured"
            else:
                event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_event(
                    plan,
                    generated_by=str(generated_by),
                    max_routes=int(payload.get("max_routes", 20)),
                )
                delivery = deliver_connector_event(
                    event,
                    connector_config,
                    provider=str(decision.get("provider") or payload.get("provider", "webhook")),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        delivery,
                        source="go_backend_rollback_drill_acknowledgement_audit_recovery_escalation",
                    )
                    | {
                        "plan_id": plan.get("plan_id"),
                        "retry_plan_id": run["retry_plan"].get("retry_plan_id"),
                        "worker_run_id": run.get("run_id"),
                    }
                )
            if not dry_run:
                execution_record = (
                    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record(
                        run,
                        decision,
                        plan=plan,
                        delivery=delivery,
                        delivery_metadata=delivery_metadata,
                        skipped=skipped,
                        executed_by=str(generated_by),
                    )
                )
                execution_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_execution_record_metadata(
                        execution_record
                    )
                )
            retry_results.append(
                {
                    "decision": decision,
                    "plan": plan,
                    "delivery": delivery,
                    "delivery_metadata": delivery_metadata,
                    "execution_record": execution_record,
                    "execution_metadata": execution_metadata,
                    "skipped": skipped,
                }
            )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_worker_run_metadata(run)
        )
        return {
            "run": run,
            "metadata": metadata,
            "retry_metadata": retry_metadata,
            "retry_results": retry_results,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health(
        expected_interval_minutes: int = 30,
        stale_metadata_minutes: int = 120,
        generated_by: str = "console",
    ) -> dict[str, object]:
        health = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health(
            _go_rollback_drill_notification_items(evidence_store),
            expected_interval_minutes=expected_interval_minutes,
            stale_metadata_minutes=stale_metadata_minutes,
            generated_by=generated_by,
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_metadata(
                health
            )
        )
        return {"health": health, "metadata": metadata}

    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_deliver(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            health = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health(
                _go_rollback_drill_notification_items(evidence_store),
                expected_interval_minutes=int(payload.get("expected_interval_minutes", 30)),
                stale_metadata_minutes=int(payload.get("stale_metadata_minutes", 120)),
                generated_by=str(generated_by),
            )
            existing_deliveries = _search_evidence_metadata(
                evidence_store,
                metadata_kind="release-connector-delivery",
                limit=500,
                offset=0,
            )["items"]
            plan = (
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan(
                    health,
                    delivery_items=existing_deliveries,
                    requested_provider=payload.get("provider", "all"),
                    available_providers=_configured_connector_providers(connector_config),
                    generated_by=str(generated_by),
                    suppression_window_minutes=int(payload.get("suppression_window_minutes", 60)),
                    force=bool(payload.get("force", False)),
                )
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_event(
                health,
                generated_by=str(generated_by),
                max_alerts=int(payload.get("max_alerts", 20)),
            )
            event["recovery_escalation_retry_health_alert_plan"] = plan
            plan_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_plan_metadata(
                    plan
                )
            )
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert",
                    )
                    | {"health_id": plan.get("health_id"), "plan_id": plan.get("plan_id")}
                )
            return {
                "health": health,
                "plan": plan,
                "delivery": result,
                "plan_metadata": plan_metadata,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": plan.get("health_id"),
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_acknowledge(
        health_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert(
                health_id,
                provider=payload["provider"],
                acknowledged_by=str(acknowledged_by),
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                plan_id=payload.get("plan_id"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_ack_metadata(
                    acknowledgement
                )
            )
            return {
                "acknowledgement": acknowledgement,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alerts(
        health_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        suppressed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_history(
            _go_rollback_drill_notification_items(evidence_store),
            health_id=health_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alert-dashboard"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_dashboard() -> dict[str, object]:
        return build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_dashboard(
            _go_rollback_drill_notification_items(evidence_store)
        )

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-plan"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_retry_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan(
            _go_rollback_drill_notification_items(evidence_store),
            policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_metadata(
                plan
            )
        )
        return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-escalations/retry-health-alerts/retry-worker-run"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_retry_worker_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        dry_run = bool(payload.get("dry_run", not bool(payload.get("execute", False))))
        if not dry_run and connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        items = _go_rollback_drill_notification_items(evidence_store)
        run = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run(
            items,
            retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
            generated_by=str(generated_by),
            dry_run=dry_run,
            max_retry_deliveries=int(payload.get("max_retry_deliveries", 5)),
        )
        retry_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_plan_metadata(
                run["retry_plan"]
            )
        )
        health_reports = {
            str(item.get("health_id") or ""): item.get("recovery_escalation_retry_health")
            for item in items
            if item.get("metadata_kind")
            == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health"
            and isinstance(item.get("recovery_escalation_retry_health"), dict)
        }
        retry_results = []
        for decision in run.get("selected_retries", []):
            if not isinstance(decision, dict):
                continue
            health = health_reports.get(str(decision.get("health_id") or ""))
            delivery = None
            delivery_metadata = None
            execution_record = None
            execution_metadata = None
            skipped = None
            if health is None:
                skipped = "recovery_escalation_retry_health_not_found"
            elif dry_run:
                skipped = "dry_run"
            else:
                event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_event(
                    health,
                    generated_by=str(generated_by),
                    max_alerts=int(payload.get("max_alerts", 20)),
                )
                delivery = deliver_connector_event(
                    event,
                    connector_config or {},
                    provider=str(decision.get("provider") or payload.get("provider", "webhook")),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        delivery,
                        source="go_backend_rollback_drill_acknowledgement_audit_recovery_escalation_retry_health_alert",
                    )
                    | {
                        "health_id": health.get("health_id"),
                        "plan_id": decision.get("plan_id", ""),
                        "retry_plan_id": run["retry_plan"].get("retry_plan_id"),
                        "worker_run_id": run.get("run_id"),
                    }
                )
            if not dry_run:
                execution_record = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record(
                    run,
                    decision,
                    health=health,
                    delivery=delivery,
                    delivery_metadata=delivery_metadata,
                    skipped=skipped,
                    executed_by=str(generated_by),
                )
                execution_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_execution_record_metadata(
                        execution_record
                    )
                )
            retry_results.append(
                {
                    "decision": decision,
                    "health": health,
                    "delivery": delivery,
                    "delivery_metadata": delivery_metadata,
                    "execution_record": execution_record,
                    "execution_metadata": execution_metadata,
                    "skipped": skipped,
                }
            )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_escalation_retry_health_alert_delivery_retry_worker_run_metadata(
                run
            )
        )
        return {
            "run": run,
            "metadata": metadata,
            "retry_metadata": retry_metadata,
            "retry_results": retry_results,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.get("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report(
        recovery_slo_minutes: int = 240,
        generated_by: str = "console",
    ) -> dict[str, object]:
        report = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report(
            _go_rollback_drill_notification_items(evidence_store),
            recovery_slo_minutes=recovery_slo_minutes,
            generated_by=generated_by,
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_metadata(report)
        )
        return {"report": report, "metadata": metadata}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-run"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_schedule_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        run = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run(
            _go_rollback_drill_notification_items(evidence_store),
            schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
            recovery_slo_minutes=int(payload.get("recovery_slo_minutes", 240)),
            generated_by=str(generated_by),
        )
        run_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run_metadata(
                run
            )
        )
        report = run.get("executive_report", {}) if isinstance(run.get("executive_report"), dict) else {}
        report_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_metadata(report)
        )
        return {
            "run": run,
            "metadata": run_metadata,
            "report_metadata": report_metadata,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/schedule-runs/{run_id}/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_deliver(
        run_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        items = _go_rollback_drill_notification_items(evidence_store)
        run_metadata = next(
            (
                item
                for item in items
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run"
                and item.get("run_id") == run_id
                and isinstance(item.get("recovery_executive_report_schedule_run"), dict)
            ),
            None,
        )
        run = run_metadata["recovery_executive_report_schedule_run"] if run_metadata else None
        if run is None and run_id == "latest":
            run = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run(
                items,
                schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
                recovery_slo_minutes=int(payload.get("recovery_slo_minutes", 240)),
                generated_by=str(generated_by),
            )
            run_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_schedule_run_metadata(
                    run
                )
            )
            report = run.get("executive_report", {}) if isinstance(run.get("executive_report"), dict) else {}
            evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_metadata(report)
            )
        if run is None:
            raise HTTPException(status_code=404, detail="recovery executive report schedule run not found")
        event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_event(
            run,
            generated_by=str(generated_by),
            max_risks=int(payload.get("max_risks", 10)),
        )
        result = deliver_connector_event(
            event,
            connector_config,
            provider=str(payload.get("provider") or "webhook"),
            retries=int(payload.get("retries", 2)),
            timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
        )
        report = run.get("executive_report", {}) if isinstance(run.get("executive_report"), dict) else {}
        metadata = evidence_store.upsert(
            build_connector_delivery_metadata(
                result,
                source="go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report",
            )
            | {
                "run_id": run.get("run_id"),
                "executive_report_id": report.get("executive_report_id", ""),
            }
        )
        return {
            "run": run,
            "delivery": result,
            "metadata": metadata,
            "run_metadata": run_metadata,
            "success": bool(result.get("success")),
            "event_id": run.get("run_id"),
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-plan"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan(
            _go_rollback_drill_notification_items(evidence_store),
            policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan_metadata(
                plan
            )
        )
        return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-worker-run"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        dry_run = bool(payload.get("dry_run", not bool(payload.get("execute", False))))
        if not dry_run and connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        items = _go_rollback_drill_notification_items(evidence_store)
        run = (
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run(
                items,
                retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
                schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
                generated_by=str(generated_by),
                dry_run=dry_run,
                max_retry_deliveries=int(payload.get("max_retry_deliveries", 5)),
            )
        )
        retry_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_plan_metadata(
                run["retry_plan"]
            )
        )
        schedule_runs = {
            str(item.get("run_id") or ""): item.get("recovery_executive_report_schedule_run")
            for item in items
            if item.get("metadata_kind")
            == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run"
            and isinstance(item.get("recovery_executive_report_schedule_run"), dict)
        }
        retry_results = []
        for decision in run.get("selected_retries", []):
            if not isinstance(decision, dict):
                continue
            schedule_run = schedule_runs.get(str(decision.get("run_id") or ""))
            delivery = None
            delivery_metadata = None
            execution_record = None
            execution_metadata = None
            skipped = None
            if schedule_run is None:
                skipped = "recovery_executive_report_schedule_run_not_found"
            elif dry_run:
                skipped = "dry_run"
            else:
                event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_event(
                    schedule_run,
                    generated_by=str(generated_by),
                    max_risks=int(payload.get("max_risks", 10)),
                )
                delivery = deliver_connector_event(
                    event,
                    connector_config or {},
                    provider=str(decision.get("provider") or payload.get("provider", "webhook")),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                report = (
                    schedule_run.get("executive_report", {})
                    if isinstance(schedule_run.get("executive_report"), dict)
                    else {}
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        delivery,
                        source="go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report",
                    )
                    | {
                        "run_id": schedule_run.get("run_id"),
                        "executive_report_id": report.get("executive_report_id", ""),
                        "retry_plan_id": run["retry_plan"].get("retry_plan_id"),
                        "worker_run_id": run.get("run_id"),
                    }
                )
            if not dry_run:
                execution_record = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record(
                    run,
                    decision,
                    schedule_run=schedule_run,
                    delivery=delivery,
                    delivery_metadata=delivery_metadata,
                    skipped=skipped,
                    executed_by=str(generated_by),
                )
                execution_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_execution_record_metadata(
                        execution_record
                    )
                )
            retry_results.append(
                {
                    "decision": decision,
                    "schedule_run": schedule_run,
                    "delivery": delivery,
                    "delivery_metadata": delivery_metadata,
                    "execution_record": execution_record,
                    "execution_metadata": execution_metadata,
                    "skipped": skipped,
                }
            )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_worker_run_metadata(
                run
            )
        )
        return {
            "run": run,
            "metadata": metadata,
            "retry_metadata": retry_metadata,
            "retry_results": retry_results,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health(
        expected_interval_minutes: int = 60,
        stale_metadata_minutes: int = 180,
        generated_by: str = "console",
    ) -> dict[str, object]:
        health = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health(
            _go_rollback_drill_notification_items(evidence_store),
            expected_interval_minutes=expected_interval_minutes,
            stale_metadata_minutes=stale_metadata_minutes,
            generated_by=generated_by,
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_metadata(
                health
            )
        )
        return {"health": health, "metadata": metadata}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_deliver(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            health = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health(
                _go_rollback_drill_notification_items(evidence_store),
                expected_interval_minutes=int(payload.get("expected_interval_minutes", 60)),
                stale_metadata_minutes=int(payload.get("stale_metadata_minutes", 180)),
                generated_by=str(generated_by),
            )
            existing_deliveries = _search_evidence_metadata(
                evidence_store,
                metadata_kind="release-connector-delivery",
                limit=500,
                offset=0,
            )["items"]
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan(
                health,
                delivery_items=existing_deliveries,
                requested_provider=payload.get("provider", "all"),
                available_providers=_configured_connector_providers(connector_config),
                generated_by=str(generated_by),
                suppression_window_minutes=int(payload.get("suppression_window_minutes", 60)),
                force=bool(payload.get("force", False)),
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_event(
                health,
                generated_by=str(generated_by),
                max_alerts=int(payload.get("max_alerts", 20)),
            )
            event["recovery_executive_report_delivery_retry_health_alert_plan"] = plan
            plan_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_plan_metadata(
                    plan
                )
            )
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert",
                    )
                    | {"health_id": plan.get("health_id"), "plan_id": plan.get("plan_id")}
                )
            return {
                "health": health,
                "plan": plan,
                "delivery": result,
                "plan_metadata": plan_metadata,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": plan.get("health_id"),
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/{health_id}/acknowledgements"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_acknowledge(
        health_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert(
                health_id,
                provider=payload["provider"],
                acknowledged_by=str(acknowledged_by),
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                plan_id=payload.get("plan_id"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_ack_metadata(
                    acknowledgement
                )
            )
            return {
                "acknowledgement": acknowledgement,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alerts(
        health_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        suppressed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_history(
            _go_rollback_drill_notification_items(evidence_store),
            health_id=health_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alert-dashboard"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_dashboard() -> dict[str, object]:
        return build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_dashboard(
            _go_rollback_drill_notification_items(evidence_store)
        )

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-plan"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_retry_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        plan = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan(
            _go_rollback_drill_notification_items(evidence_store),
            policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_metadata(
                plan
            )
        )
        return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/recovery-executive-report/delivery-retry-health-alerts/retry-worker-run"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_retry_worker_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        dry_run = bool(payload.get("dry_run", not bool(payload.get("execute", False))))
        if not dry_run and connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        items = _go_rollback_drill_notification_items(evidence_store)
        run = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run(
            items,
            retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
            generated_by=str(generated_by),
            dry_run=dry_run,
            max_retry_deliveries=int(payload.get("max_retry_deliveries", 5)),
        )
        retry_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_plan_metadata(
                run["retry_plan"]
            )
        )
        health_reports = {
            str(item.get("health_id") or ""): item.get("recovery_executive_report_delivery_retry_health")
            for item in items
            if item.get("metadata_kind")
            == "go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health"
            and isinstance(item.get("recovery_executive_report_delivery_retry_health"), dict)
        }
        retry_results = []
        for decision in run.get("selected_retries", []):
            if not isinstance(decision, dict):
                continue
            health = health_reports.get(str(decision.get("health_id") or ""))
            delivery = None
            delivery_metadata = None
            execution_record = None
            execution_metadata = None
            skipped = None
            if health is None:
                skipped = "recovery_executive_report_delivery_retry_health_not_found"
            elif dry_run:
                skipped = "dry_run"
            else:
                event = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_event(
                    health,
                    generated_by=str(generated_by),
                    max_alerts=int(payload.get("max_alerts", 20)),
                )
                delivery = deliver_connector_event(
                    event,
                    connector_config or {},
                    provider=str(decision.get("provider") or payload.get("provider", "webhook")),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        delivery,
                        source="go_backend_rollback_drill_acknowledgement_audit_recovery_executive_report_delivery_retry_health_alert",
                    )
                    | {
                        "health_id": health.get("health_id"),
                        "plan_id": decision.get("plan_id", ""),
                        "retry_plan_id": run["retry_plan"].get("retry_plan_id"),
                        "worker_run_id": run.get("run_id"),
                    }
                )
            if not dry_run:
                execution_record = build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record(
                    run,
                    decision,
                    health=health,
                    delivery=delivery,
                    delivery_metadata=delivery_metadata,
                    skipped=skipped,
                    executed_by=str(generated_by),
                )
                execution_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_execution_record_metadata(
                        execution_record
                    )
                )
            retry_results.append(
                {
                    "decision": decision,
                    "health": health,
                    "delivery": delivery,
                    "delivery_metadata": delivery_metadata,
                    "execution_record": execution_record,
                    "execution_metadata": execution_metadata,
                    "skipped": skipped,
                }
            )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_recovery_executive_report_delivery_retry_health_alert_delivery_retry_worker_run_metadata(
                run
            )
        )
        return {
            "run": run,
            "metadata": metadata,
            "retry_metadata": retry_metadata,
            "retry_results": retry_results,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closure-dashboard"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closure_dashboard() -> dict[str, object]:
        return build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closure_dashboard(
            _go_rollback_drill_notification_items(evidence_store)
        )

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_readiness(
        generated_by: str = "console",
        persist: bool = True,
    ) -> dict[str, object]:
        summary = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary(
            _go_rollback_drill_notification_items(evidence_store),
            generated_by=generated_by,
        )
        metadata = None
        if persist:
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary_metadata(
                    summary
                )
            )
        return {"summary": summary, "metadata": metadata}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-operator-runbook-export"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_operator_runbook_export(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        export = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export(
            _go_rollback_drill_notification_items(evidence_store),
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_operator_runbook_export_metadata(
                export
            )
        )
        readiness_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_summary_metadata(
                export["readiness_summary"]
            )
        )
        return {
            "export": export,
            "metadata": metadata,
            "readiness_metadata": readiness_metadata,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-readiness/{summary_id}/approval-decisions"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_readiness_approval_decide(
        summary_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        decided_by = actor_context.get("actor") if actor_context else payload.get("decided_by", payload.get("approved_by"))
        if not decided_by:
            raise HTTPException(status_code=400, detail="decided_by is required")
        items = _go_rollback_drill_notification_items(evidence_store)
        readiness_metadata = next(
            (
                item
                for item in items
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-readiness-summary"
                and item.get("summary_id") == summary_id
            ),
            None,
        )
        if readiness_metadata is None:
            raise HTTPException(status_code=404, detail="release readiness summary not found")
        readiness_summary = (
            readiness_metadata.get("final_reporting_release_readiness_summary")
            if isinstance(readiness_metadata.get("final_reporting_release_readiness_summary"), dict)
            else readiness_metadata
        )
        try:
            decision = (
                decide_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_approval(
                    readiness_summary,
                    decided_by=str(decided_by),
                    approval_state=payload.get("approval_state", "approved"),
                    external_ref=payload.get("external_ref"),
                    notes=payload.get("notes"),
                    override_blockers=bool(payload.get("override_blockers", False)),
                )
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_readiness_approval_metadata(
                    decision
                )
            )
            return {
                "decision": decision,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-record-attachment"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_record_attachment(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        attached_by = actor_context.get("actor") if actor_context else payload.get("attached_by", payload.get("decided_by"))
        if not attached_by:
            raise HTTPException(status_code=400, detail="attached_by is required")
        if not payload.get("release_record_ref"):
            raise HTTPException(status_code=400, detail="release_record_ref is required")
        items = _go_rollback_drill_notification_items(evidence_store)
        approval_decision_id = str(payload.get("approval_decision_id") or "")
        approval_metadata = next(
            (
                item
                for item in items
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-readiness-approval-decision"
                and (not approval_decision_id or item.get("decision_id") == approval_decision_id)
                and item.get("approval_state") == "approved"
            ),
            None,
        )
        if approval_metadata is None:
            raise HTTPException(status_code=404, detail="approved release readiness decision not found")
        approval_decision = (
            approval_metadata.get("final_reporting_release_readiness_approval_decision")
            if isinstance(approval_metadata.get("final_reporting_release_readiness_approval_decision"), dict)
            else approval_metadata
        )
        try:
            attachment = (
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_record_attachment(
                    items,
                    approval_decision,
                    release_record_ref=str(payload["release_record_ref"]),
                    attached_by=str(attached_by),
                    notes=payload.get("notes"),
                )
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_record_attachment_metadata(
                    attachment
                )
            )
            return {
                "attachment": attachment,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closure-packet-verification"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification(
        release_record_ref: Optional[str] = None,
        generated_by: str = "console",
        persist: bool = True,
    ) -> dict[str, object]:
        verification = (
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification(
                _go_rollback_drill_notification_items(evidence_store),
                release_record_ref=release_record_ref,
                generated_by=generated_by,
            )
        )
        metadata = None
        if persist:
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification_metadata(
                    verification
                )
            )
        return {"verification": verification, "metadata": metadata}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        export = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export(
            _go_rollback_drill_notification_items(evidence_store),
            release_record_ref=payload.get("release_record_ref"),
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_metadata(export)
        )
        verification_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification_metadata(
                export["verification"]
            )
        )
        return {
            "export": export,
            "metadata": metadata,
            "verification_metadata": verification_metadata,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export_deliver(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            export = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export(
                _go_rollback_drill_notification_items(evidence_store),
                release_record_ref=payload.get("release_record_ref"),
                generated_by=str(generated_by),
            )
            export_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_metadata(export)
            )
            verification_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closure_packet_verification_metadata(
                    export["verification"]
                )
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_event(
                export,
                generated_by=str(generated_by),
                max_markdown_chars=int(payload.get("max_markdown_chars", 12000)),
            )
            result = deliver_connector_event(
                event,
                connector_config,
                provider=str(payload.get("provider") or payload.get("delivery_provider") or "webhook"),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
            metadata = evidence_store.upsert(
                build_connector_delivery_metadata(
                    result,
                    source="go_backend_rollback_drill_acknowledgement_audit_final_reporting_auditor_export",
                )
                | {
                    "export_id": export.get("export_id"),
                    "verification_id": export.get("verification_id"),
                    "release_record_ref": export.get("release_record_ref"),
                }
            )
            return {
                "export": export,
                "event": event,
                "delivery": result,
                "metadata": metadata,
                "export_metadata": export_metadata,
                "verification_metadata": verification_metadata,
                "success": bool(result.get("success")),
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-immutable-archive-reference"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_immutable_archive_reference(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        archived_by = actor_context.get("actor") if actor_context else payload.get("archived_by", "console")
        try:
            export = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export(
                _go_rollback_drill_notification_items(evidence_store),
                release_record_ref=payload.get("release_record_ref"),
                generated_by=str(archived_by),
            )
            export_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_metadata(export)
            )
            reference = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_immutable_archive_reference(
                export,
                archive_ref=str(payload.get("archive_ref") or ""),
                archive_provider=str(payload.get("archive_provider") or "external_immutable_store"),
                archived_by=str(archived_by),
                retention_until=payload.get("retention_until"),
                legal_hold=bool(payload.get("legal_hold", False)),
                archive_hash=payload.get("archive_hash"),
                notes=payload.get("notes"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_immutable_archive_reference_metadata(
                    reference
                )
            )
            return {
                "reference": reference,
                "metadata": metadata,
                "export": export,
                "export_metadata": export_metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-plan"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        plan = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan(
            _go_rollback_drill_notification_items(evidence_store),
            policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan_metadata(
                plan
            )
        )
        return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-auditor-export/delivery-retry-worker-run"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_worker_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        dry_run = bool(payload.get("dry_run", not bool(payload.get("execute", False))))
        items = _go_rollback_drill_notification_items(evidence_store)
        run = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_worker_run(
            items,
            retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
            generated_by=str(generated_by),
            dry_run=dry_run,
            max_retry_deliveries=int(payload.get("max_retry_deliveries", 5)),
        )
        retry_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_plan_metadata(
                run["retry_plan"]
            )
        )
        exports = {
            str(item.get("export_id") or ""): item.get("final_reporting_auditor_export")
            for item in items
            if item.get("metadata_kind")
            == "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export"
            and isinstance(item.get("final_reporting_auditor_export"), dict)
        }
        retry_results = []
        for decision in run.get("selected_retries", []):
            if not isinstance(decision, dict):
                continue
            export = exports.get(str(decision.get("export_id") or ""))
            delivery = None
            delivery_metadata = None
            execution_record = None
            execution_metadata = None
            skipped = None
            if export is None:
                skipped = "auditor_export_not_found"
            elif dry_run:
                skipped = "dry_run"
            elif connector_config is None:
                skipped = "connector_config_not_configured"
            else:
                event = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_event(
                    export,
                    generated_by=str(generated_by),
                    max_markdown_chars=int(payload.get("max_markdown_chars", 12000)),
                )
                delivery = deliver_connector_event(
                    event,
                    connector_config,
                    provider=str(decision.get("provider") or payload.get("provider", "webhook")),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        delivery,
                        source="go_backend_rollback_drill_acknowledgement_audit_final_reporting_auditor_export",
                    )
                    | {
                        "export_id": export.get("export_id"),
                        "verification_id": export.get("verification_id"),
                        "release_record_ref": export.get("release_record_ref"),
                        "retry_plan_id": run["retry_plan"].get("retry_plan_id"),
                        "worker_run_id": run.get("run_id"),
                    }
                )
            if not dry_run:
                execution_record = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_execution_record(
                    run,
                    decision,
                    export=export,
                    delivery=delivery,
                    delivery_metadata=delivery_metadata,
                    skipped=skipped,
                    executed_by=str(generated_by),
                )
                execution_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_execution_record_metadata(
                        execution_record
                    )
                )
            retry_results.append(
                {
                    "decision": decision,
                    "delivery": delivery,
                    "delivery_metadata": delivery_metadata,
                    "execution_record": execution_record,
                    "execution_metadata": execution_metadata,
                    "skipped": skipped,
                }
            )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_auditor_export_delivery_retry_worker_run_metadata(
                run
            )
        )
        return {
            "run": run,
            "metadata": metadata,
            "retry_metadata": retry_metadata,
            "retry_results": retry_results,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health(
        generated_by: str = "console",
        require_archive_hash: bool = True,
        require_retention_until: bool = True,
        persist: bool = True,
    ) -> dict[str, object]:
        health = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health(
            _go_rollback_drill_notification_items(evidence_store),
            generated_by=generated_by,
            require_archive_hash=require_archive_hash,
            require_retention_until=require_retention_until,
        )
        metadata = (
            evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_metadata(
                    health
                )
            )
            if persist
            else build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_metadata(
                health
            )
        )
        return {"health": health, "metadata": metadata}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_deliver(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            health = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health(
                _go_rollback_drill_notification_items(evidence_store),
                generated_by=str(generated_by),
                require_archive_hash=bool(payload.get("require_archive_hash", True)),
                require_retention_until=bool(payload.get("require_retention_until", True)),
            )
            existing_deliveries = _search_evidence_metadata(
                evidence_store,
                metadata_kind="release-connector-delivery",
                limit=500,
                offset=0,
            )["items"]
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_plan(
                health,
                delivery_items=existing_deliveries,
                requested_provider=payload.get("provider", "all"),
                available_providers=_configured_connector_providers(connector_config),
                generated_by=str(generated_by),
                suppression_window_minutes=int(payload.get("suppression_window_minutes", 60)),
                force=bool(payload.get("force", False)),
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_event(
                health,
                generated_by=str(generated_by),
                max_alerts=int(payload.get("max_alerts", 20)),
            )
            event["final_reporting_archive_reference_health_alert_plan"] = plan
            plan_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_plan_metadata(
                    plan
                )
            )
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="go_backend_rollback_drill_acknowledgement_audit_final_reporting_archive_reference_health_alert",
                    )
                    | {"health_id": plan.get("health_id"), "plan_id": plan.get("plan_id")}
                )
            return {
                "health": health,
                "plan": plan,
                "delivery": result,
                "plan_metadata": plan_metadata,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": plan.get("health_id"),
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts/{health_id}/acknowledgements"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_acknowledge(
        health_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert(
                health_id,
                provider=payload["provider"],
                acknowledged_by=str(acknowledged_by),
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                plan_id=payload.get("plan_id"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_ack_metadata(
                    acknowledgement
                )
            )
            return {
                "acknowledgement": acknowledgement,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alerts"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alerts(
        health_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        suppressed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_history(
            _go_rollback_drill_notification_items(evidence_store),
            health_id=health_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-archive-reference-health-alert-dashboard"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_dashboard() -> dict[str, object]:
        return build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_archive_reference_health_alert_dashboard(
            _go_rollback_drill_notification_items(evidence_store)
        )

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-readiness-bundle"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_readiness_bundle(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        bundle = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_readiness_bundle(
            _go_rollback_drill_notification_items(evidence_store),
            release_record_ref=payload.get("release_record_ref"),
            generated_by=str(generated_by),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_readiness_bundle_metadata(bundle)
        )
        return {
            "bundle": bundle,
            "metadata": metadata,
            "actor": _public_actor_context(actor_context) if actor_context else None,
        }

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-signed-archive-manifest"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_signed_archive_manifest(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        signed_by = actor_context.get("actor") if actor_context else payload.get("signed_by", "console")
        bundle = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_readiness_bundle(
            _go_rollback_drill_notification_items(evidence_store),
            release_record_ref=payload.get("release_record_ref"),
            generated_by=str(signed_by),
        )
        bundle_metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_readiness_bundle_metadata(bundle)
        )
        try:
            manifest = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_signed_archive_manifest(
                bundle,
                signed_by=str(signed_by),
                signature=payload.get("signature"),
                signature_key_id=payload.get("signature_key_id"),
                signature_algorithm=str(
                    payload.get("signature_algorithm") or "external-kms-or-private-signing-service"
                ),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_signed_archive_manifest_metadata(
                    manifest
                )
            )
            return {
                "manifest": manifest,
                "metadata": metadata,
                "bundle": bundle,
                "bundle_metadata": bundle_metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_summary(
        release_record_ref: Optional[str] = None,
        generated_by: str = "console",
        persist: bool = True,
    ) -> dict[str, object]:
        summary = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary(
            _go_rollback_drill_notification_items(evidence_store),
            release_record_ref=release_record_ref,
            generated_by=generated_by,
        )
        metadata = (
            evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary_metadata(
                    summary
                )
            )
            if persist
            else build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary_metadata(
                summary
            )
        )
        return {"summary": summary, "metadata": metadata}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_deliver(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            summary = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary(
                _go_rollback_drill_notification_items(evidence_store),
                release_record_ref=payload.get("release_record_ref"),
                generated_by=str(generated_by),
            )
            summary_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary_metadata(
                    summary
                )
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_event(
                summary,
                generated_by=str(generated_by),
                max_summary_chars=int(payload.get("max_summary_chars", 12000)),
            )
            event_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_metadata(
                    event
                )
            )
            result = deliver_connector_event(
                event,
                connector_config,
                provider=str(payload.get("provider") or payload.get("delivery_provider") or "webhook"),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
            metadata = evidence_store.upsert(
                build_connector_delivery_metadata(
                    result,
                    source="go_backend_rollback_drill_acknowledgement_audit_final_reporting_release_closeout",
                )
                | {
                    "summary_id": summary.get("summary_id"),
                    "bundle_id": summary.get("bundle_id"),
                    "manifest_id": summary.get("manifest_id"),
                    "release_record_ref": summary.get("release_record_ref"),
                }
            )
            return {
                "summary": summary,
                "event": event,
                "delivery": result,
                "metadata": metadata,
                "event_metadata": event_metadata,
                "summary_metadata": summary_metadata,
                "success": bool(result.get("success")),
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-health"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_health(
        expiry_warning_days: int = 30,
        generated_by: str = "console",
        persist: bool = True,
    ) -> dict[str, object]:
        health = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health(
            _go_rollback_drill_notification_items(evidence_store),
            expiry_warning_days=expiry_warning_days,
            generated_by=generated_by,
        )
        metadata = (
            evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_metadata(
                    health
                )
            )
            if persist
            else build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_metadata(
                health
            )
        )
        return {"health": health, "metadata": metadata}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-health-alerts/deliver"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_deliver(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            health = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health(
                _go_rollback_drill_notification_items(evidence_store),
                expiry_warning_days=int(payload.get("expiry_warning_days", 30)),
                generated_by=str(generated_by),
            )
            health_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_metadata(
                    health
                )
            )
            provider = str(payload.get("provider") or payload.get("delivery_provider") or "webhook")
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_plan(
                health,
                provider=provider,
                generated_by=str(generated_by),
                force=bool(payload.get("force", False)),
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_event(
                plan,
                generated_by=str(generated_by),
            )
            event["final_reporting_closeout_retention_health_alert_plan"] = plan
            plan_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_health_alert_plan_metadata(
                    plan
                )
            )
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source=(
                            "go_backend_rollback_drill_acknowledgement_audit_final_reporting_"
                            "closeout_retention_health_alert"
                        ),
                    )
                    | {"health_id": plan.get("health_id"), "plan_id": plan.get("plan_id")}
                )
            return {
                "health": health,
                "health_metadata": health_metadata,
                "plan": plan,
                "plan_metadata": plan_metadata,
                "event": event,
                "delivery": result,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary/delivery-retry-plan"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_plan(
                _go_rollback_drill_notification_items(evidence_store),
                policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else payload,
                generated_by=str(generated_by),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_plan_metadata(
                    plan
                )
            )
            return {
                "plan": plan,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-release-closeout-summary/delivery-retry-worker-run"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_worker_run(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        execute = bool(payload.get("execute", False))
        dry_run = bool(payload.get("dry_run", not execute))
        if execute and connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        try:
            run = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_worker_run(
                _go_rollback_drill_notification_items(evidence_store),
                retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else payload,
                schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else payload,
                generated_by=str(generated_by),
                dry_run=dry_run,
                max_retry_deliveries=int(payload.get("max_retry_deliveries", 5)),
            )
            retry_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_plan_metadata(
                    run["retry_plan"]
                )
            )
            retry_results = []
            for decision in run.get("selected_retries", []):
                skipped = "dry_run" if dry_run else None
                summary = None
                event = None
                delivery = None
                delivery_metadata = None
                if not dry_run:
                    summary = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary(
                        _go_rollback_drill_notification_items(evidence_store),
                        release_record_ref=decision.get("release_record_ref") or payload.get("release_record_ref"),
                        generated_by=str(generated_by),
                    )
                    event = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_event(
                        summary,
                        generated_by=str(generated_by),
                        max_summary_chars=int(payload.get("max_summary_chars", 12000)),
                    )
                    delivery = deliver_connector_event(
                        event,
                        connector_config,
                        provider=str(decision.get("provider") or payload.get("provider") or "webhook"),
                        retries=int(payload.get("retries", 1)),
                        timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                    )
                    delivery_metadata = evidence_store.upsert(
                        build_connector_delivery_metadata(
                            delivery,
                            source="go_backend_rollback_drill_acknowledgement_audit_final_reporting_release_closeout",
                        )
                        | {
                            "summary_id": summary.get("summary_id"),
                            "bundle_id": summary.get("bundle_id"),
                            "manifest_id": summary.get("manifest_id"),
                            "release_record_ref": summary.get("release_record_ref"),
                        }
                    )
                execution_record = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_execution_record(
                    run,
                    decision,
                    summary=summary,
                    delivery=delivery,
                    delivery_metadata=delivery_metadata,
                    skipped=skipped,
                    executed_by=str(generated_by),
                )
                execution_metadata = evidence_store.upsert(
                    build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_execution_record_metadata(
                        execution_record
                    )
                )
                retry_results.append(
                    {
                        "decision": decision,
                        "event": event,
                        "delivery": delivery,
                        "delivery_metadata": delivery_metadata,
                        "execution_record": execution_record,
                        "execution_metadata": execution_metadata,
                        "skipped": skipped,
                    }
                )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_delivery_retry_worker_run_metadata(
                    run
                )
            )
            return {
                "run": run,
                "metadata": metadata,
                "retry_metadata": retry_metadata,
                "retry_results": retry_results,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-review"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_review(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        requested_by = actor_context.get("actor") if actor_context else payload.get("requested_by", "console")
        try:
            summary = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary(
                _go_rollback_drill_notification_items(evidence_store),
                release_record_ref=payload.get("release_record_ref"),
                generated_by=str(requested_by),
            )
            summary_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary_metadata(
                    summary
                )
            )
            request = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_request(
                summary,
                requested_by=str(requested_by),
                retention_until=payload.get("retention_until"),
                legal_hold=bool(payload.get("legal_hold", False)),
                review_reason=payload.get("review_reason"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_request_metadata(
                    request
                )
            )
            return {
                "request": request,
                "metadata": metadata,
                "summary": summary,
                "summary_metadata": summary_metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-retention-review/{review_id}/decisions"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_decision(
        review_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        decided_by = actor_context.get("actor") if actor_context else payload.get("decided_by", "console")
        items = _go_rollback_drill_notification_items(evidence_store)
        request_metadata = next(
            (
                item
                for item in sorted(items, key=lambda entry: str(entry.get("created_at", "")), reverse=True)
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-closeout-retention-review-request"
                and (review_id == "latest" or item.get("review_id") == review_id)
            ),
            None,
        )
        if request_metadata is None:
            raise HTTPException(status_code=404, detail="retention review request not found")
        request = (
            request_metadata.get("final_reporting_closeout_retention_review_request")
            if isinstance(request_metadata.get("final_reporting_closeout_retention_review_request"), dict)
            else request_metadata
        )
        try:
            decision = decide_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review(
                request,
                decision=str(payload.get("decision") or payload.get("decision_state") or "approved"),
                decided_by=str(decided_by),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_retention_review_decision_metadata(
                    decision
                )
            )
            return {
                "decision": decision,
                "metadata": metadata,
                "request": request,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/final-reporting-closeout-artifact-bundle"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_final_reporting_closeout_artifact_bundle(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        items = _go_rollback_drill_notification_items(evidence_store)
        sorted_items = sorted(items, key=lambda entry: str(entry.get("created_at", "")), reverse=True)
        readiness_metadata = next(
            (
                item
                for item in sorted_items
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-readiness-bundle"
                and (not payload.get("release_record_ref") or item.get("release_record_ref") == payload.get("release_record_ref"))
            ),
            {},
        )
        manifest_metadata = next(
            (
                item
                for item in sorted_items
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-signed-archive-manifest"
                and (not payload.get("release_record_ref") or item.get("release_record_ref") == payload.get("release_record_ref"))
            ),
            {},
        )
        retention_decision_metadata = next(
            (
                item
                for item in sorted_items
                if item.get("metadata_kind")
                == "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-closeout-retention-review-decision"
                and item.get("decision_state") == "approved"
                and (not payload.get("release_record_ref") or item.get("release_record_ref") == payload.get("release_record_ref"))
            ),
            {},
        )
        readiness_bundle = (
            readiness_metadata.get("final_reporting_readiness_bundle")
            if isinstance(readiness_metadata.get("final_reporting_readiness_bundle"), dict)
            else readiness_metadata
        )
        signed_manifest = (
            manifest_metadata.get("final_reporting_signed_archive_manifest")
            if isinstance(manifest_metadata.get("final_reporting_signed_archive_manifest"), dict)
            else manifest_metadata
        )
        retention_decision = (
            retention_decision_metadata.get("final_reporting_closeout_retention_review_decision")
            if isinstance(retention_decision_metadata.get("final_reporting_closeout_retention_review_decision"), dict)
            else retention_decision_metadata
        )
        try:
            summary = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary(
                items,
                release_record_ref=payload.get("release_record_ref"),
                generated_by=str(generated_by),
            )
            summary_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_release_closeout_summary_metadata(
                    summary
                )
            )
            artifact_bundle = build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_artifact_bundle(
                summary,
                readiness_bundle=readiness_bundle if readiness_bundle else None,
                signed_manifest=signed_manifest if signed_manifest else None,
                retention_decision=retention_decision if retention_decision else None,
                generated_by=str(generated_by),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_final_reporting_closeout_artifact_bundle_metadata(
                    artifact_bundle
                )
            )
            return {
                "artifact_bundle": artifact_bundle,
                "metadata": metadata,
                "summary": summary,
                "summary_metadata": summary_metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_health(
        expected_interval_minutes: int = 30,
        stale_metadata_minutes: int = 120,
    ) -> dict[str, object]:
        return build_go_rollback_drill_acknowledgement_audit_delivery_worker_health(
            _go_rollback_drill_notification_items(evidence_store),
            expected_interval_minutes=expected_interval_minutes,
            stale_metadata_minutes=stale_metadata_minutes,
        )

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/deliver")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_deliver(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            health = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health(
                _go_rollback_drill_notification_items(evidence_store),
                expected_interval_minutes=int(payload.get("expected_interval_minutes", 30)),
                stale_metadata_minutes=int(payload.get("stale_metadata_minutes", 120)),
            )
            existing_deliveries = _search_evidence_metadata(
                evidence_store,
                metadata_kind="release-connector-delivery",
                limit=500,
                offset=0,
            )["items"]
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan(
                health,
                delivery_items=existing_deliveries,
                requested_provider=payload.get("provider", "all"),
                available_providers=_configured_connector_providers(connector_config),
                generated_by=str(generated_by),
                suppression_window_minutes=int(payload.get("suppression_window_minutes", 60)),
                force=bool(payload.get("force", False)),
            )
            event = build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_event(
                health,
                generated_by=str(generated_by),
                max_alerts=int(payload.get("max_alerts", 20)),
            )
            event["worker_health_alert_plan"] = plan
            plan_metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_plan_metadata(plan)
            )
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="go_backend_rollback_drill_acknowledgement_audit_worker_health_alert",
                    )
                    | {"health_id": plan.get("health_id"), "plan_id": plan.get("plan_id")}
                )
            return {
                "health": health,
                "plan": plan,
                "delivery": result,
                "plan_metadata": plan_metadata,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": plan.get("health_id"),
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts/{health_id}/acknowledgements"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_acknowledge(
        health_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert(
                health_id,
                provider=payload["provider"],
                acknowledged_by=str(acknowledged_by),
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                plan_id=payload.get("plan_id"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_ack_metadata(
                    acknowledgement
                )
            )
            return {
                "acknowledgement": acknowledgement,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alerts")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alerts(
        health_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        suppressed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_history(
            _go_rollback_drill_notification_items(evidence_store),
            health_id=health_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )

    @app.get("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/worker-health-alert-dashboard")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_worker_health_alert_dashboard() -> dict[str, object]:
        return build_go_rollback_drill_acknowledgement_audit_delivery_worker_health_alert_dashboard(
            _go_rollback_drill_notification_items(evidence_store)
        )

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-plans/{retry_plan_id}/acknowledgements"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_retry_acknowledge(
        retry_plan_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        acknowledged_by = actor_context.get("actor") if actor_context else payload.get("acknowledged_by")
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not acknowledged_by:
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_go_rollback_drill_acknowledgement_audit_delivery_retry(
                retry_plan_id,
                provider=payload["provider"],
                acknowledged_by=str(acknowledged_by),
                acknowledgement_state=payload.get("acknowledgement_state", "accepted"),
                delivery_id=payload.get("delivery_id"),
                audit_id=payload.get("audit_id"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_retry_ack_metadata(acknowledgement)
            )
            return {
                "acknowledgement": acknowledgement,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plan")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_retry_execution_approval_plan(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        try:
            plan = build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan(
                _go_rollback_drill_notification_items(evidence_store),
                generated_by=str(generated_by),
                policy=payload.get("approval_policy") if isinstance(payload.get("approval_policy"), dict) else None,
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_plan_metadata(plan)
            )
            return {"plan": plan, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/retry-execution-approval-plans/{approval_plan_id}/decisions"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_retry_execution_approval_decide(
        approval_plan_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        decided_by = actor_context.get("actor") if actor_context else payload.get("decided_by", payload.get("approved_by"))
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not decided_by:
            raise HTTPException(status_code=400, detail="decided_by is required")
        try:
            decision = decide_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval(
                approval_plan_id,
                provider=payload["provider"],
                decided_by=str(decided_by),
                approval_state=payload.get("approval_state", "approved"),
                retry_plan_id=payload.get("retry_plan_id"),
                delivery_id=payload.get("delivery_id"),
                audit_id=payload.get("audit_id"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_retry_execution_approval_decision_metadata(
                    decision
                )
            )
            return {
                "decision": decision,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbook")
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_connector_recovery_playbook(
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        generated_by = actor_context.get("actor") if actor_context else payload.get("generated_by", "console")
        playbook = build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook(
            _go_rollback_drill_notification_items(evidence_store),
            generated_by=str(generated_by),
            min_failure_count=int(payload.get("min_failure_count", 2)),
            lookback_hours=int(payload.get("lookback_hours", 24)),
        )
        metadata = evidence_store.upsert(
            build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_playbook_metadata(playbook)
        )
        return {"playbook": playbook, "metadata": metadata, "actor": _public_actor_context(actor_context) if actor_context else None}

    @app.post(
        "/runtime/go-pilot/rollback-drill-notifications/acknowledgements/audit-delivery/connector-recovery-playbooks/{playbook_id}/closures"
    )
    def runtime_go_pilot_rollback_drill_notification_acknowledgement_audit_delivery_connector_recovery_close(
        playbook_id: str,
        payload: dict,
        authorization: Optional[str] = Header(default=None),
    ) -> dict[str, object]:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        closed_by = actor_context.get("actor") if actor_context else payload.get("closed_by")
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not closed_by:
            raise HTTPException(status_code=400, detail="closed_by is required")
        try:
            closure = close_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery(
                playbook_id,
                provider=payload["provider"],
                closed_by=str(closed_by),
                closure_state=payload.get("closure_state", "resolved"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                verification_refs=payload.get("verification_refs")
                if isinstance(payload.get("verification_refs"), list)
                else None,
            )
            metadata = evidence_store.upsert(
                build_go_rollback_drill_acknowledgement_audit_delivery_connector_recovery_closure_metadata(
                    closure
                )
            )
            return {
                "closure": closure,
                "metadata": metadata,
                "actor": _public_actor_context(actor_context) if actor_context else None,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/runtime/go-pilot/rollback-drill-notifications")
    def runtime_go_pilot_rollback_drill_notification_history(
        schedule_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        connector_delivery_source: Optional[str] = None,
        delivery_success: Optional[bool] = None,
        alert_level: Optional[str] = None,
        audit_id: Optional[str] = None,
        delivery_id: Optional[str] = None,
        cadence: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_notification_history(
            _go_rollback_drill_notification_items(evidence_store),
            schedule_id=schedule_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            connector_delivery_source=connector_delivery_source,
            delivery_success=delivery_success,
            alert_level=alert_level,
            audit_id=audit_id,
            delivery_id=delivery_id,
            cadence=cadence,
            limit=limit,
            offset=offset,
        )

    @app.get("/runtime/go-pilot/rollback-drill-notifications/dashboard")
    def runtime_go_pilot_rollback_drill_notification_dashboard() -> dict[str, object]:
        return build_go_rollback_drill_notification_dashboard(
            _go_rollback_drill_notification_items(evidence_store)
        )

    @app.get("/runtime/go-pilot/rollback-drill-notifications/routes")
    def runtime_go_pilot_rollback_drill_notification_routes(
        schedule_id: Optional[str] = None,
        provider: Optional[str] = None,
        owner: Optional[str] = None,
        action: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_routing_history(
            _go_rollback_drill_notification_items(evidence_store),
            schedule_id=schedule_id,
            provider=provider,
            owner=owner,
            action=action,
            category=category,
            limit=limit,
            offset=offset,
        )

    @app.get("/runtime/go-pilot/rollback-drill-notifications/suppression-trends")
    def runtime_go_pilot_rollback_drill_notification_suppression_trends(
        schedule_id: Optional[str] = None,
        provider: Optional[str] = None,
        owner: Optional[str] = None,
        generated_by: str = "console",
    ) -> dict[str, object]:
        trend = build_go_rollback_drill_routing_suppression_trend(
            _go_rollback_drill_notification_items(evidence_store),
            schedule_id=schedule_id,
            provider=provider,
            owner=owner,
            generated_by=generated_by,
        )
        metadata = evidence_store.upsert(build_go_rollback_drill_routing_suppression_trend_metadata(trend))
        return {"trend": trend, "metadata": metadata}

    @app.post("/runtime/go-pilot/rollback-drill-notifications/escalation-plan")
    def runtime_go_pilot_rollback_drill_notification_escalation_plan(payload: dict) -> dict[str, object]:
        plan = build_go_rollback_drill_notification_escalation_plan(
            _go_rollback_drill_notification_items(evidence_store),
            policy=payload.get("policy") if isinstance(payload.get("policy"), dict) else None,
            generated_by=payload.get("generated_by", "console"),
        )
        metadata = evidence_store.upsert(build_go_rollback_drill_notification_escalation_plan_metadata(plan))
        return {"plan": plan, "metadata": metadata}

    @app.post("/runtime/go-pilot/evaluate")
    def runtime_go_pilot_evaluate(payload: dict) -> dict[str, object]:
        return evaluate_with_go_pilot(payload)

    @app.get("/repositories")
    def repository_index(
        provider: Optional[str] = None,
        owner: Optional[str] = None,
        policy_pack: Optional[str] = None,
        status: Optional[str] = None,
        risk_tier: Optional[str] = None,
    ) -> dict:
        return inventory_store.list_repositories(
            provider=provider,
            owner=owner,
            policy_pack=policy_pack,
            status=status,
            risk_tier=risk_tier,
        )

    @app.post("/repositories")
    def upsert_repository(payload: dict) -> dict:
        try:
            return inventory_store.upsert_repository(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid repository record") from exc

    @app.get("/repositories/{repository_id:path}")
    def repository_item(repository_id: str) -> dict:
        item = inventory_store.get_repository(repository_id)
        if item is None:
            raise HTTPException(status_code=404, detail="repository not found")
        return item

    @app.get("/policy-rollouts")
    def policy_rollout_index(
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        state: Optional[str] = None,
        mode: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> dict:
        return inventory_store.list_policy_rollouts(
            repository=repository,
            policy_pack=policy_pack,
            state=state,
            mode=mode,
            owner=owner,
        )

    @app.post("/policy-rollouts")
    def upsert_policy_rollout(payload: dict) -> dict:
        try:
            return inventory_store.upsert_policy_rollout(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid policy rollout record") from exc

    @app.post("/policy-rollouts/change-plan")
    def policy_rollout_change_plan(payload: dict) -> dict:
        current = inventory_store.get_policy_rollout(str(payload.get("rollout_id", ""))) if payload.get("rollout_id") else None
        requested = payload.get("changes") if isinstance(payload.get("changes"), dict) else payload
        try:
            return build_rollout_change_plan(current, requested)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/policy-rollouts/apply-change")
    def policy_rollout_apply_change(payload: dict, authorization: Optional[str] = Header(default=None)) -> dict:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        current = inventory_store.get_policy_rollout(str(payload.get("rollout_id", ""))) if payload.get("rollout_id") else None
        requested = payload.get("changes") if isinstance(payload.get("changes"), dict) else payload
        try:
            plan = build_rollout_change_plan(current, requested)
            rollout = inventory_store.upsert_policy_rollout(plan["after"])
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "schema_version": "cavra.policy_rollout.change_result.v1",
            "product": "CAVRA",
            "actor": _public_actor_context(actor_context) if actor_context else None,
            "plan": plan,
            "rollout": rollout,
        }

    @app.get("/policy-rollout-details/{rollout_id:path}")
    @app.get("/policy-rollouts/{rollout_id}/detail")
    def policy_rollout_detail(rollout_id: str) -> dict:
        rollout = inventory_store.get_policy_rollout(rollout_id)
        if rollout is None:
            raise HTTPException(status_code=404, detail="policy rollout not found")
        return _policy_rollout_detail(rollout, inventory_store, activity_store, integration_store)

    @app.get("/policy-rollouts/{rollout_id:path}")
    def policy_rollout_item(rollout_id: str) -> dict:
        item = inventory_store.get_policy_rollout(rollout_id)
        if item is None:
            raise HTTPException(status_code=404, detail="policy rollout not found")
        return item

    @app.get("/agents")
    def agents(status: Optional[str] = None, owner: Optional[str] = None) -> dict:
        return registry_store.list_agents(status=status, owner=owner)

    @app.get("/agents/profiles")
    def agent_profiles() -> dict:
        return default_agent_profiles()

    @app.get("/agents/enforcement-readiness")
    def agent_enforcement_readiness() -> dict[str, object]:
        return agent_enforcement_readiness_report(repo_root=Path.cwd())

    @app.post("/agents")
    def upsert_agent(payload: dict) -> dict:
        try:
            return registry_store.upsert_agent(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid agent record") from exc

    @app.get("/agents/{agent_id}")
    def agent(agent_id: str) -> dict:
        item = registry_store.get_agent(agent_id)
        if item is None:
            raise HTTPException(status_code=404, detail="agent not found")
        return item

    @app.get("/mcp/servers")
    def mcp_servers(
        trust_tier: Optional[str] = None,
        approval_state: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> dict:
        return registry_store.list_mcp_servers(trust_tier=trust_tier, approval_state=approval_state, capability=capability)

    @app.get("/mcp/tool-classifications")
    def mcp_tool_classifications(capability: Optional[str] = None) -> dict:
        if capability:
            item = classify_mcp_capability(capability)
            if item is None:
                raise HTTPException(status_code=404, detail="MCP capability classification not found")
            return item
        return default_mcp_tool_classifications()

    @app.post("/mcp/servers")
    def upsert_mcp_server(payload: dict) -> dict:
        try:
            return registry_store.upsert_mcp_server(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid MCP server record") from exc

    @app.get("/mcp/servers/{server_id}")
    def mcp_server(server_id: str) -> dict:
        item = registry_store.get_mcp_server(server_id)
        if item is None:
            raise HTTPException(status_code=404, detail="MCP server not found")
        return item

    @app.get("/mcp/trust")
    def mcp_trust(server: str, tool: str = "unknown", capability: Optional[str] = None) -> dict:
        return registry_store.evaluate_mcp(server, tool, capability)

    @app.get("/integrations")
    def integration_index(
        provider: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        owner: Optional[str] = None,
        environment: Optional[str] = None,
        health_status: Optional[str] = None,
    ) -> dict:
        return integration_store.list_integrations(
            provider=provider,
            category=category,
            status=status,
            owner=owner,
            environment=environment,
            health_status=health_status,
        )

    @app.post("/integrations")
    def upsert_integration(payload: dict) -> dict:
        try:
            return integration_store.upsert_integration(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid integration record") from exc

    @app.get("/integrations/{integration_id}")
    def integration_item(integration_id: str) -> dict:
        item = integration_store.get_integration(integration_id)
        if item is None:
            raise HTTPException(status_code=404, detail="integration not found")
        return item

    @app.post("/integrations/{integration_id}/deliver")
    def deliver_integration(integration_id: str, payload: dict) -> dict:
        item = integration_store.get_integration(integration_id)
        if item is None:
            raise HTTPException(status_code=404, detail="integration not found")
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        event = payload.get("event") if isinstance(payload.get("event"), dict) else payload
        event = {
            "event_type": "cavra.integration.delivery",
            "product": "CAVRA",
            "integration_id": item.get("integration_id"),
            "integration_provider": item.get("provider"),
            "integration_category": item.get("category"),
            **event,
        }
        try:
            return deliver_connector_event(
                event,
                connector_config,
                provider=payload.get("provider", item.get("provider", "all")),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/pilot-intakes")
    def pilot_intake_index(
        overall_status: Optional[str] = None,
        repository: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return pilot_intake_store.list(
            overall_status=overall_status,
            repository=repository,
            limit=limit,
            offset=offset,
        )

    @app.post("/pilot-intakes")
    def upsert_pilot_intake(payload: dict) -> dict:
        try:
            return pilot_intake_store.upsert(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/pilot-intakes/{intake_id}")
    def pilot_intake_item(intake_id: str) -> dict:
        item = pilot_intake_store.get(intake_id)
        if item is None:
            raise HTTPException(status_code=404, detail="pilot intake not found")
        return item

    @app.get("/pilot-intakes/{intake_id}/readiness")
    def pilot_intake_readiness(intake_id: str) -> dict:
        item = pilot_intake_store.get(intake_id)
        if item is None:
            raise HTTPException(status_code=404, detail="pilot intake not found")
        return item["readiness"]

    @app.post("/pilot-intakes/{intake_id}/private-handoff-plan")
    def pilot_intake_private_handoff_plan(intake_id: str, payload: dict) -> dict:
        item = pilot_intake_store.get(intake_id)
        if item is None:
            raise HTTPException(status_code=404, detail="pilot intake not found")
        try:
            return build_private_persistence_handoff_plan(
                item,
                tenant_id=payload.get("tenant_id", ""),
                providers=payload.get("providers"),
                requested_by=payload.get("requested_by", "console"),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/risk/events")
    @app.get("/compliance/mappings")
    def empty_collection() -> list[dict]:
        return []

    @app.get("/approvals")
    def approvals(
        state: Optional[str] = None,
        approver_group: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return approval_store.list(state=state, approver_group=approver_group, limit=limit, offset=offset)

    @app.post("/approvals")
    def create_approval(payload: dict) -> dict:
        decision = payload["decision"] if isinstance(payload.get("decision"), dict) else payload
        try:
            return approval_store.create_request(
                decision,
                approver_group=payload.get("approver_group"),
                requested_by=payload.get("requested_by", "ai-agent"),
                ttl_hours=int(payload.get("ttl_hours", 24)),
                routing_rules=routing_rules,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/approvals/break-glass")
    def break_glass(payload: dict, authorization: Optional[str] = Header(default=None)) -> dict:
        actor_context = _console_mutation_actor_context(
            payload,
            authorization=authorization,
            oidc_config=oidc_config,
            rbac_rules=rbac_rules,
        )
        decision = payload["decision"] if isinstance(payload.get("decision"), dict) else payload
        if actor_context:
            synthetic_approval = {
                "state": "pending",
                "break_glass": True,
                "approver_group": payload.get("approver_group", "Change Advisory Board"),
                "decision": decision,
            }
            if not actor_can_decide(actor_context, synthetic_approval, action="approved", rbac_rules=rbac_rules):
                raise HTTPException(status_code=403, detail="actor is not authorized for break-glass")
        try:
            return approval_store.break_glass(
                decision=decision,
                actor=actor_context.get("actor") if actor_context else payload.get("actor", ""),
                reason=payload.get("reason", ""),
                approver_group=payload.get("approver_group", "Change Advisory Board"),
                external_ref=payload.get("external_ref"),
                ttl_hours=int(payload.get("ttl_hours", 4)),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/approvals/{approval_id}")
    def approval(approval_id: str) -> dict:
        item = approval_store.get(approval_id)
        if item is None:
            raise HTTPException(status_code=404, detail="approval not found")
        return item

    @app.post("/approvals/{approval_id}/approve")
    def approve(approval_id: str, payload: dict, authorization: Optional[str] = Header(default=None)) -> dict:
        return _decide_approval(
            approval_store,
            approval_id,
            state="approved",
            payload=payload,
            rbac_rules=rbac_rules,
            oidc_config=oidc_config,
            authorization=authorization,
        )

    @app.post("/approvals/{approval_id}/deny")
    def deny(approval_id: str, payload: dict, authorization: Optional[str] = Header(default=None)) -> dict:
        return _decide_approval(
            approval_store,
            approval_id,
            state="denied",
            payload=payload,
            rbac_rules=rbac_rules,
            oidc_config=oidc_config,
            authorization=authorization,
        )

    @app.post("/approvals/{approval_id}/expire")
    def expire(approval_id: str, payload: Optional[dict] = None, authorization: Optional[str] = Header(default=None)) -> dict:
        return _decide_approval(
            approval_store,
            approval_id,
            state="expired",
            payload=payload or {"actor": "system", "reason": "approval expired"},
            rbac_rules=rbac_rules,
            oidc_config=oidc_config,
            authorization=authorization,
        )

    @app.post("/approvals/{approval_id}/deliver")
    def deliver_approval(approval_id: str, payload: Optional[dict] = None) -> dict:
        item = approval_store.get(approval_id)
        if item is None:
            raise HTTPException(status_code=404, detail="approval not found")
        if provider_config is None:
            raise HTTPException(status_code=400, detail="approval provider config is not configured")
        payload = payload or {}
        try:
            return deliver_provider_requests(
                item,
                provider_config,
                provider=payload.get("provider", "all"),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/approvals/{approval_id}/attach-decision")
    def attach_decision_approval(approval_id: str, payload: dict) -> dict:
        item = approval_store.get(approval_id)
        if item is None:
            raise HTTPException(status_code=404, detail="approval not found")
        try:
            return attach_approval_to_decision(payload, item)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/evidence")
    def evidence_index(
        session_id: Optional[str] = None,
        signer: Optional[str] = None,
        min_blocked: Optional[int] = None,
        has_approvals: Optional[bool] = None,
        metadata_kind: Optional[str] = None,
        rollout_status: Optional[str] = None,
        environment: Optional[str] = None,
        deployment_target: Optional[str] = None,
        target_ring: Optional[str] = None,
        approval_state: Optional[str] = None,
        promotion_execution_status: Optional[str] = None,
        rollback_execution_status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ):
        if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
            return evidence_store.search(
                session_id=session_id,
                signer=signer,
                min_blocked=min_blocked,
                has_approvals=has_approvals,
                metadata_kind=metadata_kind,
                rollout_status=rollout_status,
                environment=environment,
                deployment_target=deployment_target,
                target_ring=target_ring,
                approval_state=approval_state,
                promotion_execution_status=promotion_execution_status,
                rollback_execution_status=rollback_execution_status,
                limit=limit,
                offset=offset,
            )
        return _filter_json_evidence(
            evidence_store.list(),
            session_id=session_id,
            signer=signer,
            min_blocked=min_blocked,
            has_approvals=has_approvals,
            metadata_kind=metadata_kind,
            rollout_status=rollout_status,
            environment=environment,
            deployment_target=deployment_target,
            target_ring=target_ring,
            approval_state=approval_state,
            promotion_execution_status=promotion_execution_status,
            rollback_execution_status=rollback_execution_status,
            limit=limit,
            offset=offset,
        )

    @app.get("/promotion-executions")
    def promotion_execution_index(
        rollout_id: Optional[str] = None,
        target_ring: Optional[str] = None,
        approval_state: Optional[str] = None,
        deployment_target: Optional[str] = None,
        promotion_execution_status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="rollout-promotion-execution",
            deployment_target=deployment_target,
            target_ring=target_ring,
            approval_state=approval_state,
            promotion_execution_status=promotion_execution_status,
            limit=500,
            offset=0,
        )
        items = result["items"]
        if rollout_id:
            items = [item for item in items if item.get("rollout_id") == rollout_id]
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        return {"items": items[offset : offset + limit], "total": len(items), "limit": limit, "offset": offset}

    @app.get("/promotion-executions/{execution_id}")
    def promotion_execution_detail(execution_id: str) -> dict:
        item = evidence_store.get(execution_id)
        if item is None or item.get("metadata_kind") != "rollout-promotion-execution":
            raise HTTPException(status_code=404, detail="promotion execution not found")
        return item

    @app.get("/promotion-executions/{execution_id}/audit-export")
    def promotion_execution_audit_export(execution_id: str) -> dict:
        item = evidence_store.get(execution_id)
        if item is None or item.get("metadata_kind") != "rollout-promotion-execution":
            raise HTTPException(status_code=404, detail="promotion execution not found")
        execution = item.get("execution")
        if not isinstance(execution, dict):
            raise HTTPException(status_code=400, detail="promotion execution metadata is missing execution payload")
        return {
            "schema_version": "cavra.rollout-promotion.audit-export.v1",
            "event": build_rollout_promotion_execution_audit_event(execution),
        }

    @app.post("/promotion-executions/{execution_id}/audit-export/deliver")
    def promotion_execution_audit_deliver(execution_id: str, payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        item = evidence_store.get(execution_id)
        if item is None or item.get("metadata_kind") != "rollout-promotion-execution":
            raise HTTPException(status_code=404, detail="promotion execution not found")
        execution = item.get("execution")
        if not isinstance(execution, dict):
            raise HTTPException(status_code=400, detail="promotion execution metadata is missing execution payload")
        try:
            result = deliver_connector_event(
                build_rollout_promotion_execution_audit_event(execution),
                connector_config,
                provider=payload.get("provider", "all"),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
            metadata = evidence_store.upsert(
                build_connector_delivery_metadata(result, source="release_governance_promotion")
            )
            return result | {"metadata": metadata}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/promotion-executions/{execution_id}/rollback-execution")
    def promotion_execution_rollback(execution_id: str, payload: dict) -> dict:
        item = evidence_store.get(execution_id)
        if item is None or item.get("metadata_kind") != "rollout-promotion-execution":
            raise HTTPException(status_code=404, detail="promotion execution not found")
        execution = item.get("execution")
        if not isinstance(execution, dict):
            raise HTTPException(status_code=400, detail="promotion execution metadata is missing execution payload")
        approval_id = payload.get("approval_id")
        if not approval_id:
            raise HTTPException(status_code=400, detail="rollback execution requires approval_id")
        approval = approval_store.get(str(approval_id))
        if approval is None:
            raise HTTPException(status_code=404, detail="approval not found")
        result = create_managed_endpoint_rollout_rollback_execution(
            execution,
            approval,
            output_dir=None,
            executed_by=payload.get("executed_by", "console"),
            rollback_reason=payload.get("rollback_reason", "Rollback approved from promotion execution audit."),
            execution_environment=payload.get("execution_environment"),
            notes=payload.get("notes"),
        )
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = None
        if result.rollback:
            metadata = evidence_store.upsert(build_managed_endpoint_rollout_rollback_execution_metadata(result.rollback))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/rollback-executions/{rollback_id}")
    def rollback_execution_detail(rollback_id: str) -> dict:
        item = evidence_store.get(rollback_id)
        if item is None or item.get("metadata_kind") != "rollout-rollback-execution":
            raise HTTPException(status_code=404, detail="rollback execution not found")
        return item

    @app.post("/rollback-executions/{rollback_id}/deliver")
    def rollback_execution_deliver(rollback_id: str, payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        item = evidence_store.get(rollback_id)
        if item is None or item.get("metadata_kind") != "rollout-rollback-execution":
            raise HTTPException(status_code=404, detail="rollback execution not found")
        rollback = item.get("rollback")
        if not isinstance(rollback, dict):
            raise HTTPException(status_code=400, detail="rollback execution metadata is missing rollback payload")
        try:
            result = deliver_connector_event(
                build_rollout_rollback_execution_audit_event(rollback),
                connector_config,
                provider=payload.get("provider", "all"),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
            metadata = evidence_store.upsert(
                build_connector_delivery_metadata(result, source="release_governance_rollback")
            )
            return result | {"metadata": metadata}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/release-connector-deliveries")
    def release_connector_delivery_index(
        provider: Optional[str] = None,
        event_type: Optional[str] = None,
        event_id: Optional[str] = None,
        success: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="release-connector-delivery",
            limit=500,
            offset=0,
        )
        return filter_connector_delivery_history(
            result["items"],
            provider=provider,
            event_type=event_type,
            event_id=event_id,
            success=success,
            limit=limit,
            offset=offset,
        )

    @app.get("/release-connector-deliveries/dashboard")
    def release_connector_delivery_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="release-connector-delivery",
            limit=500,
            offset=0,
        )
        return build_connector_delivery_dashboard(result["items"])

    @app.get("/release-channel-promotions")
    def release_channel_promotion_index(
        channel: Optional[str] = None,
        target_ring: Optional[str] = None,
        approval_state: Optional[str] = None,
        approval_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="release-channel-promotion-request",
            target_ring=target_ring,
            approval_state=approval_state,
            limit=500,
            offset=0,
        )
        items = result["items"]
        if channel:
            items = [item for item in items if item.get("channel") == channel]
        if approval_id:
            items = [item for item in items if item.get("approval_id") == approval_id]
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        return {"items": items[offset : offset + limit], "total": len(items), "limit": limit, "offset": offset}

    @app.get("/release-channel-promotions/{request_id}")
    def release_channel_promotion_detail(request_id: str) -> dict:
        item = evidence_store.get(request_id)
        if item is None or item.get("metadata_kind") != "release-channel-promotion-request":
            raise HTTPException(status_code=404, detail="release channel promotion request not found")
        return item

    @app.get("/endpoint-management-exports")
    def endpoint_management_export_index(
        channel: Optional[str] = None,
        provider: Optional[str] = None,
        approval_id: Optional[str] = None,
        request_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-management-export",
            limit=500,
            offset=0,
        )
        items = result["items"]
        if channel:
            items = [item for item in items if item.get("channel") == channel]
        if provider:
            items = [item for item in items if provider in (item.get("providers", []) or [])]
        if approval_id:
            items = [item for item in items if item.get("approval_id") == approval_id]
        if request_id:
            items = [item for item in items if item.get("request_id") == request_id]
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        return {"items": items[offset : offset + limit], "total": len(items), "limit": limit, "offset": offset}

    @app.get("/endpoint-management-exports/dashboard")
    def endpoint_management_export_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-management-export",
            limit=500,
            offset=0,
        )
        return build_endpoint_management_export_dashboard(result["items"])

    @app.get("/endpoint-management-exports/{export_id}")
    def endpoint_management_export_detail(export_id: str) -> dict:
        item = evidence_store.get(export_id)
        if item is None or item.get("metadata_kind") != "endpoint-management-export":
            raise HTTPException(status_code=404, detail="endpoint management export not found")
        return item

    @app.get("/endpoint-management-exports/{export_id}/artifacts")
    def endpoint_management_export_artifact_index(export_id: str) -> dict:
        metadata = _get_endpoint_management_export_or_404(evidence_store, export_id)
        root = _configured_artifact_root(evidence_artifact_root)
        encoded_export_id = quote(export_id, safe="")
        try:
            return list_evidence_artifacts(
                root,
                export_id,
                metadata=metadata,
                base_path=f"/endpoint-management-exports/{encoded_export_id}/artifacts",
                bundle_path=f"/endpoint-management-exports/{encoded_export_id}/artifact-bundle",
            )
        except EvidenceArtifactError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/endpoint-management-exports/{export_id}/artifact-bundle")
    def endpoint_management_export_artifact_bundle(export_id: str):
        metadata = _get_endpoint_management_export_or_404(evidence_store, export_id)
        root = _configured_artifact_root(evidence_artifact_root)
        try:
            artifact_metadata, payload = build_evidence_artifact_archive(root, export_id, metadata=metadata)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="endpoint management export artifacts not found") from exc
        except EvidenceArtifactError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return Response(
            payload,
            media_type=artifact_metadata["media_type"],
            headers={
                "content-disposition": f'attachment; filename="{artifact_metadata["artifact"]}"',
                "x-cavra-artifact-sha256": str(artifact_metadata["sha256"]),
                "x-cavra-artifact-count": str(artifact_metadata["artifact_count"]),
            },
        )

    @app.get("/endpoint-management-exports/{export_id}/artifacts/{artifact_name}")
    def endpoint_management_export_artifact(export_id: str, artifact_name: str):
        metadata = _get_endpoint_management_export_or_404(evidence_store, export_id)
        root = _configured_artifact_root(evidence_artifact_root)
        try:
            artifact_metadata, payload = load_evidence_artifact(root, export_id, artifact_name, metadata=metadata)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="endpoint management export artifact not found") from exc
        except EvidenceArtifactError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return Response(
            payload,
            media_type=artifact_metadata["media_type"],
            headers={
                "content-disposition": f'attachment; filename="{artifact_metadata["artifact"]}"',
                "x-cavra-artifact-sha256": str(artifact_metadata["sha256"]),
                "x-cavra-artifact-kind": str(artifact_metadata["kind"]),
            },
        )

    @app.post("/endpoint-management-exports/{export_id}/publish")
    def endpoint_management_export_publish(export_id: str, payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        metadata = _get_endpoint_management_export_or_404(evidence_store, export_id)
        manifest = metadata.get("manifest")
        if not isinstance(manifest, dict):
            raise HTTPException(status_code=400, detail="endpoint management export metadata is missing manifest payload")
        export_dir = None
        if metadata.get("bundle_dir"):
            root = _configured_artifact_root(evidence_artifact_root)
            export_dir = _resolve_under_artifact_root(root, metadata.get("bundle_dir"), "endpoint management export directory")
        try:
            event_result = build_endpoint_management_publication_event(
                manifest,
                export_dir=export_dir,
                export_id=export_id,
                provider=payload.get("provider", "all"),
                requested_by=payload.get("requested_by", "console"),
            )
            if not event_result.valid or event_result.event is None:
                raise ValueError("; ".join(event_result.errors) or "endpoint management publication event is invalid")
            result = deliver_connector_event(
                event_result.event,
                connector_config,
                provider=payload.get("provider", "all"),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
            publication_metadata = evidence_store.upsert(
                build_endpoint_management_publication_metadata(result, event_result.event)
            )
            return event_result.to_dict() | {"delivery": result, "metadata": publication_metadata}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/endpoint-management-publications")
    def endpoint_management_publication_index(
        provider: Optional[str] = None,
        export_id: Optional[str] = None,
        channel: Optional[str] = None,
        success: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-management-publication-delivery",
            limit=500,
            offset=0,
        )
        return filter_endpoint_management_publication_history(
            result["items"],
            provider=provider,
            export_id=export_id,
            channel=channel,
            success=success,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-management-publications/dashboard")
    def endpoint_management_publication_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-management-publication-delivery",
            limit=500,
            offset=0,
        )
        return build_endpoint_management_publication_dashboard(result["items"])

    @app.post("/endpoint-inventory/ingest")
    def endpoint_inventory_ingest(payload: dict) -> dict:
        provider = payload.get("provider")
        inventory = payload.get("inventory") or payload.get("payload")
        if not provider or not isinstance(inventory, dict):
            raise HTTPException(status_code=400, detail="provider and inventory object are required")
        result = ingest_endpoint_inventory(
            str(provider),
            inventory,
            channel=payload.get("channel"),
            observed_at=payload.get("observed_at"),
            source=payload.get("source"),
        )
        if not result.valid or result.ingestion is None:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = evidence_store.upsert(build_endpoint_inventory_ingestion_metadata(result.ingestion))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/endpoint-inventory-ingestions")
    def endpoint_inventory_ingestion_index(
        provider: Optional[str] = None,
        channel: Optional[str] = None,
        deployment_target: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-inventory-ingestion",
            limit=500,
            offset=0,
        )
        return filter_endpoint_inventory_ingestion_history(
            result["items"],
            provider=provider,
            channel=channel,
            deployment_target=deployment_target,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-inventory-ingestions/dashboard")
    def endpoint_inventory_ingestion_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-inventory-ingestion",
            limit=500,
            offset=0,
        )
        return build_endpoint_inventory_ingestion_dashboard(result["items"])

    @app.post("/endpoint-inventory/freshness-report")
    def endpoint_inventory_freshness_report(payload: dict) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-inventory-ingestion",
            limit=500,
            offset=0,
        )
        freshness = evaluate_endpoint_inventory_freshness(
            result["items"],
            provider=payload.get("provider"),
            channel=payload.get("channel"),
            deployment_target=payload.get("deployment_target"),
            max_age_hours=int(payload.get("max_age_hours", 24)),
            critical_age_hours=int(payload.get("critical_age_hours", 48)),
        )
        if not freshness.valid or freshness.report is None:
            raise HTTPException(status_code=400, detail={"errors": freshness.errors, "warnings": freshness.warnings})
        metadata = evidence_store.upsert(build_endpoint_inventory_freshness_metadata(freshness.report))
        return freshness.to_dict() | {"metadata": metadata}

    @app.get("/endpoint-inventory-freshness")
    def endpoint_inventory_freshness_index(
        alert_level: Optional[str] = None,
        provider: Optional[str] = None,
        channel: Optional[str] = None,
        deployment_target: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-inventory-freshness-report",
            limit=500,
            offset=0,
        )
        return filter_endpoint_inventory_freshness_history(
            result["items"],
            alert_level=alert_level,
            provider=provider,
            channel=channel,
            deployment_target=deployment_target,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-inventory-freshness/dashboard")
    def endpoint_inventory_freshness_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-inventory-freshness-report",
            limit=500,
            offset=0,
        )
        return build_endpoint_inventory_freshness_dashboard(result["items"])

    @app.post("/endpoint-deployment/reconcile")
    def endpoint_deployment_reconcile(payload: dict) -> dict:
        desired_manifest = payload.get("desired_manifest")
        observed_inventory = payload.get("observed_inventory")
        if not isinstance(desired_manifest, dict) or not isinstance(observed_inventory, dict):
            raise HTTPException(status_code=400, detail="desired_manifest and observed_inventory are required objects")
        result = reconcile_managed_endpoint_deployment(
            desired_manifest,
            observed_inventory,
            stale_after_hours=int(payload.get("stale_after_hours", 24)),
            require_package_verification=False,
        )
        if not result.valid or result.report is None:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = evidence_store.upsert(build_managed_endpoint_reconciliation_metadata(result.report))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/endpoint-reconciliations")
    def endpoint_reconciliation_index(
        drift_status: Optional[str] = None,
        alert_level: Optional[str] = None,
        deployment_target: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="managed-endpoint-reconciliation",
            limit=500,
            offset=0,
        )
        return filter_managed_endpoint_reconciliation_history(
            result["items"],
            drift_status=drift_status,
            alert_level=alert_level,
            deployment_target=deployment_target,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-reconciliations/dashboard")
    def endpoint_reconciliation_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="managed-endpoint-reconciliation",
            limit=500,
            offset=0,
        )
        return build_managed_endpoint_reconciliation_dashboard(result["items"])

    @app.post("/endpoint-inventory-ingestions/{inventory_id}/reconcile")
    def endpoint_inventory_ingestion_reconcile(inventory_id: str, payload: dict) -> dict:
        item = evidence_store.get(inventory_id)
        if item is None or item.get("metadata_kind") != "endpoint-inventory-ingestion":
            raise HTTPException(status_code=404, detail="endpoint inventory ingestion not found")
        desired_manifest = payload.get("desired_manifest")
        if not isinstance(desired_manifest, dict):
            raise HTTPException(status_code=400, detail="desired_manifest is required")
        result = automate_endpoint_reconciliation_from_ingestion(
            desired_manifest,
            item,
            stale_after_hours=int(payload.get("stale_after_hours", 24)),
            remediation_strategy=payload.get("remediation_strategy", payload.get("strategy", "mixed")),
            requested_by=payload.get("requested_by", "console"),
            approver_group=payload.get("approver_group", "Endpoint Change Advisory Board"),
            ttl_hours=int(payload.get("ttl_hours", 24)),
        )
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        if result.reconciliation:
            evidence_store.upsert(build_managed_endpoint_reconciliation_metadata(result.reconciliation))
        if result.approval:
            approval_store.upsert(result.approval)
        if result.remediation_request:
            evidence_store.upsert(build_endpoint_drift_remediation_request_metadata(result.remediation_request))
        metadata = None
        if result.automation:
            metadata = evidence_store.upsert(build_endpoint_reconciliation_automation_metadata(result.automation))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/endpoint-reconciliation-automations")
    def endpoint_reconciliation_automation_index(
        drift_status: Optional[str] = None,
        alert_level: Optional[str] = None,
        approval_state: Optional[str] = None,
        provider: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-reconciliation-automation",
            limit=500,
            offset=0,
        )
        return filter_endpoint_reconciliation_automation_history(
            result["items"],
            drift_status=drift_status,
            alert_level=alert_level,
            approval_state=approval_state,
            provider=provider,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-reconciliation-automations/dashboard")
    def endpoint_reconciliation_automation_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-reconciliation-automation",
            limit=500,
            offset=0,
        )
        return build_endpoint_reconciliation_automation_dashboard(result["items"])

    @app.post("/endpoint-reconciliations/{reconciliation_id}/remediation-request")
    def endpoint_reconciliation_remediation_request(reconciliation_id: str, payload: dict) -> dict:
        item = evidence_store.get(reconciliation_id)
        if item is None or item.get("metadata_kind") != "managed-endpoint-reconciliation":
            raise HTTPException(status_code=404, detail="endpoint reconciliation not found")
        report = item.get("report")
        if not isinstance(report, dict):
            raise HTTPException(status_code=400, detail="reconciliation metadata is missing report payload")
        result = create_endpoint_drift_remediation_request(
            report,
            strategy=payload.get("strategy", "mixed"),
            requested_by=payload.get("requested_by", "console"),
            approver_group=payload.get("approver_group", "Endpoint Change Advisory Board"),
            ttl_hours=int(payload.get("ttl_hours", 24)),
        )
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        if result.approval:
            approval_store.upsert(result.approval)
        metadata = None
        if result.request:
            metadata = evidence_store.upsert(build_endpoint_drift_remediation_request_metadata(result.request))
        return result.to_dict() | {"metadata": metadata}

    @app.post("/endpoint-remediations/{request_id}/execute")
    def endpoint_remediation_execute(request_id: str, payload: dict) -> dict:
        item = evidence_store.get(request_id)
        if item is None or item.get("metadata_kind") != "endpoint-drift-remediation-request":
            raise HTTPException(status_code=404, detail="endpoint remediation request not found")
        request_payload = item.get("request")
        if not isinstance(request_payload, dict):
            raise HTTPException(status_code=400, detail="remediation metadata is missing request payload")
        request_approval = request_payload.get("approval", {})
        approval_id = payload.get("approval_id") or (
            request_approval.get("approval_id") if isinstance(request_approval, dict) else None
        )
        if not approval_id:
            raise HTTPException(status_code=400, detail="endpoint remediation execution requires approval_id")
        approval = approval_store.get(str(approval_id))
        if approval is None:
            raise HTTPException(status_code=404, detail="approval not found")
        result = execute_endpoint_drift_remediation(
            request_payload,
            approval,
            executed_by=payload.get("executed_by", "console"),
            execution_environment=payload.get("execution_environment"),
            notes=payload.get("notes"),
        )
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = None
        if result.execution:
            metadata = evidence_store.upsert(build_endpoint_drift_remediation_execution_metadata(result.execution))
        return result.to_dict() | {"metadata": metadata}

    @app.post("/endpoint-remediations/{request_id}/handoff")
    def endpoint_remediation_handoff(request_id: str, payload: dict) -> dict:
        item = evidence_store.get(request_id)
        if item is None or item.get("metadata_kind") != "endpoint-drift-remediation-request":
            raise HTTPException(status_code=404, detail="endpoint remediation request not found")
        request_payload = item.get("request")
        if not isinstance(request_payload, dict):
            raise HTTPException(status_code=400, detail="remediation metadata is missing request payload")
        raw_providers = payload.get("providers", payload.get("provider", "all"))
        providers = raw_providers if isinstance(raw_providers, list) else [str(raw_providers)]
        result = build_endpoint_remediation_handoff(
            request_payload,
            providers=[str(provider) for provider in providers],
            requested_by=payload.get("requested_by", "console"),
            delivery_mode=payload.get("delivery_mode", "manual"),
        )
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = None
        if result.handoff:
            metadata = evidence_store.upsert(build_endpoint_remediation_handoff_metadata(result.handoff))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/endpoint-remediation-handoffs")
    def endpoint_remediation_handoff_index(
        provider: Optional[str] = None,
        approval_state: Optional[str] = None,
        request_id: Optional[str] = None,
        reconciliation_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-handoff",
            limit=500,
            offset=0,
        )
        return filter_endpoint_remediation_handoff_history(
            result["items"],
            provider=provider,
            approval_state=approval_state,
            request_id=request_id,
            reconciliation_id=reconciliation_id,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediation-handoffs/dashboard")
    def endpoint_remediation_handoff_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-handoff",
            limit=500,
            offset=0,
        )
        return build_endpoint_remediation_handoff_dashboard(result["items"])

    @app.post("/endpoint-remediation-handoffs/{handoff_id}/status")
    def endpoint_remediation_handoff_status(handoff_id: str, payload: dict) -> dict:
        item = evidence_store.get(handoff_id)
        if item is None or item.get("metadata_kind") != "endpoint-remediation-handoff":
            raise HTTPException(status_code=404, detail="endpoint remediation handoff not found")
        handoff_payload = item.get("handoff")
        if not isinstance(handoff_payload, dict):
            raise HTTPException(status_code=400, detail="handoff metadata is missing handoff payload")
        provider = payload.get("provider")
        status = payload.get("status")
        if not provider or not status:
            raise HTTPException(status_code=400, detail="provider and status are required")
        callback_payload = payload.get("callback_payload")
        if callback_payload is not None and not isinstance(callback_payload, dict):
            raise HTTPException(status_code=400, detail="callback_payload must be an object")
        result = record_endpoint_remediation_handoff_status(
            handoff_payload,
            provider=str(provider),
            status=str(status),
            external_ref=payload.get("external_ref"),
            external_url=payload.get("external_url"),
            callback_payload=callback_payload,
            recorded_by=payload.get("recorded_by", "console"),
            notes=payload.get("notes"),
        )
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = None
        if result.status:
            metadata = evidence_store.upsert(build_endpoint_remediation_handoff_status_metadata(result.status))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/endpoint-remediation-handoff-statuses")
    def endpoint_remediation_handoff_status_index(
        provider: Optional[str] = None,
        handoff_status: Optional[str] = None,
        handoff_id: Optional[str] = None,
        request_id: Optional[str] = None,
        external_ref: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-handoff-status",
            limit=500,
            offset=0,
        )
        return filter_endpoint_remediation_handoff_status_history(
            result["items"],
            provider=provider,
            handoff_status=handoff_status,
            handoff_id=handoff_id,
            request_id=request_id,
            external_ref=external_ref,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediation-handoff-statuses/dashboard")
    def endpoint_remediation_handoff_status_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-handoff-status",
            limit=500,
            offset=0,
        )
        return build_endpoint_remediation_handoff_status_dashboard(result["items"])

    @app.post("/endpoint-remediation-sla/report")
    def endpoint_remediation_sla_report(payload: dict) -> dict:
        handoffs = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-handoff",
            limit=500,
            offset=0,
        )["items"]
        statuses = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-handoff-status",
            limit=500,
            offset=0,
        )["items"]
        result = build_endpoint_remediation_sla_report(
            handoffs,
            statuses,
            warning_hours=int(payload.get("warning_hours", 24)),
            critical_hours=int(payload.get("critical_hours", 48)),
            generated_by=payload.get("generated_by", "console"),
        )
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = None
        if result.report:
            metadata = evidence_store.upsert(build_endpoint_remediation_sla_report_metadata(result.report))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/endpoint-remediation-sla-reports")
    def endpoint_remediation_sla_report_index(
        alert_level: Optional[str] = None,
        min_breached: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-sla-report",
            limit=500,
            offset=0,
        )
        return filter_endpoint_remediation_sla_report_history(
            result["items"],
            alert_level=alert_level,
            min_breached=min_breached,
            limit=limit,
            offset=offset,
        )

    @app.post("/endpoint-remediation-sla-reports/{report_id}/deliver")
    def endpoint_remediation_sla_report_deliver(report_id: str, payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        item = evidence_store.get(report_id)
        if item is None or item.get("metadata_kind") != "endpoint-remediation-sla-report":
            raise HTTPException(status_code=404, detail="endpoint remediation SLA report not found")
        report = item.get("report")
        if not isinstance(report, dict):
            raise HTTPException(status_code=400, detail="endpoint remediation SLA metadata is missing report payload")
        try:
            existing_deliveries = _search_evidence_metadata(
                evidence_store,
                metadata_kind="release-connector-delivery",
                limit=500,
                offset=0,
            )["items"]
            plan = build_endpoint_remediation_sla_notification_plan(
                report,
                policy=payload.get("routing_policy") if isinstance(payload.get("routing_policy"), dict) else None,
                delivery_items=existing_deliveries,
                requested_provider=payload.get("provider", "all"),
                available_providers=_configured_connector_providers(connector_config),
                generated_by=payload.get("generated_by", "console"),
                suppression_window_minutes=payload.get("suppression_window_minutes"),
                force=bool(payload.get("force", False)),
            )
            event = build_endpoint_remediation_sla_notification_event(
                report,
                generated_by=payload.get("generated_by", "console"),
                max_escalations=int(payload.get("max_escalations", 10)),
            )
            event["notification_plan"] = plan
            plan_metadata = evidence_store.upsert(build_endpoint_remediation_sla_notification_plan_metadata(plan))
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(result, source="endpoint_remediation_sla_notification")
                )
            return {
                "plan": plan,
                "delivery": result,
                "plan_metadata": plan_metadata,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": report_id,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/endpoint-remediation-sla-reports/{report_id}/acknowledgements")
    def endpoint_remediation_sla_report_acknowledge(report_id: str, payload: dict) -> dict:
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not payload.get("acknowledged_by"):
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_endpoint_remediation_sla_notification(
                report_id,
                provider=payload["provider"],
                acknowledged_by=payload["acknowledged_by"],
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                plan_id=payload.get("plan_id"),
            )
            metadata = evidence_store.upsert(build_endpoint_remediation_sla_notification_ack_metadata(acknowledgement))
            return {"acknowledgement": acknowledgement, "metadata": metadata}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/endpoint-remediation-sla-notifications")
    def endpoint_remediation_sla_notification_index(
        report_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        suppressed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        items = _endpoint_remediation_sla_notification_items(evidence_store)
        return filter_endpoint_remediation_sla_notification_history(
            items,
            report_id=report_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediation-sla-notifications/dashboard")
    def endpoint_remediation_sla_notification_dashboard() -> dict:
        return build_endpoint_remediation_sla_notification_dashboard(
            _endpoint_remediation_sla_notification_items(evidence_store)
        )

    @app.post("/endpoint-remediation-sla-notifications/escalation-plan")
    def endpoint_remediation_sla_escalation_plan(payload: dict) -> dict:
        plan = build_endpoint_remediation_sla_escalation_plan(
            _endpoint_remediation_sla_notification_items(evidence_store),
            policy=payload.get("slo_policy") if isinstance(payload.get("slo_policy"), dict) else None,
            generated_by=payload.get("generated_by", "console"),
        )
        metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_plan_metadata(plan))
        return {"plan": plan, "metadata": metadata}

    @app.post("/endpoint-remediation-sla-escalations/{plan_id}/deliver")
    def endpoint_remediation_sla_escalation_deliver(plan_id: str, payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        item = evidence_store.get(plan_id)
        if item is None or item.get("metadata_kind") != "endpoint-remediation-sla-escalation-plan":
            raise HTTPException(status_code=404, detail="endpoint remediation SLA escalation plan not found")
        plan = item.get("escalation_plan")
        if not isinstance(plan, dict):
            raise HTTPException(status_code=400, detail="endpoint remediation SLA escalation metadata is missing plan payload")
        try:
            event = build_endpoint_remediation_sla_escalation_delivery_event(
                plan,
                generated_by=payload.get("generated_by", "console"),
                max_routes=int(payload.get("max_routes", 20)),
            )
            result = None
            metadata = None
            if event["routes"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=payload.get("provider", "all"),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="endpoint_remediation_sla_escalation_delivery",
                    )
                )
            return {
                "event": event,
                "delivery": result,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": plan_id,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/endpoint-remediation-sla-escalations/{plan_id}/reviews")
    def endpoint_remediation_sla_escalation_review_endpoint(plan_id: str, payload: dict) -> dict:
        for field in ("report_id", "provider", "owner", "reviewed_by"):
            if not payload.get(field):
                raise HTTPException(status_code=400, detail=f"{field} is required")
        try:
            review = review_endpoint_remediation_sla_escalation(
                plan_id,
                report_id=payload["report_id"],
                provider=payload["provider"],
                owner=payload["owner"],
                reviewed_by=payload["reviewed_by"],
                review_state=payload.get("review_state", "accepted"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
            )
            metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_review_metadata(review))
            return {"review": review, "metadata": metadata}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/endpoint-remediation-sla-escalations")
    def endpoint_remediation_sla_escalation_index(
        owner: Optional[str] = None,
        provider: Optional[str] = None,
        alert_level: Optional[str] = None,
        active_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return filter_endpoint_remediation_sla_escalation_history(
            _endpoint_remediation_sla_escalation_items(evidence_store),
            owner=owner,
            provider=provider,
            alert_level=alert_level,
            active_only=active_only,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediation-sla-escalations/dashboard")
    def endpoint_remediation_sla_escalation_dashboard() -> dict:
        return build_endpoint_remediation_sla_escalation_dashboard(
            _endpoint_remediation_sla_escalation_items(evidence_store)
        )

    @app.get("/endpoint-remediation-sla-escalation-actions")
    def endpoint_remediation_sla_escalation_action_index(
        plan_id: Optional[str] = None,
        owner: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        review_state: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return filter_endpoint_remediation_sla_escalation_action_history(
            _endpoint_remediation_sla_escalation_action_items(evidence_store),
            plan_id=plan_id,
            owner=owner,
            provider=provider,
            metadata_kind=metadata_kind,
            review_state=review_state,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediation-sla-escalation-actions/dashboard")
    def endpoint_remediation_sla_escalation_action_dashboard() -> dict:
        return build_endpoint_remediation_sla_escalation_action_dashboard(
            _endpoint_remediation_sla_escalation_action_items(evidence_store)
        )

    @app.post("/endpoint-remediation-sla-escalations/recurrence-plan")
    def endpoint_remediation_sla_escalation_recurrence_plan(payload: dict) -> dict:
        plan = build_endpoint_remediation_sla_escalation_recurrence_plan(
            _endpoint_remediation_sla_escalation_action_items(evidence_store),
            policy=payload.get("recurrence_policy") if isinstance(payload.get("recurrence_policy"), dict) else None,
            generated_by=payload.get("generated_by", "console"),
        )
        metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_recurrence_plan_metadata(plan))
        return {"plan": plan, "metadata": metadata}

    @app.get("/endpoint-remediation-sla-escalation-recurrences")
    def endpoint_remediation_sla_escalation_recurrence_index(
        plan_id: Optional[str] = None,
        owner: Optional[str] = None,
        provider: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return filter_endpoint_remediation_sla_escalation_recurrence_history(
            _endpoint_remediation_sla_escalation_recurrence_items(evidence_store),
            plan_id=plan_id,
            owner=owner,
            provider=provider,
            action=action,
            limit=limit,
            offset=offset,
        )

    @app.post("/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/deliver")
    def endpoint_remediation_sla_escalation_recurrence_deliver(recurrence_plan_id: str, payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        item = evidence_store.get(recurrence_plan_id)
        if item is None or item.get("metadata_kind") != "endpoint-remediation-sla-escalation-recurrence-plan":
            raise HTTPException(status_code=404, detail="endpoint remediation SLA escalation recurrence plan not found")
        plan = item.get("recurrence_plan")
        if not isinstance(plan, dict):
            raise HTTPException(status_code=400, detail="endpoint remediation SLA recurrence metadata is missing plan payload")
        try:
            event = build_endpoint_remediation_sla_escalation_recurrence_delivery_event(
                plan,
                generated_by=payload.get("generated_by", "console"),
                max_routes=int(payload.get("max_routes", 50)),
            )
            result = None
            metadata = None
            if event["routes"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=payload.get("provider", "all"),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="endpoint_remediation_sla_escalation_recurrence_delivery",
                    )
                )
            return {
                "event": event,
                "delivery": result,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": recurrence_plan_id,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/suppression-audit")
    def endpoint_remediation_sla_escalation_suppression_audit(recurrence_plan_id: str) -> dict:
        item = evidence_store.get(recurrence_plan_id)
        if item is None or item.get("metadata_kind") != "endpoint-remediation-sla-escalation-recurrence-plan":
            raise HTTPException(status_code=404, detail="endpoint remediation SLA escalation recurrence plan not found")
        plan = item.get("recurrence_plan")
        if not isinstance(plan, dict):
            raise HTTPException(status_code=400, detail="endpoint remediation SLA recurrence metadata is missing plan payload")
        audit = build_endpoint_remediation_sla_escalation_suppression_audit(plan, generated_by="console")
        metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_suppression_audit_metadata(audit))
        return {"audit": audit, "metadata": metadata}

    @app.post("/endpoint-remediation-sla-escalation-recurrences/retry-plan")
    def endpoint_remediation_sla_escalation_recurrence_retry_plan(payload: dict) -> dict:
        try:
            plan = build_endpoint_remediation_sla_escalation_recurrence_retry_plan(
                _endpoint_remediation_sla_escalation_action_items(evidence_store),
                policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
                generated_by=payload.get("generated_by", "console"),
            )
            metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata(plan))
            return {"plan": plan, "metadata": metadata}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/endpoint-remediation-sla-escalation-recurrences/{recurrence_plan_id}/owner-digest")
    def endpoint_remediation_sla_escalation_owner_digest(recurrence_plan_id: str, payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        item = evidence_store.get(recurrence_plan_id)
        if item is None or item.get("metadata_kind") != "endpoint-remediation-sla-escalation-recurrence-plan":
            raise HTTPException(status_code=404, detail="endpoint remediation SLA escalation recurrence plan not found")
        recurrence_plan = item.get("recurrence_plan")
        if not isinstance(recurrence_plan, dict):
            raise HTTPException(status_code=400, detail="endpoint remediation SLA recurrence metadata is missing plan payload")
        retry_plan = None
        retry_plan_id = payload.get("retry_plan_id")
        if retry_plan_id:
            retry_item = evidence_store.get(str(retry_plan_id))
            if retry_item is None or retry_item.get("metadata_kind") != "endpoint-remediation-sla-escalation-recurrence-retry-plan":
                raise HTTPException(status_code=404, detail="endpoint remediation SLA recurrence retry plan not found")
            retry_plan = retry_item.get("retry_plan")
        try:
            event = build_endpoint_remediation_sla_escalation_owner_digest_event(
                recurrence_plan,
                retry_plan=retry_plan if isinstance(retry_plan, dict) else None,
                generated_by=payload.get("generated_by", "console"),
            )
            digest_metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_owner_digest_metadata(event))
            result = None
            delivery_metadata = None
            if event["owners"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=payload.get("provider", "all"),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="endpoint_remediation_sla_escalation_owner_digest",
                    )
                )
            return {
                "event": event,
                "digest_metadata": digest_metadata,
                "delivery": result,
                "metadata": delivery_metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/endpoint-remediation-sla-escalation-recurrences/suppression-trends")
    def endpoint_remediation_sla_escalation_suppression_trends() -> dict:
        trend = build_endpoint_remediation_sla_escalation_suppression_trends(
            _endpoint_remediation_sla_escalation_action_items(evidence_store),
            generated_by="console",
        )
        metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_suppression_trend_metadata(trend))
        return {"trend": trend, "metadata": metadata}

    @app.post("/endpoint-remediation-sla-escalation-recurrences/automation-run")
    def endpoint_remediation_sla_escalation_recurrence_automation_run(payload: dict) -> dict:
        dry_run = bool(payload.get("dry_run", not bool(payload.get("execute", False))))
        run = build_endpoint_remediation_sla_escalation_recurrence_automation_run(
            _endpoint_remediation_sla_escalation_action_items(evidence_store),
            retry_policy=payload.get("retry_policy") if isinstance(payload.get("retry_policy"), dict) else None,
            schedule=payload.get("schedule") if isinstance(payload.get("schedule"), dict) else None,
            generated_by=payload.get("generated_by", "console"),
            dry_run=dry_run,
            max_digest_plans=int(payload.get("max_digest_plans", 5)),
        )
        retry_metadata = evidence_store.upsert(
            build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata(run["retry_plan"])
        )
        trend_metadata = evidence_store.upsert(
            build_endpoint_remediation_sla_escalation_suppression_trend_metadata(run["suppression_trend"])
        )
        digest_results = []
        for event in run.get("owner_digest_events", []):
            digest_metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_owner_digest_metadata(event))
            delivery = None
            delivery_metadata = None
            skipped = None
            if dry_run:
                skipped = "dry_run"
            elif connector_config is None:
                skipped = "connector_config_not_configured"
            else:
                delivery = deliver_connector_event(
                    event,
                    connector_config,
                    provider=payload.get("provider", "all"),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                delivery_metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        delivery,
                        source="endpoint_remediation_sla_escalation_owner_digest",
                    )
                )
            digest_results.append(
                {
                    "event": event,
                    "digest_metadata": digest_metadata,
                    "delivery": delivery,
                    "delivery_metadata": delivery_metadata,
                    "skipped": skipped,
                }
            )
        metadata = evidence_store.upsert(build_endpoint_remediation_sla_escalation_recurrence_automation_run_metadata(run))
        return {
            "run": run,
            "metadata": metadata,
            "retry_metadata": retry_metadata,
            "trend_metadata": trend_metadata,
            "owner_digests": digest_results,
        }

    @app.get("/endpoint-remediation-sla-escalation-recurrence-automations")
    def endpoint_remediation_sla_escalation_recurrence_automation_index(
        dry_run: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return filter_endpoint_remediation_sla_escalation_recurrence_automation_history(
            _endpoint_remediation_sla_escalation_recurrence_automation_items(evidence_store),
            dry_run=dry_run,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediation-sla-escalation-recurrence-automations/dashboard")
    def endpoint_remediation_sla_escalation_recurrence_automation_dashboard() -> dict:
        return build_endpoint_remediation_sla_escalation_recurrence_automation_dashboard(
            _endpoint_remediation_sla_escalation_recurrence_automation_items(evidence_store)
        )

    @app.get("/endpoint-remediation-sla-escalation-recurrence-automations/health")
    def endpoint_remediation_sla_escalation_recurrence_automation_health(
        expected_interval_minutes: int = 30,
        stale_metadata_minutes: int = 120,
    ) -> dict:
        return build_endpoint_remediation_sla_escalation_recurrence_automation_health(
            _endpoint_remediation_sla_escalation_action_items(evidence_store),
            expected_interval_minutes=expected_interval_minutes,
            stale_metadata_minutes=stale_metadata_minutes,
        )

    @app.post("/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/deliver")
    def endpoint_remediation_sla_escalation_recurrence_automation_health_alert_deliver(payload: dict) -> dict:
        if connector_config is None:
            raise HTTPException(status_code=400, detail="connector config is not configured")
        try:
            items = _endpoint_remediation_sla_escalation_action_items(evidence_store)
            health = build_endpoint_remediation_sla_escalation_recurrence_automation_health(
                items,
                expected_interval_minutes=int(payload.get("expected_interval_minutes", 30)),
                stale_metadata_minutes=int(payload.get("stale_metadata_minutes", 120)),
            )
            existing_deliveries = _search_evidence_metadata(
                evidence_store,
                metadata_kind="release-connector-delivery",
                limit=500,
                offset=0,
            )["items"]
            plan = build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan(
                health,
                policy=payload.get("routing_policy") if isinstance(payload.get("routing_policy"), dict) else None,
                delivery_items=existing_deliveries,
                requested_provider=payload.get("provider", "all"),
                available_providers=_configured_connector_providers(connector_config),
                generated_by=payload.get("generated_by", "console"),
                suppression_window_minutes=payload.get("suppression_window_minutes"),
                force=bool(payload.get("force", False)),
            )
            event = build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_event(
                health,
                generated_by=payload.get("generated_by", "console"),
                max_alerts=int(payload.get("max_alerts", 20)),
            )
            event["health_alert_plan"] = plan
            plan_metadata = evidence_store.upsert(
                build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan_metadata(plan)
            )
            result = None
            metadata = None
            if plan["selected_providers"]:
                result = deliver_connector_event(
                    event,
                    connector_config,
                    provider=",".join(plan["selected_providers"]),
                    retries=int(payload.get("retries", 2)),
                    timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
                )
                metadata = evidence_store.upsert(
                    build_connector_delivery_metadata(
                        result,
                        source="endpoint_remediation_sla_escalation_recurrence_automation_health_alert",
                    )
                )
            return {
                "health": health,
                "plan": plan,
                "delivery": result,
                "plan_metadata": plan_metadata,
                "metadata": metadata,
                "success": bool(result.get("success")) if isinstance(result, dict) else True,
                "event_id": plan.get("health_id"),
            }
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/{health_id}/acknowledgements")
    def endpoint_remediation_sla_escalation_recurrence_automation_health_alert_acknowledge(
        health_id: str,
        payload: dict,
    ) -> dict:
        if not payload.get("provider"):
            raise HTTPException(status_code=400, detail="provider is required")
        if not payload.get("acknowledged_by"):
            raise HTTPException(status_code=400, detail="acknowledged_by is required")
        try:
            acknowledgement = acknowledge_endpoint_remediation_sla_escalation_recurrence_automation_health_alert(
                health_id,
                provider=payload["provider"],
                acknowledged_by=payload["acknowledged_by"],
                acknowledgement_state=payload.get("acknowledgement_state", "acknowledged"),
                external_ref=payload.get("external_ref"),
                notes=payload.get("notes"),
                plan_id=payload.get("plan_id"),
            )
            metadata = evidence_store.upsert(
                build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_ack_metadata(
                    acknowledgement
                )
            )
            return {"acknowledgement": acknowledgement, "metadata": metadata}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts")
    def endpoint_remediation_sla_escalation_recurrence_automation_health_alert_index(
        health_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        suppressed: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return filter_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_history(
            _endpoint_remediation_sla_escalation_action_items(evidence_store),
            health_id=health_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts/dashboard")
    def endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard() -> dict:
        return build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard(
            _endpoint_remediation_sla_escalation_action_items(evidence_store)
        )

    @app.get("/endpoint-remediation-sla-escalation-recurrences/dashboard")
    def endpoint_remediation_sla_escalation_recurrence_dashboard() -> dict:
        return build_endpoint_remediation_sla_escalation_recurrence_dashboard(
            _endpoint_remediation_sla_escalation_recurrence_items(evidence_store)
        )

    @app.get("/endpoint-remediation-sla-reports/dashboard")
    def endpoint_remediation_sla_report_dashboard() -> dict:
        result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-remediation-sla-report",
            limit=500,
            offset=0,
        )
        return build_endpoint_remediation_sla_dashboard(result["items"])

    @app.get("/endpoint-remediations")
    def endpoint_remediation_index(
        metadata_kind: Optional[str] = None,
        reconciliation_id: Optional[str] = None,
        approval_state: Optional[str] = None,
        execution_status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        request_result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-drift-remediation-request",
            limit=500,
            offset=0,
        )
        execution_result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-drift-remediation-execution",
            limit=500,
            offset=0,
        )
        return filter_endpoint_drift_remediation_history(
            [*request_result["items"], *execution_result["items"]],
            metadata_kind=metadata_kind,
            reconciliation_id=reconciliation_id,
            approval_state=approval_state,
            execution_status=execution_status,
            limit=limit,
            offset=offset,
        )

    @app.get("/endpoint-remediations/dashboard")
    def endpoint_remediation_dashboard() -> dict:
        request_result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-drift-remediation-request",
            limit=500,
            offset=0,
        )
        execution_result = _search_evidence_metadata(
            evidence_store,
            metadata_kind="endpoint-drift-remediation-execution",
            limit=500,
            offset=0,
        )
        return build_endpoint_drift_remediation_dashboard([*request_result["items"], *execution_result["items"]])

    @app.post("/evidence")
    def upsert_evidence_metadata(payload: dict) -> dict:
        try:
            return evidence_store.upsert(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/evidence/{session_id}/artifacts")
    def evidence_artifact_index(session_id: str) -> dict:
        metadata = _get_evidence_metadata_or_404(evidence_store, session_id)
        root = _configured_artifact_root(evidence_artifact_root)
        encoded_session_id = quote(session_id, safe="")
        try:
            return list_evidence_artifacts(
                root,
                session_id,
                metadata=metadata,
                base_path=f"/evidence/{encoded_session_id}/artifacts",
                bundle_path=f"/evidence/{encoded_session_id}/artifact-bundle",
            )
        except EvidenceArtifactError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/evidence/{session_id}/promotion-request")
    def evidence_rollout_promotion_request(session_id: str, payload: dict) -> dict:
        metadata = _get_evidence_metadata_or_404(evidence_store, session_id)
        if metadata.get("metadata_kind") != "managed-endpoint-rollout":
            raise HTTPException(status_code=400, detail="promotion requests require managed endpoint rollout metadata")
        root = _configured_artifact_root(evidence_artifact_root)
        rollout_dir = _resolve_under_artifact_root(root, metadata.get("bundle_dir"), "rollout evidence directory")
        package_dir = None
        if payload.get("package_dir"):
            package_dir = _resolve_under_artifact_root(root, payload.get("package_dir"), "release package directory")
        signing_key_pem = os.environ.get("CAVRA_ROLLOUT_PROMOTION_SIGNING_KEY") or os.environ.get("CAVRA_GO_RELEASE_SIGNING_KEY")
        try:
            result = create_managed_endpoint_rollout_promotion_request(
                rollout_dir,
                output_dir=None,
                target_ring=payload.get("target_ring", "production"),
                requested_by=payload.get("requested_by", "console"),
                approver_group=payload.get("approver_group", "Change Advisory Board"),
                ttl_hours=int(payload.get("ttl_hours", 24)),
                signing_key_pem=signing_key_pem,
                signer=payload.get("signer", "release-manager"),
                package_dir=package_dir,
                require_package_verification=bool(payload.get("require_package_verification", True)),
                require_signatures=bool(payload.get("require_signatures", True)),
                require_provenance=bool(payload.get("require_provenance", True)),
            )
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        if result.approval:
            approval_store.upsert(result.approval)
        return result.to_dict()

    @app.post("/evidence/{session_id}/promotion-execution")
    def evidence_rollout_promotion_execution(session_id: str, payload: dict) -> dict:
        metadata = _get_evidence_metadata_or_404(evidence_store, session_id)
        if metadata.get("metadata_kind") != "managed-endpoint-rollout":
            raise HTTPException(status_code=400, detail="promotion executions require managed endpoint rollout metadata")
        request_payload = payload.get("request")
        if not isinstance(request_payload, dict):
            raise HTTPException(status_code=400, detail="promotion execution requires request payload")
        if request_payload.get("rollout_id") != session_id:
            raise HTTPException(status_code=400, detail="promotion request rollout_id does not match evidence session")
        request_approval = request_payload.get("approval", {})
        approval_id = payload.get("approval_id") or (
            request_approval.get("approval_id") if isinstance(request_approval, dict) else None
        )
        if not approval_id:
            raise HTTPException(status_code=400, detail="promotion execution requires approval_id")
        approval = approval_store.get(str(approval_id))
        if approval is None:
            raise HTTPException(status_code=404, detail="approval not found")
        try:
            result = create_managed_endpoint_rollout_promotion_execution(
                request_payload,
                approval,
                output_dir=None,
                executed_by=payload.get("executed_by", "console"),
                execution_environment=payload.get("execution_environment"),
                notes=payload.get("notes"),
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not result.valid:
            raise HTTPException(status_code=400, detail={"errors": result.errors, "warnings": result.warnings})
        metadata = None
        if result.execution:
            metadata = evidence_store.upsert(build_managed_endpoint_rollout_promotion_execution_metadata(result.execution))
        return result.to_dict() | {"metadata": metadata}

    @app.get("/evidence/{session_id}/artifact-bundle")
    def evidence_artifact_bundle(session_id: str):
        metadata = _get_evidence_metadata_or_404(evidence_store, session_id)
        root = _configured_artifact_root(evidence_artifact_root)
        try:
            artifact_metadata, payload = build_evidence_artifact_archive(root, session_id, metadata=metadata)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="evidence artifacts not found") from exc
        except EvidenceArtifactError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return Response(
            payload,
            media_type=artifact_metadata["media_type"],
            headers={
                "content-disposition": f'attachment; filename="{artifact_metadata["artifact"]}"',
                "x-cavra-artifact-sha256": str(artifact_metadata["sha256"]),
            },
        )

    @app.get("/evidence/{session_id}/artifacts/{artifact_name}")
    def evidence_artifact(session_id: str, artifact_name: str):
        metadata = _get_evidence_metadata_or_404(evidence_store, session_id)
        root = _configured_artifact_root(evidence_artifact_root)
        try:
            artifact_metadata, payload = load_evidence_artifact(root, session_id, artifact_name, metadata=metadata)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="evidence artifact not found") from exc
        except EvidenceArtifactError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return Response(
            payload,
            media_type=artifact_metadata["media_type"],
            headers={
                "content-disposition": f'attachment; filename="{artifact_metadata["artifact"]}"',
                "x-cavra-artifact-sha256": str(artifact_metadata["sha256"]),
            },
        )

    @app.get("/evidence/{session_id}")
    def evidence_metadata(session_id: str) -> dict:
        item = evidence_store.get(session_id)
        if item is None:
            raise HTTPException(status_code=404, detail="evidence metadata not found")
        return item

    @app.get("/api/sandbox/scenarios")
    def sandbox_scenarios() -> list[dict]:
        return available_sandbox_scenarios()

    @app.get("/api/sandbox/metrics")
    def sandbox_metrics() -> dict:
        summary = activity_store.summarize_sessions(repository="sandbox/before-the-agent-acts", agent_id="sandbox-agent")
        return {
            "schema_version": "cavra.sandbox.metrics.v1",
            "product": "CAVRA",
            "source": "activity_store",
            "tracking": "none",
            "telemetry": "disabled",
            "scenario": "before-the-agent-acts",
            "repository": "sandbox/before-the-agent-acts",
            "total_runs": summary["total_sessions"],
            "total_decisions": summary["total_decisions"],
            "blocked_actions": summary["total_blocked"],
            "approval_required_actions": summary["total_approval_required"],
            "latest_run_at": summary["latest_session_at"],
            "generated_at": utc_now(),
        }

    @app.post("/api/sandbox/run")
    def sandbox_run(payload: Optional[dict] = None) -> dict:
        try:
            run = create_sandbox_run(**(payload or {}))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        runs[run["run_id"]] = run
        _persist_sandbox_run(run, evidence_store, activity_store)
        return run

    @app.get("/api/sandbox/runs/{run_id}")
    def get_run(run_id: str) -> dict:
        return _sandbox_run_or_404(runs, run_id)

    @app.get("/api/sandbox/runs/{run_id}/events")
    def get_events(run_id: str) -> list[dict]:
        return _sandbox_run_or_404(runs, run_id)["events"]

    @app.get("/api/sandbox/runs/{run_id}/evidence")
    def get_evidence(run_id: str):
        return Response(evidence_json(_sandbox_run_or_404(runs, run_id)), media_type="application/json")

    @app.get("/api/sandbox/runs/{run_id}/attestation")
    def get_attestation(run_id: str):
        return Response(pr_attestation(_sandbox_run_or_404(runs, run_id)), media_type="text/markdown")

    @app.get("/api/sandbox/runs/{run_id}/compliance")
    def get_compliance(run_id: str):
        return Response(compliance_mapping(_sandbox_run_or_404(runs, run_id)), media_type="text/markdown")

    @app.post("/api/sandbox/runs/{run_id}/replay")
    def replay(run_id: str) -> dict:
        previous = _sandbox_run_or_404(runs, run_id)
        run = create_sandbox_run(previous["policy_mode"], previous["persona"], previous["scenario"], previous["policy_pack"])
        runs[run["run_id"]] = run
        _persist_sandbox_run(run, evidence_store, activity_store)
        return run

    return app


def _csv_env(name: str) -> list[str]:
    return [item.strip() for item in os.environ.get(name, "").split(",") if item.strip()]


def _sandbox_run_or_404(runs: dict[str, dict], run_id: str) -> dict:
    run = runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="sandbox run not found")
    return run


def _persist_sandbox_run(
    run: dict,
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
    activity_store: ActivityStore | SQLiteActivityStore,
) -> None:
    evidence_store.upsert(sandbox_evidence_metadata(run))
    activity_store.upsert_session(sandbox_activity_session(run))
    for event in run["events"]:
        activity_store.upsert_decision(
            {
                **event,
                "evidence_refs": event.get("evidence_refs") or event.get("evidence_generated", []),
                "requested_operation": event.get("action_type"),
            }
        )


def _filter_json_evidence(
    items: list[dict],
    *,
    session_id: Optional[str] = None,
    signer: Optional[str] = None,
    min_blocked: Optional[int] = None,
    has_approvals: Optional[bool] = None,
    metadata_kind: Optional[str] = None,
    rollout_status: Optional[str] = None,
    environment: Optional[str] = None,
    deployment_target: Optional[str] = None,
    target_ring: Optional[str] = None,
    approval_state: Optional[str] = None,
    promotion_execution_status: Optional[str] = None,
    rollback_execution_status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, object]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = items
    if session_id:
        filtered = [item for item in filtered if session_id in str(item.get("session_id", ""))]
    if signer:
        filtered = [item for item in filtered if item.get("signer") == signer]
    if min_blocked is not None:
        filtered = [item for item in filtered if int(item.get("blocked_count", 0)) >= min_blocked]
    if has_approvals is not None:
        filtered = [
            item
            for item in filtered
            if (int(item.get("approval_required_count", 0)) > 0) is has_approvals
        ]
    if metadata_kind:
        filtered = [item for item in filtered if item.get("metadata_kind") == metadata_kind]
    if rollout_status:
        filtered = [item for item in filtered if item.get("rollout_status") == rollout_status]
    if environment:
        filtered = [item for item in filtered if item.get("environment") == environment]
    if deployment_target:
        filtered = [
            item
            for item in filtered
            if deployment_target in {str(target) for target in item.get("deployment_targets", [])}
        ]
    if target_ring:
        filtered = [item for item in filtered if item.get("target_ring") == target_ring]
    if approval_state:
        filtered = [item for item in filtered if item.get("approval_state") == approval_state]
    if promotion_execution_status:
        filtered = [
            item
            for item in filtered
            if item.get("promotion_execution_status") == promotion_execution_status
        ]
    if rollback_execution_status:
        filtered = [
            item
            for item in filtered
            if item.get("rollback_execution_status") == rollback_execution_status
        ]
    return {
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def _search_evidence_metadata(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
    **filters: object,
) -> dict:
    if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
        return evidence_store.search(**filters)
    return _filter_json_evidence(evidence_store.list(), **filters)


def _endpoint_remediation_sla_notification_items(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
) -> list[dict]:
    if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
        plans = evidence_store.search(metadata_kind="endpoint-remediation-sla-notification-plan", limit=500)["items"]
        acknowledgements = evidence_store.search(metadata_kind="endpoint-remediation-sla-notification-ack", limit=500)[
            "items"
        ]
        deliveries = evidence_store.search(metadata_kind="release-connector-delivery", limit=500)["items"]
        return [*plans, *acknowledgements, *deliveries]
    return evidence_store.list()


def _go_rollback_drill_notification_items(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
) -> list[dict]:
    if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
        plans = evidence_store.search(metadata_kind="go-backend-rollback-drill-notification-plan", limit=500)["items"]
        acknowledgements = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-notification-ack",
            limit=500,
        )["items"]
        escalations = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-notification-escalation-plan",
            limit=500,
        )["items"]
        suppression_trends = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-routing-suppression-trend",
            limit=500,
        )["items"]
        audit_packages = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-package",
            limit=500,
        )["items"]
        audit_delivery_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-plan",
            limit=500,
        )["items"]
        audit_delivery_retry_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-retry-plan",
            limit=500,
        )["items"]
        audit_delivery_retry_acks = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-retry-ack",
            limit=500,
        )["items"]
        audit_delivery_retry_execution_approval_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-plan",
            limit=500,
        )["items"]
        audit_delivery_retry_execution_approval_decisions = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-approval-decision",
            limit=500,
        )["items"]
        audit_delivery_retry_execution_records = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-retry-execution-record",
            limit=500,
        )["items"]
        audit_delivery_connector_recovery_playbooks = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-playbook",
            limit=500,
        )["items"]
        audit_delivery_connector_recovery_closures = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-connector-recovery-closure",
            limit=500,
        )["items"]
        audit_delivery_retry_recovery_reports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-retry-recovery-report",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-plan",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_acks = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-ack",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_retry_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-delivery-retry-plan",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_retry_worker_runs = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-worker-run",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_retry_execution_records = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-execution-record",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_retry_health_reports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_retry_health_alerts = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-plan",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_retry_health_alert_acks = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-ack",
            limit=500,
        )["items"]
        audit_delivery_recovery_escalation_retry_health_alert_retry_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-escalation-retry-health-alert-delivery-retry-plan",
            limit=500,
        )["items"]
        audit_delivery_recovery_executive_reports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report",
            limit=500,
        )["items"]
        audit_delivery_recovery_executive_report_schedule_runs = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-schedule-run",
            limit=500,
        )["items"]
        audit_delivery_recovery_executive_report_delivery_retry_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-plan",
            limit=500,
        )["items"]
        audit_delivery_recovery_executive_report_delivery_retry_worker_runs = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-worker-run",
            limit=500,
        )["items"]
        audit_delivery_recovery_executive_report_delivery_retry_execution_records = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-execution-record",
            limit=500,
        )["items"]
        audit_delivery_recovery_executive_report_delivery_retry_health_reports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-recovery-executive-report-delivery-retry-health",
            limit=500,
        )["items"]
        audit_delivery_worker_runs = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-worker-run",
            limit=500,
        )["items"]
        audit_delivery_worker_health_alerts = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-plan",
            limit=500,
        )["items"]
        audit_delivery_worker_health_alert_acks = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-worker-health-alert-ack",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_readiness_summaries = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-readiness-summary",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_operator_runbook_exports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-operator-runbook-export",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_readiness_approvals = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-readiness-approval-decision",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_record_attachments = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-record-attachment",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_closure_packet_verifications = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-closure-packet-verification",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_auditor_exports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_auditor_export_delivery_retry_plans = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export-delivery-retry-plan",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_auditor_export_delivery_retry_worker_runs = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export-delivery-retry-worker-run",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_auditor_export_delivery_retry_execution_records = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-auditor-export-delivery-retry-execution-record",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_immutable_archive_references = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-immutable-archive-reference",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_archive_reference_health_reports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-archive-reference-health",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_archive_reference_health_alerts = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-archive-reference-health-alert-plan",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_archive_reference_health_alert_acks = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-archive-reference-health-alert-ack",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_readiness_bundles = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-readiness-bundle",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_signed_archive_manifests = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-signed-archive-manifest",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_closeout_summaries = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-closeout-summary",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_closeout_deliveries = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-release-closeout-delivery",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_closeout_retention_review_requests = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-closeout-retention-review-request",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_closeout_retention_review_decisions = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-closeout-retention-review-decision",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_closeout_artifact_bundles = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-closeout-artifact-bundle",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_closeout_retention_health_reports = evidence_store.search(
            metadata_kind="go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-closeout-retention-health",
            limit=500,
        )["items"]
        audit_delivery_final_reporting_closeout_retention_health_alerts = evidence_store.search(
            metadata_kind=(
                "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-"
                "closeout-retention-health-alert-plan"
            ),
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_closeout_delivery_retry_plans = evidence_store.search(
            metadata_kind=(
                "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-"
                "release-closeout-delivery-retry-plan"
            ),
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_closeout_delivery_retry_worker_runs = evidence_store.search(
            metadata_kind=(
                "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-"
                "release-closeout-delivery-retry-worker-run"
            ),
            limit=500,
        )["items"]
        audit_delivery_final_reporting_release_closeout_delivery_retry_execution_records = evidence_store.search(
            metadata_kind=(
                "go-backend-rollback-drill-acknowledgement-audit-delivery-final-reporting-"
                "release-closeout-delivery-retry-execution-record"
            ),
            limit=500,
        )["items"]
        deliveries = evidence_store.search(metadata_kind="release-connector-delivery", limit=500)["items"]
        return [
            *plans,
            *acknowledgements,
            *escalations,
            *suppression_trends,
            *audit_packages,
            *audit_delivery_plans,
            *audit_delivery_retry_plans,
            *audit_delivery_retry_acks,
            *audit_delivery_retry_execution_approval_plans,
            *audit_delivery_retry_execution_approval_decisions,
            *audit_delivery_retry_execution_records,
            *audit_delivery_connector_recovery_playbooks,
            *audit_delivery_connector_recovery_closures,
            *audit_delivery_retry_recovery_reports,
            *audit_delivery_recovery_escalation_plans,
            *audit_delivery_recovery_escalation_acks,
            *audit_delivery_recovery_escalation_retry_plans,
            *audit_delivery_recovery_escalation_retry_worker_runs,
            *audit_delivery_recovery_escalation_retry_execution_records,
            *audit_delivery_recovery_escalation_retry_health_reports,
            *audit_delivery_recovery_escalation_retry_health_alerts,
            *audit_delivery_recovery_escalation_retry_health_alert_acks,
            *audit_delivery_recovery_escalation_retry_health_alert_retry_plans,
            *audit_delivery_recovery_executive_reports,
            *audit_delivery_recovery_executive_report_schedule_runs,
            *audit_delivery_recovery_executive_report_delivery_retry_plans,
            *audit_delivery_recovery_executive_report_delivery_retry_worker_runs,
            *audit_delivery_recovery_executive_report_delivery_retry_execution_records,
            *audit_delivery_recovery_executive_report_delivery_retry_health_reports,
            *audit_delivery_final_reporting_release_readiness_summaries,
            *audit_delivery_final_reporting_operator_runbook_exports,
            *audit_delivery_final_reporting_release_readiness_approvals,
            *audit_delivery_final_reporting_release_record_attachments,
            *audit_delivery_final_reporting_release_closure_packet_verifications,
            *audit_delivery_final_reporting_auditor_exports,
            *audit_delivery_final_reporting_auditor_export_delivery_retry_plans,
            *audit_delivery_final_reporting_auditor_export_delivery_retry_worker_runs,
            *audit_delivery_final_reporting_auditor_export_delivery_retry_execution_records,
            *audit_delivery_final_reporting_immutable_archive_references,
            *audit_delivery_final_reporting_archive_reference_health_reports,
            *audit_delivery_final_reporting_archive_reference_health_alerts,
            *audit_delivery_final_reporting_archive_reference_health_alert_acks,
            *audit_delivery_final_reporting_readiness_bundles,
            *audit_delivery_final_reporting_signed_archive_manifests,
            *audit_delivery_final_reporting_release_closeout_summaries,
            *audit_delivery_final_reporting_release_closeout_deliveries,
            *audit_delivery_final_reporting_closeout_retention_review_requests,
            *audit_delivery_final_reporting_closeout_retention_review_decisions,
            *audit_delivery_final_reporting_closeout_artifact_bundles,
            *audit_delivery_final_reporting_closeout_retention_health_reports,
            *audit_delivery_final_reporting_closeout_retention_health_alerts,
            *audit_delivery_final_reporting_release_closeout_delivery_retry_plans,
            *audit_delivery_final_reporting_release_closeout_delivery_retry_worker_runs,
            *audit_delivery_final_reporting_release_closeout_delivery_retry_execution_records,
            *audit_delivery_worker_runs,
            *audit_delivery_worker_health_alerts,
            *audit_delivery_worker_health_alert_acks,
            *deliveries,
        ]
    return evidence_store.list()


def _endpoint_remediation_sla_escalation_items(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
) -> list[dict]:
    if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
        return evidence_store.search(metadata_kind="endpoint-remediation-sla-escalation-plan", limit=500)["items"]
    return evidence_store.list()


def _endpoint_remediation_sla_escalation_action_items(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
) -> list[dict]:
    if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
        plans = evidence_store.search(metadata_kind="endpoint-remediation-sla-escalation-plan", limit=500)["items"]
        reviews = evidence_store.search(metadata_kind="endpoint-remediation-sla-escalation-review", limit=500)["items"]
        recurrences = evidence_store.search(metadata_kind="endpoint-remediation-sla-escalation-recurrence-plan", limit=500)[
            "items"
        ]
        suppression_audits = evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-suppression-audit",
            limit=500,
        )["items"]
        retry_plans = evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-retry-plan",
            limit=500,
        )["items"]
        owner_digests = evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-owner-digest",
            limit=500,
        )["items"]
        suppression_trends = evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-suppression-trend",
            limit=500,
        )["items"]
        automation_runs = evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-run",
            limit=500,
        )["items"]
        health_alert_plans = evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan",
            limit=500,
        )["items"]
        health_alert_acks = evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack",
            limit=500,
        )["items"]
        deliveries = evidence_store.search(metadata_kind="release-connector-delivery", limit=500)["items"]
        return [
            *plans,
            *reviews,
            *recurrences,
            *suppression_audits,
            *retry_plans,
            *owner_digests,
            *suppression_trends,
            *automation_runs,
            *health_alert_plans,
            *health_alert_acks,
            *deliveries,
        ]
    return evidence_store.list()


def _endpoint_remediation_sla_escalation_recurrence_automation_items(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
) -> list[dict]:
    if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
        return evidence_store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-run",
            limit=500,
        )["items"]
    return evidence_store.list()


def _endpoint_remediation_sla_escalation_recurrence_items(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
) -> list[dict]:
    if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
        return evidence_store.search(metadata_kind="endpoint-remediation-sla-escalation-recurrence-plan", limit=500)[
            "items"
        ]
    return evidence_store.list()


def _configured_connector_providers(config: dict) -> list[str]:
    connectors = config.get("connectors", config.get("providers", config))
    if not isinstance(connectors, dict):
        return []
    return sorted(str(provider) for provider in connectors)


def _configured_artifact_root(root: Path | None) -> Path:
    if root is None:
        raise HTTPException(status_code=400, detail="evidence artifact root is not configured")
    return root.resolve()


def _resolve_under_artifact_root(root: Path, path_value: object, label: str) -> Path:
    artifact_path = Path(str(path_value or "")).resolve()
    try:
        artifact_path.relative_to(root)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"{label} is outside artifact root") from exc
    return artifact_path


def _get_evidence_metadata_or_404(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
    session_id: str,
) -> dict:
    item = evidence_store.get(session_id)
    if item is None:
        raise HTTPException(status_code=404, detail="evidence metadata not found")
    return item


def _get_endpoint_management_export_or_404(
    evidence_store: EvidenceMetadataStore | SQLiteEvidenceMetadataStore,
    export_id: str,
) -> dict:
    item = evidence_store.get(export_id)
    if item is None or item.get("metadata_kind") != "endpoint-management-export":
        raise HTTPException(status_code=404, detail="endpoint management export not found")
    return item


def _policy_rollout_detail(
    rollout: dict,
    inventory_store: InventoryStore | SQLiteInventoryStore,
    activity_store: ActivityStore | SQLiteActivityStore,
    integration_store: IntegrationStore | SQLiteIntegrationStore,
) -> dict[str, object]:
    repository = inventory_store.get_repository(str(rollout.get("repository", "")))
    policy_pack_id = str(rollout.get("policy_pack", ""))
    try:
        policy_pack = PolicyRegistry().get_policy_pack(policy_pack_id)
    except PolicyRegistryError:
        policy_pack = {
            "id": policy_pack_id,
            "title": policy_pack_id or "unknown",
            "description": "Policy pack metadata is not available in this deployment.",
            "version": rollout.get("policy_version", "unknown"),
            "policy": {},
        }
    decisions = activity_store.list_decisions(
        repository=rollout.get("repository"),
        policy_pack=policy_pack_id,
        limit=100,
        offset=0,
    )
    integrations = integration_store.list_integrations()
    return {
        "schema_version": "cavra.policy_rollout.detail.v1",
        "product": "CAVRA",
        "rollout": rollout,
        "repository": repository,
        "policy_pack": {
            "id": policy_pack.get("id"),
            "title": policy_pack.get("title"),
            "description": policy_pack.get("description"),
            "version": policy_pack.get("version"),
            "rule_summary": _policy_rule_summary(policy_pack.get("policy", {})),
        },
        "activity_summary": _decision_summary(decisions.get("items", []), int(decisions.get("total", 0))),
        "integration_summary": _integration_summary(integrations.get("items", [])),
        "readiness": _rollout_readiness(rollout, repository, integrations.get("items", [])),
    }


def _decision_summary(decisions: list[dict], total: int) -> dict[str, object]:
    outcomes: dict[str, int] = {}
    severities: dict[str, int] = {}
    for item in decisions:
        outcome = str(item.get("decision", "unknown"))
        severity = str(item.get("severity", "unknown"))
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        severities[severity] = severities.get(severity, 0) + 1
    return {
        "total": total,
        "sample_size": len(decisions),
        "outcomes": outcomes,
        "severities": severities,
        "recent_decisions": decisions[:10],
    }


def _policy_rule_summary(policy: dict[str, object]) -> dict[str, int]:
    sections = {
        "filesystem": policy.get("filesystem", {}),
        "commands": policy.get("commands", {}),
        "git": policy.get("git", {}),
        "mcp": policy.get("mcp", {}),
        "approvals": policy.get("approvals", {}),
        "evidence": policy.get("evidence", {}),
    }
    return {name: _count_rule_entries(value) for name, value in sections.items()}


def _count_rule_entries(value: object) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return sum(_count_rule_entries(item) for item in value.values())
    return 1 if value else 0


def _integration_summary(integrations: list[dict]) -> dict[str, object]:
    by_category: dict[str, int] = {}
    by_health: dict[str, int] = {}
    for item in integrations:
        category = str(item.get("category", "unknown"))
        health = str(item.get("health_status", "unknown"))
        by_category[category] = by_category.get(category, 0) + 1
        by_health[health] = by_health.get(health, 0) + 1
    return {
        "total": len(integrations),
        "by_category": by_category,
        "by_health": by_health,
        "active_or_configured": [
            item
            for item in integrations
            if item.get("status") in {"active", "configured"}
        ][:10],
    }


def _rollout_readiness(rollout: dict, repository: dict | None, integrations: list[dict]) -> dict[str, object]:
    checks = [
        {
            "id": "repository_registered",
            "status": "pass" if repository else "warn",
            "message": "Repository inventory record is present." if repository else "Repository inventory record is missing.",
        },
        {
            "id": "policy_coverage",
            "status": "pass" if int(rollout.get("coverage_percent", 0)) >= 80 else "warn",
            "message": f"Coverage is {int(rollout.get('coverage_percent', 0))}%.",
        },
        {
            "id": "source_control_integration",
            "status": "pass" if any(item.get("category") == "source_control" for item in integrations) else "warn",
            "message": "Source-control integration is inventoried."
            if any(item.get("category") == "source_control" for item in integrations)
            else "Source-control integration is not inventoried.",
        },
        {
            "id": "siem_or_storage_integration",
            "status": "pass"
            if any(item.get("category") in {"siem", "storage"} for item in integrations)
            else "warn",
            "message": "Evidence export or storage integration is inventoried."
            if any(item.get("category") in {"siem", "storage"} for item in integrations)
            else "Evidence export or storage integration is not inventoried.",
        },
    ]
    return {
        "status": "ready" if all(item["status"] == "pass" for item in checks) else "needs_attention",
        "checks": checks,
    }


def _console_security_boundary(
    *,
    oidc_configured: bool,
    rbac_configured: bool,
    cors_origins: list[str],
) -> dict[str, object]:
    return {
        "schema_version": "cavra.console.security_boundary.v1",
        "product": "CAVRA",
        "mode": "oidc_rbac_ready" if oidc_configured and rbac_configured else "local_or_demo",
        "oidc": {
            "configured": oidc_configured,
            "config_env": "CAVRA_APPROVAL_OIDC_CONFIG",
            "supported_algorithms": ["RS256"],
            "validated_claims": ["iss", "aud", "exp", "nbf", "groups", "roles", "email", "sub"],
        },
        "rbac": {
            "configured": rbac_configured,
            "config_env": "CAVRA_APPROVAL_RBAC_FILE",
            "boundaries": ["approval_group", "repository_permissions", "group_mappings"],
        },
        "cors": {
            "configured": bool(cors_origins),
            "origins": cors_origins,
        },
        "console_permissions": [
            "read_activity",
            "read_inventory",
            "read_integrations",
            "read_evidence_metadata",
            "read_console_session",
            "acknowledge_drill_notifications_requires_oidc_context_when_configured",
            "policy_publish_requires_digest_bound_approval",
            "approval_decision_requires_oidc_context_when_configured",
            "break_glass_requires_oidc_context_when_configured",
        ],
        "operator_notes": [
            "Host the console behind enterprise identity before production use.",
            "Keep backup and restore operations in the CLI or platform runbook, not browser actions.",
            "Use repository RBAC for approval decisions that affect scoped repositories.",
        ],
    }


def _decide_approval(
    approval_store: ApprovalStore,
    approval_id: str,
    *,
    state: str,
    payload: dict,
    rbac_rules: dict[str, object] | None = None,
    oidc_config: dict[str, object] | None = None,
    authorization: str | None = None,
) -> dict:
    actor_context = _console_mutation_actor_context(
        payload,
        authorization=authorization,
        oidc_config=oidc_config,
        rbac_rules=rbac_rules,
    )
    try:
        return approval_store.decide(
            approval_id,
            state=state,
            actor=actor_context.get("actor") if actor_context else payload.get("actor", ""),
            reason=payload.get("reason", ""),
            external_ref=payload.get("external_ref"),
            actor_context=actor_context,
            rbac_rules=rbac_rules,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="approval not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _console_session_context(
    *,
    authorization: str | None,
    oidc_config: dict[str, object] | None,
    rbac_rules: dict[str, object] | None,
) -> dict[str, object]:
    actor_context = _actor_context_from_authorization(authorization, oidc_config=oidc_config, rbac_rules=rbac_rules)
    repository_permissions = repository_permissions_for_actor(actor_context, rbac_rules or {}) if actor_context else []
    return {
        "schema_version": "cavra.console.session.v1",
        "product": "CAVRA",
        "mode": "authenticated" if actor_context else "auth_required" if oidc_config else "local_or_demo",
        "authenticated": actor_context is not None,
        "auth_required": bool(oidc_config),
        "actor": _public_actor_context(actor_context) if actor_context else None,
        "repository_permissions": repository_permissions,
        "permissions": _console_permissions(actor_context, repository_permissions),
        "operator_notes": [
            "Console mutation endpoints require a verified OIDC actor when OIDC or RBAC is configured.",
            "Repository-scoped permissions are evaluated from CAVRA_APPROVAL_RBAC_FILE.",
        ],
    }


def _console_permissions(
    actor_context: dict[str, object] | None,
    repository_permissions: list[dict[str, object]],
) -> dict[str, bool]:
    can_decide = bool(actor_context and (repository_permissions or actor_context.get("groups")))
    return {
        "read_activity": True,
        "read_inventory": True,
        "read_integrations": True,
        "read_evidence_metadata": True,
        "decide_approvals": can_decide,
        "publish_policy_packs": can_decide,
        "acknowledge_drill_notifications": bool(actor_context),
        "create_break_glass": bool(actor_context and "Change Advisory Board" in actor_context.get("groups", [])),
    }


def _current_policy_for_draft(draft_payload: dict) -> dict | None:
    metadata = draft_payload.get("metadata") if isinstance(draft_payload.get("metadata"), dict) else {}
    pack_id = metadata.get("id") or draft_payload.get("id")
    if not pack_id:
        return None
    try:
        return PolicyRegistry().get_policy_pack(str(pack_id)).get("policy")
    except PolicyRegistryError:
        return None


def _public_actor_context(actor_context: dict[str, object]) -> dict[str, object]:
    return {
        "actor": actor_context.get("actor"),
        "subject": actor_context.get("subject"),
        "issuer": actor_context.get("issuer"),
        "groups": actor_context.get("groups", []),
        "repository": actor_context.get("repository"),
    }


def _console_mutation_actor_context(
    payload: dict,
    *,
    authorization: str | None,
    oidc_config: dict[str, object] | None,
    rbac_rules: dict[str, object] | None,
) -> dict[str, object] | None:
    actor_context = None
    if isinstance(payload.get("actor_claims"), dict):
        actor_context = actor_context_from_claims(payload["actor_claims"], rbac_rules=rbac_rules)
    elif isinstance(payload.get("actor_token"), str):
        if not oidc_config:
            raise HTTPException(status_code=400, detail="approval OIDC config is not configured")
        try:
            actor_context = actor_context_from_oidc_token(payload["actor_token"], oidc_config, rbac_rules=rbac_rules)
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
    else:
        actor_context = _actor_context_from_authorization(authorization, oidc_config=oidc_config, rbac_rules=rbac_rules)
    if (oidc_config or rbac_rules) and actor_context is None:
        raise HTTPException(status_code=401, detail="console action requires verified actor context")
    return actor_context


def _actor_context_from_authorization(
    authorization: str | None,
    *,
    oidc_config: dict[str, object] | None,
    rbac_rules: dict[str, object] | None,
) -> dict[str, object] | None:
    token = _bearer_token(authorization)
    if not token:
        return None
    if not oidc_config:
        raise HTTPException(status_code=400, detail="console OIDC config is not configured")
    try:
        return actor_context_from_oidc_token(token, oidc_config, rbac_rules=rbac_rules)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


def _bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(status_code=401, detail="authorization header must use Bearer token")
    return token.strip()


app = create_app() if FastAPI is not None else None
