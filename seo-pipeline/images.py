"""Unsplash photo ID mappings for programmatic SEO pages."""

# Reused from existing explore pages
NEIGHBORHOOD_IMAGES = {
    "soho": ("1496442226666-8d4d0e62e6e9", "Cast-iron architecture in SoHo NYC"),
    "west-village": ("1555109307-f7d9da25c244", "West Village tree-lined street with brownstones"),
    "greenwich-village": ("1572707850781-50a4eb4c498a", "Greenwich Village historic townhouses NYC"),
    "chelsea": ("1555992643-bc38535f7115", "Chelsea neighborhood NYC art galleries"),
    "dumbo": ("1590274853856-f22d4d002c94", "DUMBO Brooklyn Manhattan Bridge view"),
    "central-park": ("1568515387631-8b650bbcdb90", "Central Park autumn trees and walking paths"),
    "williamsburg": ("1567538096630-e0c55bd6374c", "Williamsburg Brooklyn street art culture"),
    "harlem": ("1586276553693-e23e4c568d76", "Harlem brownstones and vibrant culture"),
    "midtown": ("1534430480872-3498386e7856", "Midtown Manhattan skyline city lights"),
    "tribeca": ("1558618666-fcd25c85f82e", "TriBeCa cobblestone street historic lofts"),
}

# Generic activity images for Template B/C pages
ACTIVITY_IMAGES = {
    "scavenger-hunt": ("1518391846015-55a9cc003b25", "Interactive scavenger hunt in New York City streets"),
    "mystery-walk": ("1536599018102-9f803c979b0b", "Mysterious foggy street in NYC for mystery walk"),
    "walking-tour": ("1500206329404-5057e0aefa48", "Walking tour through Manhattan elevated park"),
    "date-ideas": ("1516589178581-6cd7833ae3b2", "Couple exploring NYC streets on interactive date"),
    "team-building": ("1522083165195-3424ed4f2860", "NYC architecture team building corporate event"),
    "outdoor-escape-room": ("1477959858617-67f85cf4f1df", "Dark NYC alley outdoor escape room adventure"),
}

# Broad NYC pages (Template C)
BROAD_IMAGES = {
    "scavenger-hunt-nyc": ACTIVITY_IMAGES["scavenger-hunt"],
    "mystery-walk-nyc": ACTIVITY_IMAGES["mystery-walk"],
    "walking-tour-nyc": ACTIVITY_IMAGES["walking-tour"],
    "outdoor-escape-room-nyc": ACTIVITY_IMAGES["outdoor-escape-room"],
    "team-building-activities-nyc": ACTIVITY_IMAGES["team-building"],
    "bachelorette-party-nyc": ("1527761985-42c90681e1e8", "NYC bachelorette party nightlife speakeasy"),
    "birthday-ideas-nyc": ("1560713781-d00ac3ea1506", "NYC birthday celebration Times Square lights"),
    "corporate-events-nyc": ACTIVITY_IMAGES["team-building"],
    "things-to-do-nyc": ("1534430480872-3498386e7856", "Things to do in NYC skyline view"),
    "fun-activities-nyc": ("1518391846015-55a9cc003b25", "Fun outdoor activities in New York City"),
}


def get_image(slug, template, activity=None, neighborhood=None):
    """Return (unsplash_photo_id, alt_text) for a given page."""
    if template == "A" and neighborhood:
        photo_id, base_alt = NEIGHBORHOOD_IMAGES.get(neighborhood, ACTIVITY_IMAGES.get(activity, ("1534430480872-3498386e7856", "New York City")))
        return photo_id, base_alt
    elif template == "C":
        return BROAD_IMAGES.get(slug, ("1534430480872-3498386e7856", "New York City"))
    elif template == "B" and activity:
        return ACTIVITY_IMAGES.get(activity, ("1534430480872-3498386e7856", "New York City"))
    return ("1534430480872-3498386e7856", "New York City")


def build_img_html(photo_id, alt_text):
    """Build responsive <img> tag using Unsplash CDN."""
    base = f"https://images.unsplash.com/photo-{photo_id}"
    return f'''<div class="explore-hero-img">
                <img
                    src="{base}?w=900&h=450&fit=crop&q=80"
                    srcset="{base}?w=600&h=300&fit=crop&q=75 600w, {base}?w=900&h=450&fit=crop&q=80 900w, {base}?w=1200&h=600&fit=crop&q=80 1200w"
                    sizes="(max-width: 600px) 100vw, (max-width: 900px) 900px, 1200px"
                    alt="{alt_text}"
                    loading="lazy"
                    decoding="async"
                    style="width:100%;max-width:1200px;border-radius:8px;margin:2rem auto;display:block;"
                >
            </div>'''
