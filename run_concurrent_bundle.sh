#!/bin/bash
"""
S.P.A.C.E. Concurrent Dual-Node Orchestration Bundle
Architect: Michael C. Sims
"""
echo "================================================================="
echo " S.P.A.C.E. Concurrent Orchestration Pipeline Initiated"
echo "================================================================="

TCL_IP="10.79.70.223"
TCL_USER="u0_a284"
TCL_PORT="8022"

# Task 1: Restart local HP gateway and verify ledger (Background Job 1)
(
    echo "[*] [HP] Restarting local web gateway and auditing ledger..."
    cd ~/space_web
    pkill -f "app.py" 2>/dev/null || true
    nohup python3 app.py > flask_server.log 2>&1 &
    sleep 1
    if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/ | grep -q "200"; then
        echo "[✓] [HP] Local Gateway is LIVE (HTTP 200)"
    else
        echo "[!] [HP] Local Gateway failed to respond."
    fi
) &

# Task 2: Push local changes to GitHub repository (Background Job 2)
(
    echo "[*] [HP] Pushing updates to sovereign GitHub repository..."
    cd ~/space_web
    git add .
    git commit -m "Concurrent automated sync bundle: $(date +%d/%m/%Y)" 2>/dev/null || true
    git push origin main >/dev/null 2>&1 && echo "[✓] [GitHub] Repository synchronized successfully." || echo "[!] [GitHub] Push skipped or failed."
) &

# Task 3: Remote SSH deployment and gateway launch on TCL mobile node (Background Job 3)
(
    echo "[*] [MOBILE] Connecting to SPACE-MOBILE to pull & restart gateway..."
    ssh -o ConnectTimeout=5 -p $TCL_PORT $TCL_USER@$TCL_IP "cd ~/space_web && git pull origin main && pkill -f 'app.py' 2>/dev/null || true && nohup python3 app.py > flask_server.log 2>&1" && echo "[✓] [MOBILE] SPACE-MOBILE gateway synchronized and active." || echo "[!] [MOBILE] SSH sync skipped (node unreachable)."
) &

# Wait for all background tasks to complete concurrently
wait

echo "================================================================="
echo " [✓] Concurrent pipeline execution complete. Running health audit..."
echo "================================================================="
python3 ~/space_web/check_node_health.py $TCL_IP $TCL_USER
