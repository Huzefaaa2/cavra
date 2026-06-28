# Community Release Note Freshness

CAVRA validates public Community release notes so release documentation cannot
drift from verification evidence, README links, or wiki navigation.

## What Is Checked

`scripts/validate-community-release-note-freshness.py` scans
`docs/releases/community-v*.md` and verifies each release notes page has:

- a GitHub Release URL for the matching `community-v*` tag;
- at least one matching verification packet under `docs/release-verifications/`;
- a README link to the release notes page;
- a README link to the matching verification packet;
- a wiki release notes page linked from `docs/wiki/Home.md`;
- a wiki verification page linked from `docs/wiki/Home.md`.

## Command

```bash
python3 scripts/validate-community-release-note-freshness.py
```

## Next Recommendation

Implement Community v1.0.0 release-candidate hardening packet from the completed Node 24 readiness baseline with signed artifacts, reproducible provenance verification, GA announcement checklist, and final operator evidence.
