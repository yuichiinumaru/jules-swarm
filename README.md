# Jules Swarm

Welcome to **Jules Swarm**! This project allows you to run a "swarm" of AI agents using the Jules API. Think of it as managing a team of virtual assistants that work together to solve complex tasks for you.

## 🚀 Getting Started

Follow these simple steps to get everything up and running on your computer.

### 1. Prerequisites (What you need installed)

Before you begin, make sure you have **Python** installed.
- **Check if you have it:** Open your terminal (Command Prompt or PowerShell) and type:
  ```bash
  python --version
  ```
- **If not installed:** Download and install it from [python.org](https://www.python.org/downloads/) or [anaconda.com](https://www.anaconda.com/download/success). Make sure to check the box **"Add Python to PATH"** during installation! 

### 2. Setup (One-time only)

1.  **Download this code**:
    - Click the green **Code** button and select **Download ZIP**, then extract it.
    - OR use git: `git clone https://github.com/your-username/jules-swarm.git`

2.  **Open a Terminal**:
    - Go to the folder where you extracted the code.
    - Right-click inside the folder and select "Open in Terminal" (or "Open PowerShell window here").

3.  **Install Requirements**:
    - Run this specific command to install the necessary tools:
      ```bash
      pip install -r requirements.txt
      ```

4.  **Configure your API Key**:
<img width="714" height="415" alt="image" src="https://github.com/user-attachments/assets/66779d51-b72d-493b-83f4-13ed4679bc9f" />
    - You need a "key" to talk to the Jules AI. Get one at https://jules.google.com/settings/api
    - Copy the file named `.env.example` and rename the copy to `.env`.
    - Open `.env` with any text editor (Notepad is fine).
    - Replace `your_api_key_here` with your actual Jules API key.
      ```text
      JULES_API_KEYS="your_actual_secret_key_starts_with_AI..."
      ```
    - Save the file.

### 3. How to Run It

Now you are ready to launch the swarm!

1.  **Start the Swarm**:
    - In your terminal, run:
      ```bash
      python scripts/launch_swarm_v3.py
      ```

2.  **What happens next?**
    - The script will start and begin managing AI sessions.
    - It saves its progress in `scripts/state/sessions.json`.

3.  **Check Status**:
    - To see what your swarm is doing, you can run:
      ```bash
      python scripts/check_swarm_status.py
      ```

## 📂 Project Structure

- `scripts/`: Contains the magic python scripts that run the swarm.
- `docs/`: specific documentation about the protocol and research.
- `.env`: Your private key file (NEVER share this file!).

## 🆘 Need Help?

If you see an error saying "Module not found", try running `pip install -r requirements.txt` again.
If you see "Error reading state file", don't worry, it just means no sessions have started yet.

---
*Happy Swarming!*
