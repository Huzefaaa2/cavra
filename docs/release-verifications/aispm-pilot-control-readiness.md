# AISPM Pilot Control Readiness

This release verification records the public-safe production-pilot control
readiness gate for CAVRA AISPM. It packages the next five controls required
before a CSO/CISO can move from trial evidence to a controlled production
pilot.

| Control area | Source artifact | Status |
| --- | --- | --- |
| Pilot Exception Register | `cavra-aispm-pilot-exception-register-packet.json` | Ready |
| Pilot Risk Acceptance Summary | `cavra-aispm-pilot-risk-acceptance-packet.json` | Ready |
| Pilot Launch Board Pack | `cavra-aispm-pilot-launch-board-pack-packet.json` | Ready |
| Launch Board Pack Artifact Index | `docs/release-verifications/aispm-launch-board-pack-artifact-index.json` | Ready |
| AISPM Launch Readiness Rollup | `docs/release-verifications/aispm-launch-readiness-rollup.json` | Ready |

The Community portal exposes this as
`cavra-aispm-pilot-control-readiness-packet.json` from the AISPM dashboard.
The packet is intended for launch review, security review, procurement review,
and auditor-facing evidence preparation.

## Enterprise Boundaries

The Community packet does not implement signed approvals, named approver
identity records, board minutes, PDF board-pack delivery, tenant artifact
retention, or workflow write-back. Those capabilities require CAVRA Enterprise
or the future CAVRA SaaS control plane.

## Validation

Run:

```bash
python scripts/validate-aispm-pilot-control-readiness.py
```

The validator confirms portal IDs, packet exports, command palette entries,
release evidence index linkage, launch readiness linkage, workflow hooks, docs,
wiki mirrors, and public-safety exclusions.
