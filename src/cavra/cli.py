from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.json import JSON

from cavra.agent import AgentSessionManager
from cavra.evidence import (
    EvidenceMetadataStore,
    SQLiteEvidenceMetadataStore,
    create_evidence_bundle,
    export_attestation_verification,
    export_immutable_storage_plan,
    export_key_trust_root,
    export_retention_policy,
    export_siem_payloads,
    generate_ed25519_keypair,
    verify_evidence_bundle,
)
from cavra.integrations import CommandInterceptor
from cavra.policy_engine import (
    compile_policy as compile_policy_payload,
    diff_policies,
    load_policy_file,
    validate_policy as validate_policy_payload,
    verify_policy_signature,
    write_policy_signature,
)
from cavra.policy_registry import PolicyRegistry
from cavra.runtime import RuntimeGuard

console = Console()
app = typer.Typer(add_completion=False)
agent_app = typer.Typer(help="AI agent runtime commands.")
policy_app = typer.Typer(help="Policy registry commands.")
demo_app = typer.Typer(help="Runnable CAVRA demos.")
init_app = typer.Typer(help="Initialize CAVRA integrations.")
evidence_app = typer.Typer(help="Evidence bundle commands.")
app.add_typer(agent_app, name="agent")
app.add_typer(policy_app, name="policy")
app.add_typer(demo_app, name="demo")
app.add_typer(init_app, name="init")
app.add_typer(evidence_app, name="evidence")


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
    limit: Annotated[int, typer.Option(help="Page size.")] = 50,
    offset: Annotated[int, typer.Option(help="Page offset.")] = 0,
) -> None:
    """Search SQLite-backed evidence metadata with filters and pagination."""
    result = SQLiteEvidenceMetadataStore(sqlite).search(
        session_id=session_id,
        signer=signer,
        min_blocked=min_blocked,
        has_approvals=has_approvals,
        limit=limit,
        offset=offset,
    )
    console.print(JSON(json.dumps(result, indent=2)))


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
