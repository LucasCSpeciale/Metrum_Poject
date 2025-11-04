#!/bin/bash
# Automated setup script for LLM Benchmarking Tool
# This handles all the setup steps automatically

set -e  # Exit on any error

echo "========================================"
echo "LLM Benchmarking Tool - Setup Script"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher first"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Found Python $PYTHON_VERSION"
echo ""

# Step 1: Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi
echo ""

# Step 2: Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "Dependencies installed"
echo ""

# Step 3: Check for API key
echo "Checking for OpenRouter API key..."
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo ""
    echo "=========================================="
    echo "ACTION REQUIRED: Set your API key"
    echo "=========================================="
    echo ""
    echo "You need an OpenRouter API key to use this tool."
    echo ""
    echo "Steps:"
    echo "  1. Go to: https://openrouter.ai/keys"
    echo "  2. Sign up or log in"
    echo "  3. Create a new API key"
    echo "  4. Add at least \$5 in credits"
    echo ""
    echo "Then set your key (choose one option):"
    echo ""
    echo "Option A - Temporary (current session only):"
    echo "  export OPENROUTER_API_KEY='sk-or-v1-your-key-here'"
    echo ""
    echo "Option B - Permanent (add to ~/.zshrc or ~/.bashrc):"
    echo "  echo 'export OPENROUTER_API_KEY=\"sk-or-v1-your-key-here\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
    echo ""
    echo "=========================================="
    echo ""
else
    echo "API key is set"
fi
echo ""

# Step 4: Check Docker
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo ""
    echo "=========================================="
    echo "WARNING: Docker is not installed"
    echo "=========================================="
    echo ""
    echo "This tool requires Docker to run benchmarks."
    echo ""
    echo "Install Docker Desktop:"
    echo "  macOS:   brew install --cask docker"
    echo "  Linux:   https://docs.docker.com/engine/install/"
    echo "  Windows: https://docs.docker.com/desktop/install/windows-install/"
    echo ""
    echo "After installing, make sure Docker Desktop is running."
    echo "=========================================="
    echo ""
else
    DOCKER_VERSION=$(docker --version)
    echo "$DOCKER_VERSION found"
    
    # Check if Docker daemon is running
    if docker ps > /dev/null 2>&1; then
        echo "Docker daemon is running"
    else
        echo ""
        echo "=========================================="
        echo "WARNING: Docker daemon is not running"
        echo "=========================================="
        echo ""
        echo "Please start Docker Desktop before running benchmarks."
        echo "=========================================="
        echo ""
    fi
fi
echo ""

# Step 5: Create results directory
mkdir -p results
echo "Results directory ready"
echo ""

# Final summary
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate virtual environment (in every new terminal):"
echo "   source venv/bin/activate"
echo ""
echo "2. Set your API key (if not already set):"
echo "   export OPENROUTER_API_KEY='sk-or-v1-your-key-here'"
echo ""
echo "3. Make sure Docker Desktop is running"
echo ""
echo "4. Start the web dashboard:"
echo "   bash start_web_dashboard.sh"
echo ""
echo "5. Open browser to: http://localhost:3000"
echo ""
echo "========================================"
echo ""

