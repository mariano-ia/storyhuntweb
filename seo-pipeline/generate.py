#!/usr/bin/env python3
"""
StoryHunt Programmatic SEO Page Generator.

Usage:
    python3 seo-pipeline/generate.py                        # Generate all pending
    python3 seo-pipeline/generate.py --limit 5              # Generate first 5 pending
    python3 seo-pipeline/generate.py --slug scavenger-hunt-in-soho
    python3 seo-pipeline/generate.py --template A           # Only Template A pages
    python3 seo-pipeline/generate.py --dry-run              # Preview without generating
    python3 seo-pipeline/generate.py --regenerate           # Re-generate published pages
    python3 seo-pipeline/generate.py --sitemap-only         # Only update sitemap
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

# Add pipeline dir to path
PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.dirname(PIPELINE_DIR)
EXPLORE_DIR = os.path.join(WEB_DIR, "explore")
CACHE_DIR = os.path.join(PIPELINE_DIR, "content_cache")
CONFIG_PATH = os.path.join(PIPELINE_DIR, "config.json")
TEMPLATE_PATH = os.path.join(PIPELINE_DIR, "template.html")
SITEMAP_PATH = os.path.join(WEB_DIR, "sitemap.xml")

sys.path.insert(0, PIPELINE_DIR)
from images import get_image, build_img_html
from prompts import get_prompt


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_openai_key():
    """Load OPENAI_API_KEY from ABM .env.local or environment."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    # Try ABM .env.local
    env_path = os.path.join(WEB_DIR, "..", "StoryHuntABM", ".env.local")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    return line.strip().split("=", 1)[1].strip('"').strip("'")
    print("ERROR: OPENAI_API_KEY not found. Set it in environment or in StoryHuntABM/.env.local")
    sys.exit(1)


def generate_content(page, api_key):
    """Generate content via GPT-4o-mini, with caching."""
    slug = page["slug"]
    cache_path = os.path.join(CACHE_DIR, f"{slug}.json")

    # Check cache
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        print(f"  [CACHE] Using cached content for {slug}")
        return cached

    # Build prompt kwargs
    activity_raw = page.get("activity") or ""
    kwargs = {
        "activity_display": activity_raw.replace("-", " ").title(),
        "slug": slug,
    }
    config = load_config()
    if page.get("neighborhood"):
        kwargs["neighborhood_display"] = config["neighborhoods"].get(page["neighborhood"], page["neighborhood"].replace("-", " ").title())
    if page.get("audience"):
        kwargs["audience_display"] = config["audiences"].get(page["audience"], page["audience"].title())
    if page.get("temporal"):
        from build_config import TEMPORALS
        kwargs["temporal_display"] = TEMPORALS.get(page["temporal"], page["temporal"].replace("-", " ").title())
    if page.get("theme"):
        from build_config import THEMES
        kwargs["theme_display"] = THEMES.get(page["theme"], page["theme"].replace("-", " ").title())

    # Map activity slug to display name from config
    if page.get("activity") and page["activity"] in config["activities"]:
        kwargs["activity_display"] = config["activities"][page["activity"]]

    # For comparison/best-of pages, pass the title
    kwargs["display_title"] = page.get("title", "").replace(" | StoryHunt", "").replace(" — Which Is Better?", "").replace(" — Hidden Gems Guide", "")
    kwargs["page_title"] = page.get("h1", "").rstrip(".")

    system_msg, user_msg = get_prompt(page["template"], **kwargs)

    # Call OpenAI
    import openai
    client = openai.OpenAI(api_key=api_key)

    print(f"  [GPT] Generating content for {slug}...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    content_text = response.choices[0].message.content
    content = json.loads(content_text)

    # Validate required fields
    required = ["content_title", "subtitle", "paragraphs", "faq"]
    for field in required:
        if field not in content:
            print(f"  [WARN] Missing field '{field}' in GPT response for {slug}")
            content.setdefault(field, "")

    # Save to cache
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

    tokens = response.usage.total_tokens if response.usage else 0
    print(f"  [GPT] Done ({tokens} tokens)")
    return content


def build_faq_html(faq_items):
    """Build FAQ HTML from list of {q, a} dicts."""
    html = ""
    for item in faq_items:
        q = item.get("q", "")
        a = item.get("a", "")
        html += f'''                <h3 style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 2rem; margin-bottom: 0.5rem;">{q}</h3>
                <p>{a}</p>
'''
    return html


def build_faq_schema(faq_items):
    """Build FAQPage schema JSON entries."""
    entries = []
    for item in faq_items:
        q = item.get("q", "").replace('"', '\\"')
        a = item.get("a", "").replace('"', '\\"')
        entries.append(f'''        {{
          "@type": "Question",
          "name": "{q}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{a}"
          }}
        }}''')
    return ",\n".join(entries)


def build_related_links(related_slugs):
    """Build related hunts HTML links."""
    links = []
    for slug in related_slugs:
        # Check if file exists
        filepath = os.path.join(EXPLORE_DIR, f"{slug}.html")
        if os.path.exists(filepath):
            label = slug.replace("-", " ").title()
            # Clean up common patterns
            label = label.replace("Nyc", "NYC").replace("In ", "in ").replace("For ", "for ")
            links.append(f'<a href="{slug}.html">{label}</a>')
    if not links:
        # Fallback to existing popular pages
        links = [
            '<a href="hidden-places-nyc.html">Hidden Places NYC</a>',
            '<a href="mysteries-in-nyc.html">Mysteries in NYC</a>',
        ]
    return "\n                    ".join(links)


def render_page(page, content, template):
    """Render a complete HTML page from template + content."""
    slug = page["slug"]
    photo_id, alt_text = get_image(slug, page["template"], page.get("activity"), page.get("neighborhood"))
    hero_image = build_img_html(photo_id, alt_text)

    # Build paragraphs HTML
    paragraphs = content.get("paragraphs", [])
    paragraphs_html = "\n                ".join(f"<p>{p}</p>" for p in paragraphs)

    # Build FAQ
    faq_items = content.get("faq", [])
    faq_html = build_faq_html(faq_items)
    faq_schema = build_faq_schema(faq_items)

    # Related links
    related_links = build_related_links(page.get("related_slugs", []))

    # Clean h1 for schema (remove trailing period)
    h1_clean = page["h1"].rstrip(".")

    # Template substitution
    html = template
    replacements = {
        "{{canonical_url}}": f"https://storyhunt.city/explore/{slug}.html",
        "{{meta_desc}}": page["meta_desc"],
        "{{keywords}}": page["keywords"],
        "{{og_title}}": page["og_title"],
        "{{title}}": page["title"],
        "{{h1}}": page["h1"],
        "{{h1_clean}}": h1_clean,
        "{{subtitle}}": content.get("subtitle", "Decode the city."),
        "{{btn_text}}": page["btn_text"],
        "{{content_title}}": content.get("content_title", h1_clean),
        "{{hero_image}}": hero_image,
        "{{paragraphs_html}}": paragraphs_html,
        "{{related_links}}": related_links,
        "{{faq_html}}": faq_html,
        "{{faq_schema}}": faq_schema,
        "{{footer_location}}": page["footer_location"],
        "{{footer_status}}": page["footer_status"],
        "{{slug}}": slug,
    }

    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    return html


def update_sitemap(config):
    """Update sitemap.xml with all published pages."""
    # Read existing sitemap
    existing_urls = set()
    if os.path.exists(SITEMAP_PATH):
        import re
        with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
            sitemap_content = f.read()
        existing_urls = set(re.findall(r'<loc>([^<]+)</loc>', sitemap_content))

    # Add new pages
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_entries = []
    for page in config["pages"]:
        if page["status"] == "published":
            url = f"https://storyhunt.city/explore/{page['slug']}.html"
            if url not in existing_urls:
                new_entries.append(url)

    if not new_entries:
        print("  [SITEMAP] No new URLs to add")
        return

    # Build new sitemap
    # Parse existing entries
    import re
    entries = re.findall(r'<url>.*?</url>', sitemap_content if os.path.exists(SITEMAP_PATH) else "", re.DOTALL)

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for entry in entries:
        sitemap += f"  {entry}\n"
    for url in new_entries:
        sitemap += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>\n"""
    sitemap += "</urlset>\n"

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap)

    print(f"  [SITEMAP] Added {len(new_entries)} new URLs (total: {len(entries) + len(new_entries)})")


def main():
    parser = argparse.ArgumentParser(description="StoryHunt Programmatic SEO Generator")
    parser.add_argument("--limit", type=int, help="Max pages to generate")
    parser.add_argument("--slug", help="Generate a specific page by slug")
    parser.add_argument("--template", choices=["A", "B", "C", "D", "E", "F", "G"], help="Only generate pages of this template type")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating files")
    parser.add_argument("--regenerate", action="store_true", help="Re-generate even published pages")
    parser.add_argument("--sitemap-only", action="store_true", help="Only update sitemap.xml")
    args = parser.parse_args()

    config = load_config()
    template = load_template()

    if args.sitemap_only:
        update_sitemap(config)
        return

    # Filter pages
    pages = config["pages"]
    if args.slug:
        pages = [p for p in pages if p["slug"] == args.slug]
        if not pages:
            print(f"ERROR: Slug '{args.slug}' not found in config")
            sys.exit(1)
    elif not args.regenerate:
        pages = [p for p in pages if p["status"] == "pending"]

    if args.template:
        pages = [p for p in pages if p["template"] == args.template]

    if args.limit:
        pages = pages[:args.limit]

    if not pages:
        print("No pages to generate.")
        return

    print(f"Generating {len(pages)} pages...")

    if args.dry_run:
        for p in pages:
            print(f"  [DRY] {p['slug']} (Template {p['template']})")
        return

    # Load API key
    api_key = load_openai_key()

    generated = 0
    errors = 0

    for page in pages:
        try:
            # Generate content via GPT (with caching)
            content = generate_content(page, api_key)

            # Render HTML
            html = render_page(page, content, template)

            # Write file
            filepath = os.path.join(EXPLORE_DIR, f"{page['slug']}.html")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)

            # Update status in config
            page["status"] = "published"
            page["generated_at"] = datetime.now(timezone.utc).isoformat()
            generated += 1
            print(f"  [OK] {page['slug']}.html")

        except Exception as e:
            errors += 1
            print(f"  [ERR] {page['slug']}: {e}")

    # Save updated config
    save_config(config)

    # Update sitemap
    update_sitemap(config)

    print(f"\nDone. Generated: {generated}, Errors: {errors}")


if __name__ == "__main__":
    main()
