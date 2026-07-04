# OPA/Rego Policy Path

CAVRA policies remain authored as versioned YAML policy packs. The OPA/Rego policy path exports those packs into Rego modules, JSON data, OPA input fixtures, parity reports, and policy manifests without replacing the existing Python runtime engine.

## What This Adds

- YAML policy remains the source of truth.
- Generated Rego is Git-versioned and reviewable.
- OPA input fixtures are public-safe and repeatable.
- Python runtime decisions and Rego-compatible decisions are parity tested.
- Enterprise deployments can attach private CI, review, rollback, and runtime evidence without exposing private policy packs.

## Export

```bash
cavra policy rego-export \
  --policy-pack cavra-ai-agent-baseline \
  --output-dir dist/opa-rego
```

The export writes:

- `cavra_policy.rego`
- `data.json`
- `opa-input-fixtures.json`
- `rego-parity-report.json`
- `policy-version-manifest.json`

## Test Parity

```bash
cavra policy rego-test --policy-pack cavra-ai-agent-baseline
```

The parity suite covers sensitive file reads, policy writes, Terraform plan/apply, protected-branch pushes, and unknown MCP filesystem servers.

## Optional OPA CLI

```bash
opa check examples/opa-rego/generated/cavra_policy.rego
opa eval \
  --data examples/opa-rego/generated/cavra_policy.rego \
  --data examples/opa-rego/generated/data.json \
  --input examples/opa-rego/input.block-env-read.json \
  'data.cavra.policy.decision'
```

OPA is optional for public Python CI, but operators can use it in policy review workflows.

## Readiness

```bash
python3 scripts/validate_opa_rego_policy.py \
  --packet examples/opa-rego/enterprise-opa-rego-policy.live.sanitized.example.json \
  --require-live
```

The live gate passes when:

```text
ready_for_live_opa_rego_policy_path: true
blocker_count: 0
```

Enterprise deployments still provide private policy repository links, approval workflow evidence, CI run references, OPA runtime deployment evidence, and rollback evidence inside the customer evidence room.
