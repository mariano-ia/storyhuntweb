#!/bin/bash
# StoryHunt SEO Pipeline — Daily Publisher with robust error handling
# - Generates up to 25 pages/day (50+ if catch-up needed)
# - Sends macOS notification on success AND failure
# - Optional: pings healthchecks.io for uptime monitoring
# - Never silently fails — errors are logged and alerted

PIPELINE_DIR="$(cd "$(dirname "$0")" && pwd)"
WEB_DIR="$(dirname "$PIPELINE_DIR")"
LOG_FILE="$PIPELINE_DIR/publish.log"
STATE_FILE="$PIPELINE_DIR/.last_run"
BATCH_SIZE=25

# Optional: set HEALTHCHECKS_URL in your environment to ping healthchecks.io
# Example: export HEALTHCHECKS_URL="https://hc-ping.com/YOUR-UUID"
HEALTHCHECKS_URL="${HEALTHCHECKS_URL:-}"

cd "$WEB_DIR" || exit 1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

notify() {
    # macOS native notification
    local title="$1"
    local message="$2"
    local sound="${3:-default}"
    osascript -e "display notification \"$message\" with title \"StoryHunt SEO\" subtitle \"$title\" sound name \"$sound\"" 2>/dev/null || true
}

notify_email() {
    # Email via Resend
    local level="$1"
    local subject="$2"
    local details="${3:-}"
    python3 "$PIPELINE_DIR/notify.py" "$level" "$subject" "$details" 2>&1 | tee -a "$LOG_FILE" || true
}

ping_healthcheck() {
    local status="${1:-success}"
    if [ -n "$HEALTHCHECKS_URL" ]; then
        if [ "$status" = "success" ]; then
            curl -fsS --retry 3 -m 10 "$HEALTHCHECKS_URL" > /dev/null 2>&1 || true
        else
            curl -fsS --retry 3 -m 10 "$HEALTHCHECKS_URL/fail" > /dev/null 2>&1 || true
        fi
    fi
}

on_error() {
    local exit_code=$?
    local line_no=$1
    local msg="Script failed at line $line_no (exit $exit_code)"
    log "ERROR: $msg"
    notify "FAILED" "$msg — check publish.log" "Basso"
    notify_email "error" "Pipeline crashed" "$msg"
    ping_healthcheck "fail"
    exit $exit_code
}

trap 'on_error $LINENO' ERR

log "=== Starting daily SEO publish ==="
ping_healthcheck "start" 2>/dev/null || true

# Check if previous days were missed → increase batch
if [ -f "$STATE_FILE" ]; then
    last_run=$(cat "$STATE_FILE")
    today=$(date '+%Y-%m-%d')
    if [[ "$last_run" != "$today" ]]; then
        # Calculate days since last run
        if days_missed=$(( ($(date -j -f '%Y-%m-%d' "$today" '+%s') - $(date -j -f '%Y-%m-%d' "$last_run" '+%s')) / 86400 )) 2>/dev/null; then
            if [ "$days_missed" -gt 1 ]; then
                BATCH_SIZE=$((BATCH_SIZE * days_missed))
                # Cap at 100 to avoid SERP flagging
                if [ "$BATCH_SIZE" -gt 100 ]; then
                    BATCH_SIZE=100
                fi
                log "Missed $days_missed day(s). Batch size: $BATCH_SIZE"
            fi
        fi
    fi
fi

# Step 1: Rebuild config (expands dimensions, adds new pending pages)
log "Rebuilding config..."
python3 "$PIPELINE_DIR/build_config.py" 2>&1 | tee -a "$LOG_FILE"

# Step 2: Sync state with disk (in case files exist but config doesn't know)
python3 "$PIPELINE_DIR/sync_state.py" 2>&1 | tee -a "$LOG_FILE" || true

# Step 3: Count pending
pending=$(python3 -c "
import json
c = json.load(open('$PIPELINE_DIR/config.json'))
print(sum(1 for p in c['pages'] if p['status'] == 'pending'))
")
log "Pending pages: $pending"

if [ "$pending" -eq 0 ]; then
    log "No pending pages."
    date '+%Y-%m-%d' > "$STATE_FILE"
    notify "OK" "No pending pages. All up to date."
    ping_healthcheck "success"
    exit 0
fi

# Adjust batch if fewer pending
if [ "$pending" -lt "$BATCH_SIZE" ]; then
    BATCH_SIZE=$pending
fi

# Step 4: Pull latest first (with stash protection for unstaged changes)
log "Pulling latest from origin..."
stash_needed=0
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
    git stash push -u -m "cron-auto-stash-$(date +%s)" 2>&1 | tee -a "$LOG_FILE" && stash_needed=1
fi
git pull --rebase origin main 2>&1 | tee -a "$LOG_FILE" || {
    log "WARNING: git pull failed. Continuing anyway."
}
if [ "$stash_needed" = "1" ]; then
    git stash pop 2>&1 | tee -a "$LOG_FILE" || log "WARNING: stash pop had conflicts"
fi

# Step 5: Generate pages
log "Generating $BATCH_SIZE pages..."
python3 "$PIPELINE_DIR/generate.py" --limit "$BATCH_SIZE" 2>&1 | tee -a "$LOG_FILE"

# Step 6: Check git status for actual changes
modified=$(git status -s explore/ sitemap.xml seo-pipeline/config.json 2>/dev/null | wc -l | tr -d ' ')

if [ "$modified" -eq 0 ]; then
    log "No changes to commit."
    date '+%Y-%m-%d' > "$STATE_FILE"
    notify "OK" "Generated nothing new (already up to date)"
    ping_healthcheck "success"
    exit 0
fi

# Step 7: Commit + push
new_files=$(git status -s explore/ | grep -c '^??' || echo 0)
log "Committing changes ($new_files new files)..."
git add explore/*.html sitemap.xml seo-pipeline/config.json
git commit -m "seo: auto-publish $new_files programmatic pages ($(date '+%Y-%m-%d'))" 2>&1 | tee -a "$LOG_FILE"

log "Pushing to origin..."
if ! git push origin main 2>&1 | tee -a "$LOG_FILE"; then
    log "ERROR: git push failed"
    notify "PUSH FAILED" "$new_files pages committed locally but not pushed" "Basso"
    notify_email "error" "Git push failed" "$new_files pages committed locally but push to origin/main failed. Run 'git push' manually to recover."
    ping_healthcheck "fail"
    exit 1
fi

# Step 8: Update state and notify
date '+%Y-%m-%d' > "$STATE_FILE"

# Count remaining pending
pending_left=$(python3 -c "
import json
c = json.load(open('$PIPELINE_DIR/config.json'))
print(sum(1 for p in c['pages'] if p['status'] == 'pending'))
")

log "Done. Published $new_files pages."
log "=== Finished ==="
notify "OK" "Published $new_files new SEO pages"
notify_email "success" "Published $new_files pages" "$new_files|$pending_left"
ping_healthcheck "success"
