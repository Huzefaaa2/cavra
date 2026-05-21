# Immutable Evidence Storage

CAVRA evidence bundles can be archived in immutable object stores after local verification. This release adds deployment references for AWS S3 Object Lock and Azure Blob Storage immutability.

## Reference Bundles

- `examples/immutable-storage/aws-s3-object-lock`: S3 Object Lock bucket with versioning, KMS encryption, public-access blocking, TLS-only policy, default retention, and evidence upload script.
- `examples/immutable-storage/azure-blob-immutability`: Azure Blob Storage account and container with versioning, HTTPS-only access, public-access blocking, locked container immutability policy, optional legal hold tags, and evidence upload script.

Both references are designed as operator-owned deployment bundles. CAVRA produces evidence, retention policies, checksums, signatures, and storage plans; cloud operators own account permissions, key management, retention approval, and production lock decisions.

## Evidence Flow

1. Generate and sign a bundle.
2. Verify bundle checksums and signatures against the approved trust root.
3. Verify the bundle retention policy meets the enterprise minimum.
4. Export the immutable storage plan.
5. Upload the verified bundle into a session-scoped immutable prefix.
6. Store cloud upload evidence with the change record or audit request.

```bash
cavra evidence bundle \
  --output .cavra/evidence/latest \
  --signer platform-security \
  --private-key .cavra/keys/evidence-private.pem \
  --retention-days 2555

cavra evidence verify .cavra/evidence/latest \
  --trust-root .cavra/keys/evidence-trust-roots.json \
  --key-id prod-evidence \
  --minimum-retention-days 2555

cavra evidence storage-plan .cavra/evidence/latest \
  --output .cavra/evidence/storage \
  --retention-days 2555
```

## AWS S3 Object Lock

Use the AWS reference when your enterprise standardizes audit evidence in S3.

```bash
cd examples/immutable-storage/aws-s3-object-lock
cp variables.example.env .env
source .env
bash deploy.sh
bash upload-evidence.sh
```

Production controls:

- Create a new Object Lock-enabled bucket for CAVRA evidence.
- Use `COMPLIANCE` mode only after records-management review.
- Require KMS encryption and restrict key administration.
- Deny non-TLS access.
- Keep CAVRA runtime roles separate from retention-administration roles.
- Upload evidence only after `cavra evidence verify` succeeds.

## Azure Blob Immutability

Use the Azure reference when your enterprise standardizes audit evidence in Azure Storage.

```bash
cd examples/immutable-storage/azure-blob-immutability
cp variables.example.env .env
source .env
bash deploy.sh
bash upload-evidence.sh
```

Production controls:

- Use a dedicated storage account and container for CAVRA evidence.
- Enable blob versioning before locking the retention policy.
- Lock the immutability policy only after legal and records review.
- Use optional legal hold tags for active investigations.
- Keep upload roles separate from storage-account owner roles.
- Upload evidence only after `cavra evidence verify` succeeds.

## User Stories

- As an auditor, I can confirm CAVRA evidence was retained in a WORM-capable store.
- As a platform engineer, I can deploy cloud-native immutable evidence storage without giving CAVRA broad cloud permissions.
- As a records manager, I can map CAVRA retention policy artifacts to storage-level retention controls.
- As a security engineer, I can separate evidence upload permissions from retention bypass or storage-administration permissions.

## Enterprise Challenge Solved

AI-agent governance evidence must remain trustworthy after a release, incident, or audit request. Immutable evidence storage references close the gap between CAVRA's signed bundle artifacts and enterprise WORM storage controls, making evidence retention operationally repeatable across AWS and Azure.

## Next Work

The next recommended work is contract-level Go fixtures and production release-signing key rotation documentation.
