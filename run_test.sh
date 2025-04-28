#!/bin/bash

# Activate the virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the test script
echo "Running test script..."
python test_clip_api.py

# Provide instructions for manual testing
echo ""
echo "You can also test the API manually using the Swagger UI:"
echo "Open http://localhost:8000/docs in your browser"
