@echo off
rem Test script for MailChats Trly APIX2 Python Integration
rem This script runs the Python integration tests

echo ========================================================
echo   MailChats Trly APIX2 Python Integration Tests
echo ========================================================

rem Run the Python integration test
python test_python_integration.py

if errorlevel 1 (
    echo Tests failed with exit code %errorlevel%
    exit /b %errorlevel%
) else (
    echo All tests passed successfully!
    exit /b 0
)