package runtime

import (
	"encoding/json"
	"os"
	"testing"
)

type parityCase struct {
	Name     string            `json:"name"`
	Request  Request           `json:"request"`
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
			decision := Evaluate(item.Request)
			assertEqual(t, "decision", decision.Decision, item.Expected["decision"])
			assertEqual(t, "rule_id", decision.RuleID, item.Expected["rule_id"])
			assertEqual(t, "severity", decision.Severity, item.Expected["severity"])
			if expected := item.Expected["approver_group"]; expected != "" {
				assertEqual(t, "approver_group", decision.ApproverGroup, expected)
			}
		})
	}
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
	}
	for _, item := range cases {
		t.Run(item.Name, func(t *testing.T) {
			decision := EvaluateWithPolicy(item.Request, policy)
			assertEqual(t, "decision", decision.Decision, item.Expected["decision"])
			assertEqual(t, "rule_id", decision.RuleID, item.Expected["rule_id"])
			assertEqual(t, "severity", decision.Severity, item.Expected["severity"])
			assertEqual(t, "policy_pack", decision.PolicyPack, "cavra-go-compiled-fixture")
		})
	}
}

func assertEqual(t *testing.T, field string, actual string, expected string) {
	t.Helper()
	if actual != expected {
		t.Fatalf("%s mismatch: got %q want %q", field, actual, expected)
	}
}
