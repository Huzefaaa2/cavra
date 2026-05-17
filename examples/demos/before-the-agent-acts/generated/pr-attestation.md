# CAVRA PR Attestation

Before the agent acts, CAVRA decides.

Session: `demo-session`

## Summary

- Allowed actions: 2
- Blocked actions: 4
- Approval-required actions: 1

## Decisions

- `read_file` `.env` -> **block** via `filesystem.read.block`
- `write_file` `iam/admin-role.tf` -> **require_approval** via `filesystem.write.require_approval`
- `execute_command` `terraform plan` -> **allow** via `commands.allow`
- `execute_command` `terraform apply -auto-approve` -> **block** via `commands.block`
- `mcp_tool_call` `unknown-filesystem:read_file` -> **block** via `mcp.server.trust.block_unknown`
- `git_operation` `origin/main` -> **block** via `git.protected_branch.block_direct_push`
- `pull_request` `create PR` -> **allow_with_attestation** via `git.pull_request.allow_with_attestation`

## Reviewer Guidance

Review blocked and approval-required actions before merge. Attach this attestation to AI-assisted pull requests in regulated repositories.
