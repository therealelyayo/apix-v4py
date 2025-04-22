#!/bin/bash
# Test script for MailChats Trly APIX2 Python Integration
# This script runs the Python integration tests

echo "========================================================"
echo "  MailChats Trly APIX2 Python Integration Tests"
echo "========================================================"

# Run the Python integration test
python3 test_python_integration.py

exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Tests failed with exit code $exit_code"
fi

exit $exit_code