# LLM Benchmarking Tool

Benchmark and compare LLM performance using OpenRouter and NVIDIA GenAI-Perf. Features a web dashboard with interactive visualizations and AI-powered analysis.

## Quick Start with Docker (Recommended)

```bash
# 1. Clone and navigate
git clone https://github.com/LucasCSpeciale/Metrum_Poject.git
cd Metrum_Poject

# 2. Set your OpenRouter API key (get one at https://openrouter.ai/keys)
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

# 3. Start with Docker Compose (requires Docker Desktop installed and running)
docker-compose up

# 4. Open http://localhost:3000 in your browser
```

**Stop the application:** Press Ctrl+C, then run `docker-compose down`

## Alternative: Native Python Setup

If you prefer to run without Docker or want to modify the code:

```bash
# 1. Clone and navigate
git clone https://github.com/LucasCSpeciale/Metrum_Poject.git
cd Metrum_Poject

# 2. Run automated setup
bash setup.sh

# 3. Activate virtual environment (required every time)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Set your API key
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

# 5. Start the dashboard (Docker Desktop must be running)
bash start_web_dashboard.sh

# 6. Open http://localhost:3000
```

**Note:** Docker is required for both methods because GenAI-Perf runs in containers.

## What This Tool Does

Benchmarks LLM models on key performance metrics:
- **Time to First Token (TTFT)** - Response start time
- **Request Latency** - Total response time
- **Throughput** - Tokens generated per second
- **Output Length** - Response size statistics

Currently tests:
- GPT-4o Mini (OpenAI)
- Claude 3 Haiku (Anthropic)
- Llama 3.1 8B (Meta)

## Requirements

- **Docker Desktop** - Required for both installation methods
- **OpenRouter API Key** - Get at https://openrouter.ai/keys (add $5+ credits)
- **Python 3.7+** - Only if using native installation

## Using the Dashboard

1. Click "Run New Benchmark" to test all models (~7-10 minutes)
2. View interactive comparison charts
3. Check detailed metrics for each model
4. Read the AI-generated analysis summary
5. Export results as JSON

## Configuration

### Change Models

Edit `MODELS` in `benchmark.py`:

```python
MODELS = [
    {
        "name": "Display Name",
        "id": "provider/model-id",  # OpenRouter format
        "key": "folder-name"
    }
]
```

Find models at: https://openrouter.ai/models

### Adjust Test Parameters

In `benchmark.py`, modify the GenAI-Perf command:

```python
"--num-dataset-entries", "10",  # Number of test requests
"--synthetic-input-tokens-mean", "50",  # Average prompt length
```

**Note:** More prompts = higher cost and longer runtime.

## Troubleshooting

### "Cannot connect to Docker daemon"
Docker Desktop is not running. Start it and wait 30 seconds.

### "command not found: flask" (Native only)
Virtual environment not activated. Run: `source venv/bin/activate`

### "OPENROUTER_API_KEY not set"
Run: `export OPENROUTER_API_KEY='your-key-here'`

### Port 3000 already in use
Kill the process: `lsof -ti:3000 | xargs kill -9`

### Benchmarks fail
- Check API key is valid at https://openrouter.ai/keys
- Verify you have credits at https://openrouter.ai/credits
- Check logs: `cat results/<model-name>/genai_perf.log`

## Project Structure

```
├── benchmark.py              # Main benchmarking script
├── generate_llm_summary.py   # AI analysis generator
├── web_app.py                # Flask web dashboard
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker Compose config
├── setup.sh                  # Automated setup script
├── templates/                # HTML templates
├── static/                   # CSS, JS assets
└── results/                  # Benchmark data (generated)
```

## How It Works

```
Your Machine (Flask app)
    ↓
Docker Container (GenAI-Perf benchmarking tool)
    ↓
OpenRouter API
    ↓
LLM Models
```

GenAI-Perf runs inside Docker containers to provide consistent, isolated benchmarking regardless of your system configuration.

## License

MIT License - Free for personal and commercial use.

## Support

Open an issue on GitHub with:
- Installation method (Docker or Native)
- Operating system
- Error message
- Output of: `docker --version` and `python3 --version`

---

Built with GenAI-Perf, OpenRouter, Flask, and Docker.
