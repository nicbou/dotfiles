#!/bin/bash

#
# Sets the text that appears before the terminal commands
#

BLACK_TXT="\[\033[38;5;0m\]"
YELLOW_BG="\[\033[48;5;11m\]"
WHITE_TXT="\[\033[0;97m\]"
GRAY_BG="\[\033[48;5;243m\]"
GRAYER_BG="\[\033[48;5;240m\]"
RESET="\[$(tput sgr0)\]"


# Enable terminal colours
LSCOLORS=ExGxBxDxCxEgEdxbxgxcxd
CLICOLORS=1

# Remote machine - red hostname
PS1_REMOTE="${WHITE_TXT}${RED_BG} \u@\h ${WHITE_TXT}${GRAY_BG} ./\W ${GRAYER_BG} \A ${RESET} "

# Trim the length of the current dir in the PS1
# Requires a newer version of bash: https://unix.stackexchange.com/a/726992/60930
export PROMPT_DIRTRIM=3
PS1="${GRAYER_BG} \A ${BLACK_TXT}${YELLOW_BG} ⌂ ${WHITE_TXT}${GRAY_BG} \w ${RESET} "