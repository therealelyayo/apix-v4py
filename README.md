# APIX-V4PY: MailChats Trly APIX2 Standalone Application

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-proprietary-red)

A standalone Python application for the MailChats Trly APIX2 email management system, providing advanced email template parsing, personalization, and sending capabilities with GitHub Codespaces support for streamlined development.

## 🚀 Quick Start

### ✅ Using GitHub Codespaces (Recommended)

The fastest way to get started:

1. Click the "Code" button at the top of the repository
2. Select the "Codespaces" tab
3. Click "Create codespace on main"

Once the Codespace is ready, you can run:

```bash
python mailchats_app.py
```

### 🖥️ Local Development

```bash
# Clone the repository
git clone https://github.com/therealelyayo/apix-v4py.git
cd apix-v4py

# Install dependencies
pip install -r requirements.txt

# Run the application
python mailchats_app.py
```

## 🔨 Building the Standalone Application

The project includes a comprehensive build system for creating standalone executables for Windows, macOS, and Linux:

```bash
# Build for the current platform
python standalone_tool.py build

# Build for a specific platform (from Linux or macOS)
python standalone_tool.py build --platform windows

# Create distribution package
python standalone_tool.py dist
```

## 📊 Testing

```bash
# Run the integration test suite
python test_python_integration.py

# Run unit tests with pytest
python -m pytest

# Run tests with coverage report
python -m pytest --cov=attached_assets --cov-report=term-missing
```

## 📚 Key Features

- **Enhanced Email Parser**: Process templates with advanced personalization variables
- **Multi-platform Support**: Run on Windows, macOS, and Linux
- **Secure SMTP Integration**: Connect to mail servers with proper authentication
- **Template Analysis**: AI-powered template validation and improvement
- **Standalone Deployment**: No installation required for end-users
- **GitHub Codespaces**: Seamless cloud development environment

## 🧰 Components

- **[enhanced_email_parser.py](attached_assets/enhanced_email_parser.py)**: Core email template parsing engine
- **[send_email.py](attached_assets/send_email.py)**: Email dispatch functionality with SMTP support
- **[mailchats_app.py](mailchats_app.py)**: Main application entry point
- **[standalone_tool.py](standalone_tool.py)**: Build and packaging system

## 👨‍💻 Development

This project uses a modern Python development workflow with:

- **Pytest**: For unit and integration testing
- **Black**: For code formatting
- **Flake8**: For linting
- **GitHub Actions**: For CI/CD pipelines

The VS Code configurations and GitHub Codespaces setups are included for a seamless development experience.

## 🛠️ Available Tools

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

### 4. Distribution

Prepare a distribution package:

```bash
./standalone_tool.py distribute [--version X.Y.Z]
# or directly
python3 prepare_distribution.py [--version X.Y.Z] [--dist-dir DIR] [--output-dir DIR]
```

## 📄 License

Copyright © 2025 MailChats. All rights reserved.
