from __future__ import annotations

from pathlib import Path


def test_community_container_copies_policy_pack_directories() -> None:
    dockerfile = Path("docker/Dockerfile.community").read_text(encoding="utf-8")

    assert "COPY policies ./policies" in dockerfile
    assert "COPY policies/community ./policies/community" not in dockerfile


def test_azure_api_container_copies_policy_pack_directories() -> None:
    dockerfile = Path("docker/Dockerfile.azure-api").read_text(encoding="utf-8")

    assert "COPY policies ./policies" in dockerfile
    assert "COPY policies/community ./policies/community" not in dockerfile
