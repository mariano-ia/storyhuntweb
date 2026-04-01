#!/usr/bin/env python3
"""
Batch upgrade script for StoryHunt /explore/ pages.
Adds: nav, manifesto, inline form, social proof, trust signals.
Preserves: unique title, meta, h1, subtitle, CTA text, footer text, JSON-LD.
Fixes: em dashes replaced with periods.
"""

import os
import re
import glob

EXPLORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore')

def extract(html, pattern, group=1, default=''):
    """Extract first regex match from HTML."""
    m = re.search(pattern, html, re.DOTALL)
    return m.group(group).strip() if m else default

def fix_dashes(text):
    """Replace em dashes with periods."""
    return text.replace('—', '. ').replace('  ', ' ')

def get_template(meta_desc, meta_keywords, og_url, og_title, og_desc, title,
                 json_ld, h1_text, subtitle, btn_text, footer_line1, footer_line2):
    """Generate the upgraded page HTML."""

    # JSON-LD block (only if original had one)
    json_ld_block = ''
    if json_ld:
        json_ld_block = f"""
    <script type="application/ld+json">
    {json_ld}
    </script>"""

    # OG description (only if original had one)
    og_desc_tag = ''
    if og_desc:
        og_desc_tag = f"""
    <meta property="og:description"
        content="{og_desc}">"""

    return f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
        content="{meta_desc}">
    <meta name="keywords"
        content="{meta_keywords}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{og_url}">
    <meta property="og:title" content="{og_title}">{og_desc_tag}

    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap"
        rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
    <link rel="icon"
        href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><circle cx=%2250%22 cy=%2250%22 r=%2240%22 fill=%22%23ff0033%22/></svg>">{json_ld_block}

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-4EWN9RMYR9"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-4EWN9RMYR9');
    </script>
</head>

<body class="loading">
    <div class="noise-overlay"></div>
    <div class="grain-overlay"></div>
    <div class="video-background">
        <div class="video-overlay"></div>
    </div>
    <div class="map-grid"></div>

    <nav class="nav">
        <div class="container flex-nav">
            <a href="../index.html" class="logo-link">
                <img src="../assets/logo_story_hunt.png" alt="StoryHunt Logo" class="main-logo">
            </a>
            <div class="nav-links">
                <a href="../index.html#experiences">EXPERIENCES</a>
                <a href="../index.html#gallery">GALLERY</a>
                <a href="../index.html#testimonials">HUNTERS</a>
            </div>
            <div class="nav-right">
                <a href="#cta" class="nav-cta-btn mono">BOOK_NOW</a>
            </div>
        </div>
    </nav>

    <main id="main-content">
        <!-- Hero Section -->
        <section class="hero" id="hero">
            <div class="container">
                <div class="glitch-wrapper">
                    <h1 class="glitch reveal-text" data-text="{h1_text}">{h1_text}</h1>
                </div>
                <p class="subtitle reveal-text">{subtitle}</p>

                <div class="system-status reveal-text" style="--d: 0.5s">
                    <div class="status-block mono">
                        <span class="label">SYSTEM_LAUNCH:</span>
                        <span class="value accent" id="countdown-days">CALCULATING...</span>
                    </div>
                    <div class="status-divider"></div>
                    <div class="status-block mono">
                        <span class="label">FREE_ACCESS_GRANTS:</span>
                        <span class="value electric-blue" id="spots-counter">100 / 100</span>
                    </div>
                </div>

                <div class="hero-actions reveal-text" style="--d: 0.8s">
                    <a href="#cta" class="primary-btn mono">
                        <span class="btn-text">{btn_text}</span>
                        <span class="btn-hover">SECURE_YOUR_SPOT</span>
                    </a>
                </div>
            </div>
        </section>

        <!-- How It Works -->
        <section class="manifesto" id="how-it-works">
            <div class="container smaller">
                <div class="manifesto-grid">
                    <div class="manifesto-item reveal-text" style="--d: 0.1s">
                        <span class="step-num mono">[01]</span>
                        <p>Pick a city. Choose a story. <span class="accent">You receive a curated mystery mission set in a real neighborhood.</span></p>
                    </div>
                    <div class="manifesto-item reveal-text" style="--d: 0.2s">
                        <span class="step-num mono">[02]</span>
                        <p>Follow clues through the streets. <span class="accent">Everything happens via chat. Your phone sends you clues, riddles, and directions to hidden spots, secret doors, and forgotten places.</span></p>
                    </div>
                    <div class="manifesto-item reveal-text" style="--d: 0.3s">
                        <span class="step-num mono">[03]</span>
                        <p>Solve the puzzle. Live the legend. <span class="accent">2-3 hours of immersive adventure. No guide. No bus. Just you and the city.</span></p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Call to Action -->
        <section class="cta" id="cta">
            <div class="container smaller">
                <h2 class="reveal-text">Ready to Hunt?</h2>
                <p class="section-subtitle mono reveal-text" style="--d: 0.1s">
                    LEAVE_YOUR_EMAIL. AS_SOON_AS_WE_GO_LIVE, YOU_GET_FREE_ACCESS.
                </p>
                <form action="https://storyhunt-app.vercel.app/api/contacts" method="POST"
                    class="recruitment-form reveal-text" style="--d: 0.2s">
                    <div class="input-group">
                        <input type="email" name="email" placeholder="EMAIL_ADDRESS" required id="email" class="mono">
                        <button type="submit" class="submit-btn mono">
                            <span class="btn-text">REQUEST_ACCESS</span>
                            <span class="btn-hover">EXECUTE_REQUEST</span>
                        </button>
                    </div>
                </form>

                <!-- Social Proof Counter -->
                <div class="social-proof reveal-text" style="--d: 0.4s">
                    <div class="avatar-stack">
                        <span class="stack-avatar" style="background: #ff0033;">MK</span>
                        <span class="stack-avatar" style="background: #00d2ff;">JR</span>
                        <span class="stack-avatar" style="background: #00ff66;">AL</span>
                        <span class="stack-avatar" style="background: #ff6600;">TS</span>
                        <span class="stack-avatar" style="background: #cc00ff;">ND</span>
                        <span class="stack-avatar" style="background: #ffcc00; color: #000;">WP</span>
                    </div>
                    <div class="social-proof-text">
                        <span class="social-proof-count">500+</span>
                        <span class="social-proof-label mono">HUNTERS_COMPLETED_THE_MISSION</span>
                    </div>
                </div>

                <div class="trust-signals mono reveal-text" style="--d: 0.5s">
                    <span>NO_SPAM_EVER</span>
                    <span>INSTANT_CONFIRMATION</span>
                    <span>FREE_CANCELLATION</span>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container flex-footer">
            <div class="footer-left mono">
                <p>{footer_line1}</p>
                <p>{footer_line2}</p>
            </div>
            <div class="footer-right mono">
                <p>STORYHUNT &copy;</p>
                <p class="made-by">MADE_BY_<a href="https://www.yacare.io" target="_blank"
                        rel="noopener noreferrer">YACAR&Eacute;</a></p>
            </div>
        </div>
    </footer>

    <script src="../main.js"></script>
</body>

</html>'''


def process_file(filepath):
    """Process a single explore page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    filename = os.path.basename(filepath)

    # Extract unique content
    meta_desc = extract(html, r'<meta name="description"\s*content="([^"]*)"')
    if not meta_desc:
        meta_desc = extract(html, r'<meta name="description"[^>]*\n\s*content="([^"]*)"')

    meta_keywords = extract(html, r'<meta name="keywords"\s*content="([^"]*)"')
    if not meta_keywords:
        meta_keywords = extract(html, r'<meta name="keywords"[^>]*\n\s*content="([^"]*)"')

    og_url = extract(html, r'<meta property="og:url" content="([^"]*)"')
    og_title = extract(html, r'<meta property="og:title" content="([^"]*)"')
    og_desc = extract(html, r'<meta property="og:description"\s*content="([^"]*)"', default=None)
    if og_desc is None:
        og_desc = extract(html, r'<meta property="og:description"[^>]*\n\s*content="([^"]*)"', default=None)

    title = extract(html, r'<title>([^<]*)</title>')

    # JSON-LD
    json_ld = extract(html, r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', default=None)

    # H1 text
    h1_text = extract(html, r'data-text="([^"]*)"')

    # Subtitle - handle multi-line
    subtitle = extract(html, r'<p class="subtitle reveal-text">(.*?)</p>')
    subtitle = re.sub(r'\s+', ' ', subtitle).strip()

    # Button text
    btn_text = extract(html, r'class="btn-text">([^<]*)</span>')

    # Footer lines
    footer_left = re.search(r'<div class="footer-left mono">\s*<p>(.*?)</p>\s*<p>(.*?)</p>', html, re.DOTALL)
    footer_line1 = footer_left.group(1).strip() if footer_left else 'LOCATION: NYC'
    footer_line2 = footer_left.group(2).strip() if footer_left else 'STATUS: EXPLORING'

    # Fix dashes everywhere
    meta_desc = fix_dashes(meta_desc)
    og_title = fix_dashes(og_title)
    if og_desc:
        og_desc = fix_dashes(og_desc)
    title = fix_dashes(title)
    h1_text = fix_dashes(h1_text)
    subtitle = fix_dashes(subtitle)

    # Generate new page
    new_html = get_template(
        meta_desc=meta_desc,
        meta_keywords=meta_keywords,
        og_url=og_url,
        og_title=og_title,
        og_desc=og_desc,
        title=title,
        json_ld=json_ld,
        h1_text=h1_text,
        subtitle=subtitle,
        btn_text=btn_text,
        footer_line1=footer_line1,
        footer_line2=footer_line2
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return filename


def main():
    files = sorted(glob.glob(os.path.join(EXPLORE_DIR, '*.html')))
    print(f"Found {len(files)} explore pages to upgrade.\n")

    success = 0
    errors = []

    for filepath in files:
        try:
            filename = process_file(filepath)
            print(f"  OK  {filename}")
            success += 1
        except Exception as e:
            filename = os.path.basename(filepath)
            print(f"  ERR {filename}: {e}")
            errors.append((filename, str(e)))

    print(f"\nDone: {success}/{len(files)} upgraded successfully.")
    if errors:
        print(f"Errors ({len(errors)}):")
        for name, err in errors:
            print(f"  - {name}: {err}")


if __name__ == '__main__':
    main()
