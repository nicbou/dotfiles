# Dotfiles

Useful scripts and configs for my Macbook.

## Overview

### Nice things

* Sets the PS1 variable (what appears before the commands you type) to something useful.
* Enables terminal colours
* Adds a few useful aliases

### The `project` command

`project [-h] [-s] [-d] project_name`

Opens a specific project, starting the project and development environment if needed. Call `project -h` for more information.

`-d` will run `./scripts/dev-env.sh` if it exists. This is meant to start the dev environment (text editor, IDE, etc.)

`-s` starts the project if it has a `docker-compose.yml` file.

`-k` will kill other running Docker containers before starting the project.

`-S` is the same as `-sdk`.

### The `alert` command

`alert "Hello world"`

Shortcut for displaying a MacOS notification.

## Setup

Add this line to your `~/.bash_profile`:

```
source /path/to/this/repository/activate.sh
```
