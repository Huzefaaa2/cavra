package daemon

import (
	"encoding/json"
	"errors"
	"net"

	enforcementv1 "github.com/Huzefaaa2/cavra/go/cavra-runtime/enforcement/v1"
	cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"
)

type Evaluator func(enforcementv1.EvaluateRequest) enforcementv1.DecisionResponse

func RuntimeEvaluator(policy *cavraruntime.Policy) Evaluator {
	return func(request enforcementv1.EvaluateRequest) enforcementv1.DecisionResponse {
		runtimeRequest := request.RuntimeRequest()
		var decision cavraruntime.Decision
		if policy != nil {
			decision = cavraruntime.EvaluateWithPolicy(runtimeRequest, *policy)
		} else {
			decision = cavraruntime.Evaluate(runtimeRequest)
		}
		return enforcementv1.DecisionResponseFromRuntime(decision)
	}
}

func Serve(listener net.Listener, evaluate Evaluator) error {
	return ServeWithEvidence(listener, evaluate, nil)
}

func ServeWithEvidence(listener net.Listener, evaluate Evaluator, recorder *EvidenceRecorder) error {
	for {
		conn, err := listener.Accept()
		if err != nil {
			if errors.Is(err, net.ErrClosed) {
				return nil
			}
			return err
		}
		go func() {
			_ = HandleConnectionWithEvidence(conn, evaluate, recorder)
		}()
	}
}

func HandleConnection(conn net.Conn, evaluate Evaluator) error {
	return HandleConnectionWithEvidence(conn, evaluate, nil)
}

func HandleConnectionWithEvidence(conn net.Conn, evaluate Evaluator, recorder *EvidenceRecorder) error {
	defer conn.Close()
	var request enforcementv1.EvaluateRequest
	if err := json.NewDecoder(conn).Decode(&request); err != nil {
		return err
	}
	response := evaluate(request)
	var err error
	response, err = recorder.Record(request, response)
	if err != nil {
		return err
	}
	return json.NewEncoder(conn).Encode(response)
}
