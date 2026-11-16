#!/usr/bin/env python3
"""
LIMITLESS ECOSYSTEM - Takeout Archive Parser & ISOT Ingestion Engine
Enterprise: S.P.A.C.E. (Systematic Properties An Artisan Collective Enterprise)
Architect: Michael C. Sims
"""
import os
import json
from datetime import datetime, timezone

# Corrected path targeting local repository directory structure
TAKEOUT_DIR = os.path.expanduser("~/space_web/takeout_archive")
LEDGER_PATH = os.path.expanduser("~/space_web/isot_ledger.json")

def scan_and_parse():
    print("=========================================================================")
    print(" [LIMITLESS] Scanning Local Takeout Archive Directory for Records...")
    print(f" Source Path: {TAKEOUT_DIR}")
    print("=========================================================================")

    if not os.path.exists(TAKEOUT_DIR):
        print(f"[!] ERROR: Takeout directory not found at {TAKEOUT_DIR}")
        return

    parsed_chats = []
    file_count = 0

    for root, dirs, files in os.walk(TAKEOUT_DIR):
        for file in files:
            if file.lower().endswith((".json", ".html", ".csv", ".txt")):
                file_count += 1
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        parsed_chats.append({
                            "id": f"takeout_archive_{file_count}_{int(datetime.now(timezone.utc).timestamp())}",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "title": f"Takeout Archive Record: {file}",
                            "source": file,
                            "content_snippet": content[:300].replace("\n", " "),
                            "raw_text": content[:1000],
                            "ingested_at": datetime.now(timezone.utc).isoformat()
                        })
                except Exception as e:
                    pass

    print(f"[✓] Scan complete. Total files examined: {file_count}")
    print(f"[✓] Extracted valid records: {len(parsed_chats)}")

    if parsed_chats and os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            ledger_data = json.load(f)
        
        existing_sources = {r.get("source") for r in ledger_data.get("chat_records", [])}
        added_count = 0
        for chat in parsed_chats:
            if chat["source"] not in existing_sources:
                ledger_data["chat_records"].append(chat)
                added_count += 1

        ledger_data["total_records"] = len(ledger_data["chat_records"])
        ledger_data["last_updated"] = datetime.now(timezone.utc).isoformat()

        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(ledger_data, f, indent=2)

        print(f"[✓] Successfully injected {added_count} new Takeout archive record(s) into isot_ledger.json!")
        print(f"[✓] Updated Master Ledger Total Records: {ledger_data['total_records']}")

if __name__ == "__main__":
    scan_and_parse()
