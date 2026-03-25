# ⬡ Git Manager — Setup Guide

> Manage multiple Git accounts, switch global configs in one click, and handle credential helpers — all from a clean desktop UI.

---

## Prerequisites

| Tool | Why | Check |
|------|-----|-------|
| Python 3.8+ | Runs the app | `python --version` |
| Git | Executes git commands | `git --version` |
| pip | Builds .exe (optional) | `pip --version` |

- **Python:** https://www.python.org/downloads  _(check "Add Python to PATH")_
- **Git:** https://git-scm.com/downloads

---

## 1. Clone the Repo

```bash
git clone https://github.com/your-username/git-manager.git
cd git-manager
```

Or download the ZIP from GitHub and extract it anywhere.

---

## 2. Run with Python

Git Manager uses **only built-in Python libraries** — no `pip install` needed to run.

**Windows:**
```bash
python git_manager.py
```

**macOS / Linux:**
```bash
python3 git_manager.py
```

> 💡 On Windows, use `pythonw git_manager.py` to hide the black console window.

> ⚠️ On some Linux distros, tkinter is a separate package:
> ```bash
> sudo apt install python3-tk
> ```

---

## 3. Build a Standalone .exe (Windows only)

After this you get a single `GitManager.exe` — no Python needed on the target machine.

**Step 1 — Install PyInstaller:**
```bash
pip install pyinstaller
```

**Step 2 — Run the build script:**
```bash
# Double-click build_exe.bat  OR run in terminal:
build_exe.bat
```

**Step 3 — Find your EXE:**
```
dist\GitManager.exe
```

You can move this `.exe` anywhere — it's fully self-contained.

---

## 4. Create a Desktop Shortcut

### 🪟 Windows 10 / 11

**Step 1 — Right-click empty desktop area:**
- Right-click → **New** → **Shortcut**

**Step 2 — Set the target path:**

For the Python script:
```
pythonw "C:\full\path\to\git_manager.py"
```

For the .exe (after building):
```
"C:\full\path\to\dist\GitManager.exe"
```

**Step 3 — Name it:**
- Type `Git Manager` → click **Finish**

**Step 4 — Pin to Taskbar:**
- Right-click the new desktop shortcut → **Pin to taskbar**

---

### 🍎 macOS

**Step 1 — Create a launcher script:**

Create a file called `GitManager.command` with this content:
```bash
#!/bin/bash
cd /path/to/git-manager
python3 git_manager.py
```

Make it executable:
```bash
chmod +x ~/Desktop/GitManager.command
```

**Step 2 — Move to Desktop:**
- Double-click `GitManager.command` to launch.

**Step 3 — Add to Dock:**
- Run the app once, then right-click its Dock icon
- → **Options** → **Keep in Dock**

---

## 5. Change the App Icon

### Step A — Get a .ico file

Download a free icon from:

| Site | Notes |
|------|-------|
| [icon-icons.com](https://icon-icons.com) | Large library, direct .ico download |
| [flaticon.com](https://flaticon.com) | Huge collection, free with attribution |
| [icons8.com](https://icons8.com) | Search and download .ico directly |

Search for `"git"` or `"terminal"` and download a `.ico` file.

---

### Step B — Set icon on Windows shortcut

1. Right-click the desktop shortcut → **Properties**
2. Go to the **Shortcut** tab → click **Change Icon...**
3. Browse to your `.ico` file → click **OK**
4. Click **Apply** → click **OK**

The icon updates immediately on your desktop and taskbar.

---

### Step C — Bake icon into the .exe (Windows)

Rebuild with PyInstaller adding the `--icon` flag:

```bash
pyinstaller --onefile --noconsole --icon=icon.ico --name GitManager git_manager.py
```

Replace `icon.ico` with the path to your icon. The resulting `dist\GitManager.exe` carries the icon permanently — no shortcut needed.

---

### Step D — Set icon on macOS

1. Open your `.ico` in **Preview** → File → Export as **PNG**
2. Right-click `GitManager.command` → **Get Info** (or `Cmd+I`)
3. Drag your PNG onto the small icon thumbnail at the top-left of the Get Info window
4. Icon updates immediately

---

## Quick Reference

| What | Command / Action |
|------|-----------------|
| Run (Windows) | `python git_manager.py` |
| Run (macOS/Linux) | `python3 git_manager.py` |
| Run (no console) | `pythonw git_manager.py` |
| Build .exe | Double-click `build_exe.bat` |
| Desktop shortcut | Right-click desktop → New → Shortcut |
| Pin to taskbar | Right-click shortcut → Pin to taskbar |
| Change icon (shortcut) | Shortcut → Properties → Change Icon |
| Change icon (exe) | Add `--icon=icon.ico` to pyinstaller command |
| Profiles saved at | `~/.git_manager_profiles.json` |

---

## How It Works

| Tab | What it does |
|-----|-------------|
| **Profiles** | Save Git accounts (name + email + token). One-click switches `user.name` & `user.email` globally |
| **Global Config** | View/edit your full `~/.gitconfig`. Double-click any row to edit inline |
| **Credential Helpers** | Set `credential.helper` (manager, store, cache, osxkeychain, etc.) |

---

_Git Manager • Profiles stored in `~/.git_manager_profiles.json` • Requires Python 3.8+ and Git_
