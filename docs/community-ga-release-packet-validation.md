# Community GA Release Packet Validation

CAVRA validates public Community GA release packet JSON artifacts before merge
and before Community release publication.

## What Is Validated

`scripts/validate-release-packets.py` validates:

- packet JSON syntax;
- conformance to `docs/release-packets/community-ga-release-packet.schema.json`;
- the complete Community GA gate set;
- public-boundary flags when boundary validation passes;
- no accepted risks on `ready_for_community_ga` packets.

The validator covers packet JSON files in:

- `docs/release-packets/community-ga-*.json`
- `examples/release-packets/community-ga-*.json`

It excludes the packet schema file itself.

## CI Coverage

The validator runs in:

- Community CI;
- Community security scan;
- `cavra-required-check`;
- Community release workflow.

## Local Usage

```bash
python scripts/validate-release-packets.py
```

Use `--root` for a checkout or generated packet directory:

```bash
python scripts/validate-release-packets.py --root /path/to/cavra
```

## Next Recommendation

Continue with a final tagged Community GA release packet when the maintainer is
ready to publish an official Community GA release.
