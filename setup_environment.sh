#!/bin/bash
# =========================================================
# MailChats Trly APIX2 - One-Click Environment Setup Script
# =========================================================
# This script automates the entire setup process for the
# MailChats Trly APIX2 development environment.

set -e  # Exit on any error

# Print colored text
print_color() {
    local color=$1
    local text=$2
    
    case $color in
        "green") echo -e "\033[0;32m$text\033[0m" ;;
        "yellow") echo -e "\033[0;33m$text\033[0m" ;;
        "red") echo -e "\033[0;31m$text\033[0m" ;;
        "blue") echo -e "\033[0;34m$text\033[0m" ;;
        "magenta") echo -e "\033[0;35m$text\033[0m" ;;
        "cyan") echo -e "\033[0;36m$text\033[0m" ;;
        *) echo "$text" ;;
    esac
}

# Print header
print_header() {
    local text=$1
    local padding=$(printf '=%.0s' $(seq 1 ${#text}))
    
    echo
    print_color "cyan" "$padding"
    print_color "cyan" "$text"
    print_color "cyan" "$padding"
    echo
}

# Check system requirements
check_requirements() {
    print_header "Checking System Requirements"
    
    # Check Python version
    if command -v python3 &>/dev/null; then
        python_version=$(python3 --version | cut -d ' ' -f 2)
        print_color "green" "✓ Python $python_version found"
        
        # Check if version is at least 3.8
        required_version="3.8.0"
        if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
            print_color "red" "✗ Python version must be at least 3.8.0"
            exit 1
        fi
    else
        print_color "red" "✗ Python 3 not found. Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &>/dev/null; then
        pip_version=$(pip3 --version | awk '{print $2}')
        print_color "green" "✓ pip $pip_version found"
    else
        print_color "yellow" "! pip not found. Attempting to install..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            python3 -m ensurepip --upgrade
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt-get &>/dev/null; then
                sudo apt-get update
                sudo apt-get install -y python3-pip
            elif command -v dnf &>/dev/null; then
                sudo dnf install -y python3-pip
            elif command -v yum &>/dev/null; then
                sudo yum install -y python3-pip
            else
                print_color "red" "✗ Could not install pip. Please install pip manually."
                exit 1
            fi
        fi
    fi
    
    # Check Node.js
    if command -v node &>/dev/null; then
        node_version=$(node --version)
        print_color "green" "✓ Node.js $node_version found"
    else
        print_color "yellow" "! Node.js not found. Some features may not work."
    fi
    
    # Check npm
    if command -v npm &>/dev/null; then
        npm_version=$(npm --version)
        print_color "green" "✓ npm $npm_version found"
    else
        print_color "yellow" "! npm not found. Some features may not work."
    fi
    
    print_color "green" "All system requirements checked!"
}

# Install Python dependencies
install_python_dependencies() {
    print_header "Installing Python Dependencies"
    
    # Create a virtual environment (optional)
    if [ "$1" == "--venv" ]; then
        print_color "blue" "Creating virtual environment..."
        python3 -m venv venv
        
        # Activate virtual environment
        source venv/bin/activate
        print_color "green" "✓ Virtual environment created and activated"
    fi
    
    # Install dependencies
    print_color "blue" "Installing required Python packages..."
    pip3 install -r requirements.txt
    
    print_color "green" "✓ Python dependencies installed successfully!"
}

# Set up development tools
setup_dev_tools() {
    print_header "Setting Up Development Tools"
    
    # Install development tools
    print_color "blue" "Installing development tools..."
    pip3 install pytest pytest-cov black flake8
    
    print_color "green" "✓ Development tools installed successfully!"
}

# Configure environment
configure_environment() {
    print_header "Configuring Environment"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_color "blue" "Creating .env file..."
        cat > .env << EOL
# MailChats Trly APIX2 Environment Configuration
# Created by setup_environment.sh

# App Settings
APP_PORT=3000
DEBUG=true

# Email Settings
SMTP_HOST=mail.mailchats.com
SMTP_PORT=587
SMTP_USER=io@mailchats.com
SMTP_PASS=secure_password

# AI Integration
DEEPSEEK_API_KEY=

# Add your custom settings below
EOL
        print_color "green" "✓ .env file created"
        print_color "yellow" "! Please edit the .env file to configure your environment"
    else
        print_color "green" "✓ .env file already exists"
    fi
}

# Copy assets
copy_project_assets() {
    print_header "Copying Project Assets"
    
    print_color "blue" "Running asset copy script..."
    python3 copy_assets.py
    
    print_color "green" "✓ Assets copied successfully!"
}

# Run integration tests
run_integration_tests() {
    print_header "Running Integration Tests"
    
    print_color "blue" "Running Python integration tests..."
    python3 test_python_integration.py
    
    print_color "green" "✓ Integration tests completed!"
}

# Print success message
print_success() {
    print_header "Setup Complete!"
    
    print_color "green" "The MailChats Trly APIX2 development environment has been set up successfully!"
    echo
    print_color "blue" "Next steps:"
    echo "1. Edit the .env file to configure your environment"
    echo "2. Run the application: python3 mailchats_app.py"
    echo "3. Build the standalone application: ./standalone_tool.py build"
    echo
    print_color "yellow" "For more information, see the README.md file"
    echo
}

# Main function
main() {
    print_header "MailChats Trly APIX2 - One-Click Environment Setup"
    
    # Parse command line arguments
    use_venv=false
    skip_tests=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --venv)
                use_venv=true
                shift
                ;;
            --skip-tests)
                skip_tests=true
                shift
                ;;
            *)
                print_color "red" "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Run setup steps
    check_requirements
    
    if [ "$use_venv" = true ]; then
        install_python_dependencies "--venv"
    else
        install_python_dependencies
    fi
    
    setup_dev_tools
    configure_environment
    copy_project_assets
    
    if [ "$skip_tests" = false ]; then
        run_integration_tests
    fi
    
    print_success
}

# Run the main function
main "$@"