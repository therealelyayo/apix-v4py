#!/usr/bin/env python3
"""
Installation script for MailChats Trly APIX2
This script sets up the Python environment for building the application
"""

import os
import sys
import subprocess
import platform
import shutil
from datetime import datetime

def print_header():
    """Print a fancy header"""
    print("\n" + "=" * 70)
    print(" MailChats Trly APIX2 - Installation Script")
    print(" Version: 2.0.0")
    print(" Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70 + "\n")

def check_python_version():
    """Check if Python version is supported"""
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python 3.8 or higher is required. You have Python {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"Python version: {version.major}.{version.minor}.{version.micro} ✓")
    return True

def install_pip():
    """Ensure pip is installed and up to date"""
    print("Checking pip installation...")
    
    try:
        # Ensure pip is available and up to date
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Check pip version
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Pip version: {result.stdout.strip()} ✓")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing pip: {e}")
        return False

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("All required packages installed successfully ✓")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing required packages: {e}")
        return False

def copy_assets():
    """Copy attached assets to the assets directory"""
    print("Copying assets...")
    
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Check if there are Python files to copy
    attached_assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "attached_assets")
    if os.path.exists(attached_assets_dir):
        count = 0
        for file in os.listdir(attached_assets_dir):
            if file.endswith(".py"):
                src = os.path.join(attached_assets_dir, file)
                dst = os.path.join("assets", file)
                shutil.copy2(src, dst)
                count += 1
                print(f"  Copied {file}")
        
        if count > 0:
            print(f"Successfully copied {count} asset files ✓")
        else:
            print("No Python asset files found in attached_assets directory")
    else:
        print("Attached assets directory not found")

def verify_installation():
    """Verify that the installation was successful"""
    print("\nVerifying installation...")
    
    # Check for PyInstaller
    try:
        subprocess.run(
            [sys.executable, "-c", "import PyInstaller"],
            check=True
        )
        print("PyInstaller is installed ✓")
    except subprocess.CalledProcessError:
        print("PyInstaller is not installed correctly ✗")
        return False
    
    # Check for assets directory
    if os.path.exists("assets") and os.path.isdir("assets"):
        print("Assets directory exists ✓")
    else:
        print("Assets directory does not exist ✗")
        return False
    
    # Check for build scripts
    if platform.system() == "Windows":
        if os.path.exists("build_windows.bat"):
            print("Windows build script exists ✓")
        else:
            print("Windows build script does not exist ✗")
            return False
    else:
        if os.path.exists("build_unix.sh"):
            print("Unix build script exists ✓")
        else:
            print("Unix build script does not exist ✗")
            return False
    
    return True

def main():
    """Main entry point"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        print("\nError: Installation aborted due to incompatible Python version.")
        return 1
    
    # Install pip
    if not install_pip():
        print("\nError: Installation aborted due to pip installation failure.")
        return 1
    
    # Install requirements
    if not install_requirements():
        print("\nError: Installation aborted due to package installation failure.")
        return 1
    
    # Copy assets
    copy_assets()
    
    # Verify installation
    if not verify_installation():
        print("\nWarning: Some installation checks failed. The build process may not work correctly.")
    
    print("\n" + "=" * 70)
    print(" Installation completed successfully!")
    print(" You can now run the build script:")
    
    if platform.system() == "Windows":
        print("   > python build_app.py")
        print("   or")
        print("   > build_windows.bat")
    else:
        print("   $ python3 build_app.py")
        print("   or")
        print("   $ ./build_unix.sh")
    
    print("=" * 70 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())