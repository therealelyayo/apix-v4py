#!/bin/bash
set -e

# Print welcome message
echo "========================================================"
echo "Welcome to APIX-V4PY Development Environment"
echo "========================================================"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install additional development tools
echo "Installing development tools..."
pip install pytest pytest-cov black flake8 isort mypy

# Create necessary directories
echo "Setting up project directories..."
mkdir -p data/logs data/templates data/uploads
mkdir -p dist

# Run tests to verify setup
echo "Verifying installation with quick test..."
python -c "from attached_assets.enhanced_email_parser import EnhancedEmailParser; print('✓ EnhancedEmailParser loaded successfully')"

echo "========================================================"
echo "Setup complete! You can now start developing."
echo ""
echo "Quick start:"
echo "  python mailchats_app.py            # Run the application"
echo "  python test_python_integration.py  # Run integration tests"
echo "  python -m pytest                   # Run unit tests"
echo "========================================================"