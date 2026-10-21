# 🛠️ Cricbuzz LiveStats — Setup & Installation Guide

This document provides complete instructions for configuring, initializing, and running the **Cricbuzz LiveStats** application across local development environments and cloud platforms.

---

## 📋 System Prerequisites

| Requirement | Minimum | Recommended |
| :--- | :--- | :--- |
| **Operating System** | Windows 10+, macOS 12+, Ubuntu 20.04+ | Windows 11 / macOS Sequoia |
| **Python** | Python 3.10 | Python 3.11.x |
| **RAM** | 2 GB | 4 GB+ |
| **Disk Space** | 200 MB | 500 MB |
| **Web Browser** | Chrome, Edge, Safari, Firefox | Chrome / Edge |

---

## 🚀 Local Installation

### Step 1: Clone or Open Project
Ensure you are located inside the root project directory:
```bash
cd "Cricbuzz Project"
```

### Step 2: Initialize Virtual Environment

#### Windows (PowerShell):
```powershell
# Create environment
python -m venv .venv

# If script execution is restricted, enable RemoteSigned for current process:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate
.\.venv\Scripts\Activate.ps1
```

#### macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### Step 3: Install Required Dependencies
Install all production and test packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Secrets (RapidAPI)
Create a `.env` file in the root directory:
```env
RAPIDAPI_KEY=66ff04a6a4mshf41fde1449c1811p17111ejsn1c376b099f19
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
```

> [!NOTE]
> If `RAPIDAPI_KEY` is omitted or left blank, the application will automatically run in **Offline Mock Mode** using realistic bundled datasets with zero errors.

---

### Step 5: Initialize the Database (Optional)
The database auto-initializes on first launch, but can be manually bootstrapped or verified by running:
```bash
python utils/db_connection.py
```
Expected output:
```text
Database Initialized Successfully! Table Row Counts:
  • teams           :    6 rows
  • venues          :   10 rows
  • series          :    9 rows
  • players         :   26 rows
  • matches         :   26 rows
  • batting_stats   :   58 rows
  • bowling_stats   :   55 rows
  • fielding_stats  :   24 rows
```

---

### Step 6: Run the Test Suite
Verify that all 47 unit tests pass:
```bash
pytest tests/ -v
```

---

### Step 7: Launch the Application
Start the Streamlit development server:
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## ❓ Troubleshooting & FAQs

### 1. `Cannot find module dotenv`
**Fix**: Install `python-dotenv`:
```bash
.\.venv\Scripts\pip.exe install python-dotenv
```
Ensure your IDE interpreter is set to `.\.venv\Scripts\python.exe`.

### 2. `Execution of scripts is disabled on this system` (PowerShell)
**Fix**: Run PowerShell as Administrator or execute:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Port 8501 already in use
**Fix**: Launch Streamlit on a custom port:
```bash
streamlit run app.py --server.port 8502
```
