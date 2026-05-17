import json
import time
from base64 import urlsafe_b64encode

from fastapi.testclient import TestClient

from cavra.api import create_app


def _b64url(data: bytes) -> str:
    return urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _signed_rs256_token(claims: dict[str, object], *, kid: str = "api-test-key") -> tuple[str, dict[str, object]]:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding, rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_numbers = private_key.public_key().public_numbers()
    jwk = {
        "kty": "RSA",
        "kid": kid,
        "alg": "RS256",
        "use": "sig",
        "n": _b64url(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, "big")),
        "e": _b64url(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, "big")),
    }
    signing_input = ".".join(
        [
            _b64url(json.dumps({"alg": "RS256", "kid": kid, "typ": "JWT"}, separators=(",", ":")).encode("utf-8")),
            _b64url(json.dumps(claims, separators=(",", ":")).encode("utf-8")),
        ]
    ).encode("ascii")
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{signing_input.decode('ascii')}.{_b64url(signature)}", {"keys": [jwk]}


def test_api_persists_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())

    response = client.post("/evidence", json={"session_id": "api-session", "decision_count": 2})

    assert response.status_code == 200
    assert response.json()["session_id"] == "api-session"
    assert client.get("/evidence").json()["items"][0]["session_id"] == "api-session"
    assert client.get("/evidence/api-session").json()["decision_count"] == 2


def test_api_filters_json_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    client = TestClient(create_app())
    client.post("/evidence", json={"session_id": "blocked-session", "signer": "security", "blocked_count": 2})
    client.post("/evidence", json={"session_id": "clean-session", "signer": "docs", "blocked_count": 0})

    response = client.get("/evidence", params={"signer": "security", "min_blocked": 1, "limit": 10})

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["session_id"] == "blocked-session"


def test_api_searches_sqlite_evidence_metadata(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_DB", str(tmp_path / "metadata.db"))
    client = TestClient(create_app())
    client.post("/evidence", json={"session_id": "blocked-session", "signer": "security", "blocked_count": 2})
    client.post("/evidence", json={"session_id": "clean-session", "signer": "docs", "blocked_count": 0})

    response = client.get("/evidence", params={"signer": "security", "min_blocked": 1, "limit": 10})

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["session_id"] == "blocked-session"


def test_api_console_config_and_cors(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_EVIDENCE_METADATA_DB", raising=False)
    monkeypatch.setenv("CAVRA_EVIDENCE_METADATA_STORE", str(tmp_path / "metadata.json"))
    monkeypatch.setenv("CAVRA_CORS_ORIGINS", "http://127.0.0.1:5173")
    monkeypatch.setenv("CAVRA_PUBLIC_API_BASE_URL", "https://cavra.example")
    client = TestClient(create_app())

    config = client.get("/console/config").json()
    cors = client.options(
        "/evidence",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert config["api_base_url"] == "https://cavra.example"
    assert config["metadata_mode"] == "json"
    assert cors.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


def test_api_approval_lifecycle(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post(
        "/approvals",
        json={"decision": decision, "requested_by": "developer"},
    )
    approval_id = created.json()["approval_id"]
    approved = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "platform-security", "reason": "Scoped IAM change reviewed.", "external_ref": "CHG-22"},
    )
    listed = client.get("/approvals", params={"state": "approved"})

    assert created.status_code == 200
    assert created.json()["state"] == "pending"
    assert approved.status_code == 200
    assert approved.json()["state"] == "approved"
    assert listed.json()["total"] == 1


def test_api_approval_sqlite_store(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_APPROVAL_STORE", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_DB", str(tmp_path / "approvals.db"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post("/approvals", json={"decision": decision, "requested_by": "developer"})
    config = client.get("/console/config").json()

    assert created.status_code == 200
    assert created.json()["state"] == "pending"
    assert client.get("/approvals", params={"state": "pending"}).json()["total"] == 1
    assert config["approval_mode"] == "sqlite"


def test_api_approval_uses_repository_routing_file(monkeypatch, tmp_path) -> None:
    routing = tmp_path / "routing.json"
    routing.write_text(
        '{"approval_routing":[{"rule_id_prefix":"filesystem.write","target_contains":"iam/","approver_group":"Cloud IAM Owners"}]}',
        encoding="utf-8",
    )
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_ROUTING_FILE", str(routing))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post("/approvals", json={"decision": decision, "requested_by": "developer"})

    assert created.status_code == 200
    assert created.json()["approver_group"] == "Cloud IAM Owners"


def test_api_approval_actor_claims_enforce_group(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    rejected = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "dev@example.com", "reason": "Not authorized.", "actor_claims": {"email": "dev@example.com", "groups": ["Developers"]}},
    )
    accepted = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "iam@example.com", "reason": "Authorized.", "actor_claims": {"email": "iam@example.com", "groups": ["IAM"]}},
    )

    assert rejected.status_code == 400
    assert accepted.status_code == 200
    assert accepted.json()["state"] == "approved"


def test_api_approval_actor_token_enforces_oidc_and_repository_rbac(monkeypatch, tmp_path) -> None:
    token, jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-approvals",
            "sub": "user-123",
            "email": "owner@example.com",
            "groups": ["github-team:payments-owners"],
            "repository": "payments/api",
            "exp": int(time.time()) + 300,
        }
    )
    oidc_config = tmp_path / "oidc.json"
    rbac_file = tmp_path / "rbac.json"
    oidc_config.write_text(
        json.dumps({"issuer": "https://issuer.example", "audience": "cavra-approvals", "jwks": jwks}),
        encoding="utf-8",
    )
    rbac_file.write_text(
        json.dumps(
            {
                "approval_rbac": {
                    "group_mappings": {"github-team:payments-owners": "Payments Owners"},
                    "repository_permissions": [
                        {
                            "repository": "payments/api",
                            "approver_group": "IAM",
                            "groups": ["Payments Owners"],
                            "actions": ["approved"],
                        }
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("CAVRA_APPROVAL_DB", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_OIDC_CONFIG", str(oidc_config))
    monkeypatch.setenv("CAVRA_APPROVAL_RBAC_FILE", str(rbac_file))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    decision["repository"] = "payments/api"
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    accepted = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "owner@example.com", "reason": "OIDC repository owner.", "actor_token": token},
    )
    config = client.get("/console/config").json()

    assert accepted.status_code == 200
    assert accepted.json()["state"] == "approved"
    assert config["approval_oidc"] == "configured"
    assert config["approval_rbac"] == "configured"


def test_api_approval_actor_token_rejects_without_oidc_config(monkeypatch, tmp_path) -> None:
    token, _jwks = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-approvals",
            "sub": "user-123",
            "groups": ["IAM"],
            "exp": int(time.time()) + 300,
        }
    )
    monkeypatch.delenv("CAVRA_APPROVAL_OIDC_CONFIG", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    rejected = client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "owner@example.com", "reason": "Needs OIDC config.", "actor_token": token},
    )

    assert rejected.status_code == 400


def test_api_approval_delivers_with_configured_provider(monkeypatch, tmp_path) -> None:
    provider_config = tmp_path / "providers.json"
    provider_config.write_text(
        '{"approval_providers":{"webhook":{"url":"https://approval.example/hook"}}}',
        encoding="utf-8",
    )
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    monkeypatch.setenv("CAVRA_APPROVAL_PROVIDER_CONFIG", str(provider_config))
    calls = []

    def fake_deliver(approval, config, *, provider, retries, timeout_seconds):
        calls.append((approval, config, provider, retries, timeout_seconds))
        return {
            "schema_version": "cavra.approval.delivery.v1",
            "approval_id": approval["approval_id"],
            "success": True,
            "deliveries": [{"provider": provider, "success": True}],
        }

    monkeypatch.setattr("cavra.api.deliver_provider_requests", fake_deliver)
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    delivered = client.post(f"/approvals/{approval_id}/deliver", json={"provider": "webhook", "retries": 1, "timeout_seconds": 3})
    config = client.get("/console/config").json()

    assert delivered.status_code == 200
    assert delivered.json()["success"] is True
    assert calls[0][2:] == ("webhook", 1, 3.0)
    assert config["approval_provider_delivery"] == "configured"


def test_api_approval_delivery_requires_provider_config(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CAVRA_APPROVAL_PROVIDER_CONFIG", raising=False)
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()
    approval_id = client.post("/approvals", json={"decision": decision, "requested_by": "developer"}).json()["approval_id"]

    delivered = client.post(f"/approvals/{approval_id}/deliver", json={"provider": "webhook"})

    assert delivered.status_code == 400


def test_api_approval_accepts_raw_decision_payload(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    created = client.post("/approvals", json=decision)

    assert created.status_code == 200
    assert created.json()["decision_id"] == decision["decision_id"]


def test_api_break_glass_requires_reason(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CAVRA_APPROVAL_STORE", str(tmp_path / "approvals.json"))
    client = TestClient(create_app())
    decision = client.post(
        "/decisions",
        json={"action_type": "write_file", "target": "iam/admin-role.tf"},
    ).json()

    rejected = client.post("/approvals/break-glass", json={"decision": decision, "actor": "incident-commander"})
    accepted = client.post(
        "/approvals/break-glass",
        json={
            "decision": decision,
            "actor": "incident-commander",
            "reason": "Production recovery for active incident.",
            "external_ref": "INC-9",
        },
    )

    assert rejected.status_code == 400
    assert accepted.status_code == 200
    assert accepted.json()["state"] == "break_glass"
    assert accepted.json()["external_ref"] == "INC-9"
