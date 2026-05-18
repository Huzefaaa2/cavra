package runtime

import (
	"encoding/json"
	"os"
	"testing"
)

type parityCase struct {
	Name     string            `json:"name"`
	Request  Request           `json:"request"`
	Registry string            `json:"registry"`
	Expected map[string]string `json:"expected"`
}

func TestParityCases(t *testing.T) {
	data, err := os.ReadFile("../testdata/parity_cases.json")
	if err != nil {
		t.Fatal(err)
	}
	var cases []parityCase
	if err := json.Unmarshal(data, &cases); err != nil {
		t.Fatal(err)
	}
	for _, item := range cases {
		t.Run(item.Name, func(t *testing.T) {
			decision := evaluateParityCase(t, item)
			assertEqual(t, "decision", decision.Decision, item.Expected["decision"])
			assertEqual(t, "rule_id", decision.RuleID, item.Expected["rule_id"])
			assertEqual(t, "severity", decision.Severity, item.Expected["severity"])
			if expected := item.Expected["approver_group"]; expected != "" {
				assertEqual(t, "approver_group", decision.ApproverGroup, expected)
			}
			if expected := item.Expected["evidence_ref_prefix"]; expected != "" {
				assertNotEmpty(t, "decision_id", decision.DecisionID)
				assertNotEmpty(t, "timestamp", decision.Timestamp)
				assertHasPrefix(t, "correlation_id", decision.CorrelationID, "corr_")
				if len(decision.EvidenceRefs) == 0 {
					t.Fatal("evidence_refs must not be empty")
				}
				assertHasPrefix(t, "evidence_refs[0]", decision.EvidenceRefs[0], expected)
			}
		})
	}
}

func evaluateParityCase(t *testing.T, item parityCase) Decision {
	t.Helper()
	if item.Registry == "" {
		return Evaluate(item.Request)
	}
	registry, err := LoadTrustRegistry("../testdata/" + item.Registry)
	if err != nil {
		t.Fatal(err)
	}
	return EvaluateWithRegistry(item.Request, registry)
}

func TestCompiledPolicyCases(t *testing.T) {
	policy, err := LoadCompiledPolicy("../testdata/compiled_policy.json")
	if err != nil {
		t.Fatal(err)
	}
	cases := []parityCase{
		{
			Name: "compiled policy blocks custom secret reads",
			Request: Request{
				ActionType: "read_file",
				Target:     "config/prod.secret",
			},
			Expected: map[string]string{
				"decision": "block",
				"rule_id":  "filesystem.read.block",
				"severity": "high",
			},
		},
		{
			Name: "compiled policy allows custom read-only command",
			Request: Request{
				ActionType: "execute_command",
				Target:     "custom scan --check",
			},
			Expected: map[string]string{
				"decision": "allow",
				"rule_id":  "commands.allow",
				"severity": "low",
			},
		},
		{
			Name: "compiled policy blocks unknown MCP by default",
			Request: Request{
				ActionType: "mcp_tool_call",
				Server:     "unknown-provider",
				Tool:       "read_file",
				Capability: "filesystem",
			},
			Expected: map[string]string{
				"decision": "block",
				"rule_id":  "mcp.server.trust.block_unknown",
				"severity": "high",
			},
		},
		{
			Name: "compiled policy requires approval for protected writes",
			Request: Request{
				ActionType: "write_file",
				Target:     "iam/admin-role.tf",
				SessionID:  "compiled-approval",
			},
			Expected: map[string]string{
				"decision":            "require_approval",
				"rule_id":             "filesystem.write.require_approval",
				"severity":            "high",
				"approver_group":      "Platform Security",
				"evidence_ref_prefix": "evidence://compiled-approval/",
			},
		},
	}
	for _, item := range cases {
		t.Run(item.Name, func(t *testing.T) {
			decision := EvaluateWithPolicy(item.Request, policy)
			assertEqual(t, "decision", decision.Decision, item.Expected["decision"])
			assertEqual(t, "rule_id", decision.RuleID, item.Expected["rule_id"])
			assertEqual(t, "severity", decision.Severity, item.Expected["severity"])
			assertEqual(t, "policy_pack", decision.PolicyPack, "cavra-go-compiled-fixture")
			if expected := item.Expected["approver_group"]; expected != "" {
				assertEqual(t, "approver_group", decision.ApproverGroup, expected)
			}
			if expected := item.Expected["evidence_ref_prefix"]; expected != "" {
				if len(decision.EvidenceRefs) == 0 {
					t.Fatal("evidence_refs must not be empty")
				}
				assertHasPrefix(t, "evidence_refs[0]", decision.EvidenceRefs[0], expected)
			}
		})
	}
}

func assertEqual(t *testing.T, field string, actual string, expected string) {
	t.Helper()
	if actual != expected {
		t.Fatalf("%s mismatch: got %q want %q", field, actual, expected)
	}
}

func assertNotEmpty(t *testing.T, field string, actual string) {
	t.Helper()
	if actual == "" {
		t.Fatalf("%s must not be empty", field)
	}
}

func assertHasPrefix(t *testing.T, field string, actual string, expected string) {
	t.Helper()
	if len(actual) < len(expected) || actual[:len(expected)] != expected {
		t.Fatalf("%s prefix mismatch: got %q want prefix %q", field, actual, expected)
	}
}
