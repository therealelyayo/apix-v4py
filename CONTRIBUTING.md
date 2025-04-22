# Contributing to APIX-V4PY

Thank you for your interest in contributing to APIX-V4PY! This document provides guidelines and instructions for contributing to the project.

## Development Environment

We recommend using GitHub Codespaces for the easiest setup. Alternatively, you can clone the repository and set up your local environment.

### Using GitHub Codespaces

1. Click the "Code" button at the top of the repository
2. Select the "Codespaces" tab
3. Click "Create codespace on main"

The development container will automatically install all dependencies and tools.

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/therealelyayo/apix-v4py.git
   cd apix-v4py
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development tools:
   ```bash
   pip install pytest pytest-cov black flake8 isort mypy
   ```

## Code Style

We follow PEP 8 guidelines with some modifications:

- Line length: 120 characters maximum
- Use Black for formatting
- Use isort for import sorting
- Use descriptive variable names

Run the following commands before submitting your changes:

```bash
# Format code
black .

# Sort imports
isort .

# Check style
flake8 .
```

## Testing

All new code should include appropriate tests:

```bash
# Run unit tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=attached_assets --cov-report=term-missing
```

The integration test suite can be run with:

```bash
python test_python_integration.py
```

## Pull Request Process

1. Create a new branch for your feature or bugfix
2. Make your changes and commit them with clear, descriptive messages
3. Add tests for new functionality
4. Update documentation as needed
5. Submit a pull request to the `main` branch
6. Wait for code review and address any feedback

## Building the Standalone Application

To test your changes in the standalone application:

```bash
# Build for current platform
python standalone_tool.py build

# Test the built application
cd dist/MailChats_Trly_APIX2
./mailchats_app  # or mailchats_app.exe on Windows
```

## Documentation

Please update the relevant documentation for any changes:

- Update inline comments for new or modified functions
- Update README.md for user-facing changes
- Update integration test documentation for new features