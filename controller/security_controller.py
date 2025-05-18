import subprocess
import re
import json
import os

BLACKLIST_FILE = os.path.join(os.path.dirname(__file__), "blacklist.json")

SUSPICIOUS_KEYWORDS = [
    "ad", "ads", "boost", "clean", "popup", "notifier",
    "saver", "battery", "locker", "speed", "fast"
]

def get_installed_packages():
    try:
        output = subprocess.check_output(["adb", "shell", "pm", "list", "packages", "-3"], encoding="utf-8")
        return [line.replace("package:", "").strip() for line in output.splitlines()]
    except Exception as e:
        return []

def get_app_label(package):
    try:
        dump = subprocess.check_output(["adb", "shell", "dumpsys", "package", package], encoding="utf-8")
        match = re.search(r"application-label:'([^']+)'", dump)
        return match.group(1) if match else package
    except:
        return package

def check_blacklisted_packages():
    if not os.path.exists(BLACKLIST_FILE):
        return []

    with open(BLACKLIST_FILE, "r") as f:
        data = json.load(f)

    installed = get_installed_packages()
    blacklist = data.get("apps", [])

    matches = []
    for pkg in installed:
        if pkg in blacklist:
            matches.append((pkg, get_app_label(pkg)))

    return matches

def check_suspicious_by_keywords():
    installed = get_installed_packages()
    suspicious = []

    for pkg in installed:
        name = get_app_label(pkg).lower()
        for kw in SUSPICIOUS_KEYWORDS:
            if kw in name or kw in pkg.lower():
                suspicious.append((pkg, get_app_label(pkg)))
                break

    return suspicious

def has_overlay_permission(package):
    try:
        output = subprocess.check_output(
            ["adb", "shell", "dumpsys", "package", package],
            encoding="utf-8"
        )
        return "SYSTEM_ALERT_WINDOW" in output
    except:
        return False

def check_overlay_threats():
    installed = get_installed_packages()
    threats = []

    for pkg in installed:
        if has_overlay_permission(pkg):
            threats.append((pkg, get_app_label(pkg)))

    return threats

def summarize_threats():
    blacklisted = check_blacklisted_packages()
    suspicious = check_suspicious_by_keywords()
    overlays = check_overlay_threats()

    combined = list({(pkg, name) for (pkg, name) in blacklisted + suspicious + overlays})
    return combined
