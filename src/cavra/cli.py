from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON

from cavra import __version__
from cavra.agent import AgentSessionManager
from cavra.agent_enforcement import agent_enforcement_readiness_report
from cavra.ai_red_team import (
    build_ai_red_team_readiness_packet,
    build_guardrail_test_suite,
    build_sample_ai_artifact_metadata,
    run_guardrail_test_suite,
    run_malicious_model_checks,
    validate_ai_red_team_readiness_packet,
    validate_ai_supply_chain_metadata,
    write_ai_red_team_artifacts,
)
from cavra.benchmark_slo import (
    build_benchmark_readiness_packet,
    build_reference_benchmark_report,
    run_local_benchmark_report,
    validate_benchmark_readiness_packet,
    write_benchmark_artifacts,
)
from cavra.aispm_validation import (
    validate_aispm_replay_to_policy_ci_gate_readiness_file,
    validate_aispm_replay_to_policy_review_packet_file,
)
from cavra.continuous_monitoring import (
    DEFAULT_BASE_TIME,
    build_continuous_monitoring_readiness_packet,
    build_sample_monitoring_events,
    replay_monitoring_events,
    validate_continuous_monitoring_packet,
    write_continuous_monitoring_artifacts,
)
from cavra.customer_live_evidence import (
    build_customer_live_evidence_template,
    validate_customer_live_evidence_packet,
    write_customer_live_evidence_artifacts,
)
from cavra.customer_evidence_room import (
    build_customer_evidence_room_index,
    validate_customer_evidence_room_index,
    write_customer_evidence_room_artifacts,
)
from cavra.customer_closeout_handoff import (
    build_customer_closeout_handoff_packet,
    validate_customer_closeout_handoff_packet,
    write_customer_closeout_handoff_artifacts,
)
from cavra.customer_operating_review import (
    build_customer_operating_review_packet,
    validate_customer_operating_review_packet,
    write_customer_operating_review_artifacts,
)
from cavra.customer_renewal_expansion import (
    build_customer_renewal_expansion_packet,
    validate_customer_renewal_expansion_packet,
    write_customer_renewal_expansion_artifacts,
)
from cavra.customer_renewal_outcome import (
    build_customer_renewal_outcome_packet,
    validate_customer_renewal_outcome_packet,
    write_customer_renewal_outcome_artifacts,
)
from cavra.customer_lifecycle_rollup import (
    build_customer_lifecycle_rollup_packet,
    validate_customer_lifecycle_rollup_packet,
    write_customer_lifecycle_rollup_artifacts,
)
from cavra.customer_lifecycle_archive import (
    build_customer_lifecycle_archive_manifest,
    validate_customer_lifecycle_archive_manifest,
    write_customer_lifecycle_archive_artifacts,
)
from cavra.customer_lifecycle_status import (
    build_customer_lifecycle_status_packet,
    validate_customer_lifecycle_status_packet,
    write_customer_lifecycle_status_artifacts,
)
from cavra.customer_lifecycle_final_seal import (
    build_customer_lifecycle_final_seal_packet,
    validate_customer_lifecycle_final_seal_packet,
    write_customer_lifecycle_final_seal_artifacts,
)
from cavra.customer_lifecycle_verification_index import (
    build_customer_lifecycle_verification_index,
    validate_customer_lifecycle_verification_index,
    write_customer_lifecycle_verification_index_artifacts,
)
from cavra.customer_lifecycle_announcement import (
    build_customer_lifecycle_announcement_packet,
    validate_customer_lifecycle_announcement_packet,
    write_customer_lifecycle_announcement_artifacts,
)
from cavra.customer_lifecycle_retrospective import (
    build_customer_lifecycle_retrospective_packet,
    validate_customer_lifecycle_retrospective_packet,
    write_customer_lifecycle_retrospective_artifacts,
)
from cavra.customer_lifecycle_phase8_backlog import (
    build_customer_lifecycle_phase8_backlog_packet,
    validate_customer_lifecycle_phase8_backlog_packet,
    write_customer_lifecycle_phase8_backlog_artifacts,
)
from cavra.customer_lifecycle_phase8_kickoff import (
    build_customer_lifecycle_phase8_kickoff_packet,
    validate_customer_lifecycle_phase8_kickoff_packet,
    write_customer_lifecycle_phase8_kickoff_artifacts,
)
from cavra.customer_lifecycle_phase8_sprint1_checkpoint import (
    build_customer_lifecycle_phase8_sprint1_checkpoint_packet,
    validate_customer_lifecycle_phase8_sprint1_checkpoint_packet,
    write_customer_lifecycle_phase8_sprint1_checkpoint_artifacts,
)
from cavra.customer_lifecycle_phase8_telemetry_depth import (
    build_customer_lifecycle_phase8_telemetry_depth_packet,
    validate_customer_lifecycle_phase8_telemetry_depth_packet,
    write_customer_lifecycle_phase8_telemetry_depth_artifacts,
)
from cavra.customer_lifecycle_phase8_support_automation import (
    build_customer_lifecycle_phase8_support_automation_packet,
    validate_customer_lifecycle_phase8_support_automation_packet,
    write_customer_lifecycle_phase8_support_automation_artifacts,
)
from cavra.customer_lifecycle_phase8_lifecycle_analytics import (
    build_customer_lifecycle_phase8_lifecycle_analytics_packet,
    validate_customer_lifecycle_phase8_lifecycle_analytics_packet,
    write_customer_lifecycle_phase8_lifecycle_analytics_artifacts,
)
from cavra.customer_lifecycle_phase8_customer_health_review import (
    build_customer_lifecycle_phase8_customer_health_review_packet,
    validate_customer_lifecycle_phase8_customer_health_review_packet,
    write_customer_lifecycle_phase8_customer_health_review_artifacts,
)
from cavra.customer_lifecycle_phase8_executive_health_rollup import (
    build_customer_lifecycle_phase8_executive_health_rollup_packet,
    validate_customer_lifecycle_phase8_executive_health_rollup_packet,
    write_customer_lifecycle_phase8_executive_health_rollup_artifacts,
)
from cavra.customer_lifecycle_phase8_executive_action_plan import (
    build_customer_lifecycle_phase8_executive_action_plan_packet,
    validate_customer_lifecycle_phase8_executive_action_plan_packet,
    write_customer_lifecycle_phase8_executive_action_plan_artifacts,
)
from cavra.customer_lifecycle_phase8_action_followup_checkpoint import (
    build_customer_lifecycle_phase8_action_followup_checkpoint_packet,
    validate_customer_lifecycle_phase8_action_followup_checkpoint_packet,
    write_customer_lifecycle_phase8_action_followup_checkpoint_artifacts,
)
from cavra.customer_lifecycle_phase8_executive_followup_closeout import (
    build_customer_lifecycle_phase8_executive_followup_closeout_packet,
    validate_customer_lifecycle_phase8_executive_followup_closeout_packet,
    write_customer_lifecycle_phase8_executive_followup_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_next_cycle_readiness_index import (
    build_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
    validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet,
    write_customer_lifecycle_phase8_next_cycle_readiness_index_artifacts,
)
from cavra.customer_lifecycle_phase8_public_operating_scorecard import (
    build_customer_lifecycle_phase8_public_operating_scorecard_packet,
    validate_customer_lifecycle_phase8_public_operating_scorecard_packet,
    write_customer_lifecycle_phase8_public_operating_scorecard_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_publication_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_publication_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_refresh_checkpoint import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet,
    validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet,
    write_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_refresh_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_refresh_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_operating_loop_index import (
    build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet,
    validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet,
    write_customer_lifecycle_phase8_public_scorecard_operating_loop_index_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_executive_summary_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_distribution_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet,
    write_customer_lifecycle_phase8_public_scorecard_distribution_readiness_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_distribution_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_distribution_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_distribution_audit_index import (
    build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet,
    validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet,
    write_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_audit_review_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet,
    write_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet,
    write_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet,
    write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet,
    write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_artifacts,
)
from cavra.customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout import (
    build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet,
    validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet,
    write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_artifacts,
)
from cavra.approvals import (
    ApprovalStore,
    SQLiteApprovalStore,
    actor_context_from_claims,
    actor_context_from_oidc_token,
    deliver_provider_requests,
    export_approval_notification_payloads,
    export_provider_delivery_result,
    export_provider_request_specs,
    load_oidc_config,
    load_provider_config,
    load_rbac_rules,
    load_routing_rules,
    route_approver_group,
)
from cavra.evidence import (
    EvidenceMetadataStore,
    SQLiteEvidenceMetadataStore,
    apply_sqlite_migrations,
    create_evidence_bundle,
    export_attestation_verification,
    export_immutable_storage_plan,
    export_key_trust_root,
    export_retention_policy,
    export_siem_payloads,
    export_trust_root_distribution,
    export_trust_root_bundle,
    generate_ed25519_keypair,
    verify_evidence_bundle,
)
from cavra.go_backend import (
    GO_BACKEND_ENFORCE,
    GO_BACKEND_PROMOTED,
    GO_BACKEND_SHADOW,
    GoBackendConfig,
    acknowledge_go_rollback_drill_notification,
    build_go_rollback_drill_notification_ack_metadata,
    build_go_rollback_drill_notification_escalation_plan,
    build_go_rollback_drill_notification_event,
    build_go_rollback_drill_notification_plan,
    evaluate_with_go_pilot,
    go_backend_readiness_report,
    go_deployment_readiness_report,
    go_promotion_readiness_report,
    go_rollback_readiness_report,
    go_rollback_drill_history_report,
    go_rollback_drill_schedule_report,
    go_rollback_rehearsal_report,
)
from cavra.generic_agent_adapter import (
    build_action_taxonomy,
    build_sample_adapter_manifest,
    build_sample_generic_actions,
    evaluate_generic_actions,
    validate_adapter_manifest,
    validate_generic_adapter_readiness_packet,
    write_generic_adapter_artifacts,
)
from cavra.integrations import (
    CommandInterceptor,
    build_connector_delivery_dashboard,
    build_connector_delivery_metadata,
    deliver_connector_event,
    export_connector_delivery_result,
    filter_connector_delivery_history,
    load_connector_config,
)
from cavra.zero_trust_reference_deployments import (
    build_reference_deployment_catalog,
    validate_reference_deployment_catalog,
    validate_reference_deployment_readiness_packet,
    write_reference_deployment_artifacts,
)
from cavra.operations import (
    backup_persistent_api_stores,
    export_persistent_api_retention_plan,
    persistent_api_store_status,
    restore_persistent_api_backup,
)
from cavra.phase6_rollup import (
    build_phase6_rollup_packet,
    validate_phase6_rollup_packet,
    write_phase6_rollup_artifacts,
)
from cavra.phase4_closeout import (
    build_phase4_closeout_packet,
    validate_phase4_closeout_packet,
    write_phase4_closeout_artifacts,
)
from cavra.phase5_closeout import (
    build_phase5_closeout_packet,
    validate_phase5_closeout_packet,
    write_phase5_closeout_artifacts,
)
from cavra.managed_enterprise_live_validation_plan import (
    build_managed_enterprise_live_validation_plan,
    validate_managed_enterprise_live_validation_plan,
    write_managed_enterprise_live_validation_plan_artifacts,
)
from cavra.managed_enterprise_cutover_runbook import (
    build_managed_enterprise_cutover_runbook,
    validate_managed_enterprise_cutover_runbook,
    write_managed_enterprise_cutover_runbook_artifacts,
)
from cavra.managed_enterprise_stabilization_report import (
    build_managed_enterprise_stabilization_report,
    validate_managed_enterprise_stabilization_report,
    write_managed_enterprise_stabilization_report_artifacts,
)
from cavra.managed_enterprise_steady_state_handoff import (
    build_managed_enterprise_steady_state_handoff,
    validate_managed_enterprise_steady_state_handoff,
    write_managed_enterprise_steady_state_handoff_artifacts,
)
from cavra.managed_enterprise_operating_release_index import (
    build_managed_enterprise_operating_release_index,
    validate_managed_enterprise_operating_release_index,
    write_managed_enterprise_operating_release_index_artifacts,
)
from cavra.managed_enterprise_operating_announcement import (
    build_managed_enterprise_operating_announcement,
    validate_managed_enterprise_operating_announcement,
    write_managed_enterprise_operating_announcement_artifacts,
)
from cavra.managed_enterprise_operating_chain import (
    build_managed_enterprise_operating_chain_manifest,
    validate_managed_enterprise_operating_chain,
    write_managed_enterprise_operating_chain_artifacts,
)
from cavra.managed_enterprise_operating_certificate import (
    build_managed_enterprise_operating_certificate,
    validate_managed_enterprise_operating_certificate,
    write_managed_enterprise_operating_certificate_artifacts,
)
from cavra.managed_enterprise_certificate_publication_index import (
    build_managed_enterprise_certificate_publication_index,
    validate_managed_enterprise_certificate_publication_index,
    write_managed_enterprise_certificate_publication_index_artifacts,
)
from cavra.roadmap_intake_gate import (
    build_roadmap_intake_gate_packet,
    validate_roadmap_intake_gate_packet,
    write_roadmap_intake_gate_artifacts,
)
from cavra.roadmap_candidate_charter import (
    build_roadmap_candidate_charter,
    validate_roadmap_candidate_charter,
    write_roadmap_candidate_charter_artifacts,
)
from cavra.roadmap_future_phase_opening_gate import (
    build_roadmap_future_phase_opening_gate,
    validate_roadmap_future_phase_opening_gate,
    write_roadmap_future_phase_opening_gate_artifacts,
)
from cavra.roadmap_future_phase_registry import (
    build_roadmap_future_phase_registry,
    validate_roadmap_future_phase_registry,
    write_roadmap_future_phase_registry_artifacts,
)
from cavra.policy_engine import (
    compile_policy as compile_policy_payload,
    diff_policies,
    generate_policy_signing_keypair,
    load_policy_file,
    validate_policy as validate_policy_payload,
    verify_policy_signature,
    write_policy_signature,
)
from cavra.opa_rego_policy import (
    build_rego_policy_bundle,
    run_rego_parity_report,
    validate_opa_rego_policy_packet,
    write_rego_bundle,
)
from cavra.policy_lifecycle import (
    build_policy_lifecycle_plan,
    validate_policy_lifecycle_packet,
    write_policy_lifecycle_artifacts,
)
from cavra.policy_registry import PolicyRegistry
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
    build_endpoint_management_export_metadata,
    build_endpoint_inventory_freshness_dashboard,
    build_endpoint_inventory_freshness_metadata,
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
    build_endpoint_inventory_ingestion_dashboard,
    build_endpoint_inventory_ingestion_metadata,
    build_endpoint_reconciliation_automation_dashboard,
    build_endpoint_reconciliation_automation_metadata,
    build_managed_endpoint_reconciliation_dashboard,
    build_managed_endpoint_reconciliation_metadata,
    build_managed_endpoint_rollout_rollback_execution_metadata,
    build_managed_endpoint_rollout_promotion_execution_metadata,
    build_release_channel_promotion_request_metadata,
    build_rollout_promotion_execution_audit_event,
    build_rollout_rollback_execution_audit_event,
    create_managed_endpoint_rollout_rollback_execution,
    capture_managed_endpoint_rollout_evidence,
    create_release_channel_promotion_request,
    create_managed_endpoint_rollout_promotion_request,
    create_managed_endpoint_rollout_promotion_execution,
    create_endpoint_drift_remediation_request,
    acknowledge_endpoint_remediation_sla_escalation_recurrence_automation_health_alert,
    acknowledge_endpoint_remediation_sla_notification,
    execute_endpoint_drift_remediation,
    export_endpoint_remediation_sla_escalation_suppression_audit,
    export_endpoint_management_bundles,
    export_rollout_promotion_execution_audit,
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
    load_release_channel_manifest,
    review_endpoint_remediation_sla_escalation,
    load_workstation_updater_policy,
    reconcile_managed_endpoint_deployment,
    record_endpoint_remediation_handoff_status,
    verify_managed_endpoint_rollout_evidence,
    smoke_test_go_installers,
    validate_go_release_upgrade,
    verify_go_airgap_bundle,
    verify_go_release_package,
)
from cavra.runtime import RuntimeGuard, summarize_policy_mode

console = Console()
app = typer.Typer(add_completion=False)
agent_app = typer.Typer(help="AI agent runtime commands.")
policy_app = typer.Typer(help="Policy registry commands.")
demo_app = typer.Typer(help="Runnable CAVRA demos.")
init_app = typer.Typer(help="Initialize CAVRA integrations.")
integration_app = typer.Typer(help="Enterprise connector delivery commands.")
evidence_app = typer.Typer(help="Evidence bundle commands.")
approval_app = typer.Typer(help="Human approval router commands.")
registry_app = typer.Typer(help="Agent and MCP trust registry commands.")
ops_app = typer.Typer(help="Persistent API operations commands.")
release_app = typer.Typer(help="Release package verification commands.")
runtime_app = typer.Typer(help="Runtime backend pilot commands.")
saas_app = typer.Typer(help="Public-safe SaaS Control Plane contract commands.")
aispm_app = typer.Typer(help="AI Security Posture Management commands.")
monitor_app = typer.Typer(help="Continuous monitoring event commands.")
benchmark_app = typer.Typer(help="Benchmark and SLO regression commands.")
adapter_app = typer.Typer(help="Generic agent adapter and action taxonomy commands.")
ai_red_team_app = typer.Typer(help="Native AI red-team, guardrail, and supply-chain commands.")
deployment_app = typer.Typer(help="Reference deployment and zero-trust packaging commands.")
app.add_typer(agent_app, name="agent")
app.add_typer(policy_app, name="policy")
app.add_typer(demo_app, name="demo")
app.add_typer(init_app, name="init")
app.add_typer(integration_app, name="integration")
app.add_typer(evidence_app, name="evidence")
app.add_typer(approval_app, name="approval")
app.add_typer(registry_app, name="registry")
app.add_typer(ops_app, name="ops")
app.add_typer(release_app, name="release")
app.add_typer(runtime_app, name="runtime")
app.add_typer(saas_app, name="saas")
app.add_typer(aispm_app, name="aispm")
app.add_typer(monitor_app, name="monitor")
app.add_typer(benchmark_app, name="benchmark")
app.add_typer(adapter_app, name="adapter")
app.add_typer(ai_red_team_app, name="ai-red-team")
app.add_typer(deployment_app, name="deployment")


@app.command()
def version() -> None:
    typer.echo(f"cavra {__version__}")


@ai_red_team_app.command("guardrails")
def ai_red_team_guardrails(
    suite: Annotated[Optional[Path], typer.Option(help="Optional guardrail test suite JSON.")] = None,
) -> None:
    """Run native LLM guardrail tests."""
    payload = json.loads(suite.read_text(encoding="utf-8")) if suite else build_guardrail_test_suite()
    result = run_guardrail_test_suite(payload)
    console.print(JSON(json.dumps(result, indent=2)))
    if not result["passed"]:
        raise typer.Exit(code=1)


@ai_red_team_app.command("supply-chain")
def ai_red_team_supply_chain(
    artifact: Annotated[Optional[Path], typer.Option(help="Optional AI artifact metadata JSON.")] = None,
) -> None:
    """Validate AI artifact supply-chain metadata."""
    payload = json.loads(artifact.read_text(encoding="utf-8")) if artifact else build_sample_ai_artifact_metadata()
    result = validate_ai_supply_chain_metadata(payload)
    console.print(JSON(json.dumps(result, indent=2)))
    if not result["valid"]:
        raise typer.Exit(code=1)


@ai_red_team_app.command("malicious-model")
def ai_red_team_malicious_model(
    artifact: Annotated[Optional[Path], typer.Option(help="Optional AI artifact metadata JSON.")] = None,
) -> None:
    """Run malicious model checks against AI artifact metadata."""
    payload = json.loads(artifact.read_text(encoding="utf-8")) if artifact else build_sample_ai_artifact_metadata()
    result = run_malicious_model_checks(payload)
    console.print(JSON(json.dumps(result, indent=2)))
    if not result["passed"]:
        raise typer.Exit(code=1)


@ai_red_team_app.command("export")
def ai_red_team_export(
    output_dir: Annotated[Path, typer.Option(help="Directory for AI red-team artifacts.")] = Path("dist/ai-red-team"),
) -> None:
    """Export native AI red-team, supply-chain, malicious-model, and readiness artifacts."""
    result = write_ai_red_team_artifacts(output_dir)
    console.print(JSON(json.dumps(result, indent=2)))


@ai_red_team_app.command("readiness")
def ai_red_team_readiness(
    packet: Annotated[Path, typer.Argument(help="AI red-team readiness packet JSON.")],
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live.")] = False,
) -> None:
    """Validate an AI red-team readiness packet."""
    payload = json.loads(packet.read_text(encoding="utf-8"))
    result = validate_ai_red_team_readiness_packet(payload, require_live=require_live)
    console.print(JSON(json.dumps(result, indent=2)))
    if result["blocker_count"] or (require_live and not result["ready_for_live_ai_red_team_gate"]):
        raise typer.Exit(code=1)


@ai_red_team_app.command("packet")
def ai_red_team_packet(
    evidence_mode: Annotated[str, typer.Option(help="Evidence mode for generated packet.")] = "sample",
) -> None:
    """Emit a generated AI red-team readiness packet."""
    suite = build_guardrail_test_suite()
    run_report = run_guardrail_test_suite(suite)
    artifact = build_sample_ai_artifact_metadata()
    scan = validate_ai_supply_chain_metadata(artifact)
    malicious = run_malicious_model_checks(artifact)
    packet = build_ai_red_team_readiness_packet(suite, run_report, scan, malicious, evidence_mode=evidence_mode)
    console.print(JSON(json.dumps(packet, indent=2)))


@adapter_app.command("taxonomy")
def adapter_taxonomy(
    output: Annotated[Optional[Path], typer.Option(help="Optional JSON output path.")] = None,
) -> None:
    """Emit the public generic action taxonomy."""
    taxonomy = build_action_taxonomy()
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(taxonomy, indent=2) + "\n", encoding="utf-8")
        console.print(f"[green]written[/green] {output}")
        return
    console.print(JSON(json.dumps(taxonomy, indent=2)))


@adapter_app.command("manifest-validate")
def adapter_manifest_validate(
    manifest: Annotated[Path, typer.Argument(help="Generic adapter manifest JSON.")],
) -> None:
    """Validate a generic adapter manifest."""
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    result = validate_adapter_manifest(payload)
    console.print(JSON(json.dumps(result, indent=2)))
    if not result["valid"]:
        raise typer.Exit(code=1)


@adapter_app.command("evaluate")
def adapter_evaluate(
    actions: Annotated[Path, typer.Argument(help="Generic agent actions JSON.")],
    policy_pack: Annotated[str, typer.Option(help="CAVRA policy pack used for runtime-compatible actions.")] = (
        "cavra-ai-agent-baseline"
    ),
) -> None:
    """Evaluate generic non-coding agent actions through the CAVRA taxonomy."""
    payload = json.loads(actions.read_text(encoding="utf-8"))
    action_items = payload.get("actions", payload) if isinstance(payload, dict) else payload
    result = evaluate_generic_actions(action_items, policy_pack=policy_pack)
    console.print(JSON(json.dumps(result, indent=2)))
    counts = result["decision_counts"]
    if not (counts.get("allow", 0) >= 1 and counts.get("require_approval", 0) >= 1 and counts.get("block", 0) >= 1):
        raise typer.Exit(code=1)


@adapter_app.command("export")
def adapter_export(
    output_dir: Annotated[Path, typer.Option(help="Directory for generic adapter artifacts.")] = Path(
        "dist/generic-agent-adapter"
    ),
) -> None:
    """Export reference generic adapter taxonomy, manifest, scenario, evaluation, and packet artifacts."""
    result = write_generic_adapter_artifacts(
        build_sample_adapter_manifest(),
        build_sample_generic_actions(),
        output_dir,
    )
    console.print(JSON(json.dumps(result, indent=2)))


@adapter_app.command("readiness")
def adapter_readiness(
    packet: Annotated[Path, typer.Argument(help="Generic adapter readiness packet JSON.")],
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live.")] = False,
) -> None:
    """Validate a generic adapter readiness packet."""
    payload = json.loads(packet.read_text(encoding="utf-8"))
    result = validate_generic_adapter_readiness_packet(payload, require_live=require_live)
    console.print(JSON(json.dumps(result, indent=2)))
    if result["blocker_count"] or (require_live and not result["ready_for_live_generic_adapter_sdk"]):
        raise typer.Exit(code=1)


@deployment_app.command("zero-trust-catalog")
def deployment_zero_trust_catalog(
    repo_root: Annotated[Optional[Path], typer.Option(help="Repository root for file marker validation.")] = None,
) -> None:
    """Emit and validate the zero-trust reference deployment catalog."""
    catalog = build_reference_deployment_catalog()
    result = validate_reference_deployment_catalog(catalog, repo_root=repo_root)
    print(json.dumps({"catalog": catalog, "validation": result}, indent=2))
    if result["blocker_count"]:
        raise typer.Exit(code=1)


@deployment_app.command("zero-trust-export")
def deployment_zero_trust_export(
    output_dir: Annotated[Path, typer.Option(help="Directory for generated reference deployment artifacts.")] = Path(
        "dist/zero-trust-reference-deployments"
    ),
) -> None:
    """Export zero-trust reference deployment catalog and readiness packets."""
    result = write_reference_deployment_artifacts(output_dir)
    print(json.dumps(result, indent=2))


@deployment_app.command("zero-trust-readiness")
def deployment_zero_trust_readiness(
    packet: Annotated[Path, typer.Argument(help="Zero-trust reference deployment readiness packet JSON.")],
    repo_root: Annotated[Optional[Path], typer.Option(help="Repository root for file marker validation.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live.")] = False,
) -> None:
    """Validate a zero-trust reference deployment readiness packet."""
    payload = json.loads(packet.read_text(encoding="utf-8"))
    result = validate_reference_deployment_readiness_packet(payload, repo_root=repo_root, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_live_zero_trust_reference_deployments"]):
        raise typer.Exit(code=1)


@benchmark_app.command("export")
def benchmark_export(
    output_dir: Annotated[Path, typer.Option(help="Directory for benchmark artifacts.")] = Path("dist/benchmark-slo"),
    measured: Annotated[bool, typer.Option(help="Run a measured local benchmark instead of reference fixtures.")] = False,
    iterations: Annotated[int, typer.Option(help="Iterations for measured benchmark mode.")] = 25,
    evidence_mode: Annotated[str, typer.Option(help="Evidence mode for generated readiness packet.")] = "sample",
) -> None:
    """Export benchmark, SLO gate, and readiness artifacts."""
    report = run_local_benchmark_report(iterations) if measured else build_reference_benchmark_report()
    packet = build_benchmark_readiness_packet(report, evidence_mode=evidence_mode)
    result = write_benchmark_artifacts(report, packet, output_dir)
    console.print(JSON(json.dumps(result, indent=2)))
    if not report.get("regression_gate", {}).get("passed"):
        raise typer.Exit(code=1)


@benchmark_app.command("run")
def benchmark_run(
    measured: Annotated[bool, typer.Option(help="Run a measured local benchmark instead of reference fixtures.")] = False,
    iterations: Annotated[int, typer.Option(help="Iterations for measured benchmark mode.")] = 25,
) -> None:
    """Run or emit the benchmark/SLO report and fail when the gate has blockers."""
    report = run_local_benchmark_report(iterations) if measured else build_reference_benchmark_report()
    console.print(JSON(json.dumps(report, indent=2)))
    if not report.get("regression_gate", {}).get("passed"):
        raise typer.Exit(code=1)


@benchmark_app.command("readiness")
def benchmark_readiness(
    packet: Annotated[Path, typer.Argument(help="Benchmark/SLO readiness packet JSON.")],
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live.")] = False,
) -> None:
    """Validate a benchmark/SLO readiness packet."""
    payload = json.loads(packet.read_text(encoding="utf-8"))
    result = validate_benchmark_readiness_packet(payload, require_live=require_live)
    console.print(JSON(json.dumps(result, indent=2)))
    if result["blocker_count"] or (require_live and not result["ready_for_live_benchmark_slo_gate"]):
        raise typer.Exit(code=1)


@monitor_app.command("sample-events")
def monitor_sample_events(
    output: Annotated[Optional[Path], typer.Option(help="Optional JSON output path.")] = None,
) -> None:
    """Emit deterministic sample continuous monitoring events."""
    events = build_sample_monitoring_events()
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
        console.print(f"[green]written[/green] {output}")
        return
    console.print(JSON(json.dumps(events, indent=2)))


@monitor_app.command("replay")
def monitor_replay(
    events: Annotated[Path, typer.Argument(help="Continuous monitoring events JSON.")],
    now: Annotated[str, typer.Option(help="ISO-8601 timestamp used for stale assessment.")] = DEFAULT_BASE_TIME,
    latency_slo_ms: Annotated[int, typer.Option(help="Event latency SLO in milliseconds.")] = 5000,
    stale_after_minutes: Annotated[int, typer.Option(help="Stale assessment threshold in minutes.")] = 60,
) -> None:
    """Replay continuous monitoring events and report dedupe, latency, and freshness."""
    payload = json.loads(events.read_text(encoding="utf-8"))
    event_items = payload.get("events", payload) if isinstance(payload, dict) else payload
    result = replay_monitoring_events(
        event_items,
        now=now,
        latency_slo_ms=latency_slo_ms,
        stale_after_minutes=stale_after_minutes,
    )
    console.print(JSON(json.dumps(result, indent=2)))
    if (
        not result["required_event_types_present"]
        or result["invalid_event_count"]
        or result["latency_summary"]["violation_count"]
        or result["stale_assessment"]["stale_count"]
    ):
        raise typer.Exit(code=1)


@monitor_app.command("export")
def monitor_export(
    output_dir: Annotated[Path, typer.Option(help="Directory for event, replay, and readiness artifacts.")] = Path(
        "dist/continuous-monitoring"
    ),
    evidence_mode: Annotated[str, typer.Option(help="Evidence mode for generated readiness packet.")] = "sample",
) -> None:
    """Export sample continuous monitoring artifacts."""
    events = build_sample_monitoring_events()
    replay = replay_monitoring_events(events)
    packet = build_continuous_monitoring_readiness_packet(replay, evidence_mode=evidence_mode)
    result = write_continuous_monitoring_artifacts(
        events=events,
        replay_report=replay,
        readiness_packet=packet,
        output_dir=output_dir,
    )
    console.print(JSON(json.dumps(result, indent=2)))


@monitor_app.command("readiness")
def monitor_readiness(
    packet: Annotated[Path, typer.Argument(help="Continuous monitoring readiness packet JSON.")],
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live.")] = False,
) -> None:
    """Validate a continuous monitoring readiness packet."""
    payload = json.loads(packet.read_text(encoding="utf-8"))
    result = validate_continuous_monitoring_packet(payload, require_live=require_live)
    console.print(JSON(json.dumps(result, indent=2)))
    if result["blocker_count"] or (require_live and not result["ready_for_live_continuous_monitoring"]):
        raise typer.Exit(code=1)


@aispm_app.command("validate-review-packet")
def validate_aispm_review_packet(
    path: Annotated[Path, typer.Argument(help="Path to cavra-replay-policy-review-packet.json.")],
    json_output: bool = typer.Option(False, "--json", help="Print the validation report JSON."),
) -> None:
    """Validate an AISPM replay-to-policy review packet before PR attachment."""
    report = validate_aispm_replay_to_policy_review_packet_file(path)
    if json_output:
        typer.echo(json.dumps(report, indent=2))
    elif report["valid"]:
        console.print(f"[green]valid[/green] {path}")
    else:
        console.print(f"[red]invalid[/red] {path}")
        for error in report["errors"]:
            console.print(f"  - {error['path']}: {error['message']}")
    if not report["valid"]:
        raise typer.Exit(code=1)


@aispm_app.command("validate-ci-gate-readiness")
def validate_aispm_ci_gate_readiness(
    path: Annotated[Path, typer.Argument(help="Path to cavra-replay-policy-ci-gate-readiness.json.")],
    repo_root: Annotated[
        Optional[Path],
        typer.Option("--repo-root", help="Optional repository root to verify referenced CI template files."),
    ] = None,
    json_output: bool = typer.Option(False, "--json", help="Print the validation report JSON."),
) -> None:
    """Validate AISPM replay-to-policy CI gate readiness before production use."""
    report = validate_aispm_replay_to_policy_ci_gate_readiness_file(path, repo_root=repo_root)
    if json_output:
        typer.echo(json.dumps(report, indent=2))
    elif report["valid"]:
        console.print(f"[green]valid[/green] {path}")
    else:
        console.print(f"[red]invalid[/red] {path}")
        for error in report["errors"]:
            console.print(f"  - {error['path']}: {error['message']}")
    if not report["valid"]:
        raise typer.Exit(code=1)


@app.command()
def evaluate(
    action_type: Annotated[str, typer.Argument(help="read_file, write_file, execute_command, git_operation, mcp_tool_call.")],
    target: Annotated[str, typer.Argument(help="File path, command, Git target, or MCP server.")],
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline",
    policy_mode: Annotated[
        str, typer.Option(help="Runtime policy mode: audit_only, enforce, strict, or break_glass.")
    ] = "enforce",
    break_glass_reason: Annotated[Optional[str], typer.Option(help="Required reason when --policy-mode break_glass.")] = None,
    break_glass_actor: Annotated[Optional[str], typer.Option(help="Required actor when --policy-mode break_glass.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print the full decision JSON."),
) -> None:
    """Evaluate one action before an AI agent performs it."""
    guard = RuntimeGuard(policy_pack=policy_pack)
    if action_type == "read_file":
        decision = guard.evaluate_file_access(Path(target), "read")
    elif action_type == "write_file":
        decision = guard.evaluate_file_access(Path(target), "write")
    elif action_type == "execute_command":
        decision = guard.evaluate_command(target)
    elif action_type == "git_operation":
        decision = guard.evaluate_git_action("push", target)
    elif action_type == "mcp_tool_call":
        decision = guard.evaluate_mcp_tool_call(target, "unknown", "filesystem")
    else:
        console.print(f"[red]Unknown action type:[/red] {action_type}")
        raise typer.Exit(code=2)
    try:
        mode_summary = summarize_policy_mode(
            decision,
            policy_mode,
            break_glass_reason=break_glass_reason,
            break_glass_actor=break_glass_actor,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    if json_output:
        _print_json(mode_summary)
    else:
        console.print(f"{mode_summary['effective_decision']}: {mode_summary['mode_reason']}")


@saas_app.command("contract")
def saas_contract() -> None:
    """Print the public-safe SaaS Control Plane contract description."""

    _print_json(describe_public_contract())


@saas_app.command("operating-automation")
def saas_operating_automation(
    tenant_id: Annotated[str, typer.Argument(help="Tenant identifier for the public-safe request shape.")],
    requested_by: Annotated[str, typer.Option(help="Actor or surface requesting the handoff.")] = "community",
    automation_scope: Annotated[str, typer.Option(help="Public-safe automation scope.")] = "trial-to-paid-customer-scale",
    automation_cadence: Annotated[str, typer.Option(help="Public-safe automation cadence.")] = "daily",
    required_check: Annotated[
        Optional[list[str]],
        typer.Option("--required-check", help="Required public-safe operating automation check."),
    ] = None,
    automation_status: Annotated[str, typer.Option(help="ready, scheduled, enabled, automated, blocked, or unknown.")] = "unknown",
    billing_monitoring_status: Annotated[str, typer.Option(help="Billing monitoring status.")] = "unknown",
    license_telemetry_status: Annotated[str, typer.Option(help="License telemetry sync status.")] = "unknown",
    support_followup_status: Annotated[str, typer.Option(help="Support follow-up status.")] = "unknown",
    customer_success_review_status: Annotated[str, typer.Option(help="Customer-success review status.")] = "unknown",
    dashboard_refresh_status: Annotated[str, typer.Option(help="Dashboard refresh status.")] = "unknown",
    escalation_drill_status: Annotated[str, typer.Option(help="Escalation drill status.")] = "unknown",
    closeout_retry_status: Annotated[str, typer.Option(help="Closeout retry status.")] = "unknown",
    blocker: Annotated[Optional[list[str]], typer.Option("--blocker", help="Public-safe blocker summary.")] = None,
) -> None:
    """Print a public-safe SaaS operating automation request and placeholder response."""

    try:
        request = build_saas_operating_automation_request(
            tenant_id,
            requested_by=requested_by,
            automation_scope=automation_scope,
            automation_cadence=automation_cadence,
            required_checks=tuple(required_check) if required_check is not None else SAAS_OPERATING_AUTOMATION_CHECKS,
        )
        summary = SaaSOperatingAutomationSummary(
            tenant_id=request.tenant_id,
            automation_status=automation_status,
            billing_monitoring_status=billing_monitoring_status,
            license_telemetry_status=license_telemetry_status,
            support_followup_status=support_followup_status,
            customer_success_review_status=customer_success_review_status,
            dashboard_refresh_status=dashboard_refresh_status,
            escalation_drill_status=escalation_drill_status,
            closeout_retry_status=closeout_retry_status,
            automation_scope=automation_scope,
            automation_cadence=automation_cadence,
            blockers=tuple(blocker or ()),
        )
        response = build_saas_operating_automation_response(request, summary)
    except SaaSContractError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    _print_json({"request": request.to_dict(), "response": response.to_dict()})


@saas_app.command("worker-handoff")
def saas_worker_handoff(
    tenant_id: Annotated[str, typer.Argument(help="Tenant identifier for the public-safe handoff shape.")],
    requested_by: Annotated[str, typer.Option(help="Actor or surface requesting the handoff.")] = "community",
    deployment_environment: Annotated[str, typer.Option(help="Public-safe deployment environment label.")] = "production",
    worker_mode: Annotated[str, typer.Option(help="dry_run, shadow, live, or unknown.")] = "dry_run",
    required_check: Annotated[
        Optional[list[str]],
        typer.Option("--required-check", help="Required public-safe operating automation check."),
    ] = None,
    worker_target: Annotated[
        Optional[list[str]],
        typer.Option("--worker-target", help="Public-safe worker target name."),
    ] = None,
    handoff_status: Annotated[
        str,
        typer.Option(help="planned, ready, blocked, requires_private_service, or unknown."),
    ] = "requires_private_service",
    scheduler_ref: Annotated[str, typer.Option(help="Public-safe scheduler reference label.")] = "scheduler-pending",
    evidence_sink_ref: Annotated[
        str,
        typer.Option(help="Public-safe evidence sink reference label."),
    ] = "evidence-sink-pending",
    retry_policy_ref: Annotated[
        str,
        typer.Option(help="Public-safe retry policy reference label."),
    ] = "retry-policy-pending",
    worker_owner: Annotated[str, typer.Option(help="Public-safe worker owner role or team.")] = "operations-owner",
    blocker: Annotated[Optional[list[str]], typer.Option("--blocker", help="Public-safe blocker summary.")] = None,
) -> None:
    """Print a public-safe SaaS operating automation worker handoff request and response."""

    try:
        request = build_saas_operating_automation_worker_handoff_request(
            tenant_id,
            requested_by=requested_by,
            deployment_environment=deployment_environment,
            worker_mode=worker_mode,
            required_checks=tuple(required_check) if required_check is not None else SAAS_OPERATING_AUTOMATION_CHECKS,
            worker_targets=tuple(worker_target) if worker_target is not None else SAAS_OPERATING_AUTOMATION_CHECKS,
        )
        summary = SaaSOperatingAutomationWorkerHandoffSummary(
            tenant_id=request.tenant_id,
            handoff_status=handoff_status,
            deployment_environment=deployment_environment,
            scheduler_ref=scheduler_ref,
            evidence_sink_ref=evidence_sink_ref,
            retry_policy_ref=retry_policy_ref,
            worker_owner=worker_owner,
            worker_mode=worker_mode,
            required_checks=tuple(required_check) if required_check is not None else SAAS_OPERATING_AUTOMATION_CHECKS,
            worker_targets=tuple(worker_target) if worker_target is not None else SAAS_OPERATING_AUTOMATION_CHECKS,
            blockers=tuple(blocker or ()),
        )
        response = build_saas_operating_automation_worker_handoff_response(request, summary)
    except SaaSContractError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    _print_json({"request": request.to_dict(), "response": response.to_dict()})


@runtime_app.command("go-pilot-readiness")
def runtime_go_pilot_readiness(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    runtime_path: Annotated[str, typer.Option(help="Path to the cavra-runtime binary.")] = "",
    policy_path: Annotated[str, typer.Option(help="Path to compiled policy JSON.")] = "",
    registry_path: Annotated[str, typer.Option(help="Optional trust registry JSON path.")] = "",
    package_dir: Annotated[str, typer.Option(help="Optional verified Go runtime release package directory.")] = "",
    endpoint_deployment_path: Annotated[str, typer.Option(help="Optional endpoint deployment manifest path.")] = "",
    ci_runner_bundles_path: Annotated[str, typer.Option(help="Optional CI runner bundles manifest path.")] = "",
    channel_manifest_path: Annotated[str, typer.Option(help="Optional workstation release channel manifest path.")] = "",
    updater_policy_path: Annotated[str, typer.Option(help="Optional workstation updater policy path.")] = "",
    promotion_evidence_path: Annotated[str, typer.Option(help="Optional Go promotion evidence JSON path.")] = "",
    rollback_plan_path: Annotated[str, typer.Option(help="Optional Go rollback plan JSON path.")] = "",
    rollback_rehearsal_path: Annotated[str, typer.Option(help="Optional Go rollback rehearsal evidence JSON path.")] = "",
    rollback_drill_history_path: Annotated[str, typer.Option(help="Optional Go rollback drill history JSON path.")] = "",
    rollback_drill_max_age_days: Annotated[float, typer.Option(help="Maximum accepted age for the latest rollback drill.")] = 90.0,
    timeout_seconds: Annotated[float, typer.Option(help="Go runtime invocation timeout in seconds.")] = 5.0,
    json_output: bool = typer.Option(False, "--json", help="Print readiness JSON."),
) -> None:
    """Show opt-in Go backend pilot readiness."""
    config = GoBackendConfig(
        mode=mode,
        runtime_path=runtime_path,
        policy_path=policy_path,
        registry_path=registry_path,
        package_dir=package_dir,
        endpoint_deployment_path=endpoint_deployment_path,
        ci_runner_bundles_path=ci_runner_bundles_path,
        channel_manifest_path=channel_manifest_path,
        updater_policy_path=updater_policy_path,
        promotion_evidence_path=promotion_evidence_path,
        rollback_plan_path=rollback_plan_path,
        rollback_rehearsal_path=rollback_rehearsal_path,
        rollback_drill_history_path=rollback_drill_history_path,
        rollback_drill_max_age_days=rollback_drill_max_age_days,
        timeout_seconds=timeout_seconds,
    )
    report = go_backend_readiness_report(config)
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return
    console.print(f"Go backend pilot: {report['status']} ({report['mode']})")
    for check in report["checks"]:
        console.print(f"  {check['status']} {check['id']}: {check['message']}")


@runtime_app.command("go-deployment-readiness")
def runtime_go_deployment_readiness(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    package_dir: Annotated[str, typer.Option(help="Verified Go runtime release package directory.")] = "",
    endpoint_deployment_path: Annotated[str, typer.Option(help="Endpoint deployment manifest path.")] = "",
    ci_runner_bundles_path: Annotated[str, typer.Option(help="CI runner bundles manifest path.")] = "",
    channel_manifest_path: Annotated[str, typer.Option(help="Workstation release channel manifest path.")] = "",
    updater_policy_path: Annotated[str, typer.Option(help="Workstation updater policy path.")] = "",
    json_output: bool = typer.Option(False, "--json", help="Print deployment readiness JSON."),
) -> None:
    """Show Go backend CI runner and workstation deployment readiness."""
    config = GoBackendConfig(
        mode=mode,
        package_dir=package_dir,
        endpoint_deployment_path=endpoint_deployment_path,
        ci_runner_bundles_path=ci_runner_bundles_path,
        channel_manifest_path=channel_manifest_path,
        updater_policy_path=updater_policy_path,
    )
    report = go_deployment_readiness_report(config)
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return
    console.print(f"Go deployment readiness: {report['status']} ({report['mode']})")
    for check in report["checks"]:
        console.print(f"  {check['status']} {check['id']}: {check['message']}")


@runtime_app.command("go-promotion-readiness")
def runtime_go_promotion_readiness(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    runtime_path: Annotated[str, typer.Option(help="Path to the cavra-runtime binary.")] = "",
    policy_path: Annotated[str, typer.Option(help="Path to compiled policy JSON.")] = "",
    registry_path: Annotated[str, typer.Option(help="Optional trust registry JSON path.")] = "",
    package_dir: Annotated[str, typer.Option(help="Verified Go runtime release package directory.")] = "",
    endpoint_deployment_path: Annotated[str, typer.Option(help="Endpoint deployment manifest path.")] = "",
    ci_runner_bundles_path: Annotated[str, typer.Option(help="CI runner bundles manifest path.")] = "",
    channel_manifest_path: Annotated[str, typer.Option(help="Workstation release channel manifest path.")] = "",
    updater_policy_path: Annotated[str, typer.Option(help="Workstation updater policy path.")] = "",
    promotion_evidence_path: Annotated[str, typer.Option(help="Audited Go promotion evidence JSON path.")] = "",
    rollback_plan_path: Annotated[str, typer.Option(help="Optional Go rollback plan JSON path.")] = "",
    rollback_rehearsal_path: Annotated[str, typer.Option(help="Optional Go rollback rehearsal evidence JSON path.")] = "",
    rollback_drill_history_path: Annotated[str, typer.Option(help="Optional Go rollback drill history JSON path.")] = "",
    rollback_drill_max_age_days: Annotated[float, typer.Option(help="Maximum accepted age for the latest rollback drill.")] = 90.0,
    timeout_seconds: Annotated[float, typer.Option(help="Go runtime invocation timeout in seconds.")] = 5.0,
    json_output: bool = typer.Option(False, "--json", help="Print promotion readiness JSON."),
) -> None:
    """Show Go backend promotion readiness for optional backend use."""
    config = GoBackendConfig(
        mode=mode,
        runtime_path=runtime_path,
        policy_path=policy_path,
        registry_path=registry_path,
        package_dir=package_dir,
        endpoint_deployment_path=endpoint_deployment_path,
        ci_runner_bundles_path=ci_runner_bundles_path,
        channel_manifest_path=channel_manifest_path,
        updater_policy_path=updater_policy_path,
        promotion_evidence_path=promotion_evidence_path,
        rollback_plan_path=rollback_plan_path,
        rollback_rehearsal_path=rollback_rehearsal_path,
        rollback_drill_history_path=rollback_drill_history_path,
        rollback_drill_max_age_days=rollback_drill_max_age_days,
        timeout_seconds=timeout_seconds,
    )
    report = go_promotion_readiness_report(config)
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return
    console.print(f"Go promotion readiness: {report['status']} ({report['mode']})")
    for check in report["checks"]:
        console.print(f"  {check['status']} {check['id']}: {check['message']}")


@runtime_app.command("go-rollback-readiness")
def runtime_go_rollback_readiness(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    rollback_plan_path: Annotated[str, typer.Option(help="Approved Go rollback plan JSON path.")] = "",
    rollback_rehearsal_path: Annotated[str, typer.Option(help="Optional Go rollback rehearsal evidence JSON path.")] = "",
    json_output: bool = typer.Option(False, "--json", help="Print rollback readiness JSON."),
) -> None:
    """Show Go backend rollback readiness for promoted pilots."""
    report = go_rollback_readiness_report(
        GoBackendConfig(
            mode=mode,
            rollback_plan_path=rollback_plan_path,
            rollback_rehearsal_path=rollback_rehearsal_path,
        )
    )
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return
    console.print(f"Go rollback readiness: {report['status']} ({report['mode']})")
    for check in report["checks"]:
        console.print(f"  {check['status']} {check['id']}: {check['message']}")


@runtime_app.command("go-rollback-rehearsal")
def runtime_go_rollback_rehearsal(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    rollback_plan_path: Annotated[str, typer.Option(help="Approved Go rollback plan JSON path.")] = "",
    rollback_rehearsal_path: Annotated[str, typer.Option(help="Go rollback rehearsal evidence JSON path.")] = "",
    rollback_drill_history_path: Annotated[str, typer.Option(help="Optional Go rollback drill history JSON path.")] = "",
    rollback_drill_max_age_days: Annotated[float, typer.Option(help="Maximum accepted age for the latest rollback drill.")] = 90.0,
    json_output: bool = typer.Option(False, "--json", help="Print rollback rehearsal JSON."),
) -> None:
    """Show automated rollback rehearsal evidence status for promoted Go pilots."""
    report = go_rollback_rehearsal_report(
        GoBackendConfig(
            mode=mode,
            rollback_plan_path=rollback_plan_path,
            rollback_rehearsal_path=rollback_rehearsal_path,
            rollback_drill_history_path=rollback_drill_history_path,
            rollback_drill_max_age_days=rollback_drill_max_age_days,
        )
    )
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return
    console.print(f"Go rollback rehearsal: {report['status']} ({report['mode']})")
    for check in report["checks"]:
        console.print(f"  {check['status']} {check['id']}: {check['message']}")


@runtime_app.command("go-rollback-drills")
def runtime_go_rollback_drills(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    rollback_drill_history_path: Annotated[str, typer.Option(help="Go rollback drill history JSON path.")] = "",
    rollback_drill_max_age_days: Annotated[float, typer.Option(help="Maximum accepted age for the latest rollback drill.")] = 90.0,
    json_output: bool = typer.Option(False, "--json", help="Print rollback drill history JSON."),
) -> None:
    """Show operational rollback drill history status for promoted Go pilots."""
    report = go_rollback_drill_history_report(
        GoBackendConfig(
            mode=mode,
            rollback_drill_history_path=rollback_drill_history_path,
            rollback_drill_max_age_days=rollback_drill_max_age_days,
        )
    )
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return
    console.print(f"Go rollback drills: {report['status']} ({report['mode']})")
    for check in report["checks"]:
        console.print(f"  {check['status']} {check['id']}: {check['message']}")


@runtime_app.command("go-rollback-drill-schedule")
def runtime_go_rollback_drill_schedule(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    rollback_drill_history_path: Annotated[str, typer.Option(help="Go rollback drill history JSON path.")] = "",
    rollback_drill_max_age_days: Annotated[float, typer.Option(help="Maximum accepted age for the latest rollback drill.")] = 90.0,
    rollback_drill_schedule_path: Annotated[str, typer.Option(help="Go rollback drill schedule JSON path.")] = "",
    rollback_drill_due_soon_days: Annotated[float, typer.Option(help="Days before due date to mark drills due soon.")] = 14.0,
    json_output: bool = typer.Option(False, "--json", help="Print rollback drill schedule JSON."),
) -> None:
    """Show recurring rollback drill schedule and stale-drill notification readiness."""
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=mode,
            rollback_drill_history_path=rollback_drill_history_path,
            rollback_drill_max_age_days=rollback_drill_max_age_days,
            rollback_drill_schedule_path=rollback_drill_schedule_path,
            rollback_drill_due_soon_days=rollback_drill_due_soon_days,
        )
    )
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return
    console.print(f"Go rollback drill schedule: {report['status']} ({report['mode']})")
    for check in report["checks"]:
        console.print(f"  {check['status']} {check['id']}: {check['message']}")


@runtime_app.command("go-rollback-drill-notification-plan")
def runtime_go_rollback_drill_notification_plan(
    mode: Annotated[str, typer.Option(help="disabled, shadow, enforce, or promoted.")] = "disabled",
    rollback_drill_history_path: Annotated[str, typer.Option(help="Go rollback drill history JSON path.")] = "",
    rollback_drill_schedule_path: Annotated[str, typer.Option(help="Go rollback drill schedule JSON path.")] = "",
    routing_policy: Annotated[Optional[Path], typer.Option(help="Optional owner routing, calendar, and maintenance window policy JSON/YAML.")] = None,
    provider: Annotated[str, typer.Option(help="Connector provider to select, or all.")] = "all",
    force: Annotated[bool, typer.Option(help="Select providers even when the schedule is healthy.")] = False,
    json_output: bool = typer.Option(False, "--json", help="Print notification plan JSON."),
) -> None:
    """Build a public-safe stale rollback drill notification plan."""
    policy = load_connector_config(routing_policy) if routing_policy else None
    report = go_rollback_drill_schedule_report(
        GoBackendConfig(
            mode=mode,
            rollback_drill_history_path=rollback_drill_history_path,
            rollback_drill_schedule_path=rollback_drill_schedule_path,
        )
    )
    plan = build_go_rollback_drill_notification_plan(
        report,
        requested_provider=provider,
        generated_by="cli",
        force=force,
        routing_policy=policy,
    )
    event = build_go_rollback_drill_notification_event(report, generated_by="cli", routing_policy=policy)
    payload = {"schedule": report, "plan": plan, "event": event}
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return
    console.print(f"Go rollback drill notification plan: {plan['alert_level']} ({plan['reason']})")
    console.print(f"  selected providers: {', '.join(plan['selected_providers']) or 'none'}")


@runtime_app.command("go-rollback-drill-notification-ack")
def runtime_go_rollback_drill_notification_ack(
    schedule_id: Annotated[str, typer.Argument(help="Rollback drill schedule ID.")],
    provider: Annotated[str, typer.Option(help="Notification provider being acknowledged.")] = "",
    acknowledged_by: Annotated[str, typer.Option(help="Actor recording acknowledgement.")] = "",
    acknowledgement_state: Annotated[str, typer.Option(help="acknowledged, dismissed, escalated, or resolved.")] = "acknowledged",
    plan_id: Annotated[str, typer.Option(help="Optional notification plan ID.")] = "",
    external_ref: Annotated[str, typer.Option(help="Optional external ticket/chat reference.")] = "",
    notes: Annotated[str, typer.Option(help="Optional public-safe notes.")] = "",
    json_output: bool = typer.Option(False, "--json", help="Print acknowledgement JSON."),
) -> None:
    """Build public-safe rollback drill notification acknowledgement metadata."""
    acknowledgement = acknowledge_go_rollback_drill_notification(
        schedule_id,
        provider=provider,
        acknowledged_by=acknowledged_by,
        acknowledgement_state=acknowledgement_state,
        external_ref=external_ref,
        notes=notes,
        plan_id=plan_id,
    )
    payload = {
        "acknowledgement": acknowledgement,
        "metadata": build_go_rollback_drill_notification_ack_metadata(acknowledgement),
    }
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return
    console.print(
        f"Go rollback drill notification acknowledgement: {acknowledgement['acknowledgement_state']} "
        f"({acknowledgement['schedule_id']} / {acknowledgement['provider']})"
    )


@runtime_app.command("go-rollback-drill-escalation-plan")
def runtime_go_rollback_drill_escalation_plan(
    acknowledgement_minutes: Annotated[int, typer.Option(help="Minutes before outstanding notifications breach.")] = 60,
    routing_policy: Annotated[Optional[Path], typer.Option(help="Optional owner routing and acknowledgement SLO policy JSON/YAML.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print escalation plan JSON."),
) -> None:
    """Build an empty public-safe rollback drill notification escalation plan template."""
    policy = load_connector_config(routing_policy) if routing_policy else {}
    policy.setdefault("acknowledgement_minutes", acknowledgement_minutes)
    plan = build_go_rollback_drill_notification_escalation_plan(
        [],
        policy=policy,
        generated_by="cli",
    )
    if json_output:
        typer.echo(json.dumps(plan, indent=2))
        return
    console.print(f"Go rollback drill escalation plan: {plan['alert_level']} ({plan['route_count']} routes)")


@runtime_app.command("go-pilot-evaluate")
def runtime_go_pilot_evaluate(
    action_type: Annotated[str, typer.Argument(help="read_file, write_file, execute_command, git_operation, mcp_tool_call.")],
    target: Annotated[str, typer.Argument(help="File path, command, Git target, or MCP server.")],
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline",
    mode: Annotated[str, typer.Option(help="shadow, enforce, or promoted.")] = GO_BACKEND_SHADOW,
    runtime_path: Annotated[str, typer.Option(help="Path to the cavra-runtime binary.")] = "",
    policy_path: Annotated[str, typer.Option(help="Path to compiled policy JSON.")] = "",
    registry_path: Annotated[str, typer.Option(help="Optional trust registry JSON path.")] = "",
    package_dir: Annotated[str, typer.Option(help="Optional verified Go runtime release package directory.")] = "",
    endpoint_deployment_path: Annotated[str, typer.Option(help="Optional endpoint deployment manifest path.")] = "",
    ci_runner_bundles_path: Annotated[str, typer.Option(help="Optional CI runner bundles manifest path.")] = "",
    channel_manifest_path: Annotated[str, typer.Option(help="Optional workstation release channel manifest path.")] = "",
    updater_policy_path: Annotated[str, typer.Option(help="Optional workstation updater policy path.")] = "",
    promotion_evidence_path: Annotated[str, typer.Option(help="Optional audited Go promotion evidence JSON path.")] = "",
    rollback_plan_path: Annotated[str, typer.Option(help="Optional approved Go rollback plan JSON path.")] = "",
    rollback_rehearsal_path: Annotated[str, typer.Option(help="Optional rollback rehearsal evidence JSON path.")] = "",
    rollback_drill_history_path: Annotated[str, typer.Option(help="Optional rollback drill history JSON path.")] = "",
    rollback_drill_max_age_days: Annotated[float, typer.Option(help="Maximum accepted age for the latest rollback drill.")] = 90.0,
    rollback_drill_schedule_path: Annotated[str, typer.Option(help="Optional rollback drill schedule JSON path.")] = "",
    rollback_drill_due_soon_days: Annotated[float, typer.Option(help="Days before due date to mark drills due soon.")] = 14.0,
    timeout_seconds: Annotated[float, typer.Option(help="Go runtime invocation timeout in seconds.")] = 5.0,
    operation: Annotated[str, typer.Option(help="Optional Git operation or requested operation.")] = "",
    tool: Annotated[str, typer.Option(help="MCP tool name for mcp_tool_call.")] = "unknown",
    capability: Annotated[str, typer.Option(help="MCP capability for mcp_tool_call.")] = "",
    json_output: bool = typer.Option(False, "--json", help="Print evaluation JSON."),
) -> None:
    """Evaluate through the opt-in Go backend pilot with Python fallback."""
    if mode not in {GO_BACKEND_SHADOW, GO_BACKEND_ENFORCE, GO_BACKEND_PROMOTED}:
        console.print("[red]mode must be shadow, enforce, or promoted for go-pilot-evaluate[/red]")
        raise typer.Exit(code=2)
    request = {
        "action_type": action_type,
        "target": target,
        "policy_pack": policy_pack,
    }
    if operation:
        request["operation"] = operation
    if action_type == "mcp_tool_call":
        request["server"] = target
        request["tool"] = tool
        request["capability"] = capability
    config = GoBackendConfig(
        mode=mode,
        runtime_path=runtime_path,
        policy_path=policy_path,
        registry_path=registry_path,
        package_dir=package_dir,
        endpoint_deployment_path=endpoint_deployment_path,
        ci_runner_bundles_path=ci_runner_bundles_path,
        channel_manifest_path=channel_manifest_path,
        updater_policy_path=updater_policy_path,
        promotion_evidence_path=promotion_evidence_path,
        rollback_plan_path=rollback_plan_path,
        rollback_rehearsal_path=rollback_rehearsal_path,
        rollback_drill_history_path=rollback_drill_history_path,
        rollback_drill_max_age_days=rollback_drill_max_age_days,
        rollback_drill_schedule_path=rollback_drill_schedule_path,
        rollback_drill_due_soon_days=rollback_drill_due_soon_days,
        timeout_seconds=timeout_seconds,
    )
    result = evaluate_with_go_pilot(request, config=config)
    if json_output:
        typer.echo(json.dumps(result, indent=2))
        return
    effective = result["effective_decision"]
    console.print(
        f"{effective['decision']} via {result['selected_backend']} "
        f"(mode={result['backend_mode']}, fallback={result['fallback_used']})"
    )
    if result.get("fallback_reason"):
        console.print(f"[yellow]{result['fallback_reason']}[/yellow]")


@agent_app.command("start")
def start_agent(
    tool: Annotated[str, typer.Option(help="AI tool identifier, e.g. claude-code.")],
    repo: Annotated[Path, typer.Option(help="Path to the repository/workspace.")] = Path("."),
    policy_pack: Annotated[Optional[str], typer.Option(help="Policy pack ID to use.")] = "cavra-ai-agent-baseline",
    output: Annotated[Path, typer.Option(help="Audit output directory.")] = Path(".cavra"),
) -> None:
    """Start an AI agent governance session."""
    manager = AgentSessionManager(
        repo=repo, tool=tool, policy_pack=policy_pack, output_dir=output
    )
    session = manager.start_session()
    console.print(f"[green]✓[/green] Started session: {session.session_id}")
    console.print(f"[dim]Audit saved at: {session.audit_path}[/dim]")
    console.print(
        f"[dim]Policy pack: {session.policy_pack or 'cavra-ai-agent-baseline'}[/dim]"
    )


@agent_app.command("exec")
def exec_command(
    command: Annotated[str, typer.Argument(help="Command to execute.")],
    tool: Annotated[str, typer.Option(help="AI tool identifier.")] = "claude-code",
    repo: Annotated[Path, typer.Option(help="Repository path.")] = Path("."),
    policy_pack: Annotated[Optional[str], typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline",
    output: Annotated[Path, typer.Option(help="Audit output directory.")] = Path(".cavra"),
) -> None:
    """Execute a command under governance policy."""
    manager = AgentSessionManager(
        repo=repo, tool=tool, policy_pack=policy_pack, output_dir=output
    )
    session = manager.start_session()

    guard = RuntimeGuard(policy_pack=session.policy_pack or "cavra-ai-agent-baseline")
    interceptor = CommandInterceptor(guard, session.audit)
    result = interceptor.execute(command)

    if result.success:
        console.print("[green]✓[/green] Command executed successfully")
        if result.output:
            console.print(result.output)
    else:
        console.print(f"[red]✗[/red] {result.error}")
        raise typer.Exit(code=1)

    session.audit.write(output)


@agent_app.command("attest")
def generate_attestation(
    session_id: Annotated[str, typer.Argument(help="Session ID.")],
    audit_dir: Annotated[Path, typer.Option(help="Audit directory.")] = Path(".cavra"),
    format: Annotated[str, typer.Option(help="Output format: markdown, json, artifact")] = "markdown",
) -> None:
    """Generate PR attestation from audit session."""
    audit_path = audit_dir / f"session-{session_id}.json"
    if not audit_path.exists():
        console.print(f"[red]✗[/red] Audit file not found: {audit_path}")
        raise typer.Exit(code=1)

    audit_data = json.loads(audit_path.read_text(encoding="utf-8"))

    if format == "markdown":
        from cavra.audit import SessionAudit

        audit = SessionAudit(**audit_data)
        from cavra.integrations import GitHubPRAttestationExporter

        output = GitHubPRAttestationExporter.export_comment(audit)
        console.print(output)
    elif format == "json":
        console.print(json.dumps(audit_data, indent=2))
    elif format == "artifact":
        from cavra.audit import SessionAudit
        from cavra.integrations import GitHubPRAttestationExporter

        audit = SessionAudit(**audit_data)
        path = GitHubPRAttestationExporter.save_artifact(audit, audit_dir)
        console.print(f"[green]✓[/green] Artifact saved: {path}")
    else:
        console.print(f"[red]✗[/red] Unknown format: {format}")
        raise typer.Exit(code=1)


@agent_app.command("enforcement-readiness")
def agent_enforcement_readiness(
    repo_root: Annotated[Path, typer.Option(help="Repository root to inspect.")] = Path("."),
    settings: Annotated[
        Optional[Path],
        typer.Option(help="Optional JSON export of branch protection, required checks, and security checks."),
    ] = None,
    json_output: bool = typer.Option(False, "--json", help="Print the full readiness report JSON."),
) -> None:
    """Report whether a repository can enforce CAVRA for AI coding agents."""
    report = agent_enforcement_readiness_report(repo_root=repo_root, settings_path=settings)
    if json_output:
        typer.echo(json.dumps(report, indent=2))
        return

    status = str(report["status"])
    color = "green" if status == "ready" else "yellow" if status == "needs_attention" else "red"
    summary = report["summary"]
    console.print(f"[{color}]Agent enforcement readiness: {status}[/{color}]")
    console.print(
        f"Checks: {summary['check_count']} "
        f"passed={summary['pass_count']} warnings={summary['warning_count']} failed={summary['failed_count']}"
    )
    for check in report["checks"]:
        marker = "✓" if check["status"] == "pass" else "!" if check["status"] == "warn" else "✗"
        console.print(f"{marker} {check['id']}: {check['message']}")


@policy_app.command("list")
def list_policies() -> None:
    """List available policy packs."""
    registry = PolicyRegistry()
    packs = registry.list_policy_packs()
    console.print("Available policy packs:")
    for pack in packs:
        console.print(f"  [blue]{pack['id']}[/blue]: {pack['title']}")


@policy_app.command("validate")
def validate_policy(
    path: Annotated[Path, typer.Argument(help="Policy YAML path or policy pack directory.")]
) -> None:
    """Validate a policy pack against the CAVRA JSON Schema."""
    policy_path = path / "policy.yaml" if path.is_dir() else path
    if not policy_path.exists():
        console.print(f"[red]Policy not found:[/red] {policy_path}")
        raise typer.Exit(code=1)
    payload = load_policy_file(policy_path)
    errors = validate_policy_payload(payload)
    if errors:
        console.print(f"[red]invalid[/red] {policy_path}")
        for error in errors:
            console.print(f"  - {error}")
        raise typer.Exit(code=1)
    console.print(f"[green]valid[/green] {payload['metadata']['id']}")


@policy_app.command("test")
def test_policy(
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline"
) -> None:
    """Run core CAVRA policy assertions."""
    guard = RuntimeGuard(policy_pack=policy_pack)
    checks = [
        ("block .env read", guard.evaluate_file_access(Path(".env"), "read").decision == "block"),
        ("allow terraform plan", guard.evaluate_command("terraform plan").decision == "allow"),
        ("block terraform apply -auto-approve", guard.evaluate_command("terraform apply -auto-approve").decision == "block"),
        ("block push to main", guard.evaluate_git_action("push", "origin/main").decision == "block"),
        ("block unknown MCP filesystem server", guard.evaluate_mcp_tool_call("unknown-filesystem", "read_file", "filesystem").decision == "block"),
    ]
    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        console.print(f"{'[green]PASS[/green]' if ok else '[red]FAIL[/red]'} {name}")
    if failed:
        raise typer.Exit(code=1)


@policy_app.command("explain")
def explain_policy(
    action_type: Annotated[str, typer.Argument(help="Action type to explain.")],
    target: Annotated[str, typer.Argument(help="Action target.")],
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline",
) -> None:
    """Explain the policy decision for an action."""
    guard = RuntimeGuard(policy_pack=policy_pack)
    if action_type == "read_file":
        decision = guard.evaluate_file_access(Path(target), "read")
    elif action_type == "write_file":
        decision = guard.evaluate_file_access(Path(target), "write")
    elif action_type == "execute_command":
        decision = guard.evaluate_command(target)
    else:
        decision = guard.evaluate_mcp_tool_call(target, "unknown", action_type)
    console.print(JSON(json.dumps(decision.to_dict(), indent=2)))


@policy_app.command("compile")
def compile_policy(
    policy_pack: Annotated[str, typer.Option(help="Base policy pack ID.")] = "cavra-ai-agent-baseline",
    overlay: Annotated[Optional[list[Path]], typer.Option(help="Policy YAML or pack directory overlay.")] = None,
) -> None:
    """Compile a policy pack and optional overlays to normalized JSON."""
    registry = PolicyRegistry()
    overlays = [load_policy_file(item) for item in overlay or []]
    compiled = compile_policy_payload(registry.load_policy(policy_pack), overlays)
    errors = validate_policy_payload(compiled)
    if errors:
        console.print("[red]compiled policy is invalid[/red]")
        for error in errors:
            console.print(f"  - {error}")
        raise typer.Exit(code=1)
    console.print(JSON(json.dumps(compiled, indent=2)))


@policy_app.command("rego-export")
def rego_export_policy(
    policy_pack: Annotated[str, typer.Option(help="Base policy pack ID.")] = "cavra-ai-agent-baseline",
    output_dir: Annotated[Path, typer.Option(help="Directory for generated Rego module, data, fixtures, and manifest.")] = Path(
        "dist/opa-rego"
    ),
    overlay: Annotated[Optional[list[Path]], typer.Option(help="Policy YAML or pack directory overlay.")] = None,
) -> None:
    """Export a CAVRA policy pack to a public-safe OPA/Rego compatibility bundle."""
    bundle = build_rego_policy_bundle(policy_pack, overlays=overlay or [])
    result = write_rego_bundle(bundle, output_dir)
    console.print(JSON(json.dumps(result, indent=2)))


@policy_app.command("rego-test")
def rego_test_policy(
    policy_pack: Annotated[str, typer.Option(help="Base policy pack ID.")] = "cavra-ai-agent-baseline",
) -> None:
    """Run Rego/Python parity tests for the generated policy path."""
    report = run_rego_parity_report(policy_pack)
    console.print(JSON(json.dumps(report, indent=2)))
    if not report["passed"]:
        raise typer.Exit(code=1)


@policy_app.command("rego-readiness")
def rego_readiness_policy(
    packet: Annotated[Path, typer.Argument(help="OPA/Rego policy readiness packet JSON.")],
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live.")] = False,
) -> None:
    """Validate an OPA/Rego policy readiness packet."""
    payload = json.loads(packet.read_text(encoding="utf-8"))
    result = validate_opa_rego_policy_packet(payload, require_live=require_live)
    console.print(JSON(json.dumps(result, indent=2)))
    if result["blocker_count"] or (require_live and not result["ready_for_live_opa_rego_policy_path"]):
        raise typer.Exit(code=1)


@policy_app.command("lifecycle-plan")
def lifecycle_plan_policy(
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline",
    previous_policy_pack: Annotated[Optional[str], typer.Option(help="Optional prior policy pack ID for diff/rollback.")] = None,
    output_dir: Annotated[Path, typer.Option(help="Directory for lifecycle plan artifacts.")] = Path(
        "dist/policy-lifecycle"
    ),
    requested_by: Annotated[str, typer.Option(help="Policy lifecycle requestor identity.")] = "policy-owner@example.com",
    source_ref: Annotated[str, typer.Option(help="Git/source reference for the policy.")] = "git://Huzefaaa2/cavra/main/policies",
) -> None:
    """Export policy lifecycle lint, version, shadow, dry-run, rollback, and approval artifacts."""
    registry = PolicyRegistry()
    policy = registry.load_policy(policy_pack)
    previous = registry.load_policy(previous_policy_pack) if previous_policy_pack else None
    plan = build_policy_lifecycle_plan(
        policy,
        previous_policy=previous,
        policy_pack=policy_pack,
        requested_by=requested_by,
        source_ref=source_ref,
    )
    result = write_policy_lifecycle_artifacts(plan, output_dir)
    console.print(JSON(json.dumps(result, indent=2)))


@policy_app.command("lifecycle-readiness")
def lifecycle_readiness_policy(
    packet: Annotated[Path, typer.Argument(help="Policy lifecycle readiness packet JSON.")],
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live.")] = False,
) -> None:
    """Validate a policy lifecycle readiness packet."""
    payload = json.loads(packet.read_text(encoding="utf-8"))
    result = validate_policy_lifecycle_packet(payload, require_live=require_live)
    console.print(JSON(json.dumps(result, indent=2)))
    if result["blocker_count"] or (require_live and not result["ready_for_live_policy_lifecycle"]):
        raise typer.Exit(code=1)


@policy_app.command("diff")
def diff_policy(left: Path, right: Path) -> None:
    """Show a semantic diff between two policies."""
    diff = diff_policies(load_policy_file(left), load_policy_file(right))
    console.print(JSON(json.dumps(diff.to_dict(), indent=2)))


@policy_app.command("sign")
def sign_policy(
    path: Path,
    signer: Annotated[str, typer.Option(help="Signer identity recorded in signature metadata.")] = "local",
    key: Annotated[Optional[str], typer.Option(help="Optional HMAC key for local tamper checks.")] = None,
    private_key: Annotated[Optional[Path], typer.Option(help="Optional Ed25519 private key PEM path.")] = None,
    key_id: Annotated[Optional[str], typer.Option(help="Policy signing key identifier for Ed25519 signatures.")] = None,
) -> None:
    """Create CAVRA policy signature metadata."""
    policy_path = path / "policy.yaml" if path.is_dir() else path
    if key and private_key:
        console.print("[red]choose either --key or --private-key, not both[/red]")
        raise typer.Exit(code=1)
    sig_path = write_policy_signature(policy_path, signer=signer, key=key, private_key_path=private_key, key_id=key_id)
    console.print(f"[green]signed[/green] {sig_path}")


@policy_app.command("verify")
def verify_policy(
    path: Path,
    signature: Annotated[Optional[Path], typer.Option(help="Signature metadata path.")] = None,
    key: Annotated[Optional[str], typer.Option(help="Optional HMAC key for local tamper checks.")] = None,
    public_key: Annotated[Optional[Path], typer.Option(help="Optional Ed25519 public key PEM path.")] = None,
) -> None:
    """Verify CAVRA policy signature metadata."""
    policy_path = path / "policy.yaml" if path.is_dir() else path
    if key and public_key:
        console.print("[red]choose either --key or --public-key, not both[/red]")
        raise typer.Exit(code=1)
    ok, message = verify_policy_signature(policy_path, signature_path=signature, key=key, public_key_path=public_key)
    if not ok:
        console.print(f"[red]signature verification failed[/red]: {message}")
        raise typer.Exit(code=1)
    console.print(f"[green]signature verified[/green]: {message}")


@policy_app.command("keygen")
def policy_keygen(
    output: Annotated[Path, typer.Option(help="Directory where the local keypair will be written.")] = Path(
        ".cavra/policy-signing"
    ),
    key_id: Annotated[str, typer.Option(help="Stable key identifier to include in signatures.")] = "local-policy-signing-key",
) -> None:
    """Generate a local Ed25519 keypair for public policy signing workflows."""
    private_key = output / f"{key_id}.private.pem"
    public_key = output / f"{key_id}.public.pem"
    payload = generate_policy_signing_keypair(private_key, public_key, key_id=key_id)
    _print_json(payload)


@policy_app.command("simulate")
def simulate_policy(policy_pack: str = "cavra-ai-agent-baseline") -> None:
    """Simulate the flagship CAVRA decision sequence."""
    _run_before_agent_acts(policy_pack=policy_pack)


@policy_app.command("dry-run")
def dry_run_policy(policy_pack: str = "cavra-ai-agent-baseline") -> None:
    """Run policy simulation without enforcing changes."""
    _run_before_agent_acts(policy_pack=policy_pack)


@policy_app.command("init")
def init_policy(destination: Path = Path(".cavra/policy.yaml")) -> None:
    """Create a starter CAVRA policy."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parents[2] / "policies" / "cavra-ai-agent-baseline" / "policy.yaml"
    shutil.copyfile(source, destination)
    console.print(f"[green]created[/green] {destination}")


@policy_app.command("describe")
def describe_policy(
    pack_id: Annotated[str, typer.Argument(help="Policy pack ID.")]
) -> None:
    """Describe a policy pack."""
    registry = PolicyRegistry()
    pack = registry.get_policy_pack(pack_id)
    console.print(f"[bold]{pack['title']}[/bold]")
    console.print(f"[dim]Version: {pack.get('version', 'N/A')}[/dim]")
    console.print(f"{pack['description']}")
    console.print("")
    if pack.get("policy"):
        console.print("[yellow]Policy rules:[/yellow]")
        console.print(JSON(json.dumps(pack["policy"], indent=2)))


@init_app.command("claude-code")
def init_claude_code() -> None:
    """Initialize first-class Claude Code governance with CAVRA."""
    cavra_dir = Path(".cavra")
    cavra_dir.mkdir(exist_ok=True)
    (cavra_dir / "session").mkdir(exist_ok=True)
    if not (cavra_dir / "policy.yaml").exists():
        source = Path(__file__).resolve().parents[2] / "policies" / "cavra-ai-agent-baseline" / "policy.yaml"
        shutil.copyfile(source, cavra_dir / "policy.yaml")
    Path(".mcp.json").write_text(
        json.dumps(
            {
                "mcpServers": {
                    "cavra": {
                        "command": "cavra-mcp-server",
                        "args": [],
                        "env": {"CAVRA_POLICY": ".cavra/policy.yaml"},
                    }
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    console.print("[green]CAVRA Claude Code governance initialized.[/green]")
    console.print("Next: claude mcp add cavra -- cavra-mcp-server")


@evidence_app.command("bundle")
def bundle_evidence(
    output: Annotated[Path, typer.Option(help="Evidence bundle directory.")] = Path(".cavra/evidence/latest"),
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID for sample decisions.")] = "cavra-ai-agent-baseline",
    signer: Annotated[str, typer.Option(help="Signer identity recorded in manifest.")] = "local",
    key: Annotated[Optional[str], typer.Option(help="Optional HMAC key for manifest signature.")] = None,
    private_key: Annotated[Optional[Path], typer.Option(help="Optional Ed25519 private key PEM for manifest signature.")] = None,
    key_id: Annotated[Optional[str], typer.Option(help="Optional evidence signing key ID.")] = None,
    retention_days: Annotated[int, typer.Option(help="Evidence retention period.")] = 2555,
    classification: Annotated[str, typer.Option(help="Evidence classification recorded in retention policy.")] = "regulated-sdlc",
    legal_hold: Annotated[bool, typer.Option(help="Mark generated evidence as under legal hold.")] = False,
) -> None:
    """Generate a CAVRA evidence bundle from the flagship decision sequence."""
    decisions = _before_agent_acts_decisions(policy_pack=policy_pack)
    try:
        result = create_evidence_bundle(
            decisions,
            output,
            session_id="demo-session",
            signer=signer,
            key=key,
            private_key=private_key,
            key_id=key_id,
            retention_days=retention_days,
            classification=classification,
            legal_hold=legal_hold,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]evidence bundle created[/green] {result.bundle_dir}")
    console.print(f"[dim]manifest: {result.manifest_path}[/dim]")


@evidence_app.command("generate-keypair")
def evidence_keypair(
    private_key: Annotated[Path, typer.Option(help="Private key PEM output path.")] = Path(".cavra/keys/evidence-ed25519-private.pem"),
    public_key: Annotated[Path, typer.Option(help="Public key PEM output path.")] = Path(".cavra/keys/evidence-ed25519-public.pem"),
) -> None:
    """Generate an Ed25519 keypair for evidence manifest signatures."""
    try:
        private_path, public_path = generate_ed25519_keypair(private_key, public_key)
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]evidence keypair created[/green] {public_path}")
    console.print(f"[dim]private key: {private_path}[/dim]")


@evidence_app.command("trust-root")
def evidence_trust_root(
    public_key: Annotated[Path, typer.Argument(help="Ed25519 public key PEM.")],
    output: Annotated[Path, typer.Option(help="Trust root JSON output path.")] = Path(".cavra/keys/evidence-trust-root.json"),
    key_id: Annotated[Optional[str], typer.Option(help="Explicit key ID. Defaults to public key fingerprint prefix.")] = None,
    owner: Annotated[str, typer.Option(help="Owner of the trusted signing key.")] = "platform-security",
    status: Annotated[str, typer.Option(help="active, retired, or revoked.")] = "active",
) -> None:
    """Create a CAVRA evidence signing trust-root document."""
    path = export_key_trust_root(public_key, output, key_id=key_id, owner=owner, status=status)
    console.print(f"[green]trust root exported[/green] {path}")


@evidence_app.command("trust-bundle")
def evidence_trust_bundle(
    trust_roots: Annotated[list[Path], typer.Argument(help="One or more trust-root JSON documents.")],
    output: Annotated[Path, typer.Option(help="Trust-root bundle output path.")] = Path(".cavra/keys/evidence-trust-roots.json"),
) -> None:
    """Create a distributable bundle of CAVRA evidence trust roots."""
    try:
        path = export_trust_root_bundle(trust_roots, output)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]trust-root bundle exported[/green] {path}")


@evidence_app.command("trust-distribution")
def evidence_trust_distribution(
    trust_roots: Annotated[list[Path], typer.Argument(help="One or more trust-root JSON documents.")],
    output: Annotated[Path, typer.Option(help="Output directory for offline trust-root distribution artifacts.")] = Path(
        ".cavra/keys/trust-root-distribution"
    ),
    environment: Annotated[str, typer.Option(help="Target environment label.")] = "production",
    distribution_id: Annotated[Optional[str], typer.Option(help="Explicit distribution ID.")] = None,
    channel: Annotated[Optional[list[str]], typer.Option(help="Approved distribution channel. Repeatable.")] = None,
) -> None:
    """Create an offline distribution package for CAVRA evidence trust roots."""
    try:
        result = export_trust_root_distribution(
            trust_roots,
            output,
            environment=environment,
            distribution_id=distribution_id,
            channels=channel,
        )
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]trust-root distribution exported[/green] {result.output_dir}")
    for path in result.files:
        console.print(f"  {path}")


@evidence_app.command("verify")
def verify_evidence(
    bundle_dir: Annotated[Path, typer.Argument(help="Evidence bundle directory.")],
    key: Annotated[Optional[str], typer.Option(help="Optional HMAC key for manifest signature.")] = None,
    public_key: Annotated[Optional[Path], typer.Option(help="Optional Ed25519 public key PEM for manifest verification.")] = None,
    trust_root: Annotated[Optional[Path], typer.Option(help="Optional CAVRA evidence trust-root JSON.")] = None,
    key_id: Annotated[Optional[str], typer.Option(help="Expected evidence signing key ID.")] = None,
    minimum_retention_days: Annotated[Optional[int], typer.Option(help="Minimum acceptable retention period.")] = None,
) -> None:
    """Verify evidence bundle manifest, checksums, and optional signature."""
    ok, errors = verify_evidence_bundle(
        bundle_dir,
        key=key,
        public_key=public_key,
        trust_root=trust_root,
        key_id=key_id,
        minimum_retention_days=minimum_retention_days,
    )
    if not ok:
        console.print("[red]evidence verification failed[/red]")
        for error in errors:
            console.print(f"  - {error}")
        raise typer.Exit(code=1)
    console.print("[green]evidence verified[/green]")


@evidence_app.command("siem-event")
def print_siem_event(
    bundle_dir: Annotated[Path, typer.Argument(help="Evidence bundle directory.")]
) -> None:
    """Print the SIEM event from an evidence bundle."""
    path = bundle_dir / "siem-event.json"
    if not path.exists():
        console.print(f"[red]SIEM event not found:[/red] {path}")
        raise typer.Exit(code=1)
    console.print(JSON(path.read_text(encoding="utf-8")))


@evidence_app.command("retention-policy")
def retention_policy(
    bundle_dir: Annotated[Path, typer.Argument(help="Evidence bundle directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for retention policy.")] = Path(".cavra/evidence/retention"),
    retention_days: Annotated[int, typer.Option(help="Evidence retention period.")] = 2555,
    classification: Annotated[str, typer.Option(help="Evidence classification.")] = "regulated-sdlc",
    legal_hold: Annotated[bool, typer.Option(help="Mark evidence as under legal hold.")] = False,
) -> None:
    """Export evidence retention controls for an existing bundle."""
    try:
        result = export_retention_policy(
            bundle_dir,
            output,
            retention_days=retention_days,
            classification=classification,
            legal_hold=legal_hold,
        )
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]retention policy exported[/green] {result.output_dir}")
    for path in result.files:
        console.print(f"[dim]{path}[/dim]")


@evidence_app.command("export-siem")
def export_siem(
    bundle_dir: Annotated[Path, typer.Argument(help="Evidence bundle directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for provider payloads.")] = Path(".cavra/evidence/export"),
    provider: Annotated[str, typer.Option(help="all, splunk, sentinel, datadog, or webhook.")] = "all",
    splunk_index: Annotated[str, typer.Option(help="Splunk HEC index name.")] = "cavra",
    datadog_service: Annotated[str, typer.Option(help="Datadog service name.")] = "cavra",
) -> None:
    """Export provider-specific SIEM payloads from an evidence bundle."""
    try:
        result = export_siem_payloads(
            bundle_dir,
            output,
            provider=provider,
            splunk_index=splunk_index,
            datadog_service=datadog_service,
        )
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]SIEM payloads exported[/green] {result.output_dir}")
    for path in result.files:
        console.print(f"[dim]{path}[/dim]")


@evidence_app.command("storage-plan")
def storage_plan(
    bundle_dir: Annotated[Path, typer.Argument(help="Evidence bundle directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for immutable storage plan.")] = Path(".cavra/evidence/storage"),
    retention_days: Annotated[int, typer.Option(help="Retention period for immutable storage.")] = 2555,
    s3_bucket: Annotated[str, typer.Option(help="Reference S3 Object Lock bucket.")] = "cavra-evidence",
    s3_prefix: Annotated[str, typer.Option(help="Reference S3 prefix.")] = "evidence/",
    azure_account: Annotated[str, typer.Option(help="Reference Azure Storage account.")] = "cavraevidence",
    azure_container: Annotated[str, typer.Option(help="Reference Azure blob container.")] = "evidence",
) -> None:
    """Create S3 Object Lock and Azure immutable blob reference plans."""
    try:
        result = export_immutable_storage_plan(
            bundle_dir,
            output,
            retention_days=retention_days,
            s3_bucket=s3_bucket,
            s3_prefix=s3_prefix,
            azure_account=azure_account,
            azure_container=azure_container,
        )
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]immutable storage plan exported[/green] {result.output_dir}")
    for path in result.files:
        console.print(f"[dim]{path}[/dim]")


@evidence_app.command("verify-attestation")
def verify_attestation(
    bundle_dir: Annotated[Path, typer.Argument(help="Evidence bundle directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for attestation verification.")] = Path(".cavra/evidence/attestation"),
) -> None:
    """Verify PR attestation content against bundle evidence."""
    try:
        result = export_attestation_verification(bundle_dir, output)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    report_path = output / "pr-attestation-verification.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not report.get("valid"):
        console.print("[red]PR attestation verification failed[/red]")
        for error in report.get("errors", []):
            console.print(f"  - {error}")
        raise typer.Exit(code=1)
    console.print(f"[green]PR attestation verification exported[/green] {result.output_dir}")
    for path in result.files:
        console.print(f"[dim]{path}[/dim]")


@evidence_app.command("index")
def index_evidence(
    bundle_dir: Annotated[Path, typer.Argument(help="Evidence bundle directory.")],
    store: Annotated[Path, typer.Option(help="Evidence metadata store JSON path.")] = Path(".cavra/evidence/metadata.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite metadata database path.")] = None,
) -> None:
    """Persist searchable evidence metadata from a bundle."""
    try:
        metadata = (
            SQLiteEvidenceMetadataStore(sqlite).index_bundle(bundle_dir)
            if sqlite
            else EvidenceMetadataStore(store).index_bundle(bundle_dir)
        )
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(metadata, indent=2)))


@evidence_app.command("search")
def search_evidence(
    sqlite: Annotated[Path, typer.Option(help="SQLite metadata database path.")] = Path(".cavra/evidence/metadata.db"),
    session_id: Annotated[Optional[str], typer.Option(help="Filter by session ID substring.")] = None,
    signer: Annotated[Optional[str], typer.Option(help="Filter by signer.")] = None,
    min_blocked: Annotated[Optional[int], typer.Option(help="Minimum blocked decision count.")] = None,
    has_approvals: Annotated[Optional[bool], typer.Option(help="Filter sessions with approval-required decisions.")] = None,
    metadata_kind: Annotated[Optional[str], typer.Option(help="Filter by metadata kind, such as managed-endpoint-rollout.")] = None,
    rollout_status: Annotated[Optional[str], typer.Option(help="Filter managed endpoint rollout evidence by status.")] = None,
    environment: Annotated[Optional[str], typer.Option(help="Filter managed endpoint rollout evidence by environment.")] = None,
    deployment_target: Annotated[Optional[str], typer.Option(help="Filter managed endpoint rollout evidence by deployment target ID.")] = None,
    target_ring: Annotated[Optional[str], typer.Option(help="Filter rollout promotion executions by target ring.")] = None,
    approval_state: Annotated[Optional[str], typer.Option(help="Filter rollout promotion executions by approval state.")] = None,
    promotion_execution_status: Annotated[Optional[str], typer.Option(help="Filter rollout promotion executions by execution status.")] = None,
    rollback_execution_status: Annotated[Optional[str], typer.Option(help="Filter rollout rollback executions by execution status.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Search SQLite-backed evidence metadata with filters and pagination."""
    result = SQLiteEvidenceMetadataStore(sqlite).search(
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
    console.print(JSON(json.dumps(result, indent=2)))


@evidence_app.command("migrate")
def migrate_evidence_metadata(
    sqlite: Annotated[Path, typer.Option(help="SQLite metadata database path.")] = Path(".cavra/evidence/metadata.db"),
    migrations_dir: Annotated[Path, typer.Option(help="Directory containing SQLite migration SQL files.")] = Path("migrations/sqlite"),
) -> None:
    """Apply SQLite migrations for evidence metadata search."""
    try:
        result = apply_sqlite_migrations(sqlite, migrations_dir)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(result, indent=2)))


@approval_app.command("create")
def create_approval(
    decision_file: Annotated[Path, typer.Argument(help="Decision JSON file produced by CAVRA.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    approver_group: Annotated[Optional[str], typer.Option(help="Override approver group.")] = None,
    routing_file: Annotated[Optional[Path], typer.Option(help="Optional approval routing JSON/YAML file.")] = None,
    requested_by: Annotated[str, typer.Option(help="Requester identity.")] = "ai-agent",
    ttl_hours: Annotated[int, typer.Option(help="Approval request time to live.")] = 24,
) -> None:
    """Create a pending approval request from a CAVRA decision."""
    try:
        decision = json.loads(decision_file.read_text(encoding="utf-8"))
        approval = _approval_store(store, sqlite).create_request(
            decision,
            approver_group=approver_group,
            requested_by=requested_by,
            ttl_hours=ttl_hours,
            routing_rules=load_routing_rules(routing_file),
        )
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(approval, indent=2)))


@approval_app.command("list")
def list_approvals(
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    state: Annotated[Optional[str], typer.Option(help="Filter by state.")] = None,
    approver_group: Annotated[Optional[str], typer.Option(help="Filter by approver group.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """List approval queue entries."""
    result = _approval_store(store, sqlite).list(state=state, approver_group=approver_group, limit=limit, offset=offset)
    console.print(JSON(json.dumps(result, indent=2)))


@approval_app.command("approve")
def approve_request(
    approval_id: Annotated[str, typer.Argument(help="Approval ID.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    actor: Annotated[str, typer.Option(help="Approver identity.")] = "",
    actor_claims: Annotated[Optional[Path], typer.Option(help="Optional OIDC claims JSON for approval RBAC.")] = None,
    actor_token: Annotated[Optional[Path], typer.Option(help="Optional signed OIDC JWT file for approval RBAC.")] = None,
    oidc_config: Annotated[Optional[Path], typer.Option(help="OIDC config JSON/YAML with issuer, audience, and JWKS.")] = None,
    rbac_file: Annotated[Optional[Path], typer.Option(help="Repository RBAC JSON/YAML policy file.")] = None,
    reason: Annotated[str, typer.Option(help="Approval reason.")] = "",
    external_ref: Annotated[Optional[str], typer.Option(help="Optional ITSM, PR, or ticket reference.")] = None,
) -> None:
    """Approve a pending request."""
    _decide_cli_approval(
        store,
        sqlite,
        approval_id,
        state="approved",
        actor=actor,
        reason=reason,
        external_ref=external_ref,
        actor_claims=actor_claims,
        actor_token=actor_token,
        oidc_config=oidc_config,
        rbac_file=rbac_file,
    )


@approval_app.command("deny")
def deny_request(
    approval_id: Annotated[str, typer.Argument(help="Approval ID.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    actor: Annotated[str, typer.Option(help="Approver identity.")] = "",
    actor_claims: Annotated[Optional[Path], typer.Option(help="Optional OIDC claims JSON for approval RBAC.")] = None,
    actor_token: Annotated[Optional[Path], typer.Option(help="Optional signed OIDC JWT file for approval RBAC.")] = None,
    oidc_config: Annotated[Optional[Path], typer.Option(help="OIDC config JSON/YAML with issuer, audience, and JWKS.")] = None,
    rbac_file: Annotated[Optional[Path], typer.Option(help="Repository RBAC JSON/YAML policy file.")] = None,
    reason: Annotated[str, typer.Option(help="Denial reason.")] = "",
    external_ref: Annotated[Optional[str], typer.Option(help="Optional ITSM, PR, or ticket reference.")] = None,
) -> None:
    """Deny a pending request."""
    _decide_cli_approval(
        store,
        sqlite,
        approval_id,
        state="denied",
        actor=actor,
        reason=reason,
        external_ref=external_ref,
        actor_claims=actor_claims,
        actor_token=actor_token,
        oidc_config=oidc_config,
        rbac_file=rbac_file,
    )


@approval_app.command("expire")
def expire_request(
    approval_id: Annotated[str, typer.Argument(help="Approval ID.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    actor: Annotated[str, typer.Option(help="Actor identity.")] = "system",
    reason: Annotated[str, typer.Option(help="Expiry reason.")] = "approval expired",
) -> None:
    """Expire a pending request."""
    _decide_cli_approval(store, sqlite, approval_id, state="expired", actor=actor, reason=reason)


@approval_app.command("break-glass")
def break_glass_approval(
    decision_file: Annotated[Path, typer.Argument(help="Decision JSON file produced by CAVRA.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    actor: Annotated[str, typer.Option(help="Emergency approver identity.")] = "",
    reason: Annotated[str, typer.Option(help="Mandatory emergency reason.")] = "",
    approver_group: Annotated[str, typer.Option(help="Approver group.")] = "Change Advisory Board",
    external_ref: Annotated[Optional[str], typer.Option(help="Optional incident, ITSM, PR, or ticket reference.")] = None,
    ttl_hours: Annotated[int, typer.Option(help="Emergency approval time to live.")] = 4,
) -> None:
    """Record a break-glass override with mandatory evidence."""
    try:
        decision = json.loads(decision_file.read_text(encoding="utf-8"))
        approval = _approval_store(store, sqlite).break_glass(
            decision=decision,
            actor=actor,
            reason=reason,
            approver_group=approver_group,
            external_ref=external_ref,
            ttl_hours=ttl_hours,
        )
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(approval, indent=2)))


@approval_app.command("route")
def route_approval(
    decision_file: Annotated[Path, typer.Argument(help="Decision JSON file produced by CAVRA.")],
    routing_file: Annotated[Optional[Path], typer.Option(help="Optional approval routing JSON/YAML file.")] = None,
) -> None:
    """Show the approver group selected by approval routing policy."""
    try:
        decision = json.loads(decision_file.read_text(encoding="utf-8"))
        routing_rules = load_routing_rules(routing_file)
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    payload = {
        "decision_id": decision.get("decision_id"),
        "approver_group": route_approver_group(decision, routing_rules),
        "routing_rules": routing_rules,
    }
    console.print(JSON(json.dumps(payload, indent=2)))


@approval_app.command("export-notifications")
def export_approval_notifications(
    approval_id: Annotated[str, typer.Argument(help="Approval ID.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    output: Annotated[Path, typer.Option(help="Output directory for notification payloads.")] = Path(".cavra/approvals/notifications"),
    provider: Annotated[str, typer.Option(help="all, slack, teams, jira, servicenow, or webhook.")] = "all",
) -> None:
    """Export reference notification payloads for approval providers."""
    approval = _approval_store(store, sqlite).get(approval_id)
    if approval is None:
        console.print(f"[red]approval not found:[/red] {approval_id}")
        raise typer.Exit(code=1)
    try:
        result = export_approval_notification_payloads(approval, output, provider=provider)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]approval notification payloads exported[/green] {result.output_dir}")
    for path in result.files:
        console.print(f"[dim]{path}[/dim]")


@approval_app.command("provider-requests")
def export_approval_provider_requests(
    approval_id: Annotated[str, typer.Argument(help="Approval ID.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    output: Annotated[Path, typer.Option(help="Output directory for provider request specs.")] = Path(".cavra/approvals/provider-requests"),
    provider: Annotated[str, typer.Option(help="all, slack, teams, jira, servicenow, or webhook.")] = "all",
) -> None:
    """Export credential-free HTTP request specs for approval providers."""
    approval = _approval_store(store, sqlite).get(approval_id)
    if approval is None:
        console.print(f"[red]approval not found:[/red] {approval_id}")
        raise typer.Exit(code=1)
    try:
        result = export_provider_request_specs(approval, output, provider=provider)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]approval provider request specs exported[/green] {result.output_dir}")
    for path in result.files:
        console.print(f"[dim]{path}[/dim]")


@approval_app.command("deliver")
def deliver_approval_provider_requests(
    approval_id: Annotated[str, typer.Argument(help="Approval ID.")],
    store: Annotated[Path, typer.Option(help="Approval store JSON path.")] = Path(".cavra/approvals.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval database path.")] = None,
    config: Annotated[Optional[Path], typer.Option(help="Approval provider config JSON/YAML path.")] = None,
    output: Annotated[Path, typer.Option(help="Output directory for delivery evidence.")] = Path(".cavra/approvals/deliveries"),
    provider: Annotated[str, typer.Option(help="all, slack, teams, jira, servicenow, or webhook.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
) -> None:
    """Send live approval provider requests and write redacted delivery evidence."""
    approval = _approval_store(store, sqlite).get(approval_id)
    if approval is None:
        console.print(f"[red]approval not found:[/red] {approval_id}")
        raise typer.Exit(code=1)
    if config is None:
        console.print("[red]--config is required for live approval provider delivery[/red]")
        raise typer.Exit(code=1)
    try:
        result = deliver_provider_requests(
            approval,
            load_provider_config(config),
            provider=provider,
            retries=retries,
            timeout_seconds=timeout_seconds,
        )
        path = export_provider_delivery_result(result, output)
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(result, indent=2)))
    console.print(f"[green]approval provider delivery evidence exported[/green] {path}")


@integration_app.command("deliver")
def deliver_integration_connector_event(
    event: Annotated[Path, typer.Argument(help="Connector event JSON file, such as siem-event.json.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for delivery evidence.")] = Path(".cavra/integrations/deliveries"),
    provider: Annotated[str, typer.Option(help="all, splunk, sentinel, datadog, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
) -> None:
    """Send live connector requests and write redacted delivery evidence."""
    try:
        payload = json.loads(event.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("connector event JSON must be an object")
        result = deliver_connector_event(
            payload,
            load_connector_config(config),
            provider=provider,
            retries=retries,
            timeout_seconds=timeout_seconds,
        )
        path = export_connector_delivery_result(result, output)
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(result, indent=2)))
    console.print(f"[green]connector delivery evidence exported[/green] {path}")


@approval_app.command("migrate")
def migrate_approval_store(
    sqlite: Annotated[Path, typer.Option(help="SQLite approval database path.")] = Path(".cavra/approvals.db"),
    migrations_dir: Annotated[Path, typer.Option(help="Directory containing SQLite migration SQL files.")] = Path("migrations/sqlite"),
) -> None:
    """Apply SQLite migrations for approval persistence."""
    try:
        result = apply_sqlite_migrations(sqlite, migrations_dir)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(result, indent=2)))


def _decide_cli_approval(
    store: Path,
    sqlite: Path | None,
    approval_id: str,
    *,
    state: str,
    actor: str,
    reason: str,
    external_ref: str | None = None,
    actor_claims: Path | None = None,
    actor_token: Path | None = None,
    oidc_config: Path | None = None,
    rbac_file: Path | None = None,
) -> None:
    try:
        rbac_rules = load_rbac_rules(rbac_file)
        actor_context = _actor_context(actor_claims, actor_token, oidc_config, rbac_rules=rbac_rules)
        approval = _approval_store(store, sqlite).decide(
            approval_id,
            state=state,
            actor=actor,
            reason=reason,
            external_ref=external_ref,
            actor_context=actor_context,
            rbac_rules=rbac_rules,
        )
    except KeyError as exc:
        console.print(f"[red]approval not found:[/red] {approval_id}")
        raise typer.Exit(code=1) from exc
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    console.print(JSON(json.dumps(approval, indent=2)))


def _approval_store(store: Path, sqlite: Path | None = None) -> ApprovalStore | SQLiteApprovalStore:
    return SQLiteApprovalStore(sqlite) if sqlite else ApprovalStore(store)


def _actor_context(
    actor_claims: Path | None,
    actor_token: Path | None,
    oidc_config: Path | None,
    *,
    rbac_rules: dict[str, object],
) -> dict[str, object] | None:
    if actor_claims and actor_token:
        raise ValueError("use either --actor-claims or --actor-token, not both")
    if actor_token:
        if oidc_config is None:
            raise ValueError("--oidc-config is required with --actor-token")
        return actor_context_from_oidc_token(actor_token.read_text(encoding="utf-8").strip(), load_oidc_config(oidc_config), rbac_rules=rbac_rules)
    if actor_claims:
        return actor_context_from_claims(json.loads(actor_claims.read_text(encoding="utf-8")), rbac_rules=rbac_rules)
    return None


@registry_app.command("agent-register")
def register_agent(
    agent_id: Annotated[str, typer.Argument(help="Agent ID.")],
    store: Annotated[Path, typer.Option(help="Registry store JSON path.")] = Path(".cavra/registry.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="SQLite registry database path.")] = None,
    agent_type: Annotated[str, typer.Option(help="Agent type.")] = "coding-agent",
    vendor: Annotated[str, typer.Option(help="Agent vendor.")] = "unknown",
    version: Annotated[str, typer.Option(help="Agent version.")] = "unknown",
    capability: Annotated[list[str], typer.Option("--capability", help="Agent capability.")] = [],
    scope: Annotated[list[str], typer.Option("--scope", help="Allowed scope.")] = [],
    repository: Annotated[list[str], typer.Option("--repository", help="Allowed repository.")] = [],
    tool: Annotated[list[str], typer.Option("--tool", help="Allowed tool.")] = [],
    risk_tier: Annotated[str, typer.Option(help="Risk tier.")] = "medium",
    owner: Annotated[str, typer.Option(help="Owning team.")] = "unassigned",
    status: Annotated[str, typer.Option(help="active, disabled, or retired.")] = "active",
) -> None:
    """Register or update a governed AI-agent identity."""
    try:
        record = _registry_store(store, sqlite).upsert_agent(
            {
                "agent_id": agent_id,
                "type": agent_type,
                "vendor": vendor,
                "version": version,
                "capabilities": capability,
                "scopes": scope,
                "allowed_repositories": repository,
                "allowed_tools": tool,
                "risk_tier": risk_tier,
                "owner": owner,
                "status": status,
            }
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    _print_json(record)


@registry_app.command("agent-list")
def list_agents(
    store: Annotated[Path, typer.Option(help="Registry store JSON path.")] = Path(".cavra/registry.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="SQLite registry database path.")] = None,
    status: Annotated[Optional[str], typer.Option(help="Filter by status.")] = None,
    owner: Annotated[Optional[str], typer.Option(help="Filter by owner.")] = None,
) -> None:
    """List governed AI-agent identities."""
    _print_json(_registry_store(store, sqlite).list_agents(status=status, owner=owner))


@registry_app.command("profiles")
def list_agent_profiles() -> None:
    """List predefined AI-agent capability profiles."""
    _print_json(default_agent_profiles())


@registry_app.command("mcp-register")
def register_mcp_server(
    server_id: Annotated[str, typer.Argument(help="MCP server ID.")],
    store: Annotated[Path, typer.Option(help="Registry store JSON path.")] = Path(".cavra/registry.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="SQLite registry database path.")] = None,
    name: Annotated[Optional[str], typer.Option(help="Display name.")] = None,
    trust_tier: Annotated[str, typer.Option(help="trusted, approved, experimental, blocked, or unknown.")] = "unknown",
    capability: Annotated[list[str], typer.Option("--capability", help="Approved capability.")] = [],
    owner: Annotated[str, typer.Option(help="Owning team.")] = "unassigned",
    approval_state: Annotated[str, typer.Option(help="approved, pending, denied, or not_required.")] = "pending",
    tool: Annotated[list[str], typer.Option("--tool", help="Approved tool.")] = [],
) -> None:
    """Register or update an MCP server trust record."""
    try:
        record = _registry_store(store, sqlite).upsert_mcp_server(
            {
                "server_id": server_id,
                "name": name or server_id,
                "trust_tier": trust_tier,
                "capabilities": capability,
                "owner": owner,
                "approval_state": approval_state,
                "allowed_tools": tool,
            }
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    _print_json(record)


@registry_app.command("mcp-list")
def list_mcp_servers(
    store: Annotated[Path, typer.Option(help="Registry store JSON path.")] = Path(".cavra/registry.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="SQLite registry database path.")] = None,
    trust_tier: Annotated[Optional[str], typer.Option(help="Filter by trust tier.")] = None,
    approval_state: Annotated[Optional[str], typer.Option(help="Filter by approval state.")] = None,
    capability: Annotated[Optional[str], typer.Option(help="Filter by capability.")] = None,
) -> None:
    """List MCP server trust records."""
    result = _registry_store(store, sqlite).list_mcp_servers(trust_tier=trust_tier, approval_state=approval_state, capability=capability)
    _print_json(result)


@registry_app.command("mcp-check")
def check_mcp_server(
    server_id: Annotated[str, typer.Argument(help="MCP server ID.")],
    tool: Annotated[str, typer.Argument(help="Requested MCP tool.")],
    store: Annotated[Path, typer.Option(help="Registry store JSON path.")] = Path(".cavra/registry.json"),
    sqlite: Annotated[Optional[Path], typer.Option(help="SQLite registry database path.")] = None,
    capability: Annotated[Optional[str], typer.Option(help="Requested capability.")] = None,
) -> None:
    """Evaluate an MCP tool call against the trust registry."""
    _print_json(_registry_store(store, sqlite).evaluate_mcp(server_id, tool, capability))


@registry_app.command("mcp-classifications")
def list_mcp_classifications(
    capability: Annotated[Optional[str], typer.Option(help="Filter by capability.")] = None,
) -> None:
    """List MCP tool capability classifications."""
    if capability:
        item = classify_mcp_capability(capability)
        if item is None:
            console.print(f"[red]unknown MCP capability:[/red] {capability}")
            raise typer.Exit(code=1)
        _print_json(item)
    else:
        _print_json(default_mcp_tool_classifications())


@registry_app.command("migrate")
def migrate_registry(
    sqlite: Annotated[Path, typer.Option(help="SQLite registry database path.")] = Path(".cavra/registry.db"),
    migrations: Annotated[Path, typer.Option(help="SQLite migrations directory.")] = Path("migrations/sqlite"),
) -> None:
    """Apply SQLite migrations for the registry and other CAVRA metadata tables."""
    result = apply_sqlite_migrations(sqlite, migrations)
    _print_json(result)


def _registry_store(store: Path, sqlite: Path | None) -> RegistryStore | SQLiteRegistryStore:
    if sqlite is not None:
        return SQLiteRegistryStore(sqlite)
    return RegistryStore(store)


@ops_app.command("stores")
def list_persistent_api_stores() -> None:
    """List configured persistent API stores and whether each path exists."""
    _print_json(persistent_api_store_status())


@ops_app.command("backup")
def backup_persistent_api(
    output: Annotated[Path, typer.Option(help="Backup output directory.")] = Path(".cavra/backups/latest"),
    include_missing: Annotated[bool, typer.Option(help="Write placeholder files for missing stores.")] = False,
) -> None:
    """Back up configured JSON and SQLite persistent API stores."""
    result = backup_persistent_api_stores(output, include_missing=include_missing)
    _print_json(result)


@ops_app.command("restore")
def restore_persistent_api(
    manifest: Annotated[Path, typer.Argument(help="Backup manifest JSON path.")],
    target_dir: Annotated[Optional[Path], typer.Option(help="Optional restore directory instead of configured live paths.")] = None,
    overwrite: Annotated[bool, typer.Option(help="Overwrite existing target files.")] = False,
) -> None:
    """Restore a persistent API backup after checksum validation."""
    try:
        result = restore_persistent_api_backup(manifest, target_dir=target_dir, overwrite=overwrite)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    _print_json(result)


@ops_app.command("retention-plan")
def persistent_api_retention_plan(
    output: Annotated[Path, typer.Option(help="Output directory for retention plan artifacts.")] = Path(".cavra/operations/retention"),
    retention_days: Annotated[int, typer.Option(help="Minimum persistent API retention period.")] = 2555,
    classification: Annotated[str, typer.Option(help="Operational data classification.")] = "regulated-sdlc",
    legal_hold: Annotated[bool, typer.Option(help="Mark persistent API data as under legal hold.")] = False,
) -> None:
    """Export backup, restore-test, and retention controls for persistent API stores."""
    try:
        result = export_persistent_api_retention_plan(
            output,
            retention_days=retention_days,
            classification=classification,
            legal_hold=legal_hold,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    _print_json(result)


@release_app.command("phase6-rollup")
def release_phase6_rollup(
    packet: Annotated[Optional[Path], typer.Option(help="Optional checked-in Phase 6 rollup packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root for artifact validation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export generated packet/result.")] = None,
    require_customer_live: Annotated[bool, typer.Option(help="Require customer live deployment evidence refs.")] = False,
) -> None:
    """Validate or export the Phase 6 ecosystem expansion rollup."""
    root = repo_root.resolve()
    if export_dir:
        result = write_phase6_rollup_artifacts(root, export_dir)
    else:
        payload = json.loads(packet.read_text(encoding="utf-8")) if packet else build_phase6_rollup_packet(root)
        result = validate_phase6_rollup_packet(
            payload,
            repo_root=root,
            require_customer_live=require_customer_live,
        )
    print(json.dumps(result, indent=2))
    if not result["ready_for_phase6_public_contract_release"] or (
        require_customer_live and not result["ready_for_customer_live_phase6_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("phase4-closeout")
def release_phase4_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional checked-in Phase 4 closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root for artifact validation."),
    ] = Path("."),
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export generated packet/result."),
    ] = None,
    require_customer_live: Annotated[
        bool,
        typer.Option(help="Require customer live deployment evidence refs."),
    ] = False,
) -> None:
    """Validate or export the Phase 4 connector and scanner closeout."""
    root = repo_root.resolve()
    if export_dir:
        result = write_phase4_closeout_artifacts(root, export_dir)
    else:
        payload = (
            json.loads(packet.read_text(encoding="utf-8"))
            if packet
            else build_phase4_closeout_packet(root)
        )
        result = validate_phase4_closeout_packet(
            payload,
            repo_root=root,
            require_customer_live=require_customer_live,
        )
    print(json.dumps(result, indent=2))
    if not result["ready_for_phase4_public_contract_release"] or (
        require_customer_live
        and not result["ready_for_customer_live_phase4_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("phase5-closeout")
def release_phase5_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional checked-in Phase 5 closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root for artifact validation."),
    ] = Path("."),
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export generated packet/result."),
    ] = None,
    require_customer_live: Annotated[
        bool,
        typer.Option(help="Require customer live deployment evidence refs."),
    ] = False,
) -> None:
    """Validate or export the Phase 5 policy lifecycle and event core closeout."""
    root = repo_root.resolve()
    if export_dir:
        result = write_phase5_closeout_artifacts(root, export_dir)
    else:
        payload = (
            json.loads(packet.read_text(encoding="utf-8"))
            if packet
            else build_phase5_closeout_packet(root)
        )
        result = validate_phase5_closeout_packet(
            payload,
            repo_root=root,
            require_customer_live=require_customer_live,
        )
    print(json.dumps(result, indent=2))
    if not result["ready_for_phase5_public_contract_release"] or (
        require_customer_live
        and not result["ready_for_customer_live_phase5_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-live-evidence")
def release_customer_live_evidence(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer-live evidence packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live templates.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer-live evidence intake packet."""
    if export_dir:
        result = write_customer_live_evidence_artifacts(export_dir)
    else:
        payload = json.loads(packet.read_text(encoding="utf-8")) if packet else build_customer_live_evidence_template()
        result = validate_customer_live_evidence_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_live_evidence_intake"]):
        raise typer.Exit(code=1)


@release_app.command("customer-evidence-room")
def release_customer_evidence_room(
    index: Annotated[Optional[Path], typer.Option(help="Optional customer evidence-room index JSON.")] = None,
    intake_packet: Annotated[Optional[Path], typer.Option(help="Optional customer-live intake packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live indexes.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer evidence-room closeout index."""
    if export_dir:
        result = write_customer_evidence_room_artifacts(export_dir)
    else:
        if index:
            payload = json.loads(index.read_text(encoding="utf-8"))
        else:
            intake = json.loads(intake_packet.read_text(encoding="utf-8")) if intake_packet else None
            payload = build_customer_evidence_room_index(
                intake,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_evidence_room_index(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_evidence_room_closeout"]):
        raise typer.Exit(code=1)


@release_app.command("customer-closeout-handoff")
def release_customer_closeout_handoff(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer closeout handoff packet JSON.")] = None,
    evidence_room_index: Annotated[Optional[Path], typer.Option(help="Optional evidence-room index JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer closeout handoff packet."""
    if export_dir:
        result = write_customer_closeout_handoff_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            evidence_room = json.loads(evidence_room_index.read_text(encoding="utf-8")) if evidence_room_index else None
            payload = build_customer_closeout_handoff_packet(
                evidence_room,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_closeout_handoff_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_closeout_handoff"]):
        raise typer.Exit(code=1)


@release_app.command("customer-operating-review")
def release_customer_operating_review(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer operating review packet JSON.")] = None,
    closeout_handoff: Annotated[Optional[Path], typer.Option(help="Optional closeout handoff packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the recurring customer operating review packet."""
    if export_dir:
        result = write_customer_operating_review_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            handoff = json.loads(closeout_handoff.read_text(encoding="utf-8")) if closeout_handoff else None
            payload = build_customer_operating_review_packet(
                handoff,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_operating_review_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_operating_review"]):
        raise typer.Exit(code=1)


@release_app.command("customer-renewal-expansion")
def release_customer_renewal_expansion(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer renewal expansion packet JSON.")] = None,
    operating_review: Annotated[Optional[Path], typer.Option(help="Optional operating review packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer renewal and expansion readiness packet."""
    if export_dir:
        result = write_customer_renewal_expansion_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            review = json.loads(operating_review.read_text(encoding="utf-8")) if operating_review else None
            payload = build_customer_renewal_expansion_packet(
                review,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_renewal_expansion_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_renewal_expansion"]):
        raise typer.Exit(code=1)


@release_app.command("customer-renewal-outcome")
def release_customer_renewal_outcome(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer renewal outcome closeout packet JSON.")] = None,
    renewal_expansion: Annotated[Optional[Path], typer.Option(help="Optional renewal expansion packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer renewal outcome closeout packet."""
    if export_dir:
        result = write_customer_renewal_outcome_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            renewal = json.loads(renewal_expansion.read_text(encoding="utf-8")) if renewal_expansion else None
            payload = build_customer_renewal_outcome_packet(
                renewal,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_renewal_outcome_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_renewal_outcome_closeout"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-rollup")
def release_customer_lifecycle_rollup(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle rollup packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle executive rollup packet."""
    if export_dir:
        result = write_customer_lifecycle_rollup_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_rollup_packet(evidence_mode="live" if require_live else "sample")
        result = validate_customer_lifecycle_rollup_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_executive_rollup"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-archive")
def release_customer_lifecycle_archive(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle archive manifest JSON.")] = None,
    rollup: Annotated[Optional[Path], typer.Option(help="Optional lifecycle executive rollup packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live manifests.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle archive manifest."""
    if export_dir:
        result = write_customer_lifecycle_archive_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            rollup_payload = json.loads(rollup.read_text(encoding="utf-8")) if rollup else None
            payload = build_customer_lifecycle_archive_manifest(
                rollup_payload,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_archive_manifest(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_archive_manifest"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-status")
def release_customer_lifecycle_status(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle public status packet JSON.")] = None,
    archive: Annotated[Optional[Path], typer.Option(help="Optional lifecycle archive manifest JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle public status packet."""
    if export_dir:
        result = write_customer_lifecycle_status_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            archive_payload = json.loads(archive.read_text(encoding="utf-8")) if archive else None
            payload = build_customer_lifecycle_status_packet(
                archive_payload,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_status_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_public_status"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-final-seal")
def release_customer_lifecycle_final_seal(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle final release seal packet JSON.")] = None,
    status: Annotated[Optional[Path], typer.Option(help="Optional lifecycle public status packet JSON.")] = None,
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle final release seal packet."""
    if export_dir:
        result = write_customer_lifecycle_final_seal_artifacts(export_dir)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            status_payload = json.loads(status.read_text(encoding="utf-8")) if status else None
            payload = build_customer_lifecycle_final_seal_packet(
                status_payload,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_final_seal_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_final_release_seal"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-verification-index")
def release_customer_lifecycle_verification_index(
    index: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle verification index JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used to verify artifact paths.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live indexes.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle verification index."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_verification_index_artifacts(export_dir, root)
    else:
        if index:
            payload = json.loads(index.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_verification_index(
                root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_verification_index(payload, repo_root=root, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_verification_index"]):
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-live-validation-plan")
def release_managed_enterprise_live_validation_plan(
    plan: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise live validation plan JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized plan templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise live validation plan."""
    if export_dir:
        result = write_managed_enterprise_live_validation_plan_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_live_validation"] is True
    else:
        payload = (
            json.loads(plan.read_text(encoding="utf-8"))
            if plan
            else build_managed_enterprise_live_validation_plan(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_live_validation_plan(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_live_validation"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-cutover-runbook")
def release_managed_enterprise_cutover_runbook(
    runbook: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise cutover runbook JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized cutover runbook templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise cutover runbook."""
    if export_dir:
        result = write_managed_enterprise_cutover_runbook_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_cutover"] is True
    else:
        payload = (
            json.loads(runbook.read_text(encoding="utf-8"))
            if runbook
            else build_managed_enterprise_cutover_runbook(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_cutover_runbook(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_cutover"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-stabilization-report")
def release_managed_enterprise_stabilization_report(
    report: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise stabilization report JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized stabilization report templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise post-cutover stabilization report."""
    if export_dir:
        result = write_managed_enterprise_stabilization_report_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_stabilization_closeout"] is True
    else:
        payload = (
            json.loads(report.read_text(encoding="utf-8"))
            if report
            else build_managed_enterprise_stabilization_report(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_stabilization_report(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_stabilization_closeout"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-steady-state-handoff")
def release_managed_enterprise_steady_state_handoff(
    handoff: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise steady-state handoff JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized steady-state handoff templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise steady-state handoff packet."""
    if export_dir:
        result = write_managed_enterprise_steady_state_handoff_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_steady_state"] is True
    else:
        payload = (
            json.loads(handoff.read_text(encoding="utf-8"))
            if handoff
            else build_managed_enterprise_steady_state_handoff(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_steady_state_handoff(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_steady_state"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-operating-release-index")
def release_managed_enterprise_operating_release_index(
    index: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise operating release index JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized operating release index templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise operating release index."""
    if export_dir:
        result = write_managed_enterprise_operating_release_index_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_operating_release"] is True
    else:
        payload = (
            json.loads(index.read_text(encoding="utf-8"))
            if index
            else build_managed_enterprise_operating_release_index(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_operating_release_index(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_operating_release"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-operating-announcement")
def release_managed_enterprise_operating_announcement(
    announcement: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise operating announcement JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized operating announcement templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise operating announcement packet."""
    if export_dir:
        result = write_managed_enterprise_operating_announcement_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_operating_announcement"] is True
    else:
        payload = (
            json.loads(announcement.read_text(encoding="utf-8"))
            if announcement
            else build_managed_enterprise_operating_announcement(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_operating_announcement(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_operating_announcement"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-operating-chain")
def release_managed_enterprise_operating_chain(
    manifest: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise operating chain manifest JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized operating chain manifests."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used to resolve manifest paths."),
    ] = Path("."),
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the full Managed/Enterprise operating chain."""
    if export_dir:
        result = write_managed_enterprise_operating_chain_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_operating_chain"] is True
    else:
        payload = (
            json.loads(manifest.read_text(encoding="utf-8"))
            if manifest
            else build_managed_enterprise_operating_chain_manifest(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_operating_chain(
            payload,
            base_dir=repo_root,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_operating_chain"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-operating-certificate")
def release_managed_enterprise_operating_certificate(
    certificate: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise operating certificate JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized operating certificate templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise operating release certificate."""
    if export_dir:
        result = write_managed_enterprise_operating_certificate_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_operating_certificate"] is True
    else:
        payload = (
            json.loads(certificate.read_text(encoding="utf-8"))
            if certificate
            else build_managed_enterprise_operating_certificate(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_operating_certificate(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_operating_certificate"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("managed-enterprise-certificate-publication-index")
def release_managed_enterprise_certificate_publication_index(
    index: Annotated[
        Optional[Path],
        typer.Option(help="Optional Managed/Enterprise certificate publication index JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized publication index templates."),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the Managed/Enterprise certificate publication index."""
    if export_dir:
        result = write_managed_enterprise_certificate_publication_index_artifacts(export_dir)
        exit_ok = result["ready_for_managed_enterprise_certificate_publication"] is True
    else:
        payload = (
            json.loads(index.read_text(encoding="utf-8"))
            if index
            else build_managed_enterprise_certificate_publication_index(
                evidence_mode="live" if require_live else "sample",
            )
        )
        result = validate_managed_enterprise_certificate_publication_index(
            payload,
            require_live=require_live,
        )
        exit_ok = result["blocker_count"] == 0 and (
            not require_live
            or result["ready_for_managed_enterprise_certificate_publication"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("roadmap-intake-gate")
def release_roadmap_intake_gate(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional roadmap intake gate packet JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized roadmap intake packets."),
    ] = None,
    change_type: Annotated[
        str,
        typer.Option(help="Change type to use when building a default packet."),
    ] = "customer_monitoring_cycle",
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the roadmap intake gate."""
    if export_dir:
        result = write_roadmap_intake_gate_artifacts(export_dir)
        exit_ok = result["ready_for_roadmap_intake_decision"] is True
    else:
        payload = (
            json.loads(packet.read_text(encoding="utf-8"))
            if packet
            else build_roadmap_intake_gate_packet(
                evidence_mode="live" if require_live else "sample",
                requested_change_type=change_type,
            )
        )
        result = validate_roadmap_intake_gate_packet(payload, require_live=require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not require_live or result["ready_for_roadmap_intake_decision"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("roadmap-candidate-charter")
def release_roadmap_candidate_charter(
    charter: Annotated[
        Optional[Path],
        typer.Option(help="Optional roadmap candidate charter JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized roadmap candidate charters."),
    ] = None,
    change_type: Annotated[
        str,
        typer.Option(help="Change type to use when building a default charter."),
    ] = "new_product_capability",
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the roadmap candidate charter."""
    if export_dir:
        result = write_roadmap_candidate_charter_artifacts(export_dir)
        exit_ok = result["ready_for_roadmap_candidate_charter"] is True
    else:
        payload = (
            json.loads(charter.read_text(encoding="utf-8"))
            if charter
            else build_roadmap_candidate_charter(
                evidence_mode="live" if require_live else "sample",
                requested_change_type=change_type,
            )
        )
        result = validate_roadmap_candidate_charter(payload, require_live=require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not require_live or result["ready_for_roadmap_candidate_charter"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("roadmap-future-phase-opening-gate")
def release_roadmap_future_phase_opening_gate(
    gate: Annotated[
        Optional[Path],
        typer.Option(help="Optional roadmap future phase opening gate JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized future phase opening gates."),
    ] = None,
    change_type: Annotated[
        str,
        typer.Option(help="Change type to use when building a default future phase opening gate."),
    ] = "new_product_capability",
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the roadmap future phase opening gate."""
    if export_dir:
        result = write_roadmap_future_phase_opening_gate_artifacts(export_dir)
        exit_ok = result["ready_for_roadmap_future_phase_opening"] is True
    else:
        payload = (
            json.loads(gate.read_text(encoding="utf-8"))
            if gate
            else build_roadmap_future_phase_opening_gate(
                evidence_mode="live" if require_live else "sample",
                requested_change_type=change_type,
            )
        )
        result = validate_roadmap_future_phase_opening_gate(payload, require_live=require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not require_live or result["ready_for_roadmap_future_phase_opening"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("roadmap-future-phase-registry")
def release_roadmap_future_phase_registry(
    registry: Annotated[
        Optional[Path],
        typer.Option(help="Optional roadmap future phase registry JSON."),
    ] = None,
    export_dir: Annotated[
        Optional[Path],
        typer.Option(help="Optional directory to export sample and live sanitized future phase registries."),
    ] = None,
    change_type: Annotated[
        str,
        typer.Option(help="Change type to use when building a default future phase registry."),
    ] = "new_product_capability",
    output: Annotated[
        Optional[Path],
        typer.Option(help="Optional path for the validation result JSON."),
    ] = None,
    require_live: Annotated[
        bool,
        typer.Option(help="Require evidence_mode=live and sanitized=true."),
    ] = False,
) -> None:
    """Validate or export the roadmap future phase registry."""
    if export_dir:
        result = write_roadmap_future_phase_registry_artifacts(export_dir)
        exit_ok = result["ready_for_roadmap_future_phase_registry"] is True
    else:
        payload = (
            json.loads(registry.read_text(encoding="utf-8"))
            if registry
            else build_roadmap_future_phase_registry(
                evidence_mode="live" if require_live else "sample",
                requested_change_type=change_type,
            )
        )
        result = validate_roadmap_future_phase_registry(payload, require_live=require_live)
        exit_ok = result["blocker_count"] == 0 and (
            not require_live or result["ready_for_roadmap_future_phase_registry"] is True
        )
    payload_json = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload_json, encoding="utf-8")
    print(payload_json, end="")
    if not exit_ok:
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-announcement")
def release_customer_lifecycle_announcement(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle announcement packet JSON.")] = None,
    index: Annotated[Optional[Path], typer.Option(help="Optional lifecycle verification index JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for index generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle closeout announcement packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_announcement_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            index_payload = json.loads(index.read_text(encoding="utf-8")) if index else None
            payload = build_customer_lifecycle_announcement_packet(
                index_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_announcement_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_announcement_packet"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-retrospective")
def release_customer_lifecycle_retrospective(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle retrospective packet JSON.")] = None,
    announcement: Annotated[Optional[Path], typer.Option(help="Optional lifecycle announcement packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for announcement generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle retrospective packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_retrospective_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            announcement_payload = json.loads(announcement.read_text(encoding="utf-8")) if announcement else None
            payload = build_customer_lifecycle_retrospective_packet(
                announcement_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_retrospective_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_retrospective"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-backlog")
def release_customer_lifecycle_phase8_backlog(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle Phase 8 backlog packet JSON.")] = None,
    retrospective: Annotated[Optional[Path], typer.Option(help="Optional lifecycle retrospective packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for retrospective generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 backlog packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_backlog_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            retrospective_payload = json.loads(retrospective.read_text(encoding="utf-8")) if retrospective else None
            payload = build_customer_lifecycle_phase8_backlog_packet(
                retrospective_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_backlog_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_backlog"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-kickoff")
def release_customer_lifecycle_phase8_kickoff(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle Phase 8 kickoff packet JSON.")] = None,
    backlog: Annotated[Optional[Path], typer.Option(help="Optional lifecycle Phase 8 backlog packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for backlog generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 kickoff packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_kickoff_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            backlog_payload = json.loads(backlog.read_text(encoding="utf-8")) if backlog else None
            payload = build_customer_lifecycle_phase8_kickoff_packet(
                backlog_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_kickoff_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_kickoff"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-sprint1-checkpoint")
def release_customer_lifecycle_phase8_sprint1_checkpoint(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle Phase 8 Sprint 1 packet JSON.")] = None,
    kickoff: Annotated[Optional[Path], typer.Option(help="Optional lifecycle Phase 8 kickoff packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for kickoff generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 Sprint 1 checkpoint packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_sprint1_checkpoint_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            kickoff_payload = json.loads(kickoff.read_text(encoding="utf-8")) if kickoff else None
            payload = build_customer_lifecycle_phase8_sprint1_checkpoint_packet(
                kickoff_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_sprint1_checkpoint_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_sprint1_checkpoint"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-telemetry-depth")
def release_customer_lifecycle_phase8_telemetry_depth(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle Phase 8 telemetry packet JSON.")] = None,
    sprint1: Annotated[Optional[Path], typer.Option(help="Optional lifecycle Phase 8 Sprint 1 packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for Sprint 1 generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 telemetry depth packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_telemetry_depth_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            sprint1_payload = json.loads(sprint1.read_text(encoding="utf-8")) if sprint1 else None
            payload = build_customer_lifecycle_phase8_telemetry_depth_packet(
                sprint1_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_telemetry_depth_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_telemetry_depth"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-support-automation")
def release_customer_lifecycle_phase8_support_automation(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle Phase 8 support packet JSON.")] = None,
    sprint1: Annotated[Optional[Path], typer.Option(help="Optional lifecycle Phase 8 Sprint 1 packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for Sprint 1 generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 support automation packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_support_automation_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            sprint1_payload = json.loads(sprint1.read_text(encoding="utf-8")) if sprint1 else None
            payload = build_customer_lifecycle_phase8_support_automation_packet(
                sprint1_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_support_automation_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_support_automation"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-lifecycle-analytics")
def release_customer_lifecycle_phase8_lifecycle_analytics(
    packet: Annotated[Optional[Path], typer.Option(help="Optional customer lifecycle Phase 8 analytics packet JSON.")] = None,
    sprint1: Annotated[Optional[Path], typer.Option(help="Optional lifecycle Phase 8 Sprint 1 packet JSON.")] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for Sprint 1 generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 lifecycle analytics packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_lifecycle_analytics_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            sprint1_payload = json.loads(sprint1.read_text(encoding="utf-8")) if sprint1 else None
            payload = build_customer_lifecycle_phase8_lifecycle_analytics_packet(
                sprint1_payload,
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_lifecycle_analytics_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_lifecycle_analytics"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-customer-health-review")
def release_customer_lifecycle_phase8_customer_health_review(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 customer health review packet JSON."),
    ] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for source gate generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 customer health review packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_customer_health_review_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_customer_health_review_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_customer_health_review_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_customer_health_review"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-executive-health-rollup")
def release_customer_lifecycle_phase8_executive_health_rollup(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 executive health rollup packet JSON."),
    ] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root used for source health review generation.")] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 executive health rollup packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_executive_health_rollup_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_executive_health_rollup_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_executive_health_rollup_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_executive_health_rollup"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-executive-action-plan")
def release_customer_lifecycle_phase8_executive_action_plan(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 executive action plan packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source executive rollup generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 executive action plan packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_executive_action_plan_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_executive_action_plan_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_executive_action_plan_packet(payload, require_live=require_live)
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (require_live and not result["ready_for_customer_lifecycle_phase8_executive_action_plan"]):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-action-followup-checkpoint")
def release_customer_lifecycle_phase8_action_followup_checkpoint(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 action follow-up checkpoint packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source executive action plan generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 action follow-up checkpoint packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_action_followup_checkpoint_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_action_followup_checkpoint_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_action_followup_checkpoint_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_action_followup_checkpoint"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-executive-followup-closeout")
def release_customer_lifecycle_phase8_executive_followup_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 executive follow-up closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source action follow-up checkpoint generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 executive follow-up closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_executive_followup_closeout_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_executive_followup_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_executive_followup_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_executive_followup_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-next-cycle-readiness-index")
def release_customer_lifecycle_phase8_next_cycle_readiness_index(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 next-cycle readiness index packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source executive follow-up closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 next-cycle readiness index packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_next_cycle_readiness_index_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_next_cycle_readiness_index_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_next_cycle_readiness_index"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-operating-scorecard")
def release_customer_lifecycle_phase8_public_operating_scorecard(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public operating scorecard packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source next-cycle readiness index generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public operating scorecard packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_operating_scorecard_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_operating_scorecard_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_operating_scorecard_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_operating_scorecard"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-publication-closeout")
def release_customer_lifecycle_phase8_public_scorecard_publication_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard publication closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public operating scorecard generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard publication closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_publication_closeout_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_publication_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_publication_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-refresh-checkpoint")
def release_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard refresh checkpoint packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard publication closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard refresh checkpoint packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_checkpoint"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-refresh-closeout")
def release_customer_lifecycle_phase8_public_scorecard_refresh_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard refresh closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard refresh checkpoint generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard refresh closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_refresh_closeout_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_refresh_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_refresh_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-operating-loop-index")
def release_customer_lifecycle_phase8_public_scorecard_operating_loop_index(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard operating loop index packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard refresh closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard operating loop index packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_operating_loop_index_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_operating_loop_index_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_operating_loop_index"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-executive-summary-closeout")
def release_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard executive summary closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard operating loop index generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard executive summary closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_executive_summary_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-distribution-readiness")
def release_customer_lifecycle_phase8_public_scorecard_distribution_readiness(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard distribution readiness packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard executive summary closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard distribution readiness packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_distribution_readiness_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_distribution_readiness_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_readiness"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-distribution-closeout")
def release_customer_lifecycle_phase8_public_scorecard_distribution_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard distribution closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard distribution readiness generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard distribution closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_distribution_closeout_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_distribution_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-distribution-audit-index")
def release_customer_lifecycle_phase8_public_scorecard_distribution_audit_index(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard distribution audit index packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard distribution closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard distribution audit index packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_distribution_audit_index_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_distribution_audit_index"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-audit-review-closeout")
def release_customer_lifecycle_phase8_public_scorecard_audit_review_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard audit review closeout packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard distribution audit index generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard audit review closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_artifacts(export_dir, root)
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_audit_review_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live and not result["ready_for_customer_lifecycle_phase8_public_scorecard_audit_review_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-continuous-monitoring-readiness")
def release_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness(
    packet: Annotated[
        Optional[Path],
        typer.Option(
            help="Optional customer lifecycle Phase 8 public scorecard continuous monitoring readiness packet JSON."
        ),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard audit review closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard continuous monitoring readiness packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_continuous_monitoring_readiness"
        ]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-monitoring-activation-closeout")
def release_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(
            help="Optional customer lifecycle Phase 8 public scorecard monitoring activation closeout packet JSON."
        ),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard continuous monitoring readiness generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard monitoring activation closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_activation_closeout"
        ]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-monitoring-first-cycle-review")
def release_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard monitoring first-cycle review packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard monitoring activation closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard monitoring first-cycle review packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_first_cycle_review"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-monitoring-drift-remediation-closeout")
def release_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(
            help="Optional customer lifecycle Phase 8 public scorecard monitoring drift remediation closeout packet JSON."
        ),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard monitoring first-cycle review generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard monitoring drift remediation closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_drift_remediation_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-readiness")
def release_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard monitoring second-cycle readiness packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard monitoring drift remediation closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle readiness packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_readiness"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-activation-closeout")
def release_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(
            help="Optional customer lifecycle Phase 8 public scorecard monitoring second-cycle activation closeout packet JSON."
        ),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard monitoring second-cycle readiness generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle activation closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_activation_closeout"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-first-review")
def release_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review(
    packet: Annotated[
        Optional[Path],
        typer.Option(help="Optional customer lifecycle Phase 8 public scorecard monitoring second-cycle first review packet JSON."),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard monitoring second-cycle activation closeout generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle first review packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result["ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_first_review"]
    ):
        raise typer.Exit(code=1)


@release_app.command("customer-lifecycle-phase8-public-scorecard-monitoring-second-cycle-drift-remediation-closeout")
def release_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout(
    packet: Annotated[
        Optional[Path],
        typer.Option(
            help=(
                "Optional customer lifecycle Phase 8 public scorecard monitoring second-cycle drift "
                "remediation closeout packet JSON."
            )
        ),
    ] = None,
    repo_root: Annotated[
        Path,
        typer.Option(help="Repository root used for source public scorecard monitoring second-cycle first review generation."),
    ] = Path("."),
    export_dir: Annotated[Optional[Path], typer.Option(help="Optional directory to export sample/live packets.")] = None,
    require_live: Annotated[bool, typer.Option(help="Require evidence_mode=live and sanitized=true.")] = False,
) -> None:
    """Validate or export the customer lifecycle Phase 8 public scorecard monitoring second-cycle drift remediation closeout packet."""
    root = repo_root.resolve()
    if export_dir:
        result = write_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_artifacts(
            export_dir,
            root,
        )
    else:
        if packet:
            payload = json.loads(packet.read_text(encoding="utf-8"))
        else:
            payload = build_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
                repo_root=root,
                evidence_mode="live" if require_live else "sample",
            )
        result = validate_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout_packet(
            payload,
            require_live=require_live,
        )
    print(json.dumps(result, indent=2))
    if result["blocker_count"] or (
        require_live
        and not result[
            "ready_for_customer_lifecycle_phase8_public_scorecard_monitoring_second_cycle_drift_remediation_closeout"
        ]
    ):
        raise typer.Exit(code=1)


@release_app.command("verify-go-package")
def verify_go_package(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory.")],
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for release artifacts.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable verification output."),
) -> None:
    """Verify a CAVRA Go runtime release package."""
    result = verify_go_release_package(
        package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    if json_output:
        _print_json(result.to_dict())
    else:
        status = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status}[/] {result.package_dir}")
        for artifact in result.verified_artifacts:
            console.print(f"  artifact: {artifact}")
        for subject in result.verified_provenance:
            console.print(f"  provenance: {subject}")
        for signature in result.verified_signatures:
            console.print(f"  signature: {signature}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("verify-airgap-bundle")
def verify_airgap_bundle(
    bundle_path: Annotated[Path, typer.Argument(help="Air-gapped Go runtime zip bundle.")],
    extract_dir: Annotated[Optional[Path], typer.Option(help="Optional directory for extracted verification files.")] = None,
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for release artifacts.",
    ),
    require_bootstrap: bool = typer.Option(
        True,
        "--require-bootstrap/--allow-missing-bootstrap",
        help="Require offline trust-root bootstrap metadata.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable verification output."),
) -> None:
    """Verify an air-gapped CAVRA Go runtime release zip."""
    result = verify_go_airgap_bundle(
        bundle_path,
        extract_dir=extract_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
        require_bootstrap=require_bootstrap,
    )
    if json_output:
        _print_json(result.to_dict())
    else:
        status = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status}[/] {result.bundle_path}")
        for member in result.verified_members:
            console.print(f"  bundle member: {member}")
        for item in result.verified_bootstrap:
            console.print(f"  offline bootstrap: {item}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("validate-upgrade")
def validate_upgrade(
    previous_package_dir: Annotated[Path, typer.Argument(help="Previously approved Go release package directory.")],
    candidate_package_dir: Annotated[Path, typer.Argument(help="Candidate Go release package directory.")],
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for both release packages.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for both release packages.",
    ),
    allow_same_version: bool = typer.Option(
        False,
        "--allow-same-version",
        help="Allow rebuilt release candidates with the same semantic version.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable validation output."),
) -> None:
    """Validate a Go runtime release-candidate upgrade before promotion."""
    result = validate_go_release_upgrade(
        previous_package_dir,
        candidate_package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
        allow_same_version=allow_same_version,
    )
    if json_output:
        _print_json(result.to_dict())
    else:
        status = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status}[/] release upgrade")
        console.print(f"  previous: {result.previous_version or 'unknown'}")
        console.print(f"  candidate: {result.candidate_version or 'unknown'}")
        for binary in result.artifact_changes.get("added_binaries", []):
            console.print(f"  added binary: {binary}")
        for control in result.control_changes.get("added", []):
            console.print(f"  added control: {control}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("smoke-installers")
def smoke_installers(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory.")],
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for release artifacts.",
    ),
    execute_native: bool = typer.Option(
        True,
        "--execute-native/--skip-execution",
        help="Execute the packaged binary matching the current OS and architecture.",
    ),
    timeout_seconds: float = typer.Option(5.0, "--timeout-seconds", help="Native binary smoke-test timeout."),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable validation output."),
) -> None:
    """Smoke-test Go runtime installer metadata and the native packaged binary."""
    result = smoke_test_go_installers(
        package_dir,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
        execute_native=execute_native,
        timeout_seconds=timeout_seconds,
    )
    if json_output:
        _print_json(result.to_dict())
    else:
        status = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status}[/] installer smoke validation")
        for target in result.verified_targets:
            console.print(f"  target: {target}")
        for target in result.executed_targets:
            console.print(f"  executed: {target}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("channel-manifest")
def channel_manifest(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory.")],
    channel: Annotated[Optional[str], typer.Option(help="Optional channel to inspect, such as stable, beta, or canary.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable channel output."),
) -> None:
    """Inspect release package channel metadata for managed workstations."""
    path = package_dir / "cavra-runtime.channels.json"
    try:
        payload = load_release_channel_manifest(path)
    except (OSError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    if channel:
        channels = [item for item in payload.get("channels", []) if isinstance(item, dict) and item.get("channel") == channel]
        if not channels:
            console.print(f"[red]release channel not found: {channel}[/red]")
            raise typer.Exit(code=1)
        payload = payload | {"channels": channels}
    if json_output:
        _print_json(payload)
    else:
        console.print(f"[green]release channels[/green] {path}")
        for item in payload.get("channels", []):
            console.print(
                f"  {item.get('channel')}: {item.get('version')} "
                f"targets={len(item.get('workstation_targets', []))} auto_update={item.get('auto_update')}"
            )


@release_app.command("updater-policy")
def updater_policy(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory.")],
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable updater policy output."),
) -> None:
    """Inspect managed workstation updater policy for a release package."""
    path = package_dir / "cavra-runtime.updater-policy.json"
    try:
        payload = load_workstation_updater_policy(path)
    except (OSError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    if json_output:
        _print_json(payload)
    else:
        console.print(f"[green]updater policy[/green] {path}")
        console.print(f"  default_auto_update: {payload.get('default_auto_update')}")
        for item in payload.get("policies", []):
            console.print(
                f"  {item.get('channel')}: approval={item.get('approval_required')} "
                f"rings={len(item.get('rollout_rings', []))}"
            )


@release_app.command("request-channel-promotion")
def request_channel_promotion(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for signed channel promotion request artifacts.")] = Path(
        ".cavra/release/channel-promotion"
    ),
    channel: Annotated[str, typer.Option(help="Release channel to promote, such as stable, beta, or canary.")] = "stable",
    target_ring: Annotated[str, typer.Option(help="Endpoint rollout ring to publish into.")] = "enterprise",
    requested_by: Annotated[str, typer.Option(help="Actor or automation identity requesting promotion.")] = "release-manager",
    approver_group: Annotated[str, typer.Option(help="Approval group for channel promotion review.")] = "Endpoint Change Advisory Board",
    ttl_hours: Annotated[int, typer.Option(help="Approval request time to live in hours.")] = 24,
    signing_key: Annotated[Optional[Path], typer.Option(help="Optional Ed25519 private key PEM path. Defaults to CAVRA_RELEASE_CHANNEL_SIGNING_KEY or CAVRA_GO_RELEASE_SIGNING_KEY.")] = None,
    signer: Annotated[str, typer.Option(help="Signer identity recorded in the channel promotion request signature.")] = "release-manager",
    approval_store: Annotated[Optional[Path], typer.Option(help="Optional JSON approval store to upsert the generated approval.")] = None,
    approval_sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval store to upsert the generated approval.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index promotion request history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index promotion request history.")] = None,
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for referenced release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for referenced release artifacts.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable channel promotion output."),
) -> None:
    """Create a signed approval request for release channel promotion."""
    signing_key_pem = signing_key.read_text(encoding="utf-8") if signing_key else None
    try:
        result = create_release_channel_promotion_request(
            package_dir,
            output_dir=output,
            channel=channel,
            target_ring=target_ring,
            requested_by=requested_by,
            approver_group=approver_group,
            ttl_hours=ttl_hours,
            signing_key_pem=signing_key_pem,
            signer=signer,
            require_signatures=require_signatures,
            require_provenance=require_provenance,
        )
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    persisted: list[str] = []
    if result.valid and result.approval:
        if approval_store:
            ApprovalStore(approval_store).upsert(result.approval)
            persisted.append(str(approval_store))
        if approval_sqlite:
            SQLiteApprovalStore(approval_sqlite).upsert(result.approval)
            persisted.append(str(approval_sqlite))
    metadata = None
    indexed_metadata_stores: list[str] = []
    if result.valid and result.request:
        metadata, indexed_metadata_stores = _index_release_metadata(
            build_release_channel_promotion_request_metadata(result.request, package_dir=package_dir, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {
        "approval_stores": persisted,
        "metadata": metadata,
        "indexed_metadata_stores": indexed_metadata_stores,
    }
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] release channel promotion request")
        if result.channel:
            console.print(f"  channel: {result.channel}")
        if result.approval:
            console.print(f"  approval: {result.approval['approval_id']}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in persisted:
            console.print(f"  approval store: {store}")
        for store in indexed_metadata_stores:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("export-endpoint-management")
def export_endpoint_management(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for endpoint-management export artifacts.")] = Path(
        ".cavra/release/endpoint-management-export"
    ),
    channel: Annotated[str, typer.Option(help="Release channel to export, such as stable, beta, or canary.")] = "stable",
    provider: Annotated[str, typer.Option(help="all, jamf, intune, or linux.")] = "all",
    promotion_request: Annotated[Optional[Path], typer.Option(help="Optional signed release channel promotion request JSON to link.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index endpoint export history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index endpoint export history.")] = None,
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for referenced release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for referenced release artifacts.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable endpoint export output."),
) -> None:
    """Export Jamf, Intune, and Linux endpoint-management bundles for a release channel."""
    try:
        promotion_payload = json.loads(promotion_request.read_text(encoding="utf-8")) if promotion_request else None
        result = export_endpoint_management_bundles(
            package_dir,
            output,
            channel=channel,
            provider=provider,
            promotion_request=promotion_payload,
            require_signatures=require_signatures,
            require_provenance=require_provenance,
        )
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata = None
    indexed_metadata_stores: list[str] = []
    if result.valid and result.manifest:
        metadata, indexed_metadata_stores = _index_release_metadata(
            build_endpoint_management_export_metadata(result.manifest, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed_metadata_stores}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint-management export")
        for provider_name in result.providers:
            console.print(f"  provider: {provider_name}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed_metadata_stores:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("deliver-endpoint-export")
def deliver_endpoint_export(
    export_manifest: Annotated[Path, typer.Argument(help="endpoint-management-export-manifest.json path.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for connector delivery evidence.")] = Path(
        ".cavra/release/endpoint-publication-deliveries"
    ),
    provider: Annotated[str, typer.Option(help="all, jamf, intune, or linux.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Publish an endpoint-management export to Jamf, Intune, or Linux fleet connectors."""
    try:
        manifest = json.loads(export_manifest.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("endpoint-management export manifest JSON must be an object")
        event_result = build_endpoint_management_publication_event(
            manifest,
            export_dir=export_manifest.parent,
            provider=provider,
        )
        if not event_result.valid or event_result.event is None:
            payload = event_result.to_dict()
            if json_output:
                _print_json(payload)
            else:
                for error in event_result.errors:
                    console.print(f"  [red]error:[/] {error}")
            raise typer.Exit(code=1)
        result = deliver_connector_event(
            event_result.event,
            load_connector_config(config),
            provider=provider,
            retries=retries,
            timeout_seconds=timeout_seconds,
        )
        path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_management_publication_metadata(
            result,
            event_result.event,
            delivery_evidence=path,
        ),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = event_result.to_dict() | {
        "delivery": result,
        "delivery_evidence": str(path),
        "metadata": metadata,
        "indexed_metadata_stores": indexed,
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(result, indent=2)))
        console.print(f"[green]endpoint export connector delivery evidence exported[/green] {path}")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("ingest-endpoint-inventory")
def ingest_endpoint_inventory_command(
    source_inventory: Annotated[Path, typer.Argument(help="Provider endpoint inventory export JSON file.")],
    provider: Annotated[str, typer.Option(help="Inventory provider: jamf, intune, linux, or edr.")] = "linux",
    output: Annotated[Path, typer.Option(help="Output directory for normalized inventory artifacts.")] = Path(
        ".cavra/release/endpoint-inventory"
    ),
    channel: Annotated[Optional[str], typer.Option(help="Optional release channel for the observed inventory.")] = None,
    observed_at: Annotated[Optional[str], typer.Option(help="Override observed timestamp for normalized inventory.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index ingestion history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index ingestion history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable ingestion output."),
) -> None:
    """Normalize provider endpoint inventory exports into CAVRA endpoint observations."""
    try:
        payload = json.loads(source_inventory.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("source inventory must be a JSON object")
        result = ingest_endpoint_inventory(
            provider,
            payload,
            output_dir=output,
            channel=channel,
            observed_at=observed_at,
            source=str(source_inventory),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata = None
    indexed: list[str] = []
    if result.valid and result.ingestion:
        metadata, indexed = _index_release_metadata(
            build_endpoint_inventory_ingestion_metadata(result.ingestion, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint inventory ingestion")
        if result.inventory_id:
            console.print(f"  inventory: {result.inventory_id}")
        if result.provider:
            console.print(f"  provider: {result.provider}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("reconcile-endpoint-deployment")
def reconcile_endpoint_deployment(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory containing cavra-runtime.endpoint-deployment.json.")],
    observed_inventory: Annotated[Path, typer.Argument(help="Observed endpoint inventory JSON file.")],
    output: Annotated[Path, typer.Option(help="Output directory for reconciliation report artifacts.")] = Path(
        ".cavra/release/endpoint-reconciliation"
    ),
    stale_after_hours: Annotated[int, typer.Option(help="Hours after which endpoint observations are stale.")] = 24,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index reconciliation history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index reconciliation history.")] = None,
    require_package_verification: bool = typer.Option(
        True,
        "--require-package-verification/--skip-package-verification",
        help="Verify the Go release package before reconciling observed endpoints.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable reconciliation output."),
) -> None:
    """Compare desired signed endpoint deployment state with observed endpoint inventory."""
    try:
        desired_manifest = json.loads((package_dir / "cavra-runtime.endpoint-deployment.json").read_text(encoding="utf-8"))
        observed_payload = json.loads(observed_inventory.read_text(encoding="utf-8"))
        if not isinstance(desired_manifest, dict) or not isinstance(observed_payload, dict):
            raise ValueError("desired manifest and observed inventory must be JSON objects")
        result = reconcile_managed_endpoint_deployment(
            desired_manifest,
            observed_payload,
            package_dir=package_dir,
            output_dir=output,
            stale_after_hours=stale_after_hours,
            require_package_verification=require_package_verification,
        )
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata = None
    indexed: list[str] = []
    if result.valid and result.report:
        metadata, indexed = _index_release_metadata(
            build_managed_endpoint_reconciliation_metadata(result.report, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = result.drift_status or "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint deployment reconciliation")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("capture-rollout")
def capture_rollout(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for rollout evidence artifacts.")] = Path(
        ".cavra/release/rollout"
    ),
    deployment_id: Annotated[Optional[list[str]], typer.Option(help="Endpoint deployment target ID. Repeatable.")] = None,
    environment: Annotated[str, typer.Option(help="Target environment label.")] = "production",
    rollout_id: Annotated[Optional[str], typer.Option(help="Explicit rollout ID.")] = None,
    rollout_ring: Annotated[str, typer.Option(help="Rollout ring, such as staging, pilot, or production.")] = "staging",
    status: Annotated[str, typer.Option(help="planned, staged, succeeded, failed, or rolled_back.")] = "planned",
    actor: Annotated[str, typer.Option(help="Operator or automation identity capturing the rollout evidence.")] = "release-manager",
    change_record: Annotated[str, typer.Option(help="Change ticket or release approval reference.")] = "unassigned",
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for release artifacts.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable evidence output."),
) -> None:
    """Capture rollout evidence for managed endpoint deployment targets."""
    result = capture_managed_endpoint_rollout_evidence(
        package_dir,
        output,
        deployment_ids=deployment_id,
        environment=environment,
        rollout_id=rollout_id,
        rollout_ring=rollout_ring,
        status=status,
        actor=actor,
        change_record=change_record,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    if json_output:
        _print_json(result.to_dict())
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint rollout evidence")
        if result.rollout_id:
            console.print(f"  rollout: {result.rollout_id}")
        for target in result.deployment_targets:
            console.print(f"  target: {target}")
        for file in result.files:
            console.print(f"  file: {file}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("verify-rollout")
def verify_rollout(
    rollout_dir: Annotated[Path, typer.Argument(help="Managed endpoint rollout evidence directory.")],
    package_dir: Annotated[Optional[Path], typer.Option(help="Override Go release package directory for source artifact verification.")] = None,
    require_package_verification: bool = typer.Option(
        True,
        "--require-package-verification/--skip-package-verification",
        help="Verify the referenced release package while verifying rollout evidence.",
    ),
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for referenced release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for referenced release artifacts.",
    ),
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to upsert rollout metadata.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to upsert rollout metadata.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable verification output."),
) -> None:
    """Verify managed endpoint rollout evidence and optionally index its metadata."""
    result = verify_managed_endpoint_rollout_evidence(
        rollout_dir,
        package_dir=package_dir,
        require_package_verification=require_package_verification,
        require_signatures=require_signatures,
        require_provenance=require_provenance,
    )
    indexed: list[str] = []
    if result.valid and result.metadata:
        if metadata_json:
            EvidenceMetadataStore(metadata_json).upsert(result.metadata)
            indexed.append(str(metadata_json))
        if sqlite:
            SQLiteEvidenceMetadataStore(sqlite).upsert(result.metadata)
            indexed.append(str(sqlite))
    payload = result.to_dict() | {"indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint rollout evidence")
        if result.rollout_id:
            console.print(f"  rollout: {result.rollout_id}")
        for artifact in result.verified_artifacts:
            console.print(f"  artifact: {artifact}")
        for target in result.deployment_targets:
            console.print(f"  target: {target}")
        for store in indexed:
            console.print(f"  indexed: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("request-rollout-promotion")
def request_rollout_promotion(
    rollout_dir: Annotated[Path, typer.Argument(help="Managed endpoint rollout evidence directory.")],
    output: Annotated[Path, typer.Option(help="Output directory for signed promotion request artifacts.")] = Path(
        ".cavra/release/rollout-promotion"
    ),
    target_ring: Annotated[str, typer.Option(help="Target rollout ring to promote into.")] = "production",
    requested_by: Annotated[str, typer.Option(help="Actor or automation identity requesting promotion.")] = "release-manager",
    approver_group: Annotated[str, typer.Option(help="Approval group for promotion review.")] = "Change Advisory Board",
    ttl_hours: Annotated[int, typer.Option(help="Approval request time to live in hours.")] = 24,
    signing_key: Annotated[Optional[Path], typer.Option(help="Optional Ed25519 private key PEM path. Defaults to CAVRA_ROLLOUT_PROMOTION_SIGNING_KEY or CAVRA_GO_RELEASE_SIGNING_KEY.")] = None,
    signer: Annotated[str, typer.Option(help="Signer identity recorded in the promotion request signature.")] = "release-manager",
    package_dir: Annotated[Optional[Path], typer.Option(help="Override Go release package directory for source artifact verification.")] = None,
    approval_store: Annotated[Optional[Path], typer.Option(help="Optional JSON approval store to upsert the generated approval.")] = None,
    approval_sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval store to upsert the generated approval.")] = None,
    require_package_verification: bool = typer.Option(
        True,
        "--require-package-verification/--skip-package-verification",
        help="Verify the referenced release package while preparing the promotion request.",
    ),
    require_signatures: bool = typer.Option(
        True,
        "--require-signatures/--allow-unsigned",
        help="Require detached Ed25519 signatures for referenced release artifacts.",
    ),
    require_provenance: bool = typer.Option(
        True,
        "--require-provenance/--allow-missing-provenance",
        help="Require SLSA provenance for referenced release artifacts.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable promotion request output."),
) -> None:
    """Create a signed approval request for endpoint rollout promotion."""
    signing_key_pem = signing_key.read_text(encoding="utf-8") if signing_key else None
    try:
        result = create_managed_endpoint_rollout_promotion_request(
            rollout_dir,
            output_dir=output,
            target_ring=target_ring,
            requested_by=requested_by,
            approver_group=approver_group,
            ttl_hours=ttl_hours,
            signing_key_pem=signing_key_pem,
            signer=signer,
            package_dir=package_dir,
            require_package_verification=require_package_verification,
            require_signatures=require_signatures,
            require_provenance=require_provenance,
        )
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    persisted: list[str] = []
    if result.valid and result.approval:
        if approval_store:
            ApprovalStore(approval_store).upsert(result.approval)
            persisted.append(str(approval_store))
        if approval_sqlite:
            SQLiteApprovalStore(approval_sqlite).upsert(result.approval)
            persisted.append(str(approval_sqlite))
    payload = result.to_dict() | {"approval_stores": persisted}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] rollout promotion request")
        if result.rollout_id:
            console.print(f"  rollout: {result.rollout_id}")
        if result.approval:
            console.print(f"  approval: {result.approval['approval_id']}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in persisted:
            console.print(f"  approval store: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("execute-rollout-promotion")
def execute_rollout_promotion(
    promotion_request: Annotated[Path, typer.Argument(help="Signed rollout promotion request JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for promotion execution artifacts.")] = Path(
        ".cavra/release/rollout-promotion-execution"
    ),
    approval_json: Annotated[Optional[Path], typer.Option(help="Approved approval JSON file.")] = None,
    approval_store: Annotated[Optional[Path], typer.Option(help="JSON approval store containing the approved record.")] = None,
    approval_sqlite: Annotated[Optional[Path], typer.Option(help="SQLite approval store containing the approved record.")] = None,
    approval_id: Annotated[Optional[str], typer.Option(help="Approval ID. Defaults to the request approval_id.")] = None,
    executed_by: Annotated[str, typer.Option(help="Actor or automation identity executing promotion.")] = "release-manager",
    execution_environment: Annotated[Optional[str], typer.Option(help="Environment recorded on the execution artifact.")] = None,
    notes: Annotated[Optional[str], typer.Option(help="Optional execution note.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index the execution.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index the execution.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable promotion execution output."),
) -> None:
    """Record an approved endpoint rollout ring promotion execution."""
    try:
        request_payload = json.loads(promotion_request.read_text(encoding="utf-8"))
        selected_approval_id = approval_id or request_payload.get("approval", {}).get("approval_id")
        approval = _load_release_approval(
            selected_approval_id,
            approval_json=approval_json,
            approval_store=approval_store,
            approval_sqlite=approval_sqlite,
        )
        result = create_managed_endpoint_rollout_promotion_execution(
            request_payload,
            approval,
            output_dir=output,
            executed_by=executed_by,
            execution_environment=execution_environment,
            notes=notes,
        )
    except (OSError, json.JSONDecodeError, KeyError, ValueError, RuntimeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    indexed: list[str] = []
    if result.valid and result.execution:
        metadata = build_managed_endpoint_rollout_promotion_execution_metadata(result.execution, bundle_dir=output)
        if metadata_json:
            EvidenceMetadataStore(metadata_json).upsert(metadata)
            indexed.append(str(metadata_json))
        if sqlite:
            SQLiteEvidenceMetadataStore(sqlite).upsert(metadata)
            indexed.append(str(sqlite))
    payload = result.to_dict() | {"indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] rollout promotion execution")
        if result.rollout_id:
            console.print(f"  rollout: {result.rollout_id}")
        if result.execution:
            console.print(f"  execution: {result.execution['execution_id']}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("execute-rollout-rollback")
def execute_rollout_rollback(
    promotion_execution: Annotated[Path, typer.Argument(help="Approved rollout promotion execution JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for rollback execution artifacts.")] = Path(
        ".cavra/release/rollout-rollback-execution"
    ),
    approval_json: Annotated[Optional[Path], typer.Option(help="Approved rollback approval JSON file.")] = None,
    approval_store: Annotated[Optional[Path], typer.Option(help="JSON approval store containing the approved rollback record.")] = None,
    approval_sqlite: Annotated[Optional[Path], typer.Option(help="SQLite approval store containing the approved rollback record.")] = None,
    approval_id: Annotated[Optional[str], typer.Option(help="Rollback approval ID.")] = None,
    executed_by: Annotated[str, typer.Option(help="Actor or automation identity executing rollback.")] = "release-manager",
    rollback_reason: Annotated[str, typer.Option(help="Rollback reason recorded on the artifact.")] = "Rollback approved from promotion execution audit.",
    execution_environment: Annotated[Optional[str], typer.Option(help="Environment recorded on the rollback artifact.")] = None,
    notes: Annotated[Optional[str], typer.Option(help="Optional rollback execution note.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index the rollback.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index the rollback.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable rollback execution output."),
) -> None:
    """Record an approved endpoint rollout rollback execution."""
    try:
        execution_payload = json.loads(promotion_execution.read_text(encoding="utf-8"))
        approval = _load_release_approval(
            approval_id,
            approval_json=approval_json,
            approval_store=approval_store,
            approval_sqlite=approval_sqlite,
        )
        result = create_managed_endpoint_rollout_rollback_execution(
            execution_payload,
            approval,
            output_dir=output,
            executed_by=executed_by,
            rollback_reason=rollback_reason,
            execution_environment=execution_environment,
            notes=notes,
        )
    except (OSError, json.JSONDecodeError, KeyError, ValueError, RuntimeError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    indexed: list[str] = []
    if result.valid and result.rollback:
        metadata = build_managed_endpoint_rollout_rollback_execution_metadata(result.rollback, bundle_dir=output)
        if metadata_json:
            EvidenceMetadataStore(metadata_json).upsert(metadata)
            indexed.append(str(metadata_json))
        if sqlite:
            SQLiteEvidenceMetadataStore(sqlite).upsert(metadata)
            indexed.append(str(sqlite))
    payload = result.to_dict() | {"indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] rollout rollback execution")
        if result.rollout_id:
            console.print(f"  rollout: {result.rollout_id}")
        if result.rollback:
            console.print(f"  rollback: {result.rollback['rollback_id']}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("export-promotion-audit")
def export_promotion_audit(
    promotion_execution: Annotated[Path, typer.Argument(help="Approved rollout promotion execution JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for SIEM and ITSM audit payloads.")] = Path(
        ".cavra/release/promotion-audit-export"
    ),
    provider: Annotated[str, typer.Option(help="all, splunk, sentinel, datadog, webhook, jira, or servicenow.")] = "all",
    splunk_index: Annotated[str, typer.Option(help="Splunk HEC index name.")] = "cavra",
    datadog_service: Annotated[str, typer.Option(help="Datadog service name.")] = "cavra",
    itsm_project_key: Annotated[str, typer.Option(help="Jira project key for ITSM issue payloads.")] = "CAVRA",
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable export output."),
) -> None:
    """Export SIEM and ITSM audit payloads for a rollout promotion execution."""
    try:
        execution_payload = json.loads(promotion_execution.read_text(encoding="utf-8"))
        result = export_rollout_promotion_execution_audit(
            execution_payload,
            output,
            provider=provider,
            splunk_index=splunk_index,
            datadog_service=datadog_service,
            itsm_project_key=itsm_project_key,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    if json_output:
        _print_json(result.to_dict())
    else:
        console.print(f"[green]promotion audit exported[/green] {result.output_dir}")
        for path in result.files:
            console.print(f"  {path.name}")


@release_app.command("deliver-promotion-audit")
def deliver_promotion_audit(
    promotion_execution: Annotated[Path, typer.Argument(help="Approved rollout promotion execution JSON.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for connector delivery evidence.")] = Path(
        ".cavra/release/promotion-audit-deliveries"
    ),
    provider: Annotated[str, typer.Option(help="all, splunk, sentinel, datadog, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Deliver a rollout promotion audit event through configured connectors."""
    try:
        execution_payload = json.loads(promotion_execution.read_text(encoding="utf-8"))
        event = build_rollout_promotion_execution_audit_event(execution_payload)
        result = deliver_connector_event(
            event,
            load_connector_config(config),
            provider=provider,
            retries=retries,
            timeout_seconds=timeout_seconds,
        )
        path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_connector_delivery(
        result,
        path,
        source="release_governance_promotion",
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = result | {"delivery_evidence": str(path), "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(result, indent=2)))
        console.print(f"[green]promotion audit connector delivery evidence exported[/green] {path}")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("deliver-rollback-execution")
def deliver_rollback_execution(
    rollback_execution: Annotated[Path, typer.Argument(help="Approved rollout rollback execution JSON.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for connector delivery evidence.")] = Path(
        ".cavra/release/rollback-deliveries"
    ),
    provider: Annotated[str, typer.Option(help="all, splunk, sentinel, datadog, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Deliver a rollout rollback execution event through configured connectors."""
    try:
        rollback_payload = json.loads(rollback_execution.read_text(encoding="utf-8"))
        event = build_rollout_rollback_execution_audit_event(rollback_payload)
        result = deliver_connector_event(
            event,
            load_connector_config(config),
            provider=provider,
            retries=retries,
            timeout_seconds=timeout_seconds,
        )
        path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_connector_delivery(
        result,
        path,
        source="release_governance_rollback",
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = result | {"delivery_evidence": str(path), "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(result, indent=2)))
        console.print(f"[green]rollback execution connector delivery evidence exported[/green] {path}")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("connector-delivery-history")
def connector_delivery_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    provider: Annotated[Optional[str], typer.Option(help="Filter by connector provider.")] = None,
    event_type: Annotated[Optional[str], typer.Option(help="Filter by delivered event type.")] = None,
    event_id: Annotated[Optional[str], typer.Option(help="Filter by source promotion or rollback ID.")] = None,
    success: Annotated[Optional[bool], typer.Option(help="Filter successful or failed delivery batches.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show persisted release governance connector delivery history."""
    items = _load_release_connector_delivery_items(metadata_json=metadata_json, sqlite=sqlite)
    result = filter_connector_delivery_history(
        items,
        provider=provider,
        event_type=event_type,
        event_id=event_id,
        success=success,
        limit=limit,
        offset=offset,
    )
    _print_json(result)


@release_app.command("connector-delivery-dashboard")
def connector_delivery_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize release governance connector delivery health and alerts."""
    items = _load_release_connector_delivery_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_connector_delivery_dashboard(items))


@release_app.command("endpoint-publication-history")
def endpoint_publication_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    provider: Annotated[Optional[str], typer.Option(help="Filter by endpoint-management provider.")] = None,
    export_id: Annotated[Optional[str], typer.Option(help="Filter by endpoint-management export ID.")] = None,
    channel: Annotated[Optional[str], typer.Option(help="Filter by release channel.")] = None,
    success: Annotated[Optional[bool], typer.Option(help="Filter successful or failed delivery batches.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show persisted endpoint-management export publication history."""
    items = _load_endpoint_management_publication_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_management_publication_history(
            items,
            provider=provider,
            export_id=export_id,
            channel=channel,
            success=success,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-publication-dashboard")
def endpoint_publication_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint-management publication health and provider failures."""
    items = _load_endpoint_management_publication_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_management_publication_dashboard(items))


@release_app.command("endpoint-reconciliation-history")
def endpoint_reconciliation_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    drift_status: Annotated[Optional[str], typer.Option(help="Filter by aligned or drift_detected.")] = None,
    alert_level: Annotated[Optional[str], typer.Option(help="Filter by healthy, warning, or critical.")] = None,
    deployment_target: Annotated[Optional[str], typer.Option(help="Filter by deployment target ID.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show managed endpoint deployment reconciliation history."""
    items = _load_managed_endpoint_reconciliation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_managed_endpoint_reconciliation_history(
            items,
            drift_status=drift_status,
            alert_level=alert_level,
            deployment_target=deployment_target,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-reconciliation-dashboard")
def endpoint_reconciliation_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize managed endpoint deployment drift and stale endpoint observations."""
    items = _load_managed_endpoint_reconciliation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_managed_endpoint_reconciliation_dashboard(items))


@release_app.command("endpoint-inventory-history")
def endpoint_inventory_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    provider: Annotated[Optional[str], typer.Option(help="Filter by inventory provider.")] = None,
    channel: Annotated[Optional[str], typer.Option(help="Filter by release channel.")] = None,
    deployment_target: Annotated[Optional[str], typer.Option(help="Filter by deployment target ID.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint inventory ingestion history."""
    items = _load_endpoint_inventory_ingestion_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_inventory_ingestion_history(
            items,
            provider=provider,
            channel=channel,
            deployment_target=deployment_target,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-inventory-dashboard")
def endpoint_inventory_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize normalized endpoint inventory coverage by provider."""
    items = _load_endpoint_inventory_ingestion_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_inventory_ingestion_dashboard(items))


@release_app.command("endpoint-inventory-freshness")
def endpoint_inventory_freshness(
    output: Annotated[Path, typer.Option(help="Output directory for endpoint inventory freshness artifacts.")] = Path(
        ".cavra/release/endpoint-inventory-freshness"
    ),
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    provider: Annotated[Optional[str], typer.Option(help="Filter by inventory provider.")] = None,
    channel: Annotated[Optional[str], typer.Option(help="Filter by release channel.")] = None,
    deployment_target: Annotated[Optional[str], typer.Option(help="Filter by deployment target ID.")] = None,
    max_age_hours: Annotated[int, typer.Option(help="Warning SLA threshold in hours.")] = 24,
    critical_age_hours: Annotated[int, typer.Option(help="Critical SLA threshold in hours.")] = 48,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable freshness report output."),
) -> None:
    """Create an endpoint inventory freshness SLA report from indexed ingestions."""
    items = _load_endpoint_inventory_ingestion_items(metadata_json=metadata_json, sqlite=sqlite)
    result = evaluate_endpoint_inventory_freshness(
        items,
        output_dir=output,
        provider=provider,
        channel=channel,
        deployment_target=deployment_target,
        max_age_hours=max_age_hours,
        critical_age_hours=critical_age_hours,
    )
    metadata = None
    indexed: list[str] = []
    if result.valid and result.report:
        metadata, indexed = _index_release_metadata(
            build_endpoint_inventory_freshness_metadata(result.report, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(f"[{'green' if result.valid else 'red'}]{result.alert_level or 'invalid'}[/] endpoint inventory freshness")
        if result.report_id:
            console.print(f"  report: {result.report_id}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("endpoint-inventory-freshness-history")
def endpoint_inventory_freshness_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    alert_level: Annotated[Optional[str], typer.Option(help="Filter by alert level.")] = None,
    provider: Annotated[Optional[str], typer.Option(help="Filter by inventory provider.")] = None,
    channel: Annotated[Optional[str], typer.Option(help="Filter by release channel.")] = None,
    deployment_target: Annotated[Optional[str], typer.Option(help="Filter by deployment target ID.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint inventory freshness report history."""
    items = _load_endpoint_inventory_freshness_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_inventory_freshness_history(
            items,
            alert_level=alert_level,
            provider=provider,
            channel=channel,
            deployment_target=deployment_target,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-inventory-freshness-dashboard")
def endpoint_inventory_freshness_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint inventory freshness SLA alerts."""
    items = _load_endpoint_inventory_freshness_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_inventory_freshness_dashboard(items))


@release_app.command("automate-endpoint-reconciliation")
def automate_endpoint_reconciliation(
    package_dir: Annotated[Path, typer.Argument(help="Go release package directory containing cavra-runtime.endpoint-deployment.json.")],
    inventory_ingestion: Annotated[Path, typer.Argument(help="Endpoint inventory ingestion metadata or observations JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for automation artifacts.")] = Path(
        ".cavra/release/endpoint-reconciliation-automation"
    ),
    stale_after_hours: Annotated[int, typer.Option(help="Hours after which endpoint observations are stale.")] = 24,
    remediation_strategy: Annotated[str, typer.Option(help="Remediation strategy: mixed, republish, or rollback.")] = "mixed",
    requested_by: Annotated[str, typer.Option(help="Actor or automation identity requesting remediation.")] = "release-agent",
    approver_group: Annotated[str, typer.Option(help="Approval group for remediation review.")] = "Endpoint Change Advisory Board",
    ttl_hours: Annotated[int, typer.Option(help="Approval request time to live in hours.")] = 24,
    approval_store: Annotated[Optional[Path], typer.Option(help="Optional JSON approval store to upsert generated approval.")] = None,
    approval_sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval store to upsert generated approval.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index automation records.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index automation records.")] = None,
    require_package_verification: bool = typer.Option(
        False,
        "--require-package-verification/--skip-package-verification",
        help="Verify the Go release package before reconciling observed endpoints.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable automation output."),
) -> None:
    """Reconcile a fresh inventory ingestion and open remediation when drift is detected."""
    try:
        desired_manifest = json.loads((package_dir / "cavra-runtime.endpoint-deployment.json").read_text(encoding="utf-8"))
        ingestion = json.loads(inventory_ingestion.read_text(encoding="utf-8"))
        if not isinstance(desired_manifest, dict) or not isinstance(ingestion, dict):
            raise ValueError("desired manifest and inventory ingestion must be JSON objects")
        result = automate_endpoint_reconciliation_from_ingestion(
            desired_manifest,
            ingestion,
            package_dir=package_dir,
            output_dir=output,
            stale_after_hours=stale_after_hours,
            require_package_verification=require_package_verification,
            remediation_strategy=remediation_strategy,
            requested_by=requested_by,
            approver_group=approver_group,
            ttl_hours=ttl_hours,
        )
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    persisted: list[str] = []
    if result.valid and result.approval:
        if approval_store:
            ApprovalStore(approval_store).upsert(result.approval)
            persisted.append(str(approval_store))
        if approval_sqlite:
            SQLiteApprovalStore(approval_sqlite).upsert(result.approval)
            persisted.append(str(approval_sqlite))
    indexed: list[str] = []
    metadata: dict | None = None
    if result.valid and result.reconciliation:
        _, reconciliation_indexed = _index_release_metadata(
            build_managed_endpoint_reconciliation_metadata(result.reconciliation, bundle_dir=output / "reconciliation"),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        indexed.extend(reconciliation_indexed)
    if result.valid and result.remediation_request:
        _, request_indexed = _index_release_metadata(
            build_endpoint_drift_remediation_request_metadata(result.remediation_request, bundle_dir=output / "remediation-request"),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        indexed.extend(request_indexed)
    if result.valid and result.automation:
        metadata, automation_indexed = _index_release_metadata(
            build_endpoint_reconciliation_automation_metadata(result.automation, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        indexed.extend(automation_indexed)
    payload = result.to_dict() | {
        "approval_stores": persisted,
        "metadata": metadata,
        "indexed_metadata_stores": sorted(set(indexed)),
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(f"[{'green' if result.valid else 'red'}]{result.automation.get('alert_level') if result.automation else 'invalid'}[/] endpoint reconciliation automation")
        if result.automation_id:
            console.print(f"  automation: {result.automation_id}")
        if result.reconciliation_id:
            console.print(f"  reconciliation: {result.reconciliation_id}")
        if result.request_id:
            console.print(f"  remediation request: {result.request_id}")
        for store in persisted:
            console.print(f"  approval store: {store}")
        for store in sorted(set(indexed)):
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("endpoint-reconciliation-automation-history")
def endpoint_reconciliation_automation_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    drift_status: Annotated[Optional[str], typer.Option(help="Filter by drift status.")] = None,
    alert_level: Annotated[Optional[str], typer.Option(help="Filter by alert level.")] = None,
    approval_state: Annotated[Optional[str], typer.Option(help="Filter by approval state.")] = None,
    provider: Annotated[Optional[str], typer.Option(help="Filter by inventory provider.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint reconciliation automation history."""
    items = _load_endpoint_reconciliation_automation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_reconciliation_automation_history(
            items,
            drift_status=drift_status,
            alert_level=alert_level,
            approval_state=approval_state,
            provider=provider,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-reconciliation-automation-dashboard")
def endpoint_reconciliation_automation_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint reconciliation automations and pending remediation approvals."""
    items = _load_endpoint_reconciliation_automation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_reconciliation_automation_dashboard(items))


@release_app.command("request-endpoint-remediation")
def request_endpoint_remediation(
    reconciliation_report: Annotated[Path, typer.Argument(help="Managed endpoint reconciliation report JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for remediation request artifacts.")] = Path(
        ".cavra/release/endpoint-remediation"
    ),
    strategy: Annotated[str, typer.Option(help="Remediation strategy: mixed, republish, or rollback.")] = "mixed",
    requested_by: Annotated[str, typer.Option(help="Actor or automation identity requesting remediation.")] = "release-manager",
    approver_group: Annotated[str, typer.Option(help="Approval group for remediation review.")] = "Endpoint Change Advisory Board",
    ttl_hours: Annotated[int, typer.Option(help="Approval request time to live in hours.")] = 24,
    approval_store: Annotated[Optional[Path], typer.Option(help="Optional JSON approval store to upsert the generated approval.")] = None,
    approval_sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite approval store to upsert the generated approval.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index the request.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index the request.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable remediation request output."),
) -> None:
    """Create an approval-bound endpoint drift remediation plan."""
    try:
        report = json.loads(reconciliation_report.read_text(encoding="utf-8"))
        if not isinstance(report, dict):
            raise ValueError("reconciliation report must be a JSON object")
        result = create_endpoint_drift_remediation_request(
            report,
            output_dir=output,
            strategy=strategy,
            requested_by=requested_by,
            approver_group=approver_group,
            ttl_hours=ttl_hours,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    persisted: list[str] = []
    if result.valid and result.approval:
        if approval_store:
            ApprovalStore(approval_store).upsert(result.approval)
            persisted.append(str(approval_store))
        if approval_sqlite:
            SQLiteApprovalStore(approval_sqlite).upsert(result.approval)
            persisted.append(str(approval_sqlite))
    metadata = None
    indexed: list[str] = []
    if result.valid and result.request:
        metadata, indexed = _index_release_metadata(
            build_endpoint_drift_remediation_request_metadata(result.request, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"approval_stores": persisted, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint remediation request")
        if result.reconciliation_id:
            console.print(f"  reconciliation: {result.reconciliation_id}")
        if result.approval:
            console.print(f"  approval: {result.approval['approval_id']}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in persisted:
            console.print(f"  approval store: {store}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("export-endpoint-remediation-handoff")
def export_endpoint_remediation_handoff(
    remediation_request: Annotated[Path, typer.Argument(help="Endpoint remediation request JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for remediation handoff artifacts.")] = Path(
        ".cavra/release/endpoint-remediation-handoff"
    ),
    provider: Annotated[list[str], typer.Option(help="Handoff provider: jira, servicenow, slack, teams, private_queue, or all.")] = ["all"],
    requested_by: Annotated[str, typer.Option(help="Actor or automation identity exporting the handoff.")] = "release-manager",
    delivery_mode: Annotated[str, typer.Option(help="Handoff mode recorded on the artifact.")] = "manual",
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index the handoff.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index the handoff.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable handoff output."),
) -> None:
    """Export public-safe ITSM, ChatOps, and private connector handoff payloads."""
    try:
        request_payload = json.loads(remediation_request.read_text(encoding="utf-8"))
        if not isinstance(request_payload, dict):
            raise ValueError("remediation request must be a JSON object")
        result = build_endpoint_remediation_handoff(
            request_payload,
            output_dir=output,
            providers=provider,
            requested_by=requested_by,
            delivery_mode=delivery_mode,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    indexed: list[str] = []
    metadata = None
    if result.valid and result.handoff:
        metadata, indexed = _index_release_metadata(
            build_endpoint_remediation_handoff_metadata(result.handoff, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint remediation handoff")
        if result.handoff_id:
            console.print(f"  handoff: {result.handoff_id}")
        if result.request_id:
            console.print(f"  request: {result.request_id}")
        for provider_name in result.providers:
            console.print(f"  provider: {provider_name}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("record-endpoint-remediation-handoff-status")
def record_endpoint_remediation_handoff_status_command(
    handoff_json: Annotated[Path, typer.Argument(help="Endpoint remediation handoff JSON.")],
    provider: Annotated[str, typer.Option(help="Handoff provider reporting status.")] = "private_queue",
    status: Annotated[
        str,
        typer.Option(help="Status: queued, delivered, acknowledged, in_progress, blocked, completed, failed, cancelled."),
    ] = "delivered",
    output: Annotated[Path, typer.Option(help="Output directory for handoff status artifacts.")] = Path(
        ".cavra/release/endpoint-remediation-handoff-status"
    ),
    external_ref: Annotated[Optional[str], typer.Option(help="External ticket, message, or queue job reference.")] = None,
    external_url: Annotated[Optional[str], typer.Option(help="External URL for the ticket, message, or queue job.")] = None,
    callback_json: Annotated[Optional[Path], typer.Option(help="Optional callback payload JSON to preserve with redaction.")] = None,
    recorded_by: Annotated[str, typer.Option(help="Actor or automation identity recording status.")] = "release-manager",
    notes: Annotated[Optional[str], typer.Option(help="Optional status note.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index status.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index status.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable status output."),
) -> None:
    """Record public-safe provider status for an endpoint remediation handoff."""
    try:
        handoff = json.loads(handoff_json.read_text(encoding="utf-8"))
        if not isinstance(handoff, dict):
            raise ValueError("handoff must be a JSON object")
        callback_payload = None
        if callback_json:
            callback_payload = json.loads(callback_json.read_text(encoding="utf-8"))
            if not isinstance(callback_payload, dict):
                raise ValueError("callback payload must be a JSON object")
        result = record_endpoint_remediation_handoff_status(
            handoff,
            provider=provider,
            status=status,
            external_ref=external_ref,
            external_url=external_url,
            callback_payload=callback_payload,
            recorded_by=recorded_by,
            notes=notes,
            output_dir=output,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    indexed: list[str] = []
    metadata = None
    if result.valid and result.status:
        metadata, indexed = _index_release_metadata(
            build_endpoint_remediation_handoff_status_metadata(result.status, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint remediation handoff status")
        if result.status_id:
            console.print(f"  status: {result.status_id}")
        if result.handoff_id:
            console.print(f"  handoff: {result.handoff_id}")
        if result.provider:
            console.print(f"  provider: {result.provider}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("execute-endpoint-remediation")
def execute_endpoint_remediation(
    remediation_request: Annotated[Path, typer.Argument(help="Endpoint remediation request JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for remediation execution artifacts.")] = Path(
        ".cavra/release/endpoint-remediation-execution"
    ),
    approval_json: Annotated[Optional[Path], typer.Option(help="Approved remediation approval JSON file.")] = None,
    approval_store: Annotated[Optional[Path], typer.Option(help="JSON approval store containing the approved record.")] = None,
    approval_sqlite: Annotated[Optional[Path], typer.Option(help="SQLite approval store containing the approved record.")] = None,
    approval_id: Annotated[Optional[str], typer.Option(help="Approval ID. Defaults to the request approval_id.")] = None,
    executed_by: Annotated[str, typer.Option(help="Actor or automation identity recording execution.")] = "release-manager",
    execution_environment: Annotated[Optional[str], typer.Option(help="Environment recorded on the execution artifact.")] = None,
    notes: Annotated[Optional[str], typer.Option(help="Optional execution note.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index the execution.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index the execution.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable remediation execution output."),
) -> None:
    """Record an approved endpoint drift remediation execution."""
    try:
        request_payload = json.loads(remediation_request.read_text(encoding="utf-8"))
        if not isinstance(request_payload, dict):
            raise ValueError("remediation request must be a JSON object")
        request_approval = request_payload.get("approval", {})
        selected_approval_id = approval_id or (
            request_approval.get("approval_id") if isinstance(request_approval, dict) else None
        )
        approval = _load_release_approval(
            selected_approval_id,
            approval_json=approval_json,
            approval_store=approval_store,
            approval_sqlite=approval_sqlite,
        )
        result = execute_endpoint_drift_remediation(
            request_payload,
            approval,
            output_dir=output,
            executed_by=executed_by,
            execution_environment=execution_environment,
            notes=notes,
        )
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    indexed: list[str] = []
    metadata = None
    if result.valid and result.execution:
        metadata, indexed = _index_release_metadata(
            build_endpoint_drift_remediation_execution_metadata(result.execution, bundle_dir=output),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint remediation execution")
        if result.reconciliation_id:
            console.print(f"  reconciliation: {result.reconciliation_id}")
        if result.execution:
            console.print(f"  execution: {result.execution['execution_id']}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("endpoint-remediation-handoff-history")
def endpoint_remediation_handoff_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    provider: Annotated[Optional[str], typer.Option(help="Filter by provider.")] = None,
    approval_state: Annotated[Optional[str], typer.Option(help="Filter by approval state.")] = None,
    request_id: Annotated[Optional[str], typer.Option(help="Filter by remediation request ID.")] = None,
    reconciliation_id: Annotated[Optional[str], typer.Option(help="Filter by reconciliation ID.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint remediation handoff package history."""
    items = _load_endpoint_remediation_handoff_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_handoff_history(
            items,
            provider=provider,
            approval_state=approval_state,
            request_id=request_id,
            reconciliation_id=reconciliation_id,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-handoff-dashboard")
def endpoint_remediation_handoff_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint remediation handoff packages by provider and approval state."""
    items = _load_endpoint_remediation_handoff_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_handoff_dashboard(items))


@release_app.command("endpoint-remediation-handoff-status-history")
def endpoint_remediation_handoff_status_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    provider: Annotated[Optional[str], typer.Option(help="Filter by provider.")] = None,
    handoff_status: Annotated[Optional[str], typer.Option(help="Filter by handoff status.")] = None,
    handoff_id: Annotated[Optional[str], typer.Option(help="Filter by handoff ID.")] = None,
    request_id: Annotated[Optional[str], typer.Option(help="Filter by remediation request ID.")] = None,
    external_ref: Annotated[Optional[str], typer.Option(help="Filter by external reference.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint remediation handoff status history."""
    items = _load_endpoint_remediation_handoff_status_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_handoff_status_history(
            items,
            provider=provider,
            handoff_status=handoff_status,
            handoff_id=handoff_id,
            request_id=request_id,
            external_ref=external_ref,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-handoff-status-dashboard")
def endpoint_remediation_handoff_status_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint remediation handoff status callbacks by provider and state."""
    items = _load_endpoint_remediation_handoff_status_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_handoff_status_dashboard(items))


@release_app.command("endpoint-remediation-sla-report")
def endpoint_remediation_sla_report(
    output: Annotated[Path, typer.Option(help="Output directory for endpoint remediation SLA report artifacts.")] = Path(
        ".cavra/release/endpoint-remediation-sla"
    ),
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    warning_hours: Annotated[int, typer.Option(help="Hours before a handoff is at risk.")] = 24,
    critical_hours: Annotated[int, typer.Option(help="Hours before a handoff breaches SLA.")] = 48,
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity generating the report.")] = "release-manager",
    index_metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index the report.")] = None,
    index_sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index the report.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable SLA report output."),
) -> None:
    """Generate endpoint remediation SLA, escalation, and executive reporting."""
    handoffs = _load_endpoint_remediation_handoff_items(metadata_json=metadata_json, sqlite=sqlite)
    statuses = _load_endpoint_remediation_handoff_status_items(metadata_json=metadata_json, sqlite=sqlite)
    result = build_endpoint_remediation_sla_report(
        handoffs,
        statuses,
        warning_hours=warning_hours,
        critical_hours=critical_hours,
        generated_by=generated_by,
        output_dir=output,
    )
    indexed: list[str] = []
    metadata = None
    if result.valid and result.report:
        metadata, indexed = _index_release_metadata(
            build_endpoint_remediation_sla_report_metadata(result.report, bundle_dir=output),
            metadata_json=index_metadata_json or metadata_json,
            sqlite=index_sqlite,
        )
    payload = result.to_dict() | {"metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        status_text = "valid" if result.valid else "invalid"
        console.print(f"[{'green' if result.valid else 'red'}]{status_text}[/] endpoint remediation SLA report")
        if result.report_id:
            console.print(f"  report: {result.report_id}")
        if result.report:
            summary = result.report.get("executive_summary", {})
            console.print(f"  alert: {result.report.get('alert_level')}")
            console.print(f"  tracked: {summary.get('tracked_work_item_count', 0)}")
            console.print(f"  breached: {summary.get('breached_count', 0)}")
        for file in result.files:
            console.print(f"  file: {file}")
        for store in indexed:
            console.print(f"  indexed metadata: {store}")
        for warning in result.warnings:
            console.print(f"  [yellow]warning:[/] {warning}")
        for error in result.errors:
            console.print(f"  [red]error:[/] {error}")
    if not result.valid:
        raise typer.Exit(code=1)


@release_app.command("deliver-endpoint-remediation-sla")
def deliver_endpoint_remediation_sla(
    sla_report: Annotated[Path, typer.Argument(help="Endpoint remediation SLA report JSON.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for connector delivery evidence.")] = Path(
        ".cavra/release/endpoint-remediation-sla-deliveries"
    ),
    provider: Annotated[str, typer.Option(help="all, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity delivering the notification.")] = "release-manager",
    routing_policy: Annotated[Optional[Path], typer.Option(help="Optional SLA notification routing policy JSON/YAML.")] = None,
    suppression_window_minutes: Annotated[Optional[int], typer.Option(help="Override duplicate suppression window in minutes.")] = None,
    force: Annotated[bool, typer.Option("--force", help="Bypass duplicate suppression and deliver selected providers.")] = False,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Deliver endpoint remediation SLA notifications through configured release connectors."""
    try:
        report_payload = json.loads(sla_report.read_text(encoding="utf-8"))
        report = report_payload.get("report", report_payload)
        if not isinstance(report, dict):
            raise ValueError("endpoint remediation SLA report JSON must be an object")
        connector_config = load_connector_config(config)
        policy = load_connector_config(routing_policy) if routing_policy else None
        existing_deliveries = _load_release_connector_delivery_items(metadata_json=metadata_json, sqlite=sqlite)
        plan = build_endpoint_remediation_sla_notification_plan(
            report,
            policy=policy,
            delivery_items=existing_deliveries,
            requested_provider=provider,
            available_providers=_configured_connector_providers(connector_config),
            generated_by=generated_by,
            suppression_window_minutes=suppression_window_minutes,
            force=force,
        )
        event = build_endpoint_remediation_sla_notification_event(report, generated_by=generated_by)
        event["notification_plan"] = plan
        result = None
        path = None
        if plan["selected_providers"]:
            result = deliver_connector_event(
                event,
                connector_config,
                provider=",".join(plan["selected_providers"]),
                retries=retries,
                timeout_seconds=timeout_seconds,
            )
            path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    plan_metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_notification_plan_metadata(plan),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    metadata = None
    if result is not None and path is not None:
        metadata, delivery_indexed = _index_release_connector_delivery(
            result,
            path,
            source="endpoint_remediation_sla_notification",
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        indexed.extend(delivery_indexed)
    payload = {
        "plan": plan,
        "delivery": result,
        "delivery_evidence": str(path) if path else None,
        "plan_metadata": plan_metadata,
        "metadata": metadata,
        "indexed_metadata_stores": indexed,
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        if path:
            console.print(f"[green]endpoint remediation SLA notification delivery evidence exported[/green] {path}")
        else:
            console.print("[yellow]endpoint remediation SLA notification suppressed; no connector delivery attempted[/yellow]")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("endpoint-remediation-sla-history")
def endpoint_remediation_sla_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    alert_level: Annotated[Optional[str], typer.Option(help="Filter by alert level.")] = None,
    min_breached: Annotated[Optional[int], typer.Option(help="Minimum breached handoff count.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint remediation SLA report history."""
    items = _load_endpoint_remediation_sla_report_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_sla_report_history(
            items,
            alert_level=alert_level,
            min_breached=min_breached,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-sla-dashboard")
def endpoint_remediation_sla_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint remediation SLA reports for executive release governance."""
    items = _load_endpoint_remediation_sla_report_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_sla_dashboard(items))


@release_app.command("ack-endpoint-remediation-sla")
def ack_endpoint_remediation_sla(
    report_id: Annotated[str, typer.Argument(help="Endpoint remediation SLA report ID.")],
    provider: Annotated[str, typer.Option(help="Notification provider being acknowledged.")] = "",
    acknowledged_by: Annotated[str, typer.Option(help="Actor or automation identity acknowledging the notification.")] = "",
    acknowledgement_state: Annotated[str, typer.Option(help="acknowledged, dismissed, escalated, or resolved.")] = "acknowledged",
    external_ref: Annotated[Optional[str], typer.Option(help="Optional external ticket, channel, or review reference.")] = None,
    notes: Annotated[Optional[str], typer.Option(help="Optional acknowledgement notes.")] = None,
    plan_id: Annotated[Optional[str], typer.Option(help="Optional notification plan ID.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index acknowledgement.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index acknowledgement.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable acknowledgement output."),
) -> None:
    """Record acknowledgement for an endpoint remediation SLA notification."""
    if not provider or not acknowledged_by:
        console.print("[red]--provider and --acknowledged-by are required[/red]")
        raise typer.Exit(code=2)
    try:
        acknowledgement = acknowledge_endpoint_remediation_sla_notification(
            report_id,
            provider=provider,
            acknowledged_by=acknowledged_by,
            acknowledgement_state=acknowledgement_state,
            external_ref=external_ref,
            notes=notes,
            plan_id=plan_id,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_notification_ack_metadata(acknowledgement),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = {"acknowledgement": acknowledgement, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))


@release_app.command("endpoint-remediation-sla-notification-history")
def endpoint_remediation_sla_notification_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    report_id: Annotated[Optional[str], typer.Option(help="Filter by SLA report ID.")] = None,
    provider: Annotated[Optional[str], typer.Option(help="Filter by notification provider.")] = None,
    metadata_kind: Annotated[Optional[str], typer.Option(help="Filter by notification plan, acknowledgement, or delivery metadata kind.")] = None,
    acknowledgement_state: Annotated[Optional[str], typer.Option(help="Filter acknowledgement state.")] = None,
    suppressed: Annotated[Optional[bool], typer.Option(help="Filter notification plans with suppressed providers.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint remediation SLA notification plans, deliveries, and acknowledgements."""
    items = _load_endpoint_remediation_sla_notification_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_sla_notification_history(
            items,
            report_id=report_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-sla-notification-dashboard")
def endpoint_remediation_sla_notification_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint remediation SLA notification routing and acknowledgements."""
    items = _load_endpoint_remediation_sla_notification_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_sla_notification_dashboard(items))


@release_app.command("endpoint-remediation-sla-escalation-plan")
def endpoint_remediation_sla_escalation_plan(
    slo_policy: Annotated[Optional[Path], typer.Option(help="Optional owner SLO and escalation ladder policy JSON/YAML.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to read notification metadata and index the plan.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to read notification metadata and index the plan.")] = Path(".cavra/evidence/metadata.db"),
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity generating the escalation plan.")] = "release-manager",
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable escalation plan output."),
) -> None:
    """Build owner-specific SLO and escalation-ladder status for SLA notifications."""
    try:
        policy = load_connector_config(slo_policy) if slo_policy else None
        items = _load_endpoint_remediation_sla_notification_items(metadata_json=metadata_json, sqlite=sqlite)
        plan = build_endpoint_remediation_sla_escalation_plan(items, policy=policy, generated_by=generated_by)
    except (OSError, json.JSONDecodeError, FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_plan_metadata(plan),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = {"plan": plan, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("endpoint-remediation-sla-escalation-history")
def endpoint_remediation_sla_escalation_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    owner: Annotated[Optional[str], typer.Option(help="Filter by escalation owner.")] = None,
    provider: Annotated[Optional[str], typer.Option(help="Filter by notification provider.")] = None,
    alert_level: Annotated[Optional[str], typer.Option(help="Filter by alert level.")] = None,
    active_only: Annotated[bool, typer.Option("--active-only", help="Only show plans with matching active escalations.")] = False,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint remediation SLA escalation plans."""
    items = _load_endpoint_remediation_sla_escalation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_sla_escalation_history(
            items,
            owner=owner,
            provider=provider,
            alert_level=alert_level,
            active_only=active_only,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-sla-escalation-dashboard")
def endpoint_remediation_sla_escalation_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint remediation SLA escalation ladders and owner SLOs."""
    items = _load_endpoint_remediation_sla_escalation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_sla_escalation_dashboard(items))


@release_app.command("deliver-endpoint-remediation-sla-escalation")
def deliver_endpoint_remediation_sla_escalation(
    escalation_plan: Annotated[Path, typer.Argument(help="Endpoint remediation SLA escalation plan JSON.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for connector delivery evidence.")] = Path(
        ".cavra/release/endpoint-remediation-sla-escalation-deliveries"
    ),
    provider: Annotated[str, typer.Option(help="all, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity delivering the escalation.")] = "release-manager",
    max_routes: Annotated[int, typer.Option(help="Maximum active escalation routes to include.")] = 20,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Deliver active endpoint remediation SLA escalations through configured release connectors."""
    try:
        plan_payload = json.loads(escalation_plan.read_text(encoding="utf-8"))
        plan = plan_payload.get("plan", plan_payload)
        if not isinstance(plan, dict):
            raise ValueError("endpoint remediation SLA escalation plan JSON must be an object")
        connector_config = load_connector_config(config)
        event = build_endpoint_remediation_sla_escalation_delivery_event(
            plan,
            generated_by=generated_by,
            max_routes=max_routes,
        )
        result = None
        path = None
        if event["routes"]:
            result = deliver_connector_event(
                event,
                connector_config,
                provider=provider,
                retries=retries,
                timeout_seconds=timeout_seconds,
            )
            path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata = None
    indexed: list[str] = []
    if result is not None and path is not None:
        metadata, indexed = _index_release_connector_delivery(
            result,
            path,
            source="endpoint_remediation_sla_escalation_delivery",
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = {
        "event": event,
        "delivery": result,
        "delivery_evidence": str(path) if path else None,
        "metadata": metadata,
        "indexed_metadata_stores": indexed,
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        if path:
            console.print(f"[green]endpoint remediation SLA escalation delivery evidence exported[/green] {path}")
        else:
            console.print("[yellow]endpoint remediation SLA escalation has no active routes; no delivery attempted[/yellow]")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("review-endpoint-remediation-sla-escalation")
def review_endpoint_remediation_sla_escalation_command(
    plan_id: Annotated[str, typer.Argument(help="Endpoint remediation SLA escalation plan ID.")],
    report_id: Annotated[str, typer.Option(help="SLA report ID for the reviewed route.")] = "",
    provider: Annotated[str, typer.Option(help="Notification provider for the reviewed route.")] = "",
    owner: Annotated[str, typer.Option(help="Escalation owner.")] = "",
    reviewed_by: Annotated[str, typer.Option(help="Actor or automation identity reviewing the escalation.")] = "",
    review_state: Annotated[str, typer.Option(help="accepted, deferred, resolved, false_positive, or escalated.")] = "accepted",
    external_ref: Annotated[Optional[str], typer.Option(help="Optional external ticket, channel, or review reference.")] = None,
    notes: Annotated[Optional[str], typer.Option(help="Optional review notes.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index review.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index review.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable review output."),
) -> None:
    """Record owner review for an endpoint remediation SLA escalation route."""
    if not report_id or not provider or not owner or not reviewed_by:
        console.print("[red]--report-id, --provider, --owner, and --reviewed-by are required[/red]")
        raise typer.Exit(code=2)
    try:
        review = review_endpoint_remediation_sla_escalation(
            plan_id,
            report_id=report_id,
            provider=provider,
            owner=owner,
            reviewed_by=reviewed_by,
            review_state=review_state,
            external_ref=external_ref,
            notes=notes,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_review_metadata(review),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = {"review": review, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))


@release_app.command("endpoint-remediation-sla-escalation-action-history")
def endpoint_remediation_sla_escalation_action_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    plan_id: Annotated[Optional[str], typer.Option(help="Filter by escalation plan ID.")] = None,
    owner: Annotated[Optional[str], typer.Option(help="Filter by escalation owner.")] = None,
    provider: Annotated[Optional[str], typer.Option(help="Filter by notification provider.")] = None,
    metadata_kind: Annotated[Optional[str], typer.Option(help="Filter by plan, delivery, or review metadata kind.")] = None,
    review_state: Annotated[Optional[str], typer.Option(help="Filter owner review state.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint remediation SLA escalation plans, deliveries, and owner reviews."""
    items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_sla_escalation_action_history(
            items,
            plan_id=plan_id,
            owner=owner,
            provider=provider,
            metadata_kind=metadata_kind,
            review_state=review_state,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-sla-escalation-action-dashboard")
def endpoint_remediation_sla_escalation_action_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint remediation SLA escalation delivery and owner review actions."""
    items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_sla_escalation_action_dashboard(items))


@release_app.command("endpoint-remediation-sla-escalation-recurrence-plan")
def endpoint_remediation_sla_escalation_recurrence_plan(
    recurrence_policy: Annotated[Optional[Path], typer.Option(help="Optional recurrence, owner calendar, and maintenance window policy JSON/YAML.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to read escalation action metadata and index the plan.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to read escalation action metadata and index the plan.")] = Path(".cavra/evidence/metadata.db"),
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity generating the recurrence plan.")] = "release-manager",
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable recurrence plan output."),
) -> None:
    """Plan recurring escalation follow-up with owner calendar and maintenance-window suppression."""
    try:
        policy = load_connector_config(recurrence_policy) if recurrence_policy else None
        items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
        plan = build_endpoint_remediation_sla_escalation_recurrence_plan(
            items,
            policy=policy,
            generated_by=generated_by,
        )
    except (OSError, json.JSONDecodeError, FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_recurrence_plan_metadata(plan),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = {"plan": plan, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("endpoint-remediation-sla-escalation-recurrence-history")
def endpoint_remediation_sla_escalation_recurrence_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    plan_id: Annotated[Optional[str], typer.Option(help="Filter by escalation plan ID.")] = None,
    owner: Annotated[Optional[str], typer.Option(help="Filter by escalation owner.")] = None,
    provider: Annotated[Optional[str], typer.Option(help="Filter by notification provider.")] = None,
    action: Annotated[Optional[str], typer.Option(help="Filter by recurrence action: deliver, wait, or suppress.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint remediation SLA escalation recurrence and suppression plans."""
    items = _load_endpoint_remediation_sla_escalation_recurrence_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_sla_escalation_recurrence_history(
            items,
            plan_id=plan_id,
            owner=owner,
            provider=provider,
            action=action,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-sla-escalation-recurrence-dashboard")
def endpoint_remediation_sla_escalation_recurrence_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint remediation SLA escalation recurrence suppression."""
    items = _load_endpoint_remediation_sla_escalation_recurrence_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_sla_escalation_recurrence_dashboard(items))


@release_app.command("deliver-endpoint-remediation-sla-escalation-recurrence")
def deliver_endpoint_remediation_sla_escalation_recurrence(
    recurrence_plan: Annotated[Path, typer.Argument(help="Endpoint remediation SLA escalation recurrence plan JSON.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for connector delivery evidence.")] = Path(
        ".cavra/release/endpoint-remediation-sla-escalation-recurrence-deliveries"
    ),
    provider: Annotated[str, typer.Option(help="all, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity delivering the recurrence batch.")] = "release-manager",
    max_routes: Annotated[int, typer.Option(help="Maximum deliverable recurrence routes to include.")] = 50,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Deliver recurrence-plan routes that are ready for follow-up escalation."""
    try:
        plan_payload = json.loads(recurrence_plan.read_text(encoding="utf-8"))
        plan = plan_payload.get("plan", plan_payload)
        if not isinstance(plan, dict):
            raise ValueError("endpoint remediation SLA recurrence plan JSON must be an object")
        event = build_endpoint_remediation_sla_escalation_recurrence_delivery_event(
            plan,
            generated_by=generated_by,
            max_routes=max_routes,
        )
        result = None
        path = None
        if event["routes"]:
            result = deliver_connector_event(
                event,
                load_connector_config(config),
                provider=provider,
                retries=retries,
                timeout_seconds=timeout_seconds,
            )
            path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata = None
    indexed: list[str] = []
    if result is not None and path is not None:
        metadata, indexed = _index_release_connector_delivery(
            result,
            path,
            source="endpoint_remediation_sla_escalation_recurrence_delivery",
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
    payload = {
        "event": event,
        "delivery": result,
        "delivery_evidence": str(path) if path else None,
        "metadata": metadata,
        "indexed_metadata_stores": indexed,
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        if path:
            console.print(f"[green]endpoint remediation SLA recurrence delivery evidence exported[/green] {path}")
        else:
            console.print("[yellow]recurrence plan has no deliverable routes; no delivery attempted[/yellow]")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("export-endpoint-remediation-sla-escalation-suppression-audit")
def export_endpoint_remediation_sla_escalation_suppression_audit_command(
    recurrence_plan: Annotated[Path, typer.Argument(help="Endpoint remediation SLA escalation recurrence plan JSON.")],
    output: Annotated[Path, typer.Option(help="Output directory for suppression audit export.")] = Path(
        ".cavra/release/endpoint-remediation-sla-escalation-suppression-audit"
    ),
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity exporting the audit.")] = "release-manager",
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index audit metadata.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index audit metadata.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable export output."),
) -> None:
    """Export public-safe suppression audit evidence from a recurrence plan."""
    try:
        plan_payload = json.loads(recurrence_plan.read_text(encoding="utf-8"))
        plan = plan_payload.get("plan", plan_payload)
        if not isinstance(plan, dict):
            raise ValueError("endpoint remediation SLA recurrence plan JSON must be an object")
        result = export_endpoint_remediation_sla_escalation_suppression_audit(
            plan,
            output,
            generated_by=generated_by,
        )
        audit_path = Path(result.output_dir) / "endpoint-remediation-sla-escalation-suppression-audit.json"
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_suppression_audit_metadata(audit, bundle_dir=output),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = result.to_dict() | {"audit": audit, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(f"[green]suppression audit exported[/green] {result.output_dir}")
        for path in result.files:
            console.print(f"  {path.name}")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("endpoint-remediation-sla-escalation-recurrence-retry-plan")
def endpoint_remediation_sla_escalation_recurrence_retry_plan(
    retry_policy: Annotated[Optional[Path], typer.Option(help="Optional recurrence retry policy JSON/YAML.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to read recurrence delivery metadata and index the plan.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to read recurrence delivery metadata and index the plan.")] = Path(".cavra/evidence/metadata.db"),
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity generating the retry plan.")] = "release-manager",
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable retry plan output."),
) -> None:
    """Plan safe retries for failed recurrence delivery batches."""
    try:
        policy = load_connector_config(retry_policy) if retry_policy else None
        items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
        plan = build_endpoint_remediation_sla_escalation_recurrence_retry_plan(
            items,
            policy=policy,
            generated_by=generated_by,
        )
    except (OSError, json.JSONDecodeError, FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata(plan),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = {"plan": plan, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("deliver-endpoint-remediation-sla-escalation-owner-digest")
def deliver_endpoint_remediation_sla_escalation_owner_digest(
    recurrence_plan: Annotated[Path, typer.Argument(help="Endpoint remediation SLA escalation recurrence plan JSON.")],
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    retry_plan: Annotated[Optional[Path], typer.Option(help="Optional recurrence retry plan JSON.")] = None,
    output: Annotated[Path, typer.Option(help="Output directory for owner digest delivery evidence.")] = Path(
        ".cavra/release/endpoint-remediation-sla-escalation-owner-digests"
    ),
    provider: Annotated[str, typer.Option(help="all, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity delivering the owner digest.")] = "release-manager",
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index owner digest and delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index owner digest and delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Deliver owner digest notifications for unresolved recurrence routes."""
    try:
        plan_payload = json.loads(recurrence_plan.read_text(encoding="utf-8"))
        plan = plan_payload.get("plan", plan_payload)
        if not isinstance(plan, dict):
            raise ValueError("endpoint remediation SLA recurrence plan JSON must be an object")
        retry_payload = json.loads(retry_plan.read_text(encoding="utf-8")) if retry_plan else None
        retry = retry_payload.get("plan", retry_payload) if isinstance(retry_payload, dict) else None
        event = build_endpoint_remediation_sla_escalation_owner_digest_event(
            plan,
            retry_plan=retry if isinstance(retry, dict) else None,
            generated_by=generated_by,
        )
        digest_metadata, indexed = _index_release_metadata(
            build_endpoint_remediation_sla_escalation_owner_digest_metadata(event),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        result = None
        path = None
        if event["owners"]:
            result = deliver_connector_event(
                event,
                load_connector_config(config),
                provider=provider,
                retries=retries,
                timeout_seconds=timeout_seconds,
            )
            path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    delivery_metadata = None
    if result is not None and path is not None:
        delivery_metadata, delivery_indexed = _index_release_connector_delivery(
            result,
            path,
            source="endpoint_remediation_sla_escalation_owner_digest",
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        indexed.extend(delivery_indexed)
    payload = {
        "event": event,
        "digest_metadata": digest_metadata,
        "delivery": result,
        "delivery_evidence": str(path) if path else None,
        "metadata": delivery_metadata,
        "indexed_metadata_stores": indexed,
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        if path:
            console.print(f"[green]owner digest delivery evidence exported[/green] {path}")
        else:
            console.print("[yellow]owner digest has no unresolved routes; no delivery attempted[/yellow]")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("endpoint-remediation-sla-escalation-suppression-trends")
def endpoint_remediation_sla_escalation_suppression_trends(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to read recurrence and suppression audit metadata and index trends.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to read recurrence and suppression audit metadata and index trends.")] = Path(".cavra/evidence/metadata.db"),
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity generating suppression trends.")] = "release-manager",
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable suppression trend output."),
) -> None:
    """Summarize recurrence suppression trends by reason, owner, and provider."""
    items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
    trend = build_endpoint_remediation_sla_escalation_suppression_trends(items, generated_by=generated_by)
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_suppression_trend_metadata(trend),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = {"trend": trend, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("endpoint-remediation-sla-escalation-recurrence-automation")
def endpoint_remediation_sla_escalation_recurrence_automation(
    retry_policy: Annotated[Optional[Path], typer.Option(help="Optional recurrence retry policy JSON/YAML.")] = None,
    config: Annotated[Optional[Path], typer.Option("--config", help="Optional connector config JSON/YAML path used only with --execute.")] = None,
    output: Annotated[Path, typer.Option(help="Output directory for owner digest delivery evidence.")] = Path(
        ".cavra/release/endpoint-remediation-sla-escalation-recurrence-automation"
    ),
    provider: Annotated[str, typer.Option(help="all, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    schedule_interval_minutes: Annotated[int, typer.Option(help="Idempotency window for scheduled worker runs.")] = 60,
    max_digest_plans: Annotated[int, typer.Option(help="Maximum latest recurrence plans to include in owner digest generation.")] = 5,
    dry_run: bool = typer.Option(True, "--dry-run/--execute", help="Plan by default; use --execute to deliver owner digests through configured connectors."),
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity running the worker.")] = "release-manager",
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to read recurrence metadata and index worker outputs.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to read recurrence metadata and index worker outputs.")] = Path(".cavra/evidence/metadata.db"),
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable automation output."),
) -> None:
    """Run one scheduled recurrence automation pass for retry, digest, and trend follow-up."""
    try:
        policy = load_connector_config(retry_policy) if retry_policy else None
        connector_config = load_connector_config(config) if config and not dry_run else None
        items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
        run = build_endpoint_remediation_sla_escalation_recurrence_automation_run(
            items,
            retry_policy=policy,
            schedule={"interval_minutes": schedule_interval_minutes},
            generated_by=generated_by,
            dry_run=dry_run,
            max_digest_plans=max_digest_plans,
        )
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    retry_metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_recurrence_retry_plan_metadata(run["retry_plan"]),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    trend_metadata, trend_indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_suppression_trend_metadata(run["suppression_trend"]),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    indexed.extend(trend_indexed)
    digest_results = []
    for event in run.get("owner_digest_events", []):
        digest_metadata, digest_indexed = _index_release_metadata(
            build_endpoint_remediation_sla_escalation_owner_digest_metadata(event),
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        indexed.extend(digest_indexed)
        delivery = None
        delivery_evidence = None
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
                provider=provider,
                retries=retries,
                timeout_seconds=timeout_seconds,
            )
            path = export_connector_delivery_result(delivery, output)
            delivery_evidence = str(path)
            delivery_metadata, delivery_indexed = _index_release_connector_delivery(
                delivery,
                path,
                source="endpoint_remediation_sla_escalation_owner_digest",
                metadata_json=metadata_json,
                sqlite=sqlite,
            )
            indexed.extend(delivery_indexed)
        digest_results.append(
            {
                "event": event,
                "digest_metadata": digest_metadata,
                "delivery": delivery,
                "delivery_evidence": delivery_evidence,
                "metadata": delivery_metadata,
                "skipped": skipped,
            }
        )
    metadata, run_indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_recurrence_automation_run_metadata(run),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    indexed.extend(run_indexed)
    payload = {
        "run": run,
        "metadata": metadata,
        "retry_metadata": retry_metadata,
        "trend_metadata": trend_metadata,
        "owner_digests": digest_results,
        "indexed_metadata_stores": sorted(set(indexed)),
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        for store in sorted(set(indexed)):
            console.print(f"  indexed: {store}")


@release_app.command("endpoint-remediation-sla-escalation-recurrence-automation-history")
def endpoint_remediation_sla_escalation_recurrence_automation_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    dry_run: Annotated[Optional[bool], typer.Option(help="Filter by dry-run or executed worker runs.")] = None,
    limit: Annotated[int, typer.Option(help="Maximum records to return.")] = 50,
    offset: Annotated[int, typer.Option(help="Records to skip.")] = 0,
) -> None:
    """List scheduled recurrence automation worker runs."""
    items = _load_endpoint_remediation_sla_escalation_recurrence_automation_items(
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    _print_json(
        filter_endpoint_remediation_sla_escalation_recurrence_automation_history(
            items,
            dry_run=dry_run,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-sla-escalation-recurrence-automation-dashboard")
def endpoint_remediation_sla_escalation_recurrence_automation_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize scheduled recurrence automation worker runs."""
    items = _load_endpoint_remediation_sla_escalation_recurrence_automation_items(
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    _print_json(build_endpoint_remediation_sla_escalation_recurrence_automation_dashboard(items))


@release_app.command("endpoint-remediation-sla-escalation-recurrence-automation-health")
def endpoint_remediation_sla_escalation_recurrence_automation_health(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    expected_interval_minutes: Annotated[int, typer.Option(help="Expected scheduler interval in minutes.")] = 30,
    stale_metadata_minutes: Annotated[int, typer.Option(help="Age threshold for stale recurrence metadata.")] = 120,
) -> None:
    """Report missed recurrence automation runs, stale metadata, and delivery failures."""
    items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        build_endpoint_remediation_sla_escalation_recurrence_automation_health(
            items,
            expected_interval_minutes=expected_interval_minutes,
            stale_metadata_minutes=stale_metadata_minutes,
        )
    )


@release_app.command("deliver-endpoint-remediation-sla-escalation-recurrence-automation-health-alert")
def deliver_endpoint_remediation_sla_escalation_recurrence_automation_health_alert(
    config: Path = typer.Option(..., "--config", help="Connector config JSON/YAML path."),
    output: Annotated[Path, typer.Option(help="Output directory for connector delivery evidence.")] = Path(
        ".cavra/release/endpoint-remediation-sla-escalation-recurrence-automation-health-alerts"
    ),
    provider: Annotated[str, typer.Option(help="all, webhook, slack, teams, jira, or servicenow.")] = "all",
    retries: Annotated[int, typer.Option(help="Retry count after the first attempt.")] = 2,
    timeout_seconds: Annotated[float, typer.Option(help="HTTP timeout in seconds.")] = 10.0,
    generated_by: Annotated[str, typer.Option(help="Actor or automation identity delivering the alert.")] = "release-manager",
    routing_policy: Annotated[Optional[Path], typer.Option(help="Optional health alert routing policy JSON/YAML.")] = None,
    suppression_window_minutes: Annotated[Optional[int], typer.Option(help="Override duplicate suppression window in minutes.")] = None,
    expected_interval_minutes: Annotated[int, typer.Option(help="Expected scheduler interval in minutes.")] = 30,
    stale_metadata_minutes: Annotated[int, typer.Option(help="Age threshold for stale recurrence metadata.")] = 120,
    force: Annotated[bool, typer.Option("--force", help="Bypass duplicate suppression and deliver selected providers.")] = False,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index delivery history.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index delivery history.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable delivery output."),
) -> None:
    """Deliver recurrence automation health alerts through configured release connectors."""
    try:
        connector_config = load_connector_config(config)
        policy = load_connector_config(routing_policy) if routing_policy else None
        items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
        health = build_endpoint_remediation_sla_escalation_recurrence_automation_health(
            items,
            expected_interval_minutes=expected_interval_minutes,
            stale_metadata_minutes=stale_metadata_minutes,
        )
        plan = build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan(
            health,
            policy=policy,
            delivery_items=items,
            requested_provider=provider,
            available_providers=_configured_connector_providers(connector_config),
            generated_by=generated_by,
            suppression_window_minutes=suppression_window_minutes,
            force=force,
        )
        event = build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_event(
            health,
            generated_by=generated_by,
        )
        event["health_alert_plan"] = plan
        result = None
        path = None
        if plan["selected_providers"]:
            result = deliver_connector_event(
                event,
                connector_config,
                provider=",".join(plan["selected_providers"]),
                retries=retries,
                timeout_seconds=timeout_seconds,
            )
            path = export_connector_delivery_result(result, output)
    except (OSError, json.JSONDecodeError, FileNotFoundError, RuntimeError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    plan_metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_plan_metadata(plan),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    metadata = None
    if result is not None and path is not None:
        metadata, delivery_indexed = _index_release_connector_delivery(
            result,
            path,
            source="endpoint_remediation_sla_escalation_recurrence_automation_health_alert",
            metadata_json=metadata_json,
            sqlite=sqlite,
        )
        indexed.extend(delivery_indexed)
    payload = {
        "health": health,
        "plan": plan,
        "delivery": result,
        "delivery_evidence": str(path) if path else None,
        "plan_metadata": plan_metadata,
        "metadata": metadata,
        "indexed_metadata_stores": indexed,
    }
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))
        if path:
            console.print(f"[green]recurrence automation health alert delivery evidence exported[/green] {path}")
        else:
            console.print("[yellow]recurrence automation health alert suppressed; no connector delivery attempted[/yellow]")
        for store in indexed:
            console.print(f"  indexed: {store}")


@release_app.command("ack-endpoint-remediation-sla-escalation-recurrence-automation-health-alert")
def ack_endpoint_remediation_sla_escalation_recurrence_automation_health_alert(
    health_id: Annotated[str, typer.Argument(help="Recurrence automation health alert ID.")],
    provider: Annotated[str, typer.Option(help="Notification provider being acknowledged.")] = "",
    acknowledged_by: Annotated[str, typer.Option(help="Actor or automation identity acknowledging the alert.")] = "",
    acknowledgement_state: Annotated[str, typer.Option(help="acknowledged, dismissed, escalated, or resolved.")] = "acknowledged",
    external_ref: Annotated[Optional[str], typer.Option(help="Optional external ticket, channel, or review reference.")] = None,
    notes: Annotated[Optional[str], typer.Option(help="Optional acknowledgement notes.")] = None,
    plan_id: Annotated[Optional[str], typer.Option(help="Optional health alert plan ID.")] = None,
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store to index acknowledgement.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store to index acknowledgement.")] = None,
    json_output: bool = typer.Option(False, "--json", help="Print machine-readable acknowledgement output."),
) -> None:
    """Record acknowledgement for a recurrence automation health alert."""
    if not provider or not acknowledged_by:
        console.print("[red]--provider and --acknowledged-by are required[/red]")
        raise typer.Exit(code=2)
    try:
        acknowledgement = acknowledge_endpoint_remediation_sla_escalation_recurrence_automation_health_alert(
            health_id,
            provider=provider,
            acknowledged_by=acknowledged_by,
            acknowledgement_state=acknowledgement_state,
            external_ref=external_ref,
            notes=notes,
            plan_id=plan_id,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    metadata, indexed = _index_release_metadata(
        build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_ack_metadata(acknowledgement),
        metadata_json=metadata_json,
        sqlite=sqlite,
    )
    payload = {"acknowledgement": acknowledgement, "metadata": metadata, "indexed_metadata_stores": indexed}
    if json_output:
        _print_json(payload)
    else:
        console.print(JSON(json.dumps(payload, indent=2)))


@release_app.command("endpoint-remediation-sla-escalation-recurrence-automation-health-alert-history")
def endpoint_remediation_sla_escalation_recurrence_automation_health_alert_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    health_id: Annotated[Optional[str], typer.Option(help="Filter by recurrence automation health alert ID.")] = None,
    provider: Annotated[Optional[str], typer.Option(help="Filter by notification provider.")] = None,
    metadata_kind: Annotated[Optional[str], typer.Option(help="Filter by alert plan, acknowledgement, or delivery metadata kind.")] = None,
    acknowledgement_state: Annotated[Optional[str], typer.Option(help="Filter acknowledgement state.")] = None,
    suppressed: Annotated[Optional[bool], typer.Option(help="Filter alert plans with suppressed providers.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show recurrence automation health alert plans, deliveries, and acknowledgements."""
    items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_history(
            items,
            health_id=health_id,
            provider=provider,
            metadata_kind=metadata_kind,
            acknowledgement_state=acknowledgement_state,
            suppressed=suppressed,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-sla-escalation-recurrence-automation-health-alert-dashboard")
def endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize recurrence automation health alert delivery and acknowledgements."""
    items = _load_endpoint_remediation_sla_escalation_action_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_remediation_sla_escalation_recurrence_automation_health_alert_dashboard(items))


@release_app.command("endpoint-remediation-history")
def endpoint_remediation_history(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
    metadata_kind: Annotated[Optional[str], typer.Option(help="Filter by endpoint-drift-remediation-request or endpoint-drift-remediation-execution.")] = None,
    reconciliation_id: Annotated[Optional[str], typer.Option(help="Filter by reconciliation ID.")] = None,
    approval_state: Annotated[Optional[str], typer.Option(help="Filter by approval state.")] = None,
    execution_status: Annotated[Optional[str], typer.Option(help="Filter by execution status.")] = None,
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Show endpoint drift remediation request and execution history."""
    items = _load_endpoint_drift_remediation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(
        filter_endpoint_drift_remediation_history(
            items,
            metadata_kind=metadata_kind,
            reconciliation_id=reconciliation_id,
            approval_state=approval_state,
            execution_status=execution_status,
            limit=limit,
            offset=offset,
        )
    )


@release_app.command("endpoint-remediation-dashboard")
def endpoint_remediation_dashboard(
    metadata_json: Annotated[Optional[Path], typer.Option(help="Optional JSON evidence metadata store.")] = None,
    sqlite: Annotated[Optional[Path], typer.Option(help="Optional SQLite evidence metadata store.")] = Path(".cavra/evidence/metadata.db"),
) -> None:
    """Summarize endpoint drift remediation approvals and executions."""
    items = _load_endpoint_drift_remediation_items(metadata_json=metadata_json, sqlite=sqlite)
    _print_json(build_endpoint_drift_remediation_dashboard(items))


def _index_release_metadata(
    metadata: dict,
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> tuple[dict, list[str]]:
    indexed: list[str] = []
    if metadata_json:
        EvidenceMetadataStore(metadata_json).upsert(metadata)
        indexed.append(str(metadata_json))
    if sqlite:
        SQLiteEvidenceMetadataStore(sqlite).upsert(metadata)
        indexed.append(str(sqlite))
    return metadata, indexed


def _index_release_connector_delivery(
    result: dict,
    delivery_evidence: Path,
    *,
    source: str,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> tuple[dict, list[str]]:
    metadata = build_connector_delivery_metadata(result, delivery_evidence=delivery_evidence, source=source)
    indexed: list[str] = []
    if metadata_json:
        EvidenceMetadataStore(metadata_json).upsert(metadata)
        indexed.append(str(metadata_json))
    if sqlite:
        SQLiteEvidenceMetadataStore(sqlite).upsert(metadata)
        indexed.append(str(sqlite))
    return metadata, indexed


def _load_release_connector_delivery_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(metadata_kind="release-connector-delivery", limit=500)["items"]
    return []


def _load_endpoint_management_publication_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-management-publication-delivery",
            limit=500,
        )["items"]
    return []


def _load_managed_endpoint_reconciliation_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="managed-endpoint-reconciliation",
            limit=500,
        )["items"]
    return []


def _load_endpoint_inventory_ingestion_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-inventory-ingestion",
            limit=500,
        )["items"]
    return []


def _load_endpoint_inventory_freshness_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-inventory-freshness-report",
            limit=500,
        )["items"]
    return []


def _load_endpoint_reconciliation_automation_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-reconciliation-automation",
            limit=500,
        )["items"]
    return []


def _load_endpoint_drift_remediation_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        request_items = SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-drift-remediation-request",
            limit=500,
        )["items"]
        execution_items = SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-drift-remediation-execution",
            limit=500,
        )["items"]
        return [*request_items, *execution_items]
    return []


def _load_endpoint_remediation_handoff_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-remediation-handoff",
            limit=500,
        )["items"]
    return []


def _load_endpoint_remediation_handoff_status_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-remediation-handoff-status",
            limit=500,
        )["items"]
    return []


def _load_endpoint_remediation_sla_report_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-remediation-sla-report",
            limit=500,
        )["items"]
    return []


def _load_endpoint_remediation_sla_notification_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        store = SQLiteEvidenceMetadataStore(sqlite)
        plans = store.search(metadata_kind="endpoint-remediation-sla-notification-plan", limit=500)["items"]
        acknowledgements = store.search(metadata_kind="endpoint-remediation-sla-notification-ack", limit=500)["items"]
        deliveries = store.search(metadata_kind="release-connector-delivery", limit=500)["items"]
        return [*plans, *acknowledgements, *deliveries]
    return []


def _load_endpoint_remediation_sla_escalation_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-remediation-sla-escalation-plan",
            limit=500,
        )["items"]
    return []


def _load_endpoint_remediation_sla_escalation_action_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        store = SQLiteEvidenceMetadataStore(sqlite)
        plans = store.search(metadata_kind="endpoint-remediation-sla-escalation-plan", limit=500)["items"]
        reviews = store.search(metadata_kind="endpoint-remediation-sla-escalation-review", limit=500)["items"]
        recurrences = store.search(metadata_kind="endpoint-remediation-sla-escalation-recurrence-plan", limit=500)["items"]
        suppression_audits = store.search(
            metadata_kind="endpoint-remediation-sla-escalation-suppression-audit",
            limit=500,
        )["items"]
        retry_plans = store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-retry-plan",
            limit=500,
        )["items"]
        owner_digests = store.search(
            metadata_kind="endpoint-remediation-sla-escalation-owner-digest",
            limit=500,
        )["items"]
        suppression_trends = store.search(
            metadata_kind="endpoint-remediation-sla-escalation-suppression-trend",
            limit=500,
        )["items"]
        automation_runs = store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-run",
            limit=500,
        )["items"]
        health_alert_plans = store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan",
            limit=500,
        )["items"]
        health_alert_acks = store.search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack",
            limit=500,
        )["items"]
        deliveries = store.search(metadata_kind="release-connector-delivery", limit=500)["items"]
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
    return []


def _load_endpoint_remediation_sla_escalation_recurrence_automation_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-automation-run",
            limit=500,
        )["items"]
    return []


def _load_endpoint_remediation_sla_escalation_recurrence_items(
    *,
    metadata_json: Path | None,
    sqlite: Path | None,
) -> list[dict]:
    if metadata_json:
        return EvidenceMetadataStore(metadata_json).list()
    if sqlite:
        return SQLiteEvidenceMetadataStore(sqlite).search(
            metadata_kind="endpoint-remediation-sla-escalation-recurrence-plan",
            limit=500,
        )["items"]
    return []


def _configured_connector_providers(config: dict) -> list[str]:
    connectors = config.get("connectors", config.get("providers", config))
    if not isinstance(connectors, dict):
        return []
    return sorted(str(provider) for provider in connectors)


def _load_release_approval(
    approval_id: str | None,
    *,
    approval_json: Path | None = None,
    approval_store: Path | None = None,
    approval_sqlite: Path | None = None,
) -> dict:
    if approval_json:
        return json.loads(approval_json.read_text(encoding="utf-8"))
    if not approval_id:
        raise ValueError("approval_id is required unless --approval-json is provided")
    if approval_store:
        approval = ApprovalStore(approval_store).get(approval_id)
        if approval is None:
            raise KeyError(f"approval not found: {approval_id}")
        return approval
    if approval_sqlite:
        approval = SQLiteApprovalStore(approval_sqlite).get(approval_id)
        if approval is None:
            raise KeyError(f"approval not found: {approval_id}")
        return approval
    raise ValueError("provide --approval-json, --approval-store, or --approval-sqlite")


def _print_json(payload: object) -> None:
    typer.echo(json.dumps(payload, indent=2))


@demo_app.command("before-the-agent-acts")
def demo_before_the_agent_acts(
    output: Annotated[Path, typer.Option(help="Directory for generated evidence.")] = Path("examples/demos/before-the-agent-acts/generated"),
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline",
) -> None:
    """Run the flagship CAVRA demo and generate evidence."""
    _run_before_agent_acts(output=output, policy_pack=policy_pack)


def _run_before_agent_acts(
    output: Path = Path("examples/demos/before-the-agent-acts/generated"),
    policy_pack: str = "cavra-ai-agent-baseline",
) -> None:
    decisions = _before_agent_acts_decisions(policy_pack=policy_pack)
    result = create_evidence_bundle(decisions, output, session_id="demo-session")
    for decision in decisions:
        console.print(f"{decision['action_type']} {decision['target']}: [bold]{decision['decision']}[/bold] - {decision['reason']}")
    console.print(f"[green]evidence generated[/green] {result.bundle_dir}")


def _before_agent_acts_decisions(policy_pack: str = "cavra-ai-agent-baseline") -> list[dict[str, object]]:
    guard = RuntimeGuard(policy_pack=policy_pack, agent_id="demo-agent", actor="simulated-ai-agent")
    decisions = [
        guard.evaluate_file_access(Path(".env"), "read"),
        guard.evaluate_file_access(Path("iam/admin-role.tf"), "write"),
        guard.evaluate_command("terraform plan"),
        guard.evaluate_command("terraform apply -auto-approve"),
        guard.evaluate_mcp_tool_call("unknown-filesystem", "read_file", "filesystem"),
        guard.evaluate_git_action("push", "origin/main"),
        guard.generate_pr_attestation_decision("create PR"),
    ]
    return [decision.to_dict() for decision in decisions]


def main() -> None:
    app()


if __name__ == "__main__":
    main()
