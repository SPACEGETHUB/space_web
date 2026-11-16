#!/usr/bin/env python3
import json
import os

ledger_path = os.path.expanduser("~/space_web/isot_ledger.json")
if os.path.exists(ledger_path):
    with open(ledger_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[✓] [Prereq 2] LTT Ledger ingestion verified. Total records: {data.get('total_records', 0)}")
else:
    print("[!] [Prereq 2] Ledger path not found.")
