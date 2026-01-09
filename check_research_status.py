#!/usr/bin/env python3
import os
import json
import requests
from pathlib import Path

# Configuration with absolute paths for Windows
API_BASE_URL = "https://jules.googleapis.com/v1alpha"
PROJECT_ROOT = Path(r"f:\AI\cryptosentinel-v1")
ENV_FILE_PATH = PROJECT_ROOT / "scripts" / "research" / "jules-swarm" / ".env"
STATE_FILE_PATH = PROJECT_ROOT / "scripts" / "research" / "jules-swarm" / "scripts" / "state" / "sessions.json"

def load_keys():
    if not ENV_FILE_PATH.exists(): return []
    with open(ENV_FILE_PATH, "r") as f:
        for line in f:
            if line.startswith("JULES_API_KEYS="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                return [k.strip() for k in val.split(",") if k.strip()]
    return []

def main():
    keys = load_keys()
    if not keys: 
        print("Keys not found")
        return
    
    if not STATE_FILE_PATH.exists(): 
        print("State not found")
        return

    with open(STATE_FILE_PATH, "r") as f:
        all_s = json.load(f)
    
    res_s = [s for s in all_s if s.get("component", "").startswith("paper_")]
    results = []
    
    print(f"Checking {len(res_s)} sessions...", flush=True)
    
    for i, s in enumerate(res_s):
        k = keys[i % len(keys)]
        try:
            r = requests.get(f"{API_BASE_URL}/{s['sessionId']}", headers={"x-goog-api-key": k}, timeout=10)
            data = r.json()
            state = data.get("state", "RUNNING")
            results.append(state)
        except:
            results.append("ERROR")
    
    stats = {st: results.count(st) for st in set(results)}
    print(json.dumps(stats, indent=2), flush=True)

if __name__ == "__main__":
    main()
