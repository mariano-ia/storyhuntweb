#!/usr/bin/env python3
"""
Render the FOUNDERS campaign ad video for IG Reels (1080x1920, 9:16).

Variant C copy (anti-tour positioning) — applied to 2 KIE-generated base
videos so we can A/B-test in Ads Manager.

Output:
    assets/ads/videos/founders/founders-hidden-door.mp4
    assets/ads/videos/founders/founders-pov-walking.mp4

Mirrors the pattern of overlay-conversion-ads.py but with founders-specific
copy and a /founders CTA. Uses Chrome headless to rasterise the overlay
HTML, then ffmpeg to composite onto the video.
"""

import os
import subprocess
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "assets", "ads", "videos")
OUT_DIR = os.path.join(VIDEOS_DIR, "founders")
OVERLAY_TEMPLATE = os.path.join(BASE_DIR, "templates", "overlay-reel.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FFMPEG = "/Users/marianonoceti/ffmpeg"
FONT_PATH = "/System/Library/Fonts/Monaco.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Menlo.ttc"

os.makedirs(OUT_DIR, exist_ok=True)


VARIANTS = [
    {
        "name": "nyc-skyline",
        "source_path": os.path.join(
            BASE_DIR, "assets", "reels", "2w", "raw", "voicemail",
            "raw-reel-28-last-call.mp4"
        ),
        "location": "// NEW_YORK // FREE_THIS_WEEK",
        "headline": "100 FREE.<br>THIS WEEK.",
        "subtext": "NYC's best self-guided walking tour. After Sunday: $15.",
    },
    {
        "name": "hidden-door",
        "source": "conv-hidden-door.mp4",
        "location": "// 100_DOORS // FREE_THIS_WEEK",
        "headline": "NOT A TOUR.<br>FREE THIS WEEK.",
        "subtext": "The city texts you. 100 free hunters. Six days.",
    },
    {
        "name": "pov-walking",
        "source": "conv-pov-walking.mp4",
        "location": "// 100_DOORS // NEW_YORK",
        "headline": "NOT A TOUR.<br>NOT A GUIDE.",
        "subtext": "The city texts you. 100 free this week.",
    },
]


with open(OVERLAY_TEMPLATE) as f:
    template_html = f.read()

ok = 0
for v in VARIANTS:
    input_path = v.get("source_path") or os.path.join(VIDEOS_DIR, v["source"])
    if not os.path.exists(input_path):
        print(f"  MISSING base video: {input_path}")
        continue

    output_path = os.path.join(OUT_DIR, f"founders-{v['name']}.mp4")

    # Inject overlay copy into template (hide built-in .bottom so ffmpeg paints CTA bar)
    inject = f"""<script>
    var loc = document.getElementById('location');
    var head = document.getElementById('headline');
    var sub = document.getElementById('subtext');
    if (loc) loc.innerHTML = `{v['location']}`;
    if (head) head.innerHTML = `{v['headline']}`;
    if (sub) sub.innerHTML = `{v['subtext']}`;
    var bottom = document.querySelector('.bottom');
    if (bottom) bottom.style.display = 'none';
    </script>"""
    html = template_html.replace("</body>", inject + "</body>")

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
        f.write(html)
        tmp_html = f.name

    # Screenshot overlay as transparent PNG at exact 1080x1920
    overlay_png = os.path.join(OUT_DIR, f".overlay-{v['name']}.png")
    res = subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--default-background-color=00000000",
        "--force-device-scale-factor=1",
        "--hide-scrollbars",
        "--window-size=1080,1920",
        f"--screenshot={overlay_png}",
        f"file://{tmp_html}"
    ], capture_output=True, timeout=30)
    os.unlink(tmp_html)

    if not os.path.exists(overlay_png):
        print(f"  [{v['name']}] FAIL (no overlay PNG): {res.stderr.decode()[-200:]}")
        continue

    # Composite: scale+crop video to 1080x1920, overlay PNG, paint black bars + bottom CTA
    result = subprocess.run([
        FFMPEG, "-y",
        "-i", input_path,
        "-i", overlay_png,
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
        "[1:v]scale=1080:1920[ov];"
        "[bg][ov]overlay=0:0:format=auto,"
        "drawbox=x=0:y=0:w=1080:h=6:color=black@1:t=fill,"
        "drawbox=x=0:y=1780:w=1080:h=140:color=black@1:t=fill,"
        f"drawtext=fontfile='{FONT_PATH}':text='CLAIM YOURS →':"
        "fontcolor=0xff0033:fontsize=32:x=(w-tw)/2:y=1818,"
        f"drawtext=fontfile='{FONT_PATH}':text='STORYHUNT.CITY/FOUNDERS':"
        "fontcolor=white@0.45:fontsize=22:x=(w-tw)/2:y=1870",
        "-c:a", "copy",
        output_path
    ], capture_output=True, timeout=180)

    os.unlink(overlay_png)

    if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100_000:
        size_mb = os.path.getsize(output_path) / 1_000_000
        print(f"  [{v['name']}] OK — {size_mb:.2f} MB at {output_path}")
        ok += 1
    else:
        if os.path.exists(output_path):
            os.unlink(output_path)
        stderr = result.stderr.decode()[-400:] if result.stderr else ""
        print(f"  [{v['name']}] FAIL: {stderr}")

print(f"\nDone: {ok}/{len(VARIANTS)} variants rendered into {OUT_DIR}")
