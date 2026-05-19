from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    edition_required: str
    entrypoint: str
    permissions: tuple[str, ...] = field(default_factory=tuple)
    description: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PluginManifest":
        return cls(
            name=str(payload["name"]),
            version=str(payload["version"]),
            edition_required=str(payload.get("edition_required", "community")).lower(),
            entrypoint=str(payload["entrypoint"]),
            permissions=tuple(str(item) for item in payload.get("permissions", [])),
            description=str(payload.get("description", "")),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "version": self.version,
            "edition_required": self.edition_required,
            "entrypoint": self.entrypoint,
            "permissions": list(self.permissions),
            "description": self.description,
        }
