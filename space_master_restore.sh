#!/usr/bin/env bash
# ==============================================================================
# S.P.A.C.E. Master Ecosystem & Network Restoration Script
# Commander: Michael C. Sims
# Target: Node SPACE (~/space_web)
# ==============================================================================

set -e

WORKSPACE_DIR="$HOME/space_web"
LOG_FILE="$WORKSPACE_DIR/isot_sync_daemon.log"

echo "================================================================================"
echo "[*] S.P.A.C.E. MASTER RESTORATION & AUTONOMY SEQUENCE INITIATED"
echo "================================================================================"

# 1. Permanent DNS Fix & Resolution Lock
echo "[*] Locking WSL DNS resolvers (Google 8.8.8.8 & Cloudflare 1.1.1.1)..."
sudo bash -c 'echo -e "[network]\ngenerateResolvConf = false" > /etc/wsl.conf'
sudo rm -f /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "nameserver 1.1.1.1" >> /etc/resolv.conf'

# 2. Verify Workspace & Network Reachability
if [ -d "$WORKSPACE_DIR" ]; then
cd "$WORKSPACE_DIR"
echo "[✓] Navigated to workspace: $WORKSPACE_DIR"
else
echo "[!] Workspace not found. Creating $WORKSPACE_DIR..."
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"
fi

echo "[*] Testing hostname resolution for github.com..."
if host github.com >/dev/null 2>&1; then
echo "[✓] DNS resolution successful for github.com."
else
echo "[!] DNS warning: host lookup delayed, proceeding with push retry..."
fi

# 3. Synchronize Git State & Flush Queued Commits
echo "[*] Auditing Git repository status..."
git status -s

if [ -n "$(git status --porcelain)" ]; then
echo "[*] Staging and committing pending local changes..."
git add .
git commit -m "Master Ecosystem Restoration Sync: $(date -u +'%Y-%m-%d %H:%M:%S UTC')" || true
fi

echo "[*] Pushing queued commits to origin main..."
git push origin main && echo "[✓] Successfully flushed commits to remote repository!" || echo "[!] Push deferred; check authentication token or remote URL."

# 4. Launch or Verify Background Auto-Sync Daemon (`isot_sync_daemon.sh`)
echo "[*] Managing background sync daemon..."
if pgrep -f "isot_sync_daemon.sh" > /dev/null; then
echo "[✓] isot_sync_daemon.sh is already running in the background."
else
if [ -f "./isot_sync_daemon.sh" ]; then
    chmod +x isot_sync_daemon.sh
    nohup ./isot_sync_daemon.sh > "$LOG_FILE" 2>&1 &
    echo "[✓] Launched isot_sync_daemon.sh in background (PID: $!)."
else
    echo "[!] isot_sync_daemon.sh not found in workspace."
fi
fi

# 5. Final Efficiency & Health Audit Readout
echo "================================================================================"
echo "[+] S.P.A.C.E. SYSTEM HEALTH READOUT (100% EFFICIENCY TARGET):"
echo "    - Working Branch: $(git branch --show-current)"
echo "    - Latest Commit:  $(git log -n 1 --oneline)"
if [ -f "isot_ledger.json" ]; then
RECORD_COUNT=$(python3 -c "import json; ledger=json.load(open('isot_ledger.json')); print(ledger.get('total_records', len(ledger.get('chat_records', []))))" 2>/dev/null || echo "Unknown")
echo "    - ISOT Records:   $RECORD_COUNT active entries indexed"
fi
echo "    - Daemon Status:  $(pgrep -f "isot_sync_daemon.sh" > /dev/null && echo "ONLINE (100% Efficiency)" || echo "OFFLINE")"
echo "================================================================================"
