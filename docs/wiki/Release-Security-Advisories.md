# Release Security Advisories

Security-relevant CAVRA releases must be traceable from source commit to release package, advisory, and verification command.

## Advisory Content

Every security advisory or security-impacting release note should include:

- advisory ID or release tag;
- severity and affected components;
- affected versions and fixed versions;
- customer impact and exploitation prerequisites;
- mitigation before upgrade;
- fixed commit, pull request, and release asset links;
- verification steps, including `cavra release verify-go-package`;
- release-candidate upgrade validation with `cavra release validate-upgrade`;
- release channel review with `cavra release channel-manifest`;
- managed workstation updater policy review with `cavra release updater-policy`;
- installer smoke validation with `cavra release smoke-installers`;
- rollout evidence capture with `cavra release capture-rollout`;
- rollout evidence verification and indexing with `cavra release verify-rollout`;
- signed rollout promotion approval requests with `cavra release request-rollout-promotion`;
- approved promotion execution records with `cavra release execute-rollout-promotion`;
- promotion execution search and audit drill-downs through `/promotion-executions`;
- approved rollback execution records with `cavra release execute-rollout-rollback`;
- SIEM and ITSM promotion audit exports with `cavra release export-promotion-audit`;
- connector delivery for promotion audit and rollback execution records with `cavra release deliver-promotion-audit` and `cavra release deliver-rollback-execution`;
- persisted connector delivery history and dashboard alerts with `cavra release connector-delivery-history` and `cavra release connector-delivery-dashboard`;
- rollout evidence search filters and governed rollout artifact downloads through `cavra evidence search` and the `/evidence` API;
- SBOM, installer metadata, managed endpoint deployment manifest, release channel manifest, updater policy, checksum, detached signature, GitHub keyless attestation, and SLSA provenance references.

## Go Runtime Release Gate

Before publishing a Go runtime package:

1. Build release binaries through `.github/workflows/go-release.yml`.
2. Require `CAVRA_GO_RELEASE_SIGNING_KEY` for production releases.
3. Confirm the package contains:
   - `checksums.txt`;
   - `cavra-runtime.endpoint-deployment.json`;
   - `cavra-runtime.installers.json`;
   - `cavra-runtime.sbom.spdx.json`;
   - `cavra-runtime.provenance.intoto.json`;
   - detached `*.sig.json` files;
   - `github-keyless-attestation.json`;
   - `offline-trust-root-bootstrap.json`;
   - `release-evidence.json`;
   - `release-evidence.md`.
4. Verify locally:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-<version>
```

5. Verify the air-gapped zip:

```bash
cavra release verify-airgap-bundle go/cavra-runtime/dist/cavra-go-runtime-<version>.zip
```

6. Verify the GitHub keyless attestation:

```bash
gh attestation verify go/cavra-runtime/dist/cavra-go-runtime-<version>.zip \
  --repo Huzefaaa2/cavra
```

7. Validate the candidate against the previously approved package:

```bash
cavra release validate-upgrade \
  go/cavra-runtime/dist/go-runtime-<previous-version> \
  go/cavra-runtime/dist/go-runtime-<candidate-version>
```

8. Inspect managed endpoint deployment guidance for approved runner and workstation channels:

```bash
jq '.deployment_targets[] | {id, surface, platform, installer_target}' \
  go/cavra-runtime/dist/go-runtime-<version>/cavra-runtime.endpoint-deployment.json
```

9. Smoke-test installer metadata and the native packaged runtime:

```bash
cavra release smoke-installers go/cavra-runtime/dist/go-runtime-<version>
```

10. Capture managed endpoint rollout evidence for the approved channel:

```bash
cavra release capture-rollout \
  go/cavra-runtime/dist/go-runtime-<version> \
  --deployment-id github-actions-linux-amd64-runner \
  --change-record CHG-123
```

11. Verify and index rollout evidence:

```bash
cavra release verify-rollout \
  .cavra/release/rollout \
  --metadata-json .cavra/evidence/metadata.json \
  --sqlite .cavra/evidence/metadata.db
```

12. Search the indexed rollout evidence:

```bash
cavra evidence search \
  --sqlite .cavra/evidence/metadata.db \
  --metadata-kind managed-endpoint-rollout \
  --rollout-status staged
```

13. Attach `cavra-go-runtime-<version>.zip` and `github-keyless-attestation.json` to the GitHub Release.
14. Link the release asset, keyless attestation, installer metadata, endpoint deployment manifest, rollout evidence, installer smoke result, offline bootstrap manifest, upgrade validation result, and provenance statement from the advisory.

## User Stories

- As a security engineer, I can connect an advisory to a signed release asset, keyless GitHub attestation, and provenance statement.
- As a platform owner, I can block runtime rollout until verification succeeds.
- As an enterprise architect, I can verify an air-gapped runtime bundle before restricted-network transfer.
- As a release manager, I can reject rollback versions or missing runtime targets before promoting a release candidate.
- As an endpoint engineering owner, I can approve signed install paths and platform targets before managed rollout.
- As an endpoint engineering owner, I can verify approved CI runner and developer workstation deployment channels before rollout.
- As an endpoint engineering owner, I can capture rollout status, selected target, rollback plan, and change-record evidence before endpoint promotion.
- As an endpoint engineering owner, I can verify and index rollout evidence for audit retrieval.
- As an endpoint engineering owner, I can search rollout evidence by deployment target, environment, and status during release review.
- As a release engineer, I can smoke-test the packaged runtime selected by installer metadata before release publication.
- As an auditor, I can prove that security releases follow the same evidence path as normal releases.

## Enterprise Challenge Solved

Enterprises need vulnerability response and release integrity in the same operating model. CAVRA advisories tie security fixes to signed, keyless-attested, provenance-backed artifacts, signed installer metadata, managed endpoint deployment manifests, release channel manifests, managed workstation updater policy, rollout evidence capture, rollout evidence verification and indexing, rollout evidence search filters, governed rollout artifact downloads, rollout artifact integrity status, promotion readiness indicators, signed promotion approval requests, approved promotion execution records, promotion execution search and audit drill-downs, rollback evidence links, approved rollback execution records, SIEM/ITSM promotion audit exports, connector delivery for promotion audit and rollback execution records, persisted delivery history, alerting dashboards, console/API views, installer smoke validation, and release-candidate upgrade checks so regulated teams can approve upgrades with less manual evidence collection.
