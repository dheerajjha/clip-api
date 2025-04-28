#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and install setuptools
echo "Upgrading pip and installing setuptools..."
pip install --upgrade pip setuptools wheel

# Ensure we're using a compatible NumPy version
echo "Ensuring compatible NumPy version..."
pip install "numpy<2.0.0"

# Install dependencies
echo "Installing dependencies..."
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
