#!/bin/bash
# Start the web dashboard

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    exit 1
fi

# Check if API key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "============================================"
    echo "ERROR: OPENROUTER_API_KEY not set!"
    echo "============================================"
    echo ""
    echo "Please set your OpenRouter API key:"
    echo "  export OPENROUTER_API_KEY='sk-or-v1-your-key-here'"
    echo ""
    echo "Get your key at: https://openrouter.ai/keys"
    echo "============================================"
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

