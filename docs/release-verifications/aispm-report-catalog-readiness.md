# AISPM Report Catalog Readiness

Status: ready

This public-safe release gate verifies that the AISPM CSO Report Center keeps
Community downloadable reports, Enterprise-locked report capabilities, portal
export controls, documentation, and CI validation aligned.

## Portal Packet

The AISPM dashboard renders the CSO Report Center and can copy or download
`cavra-aispm-report-catalog-packet.json`.

## Community Downloads

| Report | Format | Filename | Audience |
| --- | --- | --- | --- |
| Executive Risk Brief | Markdown | `cavra-aispm-executive-risk-brief.md` | CSO/CISO |
| Board KPI Pack | JSON | `cavra-aispm-board-kpi-pack.json` | Leadership |
| SOC 2-Style Audit Summary | Markdown | `cavra-aispm-soc2-audit-summary.md` | Audit |
| Control Coverage Export | CSV | `cavra-aispm-control-coverage.csv` | Security Engineering |
| Evidence Freshness Export | CSV | `cavra-aispm-evidence-freshness.csv` | GRC / Audit |
| Agent Risk Register | CSV | `cavra-aispm-agent-risk-register.csv` | Platform Security |

## Enterprise-Locked Capabilities

- PDF Board Pack
- XLSX Evidence Workbook
- Scheduled Email Delivery
- Recipient Governance
- Signed JSON and GRC upload packages
- Delivery audit and retry evidence

## Validation

```bash
python scripts/validate-aispm-report-catalog-readiness.py
```

The validator checks portal DOM IDs, JavaScript packet export functions,
workflow wiring, release evidence index inclusion, README links, wiki links,
and public-safety boundaries.

## Public Safety Boundary

Community report downloads use sample or local activity metadata only. The
public catalog excludes raw prompts, model reasoning, recipient addresses, SMTP
credentials, private report content, signed download URLs, customer records,
Enterprise source code, private policy packs, and tenant telemetry.
