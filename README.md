# ⚡ MATRIX_CORE: Advanced macOS System Monitor

A professional, Matrix-themed terminal system monitor specifically optimized for **Apple Silicon (M1/M2/M3)** and Intel Macs. Built with Python and the Rich library to provide a high-performance, cyberpunk-aesthetic monitoring experience.

## 🚀 Key Features

- **M-Chip Optimized Architecture:** Provides highly accurate RAM and CPU temperature readings by directly interfacing with macOS `vm_stat` and `powermetrics`.
- **Live I/O Stream:** Real-time monitoring of Network (RX/TX) and Disk (Read/Write) speeds.
- **Latency Radar:** Integrated ping monitoring to track connection stability and response times (ms).
- **Dual Operating Protocols:** Support for multiple themes including `Matrix (Green)` and `Amethyst (Purple)`.
- **Intelligent Process Tracking:** Live view of top system processes sorted by resource consumption.
- **Media Integration:** Real-time track information from Spotify and Apple Music.

## 🛠 Installation

To set up **MATRIX_CORE** as a global terminal command, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/furkyyo/matrix-core.git](https://github.com/furkyyo/matrix-core.git)
   cd matrix-core
Run the automated installer:
The installer will handle dependencies, compile the binary for your specific architecture, and set up the global command.

Bash
chmod +x install.sh
./install.sh

# ⌨️ Usage
Once installed, you can launch the system from any directory in your terminal:

matrix - Launches the System Bootloader (Interactive Menu)

matrix green - Direct boot into the Matrix Protocol (Classic Green)

matrix purple - Direct boot into the Amethyst Protocol (Levo's Purple)

# 🛡 Requirements
Operating System: macOS (Intel or Apple Silicon)

Environment: python3 installed

Dependencies: psutil, rich, pyinstaller (Automatically handled by install.sh)

Optional: osx-cpu-temp (Required for temperature monitoring on Intel-based Macs)

# 💡 Developer's Note
This project was developed as a personal passion project to explore macOS system architectures, Apple Silicon memory management, and terminal-based UI design. It represents a journey of refactoring "spaghetti code" into a modular, professional software architecture. Feedback, issues, and pull requests are always welcome!

Developed by Furkan Ozkan