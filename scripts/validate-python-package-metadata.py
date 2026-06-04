#!/usr/bin/env python3
"""Validate Community Python packaging metadata and distribution checks."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from email.parser import Parser
from pathlib import Path
from zipfile import ZipFile


METADATA_WARNING_MARKERS = (
    "_MissingDynamic",
    "SetuptoolsWarning",
    "SetuptoolsDeprecationWarning",
    "License classifiers are deprecated",
    "`project.license` as a TOML table is deprecated",
    "`install_requires` overwritten in `pyproject.toml`",
    "`extras_require` overwritten in `pyproject.toml`",
    "warning: no files found matching",
    "Package would be ignored",
)
REQUIRED_PROJECT_URLS = {
    "Bug Tracker, https://github.com/Huzefaaa2/cavra/issues",
    "Documentation, https://github.com/Huzefaaa2/cavra/tree/main/docs",
    "Source Code, https://github.com/Huzefaaa2/cavra",
}
REQUIRED_LICENSE_FILES = {"LICENSE", "NOTICE"}


def _run(command: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def _cleanup_generated_paths(root: Path) -> None:
    for relative in ("build", "src/cavra.egg-info", "cavra.egg-info"):
        path = root / relative
        if path.exists():
            shutil.rmtree(path)


def _wheel_metadata(wheel: Path) -> tuple[object, set[str]]:
    with ZipFile(wheel) as archive:
        metadata_name = next(
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        )
        names = set(archive.namelist())
        metadata = Parser().parsestr(archive.read(metadata_name).decode("utf-8"))
    return metadata, names


def validate(root: Path) -> list[str]:
    """Return validation errors for Community package metadata."""

    errors: list[str] = []
    root = root.resolve()
    _cleanup_generated_paths(root)

    with tempfile.TemporaryDirectory(prefix="cavra-package-metadata-") as temp_dir:
        out_dir = Path(temp_dir)
        build_result = _run(
            [sys.executable, "-m", "build", "--outdir", str(out_dir)],
            root,
        )
        build_output = build_result.stdout
        if build_result.returncode != 0:
            errors.append("python -m build failed")
            errors.append(build_output)
            return errors

        for marker in METADATA_WARNING_MARKERS:
            if marker in build_output:
                errors.append(f"build output contains packaging warning marker: {marker}")

        twine_result = _run(
            [sys.executable, "-m", "twine", "check", *map(str, out_dir.glob("*"))],
            root,
        )
        if twine_result.returncode != 0:
            errors.append("twine check failed")
            errors.append(twine_result.stdout)

        wheels = sorted(out_dir.glob("*.whl"))
        sdists = sorted(out_dir.glob("*.tar.gz"))
        if len(wheels) != 1:
            errors.append(f"expected exactly one wheel, found {len(wheels)}")
        if len(sdists) != 1:
            errors.append(f"expected exactly one source distribution, found {len(sdists)}")

        if wheels:
            metadata, archive_names = _wheel_metadata(wheels[0])
            if metadata.get("License-Expression") != "BUSL-1.1":
                errors.append("wheel metadata must declare License-Expression: BUSL-1.1")
            license_files = set(metadata.get_all("License-File") or [])
            if REQUIRED_LICENSE_FILES - license_files:
                errors.append("wheel metadata must include LICENSE and NOTICE license files")
            project_urls = set(metadata.get_all("Project-URL") or [])
            missing_urls = REQUIRED_PROJECT_URLS - project_urls
            if missing_urls:
                errors.append(
                    "wheel metadata missing project URLs: " + ", ".join(sorted(missing_urls))
                )
            if "License :: Other/Proprietary License" in (
                metadata.get_all("Classifier") or []
            ):
                errors.append("wheel metadata must not use deprecated license classifiers")
            if "cavra/schemas/__init__.py" not in archive_names:
                errors.append("wheel must include cavra.schemas package marker")
            schema_names = {
                name for name in archive_names if name.startswith("cavra/schemas/")
            }
            if len([name for name in schema_names if name.endswith(".schema.json")]) < 7:
                errors.append("wheel must include packaged CAVRA JSON schemas")

    _cleanup_generated_paths(root)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    args = parser.parse_args()

    errors = validate(args.root)
    if errors:
        print("CAVRA Python package metadata validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CAVRA Python package metadata validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
