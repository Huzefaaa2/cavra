from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON

from cavra.agent import AgentSessionManager
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
from cavra.integrations import (
    CommandInterceptor,
    build_connector_delivery_dashboard,
    build_connector_delivery_metadata,
    deliver_connector_event,
    export_connector_delivery_result,
    filter_connector_delivery_history,
    load_connector_config,
)
from cavra.operations import (
    backup_persistent_api_stores,
    export_persistent_api_retention_plan,
    persistent_api_store_status,
    restore_persistent_api_backup,
)
from cavra.policy_engine import (
    compile_policy as compile_policy_payload,
    diff_policies,
    load_policy_file,
    validate_policy as validate_policy_payload,
    verify_policy_signature,
    write_policy_signature,
)
from cavra.policy_registry import PolicyRegistry
from cavra.registry import (
    RegistryStore,
    SQLiteRegistryStore,
    classify_mcp_capability,
    default_agent_profiles,
    default_mcp_tool_classifications,
)
from cavra.release import (
    build_endpoint_management_export_metadata,
    build_endpoint_management_publication_dashboard,
    build_endpoint_management_publication_event,
    build_endpoint_management_publication_metadata,
    build_endpoint_drift_remediation_dashboard,
    build_endpoint_drift_remediation_execution_metadata,
    build_endpoint_drift_remediation_request_metadata,
    build_endpoint_inventory_ingestion_dashboard,
    build_endpoint_inventory_ingestion_metadata,
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
    execute_endpoint_drift_remediation,
    export_endpoint_management_bundles,
    export_rollout_promotion_execution_audit,
    filter_endpoint_drift_remediation_history,
    filter_endpoint_inventory_ingestion_history,
    filter_endpoint_management_publication_history,
    filter_managed_endpoint_reconciliation_history,
    ingest_endpoint_inventory,
    load_release_channel_manifest,
    load_workstation_updater_policy,
    reconcile_managed_endpoint_deployment,
    verify_managed_endpoint_rollout_evidence,
    smoke_test_go_installers,
    validate_go_release_upgrade,
    verify_go_airgap_bundle,
    verify_go_release_package,
)
from cavra.runtime import RuntimeGuard

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


@app.command()
def version() -> None:
    typer.echo("cavra 0.1.0")


@app.command()
def evaluate(
    action_type: Annotated[str, typer.Argument(help="read_file, write_file, execute_command, git_operation, mcp_tool_call.")],
    target: Annotated[str, typer.Argument(help="File path, command, Git target, or MCP server.")],
    policy_pack: Annotated[str, typer.Option(help="Policy pack ID.")] = "cavra-ai-agent-baseline",
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
    if json_output:
        console.print(JSON(json.dumps(decision.to_dict(), indent=2)))
    else:
        console.print(f"{decision.decision}: {decision.reason}")


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
) -> None:
    """Create CAVRA policy signature metadata."""
    policy_path = path / "policy.yaml" if path.is_dir() else path
    sig_path = write_policy_signature(policy_path, signer=signer, key=key)
    console.print(f"[green]signed[/green] {sig_path}")


@policy_app.command("verify")
def verify_policy(
    path: Path,
    signature: Annotated[Optional[Path], typer.Option(help="Signature metadata path.")] = None,
    key: Annotated[Optional[str], typer.Option(help="Optional HMAC key for local tamper checks.")] = None,
) -> None:
    """Verify CAVRA policy signature metadata."""
    policy_path = path / "policy.yaml" if path.is_dir() else path
    ok, message = verify_policy_signature(policy_path, signature_path=signature, key=key)
    if not ok:
        console.print(f"[red]signature verification failed[/red]: {message}")
        raise typer.Exit(code=1)
    console.print(f"[green]signature verified[/green]: {message}")


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
