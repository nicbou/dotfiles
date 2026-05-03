#!/bin/bash
PATH_TO_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Install git config
git config --global core.excludesFile "$PATH_TO_SCRIPT_DIR/../configs/.gitignore"

# Install ssh config
cp "$PATH_TO_SCRIPT_DIR/../configs/ssh.conf" ~/.ssh/config
chmod 600 ~/.ssh/config

# Hide the “default interactive shell is now zsh” warning on macOS.
export BASH_SILENCE_DEPRECATION_WARNING=1

# Append to the Bash history file, rather than overwriting it
shopt -s histappend;

# Make nano the default editor
export EDITOR='nano';

# Load local environment variables
ENV_FILE=scripts/env.sh
if [ -f "$ENV_FILE" ]; then
    . $ENV_FILE
fi

# Enable mise
eval "$(${HOMEBREW_PREFIX:-/opt/homebrew}/bin/mise activate bash)"

# Tab-completion for the `project` command (must run after mise puts python3 on PATH)
eval "$(python3 -c 'import argcomplete; print(argcomplete.shellcode(["project"], shell="bash"))' 2>/dev/null)"