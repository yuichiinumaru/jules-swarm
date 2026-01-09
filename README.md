# Jules Swarm

Welcome to **Jules Swarm**! This project allows you to run a "swarm" of AI agents using the Jules API. Think of it as managing a team of virtual assistants that work together to solve complex tasks for you.

## 🚀 Getting Started

Follow these steps to get everything up and running.

### 1. Prerequisites

- **Python 3.10+**: Make sure you have Python installed.
  ```bash
  python --version
  ```

### 2. Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yuichiinumaru/jules-swarm.git
    cd jules-swarm
    ```

2.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` and add your **Jules API Key**:
      ```text
      JULES_API_KEYS="your_api_key_here"
      ```
      *(You can get a key at [jules.google.com/settings/api](https://jules.google.com/settings/api))*

## 🏃 Usage

The project is organized into modular "runners" located in the `runners/` directory.

### Generic Swarm
Launches a standard swarm to execute tasks defined in a file.
```bash
python runners/generic_swarm.py --task-file tasks/test_atom.txt
```

### Paper Analysis Swarm
Specialized swarm for analyzing research papers.
```bash
python runners/paper_analysis.py --repo "your/repo-name"
```

### Check Status
Check the status of active sessions.
```bash
python runners/check_status.py
```

### Inspect Session
Get detailed JSON dump of a specific session.
```bash
python runners/inspect_session.py --session-id "YOUR_SESSION_ID"
```

### Poke Session
Send a message/input to an active session.
```bash
python runners/poke_session.py --session-id "YOUR_SESSION_ID" --message "Proceed with the plan."
```

## 📂 Project Structure

- **`swarm_core/`**: The brain of the operation. Contains the core logic, API handling, and configuration.
- **`runners/`**: Entry points for different types of swarms (generic, research, maintenance).
- **`utils/`**: Helper scripts for data processing and maintenance.
- **`tasks/`**: Text files defining tasks for the generic swarm.
- **`prompts/`**: Prompt templates used by the agents.
- **`data/`**: Storage for input data (e.g., paper IDs, repo lists).
- **`docs/`**: Documentation and protocols.
- **`state/`**: JSON files storing the state of active sessions.

## 🆘 Troubleshooting

- **"Module not found"**: Ensure you are running the scripts from the **root** folder (`jules-swarm`). Do not `cd` into `runners/` before running.
  - Correct: `python runners/generic_swarm.py`
  - Incorrect: `cd runners && python generic_swarm.py`

---
*Happy Swarming!*
