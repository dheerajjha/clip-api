#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Fixing NumPy compatibility issue..."

# Remove existing virtual environment
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create a new virtual environment
echo "Creating new virtual environment..."
python -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and install setuptools
echo "Upgrading pip and installing setuptools..."
pip install --upgrade pip setuptools wheel

# Install dependencies with pinned NumPy version
echo "Installing dependencies with NumPy<2.0.0..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
    
    # Start the server
    echo "Starting the server..."
    python -m uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
else
    echo "Error: Failed to install dependencies."
    exit 1
fi
