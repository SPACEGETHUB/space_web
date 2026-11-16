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
