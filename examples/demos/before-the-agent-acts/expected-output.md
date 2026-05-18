# Expected Output

- Read `.env` -> BLOCK
- Modify `iam/admin-role.tf` -> REQUIRE_APPROVAL
- Run `terraform plan` -> ALLOW
- Run `terraform apply -auto-approve` -> BLOCK
- Unknown MCP filesystem server -> BLOCK
- Push to `main` -> BLOCK
- Open PR -> ALLOW WITH ATTESTATION
