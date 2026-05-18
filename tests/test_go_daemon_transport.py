from pathlib import Path


def test_go_daemon_transport_docs_reference_socket_contract() -> None:
    doc = Path("docs/go-daemon-transport.md").read_text(encoding="utf-8")
    wiki = Path("docs/wiki/Go-Daemon-Transport.md").read_text(encoding="utf-8")

    assert "go/cavra-runtime/daemon" in doc
    assert "--serve" in doc
    assert "Unix-socket" in doc
    assert "EvaluateRequest" in doc
    assert "DecisionResponse" in doc
    assert "go/cavra-runtime/daemon" in wiki


def test_go_runtime_readme_references_daemon_mode() -> None:
    readme = Path("go/cavra-runtime/README.md").read_text(encoding="utf-8")

    assert "--serve" in readme
    assert "--socket" in readme
    assert "EvaluateRequest" in readme
    assert "DecisionResponse" in readme
