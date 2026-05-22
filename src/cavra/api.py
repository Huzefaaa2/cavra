from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from cavra.activity import ActivityStore, SQLiteActivityStore, utc_now
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
    acknowledge_go_rollback_drill_notification,
    build_go_rollback_drill_acknowledgement_audit_delivery_event,
    build_go_rollback_drill_acknowledgement_audit_delivery_plan,
    build_go_rollback_drill_acknowledgement_audit_delivery_plan_metadata,
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
    evaluate_with_go_pilot,
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
from cavra.policy_registry import PolicyRegistry, PolicyRegistryError
from cavra.registry import (
    RegistryStore,
    SQLiteRegistryStore,
    classify_mcp_capability,
    default_agent_profiles,
    default_mcp_tool_classifications,
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
            "approval_provider_delivery": "configured" if provider_config is not None else "disabled",
            "connector_delivery": "configured" if connector_config is not None else "disabled",
            "approval_oidc": "configured" if oidc_config else "disabled",
            "approval_rbac": "configured" if rbac_rules else "disabled",
            "evidence_artifacts": "configured" if evidence_artifact_root else "disabled",
            "registry_store": str(registry_store.path),
            "cors_origins": cors_origins,
            "endpoints": {
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
                "agents": "/agents",
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

    @app.get("/runtime/go-pilot/rollback-drill-notifications")
    def runtime_go_pilot_rollback_drill_notification_history(
        schedule_id: Optional[str] = None,
        provider: Optional[str] = None,
        metadata_kind: Optional[str] = None,
        acknowledgement_state: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, object]:
        return filter_go_rollback_drill_notification_history(
            _go_rollback_drill_notification_items(evidence_store),
            schedule_id=schedule_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
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
        deliveries = evidence_store.search(metadata_kind="release-connector-delivery", limit=500)["items"]
        return [
            *plans,
            *acknowledgements,
            *escalations,
            *suppression_trends,
            *audit_packages,
            *audit_delivery_plans,
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
