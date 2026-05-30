# 🛡️ Null Point Framework

![Null Point Framework Full Screen](assets/Full_Screen.png)

**Null Point Framework** is an advanced, centralized, and modern security and Open-Source Intelligence (OSINT) engine. Designed for educational purposes, it provides a comprehensive suite of tools for network assessment, intelligence gathering, and system auditing, all within a high-performance, terminal-based interface.

---

## ⚠️ Disclaimer

**This tool is strictly for educational purposes.** Use only on systems you own or have explicit, documented authorization to test. Unauthorized access, scanning, or testing of systems without permission is illegal. The developers are not responsible for any misuse of this software.

---

## 🚀 Features

The framework is organized into specialized categories for maximum efficiency and ease of use:

### 🌐 Network
![Network Category](assets/Network_cat.png)
Comprehensive tools for network assessment, including vulnerability scanning, IP/Port scanning, and traffic analysis.

### 👁️ OSINT
![OSINT Category](assets/OSINT_cat.png)
Powerful intelligence gathering utilities for social media, email, phone numbers, and web-based search queries.

### 🛡️ Security
![Security Category](assets/Security_cat.png)
Core security testing tools for vulnerability scanning (SQLi, XSS), password cracking, and file integrity.

### 🕵️ Stealth & Privacy
![Stealth & Privacy Category](assets/Stealth-&-Privacy_cat.png)
Essential tools for protecting your digital footprint, including IP/DNS leak tests and User-Agent rotation.

### 🛠️ Dev Tools
![Dev Tools Category](assets/Dev-Tools_cat.png)
Handy utilities for developers, like JSON formatting, JWT decoding, and URL encoding/decoding.

### 📊 Sys Monitor
![Sys Monitor Category](assets/Sys-Monitor_cat.png)
Real-time system monitoring for process memory, disk usage, and network interface statistics.

### 🌐 Advanced Intel
![Advanced Intel Category](assets/Advanced-Intel_cat.png)
Deep intelligence gathering with certificate lookups and URL expansion tools.

### 🔍 Forensics
![Forensics Category](assets/Forensics_cat.png)
Digital forensics capabilities for analyzing image metadata, hex files, and PCAP files.

### 📁 File Systems
![File Systems Category](assets/File-Systems_cat.png)
File management and analysis tools, including hash calculators and duplicate finders.

### 🌐 Web Analysis
![Web Analysis Category](assets/Web-Analysis_cat.png)
Tools for inspecting web server configurations, including header checkers and robots.txt viewers.

### 🛡️ System Hardening
![System Hardening Category](assets/System-Hardening.png)
Tools to audit and improve system security, such as port listener and firewall status checks.

### 🔐 Crypto
![Crypto Category](assets/Crypto_cat.png)
A suite of cryptographic utilities for encoding/decoding, key generation, and hash cracking.

### 🛠️ Utils
![Utils Category](assets/Utils_cat.png)
General-purpose utilities like password generators, system information, and file renamers.

### 📝 Text Utilities
![Text Utilities Category](assets/Text-Utilities_cat.png)
Specialized tools for processing text, including summarization and sentiment analysis.

### ⚙️ DevOps
![DevOps Category](assets/DevOps_cat.png)
Tools for cloud and infrastructure management, including S3 scanners and Docker listers.

### 🎮 Games
![Games Category](assets/games_cat.png)
Niche OSINT tools for various gaming platforms like Roblox, Steam, and Valorant.

---

## 📋 Prerequisites

- **Python 3.10** or higher.
- **Windows Operating System** (for `start.bat` functionality).

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Null-Point
   cd Null-Point
   ```

2. **Install Dependencies**
   Run the provided setup script to install all required libraries:
   ```bash
   .\setup.bat
   ```

## 🚀 Usage

Run the main menu application using the provided batch script:

```bash
start.bat
```

The application will launch in your terminal. Use the sidebar to select tool categories and launch specific security or OSINT tools directly in the integrated terminal window.

## 🏗️ Development Standards

All tools have been refactored to modern standards:
* **Unified Theme**: Consistent CLI output using the built-in theme.
* **CLI Robustness**: All tools support CLI arguments via `argparse`, with interactive fallbacks.
* **Error Handling**: Comprehensive exception management for network and I/O operations.
* **TUI Integration**: The menu utilizes the `Textual` framework for a modern, responsive interface.
