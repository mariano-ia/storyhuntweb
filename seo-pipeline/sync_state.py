#!/usr/bin/env python3
"""
Sync config.json state with files actually on disk.
Marks pages as 'published' if their HTML file exists in /explore/.
"""
import json
import os
from datetime import datetime, timezone

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.dirname(PIPELINE_DIR)
EXPLORE_DIR = os.path.join(WEB_DIR, "explore")
CONFIG_PATH = os.path.join(PIPELINE_DIR, "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

synced = 0
for page in config["pages"]:
    html_path = os.path.join(EXPLORE_DIR, f"{page['slug']}.html")
    if os.path.exists(html_path) and page["status"] != "published":
        page["status"] = "published"
        page.setdefault("generated_at", datetime.now(timezone.utc).isoformat())
        synced += 1
        print(f"  [SYNC] Marked as published: {page['slug']}")

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

published = sum(1 for p in config["pages"] if p["status"] == "published")
pending = sum(1 for p in config["pages"] if p["status"] == "pending")
print(f"\nDone. Synced {synced} pages. Total: {published} published, {pending} pending.")
