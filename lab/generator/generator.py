import winrm
import requests
import time
import random
import csv
import os
from datetime import datetime, timezone
import scenarios as sc

session = winrm.Session(f'http://{sc.TARGET_WIN}:5985/wsman',
                         auth=(sc.WINRM_USER, sc.WINRM_PASS),
                         transport='ntlm')

LOG_FILE = "ground_truth.csv"

def log_event(category, label, mitre, detail):
    ts = datetime.now(timezone.utc).isoformat()
    exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp_utc", "category", "label", "mitre", "detail"])
        writer.writerow([ts, category, label, mitre, detail])
    print(f"[{ts}] {category} | {label} | {detail}")

def run_scan():
    batch = sc.gen_scan_batch()
    target = f"http://{sc.TARGET_WIN}"
    headers = {"User-Agent": batch["user_agent"]}
    for path in batch["paths"]:
        try:
            requests.get(target + path, headers=headers, timeout=3)
        except Exception:
            pass
        time.sleep(random.uniform(0.1, 0.5))
    log_event("web_attack", "attack", "T1595", f"scan {len(batch['paths'])} paths, UA={batch['user_agent']}")

def run_bruteforce():
    batch = sc.gen_bruteforce_batch()
    import subprocess
    for pw in batch["passwords"]:
        subprocess.run(
            ["smbclient", "-L", f"//{sc.TARGET_WIN}", "-U", f"{batch['target_user']}%{pw}"],
            capture_output=True, timeout=5
        )
        time.sleep(random.uniform(0.5, 1.5))
    log_event("bruteforce", "attack", "T1110", f"user={batch['target_user']}, attempts={len(batch['passwords'])}")

def run_user_creation():
    batch = sc.gen_user_creation()
    user = batch["username"]
    cmd = f'net user {user} TempPass123! /add; Start-Sleep -Seconds 2; net user {user} /delete'
    session.run_ps(cmd)
    log_event("user_creation", "attack", "T1136.001", f"username={user}")

def run_app_error():
    batch = sc.gen_app_error()
    cmd = f'''
    New-EventLog -LogName Application -Source "{batch['source']}" -ErrorAction SilentlyContinue
    Write-EventLog -LogName Application -Source "{batch['source']}" -EntryType Error -EventId {batch['event_id']} -Message "Synthetic crash simulation"
    '''
    session.run_ps(cmd)
    log_event("app_error", "fp", "", f"source={batch['source']}, eventid={batch['event_id']}")

def run_benign_404():
    """FP tambahan: beberapa 404 acak dari 'user' wajar, bukan scanning"""
    target = f"http://{sc.TARGET_WIN}"
    path = "/favicon.ico" if random.random() > 0.5 else "/robots.txt"
    try:
        requests.get(target + path, timeout=3)
    except Exception:
        pass
    log_event("benign_web", "fp", "", f"normal request to {path}")

SCENARIO_WEIGHTS = {
    run_benign_404: 30,
    run_app_error: 15,
    run_scan: 20,
    run_bruteforce: 15,
    run_user_creation: 20,
}

def run_random_batch(total_runs=50, delay_range=(5, 20)):
    pool = []
    for func, weight in SCENARIO_WEIGHTS.items():
        pool += [func] * weight

    for i in range(total_runs):
        func = random.choice(pool)
        print(f"\n--- Run {i+1}/{total_runs}: {func.__name__} ---")
        try:
            func()
        except Exception as e:
            print(f"Error running {func.__name__}: {e}")
        time.sleep(random.uniform(*delay_range))

if __name__ == "__main__":
    run_random_batch(total_runs=10, delay_range=(5, 15)) # variable total_runs is interchangable
