# LLM Benchmarking Tool

A benchmarking tool for comparing LLM performance using OpenRouter and NVIDIA GenAI-Perf. Features a web dashboard with interactive visualizations and AI-powered analysis.

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/LucasCSpeciale/Metrum_Poject.git
cd Metrum_Poject

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Get OpenRouter API key at https://openrouter.ai/keys

# 5. Set your API key
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

# 6. Make sure Docker Desktop is running

# 7. Start the web dashboard
bash start_web_dashboard.sh

# 8. Open http://localhost:3000 in your browser
```

Use the web interface to run benchmarks and view results.

## What This Tool Does

Benchmarks LLM models on key performance metrics:
- **Time to First Token (TTFT)** - How fast the model starts responding
- **Latency** - Total response time
- **Throughput** - Tokens generated per second
- **Output Length** - Response size statistics

Currently configured to test:
- **GPT-4o Mini** (OpenAI)
- **Claude 3 Haiku** (Anthropic)
- **Llama 3.1 8B** (Meta)

## Requirements

- **Python 3.7+**
- **Docker Desktop** - Must be running
- **OpenRouter API Key** - Get one at https://openrouter.ai/keys

## Installation

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

You'll need to activate the virtual environment every time you open a new terminal:
```bash
source venv/bin/activate
```

### Step 2: Get an OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up or log in
3. Navigate to **Keys** in the sidebar
4. Click **Create Key** and copy it
5. Add credits to your account (at least $5 recommended)

### Step 3: Set Your API Key

**Option A: Temporary (for current terminal session)**
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
```

**Option B: Permanent (survives terminal restarts)**
```bash
# Add to ~/.zshrc (macOS) or ~/.bashrc (Linux)
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**IMPORTANT:** Never commit your actual API key to git!

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI Python client
- `flask` - Web server for dashboard
- `requests` - HTTP client

### Step 5: Verify Docker is Running

```bash
docker --version
```

If Docker is not installed:
```bash
# macOS
brew install --cask docker

# Then open Docker Desktop
```

## Usage

### Option 1: Web Dashboard (Recommended)

The easiest way to use the tool with visual charts and one-click benchmarking:

```bash
./start_web_dashboard.sh
```

Open **http://localhost:3000** in your browser.

**Features:**
- Run benchmarks with one click
- Interactive comparison charts
- Detailed metrics for each model
- AI-generated analysis summary
- Export results as JSON

### Option 2: Command Line

Run benchmarks from the terminal:

```bash
./run_benchmark.sh
```

Or run individual scripts:

```bash
# Run benchmarks
python benchmark.py

# Generate AI summary (optional)
python generate_llm_summary.py
```

## How It Works

```
benchmark.py
    ↓
Docker Container (GenAI-Perf)
    ↓
OpenRouter API
    ↓
LLM Models (GPT-4o Mini, Claude 3 Haiku, Llama 3.1 8B)
```

**GenAI-Perf** is NVIDIA's professional LLM benchmarking tool. It runs inside Docker and:
- Generates synthetic test prompts
- Measures response timing with microsecond precision
- Calculates statistical distributions (percentiles, averages, etc.)
- Exports structured JSON/CSV results

**OpenRouter** provides unified API access to multiple LLM providers using an OpenAI-compatible interface.

## Results

Benchmark results are saved to `results/`:

```
results/
├── gpt-4o-mini/
│   ├── profile_export_genai_perf.json    # Detailed metrics
│   ├── profile_export_genai_perf.csv     # Spreadsheet format
│   ├── genai_perf.log                    # Execution logs
│   └── inputs.json                       # Test prompts used
├── claude-3-haiku/
│   └── ...
├── llama-3.1-8b/
│   └── ...
├── benchmark_results.json                # Combined results
└── benchmark_summary.txt                 # Text summary

BENCHMARK_SUMMARY.md                      # AI-generated analysis
```

### Understanding the Metrics

**Time to First Token (TTFT)**
- Time until the first token appears
- Lower is better (faster perceived response)
- Critical for chat/interactive applications

**Request Latency**
- Total time from request to completion
- Includes all tokens being generated
- Lower is better

**Throughput (tokens/sec)**
- Speed of token generation
- Higher is better
- Important for long-form content

**Request Throughput (requests/sec)**
- Number of complete requests per second
- Higher is better
- Indicates overall efficiency

## Configuration

### Changing Models

Edit the `MODELS` list in `benchmark.py`:

```python
MODELS = [
    {
        "name": "Display Name",
        "id": "provider/model-id",  # OpenRouter format
        "key": "folder-name"         # Results folder name
    }
]
```

Find available models at: https://openrouter.ai/models

### Adjusting Test Parameters

In `benchmark.py`, modify the GenAI-Perf command:

```python
cmd = [
    ...
    "--synthetic-input-tokens-mean", "50",    # Average prompt length
    "--synthetic-input-tokens-stddev", "10",  # Prompt length variation
    "--num-prompts", "10",                     # Number of test requests
    ...
]
```

**Note:** Increasing `--num-prompts` will increase cost and runtime.

## AI-Powered Summary

After running benchmarks, generate an analysis using Claude 3.5 Sonnet:

```bash
python generate_llm_summary.py
```

This creates `BENCHMARK_SUMMARY.md` with:
- Executive summary
- Performance comparison
- Recommendations for each use case
- Statistical analysis

**Cost:** ~$0.01-0.02 per run

## Troubleshooting

### Virtual Environment Issues

**Error:** `command not found: flask` or `ModuleNotFoundError`
```bash
# You forgot to activate the virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Then verify it's activated - you should see (venv) in your prompt
```

**Error:** `venv` folder doesn't exist
```bash
# Create it first
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Starting Fresh:**
```bash
# Delete old venv and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker Issues

**Error:** `Cannot connect to the Docker daemon`
```bash
# Make sure Docker Desktop is running
open -a Docker
```

**Error:** `docker: command not found`
```bash
# Install Docker Desktop
brew install --cask docker
```

### OpenRouter API Issues

**Error:** `Authentication failed`
- Verify your API key in `benchmark.py`
- Ensure it starts with `sk-or-v1-`

**Error:** `Rate limit exceeded (429)`
- Reduce `--num-prompts` in `benchmark.py`
- Add delays between model benchmarks
- Check your OpenRouter account limits

### GenAI-Perf Issues

**Error:** `Model not found`
- Verify model ID at https://openrouter.ai/models
- Check for typos in model name

**Error:** `Benchmark fails with timeout`
- Some models may be slower
- Increase timeout in Docker command (currently 30s per request)

**Check Logs:**
```bash
cat results/<model-name>/genai_perf.log
```

### Web Dashboard Issues

**Port already in use:**
```bash
# Kill existing process on port 3000
lsof -ti:3000 | xargs kill -9

# Or change port in start_web_dashboard.sh
```

## Project Structure

```
Test/
├── benchmark.py                 # Main benchmarking script
├── generate_llm_summary.py      # AI analysis generator
├── web_app.py                   # Flask web dashboard
├── run_benchmark.sh             # CLI benchmark launcher
├── start_web_dashboard.sh       # Dashboard launcher
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── SETUP.md                     # Step-by-step setup guide
├── BENCHMARK_SUMMARY.md         # AI-generated analysis
├── templates/                   # HTML templates
│   ├── index.html              # Main dashboard
│   ├── comparison.html         # Model comparison
│   ├── summary.html            # AI summary view
│   └── model_detail.html       # Individual model details
├── results/                     # Benchmark data
│   └── [model-name]/           # Per-model results
└── venv/                        # Virtual environment (if using)
```

## Technical Details

### Why Docker?

GenAI-Perf is a complex tool with native dependencies (C++ binaries, specific Python versions). Docker provides:
- Pre-configured environment
- Consistent results across systems
- No local installation conflicts
- Easy updates

### Why Synthetic Prompts?

GenAI-Perf generates prompts automatically with controlled characteristics:
- Consistent length distribution
- Proper message formatting
- Reproducible tests
- Statistical validity

For custom prompts, you can provide a JSON file with the `--input-file` flag.

### Architecture Decisions

**Direct OpenRouter Connection**
- No proxy server required (simplified from v1)
- Uses GenAI-Perf's `--service-kind openai` flag
- OpenRouter provides OpenAI-compatible API
- API key passed as environment variable

**Web Dashboard Benefits**
- Visual comparison of models
- One-click benchmark execution
- Real-time progress tracking
- Persistent results storage

## Limitations

- Requires Docker (not available on all systems)
- Synthetic prompts may not match real-world usage
- OpenRouter rate limits apply
- Network latency affects results
- Single-request concurrency (not load testing)

## Future Enhancements

- [ ] Custom prompt support via file upload
- [ ] Multi-concurrency testing
- [ ] Cost estimation per model
- [ ] Historical trend tracking
- [ ] Export results to PDF
- [ ] Webhook notifications on completion

## References

- [GenAI-Perf Documentation](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/genai-perf/README.html)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [NVIDIA Triton Server](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tritonserver)

## License

MIT License - Free for personal and commercial use.

## Contributing

This is a benchmarking tool for LLM performance analysis. Feel free to adapt it for your own use cases.

---

Built with GenAI-Perf, OpenRouter, and Flask.
