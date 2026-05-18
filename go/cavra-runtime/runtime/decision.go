package runtime

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"regexp"
	"strings"
	"time"
)

type Request struct {
	SessionID          string `json:"session_id,omitempty"`
	AgentID            string `json:"agent_id,omitempty"`
	Actor              string `json:"actor,omitempty"`
	ActionType         string `json:"action_type"`
	Target             string `json:"target"`
	Operation          string `json:"operation"`
	RequestedOperation string `json:"requested_operation"`
	PolicyPack         string `json:"policy_pack"`
	Server             string `json:"server"`
	Tool               string `json:"tool"`
	Capability         string `json:"capability"`
}

type Decision struct {
	DecisionID         string   `json:"decision_id,omitempty"`
	SessionID          string   `json:"session_id,omitempty"`
	AgentID            string   `json:"agent_id,omitempty"`
	Actor              string   `json:"actor,omitempty"`
	Decision           string   `json:"decision"`
	Reason             string   `json:"reason"`
	ActionType         string   `json:"action_type"`
	Target             string   `json:"target"`
	RequestedOperation string   `json:"requested_operation"`
	PolicyPack         string   `json:"policy_pack"`
	PolicyID           string   `json:"policy_id"`
	RuleID             string   `json:"rule_id"`
	Severity           string   `json:"severity"`
	EvidenceRefs       []string `json:"evidence_refs,omitempty"`
	ApproverGroup      string   `json:"approver_group,omitempty"`
	Timestamp          string   `json:"timestamp,omitempty"`
	CorrelationID      string   `json:"correlation_id,omitempty"`
}

type Policy struct {
	id                   string
	blockRead            []string
	blockWrite           []string
	requireApprovalWrite []string
	commandBlock         []string
	commandAllow         []string
	mcpAllowedServers    []string
	mcpBlockedServers    []string
	mcpBlockUnknown      bool
}

type TrustRegistry struct {
	MCPServers []MCPServerRecord `json:"mcp_servers"`
}

type MCPServerRecord struct {
	ServerID      string   `json:"server_id"`
	Name          string   `json:"name"`
	TrustTier     string   `json:"trust_tier"`
	ApprovalState string   `json:"approval_state"`
	Capabilities  []string `json:"capabilities"`
	AllowedTools  []string `json:"allowed_tools"`
}

type compiledPolicy struct {
	Metadata struct {
		ID string `json:"id"`
	} `json:"metadata"`
	Filesystem struct {
		BlockRead            []string `json:"block_read"`
		BlockWrite           []string `json:"block_write"`
		RequireApprovalWrite []string `json:"require_approval_write"`
	} `json:"filesystem"`
	Commands struct {
		Block []string `json:"block"`
		Allow []string `json:"allow"`
	} `json:"commands"`
	MCP struct {
		AllowedServers      []string `json:"allowed_servers"`
		BlockedServers      []string `json:"blocked_servers"`
		BlockUnknownServers *bool    `json:"block_unknown_servers"`
	} `json:"mcp"`
}

func Evaluate(request Request) Decision {
	pack := request.PolicyPack
	if pack == "" {
		pack = "cavra-ai-agent-baseline"
	}
	p := builtInPolicy(pack)
	return EvaluateWithPolicy(request, p)
}

func EvaluateWithRegistry(request Request, registry TrustRegistry) Decision {
	pack := request.PolicyPack
	if pack == "" {
		pack = "cavra-ai-agent-baseline"
	}
	p := builtInPolicy(pack)
	return EvaluateWithPolicyAndRegistry(request, p, &registry)
}

func EvaluateWithPolicy(request Request, p Policy) Decision {
	return EvaluateWithPolicyAndRegistry(request, p, nil)
}

func EvaluateWithPolicyAndRegistry(request Request, p Policy, registry *TrustRegistry) Decision {
	pack := request.PolicyPack
	if pack == "" {
		pack = p.id
	}
	if pack == "" {
		pack = "cavra-ai-agent-baseline"
	}
	var decision Decision
	switch request.ActionType {
	case "read_file":
		decision = evaluateFile(request.Target, "read", pack, p)
	case "write_file":
		decision = evaluateFile(request.Target, "write", pack, p)
	case "execute_command":
		decision = evaluateCommand(request.Target, pack, p)
	case "git_operation":
		decision = evaluateGit(request.operation(), request.Target, pack)
	case "mcp_tool_call":
		if registry != nil {
			decision = evaluateMCPRegistry(request, pack, registry)
		} else {
			decision = evaluateMCP(request, pack, p)
		}
	default:
		decision = baseDecision("require_approval", "Unknown action type; review required.", request.ActionType, request.Target, request.operation(), pack, "runtime.default.require_approval", "medium", "Repository Owners")
	}
	return withRequestMetadata(decision, request)
}

func LoadTrustRegistry(path string) (TrustRegistry, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return TrustRegistry{}, err
	}
	var registry TrustRegistry
	if err := json.Unmarshal(data, &registry); err != nil {
		return TrustRegistry{}, err
	}
	return registry, nil
}

func LoadCompiledPolicy(path string) (Policy, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return Policy{}, err
	}
	var compiled compiledPolicy
	if err := json.Unmarshal(data, &compiled); err != nil {
		return Policy{}, err
	}
	p := Policy{
		id:                   compiled.Metadata.ID,
		blockRead:            stringsList(compiled.Filesystem.BlockRead),
		blockWrite:           stringsList(compiled.Filesystem.BlockWrite),
		requireApprovalWrite: stringsList(compiled.Filesystem.RequireApprovalWrite),
		commandBlock:         stringsList(compiled.Commands.Block),
		commandAllow:         stringsList(compiled.Commands.Allow),
		mcpAllowedServers:    stringsList(compiled.MCP.AllowedServers),
		mcpBlockedServers:    stringsList(compiled.MCP.BlockedServers),
		mcpBlockUnknown:      true,
	}
	if compiled.MCP.BlockUnknownServers != nil {
		p.mcpBlockUnknown = *compiled.MCP.BlockUnknownServers
	}
	return p, nil
}

func evaluateFile(target string, mode string, pack string, p Policy) Decision {
	patterns := p.blockRead
	if mode == "write" {
		patterns = p.blockWrite
	}
	for _, pattern := range patterns {
		if matchPattern(target, pattern) {
			return baseDecision("block", fmt.Sprintf("Matched sensitive path policy: %s", pattern), mode+"_file", target, mode, pack, "filesystem."+mode+".block", "high", "")
		}
	}
	if mode == "write" {
		for _, pattern := range p.requireApprovalWrite {
			if matchPattern(target, pattern) {
				return baseDecision("require_approval", fmt.Sprintf("Matched approval-required path policy: %s", pattern), "write_file", target, mode, pack, "filesystem.write.require_approval", "high", "Platform Security")
			}
		}
	}
	return baseDecision("allow", "No sensitive path policy matched.", mode+"_file", target, mode, pack, "filesystem."+mode+".allow", "low", "")
}

func evaluateCommand(command string, pack string, p Policy) Decision {
	cleaned := strings.TrimSpace(command)
	for _, pattern := range p.commandBlock {
		if matchPattern(cleaned, pattern) {
			severity := "high"
			if strings.Contains(cleaned, "apply") || strings.Contains(cleaned, "delete") {
				severity = "critical"
			}
			return baseDecision("block", fmt.Sprintf("Matched blocked command policy: %s", pattern), "execute_command", cleaned, cleaned, pack, "commands.block", severity, "")
		}
	}
	for _, pattern := range p.commandAllow {
		if matchPattern(cleaned, pattern) {
			return baseDecision("allow", fmt.Sprintf("Matched allowed command policy: %s", pattern), "execute_command", cleaned, cleaned, pack, "commands.allow", "low", "")
		}
	}
	return baseDecision("require_approval", "No allow rule matched; review required.", "execute_command", cleaned, cleaned, pack, "commands.default.require_approval", "medium", "Repository Owners")
}

func evaluateGit(operation string, target string, pack string) Decision {
	if operation == "push" && (strings.HasSuffix(target, "main") || strings.HasSuffix(target, "master")) {
		return baseDecision("block", "Direct push to protected branch is prohibited.", "git_operation", target, operation, pack, "git.protected_branch.block_direct_push", "high", "")
	}
	requested := operation
	if requested == "" {
		requested = target
	}
	return baseDecision("allow", "Git operation is allowed by policy.", "git_operation", target, requested, pack, "git.allow", "low", "")
}

func evaluateMCP(request Request, pack string, p Policy) Decision {
	target := request.Server + ":" + request.Tool
	requested := request.operation()
	if requested == "" {
		requested = request.Tool
	}
	if contains(p.mcpBlockedServers, request.Server) || (p.mcpBlockUnknown && !contains(p.mcpAllowedServers, request.Server)) {
		return baseDecision("block", "Untrusted MCP server with filesystem/tool capability is not approved.", "mcp_tool_call", target, requested, pack, "mcp.server.trust.block_unknown", "high", "")
	}
	return baseDecision("allow", "MCP server is trusted for this tool call.", "mcp_tool_call", target, requested, pack, "mcp.server.trust.allow", "low", "")
}

func evaluateMCPRegistry(request Request, pack string, registry *TrustRegistry) Decision {
	target := request.Server + ":" + request.Tool
	requested := request.operation()
	if requested == "" {
		requested = request.Tool
	}
	record := registry.FindMCPServer(request.Server)
	if record == nil {
		return baseDecision("block", "MCP server is not registered.", "mcp_tool_call", target, requested, pack, "mcp.registry.unknown", "high", "")
	}
	if record.TrustTier == "blocked" || record.ApprovalState == "denied" {
		return baseDecision("block", "MCP server is blocked or denied in the trust registry.", "mcp_tool_call", target, requested, pack, "mcp.registry.blocked", "high", "")
	}
	if record.ApprovalState == "pending" || record.TrustTier == "unknown" || record.TrustTier == "experimental" {
		return baseDecision("require_approval", "MCP server requires trust approval before use.", "mcp_tool_call", target, requested, pack, "mcp.registry.requires_approval", "medium", "AI Governance")
	}
	if len(record.AllowedTools) > 0 && !contains(record.AllowedTools, request.Tool) {
		return baseDecision("require_approval", "MCP tool is outside the server's approved tool scope.", "mcp_tool_call", target, requested, pack, "mcp.registry.tool_scope", "medium", "AI Governance")
	}
	if request.Capability != "" && len(record.Capabilities) > 0 && !contains(record.Capabilities, request.Capability) {
		return baseDecision("require_approval", "MCP capability is outside the server's approved capability scope.", "mcp_tool_call", target, requested, pack, "mcp.registry.capability_scope", "medium", "AI Governance")
	}
	return baseDecision("allow", "MCP server is approved in the trust registry.", "mcp_tool_call", target, requested, pack, "mcp.registry.allow", "low", "")
}

func (registry TrustRegistry) FindMCPServer(serverID string) *MCPServerRecord {
	for index := range registry.MCPServers {
		record := &registry.MCPServers[index]
		if record.ServerID == serverID || record.Name == serverID {
			return record
		}
	}
	return nil
}

func (request Request) operation() string {
	if request.Operation != "" {
		return request.Operation
	}
	if request.RequestedOperation != "" {
		return request.RequestedOperation
	}
	if request.Capability != "" {
		return request.Capability
	}
	return ""
}

func withRequestMetadata(decision Decision, request Request) Decision {
	decision.SessionID = defaultString(request.SessionID, "local")
	decision.AgentID = defaultString(request.AgentID, "unknown-agent")
	decision.Actor = defaultString(request.Actor, "ai-agent")
	return withEvidenceMetadata(decision)
}

func baseDecision(decision string, reason string, actionType string, target string, requested string, pack string, ruleID string, severity string, approverGroup string) Decision {
	return Decision{
		Decision:           decision,
		Reason:             reason,
		ActionType:         actionType,
		Target:             target,
		RequestedOperation: requested,
		PolicyPack:         pack,
		PolicyID:           pack,
		RuleID:             ruleID,
		Severity:           severity,
		ApproverGroup:      approverGroup,
	}
}

func withEvidenceMetadata(decision Decision) Decision {
	if decision.DecisionID == "" {
		decision.DecisionID = "dec_" + randomHex(12)
	}
	if decision.Timestamp == "" {
		decision.Timestamp = time.Now().UTC().Format(time.RFC3339Nano)
	}
	if decision.CorrelationID == "" {
		decision.CorrelationID = "corr_" + randomHex(12)
	}
	if len(decision.EvidenceRefs) == 0 {
		sessionID := defaultString(decision.SessionID, "local")
		decision.EvidenceRefs = []string{fmt.Sprintf("evidence://%s/%s", sessionID, decision.DecisionID)}
	}
	return decision
}

func randomHex(length int) string {
	if length <= 0 {
		return ""
	}
	data := make([]byte, (length+1)/2)
	if _, err := rand.Read(data); err != nil {
		return strings.Repeat("0", length)
	}
	encoded := hex.EncodeToString(data)
	if len(encoded) > length {
		return encoded[:length]
	}
	return encoded
}

func defaultString(value string, fallback string) string {
	if value == "" {
		return fallback
	}
	return value
}

func matchPattern(value string, pattern string) bool {
	quoted := regexp.QuoteMeta(pattern)
	quoted = strings.ReplaceAll(quoted, `\*\*`, ".*")
	quoted = strings.ReplaceAll(quoted, `\*`, ".*")
	matched, err := regexp.MatchString("^"+quoted+"$", value)
	return err == nil && matched
}

func contains(items []string, value string) bool {
	for _, item := range items {
		if item == value {
			return true
		}
	}
	return false
}

func stringsList(items []string) []string {
	result := make([]string, 0, len(items))
	for _, item := range items {
		cleaned := strings.TrimSpace(item)
		if cleaned != "" {
			result = append(result, cleaned)
		}
	}
	return result
}

func builtInPolicy(pack string) Policy {
	switch pack {
	case "cavra-banking-baseline":
		return Policy{
			id:                   pack,
			blockRead:            []string{".env", "**/secrets.*", "**/*.pem", "**/kubeconfig", "**/terraform.tfstate", "**/terraform.tfvars"},
			requireApprovalWrite: []string{"iam/**", "**/iam/**", "**/security/**", "**/policies/**"},
			commandBlock:         []string{"terraform apply*", "kubectl delete*", "az role assignment create*", "aws iam create-access-key*", "gcloud projects add-iam-policy-binding*", "git push origin main"},
			commandAllow:         []string{"terraform fmt*", "terraform validate*", "terraform plan*", "pytest*", "npm test*"},
		}
	case "cavra-mcp-enterprise":
		return Policy{
			id:                   pack,
			blockRead:            []string{".env", "**/secrets.*", "**/*.pem", "**/kubeconfig", "**/terraform.tfstate"},
			requireApprovalWrite: []string{"**/iam/**", "**/security/**", "**/policies/**"},
			commandBlock:         []string{"terraform apply*", "kubectl delete*", "aws iam*", "az role*"},
			commandAllow:         []string{"terraform fmt*", "terraform plan*", "git*"},
			mcpAllowedServers:    []string{"github-enterprise", "jira-enterprise", "confluence-readonly", "internal-docs-readonly"},
			mcpBlockedServers:    []string{"unknown-mcp-provider", "public-browser-mcp", "personal-drive-mcp"},
			mcpBlockUnknown:      true,
		}
	default:
		return Policy{
			id:                   pack,
			blockRead:            []string{".env", "**/secrets.*", "**/*.pem", "**/*.pfx", "**/id_rsa", "**/kubeconfig", "**/terraform.tfstate", "**/terraform.tfvars"},
			blockWrite:           []string{".github/workflows/**", "**/main.tf", "**/providers.tf", "**/backend.tf"},
			requireApprovalWrite: []string{"iam/**", "security/**", "policies/**"},
			commandBlock:         []string{"terraform apply*", "kubectl delete*", "az role assignment create*", "aws iam create-access-key*", "gcloud projects add-iam-policy-binding*", "git push origin main", "git push origin master"},
			commandAllow:         []string{"terraform fmt*", "terraform validate*", "terraform plan*", "pytest*", "npm test*"},
		}
	}
}
