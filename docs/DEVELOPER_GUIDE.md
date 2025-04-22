# Developer Guide for APIX-V4PY

## Project Structure

The APIX-V4PY project is organized as follows:

```
apix-v4py/
├── assets/                  # Python package assets
│   ├── icons/              # Application icons
│   └── templates/          # Email templates
├── attached_assets/         # Original Python scripts
│   ├── enhanced_email_parser.py  # Enhanced variable parser
│   └── send_email.py       # Email sending functionality
├── build scripts           
│   ├── build_app.py        # Universal build script
│   ├── build_standalone.py # Main build controller
│   ├── build_standalone.sh # Unix build script
│   └── build_standalone.bat # Windows build script
├── test scripts            
│   ├── tests/              # Test directory
│   └── test_python_integration.py # Integration test
├── utility scripts         
│   ├── copy_assets.py      # Asset management
│   └── prepare_distribution.py # Distribution packager
├── application files       
│   ├── __init__.py         # App package initialization
│   ├── mailchats_app.py    # Main application entrypoint
│   └── setup.py            # PyInstaller configuration
├── documentation          
│   ├── README.md           # Main documentation
│   ├── STRUCTURE.md        # Repository structure
│   └── docs/               # Documentation directory
└── data/                   # Runtime data storage
    ├── logs/               # Application logs
    ├── templates/          # User templates
    └── uploads/            # Uploaded files
```

## Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/therealelyayo/apix-v4py.git
   cd apix-v4py
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python mailchats_app.py
   ```

## Building from Source

To build the standalone application from source:

```bash
python standalone_tool.py build
```

This will create a standalone executable in the `dist` directory.

For platform-specific builds:

- Windows: `python standalone_tool.py build --platform windows`
- macOS: `python standalone_tool.py build --platform macos`
- Linux: `python standalone_tool.py build --platform linux`

## Testing

Run the test suite:

```bash
python test_python_integration.py
```

To run specific tests:

```bash
python -m unittest tests.test_basic
```

## Packaging and Distribution

Create a distribution package:

```bash
python prepare_distribution.py
```

This will create a distribution package in the `dist` directory.

## Extending Functionality

### Adding New Variables

To add new personalization variables:

1. Modify `attached_assets/enhanced_email_parser.py`
2. Add the new variable to the `apply_enhanced_mail_merge` method
3. Update the documentation in `get_available_variables`

### Implementing New Features

When implementing new features:

1. Create a new Python module in the appropriate directory
2. Update the main application file (`mailchats_app.py`) to include the new feature
3. Add tests for the new functionality
4. Update documentation

## Code Style and Conventions

This project follows PEP 8 guidelines for Python code.

Key conventions:

- Use 4 spaces for indentation
- Maximum line length of 88 characters
- Use docstrings for all public modules, functions, classes, and methods
- Write tests for all new functionality

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure functionality
5. Submit a pull request

Please ensure your code follows the project's coding standards and includes appropriate tests.