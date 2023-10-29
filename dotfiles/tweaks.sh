#!/bin/bash
PATH_TO_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Install git config
git config --global core.excludesFile "$PATH_TO_SCRIPT_DIR/../configs/.gitignore"

# Install ssh config
cp "$PATH_TO_SCRIPT_DIR/../configs/ssh.conf" ~/.ssh/config
chmod 600 ~/.ssh/config

# Hide the “default interactive shell is now zsh” warning on macOS.
export BASH_SILENCE_DEPRECATION_WARNING=1

# Build Mac M1 docker images by default
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Append to the Bash history file, rather than overwriting it
shopt -s histappend;

# Make nano the default editor
export EDITOR='nano';

# Load local environment variables
ENV_FILE=scripts/env.sh
if [ -f "$ENV_FILE" ]; then
    . $ENV_FILE
fi
