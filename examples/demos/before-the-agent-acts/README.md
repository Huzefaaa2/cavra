# Before the Agent Acts

An AI coding agent is asked: "Update this payment service and deploy the infrastructure."

The simulated agent attempts to read `.env`, modify `iam/admin-role.tf`, run `terraform plan`, run `terraform apply -auto-approve`, use an unknown filesystem MCP server, push directly to `main`, and open a PR.

CAVRA decisions: block, require approval, allow, block, block, block, and allow with attestation.

Run:

```bash
cavra demo before-the-agent-acts
```

End message: Before the agent acts, CAVRA decides.
