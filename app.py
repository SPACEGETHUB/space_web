#!/usr/bin/env python3
"""
S.P.A.C.E. Sovereign ISOT Web Gateway (Zero-Dependency http.server)
Architect: Michael C. Sims
"""
import http.server
import json
import os
import urllib.parse

PORT = 5000

class ISOTHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/" or parsed_path.path == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            try:
                with open("isot_ledger.json", "r") as f:
                    data = json.load(f)
                    records = data.get("chat_records", [])
                    total = data.get("total_records", len(records))
            except Exception:
                records = []
                total = 0

            html = f"""<!DOCTYPE html>
            <html>
            <head>
                <title>S.P.A.C.E. ISOT Sovereign Database</title>
                <style>
                    body {{ background: #0f172a; color: #f8fafc; font-family: monospace; padding: 2rem; }}
                    h1 {{ color: #38bdf8; }}
                    .card {{ background: #1e293b; border: 1px solid #334155; padding: 1rem; margin-bottom: 1rem; border-radius: 6px; }}
                    .meta {{ color: #94a3b8; font-size: 0.85rem; }}
                </style>
            </head>
            <body>
                <h1>S.P.A.C.E. Immersive Source of Truth (ISOT)</h1>
                <p>Total Records: <strong>{total}</strong> | Node: SPACE (HP)</p>
                <hr style="border-color: #334155; margin: 1rem 0;">
            """
            for rec in reversed(records):
                rid = rec.get("id", "N/A")
                rtitle = rec.get("title", rec.get("query", "Untitled Record"))
                rcontent = rec.get("content", rec.get("response", ""))
                html += f"""
                <div class="card">
                    <div><strong>[{rid}] {rtitle}</strong></div>
                    <div class="meta" style="margin-top: 0.5rem;">{rcontent[:300]}...</div>
                </div>
                """
            html += "</body></html>"
            self.wfile.write(html.encode("utf-8"))
        else:
            return super().do_GET()

if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, ISOTHandler)
    print(f"[✓] S.P.A.C.E. ISOT Gateway running on port {PORT} (Zero-Dependency)")
    httpd.serve_forever()
