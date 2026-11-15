#!/usr/bin/env python3
"""
S.P.A.C.E. Dual-Node Sovereign Health & Telemetry Engine
Architect: Michael C. Sims
"""
import json
import os
import subprocess
import sys
import urllib.request

def check_local_ledger():
    try:
        with open("isot_ledger.json", "r") as f:
            data = json.load(f)
            records = data.get("total_records", len(data.get("chat_records", [])))
            return True, records
    except Exception as e:
        return False, str(e)

def check_local_gateway(port=5000):
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False

def check_local_daemon():
    res = subprocess.run("pgrep -f 'continuous_push.sh|mobile_sync.sh|app.py'", shell=True, capture_output=True, text=True)
    pids = res.stdout.strip().split()
    return len(pids) > 0, pids

def check_remote_tcl(ip, user, port="8022"):
    remote_cmd = f"ssh -o ConnectTimeout=5 -p {port} {user}@{ip} \"cd ~/space_web && python3 -c \\\"import json; d=json.load(open('isot_ledger.json')); print(d.get('total_records', len(d.get('chat_records',[]))))\\\"\" 2>/dev/null"
    res = subprocess.run(remote_cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip().isdigit():
        return True, int(res.stdout.strip())
    return False, 0

def run_telemetry(tcl_ip=None, tcl_user=None):
    print("=================================================================")
    print(" S.P.A.C.E. Dual-Node Telemetry & System Integrity Report")
    print("=================================================================")
    
    ledger_ok, local_count = check_local_ledger()
    gateway_ok = check_local_gateway()
    daemon_ok, pids = check_local_daemon()
    
    print(f"\n[LOCAL NODE AUDIT - SPACE (HP)]")
    print(f"  └─ Master Ledger Status : {'[✓] ONLINE' if ledger_ok else '[!] FAILED'} ({local_count} records)")
    print(f"  └─ Web Gateway Port 5000: {'[✓] RESPONDING' if gateway_ok else '[!] DOWN / INACTIVE'}")
    print(f"  └─ Active System Daemons: {'[✓] RUNNING' if daemon_ok else '[!] STOPPED'} (PIDs: {', '.join(pids) if pids else 'None'})")
    
    if tcl_ip and tcl_user:
        remote_ok, remote_count = check_remote_tcl(tcl_ip, tcl_user)
        print(f"\n[REMOTE NODE AUDIT - SPACE-MOBILE ({tcl_ip}:8022)]")
        print(f"  └─ SSH Connection Status: {'[✓] LINKED' if remote_ok else '[!] UNREACHABLE'}")
        print(f"  └─ Remote Ledger Records: {remote_count if remote_ok else 'N/A'}")
        
        if ledger_ok and remote_ok:
            parity = (local_count == remote_count)
            print(f"\n[CROSS-NODE PARITY EVALUATION]")
            print(f"  └─ Parity Status        : {'[✓] 100% PARITY MATCH' if parity else '[!] PARITY MISMATCH'}")
    else:
        print("\n[*] Remote TCL check skipped. Pass TCL_IP and TCL_USER to inspect remote node.")

    print("=================================================================\n")

if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else os.getenv("TCL_IP")
    user = sys.argv[2] if len(sys.argv) > 2 else os.getenv("TCL_USER")
    run_telemetry(ip, user)
