@echo off
rem Build script for MailChats Trly APIX2 Standalone Application
rem This script coordinates the build process for creating a standalone application

setlocal enabledelayedexpansion

rem Default values
set PLATFORM=
set CLEAN=false
set SKIP_TESTS=false

rem Parse command line arguments
:parse_args
if "%~1"=="" goto :start_build
if "%~1"=="--platform" (
    set PLATFORM=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--clean" (
    set CLEAN=true
    shift
    goto :parse_args
)
if "%~1"=="--no-test" (
    set SKIP_TESTS=true
    shift
    goto :parse_args
)
echo Unknown option: %~1
exit /b 1

:start_build
rem Print header
echo ========================================================
echo   MailChats Trly APIX2 Standalone Application Builder
echo ========================================================
if defined PLATFORM (
    echo Platform: %PLATFORM%
) else (
    echo Platform: Auto-detect
)
echo Clean build: %CLEAN%
echo Skip tests: %SKIP_TESTS%
echo ========================================================

rem Ensure assets are copied
echo Copying assets...
python copy_assets.py

rem Run tests if not skipped
if "%SKIP_TESTS%"=="false" (
    echo Running Python integration tests...
    python test_python_integration.py
    if errorlevel 1 (
        echo Tests failed. Build aborted.
        exit /b 1
    )
)

rem Determine build command
set BUILD_CMD=python build_standalone.py
if defined PLATFORM (
    set BUILD_CMD=!BUILD_CMD! --platform %PLATFORM%
)

if "%CLEAN%"=="true" (
    set BUILD_CMD=!BUILD_CMD! --clean
)

rem Execute build
echo Starting build process...
%BUILD_CMD%

if errorlevel 1 (
    echo Build failed with exit code %errorlevel%
    exit /b %errorlevel%
) else (
    echo Build completed successfully!
    exit /b 0
)