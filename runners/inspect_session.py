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
    parser = argparse.ArgumentParser(description="Inspect Jules Session Details")
    parser.add_argument("ids", nargs="+", help="Session IDs to inspect (e.g. sessions/12345)")
    args = parser.parse_args()

    # Config & API
    config = SwarmConfig(env_path=repo_root / ".env")
    api = JulesAPI(config.api_base_url)

    api_keys = config.api_keys
    if not api_keys:
        print("❌ Error: API keys not found.")
        sys.exit(1)

    print(f"🔑 Using API Key ending in ...{api_keys[0][-6:]}")

    for i, session_id in enumerate(args.ids):
        print(f"\n[{i+1}/{len(args.ids)}] Inspetcting: {session_id}")
        data = api.get_session_details(api_keys[0], session_id)
        
        if data:
            print(f"✅ State: {data.get('state', 'UNKNOWN')}")
            print(f"   Name: {data.get('name')}")
            print(f"   CreateTime: {data.get('createTime')}")
            
            # Probe extra resources
            endpoints = ["suggestions", "history", "turns", "messages", "events"]
            for ep in endpoints:
                 print(f"📡  Probing: .../{ep}")
                 res_data = api.get_session_resource(api_keys[0], session_id, ep)
                 if res_data:
                     print(f"   ✅ FOUND DATA at /{ep}!")
                     data[ep] = res_data
            
            print("\n📋  Keys found in response:", list(data.keys()))
            
            if 'error' in data:
                print(f"\n❌ ERROR FOUND: {json.dumps(data['error'], indent=2)}")
                
            if 'outputs' in data:
                print(f"\n📤 OUTPUTS: {json.dumps(data['outputs'], indent=2)}")
            
            print("\n--- Full JSON Dump (truncated) ---")
            print(json.dumps(data, indent=2)[:2000] + "...")
        print("-" * 60)

if __name__ == "__main__":
    main()
