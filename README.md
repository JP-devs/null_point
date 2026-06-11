# 🛡️ Null Point Framework

![Null Point Framework](assets/main.png)

**Null Point Framework** is an advanced, centralized, and modern security and Open-Source Intelligence (OSINT) engine. Designed for educational purposes, it provides a comprehensive suite of tools for network assessment, intelligence gathering, and system auditing, all within a modern graphical interface.

---

## ⚠️ Disclaimer

**This tool is strictly for educational purposes.** Use only on systems you own or have explicit, documented authorization to test. Unauthorized access, scanning, or testing of systems without permission is illegal. The developers are not responsible for any misuse of this software.

---

## 🚀 Features

The framework is organized into specialized categories for maximum efficiency and ease of use. Below is the quick reference guide of all available modules:

| Category | Preview | Description |
| :--- | :---: | :--- |
| **🌐 Network** | ![Network](assets/network.png) | Comprehensive tools for network assessment, including vulnerability scanning, IP/Port scanning, and traffic analysis. |
| **👁️ OSINT** | ![OSINT](assets/OSINT.png) | Powerful intelligence gathering utilities for social media, email, phone numbers, and web-based search queries. |
| **🛡️ Security** | ![Security](assets/security.png) | Core security testing tools for vulnerability scanning (SQLi, XSS), password cracking, and file integrity. |
| **🕵️ Stealth & Privacy** | ![Stealth & Privacy](assets/stealth+privacy.png) | Essential tools for protecting your digital footprint, including IP/DNS leak tests and User-Agent rotation. |
| **🛠️ Dev Tools** | ![Dev Tools](assets/dev.png) | Handy utilities for developers, like JSON formatting, JWT decoding, and URL encoding/decoding. |
| **📊 Sys Monitor** | ![Sys Monitor](assets/sys.png) | Real-time system monitoring for process memory, disk usage, and network interface statistics. |
| **🌐 Advanced Intel** | ![Advanced Intel](assets/advanced_intel.png) | Deep intelligence gathering with certificate lookups and URL expansion tools. |
| **🔍 Forensics** | ![Forensics](assets/forensics.png) | Digital forensics capabilities for analyzing image metadata, hex files, and PCAP files. |
| **📁 File Systems** | ![File Systems](assets/file_systems.png) | File management and analysis tools, including hash calculators and duplicate finders. |
| **🌐 Web Analysis** | ![Web Analysis](assets/web_analysis.png) | Tools for inspecting web server configurations, including header checkers and robots.txt viewers. |
| **🛡️ System Hardening** | ![System Hardening](assets/systemm_hardening.png) | Tools to audit and improve system security, such as port listener and firewall status checks. |
| **🔐 Crypto** | ![Crypto](assets/crypto.png) | A suite of cryptographic utilities for encoding/decoding, key generation, and hash cracking. |
| **🛠️ Utils** | ![Utils](assets/utils.png) | General-purpose utilities like password generators, system information, and file renamers. |
| **📝 Text Utilities** | ![Text Utilities](assets/text_utils.png) | Specialized tools for processing text, including summarization and sentiment analysis. |
| **⚙️ DevOps** | ![DevOps](assets/devops.png) | Tools for cloud and infrastructure management, including S3 scanners and Docker listers. |
| **🎮 Games** | ![Games](assets/games.png) | Niche OSINT tools for various gaming platforms like Roblox, Steam, and Valorant. |

---

## 📋 Prerequisites

- **Python 3.10** or higher.

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/qlarped/null_point.git
   cd null_point
   ```

2. **Install Dependencies**
   Install the required libraries via pip:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Launch the framework using the GUI for a modern, window-based experience with a dynamic tool launcher:

```bash
python null_point_gui.py
```

The application allows you to select tool categories and launch specific security or OSINT tools. It supports **Tool Chaining**, allowing you to pass the output of one tool as the input to another using the `/chain` command in the search bar.

## 🏗️ Development Standards

All tools have been refactored to modern standards:
* **Unified Theme**: Consistent CLI output using the built-in theme.
* **CLI Robustness**: All tools support CLI arguments via `argparse`, with interactive fallbacks.
* **Error Handling**: Comprehensive exception management for network and I/O operations.
* **Tool Chaining**: Native support for chaining tools, enabling seamless data flow between modules.
* **Automated Testing**: A comprehensive test suite is located in `tests/`, ensuring core functionality and stability.

## 🐳 Containerization & CI/CD

* **Docker Support**: A `Dockerfile` is provided for easy deployment in containerized environments.
* **Continuous Integration**: GitHub Actions are configured to automatically run tests on every push and pull request.

## 🗺️ Future Roadmap

* **Enhanced GUI**: Integrating more complex interactive widgets and real-time data visualizations into the window-based interface.
* **Expanded Toolset**: Continuous addition of new security and OSINT modules.
* **Plugin System**: Developing a modular plugin architecture to allow users to easily add their own custom tools.
