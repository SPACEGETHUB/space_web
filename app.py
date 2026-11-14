#!/usr/bin/env python3
"""
S.P.A.C.E. ISOT Mobile Web Gateway
Architect: Michael C. Sims
"""
from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>S.P.A.C.E. Mobile ISOT Gateway</title>
    <style>
        body { font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }
        h1 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
        input { background: #161b22; color: #f0f6fc; border: 1px solid #30363d; padding: 8px; width: 60%; }
        button { background: #238636; color: white; border: none; padding: 8px 16px; cursor: pointer; }
        .record { background: #161b22; border: 1px solid #30363d; margin: 10px 0; padding: 15px; border-radius: 6px; }
        .title { font-weight: bold; color: #79c0ff; }
        .meta { color: #8b949e; font-size: 0.85em; margin-bottom: 8px; }
    </style>
</head>
<body>
    <h1>S.P.A.C.E. Sovereign Mobile ISOT Engine</h1>
    <div>
        <form method="GET" action="/">
            <input type="text" name="q" placeholder="Search ISOT database..." value="{{ query }}">
            <button type="submit">Search</button>
        </form>
    </div>
    <h2>Active Records Found: {{ records|length }}</h2>
    {% for r in records %}
    <div class="record">
        <div class="title">{{ r.get('title', 'Untitled') }}</div>
        <div class="meta">Timestamp: {{ r.get('timestamp', 'N/A') }}</div>
        <pre>{{ r.get('messages', []) | tojson(indent=2) }}</pre>
    </div>
    {% endfor %}
</body>
</html>
"""

def load_ledger():
    try:
        with open("isot_ledger.json", "r") as f:
            return json.load(f).get("chat_records", [])
    except Exception:
        return []

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "")
    records = load_ledger()
    if q:
        records = [r for r in records if q.lower() in json.dumps(r).lower()]
    return render_template_string(HTML_TEMPLATE, records=records, query=q)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
