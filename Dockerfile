# Dockerfile for LLM Benchmarking Tool
# This containerizes the entire application so users don't need to manage Python environments

FROM python:3.11-slim

# Install Docker CLI (needed to run GenAI-Perf containers)
RUN apt-get update && \
    apt-get install -y \
    docker.io \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for web dashboard
EXPOSE 3000

# Default command runs the web dashboard
CMD ["python", "web_app.py"]

