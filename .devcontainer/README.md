# Development Container for APIX-V4PY

This directory contains configuration for GitHub Codespaces and VS Code Remote Development Container, enabling you to develop in a consistent environment.

## Features

The development container includes:

- Python 3.10 with development tools
- Node.js 16 for the web frontend
- Git configuration
- Code formatting tools (Black, Flake8)
- Testing tools (PyTest)
- Recommended VS Code extensions

## Getting Started

### Using GitHub Codespaces

To start developing in GitHub Codespaces:

1. Go to https://github.com/therealelyayo/apix-v4py
2. Click the "Code" button
3. Select the "Codespaces" tab
4. Click "Create codespace on main"

### Using VS Code Remote Containers

If you prefer to use VS Code locally:

1. Install the [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
2. Clone the repository: `git clone https://github.com/therealelyayo/apix-v4py.git`
3. Open the repository in VS Code
4. Click the Remote Development icon in the bottom-left corner
5. Select "Reopen in Container"

## Available Commands

Once the container is running, you can use the following commands:

- `python mailchats_app.py` - Run the main application
- `python test_python_integration.py` - Run the integration tests
- `python -m pytest` - Run all unit tests
- `python standalone_tool.py build` - Build a standalone executable

## Customizing the Environment

You can customize the development environment by modifying:

- `devcontainer.json` - Container configuration and VS Code settings
- `requirements.txt` - Python dependencies