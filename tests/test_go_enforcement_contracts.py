import subprocess
from pathlib import Path


def test_go_enforcement_contract_generator_is_idempotent() -> None:
    contract_path = Path("go/cavra-runtime/enforcement/v1/contracts.go")
    before = contract_path.read_text(encoding="utf-8")

    subprocess.run(["python3", "scripts/generate_go_enforcement_contracts.py"], check=True)

    assert contract_path.read_text(encoding="utf-8") == before


def test_go_enforcement_contract_docs_reference_generated_package() -> None:
    doc = Path("docs/go-enforcement-contracts.md").read_text(encoding="utf-8")
    wiki = Path("docs/wiki/Go-Enforcement-Contracts.md").read_text(encoding="utf-8")

    assert "proto/cavra/enforcement/v1/enforcement.proto" in doc
    assert "go/cavra-runtime/enforcement/v1" in doc
    assert "EvaluateRequest" in doc
    assert "ReleaseGovernanceEvidence" in doc
    assert "RunnerAuthentication" in doc
    assert "RunnerIdentity" in doc
    assert "DecisionResponse" in doc
    assert "release_governance" in doc
    assert "runner_auth" in doc
    assert "go/cavra-runtime/enforcement/v1" in wiki


def test_go_release_governance_contract_fixtures_are_documented() -> None:
    fixture = Path("go/cavra-runtime/testdata/release_governance_contracts.json")
    proto = Path("proto/cavra/enforcement/v1/enforcement.proto").read_text(encoding="utf-8")
    contracts = Path("go/cavra-runtime/enforcement/v1/contracts.go").read_text(encoding="utf-8")

    assert fixture.exists()
    assert "message ReleaseGovernanceEvidence" in proto
    assert "message RunnerAuthentication" in proto
    assert "message RunnerIdentity" in proto
    assert "ReleaseGovernance  *ReleaseGovernanceEvidence" in contracts
    assert "RunnerAuth" in contracts
    assert "RuntimeRecord" in contracts
    assert "verification_status" in proto
    assert "integrity_status" in proto
    assert "audit_export_status" in proto
    assert "VerificationStatus" in contracts
    assert "IntegrityStatus" in contracts
    assert "AuditExportStatus" in contracts
    assert "rollout-promotion-audit-export" in fixture.read_text(encoding="utf-8")
    assert "rollout-rollback-audit-export" in fixture.read_text(encoding="utf-8")
