# AGENTS.md

## 🤖 Welcome, AI Developer

If you are reading this, you are likely an AI agent executing a task within the **Jules Swarm** project. This document provides the critical context you need to operate effectively, safely, and autonomously in this codebase.

### 1. Project Overview
**What is this?**
This repository contains the source code for a "Swarm" of AI agents orchestrated via the Jules API. Ideally, it manages multiple sessions (manager + workers) to solve complex tasks.

**Core Goal:**
To automate multi-step workflows by delegating sub-tasks to specialized agent sessions.

### 2. Architecture & Key Files
The system is script-based (Python).

- **`scripts/launch_swarm_v3.py`**: The **Master Switch**. This script initializes the swarm logic.
- **`scripts/check_swarm_status.py`**: The **Monitor**. Use this to read the current state of sessions.
- **`scripts/state/sessions.json`**: The **State**. A JSON log of all active/past sessions. **DO NOT DELETE THIS** unless reset is explicitly requested.
- **`docs/jules-swarm-protocol.md`**: The **Constitution**. Defines how agents should communicate and behave. READ THIS if you are modifying swarm logic.

### 3. Operational Guide

#### How to Run the Swarm
```bash
python scripts/launch_swarm_v3.py
```

#### How to Check Status
```bash
python scripts/check_swarm_status.py
```

#### Configuration
- **API Keys**: Located in `.env`. Access this via `os.environ["JULES_API_KEYS"]`.
- **Requirements**: `requests` is the main external dependency.

### 4. Constraints & Rules
- **Methodology**: We follow **Cohesive Granularity**. Keep logic grouped by function.
- **Environment**: This code runs in a standard Python 3 env. No Docker, no heavy binaries.
- **Secrets**: NEVER output the contents of `.env` to the terminal or logs.

### 5. Critical Context
- **docs/** is the source of truth for the protocol. If code contradicts docs, check validation first, but usually docs lead design.
- **scripts/tasks/** and **scripts/prompts/** contain the "brain" instructions for the swarm agents.

---
*End of Context*
