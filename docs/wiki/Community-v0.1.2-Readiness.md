# Community v0.1.2 Readiness

This readiness note closes the public Community v0.1.2 preparation item for
Python package metadata and release workflow guard evidence.

## Packaging Metadata Closure

Community package metadata is now owned by `pyproject.toml`. `setup.py` remains
as a legacy setuptools shim only, which prevents duplicate metadata from
overriding the PEP 621 project table.

Resolved build warnings:

- ignored `project_urls` metadata from `setup.py`;
- deprecated TOML table form for `project.license`;
- duplicate `install_requires` and `extras_require` metadata;
- deprecated license classifier usage;
- empty `.github/*.yaml` manifest pattern;
- data-only `cavra.schemas` package warning.

Validation command:

```bash
python3 scripts/validate-python-package-metadata.py
```

Required evidence:

- `python -m build` completes without setuptools metadata warning markers;
- `python -m twine check` passes for the built wheel and source distribution;
- wheel metadata declares `License-Expression: BUSL-1.1`;
- wheel metadata includes `LICENSE` and `NOTICE`;
- project URLs are present in the wheel metadata;
- packaged CAVRA JSON schemas are included in the wheel.

## Release Workflow Guard Evidence

Community release workflows now include explicit guard evidence for public-safe
release automation:

- `.github/workflows/publish-pypi.yml` runs automatically only for release tags
  that start with `pypi-v`, or manually through `workflow_dispatch`;
- `.github/workflows/go-release.yml` runs automatically only for release tags
  that start with `go-runtime-v`, or manually through `workflow_dispatch`;
- `.github/workflows/community-ci.yml` runs package metadata validation for PRs
  and pushes to `main`;
- `.github/workflows/release-community.yml` runs package metadata validation
  before building Community artifacts.

## Boundary Notice

This readiness evidence covers public Community packaging metadata and workflow
guards only. It does not include Enterprise source code, private release
artifacts, paid policy packs, private registry credentials, signing keys,
license-service internals, SaaS backend code, or customer records.

## Next Recommendation

Start Community v1.0.0 stabilization planning from the completed Node 24 readiness baseline with release signing, reproducible provenance, GA announcement readiness, and final operator evidence.
