@echo off
:: =========================================================
:: MailChats Trly APIX2 - One-Click Environment Setup Script
:: =========================================================
:: This script automates the entire setup process for the
:: MailChats Trly APIX2 development environment on Windows.

setlocal enabledelayedexpansion

:: Parse command line arguments
set USE_VENV=false
set SKIP_TESTS=false

:parse_args
if "%~1"=="" goto :start_setup
if "%~1"=="--venv" (
    set USE_VENV=true
    shift
    goto :parse_args
)
if "%~1"=="--skip-tests" (
    set SKIP_TESTS=true
    shift
    goto :parse_args
)
echo Unknown option: %~1
exit /b 1

:start_setup
:: Print header
echo.
echo =========================================================
echo  MailChats Trly APIX2 - One-Click Environment Setup
echo =========================================================
echo.

:: Check system requirements
echo Checking System Requirements...
echo.

:: Check Python version
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8 or higher.
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo [32m√ Python !PYTHON_VER! found[0m
    
    :: Check if version is at least 3.8
    for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VER!") do (
        set MAJOR=%%a
        set MINOR=%%b
    )
    
    if !MAJOR! LSS 3 (
        echo [31mx Python version must be at least 3.8.0[0m
        exit /b 1
    ) else (
        if !MAJOR! EQU 3 (
            if !MINOR! LSS 8 (
                echo [31mx Python version must be at least 3.8.0[0m
                exit /b 1
            )
        )
    )
)

:: Check pip
pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [33m! pip not found. Attempting to install...[0m
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo [31mx Failed to install pip. Please install pip manually.[0m
        exit /b 1
    )
) else (
    for /f "tokens=2" %%i in ('pip --version') do set PIP_VER=%%i
    echo [32m√ pip !PIP_VER! found[0m
)

:: Check Node.js
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [33m! Node.js not found. Some features may not work.[0m
) else (
    for /f "tokens=1" %%i in ('node --version') do set NODE_VER=%%i
    echo [32m√ Node.js !NODE_VER! found[0m
)

:: Check npm
npm --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [33m! npm not found. Some features may not work.[0m
) else (
    for /f "tokens=1" %%i in ('npm --version') do set NPM_VER=%%i
    echo [32m√ npm !NPM_VER! found[0m
)

echo [32mAll system requirements checked![0m
echo.

:: Install Python dependencies
echo =========================================================
echo  Installing Python Dependencies
echo =========================================================
echo.

:: Create a virtual environment (optional)
if "%USE_VENV%"=="true" (
    echo Creating virtual environment...
    python -m venv venv
    
    :: Activate virtual environment
    call venv\Scripts\activate.bat
    echo [32m√ Virtual environment created and activated[0m
)

:: Install dependencies
echo Installing required Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [31mx Failed to install Python dependencies.[0m
    exit /b 1
)

echo [32m√ Python dependencies installed successfully![0m
echo.

:: Set up development tools
echo =========================================================
echo  Setting Up Development Tools
echo =========================================================
echo.

:: Install development tools
echo Installing development tools...
pip install pytest pytest-cov black flake8
if %errorlevel% neq 0 (
    echo [33m! Some development tools could not be installed.[0m
) else (
    echo [32m√ Development tools installed successfully![0m
)
echo.

:: Configure environment
echo =========================================================
echo  Configuring Environment
echo =========================================================
echo.

:: Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo # MailChats Trly APIX2 Environment Configuration
        echo # Created by setup_environment.bat
        echo.
        echo # App Settings
        echo APP_PORT=3000
        echo DEBUG=true
        echo.
        echo # Email Settings
        echo SMTP_HOST=mail.mailchats.com
        echo SMTP_PORT=587
        echo SMTP_USER=io@mailchats.com
        echo SMTP_PASS=secure_password
        echo.
        echo # AI Integration
        echo DEEPSEEK_API_KEY=
        echo.
        echo # Add your custom settings below
    ) > .env
    echo [32m√ .env file created[0m
    echo [33m! Please edit the .env file to configure your environment[0m
) else (
    echo [32m√ .env file already exists[0m
)
echo.

:: Copy assets
echo =========================================================
echo  Copying Project Assets
echo =========================================================
echo.

echo Running asset copy script...
python copy_assets.py
if %errorlevel% neq 0 (
    echo [31mx Failed to copy assets.[0m
    exit /b 1
)

echo [32m√ Assets copied successfully![0m
echo.

:: Run integration tests
if "%SKIP_TESTS%"=="false" (
    echo =========================================================
    echo  Running Integration Tests
    echo =========================================================
    echo.
    
    echo Running Python integration tests...
    python test_python_integration.py
    if %errorlevel% neq 0 (
        echo [33m! Integration tests failed. The environment may not be fully functional.[0m
    ) else (
        echo [32m√ Integration tests completed successfully![0m
    )
    echo.
)

:: Print success message
echo =========================================================
echo  Setup Complete!
echo =========================================================
echo.

echo [32mThe MailChats Trly APIX2 development environment has been set up successfully![0m
echo.
echo [34mNext steps:[0m
echo 1. Edit the .env file to configure your environment
echo 2. Run the application: python mailchats_app.py
echo 3. Build the standalone application: python standalone_tool.py build
echo.
echo [33mFor more information, see the README.md file[0m
echo.

endlocal