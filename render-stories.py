#!/usr/bin/env python3
"""
Render 20 Instagram Stories (1080x1920) from templates.
Each story matches a social-calendar.json entry but with story-optimized layout.
"""

import json
import os
import subprocess
import base64
import ssl
import certifi
import urllib.request
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORIES_DIR = os.path.join(BASE_DIR, "assets", "stories")
CALENDAR_FILE = os.path.join(BASE_DIR, "social-calendar.json")

os.makedirs(STORIES_DIR, exist_ok=True)


def download_image_as_base64(url):
    try:
        ctx = ssl.create_default_context(cafile=certifi.where())
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = resp.read()
            return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
    except Exception as e:
        print(f"    WARNING: Could not download {url}: {e}")
        return None


def build_mystery_story(post):
    bg_b64 = download_image_as_base64(post["bg_image"]) if post.get("bg_image") else None
    bg_css = f"url('{bg_b64}')" if bg_b64 else "linear-gradient(135deg, #0a0a0a, #1a1a2e)"
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; width: 1080px; height: 1920px; overflow: hidden; }}
.story {{ width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #050505; font-family: 'Inter', sans-serif; }}
.bg {{ position: absolute; inset: 0; background: {bg_css} center/cover; filter: brightness(0.3) contrast(1.1); }}
.scanlines {{ position: absolute; inset: 0; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.12) 2px, rgba(0,0,0,0.12) 4px); }}
.vignette {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.6) 100%); }}
.content {{ position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 80px 56px; }}
.top {{ display: flex; justify-content: space-between; align-items: center; }}
.status {{ font-family: 'Space Mono', monospace; font-size: 14px; color: rgba(255,255,255,0.4); display: flex; align-items: center; gap: 10px; }}
.dot {{ width: 10px; height: 10px; background: #ff0033; border-radius: 50%; box-shadow: 0 0 10px #ff0033; }}
.logo {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; color: #fff; letter-spacing: 0.1em; }}
.logo span {{ color: #ff0033; }}
.middle {{ display: flex; flex-direction: column; gap: 28px; }}
.location {{ font-family: 'Space Mono', monospace; font-size: 16px; color: #00d2ff; letter-spacing: 0.15em; }}
.headline {{ font-size: 64px; font-weight: 900; color: #fff; line-height: 1.08; text-shadow: 4px 0 #ff0033, -4px 0 #00d2ff; }}
.subtext {{ font-size: 22px; color: rgba(255,255,255,0.7); line-height: 1.5; }}
.bottom {{ display: flex; flex-direction: column; gap: 16px; align-items: center; }}
.cta {{ font-family: 'Space Mono', monospace; font-size: 18px; color: #ff0033; letter-spacing: 0.1em; font-weight: 700; }}
.arrow {{ font-size: 28px; color: #ff0033; }}
.url {{ font-family: 'Space Mono', monospace; font-size: 14px; color: rgba(255,255,255,0.3); letter-spacing: 0.1em; }}
</style></head>
<body>
<div class="story">
    <div class="bg"></div><div class="scanlines"></div><div class="vignette"></div>
    <div class="content">
        <div class="top">
            <div class="status"><div class="dot"></div>LIVE_TRANSMISSION</div>
            <div class="logo">STORY<span>HUNT</span></div>
        </div>
        <div class="middle">
            <div class="location">{post.get('location', '// NYC')}</div>
            <div class="headline">{post['headline']}</div>
            <div class="subtext">{post['subtext']}</div>
        </div>
        <div class="bottom">
            <div class="cta">DECODE_THE_CITY</div>
            <div class="arrow">↑</div>
            <div class="url">STORYHUNT.CITY</div>
        </div>
    </div>
</div>
</body></html>"""


def build_data_story(post):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; width: 1080px; height: 1920px; overflow: hidden; }}
.story {{ width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #050505; font-family: 'Space Mono', monospace; }}
.grid {{ position: absolute; inset: 0; background: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px); background-size: 40px 40px; }}
.content {{ position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 80px 56px; }}
.header {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.tag {{ font-size: 14px; color: #050505; background: #00d2ff; padding: 8px 16px; font-weight: 700; letter-spacing: 0.08em; }}
.logo {{ font-size: 16px; font-weight: 700; color: #fff; letter-spacing: 0.1em; }}
.logo span {{ color: #ff0033; }}
.body {{ display: flex; flex-direction: column; gap: 40px; }}
.terminal {{ font-size: 14px; color: rgba(255,255,255,0.3); }}
.terminal .p {{ color: #ff0033; }}
.num {{ font-size: 180px; font-weight: 700; color: #ff0033; line-height: 1; text-shadow: 0 0 60px rgba(255,0,51,0.3); }}
.label {{ font-size: 16px; color: rgba(255,255,255,0.5); letter-spacing: 0.15em; text-transform: uppercase; margin-top: -12px; }}
.fact {{ font-family: 'Inter', sans-serif; font-size: 32px; font-weight: 700; color: #fff; line-height: 1.4; }}
.fact .highlight {{ color: #00d2ff; }}
.footer {{ display: flex; flex-direction: column; gap: 16px; align-items: center; }}
.src {{ font-size: 12px; color: rgba(255,255,255,0.2); text-align: center; line-height: 1.8; }}
.cta {{ font-size: 16px; color: #00d2ff; font-weight: 700; letter-spacing: 0.1em; }}
</style></head>
<body>
<div class="story">
    <div class="grid"></div>
    <div class="content">
        <div class="header">
            <div class="tag">{post.get('tag', 'DID_YOU_KNOW')}</div>
            <div class="logo">STORY<span>HUNT</span></div>
        </div>
        <div class="body">
            <div class="terminal"><span class="p">$</span> {post.get('terminal_line', '')[2:]}</div>
            <div>
                <div class="num">{post['fact_number']}</div>
                <div class="label">{post['fact_label']}</div>
            </div>
            <div class="fact">{post['fact_text']}</div>
        </div>
        <div class="footer">
            <div class="src">SRC: NYC_ARCHIVES // DECLASSIFIED</div>
            <div class="cta">STORYHUNT.CITY ↑</div>
        </div>
    </div>
</div>
</body></html>"""


def build_quote_story(post):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #000; width: 1080px; height: 1920px; overflow: hidden; }}
.story {{ width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #050505; font-family: 'Inter', sans-serif; }}
.g1 {{ position: absolute; bottom: -300px; left: -300px; width: 800px; height: 800px; background: radial-gradient(circle, rgba(255,0,51,0.12) 0%, transparent 70%); }}
.g2 {{ position: absolute; top: -200px; right: -200px; width: 700px; height: 700px; background: radial-gradient(circle, rgba(0,210,255,0.08) 0%, transparent 70%); }}
.border {{ position: absolute; inset: 40px; border: 1px solid rgba(255,255,255,0.06); }}
.content {{ position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 100px 64px; }}
.top {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.mark {{ font-family: 'Space Mono', monospace; font-size: 80px; color: rgba(255,0,51,0.25); font-weight: 700; line-height: 1; }}
.logo {{ font-family: 'Space Mono', monospace; font-size: 16px; font-weight: 700; color: #fff; letter-spacing: 0.1em; }}
.logo span {{ color: #ff0033; }}
.mid {{ display: flex; flex-direction: column; gap: 36px; }}
.quote {{ font-size: 54px; font-weight: 900; color: #fff; line-height: 1.2; }}
.quote .em {{ color: #00d2ff; text-decoration: underline; text-decoration-color: rgba(0,210,255,0.3); text-underline-offset: 8px; }}
.div {{ width: 80px; height: 4px; background: #ff0033; }}
.attr {{ font-family: 'Space Mono', monospace; font-size: 15px; color: rgba(255,255,255,0.4); letter-spacing: 0.1em; }}
.bot {{ display: flex; flex-direction: column; gap: 12px; align-items: center; }}
.tag {{ font-family: 'Space Mono', monospace; font-size: 14px; color: rgba(255,255,255,0.3); letter-spacing: 0.08em; text-align: center; line-height: 1.8; }}
.url {{ font-family: 'Space Mono', monospace; font-size: 18px; color: #ff0033; font-weight: 700; }}
</style></head>
<body>
<div class="story">
    <div class="g1"></div><div class="g2"></div><div class="border"></div>
    <div class="content">
        <div class="top">
            <div class="mark">"</div>
            <div class="logo">STORY<span>HUNT</span></div>
        </div>
        <div class="mid">
            <div class="quote">{post['quote']}</div>
            <div class="div"></div>
            <div class="attr">{post['attribution']}</div>
        </div>
        <div class="bot">
            <div class="tag">DECODE_THE_CITY<br>LIVE_THE_STORY</div>
            <div class="url">STORYHUNT.CITY</div>
        </div>
    </div>
</div>
</body></html>"""


BUILDERS = {"mystery": build_mystery_story, "data": build_data_story, "quote": build_quote_story}


def render_story(post, index):
    template = post["template"]
    builder = BUILDERS.get(template)
    if not builder:
        return False

    html = builder(post)
    filename = f"story-{index+1:02d}-{post['date']}-{template}.png"
    out_path = os.path.join(STORIES_DIR, filename)

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False) as f:
        f.write(html)
        tmp = f.name

    try:
        result = subprocess.run([
            CHROME, "--headless=new", "--disable-gpu",
            f"--screenshot={out_path}",
            "--window-size=1080,1920",
            "--hide-scrollbars",
            f"file://{tmp}",
        ], capture_output=True, timeout=30, text=True)
        if os.path.exists(out_path):
            print(f"  OK  {filename} ({os.path.getsize(out_path):,} bytes)")
            return True
        else:
            print(f"  FAIL  {filename}")
            return False
    except Exception as e:
        print(f"  FAIL  {filename} — {e}")
        return False
    finally:
        os.unlink(tmp)


def main():
    with open(CALENDAR_FILE) as f:
        calendar = json.load(f)

    posts = calendar["posts"]
    print(f"{'='*60}")
    print(f"StoryHunt Story Renderer — {len(posts)} stories")
    print(f"Output: {STORIES_DIR}")
    print(f"{'='*60}")

    ok = 0
    for i, post in enumerate(posts):
        print(f"\n  [{post['date']}] {post['content_type']} ({post['template']})")
        if render_story(post, i):
            ok += 1

    print(f"\n{'='*60}")
    print(f"Rendered: {ok}/{len(posts)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
