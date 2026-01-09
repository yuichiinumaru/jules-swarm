#!/usr/bin/env python3
import subprocess
import json
import time
import sys

def run_command(command, shell=True):
    """Utility to run shell commands and return output."""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None

def check_gh_installed():
    """Verify that GitHub CLI is installed."""
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_open_prs():
    """Fetch open PRs ordered by creation date."""
    print("📋 Fetching open Pull Requests...")
    cmd = 'gh pr list --state open --limit 100 --json number,createdAt'
    output = run_command(cmd)
    
    if not output:
        return []
        
    try:
        prs = json.loads(output)
        # Sort by creation date (oldest first)
        prs.sort(key=lambda x: x['createdAt'])
        return prs
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error parsing PR list: {e}")
        return []

import argparse

def process_pr(pr_number, current, total, dry_run=False):
    """Attempt to merge a single PR."""
    print("-" * 50)
    print(f"🔨 Processing PR #{pr_number} ({current}/{total})...")
    
    if dry_run:
        print(f"🔍 [Dry Run] Would merge PR #{pr_number}")
        return True

    # 1. Mark as ready (in case it's a draft)
    run_command(f'gh pr ready {pr_number}')
    
    # 2. Attempt squash merge
    merge_cmd = f'gh pr merge {pr_number} --squash --delete-branch'
    result = run_command(merge_cmd)
    
    if result is not None:
        print(f"✅ Success! PR #{pr_number} merged and branch deleted.")
        return True
    else:
        print(f"⚠️  Conflict or CI Error on PR #{pr_number}. Skipping...")
        return False

def main():
    parser = argparse.ArgumentParser(description="🚂 Python Merge Train (Oldest -> Newest)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be merged without performing actual merges")
    args = parser.parse_args()

    print("🚂 Starting the Python Merge Train (Oldest -> Newest)...")
    if args.dry_run:
        print("🔍 RUNNING IN DRY-RUN MODE")
    
    if not check_gh_installed():
        print("❌ Error: GitHub CLI (gh) is not installed.")
        sys.exit(1)
        
    prs = get_open_prs()
    
    if not prs:
        print("✅ No open PRs to process.")
        return

    total = len(prs)
    print(f"📋 Found {total} open PRs.")
    
    merged_count = 0
    for i, pr in enumerate(prs, 1):
        if process_pr(pr['number'], i, total, dry_run=args.dry_run):
            merged_count += 1
        
        # Fast sleep to be nice to API
        time.sleep(1)
        
    print("-" * 50)
    status_text = "Would have merged" if args.dry_run else "Merged"
    print(f"🏁 End of line. {status_text} {merged_count}/{total} PRs.")
    print("Remaining PRs require manual attention.")

if __name__ == "__main__":
    main()
