import os
import platform
import subprocess
import re
from pathlib import Path

# -----------------------------
# 📁 PATH HELPERS
# -----------------------------

def _home_dir():
    return Path.home()

def _pictures_dir():
    return _home_dir() / "Pictures"

def _downloads_dir():
    return _home_dir() / "Downloads"

# -----------------------------
# 🌐 OPEN GOOGLE
# -----------------------------

def open_google():
    system = platform.system()

    if system == "Darwin":  # macOS
        subprocess.Popen(["open", "-a", "Google Chrome", "https://www.google.com"])
    elif system == "Windows":
        subprocess.Popen(["start", "chrome", "https://www.google.com"], shell=True)
    else:
        subprocess.Popen(["xdg-open", "https://www.google.com"])

    return "Opening Google"

# -----------------------------
# 🚀 UNIVERSAL APP OPENER
# -----------------------------

APP_MAP = {
    "calculator": "Calculator",
    "calc": "Calculator",
    "chrome": "Google Chrome",
    "google": "Google Chrome",
    "vscode": "Visual Studio Code",
    "code": "Visual Studio Code",
    "spotify": "Spotify",
    "terminal": "Terminal"
}

def open_application(app_name: str) -> str:
    system = platform.system()

    app_name = app_name.lower().strip()

    # map friendly names → real app names
    app_name = APP_MAP.get(app_name, app_name)

    try:
        if system == "Darwin":
            subprocess.Popen(["open", "-a", app_name])

        elif system == "Windows":
            subprocess.Popen(["start", app_name], shell=True)

        else:
            subprocess.Popen([app_name])

        return f"Opening {app_name}"

    except Exception as e:
        return f"Could not open {app_name}: {str(e)}"

# -----------------------------
# 📂 FOLDER OPEN
# -----------------------------

def open_pictures():
    subprocess.Popen(["open", str(_pictures_dir())])
    return "Opening Pictures"

def open_downloads():
    subprocess.Popen(["open", str(_downloads_dir())])
    return "Opening Downloads"

# -----------------------------
# 🔍 FILE SEARCH
# -----------------------------

def file_search(name: str):
    results = []
    for path in _home_dir().rglob(name):
        results.append(str(path))
        if len(results) >= 5:
            break

    if results:
        return "Found:\n" + "\n".join(results)
    return "File not found"

# -----------------------------
# 🎯 MAIN COMMAND EXECUTION
# -----------------------------

def execute_command(command: str) -> str:
    command = (command or "").strip().lower()

    # 🚀 UNIVERSAL OPEN COMMAND
    if command.startswith(("open ", "launch ", "start ")):
        app_name = command.replace("open ", "").replace("launch ", "").replace("start ", "").strip()

        # special handling
        if "google" in app_name or "browser" in app_name:
            return open_google()

        if "pictures" in app_name:
            return open_pictures()

        if "downloads" in app_name:
            return open_downloads()

        return open_application(app_name)

    # 🔍 FILE SEARCH
    if command.startswith("find ") or command.startswith("search "):
        file_name = command.split(" ", 1)[1]
        return file_search(file_name)

    return "Command not found"

def execute_multi_command(command: str):
    # split using "and"
    parts = command.split(" and ")

    results = []

    for part in parts:
        part = part.strip()

        result = execute_command(part)
        results.append(result)

    return " | ".join(results)