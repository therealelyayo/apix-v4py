#!/usr/bin/env python3
"""
MailChats Trly APIX2 Standalone Tool
This is a unified tool for managing the standalone application lifecycle
"""

import os
import sys
import argparse
import subprocess
import platform
import datetime
import webbrowser

VERSION = "2.0.0"

def print_header():
    """Print a fancy header"""
    print("\n" + "=" * 70)
    print(" MailChats Trly APIX2 - Standalone Tool")
    print(f" Version: {VERSION}")
    print(f" Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

def run_command(cmd, check=True):
    """Run a command and print output in real-time"""
    print(f"Running: {' '.join(cmd)}")
    
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
    
    if check and process.returncode != 0:
        print(f"Command failed with return code {process.returncode}")
        return False
    
    return True

def is_windows():
    """Check if running on Windows"""
    return platform.system() == "Windows"

def test_python_integration():
    """Run the Python integration test"""
    print("Running Python integration test...")
    
    if is_windows():
        script = ["python", "python_app\\test_python_integration.py"]
    else:
        script = ["python3", "python_app/test_python_integration.py"]
    
    return run_command(script, check=False)

def copy_assets():
    """Copy assets from attached_assets to python_app/assets"""
    print("Copying Python assets...")
    
    if is_windows():
        script = ["python", "copy_assets.py"]
    else:
        script = ["python3", "copy_assets.py"]
    
    return run_command(script, check=False)

def build_application(platform_name=None, clean=False, no_test=False):
    """Build the standalone application"""
    print("Building standalone application...")
    
    if is_windows():
        script = ["build_standalone.bat"]
        if platform_name:
            script.extend(["--platform", platform_name])
        if clean:
            script.append("--clean")
        if no_test:
            script.append("--no-test")
    else:
        script = ["./build_standalone.sh"]
        if platform_name:
            script.extend(["--platform", platform_name])
        if clean:
            script.append("--clean")
        if no_test:
            script.append("--no-test")
    
    return run_command(script, check=False)

def prepare_distribution(version=VERSION):
    """Prepare the distribution package"""
    print("Preparing distribution package...")
    
    if is_windows():
        script = ["python", "prepare_distribution.py", "--version", version]
    else:
        script = ["python3", "prepare_distribution.py", "--version", version]
    
    return run_command(script, check=False)

def open_documentation():
    """Open the documentation files in the default browser"""
    docs = ["STANDALONE_APP.md", "DISTRIBUTION.md"]
    found = 0
    
    for doc in docs:
        if os.path.exists(doc):
            file_url = f"file://{os.path.abspath(doc)}"
            print(f"Opening {doc}...")
            webbrowser.open(file_url)
            found += 1
    
    if found == 0:
        print("Documentation files not found.")
        return False
    
    return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="MailChats Trly APIX2 Standalone Tool")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run Python integration test")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build the standalone application")
    build_parser.add_argument("--platform", choices=["windows", "linux", "macos"], 
                             help="Target platform (default: current platform)")
    build_parser.add_argument("--clean", action="store_true", help="Clean previous build files")
    build_parser.add_argument("--no-test", action="store_true", help="Skip integration tests")
    
    # Distribute command
    dist_parser = subparsers.add_parser("distribute", help="Prepare a distribution package")
    dist_parser.add_argument("--version", default=VERSION, help=f"Version number (default: {VERSION})")
    
    # Assets command
    assets_parser = subparsers.add_parser("assets", help="Copy Python assets")
    
    # Docs command
    docs_parser = subparsers.add_parser("docs", help="Open documentation files")
    
    # All command
    all_parser = subparsers.add_parser("all", help="Run the entire process (test, build, distribute)")
    all_parser.add_argument("--platform", choices=["windows", "linux", "macos"], 
                           help="Target platform (default: current platform)")
    all_parser.add_argument("--clean", action="store_true", help="Clean previous build files")
    all_parser.add_argument("--version", default=VERSION, help=f"Version number (default: {VERSION})")
    
    args = parser.parse_args()
    
    print_header()
    
    if args.command == "test":
        return 0 if test_python_integration() else 1
    elif args.command == "build":
        return 0 if build_application(args.platform, args.clean, args.no_test) else 1
    elif args.command == "distribute":
        return 0 if prepare_distribution(args.version) else 1
    elif args.command == "assets":
        return 0 if copy_assets() else 1
    elif args.command == "docs":
        return 0 if open_documentation() else 1
    elif args.command == "all":
        print("Running the entire process...")
        
        success = copy_assets()
        if not success:
            print("Warning: Asset copying failed, but continuing...")
        
        success = test_python_integration()
        if not success:
            print("Warning: Integration test failed, but continuing...")
        
        success = build_application(args.platform, args.clean, False)
        if not success:
            print("Error: Build failed, stopping process")
            return 1
        
        success = prepare_distribution(args.version)
        if not success:
            print("Error: Distribution preparation failed")
            return 1
        
        print("\nEntire process completed successfully!")
        return 0
    else:
        print("Please specify a command. Use --help for more information.")
        return 1

if __name__ == "__main__":
    sys.exit(main())