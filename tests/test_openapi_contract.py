from __future__ import annotations

import json
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from cavra import __version__
from cavra.api import create_app


def test_api_version_and_openapi_metadata_match_package() -> None:
    client = TestClient(create_app())

    version = client.get("/version").json()
    openapi = client.get("/openapi.json").json()

    assert version["version"] == __version__
    assert openapi["info"]["version"] == __version__
    assert openapi["x-cavra-api-versioning"]["public_contract"] == "cavra.api.v1"
    assert openapi["x-cavra-governed-assets"] == ["agent_actions", "models_and_artifacts"]


def test_checked_in_openapi_contract_is_current() -> None:
    checked_in = json.loads(Path("openapi/cavra-api.openapi.json").read_text(encoding="utf-8"))
    generated = create_app().openapi()

    assert checked_in == generated


def test_openapi_contract_validator_passes() -> None:
    subprocess.run(["python3", "scripts/validate_openapi_contract.py"], check=True)
