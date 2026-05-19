# Plugin Architecture

CAVRA exposes a public plugin runtime so Community and private Enterprise
extensions can share a stable manifest format without exposing Enterprise
source code.

## Manifest

```json
{
  "name": "sample-community-plugin",
  "version": "0.1.0",
  "edition_required": "community",
  "entrypoint": "package.module:Plugin",
  "permissions": ["policy:evaluate"],
  "description": "Plugin description"
}
```

## Community Plugins

Community plugins may live under `plugins/community` and must require
`edition_required=community`.

## Enterprise Plugins

Enterprise plugins must be delivered as private packages, private artifacts, or
private containers. They should use `edition_required=enterprise` and be loaded
only when the private Enterprise package and a valid Enterprise entitlement are
available.

## Enforcement

The public loader rejects Enterprise plugins in Community mode with:

> This feature is available in CAVRA Enterprise. See docs/enterprise/features.md for details.

The public repository must not include Enterprise plugin implementation.
