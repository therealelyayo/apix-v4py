# APIX-V4PY Repository Structure

## Overview

This repository contains the Python standalone version of MailChats Trly APIX2, codenamed APIX-V4PY. The application bundles the web-based email management system into a single executable with all dependencies included.

## Directory Structure

```
apix-v4py/
├── assets/                  # Python package assets
│   ├── __init__.py         # Package initialization
│   └── README.md           # Assets documentation
├── attached_assets/        # Original Python scripts
│   ├── enhanced_email_parser.py  # Enhanced variable parser
│   └── send_email.py       # Email sending functionality
├── build scripts:
│   ├── build_app.py        # Universal build script
│   ├── build_standalone.py # Main build controller
│   ├── build_standalone.sh # Unix build script
│   ├── build_standalone.bat # Windows build script
│   ├── build_unix.sh       # Unix-specific build
│   └── build_windows.bat   # Windows-specific build
├── test scripts:
│   ├── test_python_integration.py # Integration test
│   ├── test_python.sh     # Unix test script
│   └── test_python.bat    # Windows test script
├── utility scripts:
│   ├── copy_assets.py     # Asset management
│   ├── prepare_distribution.py # Distribution packager
│   └── standalone_tool.py # All-in-one tool
├── application:
│   ├── __init__.py        # App package initialization
│   ├── mailchats_app.py   # Main application entrypoint
│   ├── setup.py           # PyInstaller configuration
│   └── install.py         # Installation script
├── documentation:
│   ├── README.md          # Main documentation
│   ├── STANDALONE_APP.md  # Standalone app guide
│   └── DISTRIBUTION.md    # Distribution guide
├── requirements.txt       # Python dependencies
└── .gitignore             # Git exclusions
```

## Key Components

1. **Main Application** (`mailchats_app.py`):
   - Entry point for the standalone application
   - Manages the Node.js server lifecycle
   - Handles configuration and command-line arguments

2. **Build System**:
   - `build_app.py`: Cross-platform build script
   - Platform-specific helpers for Windows and Unix
   - PyInstaller configuration in `setup.py`

3. **Asset Management**:
   - `copy_assets.py`: Copies Python assets
   - Email functionality in `attached_assets/`
   - Enhanced personalization in `enhanced_email_parser.py`

4. **Testing**:
   - `test_python_integration.py`: Validates Python integration
   - Platform-specific test runners

5. **Distribution**:
   - `prepare_distribution.py`: Creates distribution packages
   - Handles versioning and platform-specific packaging

6. **All-in-One Tool** (`standalone_tool.py`):
   - Single interface for all operations
   - Supports testing, building, and distribution
   - Command-line interface for all functions

## How to Use

See `README.md` for detailed usage instructions.