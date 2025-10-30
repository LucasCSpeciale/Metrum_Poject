#!/bin/bash
# Start the web dashboard

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    exit 1
fi

echo "==========================================="
echo "Starting LLM Benchmark Web Dashboard"
echo "==========================================="
echo ""
echo "Dashboard will be available at:"
echo "  http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "==========================================="
echo ""

# Activate venv and start web app
source venv/bin/activate
python web_app.py

