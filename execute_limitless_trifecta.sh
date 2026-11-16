#!/usr/bin/env bash
# ==============================================================================
# LIMITLESS ECOSYSTEM - MASTER TRIFECTA BUNDLE (CONCURRENT + SEQUENTIAL)
# Enterprise: S.P.A.C.E. (Systematic Properties An Artisan Collective Enterprise)
# Architect : Michael C. Sims
# Node      : SPACE (HP Primary Workstation - WSL 2)
# ==============================================================================

set -e
BASE_DIR="$HOME/space_web"
cd "$BASE_DIR"

echo "========================================================================="
echo " [LIMITLESS] Initiating Master Trifecta Execution Pipeline"
echo "========================================================================="

# ------------------------------------------------------------------------------
# PHASE 1: CONCURRENT EXECUTION (OPTION A: LEDGER INGEST + OPTION B: UI UPGRADE)
# ------------------------------------------------------------------------------
echo "[*] [PHASE 1] Launching Option A (Ledger Expansion) & Option B (UI Upgrade) concurrently..."

# Job 1A: Inject verified operational milestone into isot_ledger.json
(
    python3 - << 'PY_LEDGER'
import json
import os
from datetime import datetime, timezone

ledger_path = os.path.expanduser("~/space_web/isot_ledger.json")
with open(ledger_path, "r", encoding="utf-8") as f:
    data = json.load(f)

now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
new_id = f"limitless_{int(datetime.now(timezone.utc).timestamp())}"

new_record = {
    "id": new_id,
    "timestamp": now_iso,
    "title": "Limitless Ecosystem Trifecta Synchronization & Taxonomy Lock",
    "source": "execute_limitless_trifecta.sh",
    "content_snippet": "Locked S.P.A.C.E. corporate taxonomy and Limitless operating environment. Upgraded web gateway UI and queued GitHub relay commits.",
    "raw_text": "Enterprise: S.P.A.C.E. (Systematic Properties An Artisan Collective Enterprise). Ecosystem: Limitless. Executed concurrent ledger ingestion, web gateway UI enhancement, and network watchdog relay.",
    "ingested_at": datetime.now(timezone.utc).isoformat()
}

# Prevent duplicate injection on re-runs
if not any(r.get("title") == new_record["title"] for r in data.get("chat_records", [])):
    data["chat_records"].append(new_record)
    data["total_records"] = len(data["chat_records"])
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(ledger_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[✓] [Job 1A] Injected record [{new_id}]. Total records: {data['total_records']}")
else:
    print(f"[✓] [Job 1A] Milestone record already verified in ledger. Total records: {data['total_records']}")
PY_LEDGER
) &
PID_1A=$!

# Job 1B: Upgrade app.py with live search filtering, taxonomy header, and status badges
(
    cat << 'PY_APP' > "$BASE_DIR/app.py"
#!/usr/bin/env python3
"""
LIMITLESS ECOSYSTEM - Sovereign ISOT Web Gateway (Zero-Dependency http.server)
Enterprise: S.P.A.C.E. (Systematic Properties An Artisan Collective Enterprise)
Architect: Michael C. Sims
"""
import http.server
import json
import urllib.parse

PORT = 5000

class ISOTHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path in ("/", ""):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            try:
                with open("isot_ledger.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    records = data.get("chat_records", [])
                    total = data.get("total_records", len(records))
                    last_updated = data.get("last_updated", "N/A")
            except Exception:
                records = []
                total = 0
                last_updated = "ERROR"

            cards_html = ""
            for rec in reversed(records):
                rid = rec.get("id", "N/A")
                rtitle = rec.get("title", rec.get("query", "Untitled Record"))
                ts = rec.get("timestamp", "N/A")
                src = rec.get("source", "local")
                rcontent = rec.get("raw_text", rec.get("content_snippet", rec.get("response", "")))
                cards_html += f"""
                <div class="card" data-search="{rtitle.lower()} {rcontent.lower()} {rid.lower()}">
                    <div class="card-header">
                        <span class="title">[{rid}] {rtitle}</span>
                        <span class="badge">{src}</span>
                    </div>
                    <div class="timestamp">Timestamp: {ts}</div>
                    <div class="content">{rcontent}</div>
                </div>
                """

            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LIMITLESS | S.P.A.C.E. ISOT Gateway</title>
    <style>
        body {{ background: #0b1120; color: #f8fafc; font-family: 'Courier New', monospace; padding: 2rem; max-width: 1100px; margin: auto; }}
        header {{ border-bottom: 2px solid #1e293b; padding-bottom: 1rem; margin-bottom: 1.5rem; }}
        h1 {{ color: #38bdf8; margin: 0 0 0.4rem 0; font-size: 1.6rem; }}
        .sub {{ color: #94a3b8; font-size: 0.9rem; }}
        .status-bar {{ display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0; }}
        .pill {{ background: #1e293b; border: 1px solid #334155; padding: 0.4rem 0.8rem; border-radius: 4px; font-size: 0.85rem; }}
        .pill.live {{ border-color: #10b981; color: #34d399; }}
        input[type="text"] {{ width: 100%; box-sizing: border-box; padding: 0.75rem; background: #1e293b; border: 1px solid #475569; color: #f8fafc; border-radius: 6px; font-family: inherit; margin-bottom: 1.5rem; }}
        .card {{ background: #1e293b; border: 1px solid #334155; padding: 1.1rem; margin-bottom: 1rem; border-radius: 6px; }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; }}
        .title {{ color: #7dd3fc; font-weight: bold; }}
        .badge {{ background: #0f172a; color: #38bdf8; border: 1px solid #38bdf8; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; }}
        .timestamp {{ color: #64748b; font-size: 0.8rem; margin: 0.3rem 0 0.6rem 0; }}
        .content {{ color: #cbd5e1; font-size: 0.9rem; line-height: 1.45; }}
    </style>
</head>
<body>
    <header>
        <h1>LIMITLESS OPERATING ENVIRONMENT // ISOT LEDGER</h1>
        <div class="sub">Enterprise: S.P.A.C.E. (Systematic Properties An Artisan Collective Enterprise) | Architect: Michael C. Sims</div>
        <div class="status-bar">
            <div class="pill live">[✓] HP NODE (SPACE): ONLINE</div>
            <div class="pill">RECORDS: <strong>{total}</strong></div>
            <div class="pill">LAST SYNC: {last_updated}</div>
        </div>
    </header>
    <input type="text" id="filterInput" onkeyup="filterRecords()" placeholder="Filter ISOT records by keyword, ID, or title...">
    <div id="recordsContainer">{cards_html}</div>
    <script>
        function filterRecords() {{
            const q = document.getElementById('filterInput').value.toLowerCase();
            document.querySelectorAll('.card').forEach(card => {{
                card.style.display = card.getAttribute('data-search').includes(q) ? '' : 'none';
            }});
        }}
    </script>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
        else:
            return super().do_GET()

if __name__ == "__main__":
    httpd = http.server.HTTPServer(('', PORT), ISOTHandler)
    print(f"[✓] LIMITLESS ISOT Gateway live on port {PORT}")
    httpd.serve_forever()
PY_APP
    chmod +x "$BASE_DIR/app.py"
    echo "[✓] [Job 1B] Upgraded app.py web gateway with live search & status telemetry."
) &
PID_1B=$!

# Wait for both concurrent Phase 1 jobs to finish before restarting the gateway
wait $PID_1A
wait $PID_1B
echo "[✓] [PHASE 1] Concurrent execution complete."

# ------------------------------------------------------------------------------
# PHASE 2: SEQUENTIAL GATEWAY RELOAD & VERIFICATION
# ------------------------------------------------------------------------------
echo "[*] [PHASE 2] Restarting local gateway on port 5000 to load upgraded UI & ledger..."
pkill -f "app.py" 2>/dev/null || true
nohup python3 "$BASE_DIR/app.py" > "$BASE_DIR/flask_server.log" 2>&1 &
sleep 2

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/)
if [ "$HTTP_CODE" = "200" ]; then
    echo "[✓] [PHASE 2] Gateway verified LIVE (HTTP 200) serving updated records."
else
    echo "[!] [PHASE 2] Warning: Gateway returned HTTP $HTTP_CODE"
fi

# ------------------------------------------------------------------------------
# PHASE 3: SEQUENTIAL GIT COMMIT & NETWORK WATCHDOG RELAY (OPTION C)
# ------------------------------------------------------------------------------
echo "[*] [PHASE 3] Staging local commits and checking GitHub relay connectivity..."
git add isot_ledger.json app.py execute_limitless_trifecta.sh
git commit -m "Limitless Trifecta Update ($(date +%d/%m/%Y)): Ledger +1, UI v2" 2>/dev/null || echo "[*] Working tree already committed."

AHEAD_COUNT=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
echo "[*] Local branch is ahead of origin/main by $AHEAD_COUNT commit(s)."

if ping -c 1 -W 3 github.com >/dev/null 2>&1; then
    echo "[✓] Network connectivity online! Pushing $AHEAD_COUNT commit(s) to GitHub..."
    git push origin main && echo "[✓] [PHASE 3] Sovereign GitHub repository synchronized!"
else
    echo "[!] [PHASE 3] WSL 2 DNS/Network still isolated (github.com unreachable)."
    echo "[*] All $AHEAD_COUNT commit(s) are safely locked on disk and ready."
    echo "[*] To auto-push as soon as network returns, run: until ping -c1 -W2 github.com &>/dev/null; do sleep 15; done && git push origin main"
fi

echo "========================================================================="
echo " [✓] LIMITLESS MASTER TRIFECTA PIPELINE COMPLETE"
echo "========================================================================="
