#!/usr/bin/env python3
import sys
import json
import argparse
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))

from research.swarm_core.config import SwarmConfig
from research.swarm_core.api import JulesAPI

def main():
    parser = argparse.ArgumentParser(description="Check Swarm Status")
    parser.add_argument("--poke", action="store_true", help="Send 'hi' to sessions that seem stuck (not implemented yet)")
    args = parser.parse_args()

    # Config & API
    config = SwarmConfig(env_path=repo_root / ".env")
    api = JulesAPI(config.api_base_url)
    
    api_keys = config.api_keys
    if not api_keys:
        print("❌ Error: API keys not found.")
        sys.exit(1)
    
    # State File
    state_file = repo_root / "research/state/sessions.json"
    if not state_file.exists():
        print(f"⚠️  No session state file found at {state_file}")
        sys.exit(0)
        
    with open(state_file, "r") as f:
        sessions = json.load(f)

    print(f"{'COMPONENT':<20} | {'STATUS':<15} | {'SESSION ID':<40}")
    print("-" * 80)
    
    completed_count = 0
    
    for i, session in enumerate(sessions):
        # Round Robin Key
        api_key = api_keys[i % len(api_keys)]
        
        details = api.get_session_details(api_key, session["sessionId"])
        
        status = "UNKNOWN"
        if details:
            if details.get("state"):
                status = details.get("state")
            elif details.get("outputs"):
                status = "DONE (PR Ready)"
            else:
                status = "RUNNING"
        
        print(f"{session.get('component', 'N/A'):<20} | {status:<15} | {session['sessionId']:<40}")
        
        if "DONE" in str(status).upper() or "SUCCEEDED" in str(status).upper():
            completed_count += 1

    print("-" * 80)
    print(f"Summary: {completed_count}/{len(sessions)} tasks completed.")

if __name__ == "__main__":
    main()
