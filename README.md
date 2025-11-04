# LLM Benchmarking Tool

Benchmark and compare LLM performance using OpenRouter and NVIDIA GenAI-Perf. Features a web dashboard with interactive visualizations and AI-powered analysis.

## Quick Start

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

**Alternative:** Use the convenience script: `bash start_docker.sh` (includes error checking)

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

- **Docker Desktop** - Must be installed and running
- **OpenRouter API Key** - Get at https://openrouter.ai/keys 

## Using the Dashboard

1. Click "Run Benchmarks" to test all models (~7-10 minutes)
2. View interactive comparison charts
3. Check detailed metrics for each model
4. Read the AI-generated analysis summary (generated automatically after benchmarks complete)

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
"--concurrency", "10",  # Number of concurrent requests
```

**Note:** More prompts = higher cost and longer runtime. Higher concurrency increases throughput but may slightly increase latency.

## Troubleshooting

### "Cannot connect to Docker daemon"
Docker Desktop is not running. Start Docker Desktop and wait 30 seconds, then try again.

### "OPENROUTER_API_KEY not set"
Set your API key: `export OPENROUTER_API_KEY='your-key-here'`

Or create a `.env` file in the project root:
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### Port 3000 already in use
Kill the process: `lsof -ti:3000 | xargs kill -9`

Or change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:3000"  # Use port 8080 instead
```

### Benchmarks fail
- Check API key is valid at https://openrouter.ai/keys
- Verify you have credits at https://openrouter.ai/credits
- Check container logs: `docker logs llm-benchmark-tool`
- Check benchmark logs: `docker exec llm-benchmark-tool cat /app/results/<model-name>/genai_perf.log`

### Container keeps restarting
Check if API key is set: `docker logs llm-benchmark-tool --tail 20`

## Project Structure

```
├── benchmark.py              # Main benchmarking script
├── generate_llm_summary.py   # AI analysis generator
├── web_app.py                # Flask web dashboard
├── requirements.txt          # Python dependencies (for Docker)
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker Compose config
├── start_docker.sh           # Convenience script with error checking
├── templates/                # HTML templates
└── results/                  # Benchmark data (generated)
```

## How It Works

```
Docker Container (Flask web app + Python)
    ↓
Docker-in-Docker (GenAI-Perf benchmarking tool)
    ↓
OpenRouter API
    ↓
LLM Models
```

The entire application runs in Docker containers. GenAI-Perf runs inside nested Docker containers to provide consistent, isolated benchmarking regardless of your system configuration.

## License

MIT License - Free for personal and commercial use.

## Support

Open an issue on GitHub with:
- Operating system
- Error message
- Output of: `docker --version`
- Container logs: `docker logs llm-benchmark-tool`

---

Built with GenAI-Perf, OpenRouter, Flask, and Docker.
