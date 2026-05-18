package daemon

import (
	"net"
	"os"
	"path/filepath"
	"strconv"
	"testing"
	"time"
)

func TestDefaultPIDPathUsesSocketPath(t *testing.T) {
	if got := DefaultPIDPath("/tmp/cavra.sock"); got != "/tmp/cavra.sock.pid" {
		t.Fatalf("pid path mismatch: got %q", got)
	}
	if got := DefaultPIDPath(""); got != ".cavra/cavra-runtime.pid" {
		t.Fatalf("default pid path mismatch: got %q", got)
	}
}

func TestStatusDaemonUsesPIDFileAndSocketProbe(t *testing.T) {
	socketPath := filepath.Join(t.TempDir(), "cavra-runtime.sock")
	pidPath := socketPath + ".pid"
	if err := os.WriteFile(pidPath, []byte(strconv.Itoa(os.Getpid())+"\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	listener, err := net.Listen("unix", socketPath)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	go func() {
		_ = Serve(listener, RuntimeEvaluator(nil))
	}()

	status, err := StatusDaemon(LifecycleConfig{
		SocketPath:     socketPath,
		PIDPath:        pidPath,
		StartupTimeout: time.Second,
	})
	if err != nil {
		t.Fatal(err)
	}
	if !status.Running {
		t.Fatalf("expected daemon to be running: %+v", status)
	}
	if !status.ProcessRunning {
		t.Fatalf("expected process to be running: %+v", status)
	}
	if !status.SocketResponsive {
		t.Fatalf("expected socket to be responsive: %+v", status)
	}
}

func TestStatusDaemonReportsStoppedWithoutPID(t *testing.T) {
	socketPath := filepath.Join(t.TempDir(), "missing.sock")
	status, err := StatusDaemon(LifecycleConfig{
		SocketPath:     socketPath,
		StartupTimeout: 10 * time.Millisecond,
	})
	if err != nil {
		t.Fatal(err)
	}
	if status.Running {
		t.Fatalf("expected daemon to be stopped: %+v", status)
	}
	if status.Message != "daemon is not running" {
		t.Fatalf("message mismatch: got %q", status.Message)
	}
}
