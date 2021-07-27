#!/bin/bash
PATH_TO_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

alias dcmp=docker-compose
alias project="python3 '$PATH_TO_SCRIPT_DIR/../scripts/project.py'"