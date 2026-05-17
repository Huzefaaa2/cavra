# CAVRA Architecture

## Layers

1. Core policy and audit model
   - policy registry
   - runtime rule evaluation
   - audit evidence generation
2. Agent runtime wrapper
   - session lifecycle
   - command/file/git/MCP guards
   - agent identity and environment metadata
3. Integrations
   - CLI
   - webhook/API clients
   - GitHub PR attestation
   - SIEM / GRC evidence exports

## Components

- `cavra.cli`
- `cavra.agent`
- `cavra.runtime`
- `cavra.audit`
- `cavra.policy_registry`

## Policy packs

Policy packs are stored under `policies/` and define sensitive path rules, blocked commands, and governance behaviour.

## Audit

Each AI session produces a JSON audit bundle and optional markdown attestation for PR workflows.
