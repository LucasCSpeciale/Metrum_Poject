#!/bin/bash
# Start the web dashboard

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    exit 1
fi

# Check if port 3000 is in use and kill it
PORT=3000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "Port $PORT is already in use. Stopping existing process..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null
    echo "Existing process stopped."
    echo ""
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

