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

# Local machine - yellow hostname
PS1_LOCAL="${BLACK_TXT}${YELLOW_BG} \u@\h ${WHITE_TXT}${GRAY_BG} ./\W ${GRAYER_BG} \A ${RESET} "

# Remote machine - red hostname
PS1_REMOTE="${WHITE_TXT}${RED_BG} \u@\h ${WHITE_TXT}${GRAY_BG} ./\W ${GRAYER_BG} \A ${RESET} "

PS1="${PS1_LOCAL}"