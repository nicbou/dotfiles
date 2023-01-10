#!/usr/bin/env python3
import argparse
import os
import time
import sys
import subprocess
from pathlib import Path

PROJECTS_DIR = Path('~/Documents/Projects').expanduser()

parser = argparse.ArgumentParser(description='Switch between projects')

parser.add_argument("project_name", help="The name of the directory containing the project")
parser.add_argument('-S', '--start-all', help="start the project and launch the development environment", action="store_true")
parser.add_argument('-s', '--start', help="start the project", action="store_true")
parser.add_argument('-k', '--kill-others', help="kill other Docker containers before starting the project", action="store_true")
parser.add_argument('-d', '--dev', help="launch the development environment", action="store_true")

args = parser.parse_args()

project_dir = PROJECTS_DIR / args.project_name / 'source'
docker_compose_file = project_dir / "docker-compose.yml"
dev_env_file = project_dir / "scripts/dev-env.sh"

assert project_dir.exists(), f"{project_dir} does not exist"
os.chdir(project_dir)

if args.dev or args.start_all:
    if dev_env_file.exists():
        print("Launching dev environment...")
        subprocess.Popen(
            dev_env_file,
            stdout=sys.stdout,
            stderr=sys.stderr,
        ).wait()
    else:
        error_message = "No suitable way to launch the dev environment"
        if args.start_all:
            print(error_message)
        else:
            raise Exception(error_message)

if args.kill_others or args.start_all:
    print("Stopping all docker instances...")
    subprocess.Popen(
        'docker kill $(docker ps -q)',
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    ).wait()


def is_docker_up():
    return subprocess.Popen(
        'docker stats --no-stream'.split(),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).wait() == 0


if args.start or args.start_all:
    if docker_compose_file.exists():
        if not is_docker_up():
            print("Starting docker", end='', flush=True)
            os.system('open --background -a Docker')
            while not is_docker_up():
                time.sleep(1)
                print(".", end='', flush=True)
            print('')

        print("Starting project...")
        subprocess.Popen(
            'docker compose up --build -d',
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        ).wait()
    else:
        error_message = "No suitable way to start the project"
        if args.start_all:
            print(error_message)
        else:
            raise Exception(error_message)

# We can't change the cwd of the parent shell, so we start another shell in that directory
os.system('bash -l')
