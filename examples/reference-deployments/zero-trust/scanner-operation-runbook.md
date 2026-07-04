# CAVRA Zero-Trust Scanner Operation Runbook

This runbook keeps the scanner customer-side and metadata-only. It is for
private VPCs, private subnets, Kubernetes clusters, on-premises servers, and
air-gapped estates.

## Boundary

- Run scanner jobs inside the customer-controlled network.
- Export only metadata-only results: asset references, hashes, risk scores,
  findings, and evidence references.
- No raw model weights, no raw model bytes, no training data, no prompt samples,
  no source code, and no credentials leave the boundary.
- Store signed evidence in the customer evidence location before forwarding
  references to CAVRA.

## Customer-Side Steps

1. Set `CAVRA_SCANNER_MODE=metadata_only`.
2. Set `CAVRA_FAIL_CLOSED=true`.
3. Set `CAVRA_TENANT_ID` and `CAVRA_WORKSPACE_ID`.
4. Run the scanner against the local model, artifact, package, or registry
   metadata source.
5. Validate the result with `scripts/validate_zero_trust_scanner.py`.
6. Attach evidence references to the readiness packet, not raw assets.

## Closeout Evidence

Capture these references for production use:

- scanner deployment commit or image digest;
- firewall, private endpoint, or routing proof;
- negative raw-egress test result;
- signed scan result;
- incident drill or revocation drill evidence;
- tenant/workspace ownership record.
