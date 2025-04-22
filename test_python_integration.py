#!/usr/bin/env python3
"""
Test script for MailChats Trly APIX2 Python Integration
This script verifies that all the Python dependencies and assets are working correctly
"""

import os
import sys
import importlib
import subprocess
import tempfile

# Add parent directory and assets to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
assets_dir = os.path.join(parent_dir, "attached_assets")

sys.path.append(parent_dir)
sys.path.append(assets_dir)

def print_header(text):
    """Print a nicely formatted header"""
    print("\n" + "=" * 60)
    print(" " + text)
    print("=" * 60)

def check_import(module_name):
    """Try to import a module and report results"""
    try:
        module = importlib.import_module(module_name)
        return True, f"✓ Successfully imported {module_name}"
    except ImportError as e:
        return False, f"✗ Failed to import {module_name}: {str(e)}"
    except Exception as e:
        return False, f"✗ Error when importing {module_name}: {str(e)}"

def check_file_exists(filepath, required=True):
    """Check if a file exists and report results"""
    exists = os.path.exists(filepath)
    if exists:
        return True, f"✓ Found file: {filepath}"
    elif required:
        return False, f"✗ Required file not found: {filepath}"
    else:
        return True, f"ℹ Optional file not found: {filepath}"

def test_enhanced_email_parser():
    """Test the EnhancedEmailParser class"""
    print_header("Testing EnhancedEmailParser")
    
    # Check if the file exists
    parser_path = os.path.join(assets_dir, "enhanced_email_parser.py")
    success, message = check_file_exists(parser_path)
    print(message)
    if not success:
        return False
    
    # Try to import the class
    try:
        from enhanced_email_parser import EnhancedEmailParser
        parser = EnhancedEmailParser()
        print("✓ Successfully imported EnhancedEmailParser class")
        
        # Test basic methods
        variables = parser.get_available_variables()
        print(f"✓ get_available_variables() returned {len(variables)} variables")
        
        # Test parse_recipient_line
        recipient = "test@example.com|firstname=John|lastname=Doe"
        parsed = parser.parse_recipient_line(recipient)
        if parsed and 'email' in parsed and 'firstname' in parsed:
            print(f"✓ parse_recipient_line() successfully parsed the recipient")
        else:
            print(f"✗ parse_recipient_line() failed to parse the recipient")
            return False
        
        # Test apply_enhanced_mail_merge
        template = "Hello {{firstname}} {{lastname}} ({{email}})"
        merged = parser.apply_enhanced_mail_merge(template, recipient)
        if "Hello John Doe (test@example.com)" in merged:
            print(f"✓ apply_enhanced_mail_merge() successfully merged the template")
        else:
            print(f"✗ apply_enhanced_mail_merge() failed to merge the template")
            print(f"  Result: {merged}")
            return False
        
        # Generate documentation test
        doc = parser.generate_documentation()
        if doc and len(doc) > 100:  # Just a basic check that it returned something substantial
            print(f"✓ generate_documentation() returned {len(doc)} characters")
        else:
            print(f"✗ generate_documentation() failed")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import EnhancedEmailParser: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error when testing EnhancedEmailParser: {str(e)}")
        return False

def test_send_email():
    """Test the send_email.py module"""
    print_header("Testing send_email.py")
    
    # Check if the file exists
    send_email_path = os.path.join(assets_dir, "send_email.py")
    success, message = check_file_exists(send_email_path)
    print(message)
    if not success:
        return False
    
    # Try to import functions
    try:
        from send_email import apply_mail_merge, read_smtp_credentials
        print("✓ Successfully imported functions from send_email.py")
        
        # Test apply_mail_merge function
        template = "Hello {email} at {domain}!"
        merged = apply_mail_merge(template, "test@example.com", "test", "example.com", "12:00")
        if "Hello test@example.com at example.com!" in merged:
            print(f"✓ apply_mail_merge() successfully merged the template")
        else:
            print(f"✗ apply_mail_merge() failed to merge the template")
            print(f"  Result: {merged}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import from send_email.py: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error when testing send_email.py: {str(e)}")
        return False

def test_command_line_execution():
    """Test command-line execution of the Python scripts"""
    print_header("Testing Command-Line Execution")
    
    # Test send_email.py with --help
    send_email_path = os.path.join(assets_dir, "send_email.py")
    try:
        result = subprocess.run(
            [sys.executable, send_email_path, "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and "usage:" in result.stdout.lower():
            print("✓ send_email.py executed successfully with --help")
        else:
            print(f"✗ send_email.py failed to execute with --help")
            print(f"  Return code: {result.returncode}")
            print(f"  Output: {result.stdout}")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error executing send_email.py: {str(e)}")
        return False
    
    return True

def test_project_structure():
    """Test the overall project structure"""
    print_header("Testing Project Structure")
    
    # Check if the necessary directories exist
    directories = [
        (os.path.join(parent_dir, "attached_assets"), True),
        (os.path.join(parent_dir, "client"), True),
        (os.path.join(parent_dir, "server"), True),
        (os.path.join(parent_dir, "shared"), True),
    ]
    
    all_success = True
    for path, required in directories:
        success, message = check_file_exists(path, required)
        print(message)
        if not success:
            all_success = False
    
    # Check if key files exist
    files = [
        (os.path.join(parent_dir, "package.json"), True),
        (os.path.join(parent_dir, "vite.config.ts"), True),
        (os.path.join(parent_dir, "tsconfig.json"), True),
        (os.path.join(assets_dir, "send_email.py"), True),
        (os.path.join(assets_dir, "enhanced_email_parser.py"), True),
    ]
    
    for path, required in files:
        success, message = check_file_exists(path, required)
        print(message)
        if not success:
            all_success = False
    
    return all_success

def main():
    """Main test function"""
    print("\n🧪 MailChats Trly APIX2 - Python Integration Test 🧪")
    print("This script verifies that all the Python dependencies and assets are working correctly")
    
    test_results = {
        "Project Structure": test_project_structure(),
        "EnhancedEmailParser": test_enhanced_email_parser(),
        "send_email.py": test_send_email(),
        "Command-Line Execution": test_command_line_execution(),
    }
    
    print_header("Test Results Summary")
    all_passed = True
    for test_name, result in test_results.items():
        status = "PASS" if result else "FAIL"
        status_symbol = "✓" if result else "✗"
        print(f"{status_symbol} {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! The Python integration is working correctly.")
        print("   You can proceed with building the standalone application.")
    else:
        print("❌ Some tests failed. Please fix the issues before building the application.")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())