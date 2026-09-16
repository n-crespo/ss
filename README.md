# ss 📸

A lightweight Windows region-snipping utility built with Python and PyQt6. Designed to launch instantly and stay out of your way.

## Features

- **Minimalist Workflow**:
  - **Left-Click + Drag**: Capture region $\rightarrow$ Copy image to clipboard.
  - **Right-Click + Drag**: Capture region $\rightarrow$ Copy image to clipboard and save to `~/Downloads` as `Screenshot-YYYY-MM-DD_HH-MM-SS.png`.
  - **Escape Key**: Dismiss overlay.
- **Zero Config**: No setup required. PRs for customisability are welcome.

## Installation

1. Go to the **[Releases](https://github.com/n-crespo/ss/releases)** page.
2. Download the latest `ss.zip`.
3. Extract `ss.zip` to your preferred directory (e.g., `C:\Tools\ss`).
4. Run `ss.exe` manually, or add to your Path

> **Important:** Keep `ss.exe` and its `_internal/` folder in the same directory.

## Usage

Add your install directory (e.g., `C:\Tools\ss`) to your Windows User `PATH` via PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools\ss", "User")
```

After restarting your terminal, invoke the utility from anywhere by running:

```ps1
ss
```

### (optional) AutoHotkey Shortcut (`Win + Shift + S`)

To replace Windows Snipping Tool with `ss`, you can map it with AutoHotkey:

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

## Build from Source

### Prerequisites

- Python 3.11+
- `just` (`winget install Casey.Just`)

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

# build executable
just build
# clean artifacts
just clean
```
