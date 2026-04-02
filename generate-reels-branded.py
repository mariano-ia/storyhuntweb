#!/usr/bin/env python3
"""
Generate 20 branded StoryHunt Reels:
1. Generate AI video via fal.ai Minimax
2. Crop to vertical 9:16
3. Add branding overlay (logo, text, CTA) via FFmpeg
"""

import json, os, time, subprocess, urllib.request, ssl, certifi, tempfile

FAL_KEY = "0f8a2107-d148-4f16-9938-cadfacf358f0:85f965ad853c569cf33eb934ee283f9b"
FFMPEG = "/tmp/ffmpeg-bin/ffmpeg"
LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo_story_hunt.png")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REELS_DIR = os.path.join(BASE_DIR, "assets", "reels")
CTX = ssl.create_default_context(cafile=certifi.where())

os.makedirs(REELS_DIR, exist_ok=True)

# Each reel: (video_prompt, intro_lines, headline_lines, red_highlight, product_lines, secondary_line)
REELS = [
    # 1. Apr 3 — SoHo
    {
        "video_prompt": "Cinematic slow tracking shot through SoHo cobblestone streets at golden hour dusk in NYC. Cast-iron facades, fire escapes, mist from manholes. Dark cinematic grading. Vertical 9:16.",
        "intro": ["Your phone buzzes.", "A message from someone", "you have never met."],
        "headline": ["The clue is hidden", "in this building.", "You have 90 seconds."],
        "highlight": ["A chat-based mystery walk", "through NYC. No guide. No bus."],
        "secondary": "Just you, your phone, and the city.",
        "filename": "reel-01-soho.mp4",
    },
    # 2. Apr 6 — Grand Central
    {
        "video_prompt": "Cinematic interior of Grand Central Terminal, camera slowly tilting up to reveal astronomical ceiling. Golden light through arched windows. Art deco details. Vertical 9:16.",
        "intro": ["The chat says:", "Go to the lower level.", "Find the tile that doesn't belong."],
        "headline": ["A secret platform", "61 feet below.", "Nobody knows it exists."],
        "highlight": ["An interactive adventure", "played entirely through your phone."],
        "secondary": "Real streets. Real clues. Real mystery.",
        "filename": "reel-02-grand-central.mp4",
    },
    # 3. Apr 7 — West Village
    {
        "video_prompt": "Cinematic slow dolly through narrow West Village streets at twilight. Brownstone buildings, iron railings, warm window lights, tree-lined sidewalks. Intimate atmosphere. Vertical 9:16.",
        "intro": ["New message received.", "The narrowest house in NYC", "is watching you."],
        "headline": ["9.5 feet wide.", "Three stories.", "One secret inside."],
        "highlight": ["Follow clues through the streets.", "Solve puzzles. Decode the city."],
        "secondary": "2-3 hours. No guide. Just the adventure.",
        "filename": "reel-03-west-village.mp4",
    },
    # 4. Apr 8 — Midtown alley
    {
        "video_prompt": "Cinematic POV walking through a narrow Midtown Manhattan alley. Tall buildings creating deep shadows. Camera moves forward, light at the end. Urban mystery. Vertical 9:16.",
        "intro": ["3:14 PM. Midtown.", "The chat sends you", "somewhere maps don't show."],
        "headline": ["Turn left.", "Into the alley.", "Now."],
        "highlight": ["Your phone is your guide.", "The city is the game board."],
        "secondary": "Every corner hides a clue.",
        "filename": "reel-04-midtown-alley.mp4",
    },
    # 5. Apr 9 — Whispering Gallery
    {
        "video_prompt": "Cinematic low angle of ornate tiled arches and vaulted ceiling in a grand train station. Warm ambient light, art deco patterns. Mysterious echoing atmosphere. Vertical 9:16.",
        "intro": ["Stand in the corner.", "Face the wall.", "Whisper."],
        "headline": ["Someone 30 feet away", "hears every word.", "The ceiling carries secrets."],
        "highlight": ["Discover what's hidden in", "the places you walk past every day."],
        "secondary": "A mystery walk unlike anything you've tried.",
        "filename": "reel-05-whispering.mp4",
    },
    # 6. Apr 10 — Bryant Park underground
    {
        "video_prompt": "Cinematic aerial descent over Bryant Park NYC, pushing down through autumn trees toward the lawn. Skyscrapers surrounding. Golden hour. Mysterious atmosphere. Vertical 9:16.",
        "intro": ["84,000 square feet.", "Hidden underground.", "Right beneath your feet."],
        "headline": ["The city has layers", "you've never seen.", "We'll show you."],
        "highlight": ["A chat-based adventure that", "takes you below the surface."],
        "secondary": "Free early access. Limited spots.",
        "filename": "reel-06-bryant-park.mp4",
    },
    # 7. Apr 13 — Harlem
    {
        "video_prompt": "Cinematic slow pan across Harlem brownstone block at sunset. Ornate cornices, fire escapes, golden light. Jazz era atmosphere, vintage street lamps. Vertical 9:16.",
        "intro": ["The jazz never stopped.", "You just stopped", "listening."],
        "headline": ["Cotton Club.", "Strivers' Row.", "The ghosts play on."],
        "highlight": ["Walk the streets where legends", "lived. Your phone tells the story."],
        "secondary": "Harlem like you've never experienced it.",
        "filename": "reel-07-harlem.mp4",
    },
    # 8. Apr 14 — Quote
    {
        "video_prompt": "Abstract cinematic NYC lights at night, slowly moving warm amber and cool blue bokeh circles. Out of focus city creating ethereal mysterious pattern. Slow motion. Vertical 9:16.",
        "intro": ["FIELD_NOTE //", "NYC_DISPATCH_042", ""],
        "headline": ["The city is not", "a place. It's a puzzle", "waiting to be decoded."],
        "highlight": ["StoryHunt. Coming soon.", ""],
        "secondary": "storyhunt.city",
        "filename": "reel-08-quote.mp4",
    },
    # 9. Apr 15 — Flatiron hidden bar
    {
        "video_prompt": "Cinematic shot of Flatiron Building at dusk, camera slowly orbiting the triangular building. Dramatic sky, moody lighting, urban mystery. Vertical 9:16.",
        "intro": ["No sign. No name.", "Just a door.", "Open since 1854."],
        "headline": ["The oldest bar", "in New York.", "Can you find it?"],
        "highlight": ["Your phone sends the clues.", "The city hides the answers."],
        "secondary": "An adventure that starts with a text.",
        "filename": "reel-09-flatiron.mp4",
    },
    # 10. Apr 16 — Brooklyn Bridge
    {
        "video_prompt": "Cinematic shot of Brooklyn Bridge stone arches from below, camera tilting up along massive granite towers. Golden hour light on cables. Dramatic scale. Vertical 9:16.",
        "intro": ["Inside the bridge.", "Behind the stone.", "A wine cellar. Sealed in 1876."],
        "headline": ["The city is full", "of locked doors.", "We have the keys."],
        "highlight": ["A mystery walk played", "through chat. 100% real locations."],
        "secondary": "No actors. No scripts. Just you and NYC.",
        "filename": "reel-10-brooklyn-bridge.mp4",
    },
    # 11. Apr 17 — DUMBO
    {
        "video_prompt": "Cinematic shot from DUMBO Brooklyn looking up at Manhattan Bridge framed between brick warehouses. Camera pushes forward. Moody overcast. Industrial aesthetic. Vertical 9:16.",
        "intro": ["Everyone photographs", "the bridge.", "Nobody looks underneath."],
        "headline": ["What's hidden", "in the shadows", "of DUMBO?"],
        "highlight": ["Get a clue. Follow it.", "Solve it. Get the next one."],
        "secondary": "The most immersive way to explore NYC.",
        "filename": "reel-11-dumbo.mp4",
    },
    # 12. Apr 20 — Mosaic trail
    {
        "video_prompt": "Cinematic extreme close-up of colorful ornate subway mosaic tiles in NYC, camera slowly pulling back to reveal pattern. Underground fluorescent light. Mysterious. Vertical 9:16.",
        "intro": ["New message:", "Look down.", "The first clue is under your feet."],
        "headline": ["Follow the", "mosaic trail.", "Don't lose it."],
        "highlight": ["A 2-hour adventure that turns", "NYC into an escape room."],
        "secondary": "Your phone is the only guide you need.",
        "filename": "reel-12-mosaic.mp4",
    },
    # 13. Apr 21 — City Hall Station
    {
        "video_prompt": "Cinematic shot of ornate abandoned underground space with tiled arches, chandeliers, Guastavino ceiling. Dim mysterious lighting, dust in light beams. Vertical 9:16.",
        "intro": ["Closed since 1945.", "Stained glass.", "Brass chandeliers. Underground."],
        "headline": ["There's a station", "under City Hall.", "You can see it."],
        "highlight": ["We take you to places", "most New Yorkers never find."],
        "secondary": "Chat-based. Self-guided. Unforgettable.",
        "filename": "reel-13-city-hall.mp4",
    },
    # 14. Apr 22 — Chrysler Building
    {
        "video_prompt": "Cinematic interior slowly tilting up inside grand Art Deco lobby with marble walls and elaborate painted ceiling mural. Golden lighting, geometric patterns. Vertical 9:16.",
        "intro": ["97 feet of painted ceiling.", "Right above your head.", "Almost nobody looks up."],
        "headline": ["The city rewards", "those who look", "closer."],
        "highlight": ["StoryHunt trains your eyes", "to see what others miss."],
        "secondary": "Every building has a story. Most are classified.",
        "filename": "reel-14-chrysler.mp4",
    },
    # 15. Apr 23 — Chelsea
    {
        "video_prompt": "Cinematic tracking shot through Chelsea gallery district NYC. White-walled galleries with glass windows. Evening light, art visible inside. Sophisticated urban atmosphere. Vertical 9:16.",
        "intro": ["200 galleries.", "10 blocks.", "One hidden message."],
        "headline": ["The Nabisco factory", "baked Oreos here.", "Now it hides something else."],
        "highlight": ["Walk. Solve. Discover.", "A mystery in every neighborhood."],
        "secondary": "Chelsea has never been explored like this.",
        "filename": "reel-15-chelsea.mp4",
    },
    # 16. Apr 24 — Quote 2
    {
        "video_prompt": "Cinematic timelapse clouds over NYC skyline at sunset to night. City lights turning on. Dramatic sky orange to blue to black. Urban atmosphere. Vertical 9:16.",
        "intro": ["FIELD_NOTE //", "NYC_DISPATCH_078", ""],
        "headline": ["Every building", "has a story.", "Most are classified."],
        "highlight": ["StoryHunt. Decode the city.", ""],
        "secondary": "storyhunt.city",
        "filename": "reel-16-quote2.mp4",
    },
    # 17. Apr 27 — Tribeca Ghostbusters
    {
        "video_prompt": "Cinematic shot of classic NYC fire station with red doors, camera slowly approaching. American flag, vintage architecture, afternoon shadows. Mysterious. Vertical 9:16.",
        "intro": ["Hook & Ladder 8.", "North Moore Street.", "Still answering calls since 1903."],
        "headline": ["The Ghostbusters", "firehouse is real.", "And we'll take you there."],
        "highlight": ["Real locations. Real history.", "Delivered through your phone."],
        "secondary": "Tribeca like you've never seen it.",
        "filename": "reel-17-tribeca.mp4",
    },
    # 18. Apr 28 — Central Park Ramble
    {
        "video_prompt": "Cinematic shot moving through dense forest path in Central Park. Dappled sunlight through thick canopy, winding stone path, wild vegetation. Mysterious woodland. Vertical 9:16.",
        "intro": ["38 acres of wilderness.", "In the middle of Manhattan.", "There's a cave."],
        "headline": ["Most New Yorkers", "have never found it.", "Will you?"],
        "highlight": ["A mystery walk that reveals", "what's hidden in plain sight."],
        "secondary": "Central Park has secrets. We know them.",
        "filename": "reel-18-central-park.mp4",
    },
    # 19. Apr 29 — Greenwich Village
    {
        "video_prompt": "Cinematic shot of Washington Square Park arch at dusk. Camera slowly approaches white marble arch. Warm lighting, bohemian atmosphere. Vertical 9:16.",
        "intro": ["The Beats wrote here.", "Stonewall started here.", "Dylan played his first gig here."],
        "headline": ["Three revolutions.", "Six blocks.", "One mystery walk."],
        "highlight": ["History comes alive when", "your phone tells the story."],
        "secondary": "Greenwich Village. Decoded.",
        "filename": "reel-19-greenwich.mp4",
    },
    # 20. Apr 30 — Architecture
    {
        "video_prompt": "Cinematic extreme low angle looking straight up at ornate Midtown Manhattan building facades. Gargoyles, architectural details. Camera slowly rotating. Dramatic perspective. Vertical 9:16.",
        "intro": ["The chat says:", "Look up.", "The answer is in the architecture."],
        "headline": ["You have", "90 seconds.", "Clock starts now."],
        "highlight": ["The most thrilling way", "to explore New York City."],
        "secondary": "Free early access at storyhunt.city",
        "filename": "reel-20-architecture.mp4",
    },
]


def fal_post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode(),
        headers={"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read())

def fal_get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Key {FAL_KEY}"})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read())

def download_file(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=CTX, timeout=120) as resp:
        with open(path, 'wb') as f:
            f.write(resp.read())


def submit_video(prompt):
    try:
        result = fal_post("https://queue.fal.run/fal-ai/minimax-video", {
            "prompt": prompt, "prompt_optimizer": True
        })
        return result.get("request_id")
    except Exception as e:
        print(f"    ERROR: {e}")
        return None


def wait_for_video(request_id):
    for _ in range(60):
        time.sleep(10)
        try:
            status = fal_get(f"https://queue.fal.run/fal-ai/minimax-video/requests/{request_id}/status")
            if status.get("status") == "COMPLETED":
                result = fal_get(f"https://queue.fal.run/fal-ai/minimax-video/requests/{request_id}")
                return result.get("video", {}).get("url")
            elif status.get("status") == "FAILED":
                return None
        except:
            pass
    return None


def brand_video(raw_path, out_path, reel):
    intro = reel["intro"]
    hl = reel["headline"]
    hi = reel["highlight"]
    sec = reel["secondary"]

    # Pad arrays to 3 elements
    while len(intro) < 3: intro.append("")
    while len(hl) < 3: hl.append("")
    while len(hi) < 2: hi.append("")

    filters = f"""
    [0:v]crop=in_h*9/16:in_h,scale=1080:1920[bg];
    [1:v]scale=240:-1[logo];
    [bg]drawbox=x=0:y=0:w=iw:h=ih:color=black@0.5:t=fill[dark];
    [dark][logo]overlay=W-280:50[wl];
    [wl]
    drawtext=text='{intro[0]}':fontfile=/System/Library/Fonts/SFMono-Regular.otf:fontsize=30:fontcolor=0x00d2ff:x=60:y=h/2-300,
    drawtext=text='{intro[1]}':fontfile=/System/Library/Fonts/SFMono-Regular.otf:fontsize=30:fontcolor=0x00d2ff:x=60:y=h/2-260,
    drawtext=text='{intro[2]}':fontfile=/System/Library/Fonts/SFMono-Regular.otf:fontsize=30:fontcolor=0x00d2ff:x=60:y=h/2-220,
    drawtext=text='{hl[0]}':fontfile=/System/Library/Fonts/SFNS.ttf:fontsize=76:fontcolor=white:x=60:y=h/2-130,
    drawtext=text='{hl[1]}':fontfile=/System/Library/Fonts/SFNS.ttf:fontsize=76:fontcolor=white:x=60:y=h/2-46,
    drawtext=text='{hl[2]}':fontfile=/System/Library/Fonts/SFNS.ttf:fontsize=76:fontcolor=0xff0033:x=60:y=h/2+38,
    drawbox=x=40:y=h/2+160:w=960:h=130:color=0xff0033@0.9:t=fill,
    drawtext=text='{hi[0]}':fontfile=/System/Library/Fonts/SFMono-Bold.otf:fontsize=32:fontcolor=white:x=80:y=h/2+180,
    drawtext=text='{hi[1]}':fontfile=/System/Library/Fonts/SFMono-Bold.otf:fontsize=32:fontcolor=white:x=80:y=h/2+220,
    drawbox=x=40:y=h/2+310:w=960:h=70:color=0x00d2ff@0.15:t=fill,
    drawtext=text='{sec}':fontfile=/System/Library/Fonts/SFNS.ttf:fontsize=30:fontcolor=white@0.8:x=80:y=h/2+328,
    drawtext=text='FREE EARLY ACCESS':fontfile=/System/Library/Fonts/SFMono-Bold.otf:fontsize=36:fontcolor=0xff0033:x=(w-370)/2:y=h-240,
    drawtext=text='storyhunt.city':fontfile=/System/Library/Fonts/SFMono-Regular.otf:fontsize=28:fontcolor=white@0.6:x=(w-230)/2:y=h-190
    """

    result = subprocess.run([
        FFMPEG, "-y", "-i", raw_path, "-i", LOGO,
        "-filter_complex", filters,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-an", out_path
    ], capture_output=True, timeout=60, text=True)

    return os.path.exists(out_path) and os.path.getsize(out_path) > 50000


def main():
    total = len(REELS)
    print(f"{'='*60}")
    print(f"StoryHunt Branded Reel Generator — {total} videos")
    print(f"Est. cost: ~${total * 0.50:.2f} | Est. time: ~{total * 4} min")
    print(f"{'='*60}")

    batch_size = 3
    ok = 0

    for batch_start in range(0, total, batch_size):
        batch = REELS[batch_start:batch_start+batch_size]
        batch_indices = list(range(batch_start, batch_start+len(batch)))
        print(f"\n--- Batch {batch_start//batch_size+1}: reels {batch_indices[0]+1}-{batch_indices[-1]+1} ---")

        # Skip already done
        jobs = []
        for i, reel in zip(batch_indices, batch):
            out_path = os.path.join(REELS_DIR, reel["filename"])
            if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
                print(f"  SKIP {reel['filename']} — already exists")
                ok += 1
                jobs.append(None)
                continue

            print(f"  Submitting {reel['filename']}...")
            req_id = submit_video(reel["video_prompt"])
            jobs.append((req_id, reel, out_path))

        # Wait and process
        for job in jobs:
            if job is None:
                continue
            req_id, reel, out_path = job
            if not req_id:
                print(f"  FAIL {reel['filename']} — no request ID")
                continue

            print(f"  Waiting for {reel['filename']}...")
            video_url = wait_for_video(req_id)
            if not video_url:
                print(f"  FAIL {reel['filename']} — video generation failed")
                continue

            raw_path = os.path.join(tempfile.gettempdir(), f"raw-{reel['filename']}")
            print(f"  Downloading raw video...")
            download_file(video_url, raw_path)

            print(f"  Branding with FFmpeg...")
            if brand_video(raw_path, out_path, reel):
                size = os.path.getsize(out_path)
                print(f"  OK  {reel['filename']} ({size:,} bytes)")
                ok += 1
            else:
                print(f"  FAIL {reel['filename']} — FFmpeg error")

            # Cleanup raw
            try: os.unlink(raw_path)
            except: pass

    print(f"\n{'='*60}")
    print(f"Completed: {ok}/{total}")
    print(f"Output: {REELS_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
