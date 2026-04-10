#!/usr/bin/env python3
"""Generate config.json with all 94 page definitions."""
import json
import os

ACTIVITIES = {
    "scavenger-hunt": {"display": "Scavenger Hunt", "keyword": "scavenger hunt"},
    "mystery-walk": {"display": "Mystery Walk", "keyword": "mystery walk"},
    "walking-tour": {"display": "Walking Tour", "keyword": "walking tour"},
    "date-ideas": {"display": "Date Ideas", "keyword": "date ideas"},
    "team-building": {"display": "Team Building", "keyword": "team building"},
    "outdoor-escape-room": {"display": "Outdoor Escape Room", "keyword": "outdoor escape room"},
}

NEIGHBORHOODS = {
    "soho": "SoHo",
    "west-village": "West Village",
    "greenwich-village": "Greenwich Village",
    "chelsea": "Chelsea",
    "dumbo": "DUMBO",
    "central-park": "Central Park",
    "williamsburg": "Williamsburg",
    "harlem": "Harlem",
    "midtown": "Midtown",
    "tribeca": "TriBeCa",
}

AUDIENCES = {
    "couples": "Couples",
    "tourists": "Tourists",
    "families": "Families",
    "groups": "Groups",
}

# Template C broad pages
BROAD_PAGES = [
    ("scavenger-hunt-nyc", "Scavenger Hunt", "Scavenger Hunt NYC"),
    ("mystery-walk-nyc", "Mystery Walk", "Mystery Walk NYC"),
    ("walking-tour-nyc", "Walking Tour", "Walking Tour NYC"),
    ("outdoor-escape-room-nyc", "Outdoor Escape Room", "Outdoor Escape Room NYC"),
    ("team-building-activities-nyc", "Team Building Activities", "Team Building Activities NYC"),
    ("bachelorette-party-nyc", "Bachelorette Party", "Bachelorette Party NYC"),
    ("birthday-ideas-nyc", "Birthday Ideas", "Birthday Ideas NYC"),
    ("corporate-events-nyc", "Corporate Events", "Corporate Events NYC"),
    ("things-to-do-nyc", "Things to Do", "Things to Do NYC"),
    ("fun-activities-nyc", "Fun Activities", "Fun Activities NYC"),
]

# Existing page slugs (to check for conflicts and build related links)
EXISTING_EXPLORE = [
    "soho", "chelsea", "midtown", "central-park", "west-village", "tribeca",
    "flatiron", "dumbo", "williamsburg", "harlem", "bushwick", "times-square",
    "greenwich-village", "bryant-park", "high-line", "upper-east-side", "grand-central",
    "hidden-places-nyc", "secret-spots-nyc", "urban-legends-nyc", "mysteries-in-nyc",
    "weird-places-nyc", "true-crime-tours-nyc", "haunted-places-nyc", "ghost-tours-nyc",
    "speakeasies-nyc", "mob-history-nyc", "abandoned-places-nyc", "movie-locations-nyc",
    "literary-tours-nyc", "architectural-marvels-nyc", "underground-tunnels-nyc",
    "haunted-places-greenwich-village", "true-crime-lower-east-side",
    "hidden-speakeasies-soho", "secret-gardens-central-park", "mob-history-little-italy",
    "ghosts-of-broadway", "abandoned-stations-nyc-subway", "weird-history-williamsburg",
    "literary-secrets-west-village", "hidden-art-dumbo",
]

# Map activities to related existing topic pages
ACTIVITY_TOPIC_MAP = {
    "scavenger-hunt": ["hidden-places-nyc", "secret-spots-nyc"],
    "mystery-walk": ["mysteries-in-nyc", "urban-legends-nyc"],
    "walking-tour": ["architectural-marvels-nyc", "movie-locations-nyc"],
    "date-ideas": ["speakeasies-nyc", "hidden-places-nyc"],
    "team-building": ["hidden-places-nyc", "secret-spots-nyc"],
    "outdoor-escape-room": ["mysteries-in-nyc", "underground-tunnels-nyc"],
}


def make_related_a(activity, neighborhood, all_slugs):
    """Related links for Template A pages."""
    related = []
    # 1. Existing neighborhood page
    if neighborhood in EXISTING_EXPLORE:
        related.append(neighborhood)
    # 2. Broad activity page
    broad = f"{activity}-nyc"
    if broad in all_slugs:
        related.append(broad)
    # 3. Different activity in same neighborhood
    other_activities = [a for a in ACTIVITIES if a != activity]
    for oa in other_activities[:1]:
        other_slug = f"{oa}-in-{neighborhood}"
        if other_slug in all_slugs:
            related.append(other_slug)
    # Fallback to topic pages
    if len(related) < 3:
        for topic in ACTIVITY_TOPIC_MAP.get(activity, []):
            if topic not in related:
                related.append(topic)
            if len(related) >= 3:
                break
    return related[:3]


def make_related_b(activity, audience, all_slugs):
    """Related links for Template B pages."""
    related = []
    # 1. Broad activity page
    broad = f"{activity}-nyc"
    if broad in all_slugs:
        related.append(broad)
    # 2. Same activity, different audience
    other_audiences = [a for a in AUDIENCES if a != audience]
    for oa in other_audiences[:1]:
        slug = f"{activity}-for-{oa}"
        if slug in all_slugs:
            related.append(slug)
    # 3. Template A page in popular neighborhood
    for nb in ["soho", "west-village", "greenwich-village"]:
        slug = f"{activity}-in-{nb}"
        if slug in all_slugs and slug not in related:
            related.append(slug)
            break
    # Fallback
    if len(related) < 3:
        for topic in ACTIVITY_TOPIC_MAP.get(activity, []):
            if topic not in related:
                related.append(topic)
            if len(related) >= 3:
                break
    return related[:3]


def make_related_c(slug, all_slugs):
    """Related links for Template C pages."""
    related = []
    # Find the base activity
    base_activity = None
    for act in ACTIVITIES:
        if slug.startswith(act):
            base_activity = act
            break
    # 1-2. Template A pages in top neighborhoods
    if base_activity:
        for nb in ["soho", "west-village", "central-park"]:
            candidate = f"{base_activity}-in-{nb}"
            if candidate in all_slugs:
                related.append(candidate)
            if len(related) >= 2:
                break
    # 3. Related existing topic
    if base_activity and base_activity in ACTIVITY_TOPIC_MAP:
        for topic in ACTIVITY_TOPIC_MAP[base_activity]:
            if topic not in related:
                related.append(topic)
                break
    # Fallback
    if len(related) < 3:
        for fallback in ["hidden-places-nyc", "mysteries-in-nyc", "secret-spots-nyc"]:
            if fallback not in related:
                related.append(fallback)
            if len(related) >= 3:
                break
    return related[:3]


def build_config():
    pages = []
    all_slugs = set()

    # Pre-compute all slugs for related link resolution
    for act in ACTIVITIES:
        for nb in NEIGHBORHOODS:
            all_slugs.add(f"{act}-in-{nb}")
        for aud in AUDIENCES:
            all_slugs.add(f"{act}-for-{aud}")
    for slug, _, _ in BROAD_PAGES:
        all_slugs.add(slug)

    # Template A: activity-in-neighborhood (60 pages)
    for act_slug, act_data in ACTIVITIES.items():
        for nb_slug, nb_display in NEIGHBORHOODS.items():
            slug = f"{act_slug}-in-{nb_slug}"
            act_display = act_data["display"]
            keyword = act_data["keyword"]

            pages.append({
                "slug": slug,
                "template": "A",
                "activity": act_slug,
                "neighborhood": nb_slug,
                "audience": None,
                "title": f"{act_display} in {nb_display} NYC | StoryHunt",
                "h1": f"{act_display} in {nb_display}.",
                "meta_desc": f"Explore {nb_display} on an interactive {keyword.lower()} through NYC. Solve clues, uncover hidden history, and decode the neighborhood. No guide needed — book your mission now.",
                "keywords": f"{keyword} {nb_display}, {nb_display} {keyword} NYC, StoryHunt {nb_display}, interactive {keyword} NYC",
                "og_title": f"{act_display} in {nb_display} — Interactive NYC Adventure | StoryHunt",
                "btn_text": f"START_THE_HUNT_IN_{nb_display.upper().replace(' ', '_')}",
                "footer_location": f"LOCATION: {nb_display.upper().replace(' ', '_')}_NYC",
                "footer_status": f"STATUS: {act_display.upper().replace(' ', '_')}_ACTIVE",
                "related_slugs": make_related_a(act_slug, nb_slug, all_slugs),
                "status": "pending",
            })

    # Template B: activity-for-audience (24 pages)
    for act_slug, act_data in ACTIVITIES.items():
        for aud_slug, aud_display in AUDIENCES.items():
            slug = f"{act_slug}-for-{aud_slug}"
            act_display = act_data["display"]
            keyword = act_data["keyword"]

            pages.append({
                "slug": slug,
                "template": "B",
                "activity": act_slug,
                "neighborhood": None,
                "audience": aud_slug,
                "title": f"{act_display} for {aud_display} in NYC | StoryHunt",
                "h1": f"{act_display} for {aud_display}.",
                "meta_desc": f"The perfect {keyword.lower()} for {aud_display.lower()} in NYC. Interactive mystery walk with phone-guided clues through hidden streets. No guide needed — book now.",
                "keywords": f"{keyword} for {aud_display.lower()} NYC, NYC {keyword} {aud_display.lower()}, StoryHunt {aud_display.lower()}, interactive adventure {aud_display.lower()}",
                "og_title": f"{act_display} for {aud_display} — NYC Interactive Adventure | StoryHunt",
                "btn_text": f"START_THE_HUNT",
                "footer_location": "LOCATION: NEW_YORK_CITY",
                "footer_status": f"STATUS: {act_display.upper().replace(' ', '_')}_ACTIVE",
                "related_slugs": make_related_b(act_slug, aud_slug, all_slugs),
                "status": "pending",
            })

    # Template C: broad activity-nyc (10 pages)
    for slug, act_display, page_title in BROAD_PAGES:
        # Skip if conflicts with existing page
        if slug in EXISTING_EXPLORE:
            print(f"  [SKIP] {slug} conflicts with existing page")
            continue

        keyword = slug.replace("-", " ")
        pages.append({
            "slug": slug,
            "template": "C",
            "activity": slug.replace("-nyc", "").replace("-activities", "").replace("-ideas", "").replace("-events", ""),
            "neighborhood": None,
            "audience": None,
            "title": f"{page_title} — Interactive Mystery Walk | StoryHunt",
            "h1": f"{page_title}.",
            "meta_desc": f"Discover the best {keyword.lower()} — interactive mystery walks through NYC's hidden streets. Solve clues, explore history, decode the city. No guide needed. Book now.",
            "keywords": f"{keyword}, best {keyword}, {keyword} interactive, StoryHunt NYC, mystery walk NYC",
            "og_title": f"{page_title} — Interactive Adventure | StoryHunt",
            "btn_text": "START_THE_HUNT_IN_NYC",
            "footer_location": "LOCATION: NEW_YORK_CITY",
            "footer_status": f"STATUS: MISSIONS_ACTIVE",
            "related_slugs": make_related_c(slug, all_slugs),
            "status": "pending",
        })

    config = {
        "base_url": "https://storyhunt.city",
        "neighborhoods": {k: v for k, v in NEIGHBORHOODS.items()},
        "activities": {k: v["display"] for k, v in ACTIVITIES.items()},
        "audiences": {k: v for k, v in AUDIENCES.items()},
        "pages": pages,
    }

    return config


if __name__ == "__main__":
    config = build_config()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"Generated config.json with {len(config['pages'])} pages:")
    templates = {}
    for p in config["pages"]:
        templates[p["template"]] = templates.get(p["template"], 0) + 1
    for t, count in sorted(templates.items()):
        print(f"  Template {t}: {count} pages")
