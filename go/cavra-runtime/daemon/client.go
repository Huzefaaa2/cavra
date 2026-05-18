package daemon

import (
	"encoding/json"
	"errors"
	"net"
	"time"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
)

const DefaultClientTimeout = 5 * time.Second

type Client struct {
	SocketPath string
	Timeout    time.Duration
}

func NewClient(socketPath string) Client {
	return Client{
		SocketPath: socketPath,
		Timeout:    DefaultClientTimeout,
	}
}

func (client Client) Evaluate(request enforcementv1.EvaluateRequest) (enforcementv1.DecisionResponse, error) {
	if client.SocketPath == "" {
		return enforcementv1.DecisionResponse{}, errors.New("daemon socket path is required")
	}
	timeout := client.Timeout
	if timeout <= 0 {
		timeout = DefaultClientTimeout
	}
	conn, err := net.DialTimeout("unix", client.SocketPath, timeout)
	if err != nil {
		return enforcementv1.DecisionResponse{}, err
	}
	defer conn.Close()
	if err := conn.SetDeadline(time.Now().Add(timeout)); err != nil {
		return enforcementv1.DecisionResponse{}, err
	}
	if err := json.NewEncoder(conn).Encode(request); err != nil {
		return enforcementv1.DecisionResponse{}, err
	}
	var response enforcementv1.DecisionResponse
	if err := json.NewDecoder(conn).Decode(&response); err != nil {
		return enforcementv1.DecisionResponse{}, err
	}
	return response, nil
}
