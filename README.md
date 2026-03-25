<div align="center">

```
 ██████╗ ██╗████████╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗
██╔════╝ ██║╚══██╔══╝    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
██║  ███╗██║   ██║       ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
██║   ██║██║   ██║       ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
╚██████╔╝██║   ██║       ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═╝   ╚═╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
```

**Switch Git accounts in one click.**  
Manage profiles, global config, and credential helpers — all from a clean desktop UI.

<br/>

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-238636?style=flat-square)
![Dependencies](https://img.shields.io/badge/Dependencies-None-success?style=flat-square)
![Git](https://img.shields.io/badge/Requires-Git-F05032?style=flat-square&logo=git&logoColor=white)

</div>

---

## What is this?

Git Manager is a lightweight desktop app for developers who work with **multiple Git identities** — personal projects, work accounts, freelance clients, open source contributions.

Instead of remembering and typing `git config --global user.name` every time you switch contexts, Git Manager lets you **save all your accounts once** and switch between them with a single click.

```
┌─────────────────────────────────────────────────────┐
│  ⬡  GIT MANAGER                                     │
├───────────────┬──────────────────┬──────────────────┤
│   Profiles    │  Global Config   │ Credential Helpers│
├───────────────┴──────────────────┴──────────────────┤
│                                                      │
│  ● work@company.com          [ Apply ] [ Edit ] [✕] │
│  ○ personal@gmail.com        [ Apply ] [ Edit ] [✕] │
│  ○ freelance@client.com      [ Apply ] [ Edit ] [✕] │
│                                                      │
│  ACTIVE:  John Doe (work@company.com)               │
└─────────────────────────────────────────────────────┘
```

---

## Features

- **Profile switching** — Save unlimited Git accounts (name + email + optional token). One click applies them globally.
- **Global config editor** — View and edit your entire `~/.gitconfig` as a live table. Double-click any row to update.
- **Credential helper management** — Set `manager`, `store`, `cache`, `osxkeychain`, `wincred`, or any custom helper in one click.
- **Zero dependencies** — Uses only Python's standard library (`tkinter`, `subprocess`, `json`, `os`).
- **Profiles persist** — Saved to `~/.git_manager_profiles.json`, survives reboots and reinstalls.
- **Works everywhere** — Windows, macOS, Linux.

---

## Prerequisites

| Tool | Version | Check | Download |
|------|---------|-------|----------|
| Python | 3.8+ | `python --version` | [python.org](https://www.python.org/downloads) |
| Git | Any | `git --version` | [git-scm.com](https://git-scm.com/downloads) |
| pip | Any | `pip --version` | Included with Python |

> **Windows:** During Python install, check **"Add Python to PATH"** or the commands below won't work.

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-username/git-manager.git
cd git-manager

# 2. Run it  (no pip install needed)
python git_manager.py          # Windows
python3 git_manager.py         # macOS / Linux
pythonw git_manager.py         # Windows — hides the console window
```

That's it. The app opens immediately.

> **Linux only:** If you get a tkinter error, install it first:
> ```bash
> sudo apt install python3-tk    # Debian / Ubuntu
> sudo dnf install python3-tkinter  # Fedora
> ```

---

## Build a Standalone .exe (Windows)

If you want to share the app or run it without Python installed:

```bash
# Step 1 — Install PyInstaller
pip install pyinstaller

# Step 2 — Build (or just double-click build_exe.bat)
pyinstaller --onefile --noconsole --name GitManager git_manager.py

# Step 3 — Your exe is here:
#   dist\GitManager.exe
```

Move `GitManager.exe` anywhere. It's fully self-contained — no Python needed on the target machine.

**To bake a custom icon into the exe:**
```bash
pyinstaller --onefile --noconsole --icon=icon.ico --name GitManager git_manager.py
```

---

## Desktop Shortcut & Taskbar Pin

### 🪟 Windows

1. Right-click empty desktop → **New → Shortcut**
2. Set the target:
   - For Python: `pythonw "C:\full\path\to\git_manager.py"`
   - For EXE: `"C:\full\path\to\dist\GitManager.exe"`
3. Name it **Git Manager** → click **Finish**
4. Right-click the shortcut → **Pin to taskbar**

**Change the icon:**
Right-click shortcut → **Properties** → **Shortcut tab** → **Change Icon...** → browse to a `.ico` file.

Get free icons at [icon-icons.com](https://icon-icons.com) — search `"git"` or `"terminal"`.

---

### 🍎 macOS

```bash
# Create a launcher script
cat > ~/Desktop/GitManager.command << 'EOF'
#!/bin/bash
cd /path/to/git-manager
python3 git_manager.py
EOF

# Make it executable
chmod +x ~/Desktop/GitManager.command
```

Double-click `GitManager.command` to launch.  
**Dock pin:** Run the app once → right-click Dock icon → **Options → Keep in Dock**.

**Change the icon:**
1. Export your icon as PNG (Preview → File → Export)
2. Right-click `GitManager.command` → **Get Info** (`Cmd+I`)
3. Drag the PNG onto the icon thumbnail at the top-left of Get Info

---

### 🐧 Linux

```bash
# Create a .desktop launcher
cat > ~/.local/share/applications/git-manager.desktop << 'EOF'
[Desktop Entry]
Name=Git Manager
Exec=python3 /path/to/git_manager.py
Icon=/path/to/icon.png
Type=Application
Categories=Development;
EOF

# Make it executable
chmod +x ~/.local/share/applications/git-manager.desktop
```

It now appears in your application launcher. Pin it to your taskbar/dock from there.

---

## How It Works

### Tab 1 — Profiles

Save as many Git identities as you need. Each profile stores:

| Field | Description |
|-------|-------------|
| Name | `git config user.name` value |
| Email | `git config user.email` value |
| Token | Optional — stored locally in `~/.git_manager_profiles.json` |
| Token hint | Masked preview (e.g. `ghp_****ab`) shown in the UI |

Clicking **Apply** runs:
```bash
git config --global user.name  "Your Name"
git config --global user.email "your@email.com"
```

The active account is highlighted in green.

---

### Tab 2 — Global Config

A live view of your entire `~/.gitconfig`. Every key-value pair is listed and editable.

- **Double-click** any row to edit the value inline
- **Quick-set** buttons for `user.name`, `user.email`, `core.editor`
- **Add Key** to insert any new config entry

---

### Tab 3 — Credential Helpers

One-click buttons to set the most common credential helpers:

| Helper | Best for |
|--------|----------|
| `manager` | Git Credential Manager (Windows/macOS recommended) |
| `manager-core` | Git Credential Manager Core (older GCM) |
| `store` | Plaintext file (`~/.git-credentials`) |
| `cache` | In-memory, expires after 15 min |
| `osxkeychain` | macOS Keychain |
| `wincred` | Windows Credential Store |

Or type any custom helper and click **Apply**.

---

## File Structure

```
git-manager/
├── git_manager.py          # Main application (run this)
├── build_exe.bat           # Windows: builds GitManager.exe
├── README.md               # This file
├── SETUP.md                # Detailed setup guide
└── GitManager_Setup_Guide.pdf   # Printable PDF guide
```

**Runtime files created automatically:**
```
~/.git_manager_profiles.json    # Your saved Git profiles
```

---

## Security Notes

- Profiles (including optional tokens) are saved in **plaintext** at `~/.git_manager_profiles.json`.
- This file is only readable by your OS user account.
- For production/team use, consider storing tokens in your OS keychain and leaving the token field blank in the profile.
- Git Manager only runs `git config` commands — it never sends data anywhere.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `python: command not found` | Use `python3` instead, or reinstall Python with PATH enabled |
| `ModuleNotFoundError: tkinter` | `sudo apt install python3-tk` (Linux) |
| App opens then closes immediately | Run from terminal to see error output |
| `git: command not found` | Install Git and restart your terminal |
| Changes not applying | Make sure Git is installed and accessible from terminal |
| Profiles lost after update | They're in `~/.git_manager_profiles.json` — back this file up |

---

## Quick Reference

```
Run app (Windows)         python git_manager.py
Run app (macOS/Linux)     python3 git_manager.py
Run (no console)          pythonw git_manager.py
Build .exe                build_exe.bat  or  pyinstaller --onefile ...
Build with icon           pyinstaller --onefile --icon=icon.ico ...
Desktop shortcut          Right-click desktop → New → Shortcut
Pin to taskbar            Right-click shortcut → Pin to taskbar
Change shortcut icon      Shortcut → Properties → Change Icon
Profiles file             ~/.git_manager_profiles.json
```

---

## Contributing

Pull requests welcome. To add a feature or fix a bug:

```bash
git clone https://github.com/your-username/git-manager.git
cd git-manager
# make your changes to git_manager.py
python git_manager.py   # test it
# open a PR
```

---

## License

MIT — do whatever you want with it.

---

<div align="center">

Made with `git config` and frustration.

</div>
