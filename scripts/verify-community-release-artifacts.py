#!/usr/bin/env python3
"""Verify public CAVRA Community release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import venv
from pathlib import Path
from typing import Any


DEFAULT_TAG = "community-v0.1.1"
DEFAULT_VERSION = "0.1.1"
DEFAULT_WHEEL_SHA256 = "32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a"
DEFAULT_SDIST_SHA256 = "b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950"
RELEASE_BASE_URL = "https://github.com/Huzefaaa2/cavra/releases/download"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/octet-stream",
            "User-Agent": "cavra-community-release-verifier/1.0",
        },
    )
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                output_path.write_bytes(response.read())
            return
        except Exception as exc:  # pragma: no cover - network retry branch
            last_error = exc
            if attempt < 3:
                time.sleep(attempt)
    if last_error is not None:
        raise last_error


def run_command(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def smoke_install_wheel(wheel_path: Path) -> str:
    with tempfile.TemporaryDirectory(prefix="cavra-release-smoke-") as temp_dir:
        venv_dir = Path(temp_dir) / "venv"
        venv.EnvBuilder(with_pip=True).create(venv_dir)
        python = venv_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        cavra = venv_dir / ("Scripts/cavra.exe" if sys.platform == "win32" else "bin/cavra")

        run_command([str(python), "-m", "pip", "install", "--upgrade", "pip"])
        run_command([str(python), "-m", "pip", "install", str(wheel_path)])
        return run_command([str(cavra), "version"])


def verify_release(
    *,
    tag: str,
    version: str,
    wheel_sha256: str,
    sdist_sha256: str,
    output_dir: Path,
    skip_install_smoke: bool,
) -> dict[str, Any]:
    wheel_name = f"cavra-{version}-py3-none-any.whl"
    sdist_name = f"cavra-{version}.tar.gz"
    artifacts = [
        {
            "name": wheel_name,
            "url": f"{RELEASE_BASE_URL}/{tag}/{wheel_name}",
            "expected_sha256": wheel_sha256,
        },
        {
            "name": sdist_name,
            "url": f"{RELEASE_BASE_URL}/{tag}/{sdist_name}",
            "expected_sha256": sdist_sha256,
        },
    ]

    verified_artifacts: list[dict[str, Any]] = []
    for artifact in artifacts:
        output_path = output_dir / artifact["name"]
        download(str(artifact["url"]), output_path)
        actual_sha256 = sha256_file(output_path)
        verified_artifacts.append(
            {
                **artifact,
                "path": str(output_path),
                "actual_sha256": actual_sha256,
                "sha256_match": actual_sha256 == artifact["expected_sha256"],
            }
        )

    if not all(item["sha256_match"] for item in verified_artifacts):
        raise ValueError("One or more release artifact checksums did not match.")

    install_smoke = None
    if not skip_install_smoke:
        install_smoke = {
            "command": "cavra version",
            "output": smoke_install_wheel(output_dir / wheel_name),
            "status": "pass",
        }

    return {
        "schema_version": "cavra.community_release_verification.v1",
        "tag": tag,
        "version": version,
        "release_url": f"https://github.com/Huzefaaa2/cavra/releases/tag/{tag}",
        "artifacts": verified_artifacts,
        "install_smoke": install_smoke,
        "status": "pass",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", default=DEFAULT_TAG, help="Release tag to verify.")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="Package version to verify.")
    parser.add_argument("--wheel-sha256", default=DEFAULT_WHEEL_SHA256, help="Expected wheel SHA-256.")
    parser.add_argument("--sdist-sha256", default=DEFAULT_SDIST_SHA256, help="Expected source distribution SHA-256.")
    parser.add_argument("--output-dir", type=Path, help="Directory for downloaded artifacts.")
    parser.add_argument(
        "--skip-install-smoke",
        action="store_true",
        help="Skip clean virtualenv installation smoke test.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="cavra-community-release-"))
    try:
        result = verify_release(
            tag=args.tag,
            version=args.version,
            wheel_sha256=args.wheel_sha256,
            sdist_sha256=args.sdist_sha256,
            output_dir=output_dir,
            skip_install_smoke=args.skip_install_smoke,
        )
    except Exception as exc:
        print(f"CAVRA Community release artifact verification failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if args.output_dir is None and output_dir.exists():
            shutil.rmtree(output_dir, ignore_errors=True)

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
