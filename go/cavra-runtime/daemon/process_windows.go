//go:build windows

package daemon

import "syscall"

const processQueryLimitedInformation = 0x1000

func platformProcessRunning(pid int) bool {
	handle, err := syscall.OpenProcess(processQueryLimitedInformation, false, uint32(pid))
	if err == nil {
		_ = syscall.CloseHandle(handle)
		return true
	}
	if errno, ok := err.(syscall.Errno); ok {
		return errno == syscall.ERROR_ACCESS_DENIED
	}
	return false
}
