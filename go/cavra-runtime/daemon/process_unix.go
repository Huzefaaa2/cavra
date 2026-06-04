//go:build !windows

package daemon

import (
	"errors"
	"syscall"
)

func platformProcessRunning(pid int) bool {
	err := syscall.Kill(pid, 0)
	return err == nil || errors.Is(err, syscall.EPERM)
}
