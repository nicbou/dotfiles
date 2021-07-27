#!/bin/bash
PATH_TO_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

git config --global core.excludesFile "$PATH_TO_SCRIPT_DIR/../configs/.gitignore"

# Hide the “default interactive shell is now zsh” warning on macOS.
export BASH_SILENCE_DEPRECATION_WARNING=1

# Append to the Bash history file, rather than overwriting it
shopt -s histappend;

# Make nano the default editor
export EDITOR='nano';