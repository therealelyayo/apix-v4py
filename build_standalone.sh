#!/bin/bash
# Build script for MailChats Trly APIX2 Standalone Application
# This script coordinates the build process for creating a standalone application

# Default values
PLATFORM=""
CLEAN=false
SKIP_TESTS=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --platform)
            PLATFORM="$2"
            shift 2
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --no-test)
            SKIP_TESTS=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Print header
echo "========================================================"
echo "  MailChats Trly APIX2 Standalone Application Builder"
echo "========================================================"
echo "Platform: ${PLATFORM:-Auto-detect}"
echo "Clean build: $CLEAN"
echo "Skip tests: $SKIP_TESTS"
echo "========================================================"

# Ensure assets are copied
echo "Copying assets..."
python3 copy_assets.py

# Run tests if not skipped
if [ "$SKIP_TESTS" = false ]; then
    echo "Running Python integration tests..."
    python3 test_python_integration.py
    if [ $? -ne 0 ]; then
        echo "Tests failed. Build aborted."
        exit 1
    fi
fi

# Determine build command
BUILD_CMD="python3 build_standalone.py"
if [ -n "$PLATFORM" ]; then
    BUILD_CMD="$BUILD_CMD --platform $PLATFORM"
fi

if [ "$CLEAN" = true ]; then
    BUILD_CMD="$BUILD_CMD --clean"
fi

# Execute build
echo "Starting build process..."
$BUILD_CMD

exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "Build completed successfully!"
else
    echo "Build failed with exit code $exit_code"
fi

exit $exit_code