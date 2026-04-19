#!/usr/bin/env python3
"""
Send email notifications via Resend (reusing StoryHuntABM env vars).

Usage:
    python3 notify.py success "Published 25 pages today"
    python3 notify.py error "Git push failed: [error details]"
    python3 notify.py summary "Today's run generated 25 pages, 2 errors"
"""
import os
import sys
import json
import ssl
import urllib.request
import urllib.error

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()


def load_env():
    """Load Resend credentials from StoryHuntABM .env.local."""
    env = {}
    paths = [
        os.path.expanduser("~/Desktop/Antigravity/StoryHuntABM/.env.local"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "StoryHuntABM", ".env.local"),
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            break
    return env


def send_email(subject, body_html, level="info"):
    """Send email via Resend API. Returns True on success."""
    env = load_env()
    api_key = env.get("RESEND_API_KEY")
    to_email = env.get("NOTIFICATION_EMAIL", "marianonoceti@gmail.com")

    if not api_key:
        print("ERROR: RESEND_API_KEY not found", file=sys.stderr)
        return False

    # Subject prefix by level
    prefixes = {
        "error": "🚨 [SEO Cron]",
        "warning": "⚠️ [SEO Cron]",
        "success": "✅ [SEO Cron]",
        "info": "[SEO Cron]",
    }
    prefix = prefixes.get(level, "[SEO Cron]")
    full_subject = f"{prefix} {subject}"

    payload = {
        "from": "StoryHunt SEO <hello@storyhunt.city>",
        "to": [to_email],
        "subject": full_subject,
        "html": body_html,
    }

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "storyhunt-seo-pipeline/1.0",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
            if resp.status in (200, 201, 202):
                print(f"Email sent: {full_subject}")
                return True
            else:
                print(f"Email failed: HTTP {resp.status}", file=sys.stderr)
                return False
    except urllib.error.HTTPError as e:
        print(f"Email HTTP error: {e.code} — {e.read().decode()}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Email error: {e}", file=sys.stderr)
        return False


def build_error_email(title, details, log_tail=""):
    """Build HTML body for error notification."""
    return f"""
    <div style="font-family:-apple-system,sans-serif;max-width:600px">
      <h2 style="color:#d32f2f">SEO Cron Failed</h2>
      <p><strong>{title}</strong></p>
      <pre style="background:#f5f5f5;padding:12px;border-left:3px solid #d32f2f;white-space:pre-wrap;font-size:13px">{details}</pre>
      {'<h3>Recent log output:</h3><pre style="background:#f5f5f5;padding:12px;font-size:11px;white-space:pre-wrap">' + log_tail + '</pre>' if log_tail else ''}
      <hr>
      <p style="color:#666;font-size:12px">
        Machine: {os.uname().nodename}<br>
        Log file: ~/Desktop/Antigravity/StoryHuntWeb/seo-pipeline/publish.log<br>
        To debug: <code>cd ~/Desktop/Antigravity/StoryHuntWeb &amp;&amp; bash seo-pipeline/daily-publish.sh</code>
      </p>
    </div>
    """


def build_success_email(pages_published, pending_left, run_details=""):
    """Build HTML body for success notification."""
    try:
        pending_n = int(pending_left)
        eta = max(1, pending_n // 25)
    except (ValueError, TypeError):
        eta = "?"
    return f"""
    <div style="font-family:-apple-system,sans-serif;max-width:600px">
      <h2 style="color:#2e7d32">SEO Cron: Published {pages_published} pages</h2>
      <table style="border-collapse:collapse;margin:16px 0">
        <tr><td style="padding:6px 12px"><strong>Published today</strong></td><td style="padding:6px 12px">{pages_published}</td></tr>
        <tr><td style="padding:6px 12px"><strong>Pending queue</strong></td><td style="padding:6px 12px">{pending_left} pages</td></tr>
      </table>
      {'<h3>Details:</h3><pre style="background:#f5f5f5;padding:12px;font-size:12px;white-space:pre-wrap">' + run_details + '</pre>' if run_details else ''}
      <p style="color:#666;font-size:12px">At current pace (~25/day), queue clears in ~{eta} days.</p>
    </div>
    """


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: notify.py <level> <subject> [details]")
        print("  level: error | warning | success | info")
        sys.exit(1)

    level = sys.argv[1]
    subject = sys.argv[2]
    details = sys.argv[3] if len(sys.argv) > 3 else ""

    log_tail = ""
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish.log")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            lines = f.readlines()
        log_tail = "".join(lines[-30:])

    if level == "error":
        body = build_error_email(subject, details, log_tail)
    elif level == "success":
        body = build_success_email(
            pages_published=details.split("|")[0] if "|" in details else details,
            pending_left=details.split("|")[1] if "|" in details else "?",
            run_details=log_tail[-1500:],
        )
    else:
        body = f"<p>{details}</p><pre>{log_tail}</pre>"

    ok = send_email(subject, body, level=level)
    sys.exit(0 if ok else 1)
