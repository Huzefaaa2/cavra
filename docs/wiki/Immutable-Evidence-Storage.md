# Immutable Evidence Storage

CAVRA now includes deployment references for immutable evidence archives.

## Reference Bundles

- `examples/immutable-storage/aws-s3-object-lock`: S3 Object Lock deployment and upload scripts.
- `examples/immutable-storage/azure-blob-immutability`: Azure Blob immutability deployment and upload scripts.

## How To Use

Generate and verify CAVRA evidence:

```bash
cavra evidence bundle --output .cavra/evidence/latest --signer platform-security --retention-days 2555
cavra evidence verify .cavra/evidence/latest --trust-root .cavra/keys/evidence-trust-roots.json --key-id prod-evidence --minimum-retention-days 2555
cavra evidence storage-plan .cavra/evidence/latest --output .cavra/evidence/storage --retention-days 2555
```

Deploy AWS S3 Object Lock:

```bash
cd examples/immutable-storage/aws-s3-object-lock
cp variables.example.env .env
source .env
bash deploy.sh
bash upload-evidence.sh
```

Deploy Azure Blob immutability:

```bash
cd examples/immutable-storage/azure-blob-immutability
cp variables.example.env .env
source .env
bash deploy.sh
bash upload-evidence.sh
```

## Controls

- Verify evidence before upload.
- Use session-scoped object prefixes.
- Keep upload roles separate from retention administration.
- Use AWS S3 Object Lock compliance mode only after records-management review.
- Lock Azure immutability policies only after retention requirements are approved.
- Store cloud upload output with the change record or audit request.

## User Stories

- As an auditor, I can confirm CAVRA evidence was retained in a WORM-capable store.
- As a platform engineer, I can deploy immutable storage without granting CAVRA broad cloud permissions.
- As a records manager, I can map CAVRA retention policy artifacts to cloud retention controls.

## Enterprise Value

Immutable storage references connect CAVRA's signed evidence bundles to enterprise retention controls. This helps regulated teams prove that AI-agent governance evidence was preserved after review, release, incident response, or audit.

## Next

Go daemon lifecycle management, daemon evidence hooks, and public sandbox URL validation after deployment from `main`.
