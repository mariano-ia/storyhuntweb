#!/bin/bash
# StoryHunt SEO Pipeline — Daily Publisher
# Generates up to 25 pages/day (50 if yesterday was missed)
# Designed to run via launchd daily

set -e

PIPELINE_DIR="$(cd "$(dirname "$0")" && pwd)"
WEB_DIR="$(dirname "$PIPELINE_DIR")"
LOG_FILE="$PIPELINE_DIR/publish.log"
STATE_FILE="$PIPELINE_DIR/.last_run"
BATCH_SIZE=25

cd "$WEB_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Starting daily SEO publish ==="

# Check if yesterday was missed → double batch
if [ -f "$STATE_FILE" ]; then
    last_run=$(cat "$STATE_FILE")
    yesterday=$(date -v-1d '+%Y-%m-%d')
    if [[ "$last_run" < "$yesterday" ]]; then
        days_missed=$(( ($(date '+%s') - $(date -j -f '%Y-%m-%d' "$last_run" '+%s')) / 86400 ))
        if [ "$days_missed" -gt 1 ]; then
            BATCH_SIZE=$((BATCH_SIZE * days_missed))
            # Cap at 100 to avoid spamming
            if [ "$BATCH_SIZE" -gt 100 ]; then
                BATCH_SIZE=100
            fi
            log "Missed $days_missed day(s). Batch size increased to $BATCH_SIZE"
        fi
    fi
fi

# Step 1: Expand config with new pages (if build_config adds new dimensions)
log "Rebuilding config..."
python3 "$PIPELINE_DIR/build_config.py" 2>&1 | tee -a "$LOG_FILE"

# Step 2: Count pending pages
pending=$(python3 -c "
import json
c = json.load(open('$PIPELINE_DIR/config.json'))
print(sum(1 for p in c['pages'] if p['status'] == 'pending'))
")
log "Pending pages: $pending"

if [ "$pending" -eq 0 ]; then
    log "No pending pages. Nothing to do."
    date '+%Y-%m-%d' > "$STATE_FILE"
    exit 0
fi

# Adjust batch if fewer pending than batch size
if [ "$pending" -lt "$BATCH_SIZE" ]; then
    BATCH_SIZE=$pending
fi

# Step 3: Generate pages
log "Generating $BATCH_SIZE pages..."
python3 "$PIPELINE_DIR/generate.py" --limit "$BATCH_SIZE" 2>&1 | tee -a "$LOG_FILE"

# Step 4: Check if anything was actually generated
new_files=$(git status -s explore/ | grep '^?' | wc -l | tr -d ' ')
modified_files=$(git status -s explore/ sitemap.xml seo-pipeline/config.json | wc -l | tr -d ' ')

if [ "$modified_files" -eq 0 ]; then
    log "No new files generated. Skipping commit."
    date '+%Y-%m-%d' > "$STATE_FILE"
    exit 0
fi

# Step 5: Commit and push
log "Committing $new_files new pages..."
git add explore/*.html sitemap.xml seo-pipeline/config.json
git commit -m "seo: auto-publish $new_files programmatic pages ($(date '+%Y-%m-%d'))" 2>&1 | tee -a "$LOG_FILE"
git push origin main 2>&1 | tee -a "$LOG_FILE"

# Step 6: Update state
date '+%Y-%m-%d' > "$STATE_FILE"
log "Done. Published $new_files pages."
log "=== Finished ==="
