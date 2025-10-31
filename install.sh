#!/bin/bash

# StokWELL Installation Script
# This script sets up the StokWELL desktop application

echo "StokWELL Installation Script"
echo "============================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.6 or later."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip for Python 3."
    exit 1
fi

echo "pip3 found: $(pip3 --version)"

# Install requirements
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully!"
else
    echo "Error: Failed to install dependencies."
    exit 1
fi

# Make scripts executable
chmod +x stokwell.py
chmod +x stokwell_cli.py

echo ""
echo "Installation completed successfully!"
echo ""
echo "To run StokWELL:"
echo "  GUI version: python3 stokwell.py"
echo "  CLI version: python3 stokwell.py --cli"
echo ""
echo "To run tests:"
echo "  python3 test_stokwell.py"
echo ""

