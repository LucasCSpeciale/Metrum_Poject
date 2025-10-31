# Setup Guide for New Users

Follow these steps exactly to get the benchmarking tool running.

## Prerequisites

Before starting, make sure you have:
- Python 3.7 or higher installed
- Docker Desktop installed and running
- An OpenRouter account with API key

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/LucasCSpeciale/Metrum_Poject.git
cd Metrum_Poject
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

This creates a folder called `venv` in your project directory. This keeps all dependencies isolated.

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should now see `(venv)` at the beginning of your terminal prompt. This means the virtual environment is active.

**IMPORTANT:** You must activate the virtual environment every time you open a new terminal window!

### 4. Install Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This installs Flask, OpenAI client, and other required packages into your virtual environment.

### 5. Get OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up or log in
3. Click on **Keys** in the sidebar
4. Click **Create Key**
5. Copy the key (starts with `sk-or-v1-`)
6. Add at least $5 in credits to your account

### 6. Set Your API Key

**For the current session:**
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-actual-key-here'
```

Replace `sk-or-v1-your-actual-key-here` with your real key from step 5.

**To make it permanent** (so you don't have to set it every time):

On macOS/Linux:
```bash
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 7. Start Docker Desktop

Make sure Docker Desktop is running:

```bash
docker --version
```

You should see something like: `Docker version 24.0.0, build...`

If not, open Docker Desktop application.

### 8. Run the Web Dashboard

```bash
bash start_web_dashboard.sh
```

### 9. Open Your Browser

Navigate to: http://localhost:3000

You should see the LLM Benchmark Dashboard!

## Running Benchmarks

1. In the web dashboard, click **"Run New Benchmark"**
2. Wait 5-10 minutes while it tests all three models
3. View the results in interactive charts
4. Check out the AI-generated summary

## Common Issues

### "command not found: flask"

You forgot to activate the virtual environment. Run:
```bash
source venv/bin/activate
```

### "OPENROUTER_API_KEY not set"

You need to export your API key:
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
```

### "Cannot connect to Docker daemon"

Docker Desktop is not running. Open the Docker Desktop application.

### All benchmarks fail

Check these in order:
1. Is virtual environment activated? Look for `(venv)` in your prompt
2. Is API key set? Run: `echo $OPENROUTER_API_KEY`
3. Is Docker running? Run: `docker ps`
4. Do you have credits on OpenRouter? Check https://openrouter.ai/credits

### Starting Over

If things are broken, start fresh:

```bash
# 1. Deactivate current venv
deactivate

# 2. Delete old venv
rm -rf venv

# 3. Create new venv
python3 -m venv venv

# 4. Activate it
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Set API key again
export OPENROUTER_API_KEY='your-key-here'

# 7. Run dashboard
bash start_web_dashboard.sh
```

## Need Help?

Open an issue on GitHub with:
- What command you ran
- The error message you got
- Your operating system
- Python version (`python3 --version`)
- Docker version (`docker --version`)

