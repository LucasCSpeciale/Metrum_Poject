#!/bin/bash
# Quick script to start the application using Docker

echo "========================================"
echo "Starting LLM Benchmark Tool (Docker)"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "ERROR: Docker is not running"
    echo ""
    echo "Please start Docker Desktop first:"
    echo "  - macOS: open -a Docker"
    echo "  - Or manually open Docker Desktop application"
    echo ""
    exit 1
fi

# Check if API key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "ERROR: OPENROUTER_API_KEY not set"
    echo ""
    echo "Please set your API key:"
    echo "  export OPENROUTER_API_KEY='sk-or-v1-your-key-here'"
    echo ""
    echo "Get your key at: https://openrouter.ai/keys"
    echo ""
    exit 1
fi

echo "Docker is running"
echo "API key is set"
echo ""
echo "Starting containers..."
echo "Dashboard will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

# Start with docker-compose
docker-compose up

