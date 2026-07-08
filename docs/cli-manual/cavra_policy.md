# cavra policy

## Name

`cavra policy` - generated CAVRA CLI manual page.

## Synopsis

```bash
cavra policy --help
```

## Description

This page is generated from the command's Typer help output. Use it as the authoritative option reference for this command.

## Help Output

```text
                                                                                                                                            
 Usage: python -m cavra.cli policy [OPTIONS] COMMAND [ARGS]...                                                                              
                                                                                                                                            
 Policy registry commands.                                                                                                                  
                                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ list                 List available policy packs.                                                                                        │
│ validate             Validate a policy pack against the CAVRA JSON Schema.                                                               │
│ test                 Run core CAVRA policy assertions.                                                                                   │
│ explain              Explain the policy decision for an action.                                                                          │
│ compile              Compile a policy pack and optional overlays to normalized JSON.                                                     │
│ rego-export          Export a CAVRA policy pack to a public-safe OPA/Rego compatibility bundle.                                          │
│ rego-test            Run Rego/Python parity tests for the generated policy path.                                                         │
│ rego-readiness       Validate an OPA/Rego policy readiness packet.                                                                       │
│ lifecycle-plan       Export policy lifecycle lint, version, shadow, dry-run, rollback, and approval artifacts.                           │
│ lifecycle-readiness  Validate a policy lifecycle readiness packet.                                                                       │
│ diff                 Show a semantic diff between two policies.                                                                          │
│ sign                 Create CAVRA policy signature metadata.                                                                             │
│ verify               Verify CAVRA policy signature metadata.                                                                             │
│ keygen               Generate a local Ed25519 keypair for public policy signing workflows.                                               │
│ simulate             Simulate the flagship CAVRA decision sequence.                                                                      │
│ dry-run              Run policy simulation without enforcing changes.                                                                    │
│ init                 Create a starter CAVRA policy.                                                                                      │
│ describe             Describe a policy pack.                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## See Also

- [`cavra agent`](cavra_agent.md)
- [`cavra demo`](cavra_demo.md)
- [`cavra init`](cavra_init.md)
- [`cavra integration`](cavra_integration.md)
- [`cavra evidence`](cavra_evidence.md)
- [`cavra approval`](cavra_approval.md)
- [`cavra registry`](cavra_registry.md)
- [`cavra ops`](cavra_ops.md)

## Regenerate

```bash
python3 scripts/generate_cli_reference.py --repo-root .
```
