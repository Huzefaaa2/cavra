from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Annotated, Optional

import yaml
import typer
from rich.console import Console
from rich.json import JSON

from cavra.agent import AgentSessionManager
from cavra.integrations import (
    CommandInterceptor,
    GitHubPRAttestationExporter,
    WebhookExporter,
)
from cavra.policy_registry import PolicyRegistry
from cavra.runtime import RuntimeGuard

console = Console()
app = typer.Typer(add_completion=False)
agent_app = typer.Typer(help="AI agent runtime commands.")
policy_app = typer.Typer(help="Policy registry commands.")
demo_app = typer.Typer(help="Runnable CAVRA demos.")
init_app = typer.Typer(help="Initialize CAVRA integrations.")
app.add_typer(agent_app, name="agent")
app.add_typer(policy_app, name="policy")
app.add_typer(demo_app, name="demo")
app.add_typer(init_app, name="init")


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
        console.print(f"[green]✓[/green] Command executed successfully")
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
    """Validate a policy pack has required CAVRA metadata and rule sections."""
    policy_path = path / "policy.yaml" if path.is_dir() else path
    if not policy_path.exists():
        console.print(f"[red]Policy not found:[/red] {policy_path}")
        raise typer.Exit(code=1)
    payload = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("metadata"), dict):
        console.print("[red]Invalid policy: missing metadata object.[/red]")
        raise typer.Exit(code=1)
    if not payload["metadata"].get("id"):
        console.print("[red]Invalid policy: missing metadata.id.[/red]")
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
def compile_policy(policy_pack: str = "cavra-ai-agent-baseline") -> None:
    """Compile a policy pack to normalized JSON."""
    registry = PolicyRegistry()
    console.print(JSON(json.dumps(registry.load_policy(policy_pack), indent=2)))


@policy_app.command("diff")
def diff_policy(left: Path, right: Path) -> None:
    """Show the paths being compared for policy review workflows."""
    console.print(f"CAVRA policy diff requested: {left} -> {right}")


@policy_app.command("sign")
def sign_policy(path: Path) -> None:
    """Create a deterministic local signature placeholder for a policy file."""
    import hashlib

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    sig_path = path.with_suffix(path.suffix + ".sig")
    sig_path.write_text(f"sha256:{digest}\n", encoding="utf-8")
    console.print(f"[green]signed[/green] {sig_path}")


@policy_app.command("verify")
def verify_policy(path: Path) -> None:
    """Verify the local SHA-256 signature created by `cavra policy sign`."""
    import hashlib

    sig_path = path.with_suffix(path.suffix + ".sig")
    expected = sig_path.read_text(encoding="utf-8").strip().removeprefix("sha256:")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected != actual:
        console.print("[red]signature verification failed[/red]")
        raise typer.Exit(code=1)
    console.print("[green]signature verified[/green]")


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
    output.mkdir(parents=True, exist_ok=True)
    evidence = {"product": "CAVRA", "tagline": "Before the agent acts, CAVRA decides.", "decisions": [d.to_dict() for d in decisions]}
    (output / "evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    (output / "sandbox-run-summary.json").write_text(json.dumps({"events": len(decisions), "blocked": sum(1 for d in decisions if d.decision == "block")}, indent=2), encoding="utf-8")
    (output / "pr-attestation.md").write_text("# CAVRA PR Attestation\n\nBefore the agent acts, CAVRA decides.\n\nGenerated for the Before the Agent Acts demo.\n", encoding="utf-8")
    (output / "compliance-mapping.md").write_text("# CAVRA Compliance Mapping\n\nMaps demo decisions to change control, least privilege, audit logging, and human oversight.\n", encoding="utf-8")
    for decision in decisions:
        console.print(f"{decision.action_type} {decision.target}: [bold]{decision.decision}[/bold] - {decision.reason}")
    console.print(f"[green]evidence generated[/green] {output}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
