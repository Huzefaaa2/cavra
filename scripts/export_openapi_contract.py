from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cavra.api import create_app


DEFAULT_OUTPUT = Path("openapi/cavra-api.openapi.json")


def export_openapi_contract(output: Path = DEFAULT_OUTPUT) -> Path:
    app = create_app()
    schema = app.openapi()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def main() -> None:
    output = export_openapi_contract()
    print(f"CAVRA OpenAPI contract written: {output}")


if __name__ == "__main__":
    main()
