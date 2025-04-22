#!/usr/bin/env python3
"""
MailChats Trly APIX2 - Standalone Python Application
This is the main entry point for the compiled Python application.
"""

import os
import sys
import json
import subprocess
import webbrowser
import threading
import time
import signal
import shutil
import argparse
from datetime import datetime
import tempfile
import atexit

# Add local paths to sys.path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "assets"))

try:
    from assets.enhanced_email_parser import EnhancedEmailParser
    from assets.send_email import send_test_email, process_campaign
except ImportError:
    print("Error: Required Python modules not found.")
    print("This application must be run from the compiled executable or proper Python environment.")
    sys.exit(1)

# Version information
VERSION = "2.0.0"
BUILD_DATE = "April 22, 2025"

# Global variables
server_process = None
web_app_url = None
node_port = 3000
data_dir = os.path.join(current_dir, "data")
config_file = os.path.join(data_dir, "config.json")
log_file = os.path.join(data_dir, "mailchats.log")

# Default configuration
DEFAULT_CONFIG = {
    "node_port": 3000,
    "auto_launch_browser": True,
    "default_smtp_mode": "localhost",
    "default_from_name": "MailChats",
    "deepseek_api_key": "",
    "session_secret": "mailchats_secret_" + datetime.now().strftime("%Y%m%d%H%M%S"),
    "first_run": True,
    "last_run": "",
}

# Ensure directories exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(os.path.join(data_dir, "templates"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "uploads"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "logs"), exist_ok=True)

# ASCII Art Banner
BANNER = r"""
  __  __       _ _  _____ _           _         _____     _         _    ____  ___ __   _____ 
 |  \/  | __ _(_) || ____| |__   __ _| |_ ___  |_   _| __| |_  _   / \  |  _ \|_ _\ \ / /_  /
 | |\/| |/ _` | | ||  _| | '_ \ / _` | __/ __|   | || '__| | | | | / _ \ | |_) || | \ V / / / 
 | |  | | (_| | | || |___| | | | (_| | |_\__ \   | || |  | |_| |_/ ___ \|  __/ | |  | | / /_ 
 |_|  |_|\__,_|_|_||_____|_| |_|\__,_|\__|___/   |_||_|   \__, /_/   \_\_|   |___| |_|/____|
                                                          |___/                              
 Version: {0}                                                       Build Date: {1}
""".format(VERSION, BUILD_DATE)

def log(message):
    """Write a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    with open(log_file, "a") as f:
        f.write(log_message)
    
    print(message)

def load_config():
    """Load configuration from file or create with defaults"""
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                # Update with any new default keys
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            log(f"Error loading configuration: {str(e)}")
            return DEFAULT_CONFIG
    else:
        # Save default config
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file"""
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        log(f"Error saving configuration: {str(e)}")

def start_node_server(port, env_vars=None):
    """Start the Node.js server with the specified port"""
    global server_process, web_app_url
    
    if env_vars is None:
        env_vars = {}
    
    # Set up the environment for the Node.js process
    node_env = os.environ.copy()
    node_env.update(env_vars)
    node_env["PORT"] = str(port)
    
    log(f"Starting Node.js server on port {port}...")
    
    try:
        # Detect platform to determine how to open the server
        if os.name == 'nt':  # Windows
            server_process = subprocess.Popen(
                ["npm.cmd", "run", "dev"],
                cwd=os.path.join(current_dir, "app"),
                env=node_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:  # Unix-like
            server_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=os.path.join(current_dir, "app"),
                env=node_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        web_app_url = f"http://localhost:{port}"
        log(f"Server starting at {web_app_url}")
        
        # Start a thread to monitor the server output
        threading.Thread(target=monitor_server_output, daemon=True).start()
        
        # Wait a moment for the server to start
        time.sleep(3)
        
    except Exception as e:
        log(f"Failed to start server: {str(e)}")
        return False
    
    return True

def monitor_server_output():
    """Monitor and log server output"""
    while server_process and server_process.poll() is None:
        try:
            for line in iter(server_process.stdout.readline, b''):
                line_str = line.decode('utf-8', errors='replace').strip()
                if line_str:
                    log(f"[SERVER] {line_str}")
            
            for line in iter(server_process.stderr.readline, b''):
                line_str = line.decode('utf-8', errors='replace').strip()
                if line_str:
                    log(f"[SERVER ERROR] {line_str}")
        except Exception as e:
            log(f"Error monitoring server output: {str(e)}")
            time.sleep(1)
    
    log("Server monitoring thread ended")

def stop_server():
    """Stop the running server"""
    global server_process
    
    if server_process:
        log("Stopping server...")
        try:
            # Try to terminate gracefully first
            if os.name == 'nt':  # Windows
                server_process.terminate()
            else:  # Unix-like
                server_process.send_signal(signal.SIGTERM)
            
            # Wait for up to 5 seconds for the process to terminate
            for _ in range(10):
                if server_process.poll() is not None:
                    break
                time.sleep(0.5)
            
            # If still running, force kill
            if server_process.poll() is None:
                log("Server didn't terminate gracefully, forcing shutdown...")
                server_process.kill()
            
            server_process = None
            return True
        
        except Exception as e:
            log(f"Error stopping server: {str(e)}")
            return False
    
    return True

def open_browser(url):
    """Open the default web browser to the specified URL"""
    try:
        log(f"Opening browser to {url}")
        webbrowser.open(url)
        return True
    except Exception as e:
        log(f"Failed to open browser: {str(e)}")
        return False

def cleanup():
    """Cleanup function to be called on exit"""
    stop_server()
    log("MailChats Trly APIX2 application closed")

def main():
    """Main entry point for the application"""
    # Register cleanup handler
    atexit.register(cleanup)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="MailChats Trly APIX2 Application")
    parser.add_argument("--port", type=int, help="Port to run the server on")
    parser.add_argument("--no-browser", action="store_true", help="Don't open the browser automatically")
    parser.add_argument("--api-key", type=str, help="DeepSeek API key")
    args = parser.parse_args()
    
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print banner
    print(BANNER)
    
    log("Starting MailChats Trly APIX2 application")
    
    # Load configuration
    config = load_config()
    
    # Update configuration based on command line arguments
    if args.port:
        config["node_port"] = args.port
    
    if args.no_browser:
        config["auto_launch_browser"] = False
    
    if args.api_key:
        config["deepseek_api_key"] = args.api_key
    
    # Update last run timestamp
    config["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config["first_run"] = False
    save_config(config)
    
    # Environment variables for the Node.js server
    env_vars = {
        "NODE_ENV": "production",
        "SESSION_SECRET": config["session_secret"]
    }
    
    # Add DeepSeek API key if configured
    if config["deepseek_api_key"]:
        env_vars["DEEPSEEK_API_KEY"] = config["deepseek_api_key"]
    
    # Start the server
    success = start_node_server(config["node_port"], env_vars)
    
    if success and config["auto_launch_browser"]:
        # Wait a moment for the server to fully initialize
        time.sleep(2)
        open_browser(web_app_url)
    
    # Keep the application running until Ctrl+C
    try:
        while server_process and server_process.poll() is None:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        stop_server()

if __name__ == "__main__":
    main()