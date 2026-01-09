#!/usr/bin/env python3
import time
import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Paths to scripts relative to repo root
# Assuming this script is run from repo root or scripts/research/
PROJECT_ROOT = Path(r"f:\AI\cryptosentinel-v1")
RESEARCH_DIR = PROJECT_ROOT / "scripts" / "research"
SWARM_DIR = RESEARCH_DIR / "jules-swarm"

LAUNCH_SCRIPT = RESEARCH_DIR / "launch_paper_analysis.py"
SYN_SCRIPT = RESEARCH_DIR / "sync_backlog_status.py"
MERGE_SCRIPT = SWARM_DIR / "merge_train.py"

def run_command(command, cwd=None, description=""):
    """Runs a shell command and returns the exit code."""
    print(f"\n🚀 [{datetime.now().strftime('%H:%M:%S')}] Starting: {description}")
    print(f"   Command: {command}")
    
    try:
        # Using shell=True for Windows command compatibility
        # check=False allows us to handle return codes manually
        result = subprocess.run(command, shell=True, check=False, cwd=cwd)
        
        if result.returncode == 0:
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Finished: {description}")
            return 0
        elif result.returncode == 10:
             # Special code for "No more tasks"
             return 10
        else:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Failed (Exit: {result.returncode}): {description}")
            return result.returncode

    except Exception as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Exception: {description}")
        print(f"   Error: {e}")
        return -1

def main():
    parser = argparse.ArgumentParser(description="Automate Research Swarm Cycle")
    parser.add_argument("--limit", type=int, default=60, help="Number of tasks to launch per batch (default: 60)")
    parser.add_argument("--interval", type=int, default=900, help="Sleep interval in seconds (default: 900 = 15 min)")
    parser.add_argument("--batches", type=int, default=1000, help="Max number of batches to run (default: 1000)")
    args = parser.parse_args()

    print(f"🤖 Starting Research Automation Cycle")
    print(f"   - Batch Size: {args.limit}")
    print(f"   - Interval: {args.interval} seconds")
    print(f"   - Scripts: \n     {LAUNCH_SCRIPT}\n     {MERGE_SCRIPT}\n     {SYN_SCRIPT}")
    
    for i in range(1, args.batches + 1):
        print(f"\n{'='*60}")
        print(f"🔄 CYCLE {i}/{args.batches}")
        print(f"{'='*60}")

        # Step 1: Launch Tasks
        cmd_launch = f'python "{LAUNCH_SCRIPT}" --limit {args.limit}'
        launch_code = run_command(cmd_launch, description="Launch Paper Analysis")
        
        if launch_code == 10:
            print("\n🎉 All research tasks completed! No pending papers found.")
            break
        elif launch_code != 0:
            print("⚠️ Issue during launch (Exit Code != 0), continuing cycle...")

        # Step 2: Wait (15 mins)
        print(f"\n⏳ Waiting {args.interval} seconds for agents to process...")
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n🛑 Cycle interrupted by user.")
            sys.exit(0)

        # Step 3: Merge Train (Process PRs)
        cmd_merge = f'python "{MERGE_SCRIPT}"' 
        run_command(cmd_merge, description="Merge Train (Process PRs)")

        # Step 4: Git Pull (Sync Codebase)
        run_command("git pull", cwd=PROJECT_ROOT, description="Git Pull (Sync Codebase)")

        # Step 5: Sync Backlog (Update checkmarks)
        cmd_sync = f'python "{SYN_SCRIPT}"'
        run_command(cmd_sync, description="Sync Backlog Status")

    print("\n🏁 Automation Cycle Completed.")

if __name__ == "__main__":
    main()
