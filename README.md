# MailChats Trly APIX2 Standalone Builder

This is a comprehensive build system for creating a standalone, cross-platform distribution of the MailChats Trly APIX2 application. The system bundles all components (Node.js, Python, and dependencies) into a single executable that can be distributed to end users.

## Quick Start

The easiest way to use this system is with the all-in-one tool:

```bash
# On Unix-like systems (Linux, macOS)
./standalone_tool.py all

# On Windows
python standalone_tool.py all
```

This will:
1. Copy Python assets to the correct location
2. Run the Python integration tests
3. Build the standalone application
4. Create a distribution package

## Available Tools

### 1. Asset Management

Copy Python assets from `attached_assets` to `python_app/assets`:

```bash
./standalone_tool.py assets
# or directly
./copy_assets.py
```

### 2. Testing

Run the Python integration tests:

```bash
./standalone_tool.py test
# or directly
./test_python.sh  # On Unix-like systems
test_python.bat   # On Windows
```

For JavaScript testing:

```bash
node test_python_integration.js
```

### 3. Building

Build the standalone application:

```bash
./standalone_tool.py build [--platform windows|linux|macos] [--clean] [--no-test]
# or directly
./build_standalone.sh [--platform windows|linux|macos] [--clean] [--no-test]  # On Unix-like systems
build_standalone.bat [--platform windows|linux|macos] [--clean] [--no-test]   # On Windows
```

Options:
- `--platform`: Target platform (default: current platform)
- `--clean`: Clean previous build files before building
- `--no-test`: Skip integration tests

For more control:

```bash
python3 python_app/build_app.py [--skip-deps]
```

### 4. Distribution

Prepare a distribution package:

```bash
./standalone_tool.py distribute [--version X.Y.Z]
# or directly
python3 prepare_distribution.py [--version X.Y.Z] [--dist-dir DIR] [--output-dir DIR]
```

Options:
- `--version`: Version number (default: 2.0.0)
- `--dist-dir`: Directory containing the built application (default: python_app/dist)
- `--output-dir`: Output directory for the distribution package (default: ./dist)

### 5. Documentation

View the documentation:

```bash
./standalone_tool.py docs
```

This will open the documentation files in your default web browser.

## Detailed Documentation

For detailed information, please refer to:

- `STANDALONE_APP.md`: Comprehensive guide for building and using the standalone application
- `DISTRIBUTION.md`: Guide for distributing the application to end users

## Structure

The build system consists of:

- `python_app/`: Main Python application directory
  - `mailchats_app.py`: Main entry point for the standalone application
  - `setup.py`: PyInstaller configuration script
  - `build_app.py`: Universal build script
  - `build_windows.bat` & `build_unix.sh`: Platform-specific build scripts
  - `test_python_integration.py`: Python integration test script
  - `assets/`: Directory for Python scripts and assets
- Root-level scripts:
  - `standalone_tool.py`: All-in-one tool for the entire process
  - `build_standalone.py`: Python implementation of the build process
  - `build_standalone.sh` & `build_standalone.bat`: Shell scripts for building
  - `test_python.sh` & `test_python.bat`: Scripts for testing Python integration
  - `copy_assets.py`: Script for copying Python assets
  - `prepare_distribution.py`: Script for creating distribution packages

## Requirements

- Python 3.8 or higher
- PyInstaller (`pip install pyinstaller`)
- Node.js and npm

## License

Copyright © 2025 MailChats. All rights reserved.