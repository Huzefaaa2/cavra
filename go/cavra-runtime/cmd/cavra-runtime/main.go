package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"os"

	cavraruntime "github.com/Huzefaaa2/cavra/go/cavra-runtime/runtime"
)

func main() {
	inputPath := flag.String("input", "-", "JSON request file, or - for stdin")
	flag.Parse()

	var reader io.Reader = os.Stdin
	if *inputPath != "-" {
		file, err := os.Open(*inputPath)
		if err != nil {
			fail(err)
		}
		defer file.Close()
		reader = file
	}

	var request cavraruntime.Request
	if err := json.NewDecoder(reader).Decode(&request); err != nil {
		fail(err)
	}
	decision := cavraruntime.Evaluate(request)
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(decision); err != nil {
		fail(err)
	}
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
