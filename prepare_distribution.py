#!/usr/bin/env python3
"""
Distribution preparation script for MailChats Trly APIX2
This script prepares the built application for distribution by
creating a properly structured zip archive.
"""

import os
import sys
import shutil
import platform
import argparse
import datetime
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

VERSION = "2.0.0"

def log(message):
    """Print a message with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_distribution_package(dist_dir, output_dir=None, version=VERSION):
    """Create a distribution package from the built application"""
    if not os.path.exists(dist_dir):
        log(f"Error: Distribution directory not found: {dist_dir}")
        return False
    
    # Determine platform-specific settings
    platform_name = platform.system().lower()
    if platform_name == "darwin":
        platform_name = "macos"
    
    # Create output directory if not specified
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare the distribution name
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dist_name = f"mailchats-trly-apix2-{version}-{platform_name}-{timestamp}"
    
    # Create a temporary directory for distribution preparation
    temp_dir = os.path.join(output_dir, dist_name)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(temp_dir)
    
    log(f"Preparing distribution package: {dist_name}")
    
    # Copy the application files
    if os.path.isdir(os.path.join(dist_dir, "mailchats_app")):
        # onedir mode
        shutil.copytree(
            os.path.join(dist_dir, "mailchats_app"),
            os.path.join(temp_dir, "mailchats_app")
        )
    else:
        # onefile mode
        for file in os.listdir(dist_dir):
            if file.startswith("mailchats_app"):
                shutil.copy2(
                    os.path.join(dist_dir, file),
                    os.path.join(temp_dir, file)
                )
    
    # Copy documentation
    if os.path.exists("STANDALONE_APP.md"):
        shutil.copy2(
            "STANDALONE_APP.md",
            os.path.join(temp_dir, "README.md")
        )
    
    # Create a basic README if not available
    if not os.path.exists(os.path.join(temp_dir, "README.md")):
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write(f"# MailChats Trly APIX2 v{version}\n\n")
            f.write(f"Build Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("## Running the Application\n\n")
            if platform_name == "windows":
                f.write("Double-click on mailchats_app.exe to run the application\n\n")
            else:
                f.write("Run ./mailchats_app to start the application\n\n")
            f.write("## Command Line Options\n\n")
            f.write("- `--port PORT`: Specify the port to run the server on (default: 3000)\n")
            f.write("- `--no-browser`: Don't open the browser automatically\n")
            f.write("- `--api-key KEY`: Set the DeepSeek API key for AI features\n")
    
    # Create additional directories
    os.makedirs(os.path.join(temp_dir, "data", "templates"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "data", "uploads"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "data", "logs"), exist_ok=True)
    
    # Create a zip file
    zip_path = os.path.join(output_dir, f"{dist_name}.zip")
    log(f"Creating zip archive: {zip_path}")
    
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    
    log(f"Distribution package created successfully: {zip_path}")
    return zip_path

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Prepare MailChats Trly APIX2 for distribution")
    parser.add_argument("--dist-dir", help="Directory containing the built application (default: python_app/dist)")
    parser.add_argument("--output-dir", help="Output directory for the distribution package (default: ./dist)")
    parser.add_argument("--version", default=VERSION, help=f"Version number (default: {VERSION})")
    args = parser.parse_args()
    
    # If dist_dir is not specified, use the default
    dist_dir = args.dist_dir
    if dist_dir is None:
        dist_dir = os.path.join("python_app", "dist")
    
    # Check if the application has been built
    if not os.path.exists(dist_dir):
        log("The application has not been built yet. Building now...")
        
        # Determine the build script based on platform
        if platform.system() == "Windows":
            build_cmd = ["build_standalone.bat"]
        else:
            build_cmd = ["./build_standalone.sh"]
        
        # Run the build script
        try:
            subprocess.run(build_cmd, check=True)
        except subprocess.CalledProcessError:
            log("Error: Failed to build the application")
            return 1
        except FileNotFoundError:
            log("Error: Build script not found")
            return 1
    
    # Create the distribution package
    zip_path = create_distribution_package(dist_dir, args.output_dir, args.version)
    
    if zip_path:
        log("\nDistribution preparation completed successfully!")
        log(f"The distribution package is available at: {zip_path}")
        return 0
    else:
        log("Error: Failed to create distribution package")
        return 1

if __name__ == "__main__":
    sys.exit(main())