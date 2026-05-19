from __future__ import annotations

from pathlib import Path

from cavra.plugin_runtime.loader import read_manifest
from cavra.plugin_runtime.manifest import PluginManifest


class PluginRegistry:
    def __init__(self, root: Path) -> None:
        self.root = root

    def discover(self) -> list[PluginManifest]:
        if not self.root.exists():
            return []
        manifests = sorted(self.root.glob("**/plugin.json"))
        return [read_manifest(path) for path in manifests]

    def community_plugins(self) -> list[PluginManifest]:
        return [plugin for plugin in self.discover() if plugin.edition_required == "community"]
