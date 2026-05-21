# High-Risk Command And Cloud/IaC Parity

CAVRA now includes shared Python and Go parity coverage for the high-risk command and cloud/IaC decisions that enterprises expect to be enforced consistently before a Go enforcement plane is promoted beyond a scaffold.

## Covered Decisions

The shared fixture `go/cavra-runtime/testdata/parity_cases.json` now proves parity for:

- Cloud IAM mutation blocking through `cavra-cloud-iam`.
- Cloud IAM read-only inspection allowance through `cavra-cloud-iam`.
- Kubernetes production apply/delete blocking through `cavra-kubernetes-prod`.
- Kubernetes read-only diff/get/describe allowance through `cavra-kubernetes-prod`.
- Terraform and OpenTofu destructive operation blocking through `cavra-terraform-prod`.
- Terraform and OpenTofu plan/read-only operation allowance through `cavra-terraform-prod`.
- GitHub force-push and admin-merge blocking through `cavra-github-enterprise`.
- OWASP LLM agentic command-injection patterns such as `curl | sh` blocking through `cavra-owasp-llm-agentic`.
- Transparent delivery agent repository-setting mutation blocking through `cavra-agentic-delivery`.
- Transparent delivery agent test command allowance through `cavra-agentic-delivery`.

## Implementation

The Go runtime built-in policy subset now mirrors the public-safe high-risk command portions of these bundled policy packs:

- `cavra-cloud-iam`
- `cavra-kubernetes-prod`
- `cavra-terraform-prod`
- `cavra-github-enterprise`
- `cavra-owasp-llm-agentic`
- `cavra-agentic-delivery`

Python remains authoritative. The Go runtime only gains parity where the shared fixture and tests prove the same decision, rule ID, severity, approver group, and evidence metadata behavior.

## Verification

Run the Python fixture verification:

```bash
python3 -m pytest tests/test_go_runtime_parity.py -q
```

Run the Go runtime tests:

```bash
cd go/cavra-runtime
go test ./...
```

Run one high-risk decision through Go:

```bash
echo '{"action_type":"execute_command","target":"aws iam attach-role-policy --role-name prod-admin --policy-arn arn:aws:iam::aws:policy/AdministratorAccess","policy_pack":"cavra-cloud-iam"}' \
  | go run ./cmd/cavra-runtime
```

Expected result:

```json
{
  "decision": "block",
  "rule_id": "commands.block",
  "severity": "high"
}
```

## User Stories

- As a platform engineer, I can trust the Go runtime to block the same high-risk cloud IAM mutations that Python blocks.
- As a Kubernetes owner, I can prove production apply/delete commands are not allowed through a second enforcement backend without parity evidence.
- As an IaC owner, I can verify Terraform and OpenTofu destructive operations are consistently blocked while plan/read-only commands remain usable.
- As a security reviewer, I can verify force-push, admin merge, and command-injection protections before enabling Go in CI runners.

## Enterprise Challenge Solved

Enterprises cannot adopt a low-latency enforcement runtime if it behaves differently from the authoritative policy plane. This parity slice turns high-risk cloud, Kubernetes, IaC, GitHub, and command-injection cases into shared test evidence, reducing the risk of inconsistent enforcement during rollout.

## Next Work

The next recommended implementation step is an explicitly opt-in Go enforcement backend pilot with audited fallback to Python, deployment readiness checks, and parity-gate evidence before any production use.
