# Dotfiles

Useful scripts and configs for my Macbook.

## Overview

### Nice things

* Sets the PS1 variable (what appears before the commands you type) to something useful.
* Enables terminal colours
* Adds a few useful aliases:
    * dcmp for docker-compose
    * proxy for an SSH proxy to my home server

### The `project` command

`project [-h] [-s] [-d] project_name`

Opens a specific project, starting the project and development environment if needed. Call `project -h` for more information.

`-d` will run `./scripts/dev-env.sh` if it exists.

`-s` will start the project if it has a Docker config.

### The `alert` command

`alert "Hello world"`

Shortcut for displaying a MacOS notification.

## Setup

Add this line to your `~/.bash_profile`:

```
source /path/to/this/repository/activate.sh
```
