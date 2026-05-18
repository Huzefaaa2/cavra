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

func assertEqual(t *testing.T, field string, actual string, expected string) {
	t.Helper()
	if actual != expected {
		t.Fatalf("%s mismatch: got %q want %q", field, actual, expected)
	}
}
