#!/usr/bin/env python3
"""Generate the public CAVRA CLI reference from Typer help output."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
ADD_TYPER_RE = re.compile(r"app\.add_typer\((?P<app>\w+),\s*name=\"(?P<name>[^\"]+)\"")
DECORATOR_RE = re.compile(r"@(?P<app>\w+)\.command\((?P<args>[^)]*)\)")
FUNCTION_RE = re.compile(r"def\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\(")


@dataclass(frozen=True)
class Command:
    path: tuple[str, ...]
    title: str


def _command_name_from_decorator(args: str, function_name: str) -> str:
    args = args.strip()
    if args:
        match = re.match(r"['\"]([^'\"]+)['\"]", args)
        if match:
            return match.group(1)
    return function_name.replace("_", "-")


def _discover_commands(cli_path: Path) -> list[Command]:
    source = cli_path.read_text(encoding="utf-8").splitlines()
    group_names: dict[str, str] = {}
    commands: list[Command] = []

    for line in source:
        match = ADD_TYPER_RE.search(line)
        if match:
            group_names[match.group("app")] = match.group("name")

    for index, line in enumerate(source):
        decorator = DECORATOR_RE.search(line)
        if not decorator:
            continue

        function_name = ""
        for next_line in source[index + 1 : index + 8]:
            function = FUNCTION_RE.search(next_line)
            if function:
                function_name = function.group("name")
                break

        if not function_name:
            raise RuntimeError(f"Unable to discover function for decorator on line {index + 1}")

        app_name = decorator.group("app")
        command_name = _command_name_from_decorator(decorator.group("args"), function_name)
        if app_name == "app":
            path = (command_name,)
        else:
            group_name = group_names.get(app_name)
            if not group_name:
                raise RuntimeError(f"Unable to map Typer app {app_name!r} to command group")
            path = (group_name, command_name)
        commands.append(Command(path=path, title=" ".join(path)))

    root = Command(path=(), title="cavra")
    groups = [Command(path=(name,), title=f"cavra {name}") for name in group_names.values()]
    discovered: list[Command] = [root, *groups, *commands]
    unique: dict[tuple[str, ...], Command] = {}
    for command in discovered:
        unique.setdefault(command.path, command)
    return list(unique.values())


def _run_help(repo_root: Path, path: tuple[str, ...]) -> str:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    env["COLUMNS"] = "140"
    env["NO_COLOR"] = "1"
    env["TERM"] = "dumb"
    cmd = [sys.executable, "-m", "cavra.cli", *path, "--help"]
    result = subprocess.run(
        cmd,
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    output = ANSI_RE.sub("", output).rstrip()
    if result.returncode != 0:
        raise RuntimeError(
            f"Help command failed for {' '.join(['cavra', *path])}: "
            f"exit={result.returncode}\n{output}"
        )
    return output


def _anchor(command: Command) -> str:
    text = "cavra" if not command.path else "cavra-" + "-".join(command.path)
    return text.lower().replace("_", "-")


def _manual_filename(command: Command) -> str:
    if not command.path:
        return "cavra.md"
    return "cavra_" + "_".join(part.replace("-", "_") for part in command.path) + ".md"


def _manual_title(command: Command) -> str:
    return "cavra" if not command.path else "cavra " + " ".join(command.path)


def _render(repo_root: Path, commands: list[Command]) -> str:
    version = _read_version(repo_root)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# CAVRA Full CLI Reference",
        "",
        f"Generated from Typer help output for CAVRA `{version}` on {now}.",
        "",
        "This is the authoritative command reference for the public CAVRA CLI. "
        "If a shorter guide and this generated reference disagree, prefer this file "
        "and regenerate it from the current source tree.",
        "",
        "## Regenerate",
        "",
        "```bash",
        "python3 scripts/generate_cli_reference.py --repo-root .",
        "```",
        "",
        "## Command Index",
        "",
    ]
    for command in commands:
        label = "cavra" if not command.path else "cavra " + " ".join(command.path)
        lines.append(f"- [{label}](#{_anchor(command)})")

    lines.append("")
    for command in commands:
        label = "cavra" if not command.path else "cavra " + " ".join(command.path)
        lines.extend(
            [
                f"## `{label}`",
                "",
                "```text",
                _run_help(repo_root, command.path),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_manual_index(commands: list[Command]) -> str:
    lines = [
        "# CAVRA CLI Manual",
        "",
        "This directory contains GitHub CLI-style manual pages generated from the live Typer command surface.",
        "",
        "Regenerate after CLI changes:",
        "",
        "```bash",
        "python3 scripts/generate_cli_reference.py --repo-root .",
        "```",
        "",
        "## Commands",
        "",
    ]
    for command in commands:
        label = _manual_title(command)
        lines.append(f"- [`{label}`]({_manual_filename(command)})")
    return "\n".join(lines).rstrip() + "\n"


def _render_manual_page(repo_root: Path, command: Command, commands: list[Command]) -> str:
    label = _manual_title(command)
    parent = command.path[:-1]
    siblings = [
        candidate
        for candidate in commands
        if candidate.path
        and candidate.path[:-1] == parent
        and candidate.path != command.path
    ]
    group_children = [
        candidate
        for candidate in commands
        if candidate.path
        and candidate.path[:-1] == command.path
    ]
    related = siblings[:8] if siblings else group_children[:8]
    lines = [
        f"# {label}",
        "",
        "## Name",
        "",
        f"`{label}` - generated CAVRA CLI manual page.",
        "",
        "## Synopsis",
        "",
        "```bash",
        f"{label} --help",
        "```",
        "",
        "## Description",
        "",
        "This page is generated from the command's Typer help output. Use it as the "
        "authoritative option reference for this command.",
        "",
        "## Help Output",
        "",
        "```text",
        _run_help(repo_root, command.path),
        "```",
        "",
    ]
    if related:
        lines.extend(["## See Also", ""])
        for item in related:
            lines.append(f"- [`{_manual_title(item)}`]({_manual_filename(item)})")
        lines.append("")
    lines.extend(
        [
            "## Regenerate",
            "",
            "```bash",
            "python3 scripts/generate_cli_reference.py --repo-root .",
            "```",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_wiki_manual_index() -> str:
    return """# CAVRA CLI Manual

The generated GitHub CLI-style manual pages live in the main repository:

- [CAVRA CLI Manual Index](https://github.com/Huzefaaa2/cavra/tree/main/docs/cli-manual)
- [Generated Full CLI Reference](CLI-Reference.md)
- [CLI Guide](CLI.md)

The manual pages are generated from Typer help output by:

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
"""


def _read_version(repo_root: Path) -> str:
    init_path = repo_root / "src" / "cavra" / "__init__.py"
    match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", init_path.read_text(encoding="utf-8"))
    if match:
        return match.group(1)
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are not current")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    commands = _discover_commands(repo_root / "src" / "cavra" / "cli.py")
    rendered = _render(repo_root, commands)
    targets = [
        repo_root / "docs" / "cli-reference.md",
        repo_root / "docs" / "wiki" / "CLI-Reference.md",
    ]
    manual_dir = repo_root / "docs" / "cli-manual"
    manual_targets = [manual_dir / "README.md", *(manual_dir / _manual_filename(command) for command in commands)]
    wiki_manual_index = repo_root / "docs" / "wiki" / "CLI-Manual.md"
    targets.extend(manual_targets)
    targets.append(wiki_manual_index)

    if args.check:
        expected: dict[Path, str] = {
            repo_root / "docs" / "cli-reference.md": rendered,
            repo_root / "docs" / "wiki" / "CLI-Reference.md": rendered,
            manual_dir / "README.md": _render_manual_index(commands),
            wiki_manual_index: _render_wiki_manual_index(),
        }
        for command in commands:
            expected[manual_dir / _manual_filename(command)] = _render_manual_page(repo_root, command, commands)
        stale = [
            str(path.relative_to(repo_root))
            for path in targets
            if not path.exists() or path.read_text(encoding="utf-8") != expected[path]
        ]
        if stale:
            print("CLI reference is stale:", ", ".join(stale), file=sys.stderr)
            return 1
        print("CLI reference is current.")
        return 0

    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target == repo_root / "docs" / "cli-reference.md" or target == repo_root / "docs" / "wiki" / "CLI-Reference.md":
            content = rendered
        elif target == manual_dir / "README.md":
            content = _render_manual_index(commands)
        elif target == wiki_manual_index:
            content = _render_wiki_manual_index()
        else:
            command = next(item for item in commands if manual_dir / _manual_filename(item) == target)
            content = _render_manual_page(repo_root, command, commands)
        target.write_text(content, encoding="utf-8")
        print(f"Wrote {target.relative_to(repo_root)}")
    print(f"Documented {len(commands)} help surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
