from __future__ import annotations

import textwrap
from pathlib import Path

from cavra.go_backend import (
    GO_BACKEND_DISABLED,
    GO_BACKEND_ENFORCE,
    GO_BACKEND_SHADOW,
    GoBackendConfig,
    evaluate_with_go_pilot,
    go_backend_config_from_env,
    go_backend_readiness_report,
)


def test_go_backend_defaults_to_disabled(monkeypatch) -> None:
    monkeypatch.delenv("CAVRA_GO_BACKEND_MODE", raising=False)

    config = go_backend_config_from_env()
    report = go_backend_readiness_report(config)

    assert config.mode == GO_BACKEND_DISABLED
    assert report["status"] == "disabled"
    assert next(item for item in report["checks"] if item["id"] == "python_fallback")["status"] == "pass"


def test_go_backend_readiness_requires_binary_and_policy(tmp_path: Path) -> None:
    config = GoBackendConfig(
        mode=GO_BACKEND_SHADOW,
        runtime_path=str(tmp_path / "missing-runtime"),
        policy_path=str(tmp_path / "missing-policy.json"),
    )

    report = go_backend_readiness_report(config)

    assert report["status"] == "needs_attention"
    assert next(item for item in report["checks"] if item["id"] == "go_runtime_binary")["status"] == "warn"
    assert next(item for item in report["checks"] if item["id"] == "go_runtime_policy")["status"] == "warn"


def test_go_backend_shadow_uses_python_when_go_matches(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")
    request = {
        "action_type": "execute_command",
        "target": "terraform plan",
        "policy_pack": "cavra-ai-agent-baseline",
    }

    result = evaluate_with_go_pilot(
        request,
        config=GoBackendConfig(mode=GO_BACKEND_SHADOW, runtime_path=str(runtime), policy_path=str(policy)),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is False
    assert result["parity_match"] is True
    assert result["go_decision"]["decision"] == "allow"


def test_go_backend_enforce_selects_go_when_parity_matches(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="allow", rule_id="commands.allow", severity="low")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(mode=GO_BACKEND_ENFORCE, runtime_path=str(runtime), policy_path=str(policy)),
    )

    assert result["selected_backend"] == "go"
    assert result["effective_decision"] == result["go_decision"]


def test_go_backend_falls_back_when_go_diverges(tmp_path: Path) -> None:
    runtime = _fake_go_runtime(tmp_path, decision="block", rule_id="commands.block", severity="critical")
    policy = tmp_path / "policy.json"
    policy.write_text("{}", encoding="utf-8")

    result = evaluate_with_go_pilot(
        {"action_type": "execute_command", "target": "terraform plan"},
        config=GoBackendConfig(mode=GO_BACKEND_ENFORCE, runtime_path=str(runtime), policy_path=str(policy)),
    )

    assert result["selected_backend"] == "python"
    assert result["fallback_used"] is True
    assert result["fallback_reason"] == "go decision diverged from Python parity gate"
    assert result["effective_decision"]["decision"] == "allow"


def _fake_go_runtime(tmp_path: Path, *, decision: str, rule_id: str, severity: str) -> Path:
    path = tmp_path / "fake-cavra-runtime"
    path.write_text(
        textwrap.dedent(
            f"""\
            #!/usr/bin/env python3
            import json
            import sys

            payload = json.loads(sys.stdin.read() or "{{}}")
            print(json.dumps({{
                "decision": "{decision}",
                "reason": "fake go runtime",
                "action_type": payload.get("action_type", "execute_command"),
                "target": payload.get("target", ""),
                "requested_operation": payload.get("target", ""),
                "policy_pack": payload.get("policy_pack", "cavra-ai-agent-baseline"),
                "policy_id": payload.get("policy_pack", "cavra-ai-agent-baseline"),
                "rule_id": "{rule_id}",
                "severity": "{severity}"
            }}))
            """
        ),
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path
