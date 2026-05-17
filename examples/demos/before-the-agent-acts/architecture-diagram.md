# Architecture Diagram

```mermaid
flowchart LR
  A[Simulated AI Agent] --> B[CAVRA Runtime Guard]
  B --> C[Policy Registry]
  B --> D[Decision Stream]
  D --> E[Evidence JSON]
  D --> F[PR Attestation]
  D --> G[Compliance Mapping]
```
