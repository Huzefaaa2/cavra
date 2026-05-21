# Opt-In Go Backend Pilot

CAVRA now includes an explicitly opt-in Go enforcement backend pilot. Python remains the authoritative runtime. The Go backend is used only when an operator enables it and the pilot can prove readiness.

## Safety Model

The pilot is intentionally conservative:

- Default mode is `disabled`.
- `shadow` mode runs Python first, attempts Go, compares decision parity, and keeps Python as the effective decision.
- `enforce` mode selects Go only when Go succeeds and matches Python on `decision`, `rule_id`, and `severity`.
- `promoted` mode selects Go only after runtime readiness, deployment readiness, approved audited parity evidence, and approved rollback controls all pass.
- Any Go runtime error, timeout, missing binary, missing compiled policy, or parity mismatch falls back to Python.
- Readiness is surfaced through the CLI and `/deployment/production-readiness`.

## Environment Variables

```bash
export CAVRA_GO_BACKEND_MODE=shadow
export CAVRA_GO_RUNTIME_PATH=/opt/cavra/bin/cavra-runtime
export CAVRA_GO_RUNTIME_POLICY=/etc/cavra/compiled-policy.json
export CAVRA_GO_RUNTIME_REGISTRY=/etc/cavra/mcp-registry.json
export CAVRA_GO_PROMOTION_EVIDENCE=/etc/cavra/go-backend-promotion-evidence.json
export CAVRA_GO_ROLLBACK_PLAN=/etc/cavra/go-backend-rollback-plan.json
export CAVRA_GO_RUNTIME_TIMEOUT_SECONDS=5
```

Supported modes:

- `disabled`: default; Python only.
- `shadow`: run Go for comparison and evidence, use Python decision.
- `enforce`: use Go only when parity matches; otherwise fall back to Python.
- `promoted`: use Go as the optional backend only when runtime, deployment, promotion, and rollback readiness pass.

## CLI Usage

Check readiness:

```bash
cavra runtime go-pilot-readiness \
  --mode shadow \
  --runtime-path /opt/cavra/bin/cavra-runtime \
  --policy-path /etc/cavra/compiled-policy.json \
  --json
```

Evaluate with the pilot:

```bash
cavra runtime go-pilot-evaluate execute_command "terraform plan" \
  --mode shadow \
  --runtime-path /opt/cavra/bin/cavra-runtime \
  --policy-path /etc/cavra/compiled-policy.json \
  --json
```

Compile a policy file for the Go runtime:

```bash
cavra policy compile --policy-pack cavra-ai-agent-baseline > /etc/cavra/compiled-policy.json
```

## API Usage

Readiness:

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/readiness
```

Promotion readiness:

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/promotion-readiness
```

Rollback readiness:

```bash
curl http://127.0.0.1:8000/runtime/go-pilot/rollback-readiness
```

Evaluation:

```bash
curl -X POST http://127.0.0.1:8000/runtime/go-pilot/evaluate \
  -H 'content-type: application/json' \
  -d '{"action_type":"execute_command","target":"terraform plan","policy_pack":"cavra-ai-agent-baseline"}'
```

Production readiness now includes `go_backend_pilot`, `go_backend_deployment`, `go_backend_promotion`, and `go_backend_rollback` sections. A disabled pilot is acceptable. An enabled pilot must have a runtime binary, compiled policy file, optional registry file if configured, Python fallback, and parity gate.

Deployment readiness is reported separately under `go_backend_deployment`. It validates CI runner bundle metadata, workstation channel manifests, and updater policy before a Go pilot is promoted into runner or workstation rollout paths.

Promotion readiness is reported separately under `go_backend_promotion`. It validates runtime readiness, deployment readiness, and a public-safe evidence file using schema `cavra.go-backend-promotion-evidence.v1`.

Rollback readiness is reported separately under `go_backend_rollback`. It validates an approved public-safe rollback plan using schema `cavra.go-backend-rollback-plan.v1`.

## User Stories

- As a platform owner, I can test the Go backend in shadow mode without changing the effective policy decision.
- As a security reviewer, I can prove Go is not selected when it diverges from Python.
- As a CI owner, I can pilot Go only after attaching readiness evidence to deployment records.
- As a release owner, I can require approved parity evidence before `promoted` mode selects Go.
- As an incident commander, I can require approved rollback controls before `promoted` mode selects Go.
- As an auditor, I can see fallback reason, selected backend, Python decision, Go decision, and parity result for each pilot evaluation.

## Enterprise Challenge Solved

Fast local enforcement is useful only if it cannot silently drift from the authoritative policy plane. This pilot gives enterprises a measured path from Python-only enforcement to Go-assisted enforcement with explicit opt-in, deployment readiness, promotion evidence, rollback controls, parity gates, and audited fallback.

## Next Work

The next recommended implementation step is to add automated rollback rehearsal evidence and dashboards for promoted Go backend pilots.
