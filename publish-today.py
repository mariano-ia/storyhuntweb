#!/usr/bin/env python3
"""
Publish today's Instagram post from social-calendar.json.
Run manually or as a daily cron job on macOS.

Usage:
    python3 publish-today.py          # publish today's post
    python3 publish-today.py --dry    # preview without publishing
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import ssl
import certifi
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_FILE = os.path.join(BASE_DIR, "social-calendar.json")
CTX = ssl.create_default_context(cafile=certifi.where())

# Instagram credentials
IG_ACCOUNT_ID = "17841444079999050"
ACCESS_TOKEN = "EAF0g8yRDv6IBRJ0zMeO96WxAFuSm2rn4kCsvu7nGTllPpqy3HUs5MWOUmFfn3ZAw32cN2kI6hoPNbDJN21BV9gzkv0ZCmEpZB7mVLeciVU1slBywNSDaoR1dq1qBVsVMfWu0FTEEiEsgWyX7GR58gVySNp5AoMU2ZCnL4AfTl3VKYwdazyYzwZCWYFFGi"
GITHUB_RAW = "https://raw.githubusercontent.com/mariano-ia/storyhuntweb/main"

# Caption templates by content_type
CAPTION_TEMPLATES = {
    "MYSTERY_TEASER": """SIGNAL_INTERCEPTED // {location}

{topic}

This is StoryHunt. A chat-based mystery walk through NYC. No guide. No bus. Just you, your phone, and the city.

Your phone sends clues. You follow them through real streets. You solve puzzles. You decode the city.

FREE EARLY ACCESS → storyhunt.city

#NYC #StoryHunt #HiddenNYC #NYCSecrets #MysteryWalk #InteractiveAdventure #ScavengerHunt #UrbanExploration #DecodeTheCity #NYCAdventure #NYCHiddenGems #ExploreNYC #ThingsToDoNYC #NYCExperience #UrbanMystery""",

    "DID_YOU_KNOW": """DATA_DECLASSIFIED // NYC_ARCHIVES

{topic}

StoryHunt takes you to the places most people walk past without knowing. A chat-based mystery walk. Your phone is the guide.

FREE EARLY ACCESS → storyhunt.city

#NYC #StoryHunt #HiddenNYC #NYCSecrets #DidYouKnow #NYCHistory #UrbanExploration #MysteryWalk #DecodeTheCity #NYCFacts #InteractiveAdventure #ScavengerHunt #ExploreNYC #NYCAdventure""",

    "NEIGHBORHOOD_SPOTLIGHT": """ZONE_SCAN_ACTIVE // {location}

{topic}

StoryHunt walks you through it — guided by chat clues sent to your phone. No guide. No bus. Just you and the streets.

FREE EARLY ACCESS → storyhunt.city

#NYC #StoryHunt #HiddenNYC #NYCSecrets #UrbanExploration #MysteryWalk #DecodeTheCity #NYCAdventure #InteractiveAdventure #ScavengerHunt #ExploreNYC #NYCNeighborhoods #NYCHiddenGems #ThingsToDoNYC""",

    "BEHIND_THE_HUNT": """TRANSMISSION_ACTIVE // FIELD_REPORT

{topic}

This is what StoryHunt feels like. A chat-based mystery walk through NYC. Your phone sends clues. You follow them. The city becomes the game.

FREE EARLY ACCESS → storyhunt.city

#NYC #StoryHunt #HiddenNYC #MysteryWalk #InteractiveAdventure #ScavengerHunt #UrbanExploration #DecodeTheCity #NYCAdventure #NYCExperience #ImmersiveExperience #NYCSecrets #ExploreNYC""",

    "QUOTE": """FIELD_NOTE // NYC_DISPATCH

{topic}

StoryHunt. A chat-based mystery walk through NYC. Coming soon.

→ storyhunt.city

#NYC #StoryHunt #DecodeTheCity #MysteryWalk #InteractiveAdventure #NYCSecrets #UrbanExploration #ScavengerHunt #NYCAdventure #HiddenNYC #NYCQuotes #CityLife #ExploreNYC""",
}


def ig_post(endpoint, data):
    """POST to Instagram Graph API."""
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        f"https://graph.facebook.com/v25.0/{endpoint}",
        data=encoded,
        method="POST"
    )
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read())


def build_caption(post):
    """Build caption from template."""
    template = CAPTION_TEMPLATES.get(post["content_type"], CAPTION_TEMPLATES["MYSTERY_TEASER"])
    return template.format(
        topic=post["topic"],
        location=post.get("location", "NYC").replace("// ", ""),
    )


def main():
    dry_run = "--dry" in sys.argv
    today = date.today().isoformat()

    with open(CALENDAR_FILE) as f:
        calendar = json.load(f)

    # Find today's post or next pending
    post = None
    post_idx = None
    for i, p in enumerate(calendar["posts"]):
        if p["status"] == "pending":
            if p["date"] == today:
                post = p
                post_idx = i
                break
            elif p["date"] <= today:
                post = p
                post_idx = i
                break

    if not post:
        print(f"No pending post for {today}. Nothing to do.")
        return

    image_url = f"{GITHUB_RAW}/{post['image_file']}"
    caption = build_caption(post)

    print(f"{'='*50}")
    print(f"Date:    {post['date']}")
    print(f"Type:    {post['content_type']}")
    print(f"Image:   {post['image_file']}")
    print(f"Caption: {caption[:100]}...")
    print(f"{'='*50}")

    if dry_run:
        print("\n[DRY RUN] Would publish the above. Run without --dry to publish.")
        return

    # Step 1: Create media container
    print("\nCreating media container...")
    result = ig_post(f"{IG_ACCOUNT_ID}/media", {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN,
    })
    creation_id = result.get("id")
    if not creation_id:
        print(f"FAIL: {result}")
        return

    print(f"Container: {creation_id}")

    # Step 2: Wait and publish
    print("Waiting 15s for processing...")
    time.sleep(15)

    print("Publishing...")
    result = ig_post(f"{IG_ACCOUNT_ID}/media_publish", {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    })
    post_id = result.get("id")
    if not post_id:
        print(f"FAIL: {result}")
        return

    print(f"PUBLISHED! Post ID: {post_id}")

    # Step 3: Update calendar
    calendar["posts"][post_idx]["status"] = "published"
    calendar["posts"][post_idx]["published_date"] = today
    calendar["posts"][post_idx]["post_id"] = post_id

    with open(CALENDAR_FILE, "w") as f:
        json.dump(calendar, f, indent=2)

    print(f"Calendar updated. Done.")


if __name__ == "__main__":
    main()
