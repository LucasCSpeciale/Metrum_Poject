#!/bin/bash
# Run the benchmark suite with the virtual environment
# Direct connection to OpenRouter (no proxy needed)

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate venv and run benchmark
echo "Running benchmarks with direct OpenRouter connection..."
source venv/bin/activate
python benchmark.py

