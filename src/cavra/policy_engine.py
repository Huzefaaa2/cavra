from __future__ import annotations

import base64
import hashlib
import hmac
import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"
PACKAGE_SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


class PolicyValidationError(ValueError):
    pass


@dataclass(frozen=True)
class PolicyDiff:
    added: list[str]
    removed: list[str]
    changed: list[str]

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "added": self.added,
            "removed": self.removed,
            "changed": self.changed,
        }


def load_policy_file(path: Path) -> dict[str, Any]:
    policy_path = path / "policy.yaml" if path.is_dir() else path
    payload = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise PolicyValidationError(f"Policy must be a YAML object: {policy_path}")
    return payload


def load_policy_schema(schema_path: Path | None = None) -> dict[str, Any]:
    candidates = [
        schema_path,
        Path.cwd() / "schemas" / "policy.schema.json",
        SCHEMA_DIR / "policy.schema.json",
        PACKAGE_SCHEMA_DIR / "policy.schema.json",
    ]
    path = next((candidate for candidate in candidates if candidate and candidate.exists()), None)
    if path is None:
        raise PolicyValidationError("CAVRA policy schema not found.")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_policy(payload: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    validator = Draft202012Validator(schema or load_policy_schema())
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        return [format_validation_error(error) for error in errors]
    return []


def format_validation_error(error: Any) -> str:
    path = ".".join(str(item) for item in error.path) or "<root>"
    return f"{path}: {error.message}"


def normalize_policy(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(payload)
    for section in ("filesystem", "commands"):
        if section in normalized and isinstance(normalized[section], dict):
            for key, value in normalized[section].items():
                if isinstance(value, list):
                    normalized[section][key] = sorted(str(item) for item in value)
    if "mcp" in normalized and isinstance(normalized["mcp"], dict):
        for key in ("allowed_servers", "blocked_servers"):
            if isinstance(normalized["mcp"].get(key), list):
                normalized["mcp"][key] = sorted(str(item) for item in normalized["mcp"][key])
    return normalized


def compile_policy(policy: dict[str, Any], overlays: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    compiled = deepcopy(policy)
    for overlay in overlays or []:
        compiled = merge_policy(compiled, overlay)
    return normalize_policy(compiled)


def merge_policy(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if key == "metadata":
            merged[key] = merge_metadata(merged.get(key, {}), value)
        elif isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_policy_section(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def merge_metadata(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if key == "inherits":
            merged[key] = value
        elif value is not None:
            merged[key] = value
    return merged


def merge_policy_section(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, list) and isinstance(merged.get(key), list):
            merged[key] = dedupe([*merged[key], *value])
        elif isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_policy_section(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def dedupe(items: list[Any]) -> list[Any]:
    seen: set[str] = set()
    result: list[Any] = []
    for item in items:
        marker = json.dumps(item, sort_keys=True)
        if marker in seen:
            continue
        seen.add(marker)
        result.append(item)
    return result


def diff_policies(left: dict[str, Any], right: dict[str, Any]) -> PolicyDiff:
    left_flat = flatten(normalize_policy(left))
    right_flat = flatten(normalize_policy(right))
    left_keys = set(left_flat)
    right_keys = set(right_flat)
    changed = sorted(key for key in left_keys & right_keys if left_flat[key] != right_flat[key])
    return PolicyDiff(
        added=sorted(right_keys - left_keys),
        removed=sorted(left_keys - right_keys),
        changed=changed,
    )


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else str(key)
            result.update(flatten(value[key], child))
        return result
    if isinstance(value, list):
        return {prefix: sorted(value) if all(isinstance(item, str) for item in value) else value}
    return {prefix: value}


def policy_digest(policy_bytes: bytes) -> str:
    return hashlib.sha256(policy_bytes).hexdigest()


def generate_policy_signing_keypair(
    private_key_path: Path,
    public_key_path: Path,
    *,
    key_id: str = "local-policy-signing-key",
) -> dict[str, Any]:
    """Generate a public Community Ed25519 policy signing keypair.

    The private key is written only to the caller-provided local path. The
    public repository should commit public trust roots, not generated private
    keys.
    """

    if not key_id.strip():
        raise ValueError("key_id is required")
    private_key_path.parent.mkdir(parents=True, exist_ok=True)
    public_key_path.parent.mkdir(parents=True, exist_ok=True)
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    private_key_path.write_bytes(private_pem)
    public_key_path.write_bytes(public_pem)
    return {
        "schema_version": "cavra.policy-signing-keypair.v1",
        "algorithm": "Ed25519",
        "key_id": key_id,
        "private_key_path": str(private_key_path),
        "public_key_path": str(public_key_path),
        "public_key_sha256": hashlib.sha256(public_pem).hexdigest(),
    }


def create_policy_signature(
    policy_path: Path,
    signer: str = "local",
    key: str | None = None,
    *,
    private_key_path: Path | None = None,
    key_id: str | None = None,
) -> dict[str, Any]:
    data = policy_path.read_bytes()
    digest = policy_digest(data)
    if private_key_path is not None:
        private_key = serialization.load_pem_private_key(private_key_path.read_bytes(), password=None)
        if not isinstance(private_key, ed25519.Ed25519PrivateKey):
            raise ValueError("policy signing private key must be Ed25519")
        signature = private_key.sign(data)
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return {
            "schema_version": "cavra.policy-signature.v1",
            "algorithm": "Ed25519",
            "digest": f"sha256:{digest}",
            "signature": base64.b64encode(signature).decode("ascii"),
            "signed_at": datetime.now(timezone.utc).isoformat(),
            "signer": signer,
            "key_id": key_id or signer,
            "public_key_sha256": hashlib.sha256(public_pem).hexdigest(),
            "policy_file": policy_path.name,
        }
    secret = (key or digest).encode("utf-8")
    signature = hmac.new(secret, data, hashlib.sha256).digest()
    return {
        "schema_version": "cavra.policy-signature.v1",
        "algorithm": "HS256" if key else "SHA256",
        "digest": f"sha256:{digest}",
        "signature": base64.b64encode(signature).decode("ascii"),
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "signer": signer,
        "policy_file": policy_path.name,
    }


def write_policy_signature(
    policy_path: Path,
    signer: str = "local",
    key: str | None = None,
    *,
    private_key_path: Path | None = None,
    key_id: str | None = None,
) -> Path:
    payload = create_policy_signature(
        policy_path,
        signer=signer,
        key=key,
        private_key_path=private_key_path,
        key_id=key_id,
    )
    sig_path = policy_path.with_suffix(policy_path.suffix + ".sig.json")
    sig_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return sig_path


def verify_policy_signature(
    policy_path: Path,
    signature_path: Path | None = None,
    key: str | None = None,
    *,
    public_key_path: Path | None = None,
) -> tuple[bool, str]:
    sig_path = signature_path or policy_path.with_suffix(policy_path.suffix + ".sig.json")
    if not sig_path.exists():
        legacy_path = policy_path.with_suffix(policy_path.suffix + ".sig")
        if legacy_path.exists():
            expected = legacy_path.read_text(encoding="utf-8").strip()
            actual = f"sha256:{policy_digest(policy_path.read_bytes())}"
            return expected == actual, "legacy SHA-256 signature"
        return False, f"signature file not found: {sig_path}"
    payload = json.loads(sig_path.read_text(encoding="utf-8"))
    actual_digest = f"sha256:{policy_digest(policy_path.read_bytes())}"
    if payload.get("digest") != actual_digest:
        return False, "policy digest mismatch"
    if payload.get("algorithm") == "Ed25519":
        if public_key_path is None:
            return False, "public key is required for Ed25519 policy signature verification"
        try:
            public_key = serialization.load_pem_public_key(public_key_path.read_bytes())
            if not isinstance(public_key, ed25519.Ed25519PublicKey):
                return False, "policy signing public key must be Ed25519"
            expected_fingerprint = hashlib.sha256(public_key_path.read_bytes()).hexdigest()
            if payload.get("public_key_sha256") != expected_fingerprint:
                return False, "policy signing public key fingerprint mismatch"
            signature = base64.b64decode(str(payload.get("signature", "")), validate=True)
            public_key.verify(signature, policy_path.read_bytes())
        except Exception as exc:
            return False, f"Ed25519 signature mismatch: {exc}"
        return True, "verified Ed25519 signature"
    expected = create_policy_signature(
        policy_path,
        signer=payload.get("signer", "local"),
        key=key,
    )
    if key and payload.get("signature") != expected["signature"]:
        return False, "HMAC signature mismatch"
    return True, f"verified {payload.get('algorithm', 'unknown')} signature"
