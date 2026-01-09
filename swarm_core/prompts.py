from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

class PromptBuilder(ABC):
    @abstractmethod
    def build(self, task_context: Dict[str, Any]) -> str:
        pass

class FileTemplateBuilder(PromptBuilder):
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        if not self.template_path.exists():
             # Fallback logic could go here or raise error
             pass

    def build(self, task_context: Dict[str, Any]) -> str:
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
            
        content = self.template_path.read_text(encoding="utf-8")
        # Simple replacement
        for key, value in task_context.items():
            placeholder = f"[{key.upper()}]"
            content = content.replace(placeholder, str(value))
        return content

class DynamicBuilder(PromptBuilder):
    def __init__(self, template_str: str):
        self.template_str = template_str

    def build(self, task_context: Dict[str, Any]) -> str:
        # Use python formatting
        return self.template_str.format(**task_context)
