#!/usr/bin/env bash
set -e
WORKSPACE_DIR="$HOME/space_web"
LOG_FILE="$WORKSPACE_DIR/isot_sync_daemon.log"
echo "================================================================================"
echo "[*] S.P.A.C.E. ALL-IN-ONE RESTORATION SEQUENCE INITIATED"
echo "================================================================================"
sudo bash -c 'echo -e "[network]\ngenerateResolvConf = false" > /etc/wsl.conf'
sudo rm -f /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "nameserver 1.1.1.1" >> /etc/resolv.conf'
cd "$WORKSPACE_DIR"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/SPACEGETHUB/space_web.git
git config --global credential.helper store
git add .
git commit -m "Master Restoration Sync: $(date -u +'%Y-%m-%d %H:%M:%S UTC')" || true
git push -u origin main && echo "[✓] Successfully flushed commits!" || echo "[!] Push deferred."
pkill -f "isot_sync_daemon.sh" || true
nohup ./isot_sync_daemon.sh > "$LOG_FILE" 2>&1 &
echo "[✓] Daemon online (PID: $!)."
echo "================================================================================"
