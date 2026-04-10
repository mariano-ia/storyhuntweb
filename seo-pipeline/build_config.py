#!/usr/bin/env python3
"""
Generate config.json with all page definitions.
Idempotent: preserves existing published pages, only adds new pending ones.
"""
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

# Phase 1 neighborhoods (already generated)
NEIGHBORHOODS_PHASE1 = {
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

# Phase 2 neighborhoods (new)
NEIGHBORHOODS_PHASE2 = {
    "lower-east-side": "Lower East Side",
    "east-village": "East Village",
    "upper-west-side": "Upper West Side",
    "flatiron": "Flatiron",
    "financial-district": "Financial District",
    "hells-kitchen": "Hell's Kitchen",
    "chinatown": "Chinatown",
    "little-italy": "Little Italy",
    "nolita": "NoLIta",
    "meatpacking-district": "Meatpacking District",
    "brooklyn-heights": "Brooklyn Heights",
    "bushwick": "Bushwick",
    "times-square": "Times Square",
    "high-line": "High Line",
    "bryant-park": "Bryant Park",
    "grand-central": "Grand Central",
}

# All neighborhoods combined
NEIGHBORHOODS = {**NEIGHBORHOODS_PHASE1, **NEIGHBORHOODS_PHASE2}

AUDIENCES = {
    "couples": "Couples",
    "tourists": "Tourists",
    "families": "Families",
    "groups": "Groups",
    "solo-travelers": "Solo Travelers",
    "friends": "Friends",
    "adults": "Adults",
    "coworkers": "Coworkers",
    "kids": "Kids",
}

# Temporal/seasonal modifiers (Template D)
TEMPORALS = {
    "this-weekend": "This Weekend",
    "tonight": "Tonight",
    "today": "Today",
    "winter": "Winter",
    "summer": "Summer",
    "spring": "Spring",
    "fall": "Fall",
    "rainy-day": "Rainy Day",
    "valentines-day": "Valentine's Day",
    "halloween": "Halloween",
    "christmas": "Christmas",
    "new-years-eve": "New Year's Eve",
}

# Theme × Activity combinations (Template E)
THEMES = {
    "haunted": "Haunted",
    "true-crime": "True Crime",
    "history": "History",
    "art": "Art",
    "food": "Food",
    "speakeasy": "Speakeasy",
    "architecture": "Architecture",
    "literary": "Literary",
    "street-art": "Street Art",
    "underground": "Underground",
    "prohibition": "Prohibition",
    "ghost": "Ghost",
    "noir": "Noir",
    "music": "Music",
}

# Comparatives (Template F)
COMPARATIVES = [
    ("storyhunt-vs-escape-room-nyc", "StoryHunt vs Escape Room NYC", "StoryHunt vs Escape Room"),
    ("mystery-walk-vs-walking-tour-nyc", "Mystery Walk vs Walking Tour NYC", "Mystery Walk vs Walking Tour"),
    ("outdoor-escape-room-vs-bar-crawl-nyc", "Outdoor Escape Room vs Bar Crawl NYC", "Outdoor Escape Room vs Bar Crawl"),
    ("interactive-walk-vs-museum-nyc", "Interactive Walk vs Museum NYC", "Interactive Walk vs Museum"),
    ("scavenger-hunt-vs-pub-crawl-nyc", "Scavenger Hunt vs Pub Crawl NYC", "Scavenger Hunt vs Pub Crawl"),
    ("mystery-walk-vs-escape-room-nyc", "Mystery Walk vs Escape Room NYC", "Mystery Walk vs Escape Room"),
    ("storyhunt-vs-walking-tour-nyc", "StoryHunt vs Walking Tour NYC", "StoryHunt vs Walking Tour"),
    ("interactive-adventure-vs-dinner-date-nyc", "Interactive Adventure vs Dinner Date NYC", "Interactive Adventure vs Dinner Date"),
    ("scavenger-hunt-vs-ghost-tour-nyc", "Scavenger Hunt vs Ghost Tour NYC", "Scavenger Hunt vs Ghost Tour"),
    ("outdoor-adventure-vs-broadway-show-nyc", "Outdoor Adventure vs Broadway Show NYC", "Outdoor Adventure vs Broadway Show"),
]

# Best-of pages (Template G): "best {theme} in {neighborhood}"
BEST_OF_COMBOS = [
    ("best-hidden-places-soho", "Best Hidden Places in SoHo", "hidden-places-nyc", "soho"),
    ("best-speakeasies-greenwich-village", "Best Speakeasies in Greenwich Village", "speakeasies-nyc", "greenwich-village"),
    ("best-haunted-spots-west-village", "Best Haunted Spots in West Village", "haunted-places-nyc", "west-village"),
    ("best-street-art-bushwick", "Best Street Art in Bushwick", "hidden-art-dumbo", "bushwick"),
    ("best-hidden-spots-central-park", "Best Hidden Spots in Central Park", "secret-gardens-central-park", "central-park"),
    ("best-history-walks-harlem", "Best History Walks in Harlem", "architectural-marvels-nyc", "harlem"),
    ("best-food-spots-chinatown", "Best Food Spots in Chinatown", "hidden-places-nyc", "chinatown"),
    ("best-art-galleries-chelsea", "Best Art Galleries in Chelsea", "hidden-art-dumbo", "chelsea"),
    ("best-crime-history-lower-east-side", "Best Crime History Lower East Side", "true-crime-lower-east-side", "lower-east-side"),
    ("best-nightlife-east-village", "Best Nightlife in East Village", "speakeasies-nyc", "east-village"),
    ("best-literary-spots-west-village", "Best Literary Spots in West Village", "literary-secrets-west-village", "west-village"),
    ("best-architecture-midtown", "Best Architecture in Midtown", "architectural-marvels-nyc", "midtown"),
    ("best-views-dumbo", "Best Views in DUMBO", "hidden-art-dumbo", "dumbo"),
    ("best-music-venues-williamsburg", "Best Music Venues in Williamsburg", "weird-history-williamsburg", "williamsburg"),
    ("best-mob-spots-little-italy", "Best Mob Spots in Little Italy", "mob-history-little-italy", "little-italy"),
    ("best-underground-spots-nyc", "Best Underground Spots in NYC", "underground-tunnels-nyc", None),
    ("best-date-spots-nyc", "Best Date Spots in NYC", "speakeasies-nyc", None),
    ("best-secret-spots-brooklyn", "Best Secret Spots in Brooklyn", "secret-spots-nyc", "dumbo"),
    ("best-weird-places-nyc", "Best Weird Places in NYC", "weird-places-nyc", None),
    ("best-ghost-stories-nyc", "Best Ghost Stories in NYC", "haunted-places-nyc", None),
]

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
    ("night-activities-nyc", "Night Activities", "Night Activities NYC"),
    ("unique-experiences-nyc", "Unique Experiences", "Unique Experiences NYC"),
    ("adventure-activities-nyc", "Adventure Activities", "Adventure Activities NYC"),
    ("romantic-things-to-do-nyc", "Romantic Things to Do", "Romantic Things to Do NYC"),
    ("cheap-things-to-do-nyc", "Cheap Things to Do", "Cheap Things to Do NYC"),
    ("free-things-to-do-nyc", "Free Things to Do", "Free Things to Do NYC"),
    ("unusual-things-to-do-nyc", "Unusual Things to Do", "Unusual Things to Do NYC"),
    ("outdoor-activities-nyc", "Outdoor Activities", "Outdoor Activities NYC"),
    ("rainy-day-activities-nyc", "Rainy Day Activities", "Rainy Day Activities NYC"),
    ("group-activities-nyc", "Group Activities", "Group Activities NYC"),
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

    # Template D: activity-nyc-{temporal} (seasonal/moment pages)
    TEMPORAL_ACTIVITIES = ["scavenger-hunt", "mystery-walk", "date-ideas", "things-to-do", "walking-tour"]
    for temp_slug, temp_display in TEMPORALS.items():
        for act_slug in TEMPORAL_ACTIVITIES:
            act_display = ACTIVITIES.get(act_slug, {"display": act_slug.replace("-", " ").title()})
            if isinstance(act_display, dict):
                act_display = act_display["display"]
            slug = f"{act_slug}-nyc-{temp_slug}"
            keyword = f"{act_display.lower()} nyc {temp_display.lower()}"
            pages.append({
                "slug": slug,
                "template": "D",
                "activity": act_slug,
                "neighborhood": None,
                "audience": None,
                "temporal": temp_slug,
                "title": f"{act_display} NYC {temp_display} | StoryHunt",
                "h1": f"{act_display} NYC — {temp_display}.",
                "meta_desc": f"Looking for a {act_display.lower()} in NYC {temp_display.lower()}? StoryHunt offers interactive mystery walks through hidden streets. Solve clues, explore history. No guide needed.",
                "keywords": f"{keyword}, {act_display.lower()} {temp_display.lower()} NYC, StoryHunt NYC, interactive adventure NYC {temp_display.lower()}",
                "og_title": f"{act_display} NYC {temp_display} — Interactive Adventure | StoryHunt",
                "btn_text": "START_THE_HUNT_NOW",
                "footer_location": "LOCATION: NEW_YORK_CITY",
                "footer_status": f"STATUS: MISSIONS_ACTIVE",
                "related_slugs": [f"{act_slug}-nyc"] if f"{act_slug}-nyc" in all_slugs else ["things-to-do-nyc", "mystery-walk-nyc"],
                "status": "pending",
            })

    # Template E: {theme}-{activity}-nyc (theme × activity combos)
    THEME_ACTIVITIES = ["walking-tour", "scavenger-hunt", "mystery-walk"]
    for theme_slug, theme_display in THEMES.items():
        for act_slug in THEME_ACTIVITIES:
            act_display = ACTIVITIES[act_slug]["display"]
            slug = f"{theme_slug}-{act_slug}-nyc"
            keyword = f"{theme_display.lower()} {act_display.lower()} nyc"
            pages.append({
                "slug": slug,
                "template": "E",
                "activity": act_slug,
                "neighborhood": None,
                "audience": None,
                "theme": theme_slug,
                "title": f"{theme_display} {act_display} NYC | StoryHunt",
                "h1": f"{theme_display} {act_display} in NYC.",
                "meta_desc": f"Explore NYC's {theme_display.lower()} side on an interactive {act_display.lower()}. Solve clues, uncover dark history, and decode the city. No guide needed — book your mission.",
                "keywords": f"{keyword}, {theme_display.lower()} {act_display.lower()} New York, StoryHunt {theme_display.lower()}, interactive {theme_display.lower()} tour NYC",
                "og_title": f"{theme_display} {act_display} NYC — Interactive Adventure | StoryHunt",
                "btn_text": "START_THE_HUNT",
                "footer_location": "LOCATION: NEW_YORK_CITY",
                "footer_status": f"STATUS: {theme_display.upper().replace(' ', '_')}_MISSION_ACTIVE",
                "related_slugs": ACTIVITY_TOPIC_MAP.get(act_slug, ["hidden-places-nyc", "mysteries-in-nyc"])[:2] + [f"{act_slug}-nyc"],
                "status": "pending",
            })

    # Template F: comparatives (vs pages)
    for slug, page_title, display_title in COMPARATIVES:
        if slug in EXISTING_EXPLORE:
            continue
        keyword = slug.replace("-", " ")
        pages.append({
            "slug": slug,
            "template": "F",
            "activity": None,
            "neighborhood": None,
            "audience": None,
            "title": f"{display_title} — Which Is Better? | StoryHunt",
            "h1": f"{display_title}.",
            "meta_desc": f"Comparing {display_title.lower()} in New York City. Which offers more fun, better value, and a more unique experience? We break it down — plus why StoryHunt wins.",
            "keywords": f"{keyword}, {display_title.lower()}, best activities NYC, StoryHunt review",
            "og_title": f"{display_title} — Honest Comparison | StoryHunt",
            "btn_text": "TRY_STORYHUNT",
            "footer_location": "LOCATION: NEW_YORK_CITY",
            "footer_status": "STATUS: COMPARISON_COMPLETE",
            "related_slugs": ["scavenger-hunt-nyc", "mystery-walk-nyc", "things-to-do-nyc"],
            "status": "pending",
        })

    # Template G: best-of pages
    for slug, page_title, related_topic, neighborhood in BEST_OF_COMBOS:
        if slug in EXISTING_EXPLORE:
            continue
        keyword = slug.replace("-", " ")
        related = [related_topic]
        if neighborhood and neighborhood in EXISTING_EXPLORE:
            related.append(neighborhood)
        related.append("hidden-places-nyc")
        pages.append({
            "slug": slug,
            "template": "G",
            "activity": None,
            "neighborhood": neighborhood,
            "audience": None,
            "title": f"{page_title} — Hidden Gems Guide | StoryHunt",
            "h1": f"{page_title}.",
            "meta_desc": f"Discover the {page_title.lower()} with StoryHunt. An insider's guide to hidden gems, secret spots, and the stories most people never hear. Explore now.",
            "keywords": f"{keyword}, {page_title.lower()} guide, StoryHunt NYC, hidden gems NYC",
            "og_title": f"{page_title} — Insider Guide | StoryHunt",
            "btn_text": "START_EXPLORING",
            "footer_location": "LOCATION: NEW_YORK_CITY",
            "footer_status": "STATUS: GUIDE_ACTIVE",
            "related_slugs": related[:3],
            "status": "pending",
        })

    # Template C: broad activity-nyc pages
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


def merge_config(new_config):
    """Merge new pages into existing config, preserving published status and generated_at."""
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

    existing_pages = {}
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            old_config = json.load(f)
        for page in old_config.get("pages", []):
            existing_pages[page["slug"]] = page

    # Merge: keep existing published pages, add new pending ones
    merged = []
    new_count = 0
    for page in new_config["pages"]:
        slug = page["slug"]
        if slug in existing_pages:
            # Preserve existing entry (keeps status, generated_at, etc.)
            merged.append(existing_pages[slug])
        else:
            # New page — add as pending
            merged.append(page)
            new_count += 1

    new_config["pages"] = merged
    return new_config, new_count


if __name__ == "__main__":
    config = build_config()
    config, new_count = merge_config(config)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    total = len(config["pages"])
    published = sum(1 for p in config["pages"] if p["status"] == "published")
    pending = sum(1 for p in config["pages"] if p["status"] == "pending")

    print(f"Config: {total} pages ({published} published, {pending} pending, {new_count} new)")
    templates = {}
    for p in config["pages"]:
        templates[p["template"]] = templates.get(p["template"], 0) + 1
    for t, count in sorted(templates.items()):
        print(f"  Template {t}: {count} pages")
