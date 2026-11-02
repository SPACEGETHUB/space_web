#!/usr/bin/env python3
"""
S.P.A.C.E. Immersive Source of Truth (ISOT) - Takeout JSON Parser
Architect: Michael C. Sims
Node: HP Laptop / WSL 2 Ubuntu (`SPACE`)

Description:
    Parses extracted Google Takeout chat/activity JSON archives and
    consolidates conversation metadata, prompts, and timestamps into
    the sovereign `isot_ledger.json` master database.
"""

import json
import os
import glob
from datetime import datetime

# File Paths
BASE_DIR = os.path.expanduser("~/space_web")
EXTRACTED_DIR = os.path.join(BASE_DIR, "takeout_archive", "extracted")
ISOT_LEDGER_FILE = os.path.join(BASE_DIR, "isot_ledger.json")

def load_isot_ledger():
    """Load existing ISOT ledger or initialize empty structure."""
    if os.path.exists(ISOT_LEDGER_FILE):
        try:
            with open(ISOT_LEDGER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[!] Warning: isot_ledger.json corrupted. Initializing new ledger.")
    
    return {
        "system": "S.P.A.C.E. Immersive Source of Truth (ISOT)",
        "architect": "Michael C. Sims",
        "last_updated": None,
        "total_records": 0,
        "chat_records": []
    }

def save_isot_ledger(ledger):
    """Save updated ISOT ledger to disk."""
    ledger["last_updated"] = datetime.now().isoformat()
    ledger["total_records"] = len(ledger["chat_records"])
    
    with open(ISOT_LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
    
    print(f"[✓] ISOT Ledger successfully updated at: {ISOT_LEDGER_FILE}")
    print(f"[✓] Total active records in ISOT database: {ledger['total_records']}")

def parse_takeout_files():
    """Locate and parse JSON files within extracted Takeout folder."""
    if not os.path.exists(EXTRACTED_DIR):
        print(f"[!] Error: Extracted Takeout directory not found at {EXTRACTED_DIR}")
        print("    Run your unzipping protocol first or place files in ~/space_web/takeout_archive/extracted/")
        return []

    # Match JSON files inside Takeout folder structure
    json_pattern = os.path.join(EXTRACTED_DIR, "**", "*.json")
    json_files = glob.glob(json_pattern, recursive=True)
    
    if not json_files:
        print(f"[!] No JSON files found in {EXTRACTED_DIR}")
        return []

    parsed_entries = []
    print(f"[*] Found {len(json_files)} potential JSON file(s). Beginning ingestion...")

    for file_path in json_files:
        # Skip manifests or metadata files if present
        if "ingestion_manifest" in file_path:
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Handle Google Takeout array format
            if isinstance(data, list):
                for item in data:
                    entry = extract_chat_data(item, file_path)
                    if entry:
                        parsed_entries.append(entry)
            elif isinstance(data, dict):
                entry = extract_chat_data(data, file_path)
                if entry:
                    parsed_entries.append(entry)

        except Exception as e:
            print(f"[!] Warning: Could not parse file {os.path.basename(file_path)}: {e}")

    return parsed_entries

def extract_chat_data(item, source_file):
    """Extract standard properties from raw Takeout chat items."""
    # Custom mapping handling multiple Takeout schema variations
    title = item.get("title") or item.get("name") or "Untitled Session"
    timestamp = item.get("time") or item.get("createTime") or datetime.now().isoformat()
    
    text_content = ""
    if "textContent" in item:
        text_content = item["textContent"]
    elif "parts" in item:
        text_content = " ".join([p.get("text", "") for p in item["parts"] if isinstance(p, dict)])
    elif "snippets" in item:
        text_content = " ".join(item.get("snippets", []))

    if not text_content and "title" not in item:
        return None

    return {
        "id": f"takeout_{hash(timestamp + title)}",
        "timestamp": timestamp,
        "title": title,
        "source": os.path.basename(source_file),
        "content_snippet": text_content[:500] if text_content else "No text snippet extracted",
        "raw_text": text_content,
        "ingested_at": datetime.now().isoformat()
    }

def main():
    print("=================================================================")
    print(" S.P.A.C.E. ISOT Takeout Parser & Database Sync Engine")
    print("=================================================================")
    
    ledger = load_isot_ledger()
    existing_ids = {r["id"] for r in ledger["chat_records"] if "id" in r}
    
    new_entries = parse_takeout_files()
    
    added_count = 0
    for entry in new_entries:
        if entry["id"] not in existing_ids:
            ledger["chat_records"].append(entry)
            existing_ids.add(entry["id"])
            added_count += 1
            
    print(f"[*] Ingestion complete: {added_count} new record(s) merged.")
    save_isot_ledger(ledger)

if __name__ == "__main__":
    main()
