# Security Policy

## Supported Versions

CAVRA is pre-1.0. Security fixes are applied to the current `main` branch and to the latest published release when release artifacts are available.

## Reporting a Vulnerability

Do not open a public GitHub issue for suspected vulnerabilities.

Report security issues through GitHub private vulnerability reporting when available for this repository. If private reporting is unavailable, contact the repository owner with:

- affected CAVRA version, commit, release asset, or workflow run;
- affected component, such as policy engine, evidence bundle, approval router, API, sandbox, Go runtime, MCP integration, or release package;
- reproduction steps or proof-of-concept details;
- expected impact, including secret exposure, policy bypass, evidence tampering, privilege escalation, unsafe release artifact, or availability risk;
- any logs, checksums, signatures, or provenance files needed to validate the report.

## Triage Targets

CAVRA triages reports by enterprise control impact:

- Critical: exploitable policy bypass, signature/provenance forgery, secret disclosure, or unauthenticated privileged mutation.
- High: evidence integrity failure, authorization bypass, release artifact integrity failure, or unsafe default-deny behavior regression.
- Medium: denial of service, audit metadata loss, or limited-scope policy evaluation mismatch.
- Low: hardening gaps, documentation ambiguity with security impact, or defense-in-depth improvements.

The project targets initial acknowledgement within two business days and remediation planning within seven business days for confirmed high or critical findings.

## Release Advisory Process

Security fixes should include:

- a private fix branch or maintainer-controlled pull request;
- regression tests for the failing control path;
- updated release evidence, SBOM, detached signatures, and SLSA provenance for affected release packages;
- a GitHub Security Advisory or release note that includes severity, affected versions, fixed versions, mitigation, and verification steps.

## Verifying Go Runtime Releases

For Go runtime release packages, verify checksums, release evidence, detached Ed25519 signatures, and SLSA provenance before distribution:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-v0.1.0
```

Unsigned dry-run packages are only for workflow validation:

```bash
cavra release verify-go-package go/cavra-runtime/dist/go-runtime-dry-run --allow-unsigned
```
