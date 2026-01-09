#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

# Add repo root to path to allow importing 'research'
# Script is in research/runners/, so root is 3 levels up
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))

from research.swarm_core.config import SwarmConfig
from research.swarm_core.providers import SimpleFileProvider
from research.swarm_core.prompts import FileTemplateBuilder
from research.swarm_core.launcher import SwarmLauncher

def main():
    parser = argparse.ArgumentParser(description="Jules Swarm Launcher (Universal Core)")
    parser.add_argument("-t", "--type", required=True, help="Type of component to refactor (atoms, molecules, organisms, or custom)")
    parser.add_argument("-n", "--concurrency", type=int, default=5, help="Batch size")
    parser.add_argument("--repo", required=True, help="GitHub repository name (owner/repo)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    
    args = parser.parse_args()

    # Config
    config = SwarmConfig(env_path=repo_root / ".env")
    
    # Paths (Absolute based on repo_root)
    tasks_dir = repo_root / "research/tasks"
    prompts_dir = repo_root / "research/prompts"
    
    # Provider
    tasks_file = tasks_dir / f"{args.type}.txt"
    if not tasks_file.exists():
        print(f"❌ Error: Task list not found at {tasks_file}")
        sys.exit(1)
    provider = SimpleFileProvider(str(tasks_file))
    
    # Prompt
    prompt_file = prompts_dir / f"{args.type}_prompt.md"
    # Fallback logic
    if not prompt_file.exists() and "_" in args.type:
        base_type = args.type.split("_")[0]
        fallback = prompts_dir / f"{base_type}_prompt.md"
        if fallback.exists():
             print(f"⚠️  Prompt file for '{args.type}' not found, using base prompt '{fallback}'")
             prompt_file = fallback
    
    if not prompt_file.exists():
        print(f"❌ Error: Prompt template not found at {prompt_file}")
        sys.exit(1)

    builder = FileTemplateBuilder(str(prompt_file))

    # Launch
    launcher = SwarmLauncher(
        config=config,
        provider=provider,
        prompt_builder=builder,
        repo_name=args.repo,
        concurrency=args.concurrency,
        dry_run=args.dry_run
    )
    
    try:
        launcher.run()
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
