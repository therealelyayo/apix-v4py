# GitHub Codespaces Guide for APIX-V4PY

This document provides detailed information about using GitHub Codespaces for development on the APIX-V4PY project.

## What is GitHub Codespaces?

GitHub Codespaces provides cloud-hosted development environments that are fully configurable and available within seconds. It allows you to develop in a consistent environment without having to set up local development tools.

## Getting Started

### Creating a Codespace

1. Navigate to the [APIX-V4PY repository](https://github.com/therealelyayo/apix-v4py)
2. Click the green "Code" button
3. Select the "Codespaces" tab
4. Click "Create codespace on main"

A new browser window will open with a fully configured VS Code environment.

### Key Features of the APIX-V4PY Codespace

Our Codespace is configured with:

- Python 3.10 runtime
- Node.js for the web frontend
- VS Code extensions for Python development
- Code formatting tools (Black, Flake8)
- Testing tools (PyTest)
- Git configuration
- Pre-installed dependencies

## Development Workflow

### Running the Application

To run the main application:

```bash
python mailchats_app.py
```

### Running Tests

To run unit tests:

```bash
python -m pytest
```

To run the integration test suite:

```bash
python test_python_integration.py
```

### Building the Application

To build the standalone application:

```bash
python standalone_tool.py build
```

### Debugging

The VS Code debugger is pre-configured with several launch configurations:

1. Run Main Application
2. Run Integration Tests
3. Run Standalone Tool
4. Debug Current Python File

Select these from the Run and Debug panel (Ctrl+Shift+D).

## Customizing Your Codespace

### VS Code Settings

VS Code settings are pre-configured, but you can customize them by editing:

- `.vscode/settings.json` - Editor settings
- `.vscode/launch.json` - Debug configurations
- `.vscode/extensions.json` - Recommended extensions

### Environment Customization

If you need to customize your environment beyond the defaults:

1. Edit `.devcontainer/devcontainer.json` to modify the container configuration
2. Edit `.devcontainer/post-create.sh` to modify initialization scripts

## Resources

- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Python in VS Code](https://code.visualstudio.com/docs/languages/python)