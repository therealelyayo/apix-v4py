# Installation Guide for APIX-V4PY

## Requirements

- Python 3.8 or higher
- Node.js 16 or higher
- Internet connection for downloading dependencies

## Installation Steps

### Windows

1. Download the latest release from the GitHub repository.
2. Run the installer: `apix-v4py-setup.exe`
3. Follow the on-screen instructions.
4. Once installed, run the application from the Start Menu.

### macOS

1. Download the latest release from the GitHub repository.
2. Mount the DMG file and drag the application to the Applications folder.
3. On first run, you may need to allow the application in System Preferences > Security & Privacy.

### Linux

1. Download the latest release from the GitHub repository.
2. Extract the archive: `tar -xzf apix-v4py-linux.tar.gz`
3. Run the installation script: `./install.sh`
4. Start the application: `./mailchats_app`

## Manual Installation from Source

```bash
# Clone the repository
git clone https://github.com/therealelyayo/apix-v4py.git
cd apix-v4py

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python mailchats_app.py
```

## Troubleshooting

If you encounter any issues during installation, please check the following:

1. Ensure you have the correct Python version installed.
2. Make sure all dependencies are installed correctly.
3. Check the logs in the data/logs directory for error messages.
4. If the problem persists, please open an issue on the GitHub repository.