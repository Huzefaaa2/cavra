from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cavra import __version__
from cavra.api import create_app


OPENAPI_PATH = Path("openapi/cavra-api.openapi.json")
REQUIRED_PATHS = [
    "/health",
    "/version",
    "/console/config",
    "/decisions",
    "/approvals",
    "/evidence",
    "/aispm/posture",
    "/aispm/dashboard/contract",
]


def main() -> None:
    failures: list[str] = []
    if not OPENAPI_PATH.exists():
        raise SystemExit(f"missing OpenAPI contract: {OPENAPI_PATH}")

    checked_in = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    generated = create_app().openapi()
    if checked_in != generated:
        failures.append("checked-in OpenAPI contract is stale; run python scripts/export_openapi_contract.py")

    if checked_in.get("info", {}).get("title") != "CAVRA API":
        failures.append("OpenAPI title must be CAVRA API")
    if checked_in.get("info", {}).get("version") != __version__:
        failures.append(f"OpenAPI version must match package version {__version__}")
    versioning = checked_in.get("x-cavra-api-versioning")
    if not isinstance(versioning, dict):
        failures.append("OpenAPI contract is missing x-cavra-api-versioning")
    else:
        if versioning.get("public_contract") != "cavra.api.v1":
            failures.append("OpenAPI public contract marker must be cavra.api.v1")
        if "Breaking changes require" not in str(versioning.get("compatibility", "")):
            failures.append("OpenAPI compatibility policy is missing breaking-change guidance")
    governed_assets = checked_in.get("x-cavra-governed-assets", [])
    if governed_assets != ["agent_actions", "models_and_artifacts"]:
        failures.append("OpenAPI governed asset marker must include agent actions and models/artifacts")

    paths = checked_in.get("paths", {})
    for required_path in REQUIRED_PATHS:
        if required_path not in paths:
            failures.append(f"OpenAPI contract is missing required path {required_path}")

    if failures:
        raise SystemExit("\n".join(failures))
    print("OpenAPI contract validated")


if __name__ == "__main__":
    main()
