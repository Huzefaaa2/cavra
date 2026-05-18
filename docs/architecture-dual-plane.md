# CAVRA Dual-Plane Architecture

CAVRA keeps Python as the management plane and introduces Go as an optional enforcement plane only where interface parity is proven.

Management plane responsibilities: policy authoring, registry, inheritance, compliance packs, risk classification, evidence, PR attestation, webhooks, SIEM/ITSM exports, FastAPI, Claude Code adapters, MCP adapters, documentation, approval routing, and SaaS/self-hosted services.

Enforcement plane responsibilities: low-latency decisions for file, command, Git, MCP, local session daemon, CI runner enforcement, audit event streaming, air-gapped deployment, and gRPC or Unix-socket interfaces.

The current Go scaffold under `go/cavra-runtime/` mirrors a critical subset of Python decisions with shared parity fixtures. GitHub Actions runs the Go tests in a dedicated `go-runtime-parity` job, and the required governance check runs the same Go suite before generating CI evidence.

The Python runtime remains authoritative until Go loads compiled policies, passes expanded golden parity tests, exposes the local daemon interface, and ships reproducible signed binaries.
