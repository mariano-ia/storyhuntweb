#!/usr/bin/env python3
"""
Apply overlay to conversion ads (5 videos) using Chrome + ffmpeg.
Each video gets its own headline + subtext tailored to the content.
"""

import os
import subprocess
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "assets", "ads", "videos")
OVERLAY_TEMPLATE = os.path.join(BASE_DIR, "templates", "overlay-reel.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FFMPEG = "/tmp/ffmpeg"

# Tailored copy per video
VIDEOS = [
    {
        "file": "conv-pov-walking.mp4",
        "location": "NEW_YORK_CITY",
        "headline": "DECODE<br>THE CITY",
        "subtext": "Your phone sends the clues.",
    },
    {
        "file": "conv-hidden-door.mp4",
        "location": "HIDDEN_DOOR // UNKNOWN",
        "headline": "DOORS<br>MOST MISS",
        "subtext": "2-3 hours. No guide. Just you.",
    },
    {
        "file": "conv-phone-cafe.mp4",
        "location": "// SIGNAL_ACQUIRED",
        "headline": "NOT A TOUR.<br>A MYSTERY.",
        "subtext": "From $9.99 — covers your whole group.",
    },
    {
        "file": "conv-underground.mp4",
        "location": "UNDERGROUND // 1912",
        "headline": "HIDDEN<br>NEW YORK",
        "subtext": "Real locations. Real history. Real walks.",
    },
    {
        "file": "conv-couple.mp4",
        "location": "// DATE_NIGHT",
        "headline": "EXPLORE<br>TOGETHER",
        "subtext": "One purchase covers you both. From $9.99.",
    },
]

with open(OVERLAY_TEMPLATE) as f:
    template_html = f.read()

ok = 0
total = 0

for video in VIDEOS:
    input_path = os.path.join(VIDEOS_DIR, video["file"])
    if not os.path.exists(input_path):
        print(f"  MISSING: {video['file']}")
        continue

    total += 1

    # Build overlay HTML with custom copy + modified CTA
    inject = f"""<script>
    var loc = document.getElementById('location');
    var head = document.getElementById('headline');
    var sub = document.getElementById('subtext');
    if (loc) loc.innerHTML = `{video['location']}`;
    if (head) head.innerHTML = `{video['headline']}`;
    if (sub) sub.innerHTML = `{video['subtext']}`;
    var cta = document.querySelector('.swipe-cta');
    if (cta) cta.innerHTML = 'START_YOUR_HUNT →';
    var url = document.querySelector('.url');
    if (url) url.innerHTML = 'STORYHUNT.CITY/START';
    </script>"""
    html = template_html.replace("</body>", inject + "</body>")

    # Write temp HTML
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as f:
        f.write(html)
        tmp_html = f.name

    # Screenshot overlay as PNG
    overlay_png = os.path.join(VIDEOS_DIR, f"overlay-{video['file'].replace('.mp4','.png')}")
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--default-background-color=00000000",
        "--window-size=1080,1920",
        f"--screenshot={overlay_png}",
        f"file://{tmp_html}"
    ], capture_output=True, timeout=30)
    os.unlink(tmp_html)

    if not os.path.exists(overlay_png):
        print(f"  [{total}] {video['file']} — FAIL (no overlay PNG)")
        continue

    # Composite: video + overlay PNG
    output_name = video['file'].replace('.mp4', '-final.mp4')
    output_path = os.path.join(VIDEOS_DIR, output_name)
    result = subprocess.run([
        FFMPEG, "-y",
        "-i", input_path,
        "-i", overlay_png,
        "-filter_complex", "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];[bg][1:v]overlay=0:0",
        "-c:a", "copy",
        output_path
    ], capture_output=True, timeout=120)

    os.unlink(overlay_png)

    if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100000:
        size = os.path.getsize(output_path)
        print(f"  [{total}] {output_name} — OK ({size:,} bytes)")
        ok += 1
    else:
        if os.path.exists(output_path):
            os.unlink(output_path)
        stderr = result.stderr.decode()[-400:] if result.stderr else ""
        print(f"  [{total}] {video['file']} — FAIL: {stderr}")

print(f"\nDone: {ok}/{total} videos processed with overlay")
