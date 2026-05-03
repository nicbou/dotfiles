#!/usr/bin/env python3
from pathlib import Path
import argparse
import os

PROJECTS_DIR = Path("~/Documents/Projects").expanduser()

parser = argparse.ArgumentParser(description="Switch between projects")

parser.add_argument(
    "project_name", help="The name of the directory containing the project"
)

parser.add_argument(
    "subdir",
    type=Path,
    nargs="?",
    help="move into the specified subdirectory of the project",
)

args = parser.parse_args()

project_dir = PROJECTS_DIR / args.project_name / "source"
if not project_dir.exists():
    project_dir = project_dir.parent


assert project_dir.exists(), f"{project_dir} does not exist"
if args.subdir:
    os.chdir(project_dir / args.subdir)
else:
    os.chdir(project_dir)


# Set iTerm tab title
print(f"\033]0;{args.project_name}\007")

# We can't change the cwd of the parent shell, so we start another shell in that directory
os.system("bash -l;")
