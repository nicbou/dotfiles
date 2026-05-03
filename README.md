# Dotfiles

Useful scripts and configs

## Overview

### Nice things

* Sets the PS1 variable (what appears before the commands you type) to something useful.
* Enables terminal colours
* Adds a few useful aliases

### The `project` command

`project [project_name]`

Sets the directory to a specific project. Press tab to autocomplete `[project_name]` See `project -h` for more information.

### The `alert` command

`alert "Hello world"`

Shortcut for displaying a MacOS notification.

## Setup

Add this line to your `~/.bash_profile`:

```
source /path/to/this/repository/activate.sh
```
