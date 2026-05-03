#!/usr/bin/env python3
"""
Daily job: archive Reddit posts and comments to
~/Documents/Artefacts/{year}/Reddit/{subreddit}-{id} - {YYYY-MM-DD}.reddit.md

Idempotent: skips any item whose output file already exists.
Uses Reddit's public JSON API — no credentials required.
"""

import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "n1c0_ds"
OUTPUT_BASE = Path.home() / "Documents" / "Artefacts"
USER_AGENT = "python:personal-archiver:v1.0 (by /u/n1c0_ds)"
SLEEP = 2  # seconds between the two API requests


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def serialize_frontmatter(fields: dict) -> str:
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def fetch_parent_body(parent_id: str) -> str | None:
    url = f"https://www.reddit.com/api/info.json?id={parent_id}"
    try:
        response = fetch_json(url)
        children = response["data"]["children"]
        if children:
            return children[0]["data"]["body"]
    except Exception:
        pass
    return None


def render_markdown(item: dict, parent_body: str | None = None) -> str:
    fields = item["data"]
    created_at = datetime.fromtimestamp(fields["created_utc"], tz=timezone.utc)

    frontmatter = {
        "author": fields["author"],
        "subreddit": f"r/{fields['subreddit']}",
        "id": fields["id"],
        "date": created_at.isoformat(),
        "url": f"https://reddit.com{fields['permalink']}",
    }

    if item["kind"] == "t3":  # post
        frontmatter["type"] = "post"
        frontmatter["title"] = fields["title"]
        body = fields.get("selftext", "")
    else:  # comment (t1)
        frontmatter["type"] = "comment"
        frontmatter["post_title"] = fields["link_title"]
        frontmatter["post_url"] = f"https://reddit.com{fields['link_permalink']}"
        body = fields["body"]
        if parent_body:
            quoted = "\n".join(f"> {line}" for line in parent_body.splitlines())
            body = f"{quoted}\n\n{body}"

    return serialize_frontmatter(frontmatter) + f"\n\n{body}"


def archive_listing(url: str) -> None:
    response = fetch_json(url)
    for item in response["data"]["children"]:
        fields = item["data"]
        created_at = datetime.fromtimestamp(fields["created_utc"], tz=timezone.utc)
        date_str = created_at.strftime("%Y-%m-%dT%H%M")
        filename = f"{date_str} - {fields['subreddit']}-{fields['id']}.reddit.md"
        output_path = OUTPUT_BASE / str(created_at.year) / "Reddit" / filename
        if output_path.exists():
            continue

        parent_body = None
        if item["kind"] == "t1":
            parent_id = fields.get("parent_id", "")
            if parent_id.startswith("t1_"):
                parent_body = fetch_parent_body(parent_id)
                time.sleep(SLEEP)

        markdown = render_markdown(item, parent_body)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")


def main() -> None:
    base_url = f"https://www.reddit.com/user/{USERNAME}"
    archive_listing(f"{base_url}/submitted.json?limit=100")
    time.sleep(SLEEP)
    archive_listing(f"{base_url}/comments.json?limit=100")


if __name__ == "__main__":
    main()
