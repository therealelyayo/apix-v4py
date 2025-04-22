#!/usr/bin/env python3
"""
Setup script for building the MailChats Trly APIX2 executable
This script uses PyInstaller to create a standalone executable
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
from datetime import datetime

# Version information
VERSION = "2.0.0"
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

def log(message):
    """Print a message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import PyInstaller
        log("PyInstaller is installed")
        return True
    except ImportError:
        log("PyInstaller is not installed. Please install it with 'pip install pyinstaller'")
        return False

def build_executable(one_file=False, upx=False, clean=False):
    """Build the executable using PyInstaller"""
    log("Building MailChats Trly APIX2 executable...")
    
    # Determine the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Clean previous build if requested
    if clean and os.path.exists("build"):
        log("Cleaning previous build...")
        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("dist", ignore_errors=True)
        for file in os.listdir(current_dir):
            if file.endswith(".spec"):
                os.remove(file)
    
    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(current_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Copy Python assets from the attached_assets directory
    attached_assets_dir = os.path.join(os.path.dirname(current_dir), "attached_assets")
    if os.path.exists(attached_assets_dir):
        log(f"Copying assets from {attached_assets_dir}...")
        for file in os.listdir(attached_assets_dir):
            if file.endswith(".py"):
                shutil.copy(
                    os.path.join(attached_assets_dir, file),
                    os.path.join(assets_dir, file)
                )
    
    # Base command
    cmd = ["pyinstaller", "--clean"]
    
    # Add options
    if one_file:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    
    # Add UPX if requested and available
    if upx:
        cmd.append("--upx-dir=upx")
    
    # Add icon based on platform
    if platform.system() == "Windows":
        icon_path = os.path.join(current_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            cmd.append(f"--icon={icon_path}")
    elif platform.system() == "Darwin":  # macOS
        icon_path = os.path.join(current_dir, "assets", "icon.icns")
        if os.path.exists(icon_path):
            cmd.append(f"--icon={icon_path}")
    
    # Add data files
    cmd.extend([
        "--add-data", f"assets{os.pathsep}assets",
        "--add-data", f"../app{os.pathsep}app",
    ])
    
    # Add the main script
    cmd.append("mailchats_app.py")
    
    # Run PyInstaller
    log(f"Running command: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Print output in real-time
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
    
    process.wait()
    
    if process.returncode != 0:
        log("Error: PyInstaller failed to build the executable")
        return False
    
    # Copy additional files to the dist directory
    dist_dir = os.path.join(current_dir, "dist")
    if one_file:
        target_dir = dist_dir
    else:
        target_dir = os.path.join(dist_dir, "mailchats_app")
    
    log(f"Copying additional files to {target_dir}...")
    
    # Copy README
    readme_path = os.path.join(current_dir, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write(f"# MailChats Trly APIX2\n\n")
            f.write(f"Version: {VERSION}\n")
            f.write(f"Build Date: {BUILD_DATE}\n\n")
            f.write(f"## Usage\n\n")
            f.write(f"Run the executable to start the application.\n")
            f.write(f"A web browser should open automatically to the application interface.\n\n")
            f.write(f"## Command Line Options\n\n")
            f.write(f"- `--port PORT`: Specify the port to run the server on (default: 3000)\n")
            f.write(f"- `--no-browser`: Don't open the browser automatically\n")
            f.write(f"- `--api-key KEY`: Set the DeepSeek API key\n")
    
    if os.path.exists(readme_path):
        shutil.copy(readme_path, os.path.join(target_dir, "README.md"))
    
    # Create data directories
    os.makedirs(os.path.join(target_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "data", "templates"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "data", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "data", "logs"), exist_ok=True)
    
    log("Build completed successfully!")
    log(f"Executable is located at: {target_dir}")
    
    return True

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="Build MailChats Trly APIX2 executable")
    parser.add_argument("--onefile", action="store_true", help="Create a single executable file")
    parser.add_argument("--upx", action="store_true", help="Use UPX to compress the executable")
    parser.add_argument("--clean", action="store_true", help="Clean previous build files")
    args = parser.parse_args()
    
    if not check_requirements():
        sys.exit(1)
    
    if build_executable(args.onefile, args.upx, args.clean):
        log("Build process completed successfully!")
    else:
        log("Build process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()