from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

from cavra.edition.community import ENTERPRISE_MESSAGE
from cavra.plugin_runtime.manifest import PluginManifest


class PluginLoadError(ValueError):
    pass


def read_manifest(path: Path) -> PluginManifest:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise PluginLoadError("plugin manifest must be a JSON object")
    return PluginManifest.from_dict(payload)


def load_plugin(manifest: PluginManifest, *, edition: str = "community") -> Any:
    if manifest.edition_required != "community" and edition == "community":
        raise PluginLoadError(ENTERPRISE_MESSAGE)
    module_name, _, attribute = manifest.entrypoint.partition(":")
    if not module_name or not attribute:
        raise PluginLoadError("plugin entrypoint must use module:attribute format")
    module = importlib.import_module(module_name)
    try:
        return getattr(module, attribute)
    except AttributeError as exc:
        raise PluginLoadError(f"plugin entrypoint not found: {manifest.entrypoint}") from exc
