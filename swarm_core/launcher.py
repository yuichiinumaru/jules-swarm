import time
import sys
from typing import Optional
from .config import SwarmConfig
from .api import JulesAPI
from .providers import TaskProvider
from .prompts import PromptBuilder

class SwarmLauncher:
    def __init__(self, 
                 config: SwarmConfig, 
                 provider: TaskProvider, 
                 prompt_builder: PromptBuilder,
                 repo_name: str,
                 concurrency: int = 1,
                 dry_run: bool = False):
        
        self.config = config
        self.provider = provider
        self.prompt_builder = prompt_builder
        self.repo_name = repo_name
        self.concurrency = concurrency
        self.dry_run = dry_run
        
        self.api = JulesAPI(config.api_base_url)

    def run(self):
        print(f"🚀 Starting Swarm Launcher for {self.repo_name}")
        tasks = self.provider.get_tasks()
        print(f"📋 Found {len(tasks)} tasks.")
        
        if not tasks:
            print("✅ No tasks found. Exiting.")
            sys.exit(10) # 10 = No tasks code

        active_count = 0
        
        for i, task in enumerate(tasks):
            # Key Rotation
            current_key = self.config.get_api_key(i)
            
            # Resolve Source ID
            if self.dry_run:
                source_name = "projects/mock/sources/mock"
            else:
                source_name = self.api.get_source_name(current_key, self.repo_name)
                if not source_name:
                    print(f"⏭️ Skipping task {task.id} due to source error.")
                    continue

            print(f"\n[{i+1}/{len(tasks)}] Processing: {task.description} (Key #{i % len(self.config.api_keys) + 1})")
            
            # Build Prompt
            context = {"component_name": task.id} # default
            if task.metadata:
                context.update(task.metadata)
                
            prompt = self.prompt_builder.build(context)
            
            # Create Session
            payload = {
                "prompt": prompt,
                "sourceContext": {
                    "source": source_name,
                    "githubRepoContext": { "startingBranch": "main" } 
                },
                "automationMode": "AUTO_CREATE_PR",
                "title": f"Task: {task.id}"
            }

            if self.dry_run:
                print(f"[DRY-RUN] Would create session for {task.id}")
                print(f"[DRY-RUN] Prompt Preview: {prompt[:100]}...")
            else:
                session = self.api.create_session(current_key, payload)
                if session:
                    print(f"🚀 Session Created! ID: {session.get('name')}")
                    self.provider.on_dispatch(task)
            
            active_count += 1
            
            # Throttling
            if active_count >= self.concurrency:
                print(f"⏳ Batch limit reached ({self.concurrency}). Pausing for 5 seconds...")
                time.sleep(5)
                active_count = 0
            else:
                time.sleep(1)

        print("\n✅ Batch dispatch completed.")
