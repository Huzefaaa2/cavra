# OPA/Rego Policy Path

CAVRA policies remain authored as versioned YAML policy packs. R5.1 adds a public OPA/Rego compatibility path so teams can export those packs into Rego modules, JSON data, OPA input fixtures, parity reports, and policy manifests without replacing the existing Python runtime engine.

The design goal is portability:

- CAVRA YAML stays the source of truth.
- Generated Rego is Git-versioned and reviewable.
- OPA input fixtures are public-safe and repeatable.
- Python runtime decisions and Rego-compatible decisions are parity tested.
- Live Enterprise deployments can attach private CI, review, and rollback evidence without exposing private policy packs.

## Export A Rego Bundle

Use the CLI:

```bash
cavra policy rego-export \
  --policy-pack cavra-ai-agent-baseline \
  --output-dir dist/opa-rego
```

Use the validator script:

```bash
python3 scripts/validate_opa_rego_policy.py \
  --policy-pack cavra-ai-agent-baseline \
  --export-dir dist/opa-rego \
  --output dist/opa-rego-export.json
```

The export writes:

- `cavra_policy.rego`
- `data.json`
- `opa-input-fixtures.json`
- `rego-parity-report.json`
- `policy-version-manifest.json`

Checked-in examples live under `examples/opa-rego/generated/`.

## Run Parity Tests

```bash
cavra policy rego-test --policy-pack cavra-ai-agent-baseline
```

Or:

```bash
python3 scripts/validate_opa_rego_policy.py \
  --policy-pack cavra-ai-agent-baseline \
  --parity \
  --output dist/opa-rego-parity.json
```

The public parity suite covers:

- blocking `.env` reads;
- requiring approval for policy writes;
- allowing `terraform plan`;
- blocking `terraform apply`;
- blocking protected-branch pushes;
- blocking unknown MCP filesystem servers.

## Optional OPA CLI Check

OPA is optional for the public Python test path. If the OPA CLI is installed, validate the generated Rego directly:

```bash
opa check examples/opa-rego/generated/cavra_policy.rego
opa eval \
  --data examples/opa-rego/generated/cavra_policy.rego \
  --data examples/opa-rego/generated/data.json \
  --input examples/opa-rego/input.block-env-read.json \
  'data.cavra.policy.decision'
```

## Review Workflow

Treat generated Rego as a derived artifact:

1. Edit the source policy YAML.
2. Run `cavra policy validate`.
3. Run `cavra policy rego-export`.
4. Run `cavra policy rego-test`.
5. Review the generated Rego diff, data diff, input fixture diff, and parity report.
6. Attach the parity report or readiness packet to the policy PR.

## Rollback

Rollback should restore the previous source YAML policy and the matching generated Rego bundle. Do not roll back only the generated Rego file, because CAVRA treats YAML policy packs as the source of truth.

## Readiness Packet

Validate sample readiness:

```bash
python3 scripts/validate_opa_rego_policy.py \
  --packet examples/opa-rego/enterprise-opa-rego-policy.sample.json
```

Validate a live sanitized packet:

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

Private Enterprise deployments still supply customer-specific policy repository links, approval workflow evidence, CI run references, OPA runtime deployment evidence, and rollback evidence inside the customer's evidence room.
