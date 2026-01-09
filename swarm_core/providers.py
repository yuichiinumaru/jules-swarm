from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path
import re

class Task:
    def __init__(self, id: str, description: str, metadata: Optional[Dict[str, Any]] = None):
        self.id = id
        self.description = description
        self.metadata = metadata or {}
    
    def __repr__(self):
        return f"Task(id='{self.id}', desc='{self.description[:30]}...')"

class TaskProvider(ABC):
    @abstractmethod
    def get_tasks(self, limit: int = 0) -> List[Task]:
        """Returns a list of tasks."""
        pass

    @abstractmethod
    def on_dispatch(self, task: Task) -> None:
        """Called when a task is successfully dispatched."""
        pass

class SimpleFileProvider(TaskProvider):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_tasks(self, limit: int = 0) -> List[Task]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Task list not found at {self.file_path}")
        
        with open(self.file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        tasks = []
        for i, line in enumerate(lines):
            tasks.append(Task(id=line, description=line))
            if limit > 0 and len(tasks) >= limit:
                break
        return tasks

    def on_dispatch(self, task: Task) -> None:
        pass  # Simple files don't track state

class BacklogProvider(TaskProvider):
    def __init__(self, backlog_path: str):
        self.backlog_path = Path(backlog_path)

    def get_tasks(self, limit: int = 0) -> List[Task]:
        if not self.backlog_path.exists():
            raise FileNotFoundError(f"Backlog not found at {self.backlog_path}")

        content = self.backlog_path.read_text(encoding="utf-8")
        # Matches: ### [ ] Paper {ID}
        pattern = r"### \[ \] Paper (.*?)$"
        matches = re.findall(pattern, content, re.MULTILINE)
        
        tasks = []
        for match in matches:
            paper_id = match.strip()
            # Construct URLs for context
            id_with_v = paper_id if "v" in paper_id else f"{paper_id}v1"
            html_url = f"https://arxiv.org/html/{id_with_v}"
            pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
            
            tasks.append(Task(
                id=paper_id,
                description=f"Process Paper {paper_id}",
                metadata={
                    "paper_id": paper_id,
                    "html_url": html_url,
                    "pdf_url": pdf_url
                }
            ))
            if limit > 0 and len(tasks) >= limit:
                break
        return tasks

    def on_dispatch(self, task: Task) -> None:
        if not self.backlog_path.exists():
            return

        content = self.backlog_path.read_text(encoding="utf-8")
        paper_id = task.id
        
        # Pattern: Header followed by status line
        target_pattern = rf"### \[ \] Paper {re.escape(paper_id)}\n- \*\*Status:\*\* Pending"
        replacement = f"### [/] Paper {paper_id}\n- **Status:** Dispatched"
        
        if re.search(target_pattern, content):
            new_content = re.sub(target_pattern, replacement, content)
            self.backlog_path.write_text(new_content, encoding="utf-8")
            print(f"📝 Marked {paper_id} as Dispatched in backlog.")
        else:
            # Fallback
            target_v2 = f"### [ ] Paper {paper_id}"
            if target_v2 in content:
                new_content = content.replace(target_v2, f"### [/] Paper {paper_id}")
                self.backlog_path.write_text(new_content, encoding="utf-8")
                print(f"📝 Marked {paper_id} as Dispatched (fallback).")
