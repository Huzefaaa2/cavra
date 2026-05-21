package main

import (
	"strings"
	"testing"
)

func TestDecodeRuntimeRequestSupportsTypedReleaseGovernanceContract(t *testing.T) {
	request, err := decodeRuntimeRequest(strings.NewReader(`{
		"session_id": "typed-cli",
		"release_governance": {
			"metadata_kind": "release-connector-delivery",
			"failed_delivery_count": 1,
			"blocked_count": 1
		}
	}`))
	if err != nil {
		t.Fatal(err)
	}
	if request.ActionType != "release_governance_record" {
		t.Fatalf("action type mismatch: got %q", request.ActionType)
	}
	if request.Record["metadata_kind"] != "release-connector-delivery" {
		t.Fatalf("metadata kind mismatch: got %+v", request.Record)
	}
	if request.Record["failed_delivery_count"] != 1 {
		t.Fatalf("failed delivery count mismatch: got %+v", request.Record)
	}
}

func TestDecodeRuntimeRequestKeepsLegacyRuntimeRecordShape(t *testing.T) {
	request, err := decodeRuntimeRequest(strings.NewReader(`{
		"session_id": "legacy-cli",
		"action_type": "release_governance_record",
		"record": {
			"metadata_kind": "rollout-promotion-execution",
			"approval_state": "approved",
			"approval_id": "apr_prod"
		}
	}`))
	if err != nil {
		t.Fatal(err)
	}
	if request.ActionType != "release_governance_record" {
		t.Fatalf("action type mismatch: got %q", request.ActionType)
	}
	if request.Record["approval_id"] != "apr_prod" {
		t.Fatalf("approval id mismatch: got %+v", request.Record)
	}
}
