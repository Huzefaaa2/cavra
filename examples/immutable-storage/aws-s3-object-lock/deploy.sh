#!/usr/bin/env bash
set -euo pipefail

: "${CAVRA_AWS_BUCKET:?Set CAVRA_AWS_BUCKET to the evidence bucket name.}"
: "${CAVRA_AWS_KMS_KEY_ID:?Set CAVRA_AWS_KMS_KEY_ID to the KMS key used for evidence encryption.}"

AWS_REGION="${AWS_REGION:-us-east-1}"
CAVRA_RETENTION_DAYS="${CAVRA_RETENTION_DAYS:-2555}"
CAVRA_RETENTION_MODE="${CAVRA_RETENTION_MODE:-COMPLIANCE}"

if aws s3api head-bucket --bucket "$CAVRA_AWS_BUCKET" 2>/dev/null; then
  echo "Bucket exists: $CAVRA_AWS_BUCKET"
else
  if [ "$AWS_REGION" = "us-east-1" ]; then
    aws s3api create-bucket \
      --bucket "$CAVRA_AWS_BUCKET" \
      --object-lock-enabled-for-bucket \
      --region "$AWS_REGION"
  else
    aws s3api create-bucket \
      --bucket "$CAVRA_AWS_BUCKET" \
      --object-lock-enabled-for-bucket \
      --region "$AWS_REGION" \
      --create-bucket-configuration "LocationConstraint=$AWS_REGION"
  fi
fi

aws s3api put-bucket-versioning \
  --bucket "$CAVRA_AWS_BUCKET" \
  --versioning-configuration Status=Enabled

aws s3api put-public-access-block \
  --bucket "$CAVRA_AWS_BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

aws s3api put-bucket-encryption \
  --bucket "$CAVRA_AWS_BUCKET" \
  --server-side-encryption-configuration "{
    \"Rules\": [{
      \"ApplyServerSideEncryptionByDefault\": {
        \"SSEAlgorithm\": \"aws:kms\",
        \"KMSMasterKeyID\": \"${CAVRA_AWS_KMS_KEY_ID}\"
      },
      \"BucketKeyEnabled\": true
    }]
  }"

aws s3api put-object-lock-configuration \
  --bucket "$CAVRA_AWS_BUCKET" \
  --object-lock-configuration "{
    \"ObjectLockEnabled\": \"Enabled\",
    \"Rule\": {
      \"DefaultRetention\": {
        \"Mode\": \"${CAVRA_RETENTION_MODE}\",
        \"Days\": ${CAVRA_RETENTION_DAYS}
      }
    }
  }"

policy_file="$(mktemp)"
cat > "$policy_file" <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::${CAVRA_AWS_BUCKET}",
        "arn:aws:s3:::${CAVRA_AWS_BUCKET}/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
POLICY

aws s3api put-bucket-policy --bucket "$CAVRA_AWS_BUCKET" --policy "file://$policy_file"
rm -f "$policy_file"

echo "CAVRA immutable evidence bucket configured: s3://${CAVRA_AWS_BUCKET}"
