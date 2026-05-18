from pathlib import Path


def test_go_daemon_transport_docs_reference_socket_contract() -> None:
    doc = Path("docs/go-daemon-transport.md").read_text(encoding="utf-8")
    wiki = Path("docs/wiki/Go-Daemon-Transport.md").read_text(encoding="utf-8")

    assert "go/cavra-runtime/daemon" in doc
    assert "--serve" in doc
    assert "--daemon" in doc
    assert "Unix-socket" in doc
    assert "EvaluateRequest" in doc
    assert "DecisionResponse" in doc
    assert "daemon.Client" in doc
    assert "go/cavra-runtime/daemon" in wiki


def test_go_runtime_readme_references_daemon_mode() -> None:
    readme = Path("go/cavra-runtime/README.md").read_text(encoding="utf-8")

    assert "--serve" in readme
    assert "--daemon" in readme
    assert "--socket" in readme
    assert "EvaluateRequest" in readme
    assert "DecisionResponse" in readme


def test_go_daemon_client_helper_is_present() -> None:
    client = Path("go/cavra-runtime/daemon/client.go").read_text(encoding="utf-8")
    cli = Path("go/cavra-runtime/cmd/cavra-runtime/main.go").read_text(encoding="utf-8")

    assert "type Client struct" in client
    assert "func NewClient" in client
    assert "func (client Client) Evaluate" in client
    assert 'flag.Bool("daemon"' in cli
    assert "daemon.NewClient(socket).Evaluate" in cli
