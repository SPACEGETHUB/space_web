#!/bin/bash
TARGET_REPO="$HOME/space_web"
LOG_FILE="$HOME/space_web/isot_sync_daemon.log"
LOCK_FILE="/tmp/isot_sync_daemon.lock"
POLL_INTERVAL=60

# Prevent duplicate daemon instances
if [ -f "$LOCK_FILE" ] && kill -0 $(cat "$LOCK_FILE") 2>/dev/null; then
    exit 0
fi
echo $$ > "$LOCK_FILE"

echo "[*] S.P.A.C.E. Live ISOT Sync Daemon active at $(date +'%d/%m/%Y %H:%M:%S')" >> "$LOG_FILE"

while true; do
    cd "$TARGET_REPO" || { sleep "$POLL_INTERVAL"; continue; }

    if [[ -n $(git status -s) ]]; then
        TIMESTAMP=$(date +'%d/%m/%Y %H:%M:%S')
        git add .
        git commit -m "ISOT Auto-Sync: $TIMESTAMP" >> "$LOG_FILE" 2>&1
        if git push origin main >> "$LOG_FILE" 2>&1; then
            echo "[+] Synced to ISOT/Cube at $TIMESTAMP" >> "$LOG_FILE"
        else
            echo "[!] Push deferred at $TIMESTAMP (will retry)" >> "$LOG_FILE"
        fi
    fi
    sleep "$POLL_INTERVAL"
done
