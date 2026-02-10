# 👁️ Hidden Eye (v1.0.0)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**Hidden Eye** is a comprehensive Windows system monitoring framework designed for authorized security auditing and research. It implements advanced persistence mechanisms and multi-threaded data exfiltration via Discord Webhooks.

---

## 🛑 Legal Disclaimer
> [!IMPORTANT]
> This software is provided for **educational purposes only**. The author assumes no liability for damages or illicit use. Unauthorized access to computer systems is a federal crime. Always obtain written consent before testing on any device.

---

## ✨ Features

### 🛠️ Persistence & Stealth
- **Auto-Escalation**: Automatically prompts for Administrator privileges on launch.
- **Hidden Deployment**: Self-replicates into a hidden folder in `%APPDATA%`.
- **Startup Persistence**: Configures a Windows Scheduled Task (`schtasks`) to run automatically upon user logon with highest privileges.

### 📊 Monitoring Capabilities
- **Synchronized Keylogger**: Captures all keystrokes, formatting special keys (Enter, Space, etc.) for readability.
- **Ambient Audio Capture**: Periodic recordings of the default system microphone saved in `.wav` format.
- **Visual Intelligence**: Automated high-frequency screenshots of the primary workstation.

### 📡 Exfiltration & Reliability
- **Webhook Integration**: Separate channels for Logs, Audio, and Screenshots.
- **Connection Awareness**: Intelligent heartbeat system that pauses data transmission during internet outages to avoid script errors.

---

## 🏗️ System Architecture

Hidden Eye operates using a parallel execution model to ensure zero data loss.

| Module | Python Engine | Target |
| :--- | :--- | :--- |
| **Input Capture** | `pynput.keyboard` | Global Key Buffer |
| **Audio Processing** | `sounddevice` / `scipy` | Default Input Device |
| **Visual Capture** | `pyautogui` | Primary Monitor |
| **Persistence** | `subprocess` / `ctypes` | Windows Task Scheduler |

---

## 🚀 Setup & Installation

### 1. Prerequisites
- **Python 3.8 or higher**
- **Windows 10/11**
- **PortAudio** (Required for audio recording)

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/yourusername/hidden-eye.git](https://github.com/yourusername/hidden-eye.git)
cd hidden-eye

# Install required dependencies
pip install pyautogui pynput requests sounddevice scipy python-dotenv
