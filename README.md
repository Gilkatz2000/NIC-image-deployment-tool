# NVMe Image Deployment Tool

A safe, production-inspired Python CLI tool for workstation image deployment and NVMe/SSD disk provisioning.


## 🧠 Overview

This project was created by **Gil Katz** and is based on real-world experience working in an enterprise R&D environment at Intel.

In that role, workstation provisioning involved deploying OS images to NVMe/SSD drives. This process carried significant risk due to manual steps and lack of validation.

This tool redesigns that workflow into a **safe, automated, and reusable system**, introducing validation, safeguards, and structured execution.


## 🎯 What This Project Demonstrates

- Infrastructure automation thinking
- Safe handling of destructive operations
- System-level awareness (disks, storage, capacity)
- CLI tool design and usability
- Production-style engineering practices (testing, linting, CI/CD)


## 🚀 Key Features

### 🔧 Core Functionality
- Detects available disks (macOS + Linux)
- Lists available image files
- Writes images to target disks using `dd`
- Supports both interactive and CLI-based execution


### ⚠️ Safety Mechanisms
- Dry-run mode enabled by default
- System disk protection (prevents overwriting OS disk)
- Image vs disk size validation (capacity check)
- Double confirmation before destructive operations (`YES` + `BURN`)
- Input validation with retry loops


### 🧠 System Awareness
- Disk detection using:
  - `lsblk` (Linux)
  - `diskutil` (macOS)
- Disk size detection and display
- Image size formatting (bytes / KB / MB / GB)


### 🧪 Engineering Practices
- Modular architecture (low coupling)
- CLI interface using `argparse`
- Logging system with verbose mode
- Unit tests with `pytest`
- Code linting with `ruff`
- Code formatting with `black`
- CI/CD pipeline with GitHub Actions


## 📦 Project Structure

NIC-image-deployment-tool/
├── main.py
├── pyproject.toml
├── requirements.txt
├── src/
│   └── nvme_imager/
│       ├── cli.py
│       ├── config.py
│       ├── browser.py
│       ├── disk.py
│       ├── imaging.py
│       ├── size_utils.py
│       └── logger.py
├── tests/
├── docs/
└── .github/workflows/