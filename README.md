# ss 📸

A lightweight Windows region-snipping utility built with Python and PyQt6. Designed to launch instantly and stay out of your way.

---

## Features

- **Minimalist Workflow**:
  - **Left-Click + Drag**: Capture region $\rightarrow$ Copy image to clipboard.
  - **Right-Click + Drag**: Capture region $\rightarrow$ Copy image to clipboard **AND** save directly to `~/Downloads` as `Screenshot-YYYY-MM-DD_HH-MM-SS.png`.
  - **Escape Key**: Dismiss overlay.
- **Zero Config**: No setup required. PRs for customisability are welcome.

---

## Installation

1. Go to the **[Releases](https://github.com/n-crespo/ss/releases)** page.
2. Download the latest `ss.zip`.
3. Extract `ss.zip` to your preferred directory (e.g., `C:\Tools\ss`).

> **Important:** Keep `ss.exe` and its `_internal/` folder in the same directory.

---

## Usage & Global Hotkey Setup

### Option A: Add to System PATH

Add your install directory (e.g., `C:\Tools\ss`) to your Windows User `PATH` via PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools\ss", "User")
```

After restarting your terminal, invoke the utility from anywhere by running:

```ps1
ss
```

### Option B: AutoHotkey Shortcut (`Win + Shift + S`)

To replace or augment the standard Windows Snipping Tool with `ss`, map it using AutoHotkey:

> [!NOTE]
> This is using AutoHotkey v1 syntax, and expects `ss.exe` to be in your path. A
> restart may be required.

```ahk
#Requires AutoHotkey v1.1
#NoEnv
#SingleInstance Force
SendMode Input

+#s:: Run, ss

```

## Local Development

### Prerequisites

- Python 3.11+
- `just` task runner (`winget install Casey.Just`)

### Setup Environment

```ps1
# Clone the repository
git clone https://github.com/n-crespo/ss.git
cd ss

# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# build exe
just build
# clean artifacts
just clean
```
