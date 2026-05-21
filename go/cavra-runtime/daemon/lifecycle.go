package daemon

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"time"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

const DefaultLifecycleTimeout = 5 * time.Second

type LifecycleConfig struct {
	SocketPath      string
	PIDPath         string
	PolicyPath      string
	RegistryPath    string
	EvidenceLogPath string
	EvidenceKey     string
	EvidenceKeyID   string
	RunnerAuthKey   string
	RunnerAuthKeyID string
	BinaryPath      string
	StartupTimeout  time.Duration
}

type LifecycleStatus struct {
	Running          bool   `json:"running"`
	PID              int    `json:"pid,omitempty"`
	SocketPath       string `json:"socket_path"`
	PIDPath          string `json:"pid_path"`
	ProcessRunning   bool   `json:"process_running"`
	SocketResponsive bool   `json:"socket_responsive"`
	Message          string `json:"message"`
}

func DefaultPIDPath(socketPath string) string {
	if socketPath == "" {
		return ".cavra/cavra-runtime.pid"
	}
	return socketPath + ".pid"
}

func StartDaemon(config LifecycleConfig) (LifecycleStatus, error) {
	config, err := normalizeLifecycleConfig(config)
	if err != nil {
		return LifecycleStatus{}, err
	}
	status, err := StatusDaemon(config)
	if err == nil && status.Running {
		return status, errors.New("daemon is already running")
	}
	if err := os.MkdirAll(filepath.Dir(config.SocketPath), 0o755); err != nil {
		return LifecycleStatus{}, err
	}
	if err := os.MkdirAll(filepath.Dir(config.PIDPath), 0o755); err != nil {
		return LifecycleStatus{}, err
	}
	_ = os.Remove(config.SocketPath)
	args := []string{"--serve", "--socket", config.SocketPath}
	if config.PolicyPath != "" {
		args = append(args, "--policy", config.PolicyPath)
	}
	if config.RegistryPath != "" {
		args = append(args, "--registry", config.RegistryPath)
	}
	if config.EvidenceLogPath != "" {
		args = append(args, "--evidence-log", config.EvidenceLogPath)
	}
	if config.EvidenceKey != "" {
		args = append(args, "--evidence-signing-key", config.EvidenceKey)
	}
	if config.EvidenceKeyID != "" {
		args = append(args, "--evidence-signing-key-id", config.EvidenceKeyID)
	}
	if config.RunnerAuthKey != "" {
		args = append(args, "--runner-auth-key", config.RunnerAuthKey)
	}
	if config.RunnerAuthKeyID != "" {
		args = append(args, "--runner-auth-key-id", config.RunnerAuthKeyID)
	}
	cmd := exec.Command(config.BinaryPath, args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Start(); err != nil {
		return LifecycleStatus{}, err
	}
	if err := os.WriteFile(config.PIDPath, []byte(strconv.Itoa(cmd.Process.Pid)+"\n"), 0o644); err != nil {
		_ = cmd.Process.Kill()
		return LifecycleStatus{}, err
	}
	_ = cmd.Process.Release()
	if err := waitForReady(config); err != nil {
		if pid, pidErr := readPID(config.PIDPath); pidErr == nil {
			if process, findErr := os.FindProcess(pid); findErr == nil {
				_ = process.Kill()
			}
		}
		_ = os.Remove(config.PIDPath)
		_ = os.Remove(config.SocketPath)
		return LifecycleStatus{}, err
	}
	return StatusDaemon(config)
}

func StopDaemon(config LifecycleConfig) (LifecycleStatus, error) {
	config, err := normalizeLifecycleConfig(config)
	if err != nil {
		return LifecycleStatus{}, err
	}
	pid, err := readPID(config.PIDPath)
	if err != nil {
		_ = os.Remove(config.SocketPath)
		return LifecycleStatus{
			Running:    false,
			SocketPath: config.SocketPath,
			PIDPath:    config.PIDPath,
			Message:    "daemon pid file not found",
		}, nil
	}
	process, err := os.FindProcess(pid)
	if err != nil {
		return LifecycleStatus{}, err
	}
	_ = process.Signal(os.Interrupt)
	deadline := time.Now().Add(config.StartupTimeout)
	for time.Now().Before(deadline) {
		if !processRunning(pid) {
			break
		}
		time.Sleep(100 * time.Millisecond)
	}
	if processRunning(pid) {
		_ = process.Kill()
	}
	_ = os.Remove(config.PIDPath)
	_ = os.Remove(config.SocketPath)
	return LifecycleStatus{
		Running:        false,
		PID:            pid,
		SocketPath:     config.SocketPath,
		PIDPath:        config.PIDPath,
		ProcessRunning: processRunning(pid),
		Message:        "daemon stopped",
	}, nil
}

func StatusDaemon(config LifecycleConfig) (LifecycleStatus, error) {
	config, err := normalizeLifecycleConfig(config)
	if err != nil {
		return LifecycleStatus{}, err
	}
	status := LifecycleStatus{
		SocketPath: config.SocketPath,
		PIDPath:    config.PIDPath,
	}
	pid, err := readPID(config.PIDPath)
	if err == nil {
		status.PID = pid
		status.ProcessRunning = processRunning(pid)
	}
	status.SocketResponsive = socketResponsive(config.SocketPath, config.StartupTimeout)
	status.Running = status.SocketResponsive && (status.ProcessRunning || status.PID == 0)
	switch {
	case status.Running:
		status.Message = "daemon is running"
	case status.PID != 0 && !status.ProcessRunning:
		status.Message = "daemon pid file exists but process is not running"
	default:
		status.Message = "daemon is not running"
	}
	return status, nil
}

func (status LifecycleStatus) JSON() ([]byte, error) {
	return json.MarshalIndent(status, "", "  ")
}

func normalizeLifecycleConfig(config LifecycleConfig) (LifecycleConfig, error) {
	if config.SocketPath == "" {
		config.SocketPath = ".cavra/cavra-runtime.sock"
	}
	if config.PIDPath == "" {
		config.PIDPath = DefaultPIDPath(config.SocketPath)
	}
	if config.StartupTimeout <= 0 {
		config.StartupTimeout = DefaultLifecycleTimeout
	}
	if config.BinaryPath == "" {
		binaryPath, err := os.Executable()
		if err != nil {
			return LifecycleConfig{}, err
		}
		config.BinaryPath = binaryPath
	}
	return config, nil
}

func waitForReady(config LifecycleConfig) error {
	deadline := time.Now().Add(config.StartupTimeout)
	for time.Now().Before(deadline) {
		if socketResponsive(config.SocketPath, 500*time.Millisecond) {
			return nil
		}
		time.Sleep(100 * time.Millisecond)
	}
	return fmt.Errorf("daemon did not become ready before %s", config.StartupTimeout)
}

func socketResponsive(socketPath string, timeout time.Duration) bool {
	client := NewClient(socketPath)
	client.Timeout = timeout
	_, err := client.Evaluate(enforcementv1.EvaluateRequest{
		ActionType:         "execute_command",
		Target:             "terraform plan",
		RequestedOperation: "terraform plan",
	})
	return err == nil
}

func readPID(path string) (int, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return 0, err
	}
	pid, err := strconv.Atoi(strings.TrimSpace(string(data)))
	if err != nil {
		return 0, err
	}
	if pid <= 0 {
		return 0, errors.New("pid must be positive")
	}
	return pid, nil
}

func processRunning(pid int) bool {
	if pid <= 0 {
		return false
	}
	err := syscall.Kill(pid, 0)
	return err == nil || errors.Is(err, syscall.EPERM)
}
