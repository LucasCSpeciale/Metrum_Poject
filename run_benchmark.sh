#!/bin/bash
# Run the benchmark suite with the virtual environment
# Direct connection to OpenRouter (no proxy needed)

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
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

# Activate venv and run benchmark
echo "Running benchmarks with direct OpenRouter connection..."
source venv/bin/activate
python benchmark.py

