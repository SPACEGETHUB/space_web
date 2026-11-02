import json
import os
import argparse

DB_FILE = "consultations.json"

def view_consultations(search_term=None):
    if not os.path.exists(DB_FILE):
        print("[S.P.A.C.E.] No consultation logs found. Database file does not exist yet.")
        return

    try:
        with open(DB_FILE, "r") as f:
            records = json.load(f)
    except json.JSONDecodeError:
        print("[S.P.A.C.E.] Error: consultations.json is corrupted or empty.")
        return

    if not records:
        print("[S.P.A.C.E.] consultations.json is currently empty.")
        return

    # Filter records if a search term is provided
    filtered_records = records
    if search_term:
        term = search_term.lower()
        filtered_records = [
            r for r in records 
            if term in r.get('entity_name', '').lower() or
               term in r.get('objective', '').lower() or
               term in r.get('narrative', '').lower()
        ]
        print(f"\n=== S.P.A.C.E. FILTERED LEDGER (Match: '{search_term}', {len(filtered_records)}/{len(records)} Records) ===")
    else:
        print(f"\n=== S.P.A.C.E. CONSULTATION LEDGER ({len(records)} Records) ===")
        
    print("=" * 60)
    
    if not filtered_records:
        print("[S.P.A.C.E.] No records match the specified search term.")
        print("=" * 60)
        return

    for i, record in enumerate(filtered_records, 1):
        print(f"[{i}] Entity Name : {record.get('entity_name', 'N/A')}")
        print(f"    Objective   : {record.get('objective', 'N/A')}")
        print(f"    Timestamp   : {record.get('timestamp', 'N/A')}")
        print(f"    Narrative   : {record.get('narrative', 'N/A')}")
        print("-" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S.P.A.C.E. Consultation Ledger Viewer & Filter")
    parser.add_argument("query", nargs="?", default=None, help="Optional keyword, entity, or objective to filter records.")
    args = parser.parse_args()
    view_consultations(args.query)
