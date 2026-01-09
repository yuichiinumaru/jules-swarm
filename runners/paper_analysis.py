#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

# Add repo root to path to allow importing 'research'
# Script is in research/runners/, so root is 3 levels up
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))

from research.swarm_core.config import SwarmConfig
from research.swarm_core.providers import BacklogProvider
from research.swarm_core.prompts import DynamicBuilder
from research.swarm_core.launcher import SwarmLauncher

# Define the specific prompt template for paper analysis
PAPER_ANALYSIS_PROMPT_TEMPLATE = """
[PHASE 1: CONTEXT UPLOAD]
INSTRUCTION:
1. Access the provided URLs to read the paper PDF and its semantic details.
2. Analyze the paper content deeply.

[PHASE 2: METHODOLOGY]
INSTRUCTION:
- You are a Research Scientist specialized in AI/ML.
- Produce a structured summary and analysis.

[PHASE 3: EXECUTION]
TASK: Analyze Paper {paper_id}
DETAILS:
- Title: {title}
- PDF URL: {pdf_url}
- Semantic URL: {semantic_url}

OUTPUT FORMAT:
Return a Markdown file with:
# {title}
## Summary
...
## Key Innovations
...
## Relevance to Project
...
## Code Implementation Ideas
...

[PHASE 4:VERIFICATION]
REQUIREMENT:
- The output must be valid Markdown.
- No hallucinations.
!EXECUTE_PROTOCOL
"""

def main():
    parser = argparse.ArgumentParser(description="Jules Swarm: Paper Analysis Launcher")
    parser.add_argument("-n", "--concurrency", type=int, default=3, help="Batch size")
    parser.add_argument("--repo", default="yuichiinumaru/void_research", help="GitHub repository name")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    args = parser.parse_args()

    # Config
    config = SwarmConfig(env_path=repo_root / ".env")
    
    # Provider (Backlog)
    backlog_path = repo_root / "research/docs/RESEARCH_BACKLOG.md"
    if not backlog_path.exists():
        print(f"❌ Error: Backlog file not found at {backlog_path}")
        sys.exit(1)
        
    provider = BacklogProvider(str(backlog_path))
    
    # Prompt
    builder = DynamicBuilder(PAPER_ANALYSIS_PROMPT_TEMPLATE)

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
