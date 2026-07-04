from __future__ import annotations

from typing import Any


COMPLIANCE_PACK_SCHEMA = "cavra.compliance.pack.v1"
COMPLIANCE_PACK_READINESS_SCHEMA = "cavra.compliance.mapping-packs.readiness.v1"
COMPLIANCE_PACK_EVIDENCE_SCHEMA = "cavra.compliance.mapping-packs.evidence.v1"
COMPLIANCE_MAPPING_REPORT_SCHEMA = "cavra.compliance.mapping-report.v1"

REQUIRED_FRAMEWORKS = {
    "nist_ai_rmf",
    "iso_iec_42001",
    "owasp_llm_genai",
    "nist_ssdf",
    "eu_ai_act",
}
REQUIRED_REPORT_FORMATS = {"json", "markdown", "csv", "aispm_report"}
SUPPORTED_UNMAPPED_POLICIES = {"manual_review", "blocker"}


def build_compliance_pack_registry() -> dict[str, Any]:
    packs = [_pack_nist_ai_rmf(), _pack_iso_iec_42001(), _pack_owasp_llm_genai(), _pack_nist_ssdf(), _pack_eu_ai_act()]
    return {
        "schema_version": "cavra.compliance.pack-registry.v1",
        "product": "CAVRA",
        "purpose": "Clause-level mapping packs for AI-agent runtime evidence, AISPM findings, and auditor reports.",
        "required_frameworks": sorted(REQUIRED_FRAMEWORKS),
        "packs": packs,
        "clause_count": sum(len(pack["clauses"]) for pack in packs),
        "mapping_inputs": [
            "finding.tags",
            "finding.category",
            "finding.finding_type",
            "finding.control_family",
            "finding.surface",
        ],
    }


def validate_compliance_pack(pack: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_pack_schema(pack, checks)
    _check_pack_identity(pack, checks)
    _check_pack_clauses(pack, checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.compliance.pack-validation.v1",
        "framework_id": pack.get("framework_id", "unknown"),
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "checks": checks,
    }


def build_compliance_mapping_report(
    findings: list[dict[str, Any]],
    *,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    registry = registry or build_compliance_pack_registry()
    mappings = [map_finding_to_clauses(finding, registry=registry) for finding in findings]
    mapped = [mapping for mapping in mappings if mapping["matched_clause_count"] > 0]
    unmapped = [mapping for mapping in mappings if mapping["matched_clause_count"] == 0]
    framework_counts: dict[str, int] = {framework: 0 for framework in REQUIRED_FRAMEWORKS}
    for mapping in mappings:
        for clause in mapping["matched_clauses"]:
            framework_counts[clause["framework_id"]] = framework_counts.get(clause["framework_id"], 0) + 1
    return {
        "schema_version": COMPLIANCE_MAPPING_REPORT_SCHEMA,
        "product": "CAVRA",
        "finding_count": len(findings),
        "mapped_finding_count": len(mapped),
        "unmapped_finding_count": len(unmapped),
        "framework_match_counts": dict(sorted(framework_counts.items())),
        "mappings": mappings,
    }


def map_finding_to_clauses(
    finding: dict[str, Any],
    *,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    registry = registry or build_compliance_pack_registry()
    finding_tags = _finding_terms(finding)
    matched: list[dict[str, Any]] = []
    for pack in registry.get("packs", []):
        for clause in pack.get("clauses", []):
            clause_tags = {str(tag).lower() for tag in clause.get("tags", [])}
            finding_types = {str(tag).lower() for tag in clause.get("finding_types", [])}
            matched_terms = sorted(finding_tags & (clause_tags | finding_types))
            if matched_terms:
                matched.append(
                    {
                        "framework_id": pack["framework_id"],
                        "framework_name": pack["framework_name"],
                        "clause_id": clause["id"],
                        "clause_title": clause["title"],
                        "matched_terms": matched_terms,
                        "evidence_requirements": clause["evidence_requirements"],
                    }
                )
    return {
        "finding_id": finding.get("id", "unidentified-finding"),
        "finding_title": finding.get("title", finding.get("summary", "Untitled finding")),
        "severity": finding.get("severity", "unknown"),
        "matched_clause_count": len(matched),
        "matched_clauses": matched,
    }


def build_enterprise_compliance_pack_readiness(
    packet: dict[str, Any] | None = None,
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    if packet is None:
        return {
            "schema_version": COMPLIANCE_PACK_READINESS_SCHEMA,
            "product": "CAVRA",
            "evidence_mode": "contract",
            "ready_for_enterprise_compliance_pack_contract": True,
            "ready_for_enterprise_live_compliance_mapping": False,
            "status": "ready_with_warnings",
            "blocker_count": 0,
            "warning_count": 1,
            "checks": [
                {
                    "name": "evidence_packet",
                    "status": "warn",
                    "message": "Enterprise compliance mapping-pack contract is available, but no sample or live packet was supplied.",
                }
            ],
        }
    return validate_enterprise_compliance_pack_packet(packet, require_live=require_live)


def validate_enterprise_compliance_pack_packet(
    packet: dict[str, Any],
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_pack_registry(packet.get("pack_registry", {}), checks)
    _check_mapping_engine(packet.get("mapping_engine", {}), checks)
    _check_coverage(packet.get("coverage", {}), checks)
    _check_reporting(packet.get("reporting", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)

    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": COMPLIANCE_PACK_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_enterprise_compliance_pack_contract": contract_ready,
        "ready_for_enterprise_live_compliance_mapping": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _pack_nist_ai_rmf() -> dict[str, Any]:
    return _pack(
        "nist_ai_rmf",
        "NIST AI RMF 1.0",
        [
            _clause("GOVERN-1.1", "AI governance policies are documented and owned.", ["governance", "policy", "ownership"]),
            _clause("MAP-1.1", "AI system context and intended use are mapped.", ["inventory", "context", "asset"]),
            _clause("MEASURE-2.2", "AI risks are measured with repeatable evidence.", ["aispm", "risk", "measurement"]),
            _clause("MANAGE-1.3", "Risk responses are prioritized and tracked.", ["remediation", "approval", "exception"]),
            _clause("GOVERN-5.1", "Human oversight is assigned for high-impact AI actions.", ["approval", "human_oversight"]),
        ],
    )


def _pack_iso_iec_42001() -> dict[str, Any]:
    return _pack(
        "iso_iec_42001",
        "ISO/IEC 42001",
        [
            _clause("4.3", "AI management system scope is defined.", ["scope", "governance", "asset"]),
            _clause("5.3", "AI roles, responsibilities, and authorities are assigned.", ["rbac", "ownership", "approval"]),
            _clause("6.1.2", "AI risks and opportunities are assessed.", ["risk", "aispm", "finding"]),
            _clause("8.2", "Operational AI controls are implemented.", ["runtime", "control", "policy"]),
            _clause("9.1", "AI management system monitoring and measurement is performed.", ["monitoring", "measurement", "reporting"]),
        ],
    )


def _pack_owasp_llm_genai() -> dict[str, Any]:
    return _pack(
        "owasp_llm_genai",
        "OWASP LLM/GenAI",
        [
            _clause("LLM01", "Prompt injection and instruction override are controlled.", ["prompt_injection", "tool_call", "mcp"]),
            _clause("LLM02", "Sensitive information disclosure is prevented.", ["data_exposure", "secret", "egress"]),
            _clause("LLM05", "Improper output handling is governed before execution.", ["command", "execution", "runtime"]),
            _clause("LLM06", "Excessive agency is limited through authorization boundaries.", ["agent", "approval", "least_privilege"]),
            _clause("LLM08", "Vector, model, and context supply-chain risks are tracked.", ["supply_chain", "model", "artifact"]),
        ],
    )


def _pack_nist_ssdf() -> dict[str, Any]:
    return _pack(
        "nist_ssdf",
        "NIST SSDF SP 800-218",
        [
            _clause("PO.1.1", "Security requirements are documented for software development.", ["policy", "sdlc", "governance"]),
            _clause("PS.3.1", "Software components are archived and protected.", ["supply_chain", "artifact", "sbom"]),
            _clause("PW.4.1", "Reusable criteria are applied before code changes.", ["code_change", "runtime", "policy"]),
            _clause("PW.7.2", "Code review and approval controls are enforced.", ["approval", "pr", "change_control"]),
            _clause("RV.1.2", "Vulnerabilities and findings are tracked to remediation.", ["finding", "remediation", "vulnerability"]),
        ],
    )


def _pack_eu_ai_act() -> dict[str, Any]:
    return _pack(
        "eu_ai_act",
        "EU AI Act",
        [
            _clause("Article 9", "Risk management system is established and maintained.", ["risk", "aispm", "governance"]),
            _clause("Article 10", "Data governance and data quality controls are applied.", ["data_governance", "data_exposure", "quality"]),
            _clause("Article 11", "Technical documentation is generated and maintained.", ["documentation", "evidence", "audit"]),
            _clause("Article 12", "Logging capabilities provide traceability.", ["audit_log", "logging", "traceability"]),
            _clause("Article 14", "Human oversight measures are implemented.", ["human_oversight", "approval", "operator"]),
        ],
    )


def _pack(framework_id: str, framework_name: str, clauses: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": COMPLIANCE_PACK_SCHEMA,
        "framework_id": framework_id,
        "framework_name": framework_name,
        "version": "2026.07",
        "owner": "CAVRA Product Security",
        "clauses": clauses,
    }


def _clause(clause_id: str, title: str, tags: list[str]) -> dict[str, Any]:
    return {
        "id": clause_id,
        "title": title,
        "tags": tags,
        "finding_types": tags,
        "evidence_requirements": [
            "runtime_decision",
            "policy_reference",
            "approval_or_exception",
            "audit_log_reference",
            "aispm_finding",
        ],
    }


def _finding_terms(finding: dict[str, Any]) -> set[str]:
    terms: set[str] = set()
    for key in ("category", "finding_type", "control_family", "surface", "source", "asset_type"):
        if finding.get(key):
            terms.add(str(finding[key]).lower())
    for tag in finding.get("tags", []):
        if tag:
            terms.add(str(tag).lower())
    return terms


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_pack_schema(pack: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if pack.get("schema_version") == COMPLIANCE_PACK_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Compliance pack schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Pack must use cavra.compliance.pack.v1.")


def _check_pack_identity(pack: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if pack.get("framework_id") in REQUIRED_FRAMEWORKS and pack.get("framework_name") and pack.get("version"):
        _add_check(checks, "pack_identity", "pass", "Pack framework identity and version are present.")
    else:
        _add_check(checks, "pack_identity", "blocker", "Pack must include required framework_id, framework_name, and version.")


def _check_pack_clauses(pack: dict[str, Any], checks: list[dict[str, str]]) -> None:
    clauses = pack.get("clauses", [])
    ids = [clause.get("id") for clause in clauses]
    valid_clauses = [
        clause
        for clause in clauses
        if clause.get("id")
        and clause.get("title")
        and clause.get("tags")
        and clause.get("evidence_requirements")
    ]
    if len(valid_clauses) >= 3 and len(ids) == len(set(ids)):
        _add_check(checks, "clauses", "pass", f"{len(valid_clauses)} clause mappings are valid.")
    else:
        _add_check(checks, "clauses", "blocker", "Pack requires at least three unique clauses with tags and evidence requirements.")


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == COMPLIANCE_PACK_EVIDENCE_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Compliance mapping evidence packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.compliance.mapping-packs.evidence.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    evidence_mode = packet.get("evidence_mode")
    if evidence_mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live compliance mapping evidence packet supplied.")
    elif evidence_mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample compliance mapping packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live compliance mapping validation requires evidence_mode=live.")


def _check_pack_registry(registry: dict[str, Any], checks: list[dict[str, str]]) -> None:
    frameworks = set(registry.get("frameworks", []))
    missing_frameworks = sorted(REQUIRED_FRAMEWORKS - frameworks)
    required_flags = {
        "approved": registry.get("approved") is True,
        "versioned": registry.get("versioned") is True,
        "clause_level": registry.get("clause_level") is True,
        "owner": bool(registry.get("owner")),
        "latest_review_ref": bool(registry.get("latest_review_ref")),
        "change_control_ref": bool(registry.get("change_control_ref")),
    }
    if not missing_frameworks and all(required_flags.values()):
        _add_check(checks, "pack_registry", "pass", "Approved clause-level registry includes every required framework.")
        return
    missing = [name for name, ok in required_flags.items() if not ok]
    if missing_frameworks:
        missing.append(f"frameworks: {', '.join(missing_frameworks)}")
    _add_check(checks, "pack_registry", "blocker", f"Pack registry is missing: {', '.join(missing)}.")


def _check_mapping_engine(engine: dict[str, Any], checks: list[dict[str, str]]) -> None:
    unmapped_policy = engine.get("unmapped_finding_policy")
    required_flags = {
        "finding_to_clause_enabled": engine.get("finding_to_clause_enabled") is True,
        "deterministic_mapping_tested": engine.get("deterministic_mapping_tested") is True,
        "tag_taxonomy_version": bool(engine.get("tag_taxonomy_version")),
        "report_schema_version": bool(engine.get("report_schema_version")),
        "supported_unmapped_policy": unmapped_policy in SUPPORTED_UNMAPPED_POLICIES,
    }
    if all(required_flags.values()):
        _add_check(checks, "mapping_engine", "pass", "Finding-to-clause mapping engine is deterministic and versioned.")
    else:
        missing = [name for name, ok in required_flags.items() if not ok]
        _add_check(checks, "mapping_engine", "blocker", f"Mapping engine is missing: {', '.join(missing)}.")


def _check_coverage(coverage: dict[str, Any], checks: list[dict[str, str]]) -> None:
    frameworks = set(coverage.get("frameworks_with_clause_tests", []))
    missing_frameworks = sorted(REQUIRED_FRAMEWORKS - frameworks)
    clause_count = _as_int(coverage.get("clause_count"))
    mapped_findings = _as_int(coverage.get("test_findings_mapped"))
    coverage_percent = _as_float(coverage.get("coverage_percent"))
    if (
        not missing_frameworks
        and clause_count is not None
        and clause_count >= 25
        and mapped_findings is not None
        and mapped_findings >= 5
        and coverage_percent is not None
        and coverage_percent >= 90.0
    ):
        _add_check(checks, "coverage", "pass", f"{clause_count} clauses and {coverage_percent:.1f}% mapping coverage validated.")
        return
    missing: list[str] = []
    if missing_frameworks:
        missing.append(f"framework clause tests: {', '.join(missing_frameworks)}")
    if clause_count is None or clause_count < 25:
        missing.append("clause_count>=25")
    if mapped_findings is None or mapped_findings < 5:
        missing.append("test_findings_mapped>=5")
    if coverage_percent is None or coverage_percent < 90.0:
        missing.append("coverage_percent>=90")
    _add_check(checks, "coverage", "blocker", f"Compliance coverage is missing: {', '.join(missing)}.")


def _check_reporting(reporting: dict[str, Any], checks: list[dict[str, str]]) -> None:
    formats = set(reporting.get("formats", []))
    missing_formats = sorted(REQUIRED_REPORT_FORMATS - formats)
    required_flags = {
        "auditor_trace_enabled": reporting.get("auditor_trace_enabled") is True,
        "evidence_bundle_linking": reporting.get("evidence_bundle_linking") is True,
        "aispm_report_linking": reporting.get("aispm_report_linking") is True,
        "sample_report_ref": bool(reporting.get("sample_report_ref")),
    }
    if not missing_formats and all(required_flags.values()):
        _add_check(checks, "reporting", "pass", "Auditor, AISPM, and export reporting paths are linked.")
        return
    missing = [name for name, ok in required_flags.items() if not ok]
    if missing_formats:
        missing.append(f"formats: {', '.join(missing_formats)}")
    _add_check(checks, "reporting", "blocker", f"Reporting path is missing: {', '.join(missing)}.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = [
        "compliance_owner",
        "pack_review_ref",
        "exception_register_ref",
        "auditor_handoff_ref",
        "latest_validation_ref",
    ]
    missing = [field for field in required if not evidence.get(field)]
    if not missing:
        _add_check(checks, "operating_evidence", "pass", "Compliance operating evidence references are present.")
    else:
        _add_check(checks, "operating_evidence", "blocker", f"Operating evidence is missing: {', '.join(missing)}.")


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
