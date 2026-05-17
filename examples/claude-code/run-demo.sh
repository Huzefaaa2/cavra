#!/usr/bin/env sh
set -eu
cavra evaluate read_file .env
cavra evaluate execute_command "terraform plan"
cavra evaluate execute_command "terraform apply -auto-approve"
cavra-mcp-server --list-tools
