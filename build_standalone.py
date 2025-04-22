#!/usr/bin/env python3
"""
Master build script for MailChats Trly APIX2 Standalone Application
This script coordinates the entire build process for creating a standalone application
"""

import os
import sys
import subprocess
import shutil
import platform
import argparse
from datetime import datetime

# Version information
VERSION = "2.0.0"
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

def print_header():
    """Print a fancy header"""
    print("\n" + "=" * 70)
    print(" MailChats Trly APIX2 - Standalone Application Builder")
    print(f" Version: {VERSION}")
    print(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

def run_command(command, cwd=None, check=True, env=None):
    """Run a command and print output in real-time"""
    print(f"Running: {' '.join(command)}")
    
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        env=env
    )
    
    # Print output in real-time
    output = []
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
        output.append(line)
    
    process.wait()
    
    if check and process.returncode != 0:
        print(f"Command failed with return code {process.returncode}")
        return False, "".join(output)
    
    return True, "".join(output)

def prepare_build_environment():
    """Prepare the build environment"""
    print("Preparing build environment...")
    
    # Create python_app directory if it doesn't exist
    if not os.path.exists("python_app"):
        print("Error: python_app directory not found")
        return False
    
    # Check if key files exist
    required_files = [
        "python_app/mailchats_app.py",
        "python_app/setup.py",
        "python_app/build_app.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Required file not found: {file}")
            return False
    
    # Copy assets from attached_assets to python_app/assets
    print("Copying Python assets...")
    if os.path.exists("copy_assets.py"):
        try:
            subprocess.run([sys.executable, "copy_assets.py"], check=True)
            print("Assets copied successfully")
        except subprocess.CalledProcessError:
            print("Warning: Failed to copy assets automatically")
            
            # Ensure assets are available
            if not os.path.exists("attached_assets"):
                print("Warning: attached_assets directory not found")
            else:
                # Count Python files in attached_assets
                py_files = [f for f in os.listdir("attached_assets") if f.endswith(".py")]
                print(f"Found {len(py_files)} Python files in attached_assets")
    else:
        print("Warning: copy_assets.py not found, skipping automatic asset copying")
    
    return True

def build_standalone_app(platform_target=None, clean=False, test=True):
    """Build the standalone application"""
    print("Building standalone application...")
    
    # Determine the platform if not specified
    if platform_target is None:
        platform_target = platform.system().lower()
    
    print(f"Target platform: {platform_target}")
    
    # Set up the Python app directory
    python_app_dir = os.path.abspath("python_app")
    
    # Install requirements first
    print("Installing requirements...")
    
    if platform_target in ["windows", "win32"]:
        success, _ = run_command(
            [sys.executable, "install.py"],
            cwd=python_app_dir
        )
    else:
        success, _ = run_command(
            [sys.executable, "install.py"],
            cwd=python_app_dir
        )
    
    if not success:
        print("Error: Failed to install requirements")
        return False
    
    # Run tests if requested
    if test:
        print("Running integration tests...")
        success, _ = run_command(
            [sys.executable, "test_python_integration.py"],
            cwd=python_app_dir
        )
        
        if not success:
            print("Warning: Integration tests failed. Proceeding with build anyway.")
    
    # Build the application
    print("Building the application...")
    
    build_cmd = [sys.executable, "build_app.py"]
    if clean:
        build_cmd.append("--clean")
    
    success, _ = run_command(build_cmd, cwd=python_app_dir)
    
    if not success:
        print("Error: Failed to build the application")
        return False
    
    # Check if the build was successful
    dist_dir = os.path.join(python_app_dir, "dist")
    if not os.path.exists(dist_dir):
        print("Error: Build failed, dist directory not found")
        return False
    
    print("Build completed successfully!")
    print(f"Application is located at: {dist_dir}")
    
    return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Build MailChats Trly APIX2 standalone application")
    parser.add_argument("--platform", choices=["windows", "linux", "macos"], help="Target platform (default: current platform)")
    parser.add_argument("--clean", action="store_true", help="Clean previous build files")
    parser.add_argument("--no-test", action="store_true", help="Skip integration tests")
    args = parser.parse_args()
    
    print_header()
    
    if not prepare_build_environment():
        print("Error: Failed to prepare build environment")
        return 1
    
    platform_target = args.platform
    clean = args.clean
    test = not args.no_test
    
    if build_standalone_app(platform_target, clean, test):
        print("\n" + "=" * 70)
        print(" Build process completed successfully!")
        print(" The standalone application is ready for distribution.")
        print("=" * 70 + "\n")
        return 0
    else:
        print("\n" + "=" * 70)
        print(" Build process failed!")
        print(" Please check the error messages above.")
        print("=" * 70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())