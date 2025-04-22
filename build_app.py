#!/usr/bin/env python3
"""
Universal build script for MailChats Trly APIX2
This script detects the platform and runs the appropriate build script
"""

import os
import sys
import platform
import subprocess
import datetime
import argparse

def print_header():
    """Print a fancy header"""
    print("\n" + "=" * 70)
    print(f" MailChats Trly APIX2 Build System")
    print(f" Version: 2.0.0")
    print(f" Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

def detect_platform():
    """Detect the platform and return the appropriate build script"""
    system = platform.system()
    
    if system == "Windows":
        return "build_windows.bat"
    elif system in ["Linux", "Darwin"]:  # Linux or macOS
        return "build_unix.sh"
    else:
        print(f"Error: Unsupported platform: {system}")
        return None

def check_python_version():
    """Check if Python version is supported"""
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python 3.8 or higher is required. You have Python {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def prepare_build_environment():
    """Prepare the build environment"""
    print("Preparing build environment...")
    
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Copy Python assets if not done already
    if not os.listdir("assets"):
        attached_assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "attached_assets")
        if os.path.exists(attached_assets_dir):
            print(f"Copying assets from {attached_assets_dir}...")
            for file in os.listdir(attached_assets_dir):
                if file.endswith(".py"):
                    src = os.path.join(attached_assets_dir, file)
                    dst = os.path.join("assets", file)
                    print(f"  Copying {file}...")
                    with open(src, "r") as src_file:
                        with open(dst, "w") as dst_file:
                            dst_file.write(src_file.read())
    
    return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Build MailChats Trly APIX2 application")
    parser.add_argument("--skip-deps", action="store_true", help="Skip installing dependencies")
    args = parser.parse_args()
    
    print_header()
    
    if not check_python_version():
        return 1
    
    if not args.skip_deps:
        install_dependencies()
    
    prepare_build_environment()
    
    build_script = detect_platform()
    if not build_script:
        return 1
    
    print(f"Running build script: {build_script}")
    
    # Make Unix build script executable if needed
    if build_script == "build_unix.sh" and not os.access(build_script, os.X_OK):
        os.chmod(build_script, 0o755)
    
    # Run the appropriate build script
    if platform.system() == "Windows":
        result = subprocess.run([build_script], shell=True)
    else:
        result = subprocess.run([f"./{build_script}"], shell=True)
    
    if result.returncode != 0:
        print("Build failed!")
        return 1
    
    print("\nBuild completed successfully!")
    print("Your executable is located in the 'dist' directory.")
    return 0

if __name__ == "__main__":
    sys.exit(main())