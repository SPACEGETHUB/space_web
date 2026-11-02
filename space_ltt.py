import json
import os
import argparse
from datetime import datetime

LEADS_FILE = "consultations.json"
TASKS_FILE = "ltt_tasks.json"

def load_json(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def cmd_leads(args):
    leads = load_json(LEADS_FILE)
    if not leads:
        print("[S.P.A.C.E.] No consultation leads found.")
        return

    print(f"\n=== S.P.A.C.E. CONSULTATION LEDGER ({len(leads)} Records) ===")
    print("=" * 65)
    for i, lead in enumerate(leads, 1):
        print(f"[{i}] Entity Name : {lead.get('entity_name', 'N/A')}")
        print(f"    Objective   : {lead.get('objective', 'N/A')}")
        print(f"    Timestamp   : {lead.get('timestamp', 'N/A')}")
        print(f"    Narrative   : {lead.get('narrative', 'N/A')}")
        print("-" * 65)

def cmd_tasks(args):
    tasks = load_json(TASKS_FILE)
    if not tasks:
        print("[L.T.T.] No active operational tasks found.")
        return

    print(f"\n=== LIVE TASK TRACKER (LTT) ({len(tasks)} Total Tasks) ===")
    print("=" * 65)
    for i, task in enumerate(tasks, 1):
        status_tag = "[DONE]" if task.get('completed') else "[ACTIVE]"
        print(f"[{i}] {status_tag} {task.get('title', 'N/A')}")
        print(f"    Priority    : {task.get('priority', 'Normal')}")
        print(f"    Created     : {task.get('timestamp', 'N/A')}")
        if task.get('source_entity'):
            print(f"    Source Lead : {task.get('source_entity')}")
        print("-" * 65)

def cmd_add_task(args):
    tasks = load_json(TASKS_FILE)
    new_task = {
        "title": args.title,
        "priority": args.priority,
        "completed": False,
        "timestamp": datetime.now().isoformat(),
        "source_entity": None
    }
    tasks.append(new_task)
    save_json(TASKS_FILE, tasks)
    print(f"[L.T.T.] Task successfully registered: '{args.title}' [{args.priority}]")

def cmd_convert(args):
    leads = load_json(LEADS_FILE)
    if not leads:
        print("[S.P.A.C.E.] No leads available to convert.")
        return
    
    if args.lead_index < 1 or args.lead_index > len(leads):
        print(f"[Error] Invalid lead index. Choose between 1 and {len(leads)}.")
        return

    lead = leads[args.lead_index - 1]
    tasks = load_json(TASKS_FILE)
    
    new_task = {
        "title": f"Stratification Protocol: {lead.get('objective', 'Consultation')} for {lead.get('entity_name', 'Client')}",
        "priority": "High",
        "completed": False,
        "timestamp": datetime.now().isoformat(),
        "source_entity": lead.get('entity_name', 'N/A'),
        "narrative": lead.get('narrative', '')
    }
    
    tasks.append(new_task)
    save_json(TASKS_FILE, tasks)
    print(f"[S.P.A.C.E. -> L.T.T.] Lead #{args.lead_index} ({lead.get('entity_name')}) successfully converted into an LTT task.")

def cmd_complete(args):
    tasks = load_json(TASKS_FILE)
    if not tasks:
        print("[L.T.T.] No tasks available to complete.")
        return
    
    if args.task_index < 1 or args.task_index > len(tasks):
        print(f"[Error] Invalid task index. Choose between 1 and {len(tasks)}.")
        return

    task = tasks[args.task_index - 1]
    task['completed'] = True
    save_json(TASKS_FILE, tasks)
    print(f"[L.T.T.] Task #{args.task_index} ('{task.get('title')}') marked as completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S.P.A.C.E. Unified Lead & Task Tracker (LTT)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("leads", help="View all consultation leads.")
    subparsers.add_parser("tasks", help="View all LTT tasks.")

    parser_add = subparsers.add_parser("add-task", help="Add a new task to LTT.")
    parser_add.add_argument("title", type=str, help="Task description / title.")
    parser_add.add_argument("-p", "--priority", type=str, default="Normal", help="Priority level (High, Normal, Low).")

    parser_conv = subparsers.add_parser("convert", help="Convert a consultation lead into an LTT task by its index number.")
    parser_conv.add_argument("lead_index", type=int, help="Index number of the lead from 'leads' command.")

    parser_comp = subparsers.add_parser("complete", help="Mark an LTT task as completed by its index number.")
    parser_comp.add_argument("task_index", type=int, help="Index number of the task from 'tasks' command.")

    args = parser.parse_args()

    if args.command == "leads":
        cmd_leads(args)
    elif args.command == "tasks":
        cmd_tasks(args)
    elif args.command == "add-task":
        cmd_add_task(args)
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "complete":
        cmd_complete(args)
