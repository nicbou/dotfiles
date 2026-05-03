#!/usr/bin/env python3
"""
Master job scheduler. Runs every hour via cron and dispatches jobs/ files whose
frequency condition is met based on their last-run timestamp.

Last-run timestamps are stored in ~/.local/share/dotfiles-jobs/<job-name>.last_run
"""

import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

JOBS_DIR = Path(__file__).parent.parent / "jobs"
STATE_DIR = Path.home() / ".local" / "share" / "dotfiles-jobs"
LOG_FILE = STATE_DIR / "run-jobs.log"
LOG_MAX_BYTES = 512 * 1024
FREQUENCIES = ["daily", "weekly", "monthly", "yearly"]


def is_due(frequency: str, now, last_run: Optional[datetime]) -> bool:
    if last_run is None:
        return True
    if frequency == "daily":
        return last_run.date() < now.date()
    if frequency == "weekly":
        return last_run.isocalendar()[:2] != now.isocalendar()[:2]
    if frequency == "monthly":
        return (last_run.year, last_run.month) != (now.year, now.month)
    if frequency == "yearly":
        return last_run.year != now.year
    return False


def read_last_run(name: str) -> Optional[datetime]:
    path = STATE_DIR / f"{name}.last_run"
    try:
        return datetime.fromisoformat(path.read_text().strip())
    except (FileNotFoundError, ValueError):
        return None


def write_last_run(name: str, now: datetime):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / f"{name}.last_run").write_text(now.isoformat())


def notify(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], check=False)


def job_name(path):
    name = path.stem
    for freq in FREQUENCIES:
        name = name.removesuffix(f"-{freq}")
    return name


def run_job(path):
    env = {**os.environ, "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"}
    runner = sys.executable if path.suffix == ".py" else "bash"
    return subprocess.run([runner, str(path)], capture_output=True, text=True, env=env)


def setup_logging():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=1)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[handler])


def main():
    setup_logging()
    now = datetime.now()
    for path in sorted(JOBS_DIR.iterdir()):
        if path.name.startswith(".") or not path.is_file():
            continue
        for frequency in FREQUENCIES:
            if f"-{frequency}." in path.name:
                name = job_name(path)
                if not is_due(frequency, now, read_last_run(name)):
                    break
                write_last_run(name, now)
                logging.info("starting %s", name)
                result = run_job(path)
                if result.returncode == 0:
                    logging.info("completed %s", name)
                    notify(name, "Completed")
                else:
                    lines = (result.stderr or result.stdout).strip().splitlines()
                    detail = lines[-1][:100] if lines else f"exit {result.returncode}"
                    logging.error("failed %s: %s", name, detail)
                    notify(name, f"Failed: {detail}")
                break


if __name__ == "__main__":
    main()
