#!/usr/bin/env python3
"""
Script to copy Python assets from attached_assets to python_app/assets
This ensures all Python scripts are available for testing and building
"""

import os
import shutil
import sys
from datetime import datetime

def log(message):
    """Print a message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    """Main function"""
    # Get directory paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(current_dir, "attached_assets")
    target_dir = os.path.join(current_dir, "python_app", "assets")
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        log(f"Error: Source directory not found: {source_dir}")
        return 1
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Count Python files in source directory
    py_files = [f for f in os.listdir(source_dir) if f.endswith(".py")]
    log(f"Found {len(py_files)} Python files in {source_dir}")
    
    if not py_files:
        log("No Python files to copy")
        return 0
    
    # Copy Python files
    copied = 0
    for file in py_files:
        source_file = os.path.join(source_dir, file)
        target_file = os.path.join(target_dir, file)
        
        try:
            shutil.copy2(source_file, target_file)
            log(f"Copied {file}")
            copied += 1
        except Exception as e:
            log(f"Error copying {file}: {str(e)}")
    
    log(f"Successfully copied {copied} of {len(py_files)} files")
    
    # Create __init__.py if it doesn't exist
    init_file = os.path.join(target_dir, "__init__.py")
    if not os.path.exists(init_file):
        try:
            with open(init_file, "w") as f:
                f.write("# Python package initialization file\n")
                f.write("# This file makes the assets directory a Python package\n")
                f.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("__version__ = '2.0.0'\n")
            log(f"Created {init_file}")
        except Exception as e:
            log(f"Error creating {init_file}: {str(e)}")
    
    log("Asset copying completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())