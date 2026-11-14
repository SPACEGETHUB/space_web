#!/usr/bin/env python3
"""
S.P.A.C.E. ISOT Terminal Search Engine
Architect: Michael C. Sims
"""
import json
import sys

def search_ledger(query):
    try:
        with open("isot_ledger.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[!] Error: isot_ledger.json not found in current directory.")
        return
    
    records = data.get("chat_records", [])
    matches = [r for r in records if query.lower() in json.dumps(r).lower()]
    
    print("=================================================================")
    print(f" S.P.A.C.E. ISOT Search Results | Query: '{query}' | Matches: {len(matches)}")
    print("=================================================================\n")
    
    for idx, m in enumerate(matches, 1):
        title = m.get("title", "Untitled Record")
        ts = m.get("timestamp", "N/A")
        print(f"[{idx}] {title} (Timestamp: {ts})")
        if "messages" in m:
            preview = str(m["messages"][:1])[:150]
            print(f"    Preview: {preview}...\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 isot_search.py <search_term>")
        sys.exit(1)
    search_ledger(" ".join(sys.argv[1:]))
