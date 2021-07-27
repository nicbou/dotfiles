#!/bin/bash
PATH_TO_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DOTFILES_DIR="$PATH_TO_SCRIPT_DIR/dotfiles"

for DOTFILE in `find $DOTFILES_DIR`
do
  [ -f "$DOTFILE" ] && source "$DOTFILE"
done