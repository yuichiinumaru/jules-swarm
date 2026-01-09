#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))

from research.swarm_core.config import SwarmConfig
from research.swarm_core.api import JulesAPI

def main():
    parser = argparse.ArgumentParser(description="Poke Jules Session")
    parser.add_argument("id", help="Session ID (e.g. sessions/12345)")
    parser.add_argument("message", help="Message to send")
    args = parser.parse_args()

    # Config & API
    config = SwarmConfig(env_path=repo_root / ".env")
    api = JulesAPI(config.api_base_url)

    api_keys = config.api_keys
    if not api_keys:
        print("❌ Error: API keys not found.")
        sys.exit(1)

    print(f"📡  Sending Input to: {args.id}")
    print(f"    Message: '{args.message}'")
    
    result = api.send_input(api_keys[0], args.id, args.message)
    
    if result:
        print("✅ Input Sent Successfully!")
        import json
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
