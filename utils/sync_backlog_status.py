#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Paths
IDEAS_DIR = Path(r"f:\AI\cryptosentinel-v1\docs\ideas")
BACKLOG_PATH = Path(r"f:\AI\cryptosentinel-v1\docs\RESEARCH_BACKLOG.md")

def get_completed_paper_ids():
    """Scans docs/ideas/*.md and returns a list of paper IDs."""
    if not IDEAS_DIR.exists():
        print("⚠️  Ideas directory not found.")
        return []
    
    # Files are named like {ID}.md. 
    # Need to handle case sensitivity if windows, but IDs are usually specific.
    # Also handle v versions e.g. 1707.02275v1.md -> paper ID is 1707.02275v1
    
    ids = []
    for f in IDEAS_DIR.glob("*.md"):
        if f.name == ".gitkeep":
            continue
        # ID is filename minus extension
        ids.append(f.stem)
    return ids

def sync_backlog():
    if not BACKLOG_PATH.exists():
        print("❌ Backlog file not found.")
        return

    content = BACKLOG_PATH.read_text(encoding="utf-8")
    original_len = len(content)
    completed_ids = get_completed_paper_ids()
    print(f"found {len(completed_ids)} completed papers.")

    updated_count = 0
    
    # We will iterate through the file line by line to process blocks
    lines = content.splitlines()
    new_lines = []
    
    current_paper_id = None
    in_block = False
    
    # Patterns
    header_regex = re.compile(r"^### \[(.*?)\] Paper (.*?)$")
    
    for line in lines:
        match = header_regex.match(line)
        if match:
            # New block starting
            in_block = True
            current_status_char = match.group(1).strip()
            current_paper_id = match.group(2).strip()
            
            if current_paper_id in completed_ids:
                # Update Header to [x]
                new_line = f"### [x] Paper {current_paper_id}"
                new_lines.append(new_line)
                updated_count += 1
            else:
                new_lines.append(line)
        elif in_block and current_paper_id in completed_ids:
            # We are inside a block of a completed paper
            
            # Update Status line
            if line.strip().startswith("- **Status:**"):
                new_lines.append("- **Status:** Completed")
            # Update Task checkboxes
            elif "- [ ] Agent:" in line:
                new_lines.append(line.replace("- [ ] Agent:", "- [x] Agent:"))
            else:
                new_lines.append(line)
        else:
            # Outside block or not a completed paper
            new_lines.append(line)
            
    new_content = "\n".join(new_lines)
    
    if new_content != content:
        BACKLOG_PATH.write_text(new_content, encoding="utf-8")
        print(f"✅ Synced {updated_count} papers in RESEARCH_BACKLOG.md")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    sync_backlog()
