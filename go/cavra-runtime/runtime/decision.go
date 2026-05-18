package runtime

import (
	"fmt"
	"regexp"
	"strings"
)

type Request struct {
	ActionType string `json:"action_type"`
	Target     string `json:"target"`
	Operation  string `json:"operation"`
	PolicyPack string `json:"policy_pack"`
	Server     string `json:"server"`
	Tool       string `json:"tool"`
	Capability string `json:"capability"`
}

type Decision struct {
	Decision           string `json:"decision"`
	Reason             string `json:"reason"`
	ActionType         string `json:"action_type"`
	Target             string `json:"target"`
	RequestedOperation string `json:"requested_operation"`
	PolicyPack         string `json:"policy_pack"`
	PolicyID           string `json:"policy_id"`
	RuleID             string `json:"rule_id"`
	Severity           string `json:"severity"`
	ApproverGroup      string `json:"approver_group,omitempty"`
}

type policy struct {
	blockRead            []string
	blockWrite           []string
	requireApprovalWrite []string
	commandBlock         []string
	commandAllow         []string
	mcpAllowedServers    []string
	mcpBlockedServers    []string
	mcpBlockUnknown      bool
}

func Evaluate(request Request) Decision {
	pack := request.PolicyPack
	if pack == "" {
		pack = "cavra-ai-agent-baseline"
	}
	p := builtInPolicy(pack)
	switch request.ActionType {
	case "read_file":
		return evaluateFile(request.Target, "read", pack, p)
	case "write_file":
		return evaluateFile(request.Target, "write", pack, p)
	case "execute_command":
		return evaluateCommand(request.Target, pack, p)
	case "git_operation":
		return evaluateGit(request.Operation, request.Target, pack)
	case "mcp_tool_call":
		return evaluateMCP(request, pack, p)
	default:
		return baseDecision("require_approval", "Unknown action type; review required.", request.ActionType, request.Target, request.Operation, pack, "runtime.default.require_approval", "medium", "Repository Owners")
	}
}

func evaluateFile(target string, mode string, pack string, p policy) Decision {
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

func evaluateCommand(command string, pack string, p policy) Decision {
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

func evaluateMCP(request Request, pack string, p policy) Decision {
	target := request.Server + ":" + request.Tool
	requested := request.Capability
	if requested == "" {
		requested = request.Tool
	}
	if contains(p.mcpBlockedServers, request.Server) || (p.mcpBlockUnknown && !contains(p.mcpAllowedServers, request.Server)) {
		return baseDecision("block", "Untrusted MCP server with filesystem/tool capability is not approved.", "mcp_tool_call", target, requested, pack, "mcp.server.trust.block_unknown", "high", "")
	}
	return baseDecision("allow", "MCP server is trusted for this tool call.", "mcp_tool_call", target, requested, pack, "mcp.server.trust.allow", "low", "")
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

func builtInPolicy(pack string) policy {
	switch pack {
	case "cavra-banking-baseline":
		return policy{
			blockRead:            []string{".env", "**/secrets.*", "**/*.pem", "**/kubeconfig", "**/terraform.tfstate", "**/terraform.tfvars"},
			requireApprovalWrite: []string{"iam/**", "**/iam/**", "**/security/**", "**/policies/**"},
			commandBlock:         []string{"terraform apply*", "kubectl delete*", "az role assignment create*", "aws iam create-access-key*", "gcloud projects add-iam-policy-binding*", "git push origin main"},
			commandAllow:         []string{"terraform fmt*", "terraform validate*", "terraform plan*", "pytest*", "npm test*"},
		}
	case "cavra-mcp-enterprise":
		return policy{
			blockRead:            []string{".env", "**/secrets.*", "**/*.pem", "**/kubeconfig", "**/terraform.tfstate"},
			requireApprovalWrite: []string{"**/iam/**", "**/security/**", "**/policies/**"},
			commandBlock:         []string{"terraform apply*", "kubectl delete*", "aws iam*", "az role*"},
			commandAllow:         []string{"terraform fmt*", "terraform plan*", "git*"},
			mcpAllowedServers:    []string{"github-enterprise", "jira-enterprise", "confluence-readonly", "internal-docs-readonly"},
			mcpBlockedServers:    []string{"unknown-mcp-provider", "public-browser-mcp", "personal-drive-mcp"},
			mcpBlockUnknown:      true,
		}
	default:
		return policy{
			blockRead:            []string{".env", "**/secrets.*", "**/*.pem", "**/*.pfx", "**/id_rsa", "**/kubeconfig", "**/terraform.tfstate", "**/terraform.tfvars"},
			blockWrite:           []string{".github/workflows/**", "**/main.tf", "**/providers.tf", "**/backend.tf"},
			requireApprovalWrite: []string{"iam/**", "security/**", "policies/**"},
			commandBlock:         []string{"terraform apply*", "kubectl delete*", "az role assignment create*", "aws iam create-access-key*", "gcloud projects add-iam-policy-binding*", "git push origin main", "git push origin master"},
			commandAllow:         []string{"terraform fmt*", "terraform validate*", "terraform plan*", "pytest*", "npm test*"},
		}
	}
}
