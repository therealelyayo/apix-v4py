# One-Click Environment Setup Guide

This guide explains how to quickly set up your development environment for the MailChats Trly APIX2 application using our automated setup scripts.

## Quick Start

### For Unix-based Systems (Linux, macOS)

```bash
# Basic setup
./setup_environment.sh

# Setup with virtual environment
./setup_environment.sh --venv

# Setup without running tests
./setup_environment.sh --skip-tests
```

### For Windows

```batch
# Basic setup
setup_environment.bat

# Setup with virtual environment
setup_environment.bat --venv

# Setup without running tests
setup_environment.bat --skip-tests
```

## What the Setup Scripts Do

The setup scripts automate the following tasks:

1. **Check System Requirements**
   - Verify Python version (3.8+ required)
   - Check for pip, Node.js, and npm
   - Install pip if missing

2. **Install Python Dependencies**
   - Create a virtual environment (optional)
   - Install all required packages from requirements.txt

3. **Set Up Development Tools**
   - Install pytest, pytest-cov, black, and flake8

4. **Configure Environment**
   - Create a .env file with default settings
   - Set up required environment variables

5. **Copy Project Assets**
   - Copy asset files to the correct locations

6. **Run Integration Tests**
   - Verify that everything is working correctly

## Command Line Options

Both scripts support the following command line options:

- `--venv`: Create and use a Python virtual environment
- `--skip-tests`: Skip running the integration tests

## Post-Setup Steps

After running the setup script, you should:

1. Edit the `.env` file to configure your environment settings
2. Run the application: `python mailchats_app.py`
3. Build the standalone application: `./standalone_tool.py build`

## Troubleshooting

If you encounter any issues during setup:

1. **Missing Dependencies**
   - Make sure Python 3.8+ is installed
   - Ensure you have administrative/sudo privileges when needed

2. **Installation Errors**
   - Check your internet connection
   - Try running the script with administrator/sudo privileges

3. **Test Failures**
   - Check the test output for specific errors
   - Verify that all environment variables are set correctly

4. **Other Issues**
   - Check the logs for detailed error messages
   - Consult the README.md and CONTRIBUTING.md files

## Manual Setup

If the automated setup doesn't work for your environment, you can follow these manual steps:

1. Install Python 3.8 or higher
2. Install pip if not included with your Python installation
3. Run `pip install -r requirements.txt`
4. Create a `.env` file with the required configuration
5. Run `python copy_assets.py` to set up the assets
6. Run `python test_python_integration.py` to verify the setup

## Cloud Development with GitHub Codespaces

For the easiest setup experience, use GitHub Codespaces:

1. Open the repository in GitHub
2. Click the "Code" button
3. Select the "Codespaces" tab
4. Click "Create codespace on main"

The Codespace will automatically run the setup script during initialization.

## Next Steps

After setting up your environment, consult these resources:

- **README.md**: Overview of the project
- **CONTRIBUTING.md**: Guidelines for contributing to the project
- **docs/DEVELOPER_GUIDE.md**: Detailed development documentation
- **docs/USER_GUIDE.md**: End-user documentation