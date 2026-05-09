#!/usr/bin/env python3
"""
Render social media posts from HTML templates using Chrome headless.
Reads social-calendar.json, generates 1080x1080 PNGs in assets/posts/.
"""

import json
import os
import subprocess
import base64
import tempfile
import ssl
import time
import certifi
import urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
POSTS_DIR = os.path.join(BASE_DIR, "assets", "posts")
CALENDAR_FILE = os.path.join(BASE_DIR, "social-calendar.json")

os.makedirs(POSTS_DIR, exist_ok=True)


FALLBACK_BGS = [
    "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1080",
    "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?w=1080",
    "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=1080",
]


def _try_download(url, attempts=3):
    ctx = ssl.create_default_context(cafile=certifi.where())
    last_err = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                return resp.read()
        except Exception as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(1.5 * (i + 1))
    print(f"    WARNING: download failed after {attempts} attempts ({url}): {last_err}")
    return None


def download_image_as_base64(url):
    """Download image as base64 data URI. Retries, then tries fallback URLs. Returns None only if all sources fail."""
    data = _try_download(url)
    if data is None:
        for fb in FALLBACK_BGS:
            if fb == url:
                continue
            print(f"    trying fallback: {fb}")
            data = _try_download(fb, attempts=2)
            if data is not None:
                break
    if data is None:
        return None
    return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"


def build_mystery_html(post):
    """Build mystery/spotlight/behind template with embedded data."""
    bg_b64 = download_image_as_base64(post["bg_image"]) if post.get("bg_image") else None
    if not bg_b64:
        raise RuntimeError(f"bg_image unavailable for {post.get('image_file')} — refusing to render overlay-only PNG")
    bg_css = f"url('{bg_b64}')"

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; width: 1080px; height: 1080px; overflow: hidden; }}
.post {{ width: 1080px; height: 1080px; position: relative; overflow: hidden; background: #050505; font-family: 'Inter', sans-serif; }}
.bg-image {{ position: absolute; inset: 0; background: {bg_css} center/cover; filter: brightness(0.35) contrast(1.1); }}
.scanlines {{ position: absolute; inset: 0; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px); }}
.content {{ position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 64px; }}
.top-bar {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.status {{ font-family: 'Space Mono', monospace; font-size: 22px; color: rgba(255,255,255,0.5); letter-spacing: 0.05em; }}
.status .dot {{ display: inline-block; width: 12px; height: 12px; background: #ff0033; border-radius: 50%; margin-right: 10px; box-shadow: 0 0 10px #ff0033; }}
.logo {{ font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; color: #fff; letter-spacing: 0.1em; }}
.logo span {{ color: #ff0033; }}
.middle {{ display: flex; flex-direction: column; gap: 24px; }}
.location {{ font-family: 'Space Mono', monospace; font-size: 24px; color: #00d2ff; letter-spacing: 0.15em; text-transform: uppercase; }}
.headline {{ font-size: 76px; font-weight: 900; color: #fff; line-height: 1.1; max-width: 900px; text-shadow: 4px 0 #ff0033, -4px 0 #00d2ff; }}
.subtext {{ font-size: 32px; color: rgba(255,255,255,0.8); line-height: 1.45; max-width: 850px; }}
.bottom-bar {{ display: flex; justify-content: space-between; align-items: flex-end; }}
.cta {{ font-family: 'Space Mono', monospace; font-size: 26px; color: #ff0033; letter-spacing: 0.1em; font-weight: 700; border: 2px solid #ff0033; padding: 16px 30px; }}
.coords {{ font-family: 'Space Mono', monospace; font-size: 20px; color: rgba(255,255,255,0.4); text-align: right; line-height: 1.6; }}
</style></head>
<body>
<div class="post">
    <div class="bg-image"></div>
    <div class="scanlines"></div>
    <div class="content">
        <div class="top-bar">
            <div class="status"><span class="dot"></span>TRANSMISSION_ACTIVE</div>
            <div class="logo">STORY<span>HUNT</span></div>
        </div>
        <div class="middle">
            <div class="location">{post.get('location', '// NYC')}</div>
            <div class="headline">{post['headline']}</div>
            <div class="subtext">{post['subtext']}</div>
        </div>
        <div class="bottom-bar">
            <div class="cta">DECODE_THE_CITY →</div>
            <div class="coords">storyhunt.city</div>
        </div>
    </div>
</div>
</body></html>"""


def build_data_html(post):
    """Build data/did-you-know template."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; width: 1080px; height: 1080px; overflow: hidden; }}
.post {{ width: 1080px; height: 1080px; position: relative; overflow: hidden; background: #050505; font-family: 'Space Mono', monospace; }}
.grid {{ position: absolute; inset: 0; background: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px); background-size: 40px 40px; }}
.content {{ position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 64px; }}
.header {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.tag {{ font-size: 22px; color: #050505; background: #00d2ff; padding: 10px 20px; font-weight: 700; letter-spacing: 0.08em; }}
.logo {{ font-size: 22px; font-weight: 700; color: #fff; letter-spacing: 0.1em; }}
.logo span {{ color: #ff0033; }}
.body {{ display: flex; flex-direction: column; gap: 36px; }}
.terminal-line {{ font-size: 22px; color: rgba(255,255,255,0.45); }}
.terminal-line .prompt {{ color: #ff0033; }}
.fact-number {{ font-size: 180px; font-weight: 700; color: #ff0033; line-height: 1; opacity: 0.9; text-shadow: 0 0 50px rgba(255,0,51,0.35); }}
.fact-label {{ font-size: 24px; color: rgba(255,255,255,0.6); letter-spacing: 0.15em; text-transform: uppercase; margin-top: -8px; }}
.fact-text {{ font-family: 'Inter', sans-serif; font-size: 44px; font-weight: 700; color: #fff; line-height: 1.35; max-width: 880px; }}
.fact-text .highlight {{ color: #00d2ff; }}
.footer {{ display: flex; justify-content: space-between; align-items: flex-end; }}
.source {{ font-size: 20px; color: rgba(255,255,255,0.4); line-height: 1.6; }}
.cta {{ font-size: 24px; color: #00d2ff; font-weight: 700; letter-spacing: 0.1em; border-bottom: 3px solid #00d2ff; padding-bottom: 6px; }}
</style></head>
<body>
<div class="post">
    <div class="grid"></div>
    <div class="content">
        <div class="header">
            <div class="tag">{post.get('tag', 'DID_YOU_KNOW')}</div>
            <div class="logo">STORY<span>HUNT</span></div>
        </div>
        <div class="body">
            <div class="terminal-line"><span class="prompt">$</span> {post.get('terminal_line', 'query --classified=true')[2:]}</div>
            <div>
                <div class="fact-number">{post['fact_number']}</div>
                <div class="fact-label">{post['fact_label']}</div>
            </div>
            <div class="fact-text">{post['fact_text']}</div>
        </div>
        <div class="footer">
            <div class="source">SRC: NYC_ARCHIVES<br>CLASSIFICATION: DECLASSIFIED</div>
            <div class="cta">STORYHUNT.CITY →</div>
        </div>
    </div>
</div>
</body></html>"""


def build_quote_html(post):
    """Build quote template."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; width: 1080px; height: 1080px; overflow: hidden; }}
.post {{ width: 1080px; height: 1080px; position: relative; overflow: hidden; background: #050505; font-family: 'Inter', sans-serif; }}
.gradient-accent {{ position: absolute; bottom: -200px; left: -200px; width: 600px; height: 600px; background: radial-gradient(circle, rgba(255,0,51,0.12) 0%, transparent 70%); }}
.gradient-accent-2 {{ position: absolute; top: -150px; right: -150px; width: 500px; height: 500px; background: radial-gradient(circle, rgba(0,210,255,0.08) 0%, transparent 70%); }}
.border-line {{ position: absolute; inset: 32px; border: 1px solid rgba(255,255,255,0.06); }}
.content {{ position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 80px; }}
.top {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.marker {{ font-family: 'Space Mono', monospace; font-size: 96px; color: rgba(255,0,51,0.3); font-weight: 700; line-height: 1; }}
.logo {{ font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; color: #fff; letter-spacing: 0.1em; }}
.logo span {{ color: #ff0033; }}
.quote-block {{ display: flex; flex-direction: column; gap: 36px; }}
.quote {{ font-size: 64px; font-weight: 900; color: #fff; line-height: 1.2; max-width: 900px; letter-spacing: -0.01em; }}
.quote .em {{ color: #00d2ff; text-decoration: underline; text-decoration-color: rgba(0,210,255,0.4); text-underline-offset: 8px; }}
.divider {{ width: 80px; height: 4px; background: #ff0033; }}
.attribution {{ font-family: 'Space Mono', monospace; font-size: 24px; color: rgba(255,255,255,0.5); letter-spacing: 0.1em; }}
.bottom {{ display: flex; justify-content: space-between; align-items: flex-end; }}
.tagline {{ font-family: 'Space Mono', monospace; font-size: 22px; color: rgba(255,255,255,0.4); letter-spacing: 0.08em; line-height: 1.6; }}
.url {{ font-family: 'Space Mono', monospace; font-size: 26px; color: #ff0033; font-weight: 700; letter-spacing: 0.05em; }}
</style></head>
<body>
<div class="post">
    <div class="gradient-accent"></div>
    <div class="gradient-accent-2"></div>
    <div class="border-line"></div>
    <div class="content">
        <div class="top">
            <div class="marker">"</div>
            <div class="logo">STORY<span>HUNT</span></div>
        </div>
        <div class="quote-block">
            <div class="quote">{post['quote']}</div>
            <div class="divider"></div>
            <div class="attribution">{post['attribution']}</div>
        </div>
        <div class="bottom">
            <div class="tagline">DECODE_THE_CITY<br>LIVE_THE_STORY</div>
            <div class="url">STORYHUNT.CITY</div>
        </div>
    </div>
</div>
</body></html>"""


def build_howitworks_html(post):
    """Build HOW_IT_WORKS template — solid black bg, cyan tag, headline + subtext."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; width: 1080px; height: 1080px; overflow: hidden; }}
.post {{ width: 1080px; height: 1080px; position: relative; overflow: hidden; background: #000; font-family: 'Inter', sans-serif; }}
.content {{ position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 64px; }}
.header {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.tag {{ font-family: 'Space Mono', monospace; font-size: 26px; color: #050505; background: #00d2ff; padding: 12px 24px; font-weight: 700; letter-spacing: 0.1em; }}
.logo {{ font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; color: #fff; letter-spacing: 0.1em; }}
.logo span {{ color: #ff0033; }}
.middle {{ display: flex; flex-direction: column; gap: 32px; }}
.headline {{ font-size: 96px; font-weight: 900; color: #fff; line-height: 1.05; max-width: 950px; letter-spacing: -0.02em; }}
.headline .em {{ color: #00d2ff; }}
.divider {{ width: 100px; height: 4px; background: #00d2ff; }}
.subtext {{ font-size: 36px; color: rgba(255,255,255,0.85); line-height: 1.4; max-width: 900px; }}
.bottom-bar {{ display: flex; justify-content: space-between; align-items: flex-end; }}
.cta {{ font-family: 'Space Mono', monospace; font-size: 26px; color: #00d2ff; letter-spacing: 0.1em; font-weight: 700; border: 2px solid #00d2ff; padding: 16px 30px; }}
.url {{ font-family: 'Space Mono', monospace; font-size: 22px; color: rgba(255,255,255,0.5); letter-spacing: 0.05em; }}
</style></head>
<body>
<div class="post">
    <div class="content">
        <div class="header">
            <div class="tag">HOW IT WORKS</div>
            <div class="logo">STORY<span>HUNT</span></div>
        </div>
        <div class="middle">
            <div class="headline">{post['headline']}</div>
            <div class="divider"></div>
            <div class="subtext">{post['subtext']}</div>
        </div>
        <div class="bottom-bar">
            <div class="cta">DECODE_THE_CITY →</div>
            <div class="url">storyhunt.city</div>
        </div>
    </div>
</div>
</body></html>"""


BUILDERS = {
    "mystery": build_mystery_html,
    "data": build_data_html,
    "quote": build_quote_html,
    "howitworks": build_howitworks_html,
}


def render_post(post):
    """Render a single post to PNG."""
    template = post["template"]
    builder = BUILDERS.get(template)
    if not builder:
        print(f"  SKIP unknown template: {template}")
        return False

    try:
        html = builder(post)
    except RuntimeError as e:
        print(f"  FAIL  {post['image_file']} — {e}")
        return False

    out_path = os.path.join(BASE_DIR, post["image_file"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False) as f:
        f.write(html)
        tmp_html = f.name

    try:
        # Render at extra height to absorb Chrome's headless viewport offset,
        # then crop top 1080x1080 so the post fills the frame edge-to-edge.
        result = subprocess.run([
            CHROME,
            "--headless=new",
            "--disable-gpu",
            f"--screenshot={out_path}",
            "--window-size=1080,1220",
            "--hide-scrollbars",
            f"file://{tmp_html}",
        ], capture_output=True, timeout=30, text=True)
        if result.stderr:
            print(f"    CHROME: {result.stderr[:200]}")

        if os.path.exists(out_path):
            try:
                from PIL import Image
                with Image.open(out_path) as im:
                    if im.size != (1080, 1080):
                        im.crop((0, 0, 1080, 1080)).save(out_path)
            except Exception as crop_err:
                print(f"    CROP_WARN: {crop_err}")
            size = os.path.getsize(out_path)
            print(f"  OK  {post['image_file']} ({size:,} bytes)")
            return True
        else:
            print(f"  FAIL  {post['image_file']} — no output")
            return False
    except Exception as e:
        print(f"  FAIL  {post['image_file']} — {e}")
        return False
    finally:
        os.unlink(tmp_html)


def main():
    with open(CALENDAR_FILE) as f:
        calendar = json.load(f)

    posts = calendar["posts"]
    total = len(posts)
    rendered = 0

    print(f"{'='*60}")
    print(f"StoryHunt Post Renderer")
    print(f"Rendering {total} posts")
    print(f"{'='*60}")

    for post in posts:
        if post["status"] == "published":
            print(f"  SKIP {post['date']} — already published")
            continue

        print(f"\n  [{post['date']}] {post['content_type']} ({post['template']})")
        if render_post(post):
            rendered += 1

    print(f"\n{'='*60}")
    print(f"Rendered: {rendered}/{total}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
