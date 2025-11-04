#!/usr/bin/env python3
"""
LLM Benchmarking Tool using OpenRouter and GenAI-Perf
Direct connection to OpenRouter API (no proxy required)
Following Project Outline specifications
"""

import subprocess
import json
import os
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
if not OPENROUTER_API_KEY:
    print("ERROR: OPENROUTER_API_KEY environment variable not set!")
    print("Please set it with: export OPENROUTER_API_KEY='your-key-here'")
    exit(1)

DOCKER_IMAGE = "nvcr.io/nvidia/tritonserver:25.01-py3-sdk"  # Has genai-perf 0.0.10 with -H flag support

##TODO: do not hardcode models, create a CLI tool that allows you to run the benchmark while take the model as an argument
# Models to benchmark - Fast, verified models
MODELS = [
    {
        "name": "GPT-4o Mini", 
        "id": "openai/gpt-4o-mini",
        "key": "gpt-4o-mini"
    },
    {
        "name": "Claude 3 Haiku",
        "id": "anthropic/claude-3-haiku", 
        "key": "claude-3-haiku"
    },
    {
        "name": "Llama 3.1 8B",
        "id": "meta-llama/llama-3.1-8b-instruct",
        "key": "llama-3.1-8b"
    }
]


def run_genai_perf_benchmark(model_info):
    """Run GenAI-Perf benchmark for a single model using Docker - Direct OpenRouter connection"""
    print(f"\n{'='*60}")
    print(f"Benchmarking: {model_info['name']} ({model_info['id']})")
    print(f"{'='*60}\n")
    
    # Create output directory
    output_dir = Path(f"results/{model_info['key']}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine workspace path for Docker-in-Docker
    # If running inside Docker, use HOST_WORKSPACE_PATH (host path for Docker socket)
    # Otherwise use current directory (native execution)
    workspace_path = os.getenv('HOST_WORKSPACE_PATH', os.getcwd())
    print(f"Using workspace path: {workspace_path}")
    
    # Build Docker command for GenAI-Perf
    # Using newer Triton image (25.01) with genai-perf 0.0.10 that has -H flag support
    # Directly connecting to OpenRouter using custom headers 
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{workspace_path}:/workspace",
        "-w", "/workspace",
        DOCKER_IMAGE,
        "genai-perf", "profile",
        "-m", model_info['id'],
        "--service-kind", "openai",  # Using OpenAI-compatible API
        "--endpoint-type", "chat",
        "-u", "https://openrouter.ai/api",  # Direct OpenRouter endpoint
        "-H", f"Authorization:Bearer {OPENROUTER_API_KEY}",  # Custom auth header 
        "-H", "HTTP-Referer:http://localhost:8000",  # Optional: For OpenRouter rankings
        "-H", "X-Title:GenAI-Perf-Benchmark",  # Optional: For OpenRouter rankings
        "--synthetic-input-tokens-mean", "50",  # Generate synthetic prompts
        "--num-dataset-entries", "10",  # Number of test prompts
        "--tokenizer", "gpt2",
        "--measurement-interval", "60000",  # 60 second measurement window (in ms)
        "--artifact-dir", f"/workspace/{output_dir}"
    ]
    
    try:
        # Run GenAI-Perf with simplified output
        print(f"Benchmarking {model_info['name']}...")
        
        # Run with output to log file only (hide verbose GenAI-Perf logs)
        log_path = output_dir / "genai_perf.log"
        with open(log_path, 'w') as log_file:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Filter output - only show important lines, log everything
            for line in process.stdout:
                line = line.rstrip()
                if line:
                    # Write all output to log file
                    log_file.write(line + '\n')
                    log_file.flush()
                    
                    # Skip irrelevant warnings
                    if 'NVIDIA Driver was not detected' in line:
                        continue
                    if 'GPU functionality will not be available' in line:
                        continue
                    if 'Use the NVIDIA Container Toolkit' in line:
                        continue
                    
                    # Only print summary tables and important messages to console
                    if any(keyword in line for keyword in [
                        'NVIDIA GenAI-Perf',
                        'Request Latency',
                        'Throughput',
                        'Generating',
                        'ERROR'
                    ]):
                        print(line)
            
            process.wait(timeout=300)
        
        if process.returncode != 0:
            print(f"\nGenAI-Perf failed for {model_info['name']} with exit code {process.returncode}")
            print(f"Check log file: {log_path}")
            return None
        
        print(f"\nBenchmark completed for {model_info['name']}")
        return output_dir
        
    except subprocess.TimeoutExpired:
        print(f"Benchmark timed out for {model_info['name']}")
        return None
    except Exception as e:
        print(f"Error running benchmark: {e}")
        import traceback
        traceback.print_exc()
        return None


def parse_genai_perf_results(output_dir):
    """Parse GenAI-Perf output files to extract performance metrics"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "output_dir": str(output_dir)
    }
    
    # Try to find and parse profile export JSON
    profile_file = output_dir / "profile_export.json"
    if profile_file.exists():
        with open(profile_file, 'r') as f:
            profile_data = json.load(f)
            results["profile"] = profile_data
    
    # Try to find and parse genai-perf CSV
    csv_files = list(output_dir.glob("*_genai_perf.csv"))
    if csv_files:
        results["csv_file"] = str(csv_files[0])
    
    # Parse log file for metrics
    log_file = output_dir / "genai_perf.log"
    if log_file.exists():
        with open(log_file, 'r') as f:
            log_content = f.read()
            results["log"] = log_content
    
    return results


def generate_summary(all_results):
    """Generate human-readable summary of benchmark results"""
    summary = []
    summary.append("\n" + "="*60)
    summary.append("BENCHMARK SUMMARY")
    summary.append("="*60 + "\n")
    
    for model_key, result in all_results.items():
        summary.append(f"\nModel: {model_key}")
        summary.append("-" * 40)
        
        if result.get("profile"):
            profile = result["profile"]
            summary.append(f"Profile data available: Yes")
            summary.append(f"Timestamp: {result.get('timestamp', 'N/A')}")
        else:
            summary.append("Status: Benchmark did not complete successfully")
        
        summary.append("")
    
    return "\n".join(summary)


def clean_old_results():
    """Clean all old benchmark results before running new benchmarks"""
    results_dir = Path("results")
    
    print("\n" + "="*60)
    print("CLEANING OLD BENCHMARK RESULTS")
    print("="*60)
    
    # Clean results directory contents
    if results_dir.exists():
        items_cleaned = 0
        for item in results_dir.iterdir():
            try:
                if item.is_dir():
                    print(f"  Removing directory: {item.name}")
                    shutil.rmtree(item)
                    items_cleaned += 1
                else:
                    print(f"  Removing file: {item.name}")
                    item.unlink()
                    items_cleaned += 1
            except Exception as e:
                print(f"  Warning: Could not remove {item.name}: {e}")
        
        if items_cleaned == 0:
            print("  No old results to clean")
        else:
            print(f"  Cleaned {items_cleaned} items from results/")
    
    # Clean top-level summary files (handle both files and directories)
    llm_summary = Path("LLM_GENERATED_SUMMARY.md")
    json_summary = Path("benchmark_data_summary.json")
    benchmark_summary = Path("BENCHMARK_SUMMARY.md")
    
    for summary_path in [llm_summary, json_summary, benchmark_summary]:
        if summary_path.exists():
            try:
                if summary_path.is_dir():
                    # Try to clean contents if it's a directory mount
                    for item in summary_path.iterdir():
                        if item.is_file():
                            item.unlink()
                    print(f"  Cleaned contents of: {summary_path.name}")
                else:
                    summary_path.unlink()
                    print(f"  Removed: {summary_path.name}")
            except (OSError, PermissionError) as e:
                # Skip if it's a mounted volume (Docker)
                print(f"  Note: {summary_path.name} is a mounted volume (will be overwritten)")
    
    print("="*60 + "\n")
    
    # Ensure results directory exists
    results_dir.mkdir(exist_ok=True)


def generate_llm_summary():
    """Automatically generate LLM-powered summary after benchmarks complete"""
    print("\n" + "="*60)
    print("Generating LLM-Powered Summary...")
    print("="*60)
    
    try:
        result = subprocess.run(
            ["python", "generate_llm_summary.py"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("LLM summary generated successfully!")
            print("Summary saved to: LLM_GENERATED_SUMMARY.md")
        else:
            print("LLM summary generation had issues:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("LLM summary generation timed out")
    except Exception as e:
        print(f"Error generating LLM summary: {e}")


def main():
    """Main benchmarking workflow"""
    print("="*60)
    print("LLM Benchmarking with OpenRouter and GenAI-Perf")
    print("="*60)
    print("\nThis will take approximately 7-10 minutes to complete...")
    print("="*60)
    
    # Step 1: Clean old results
    clean_old_results()
    
    # Step 2: Create results directory
    Path("results").mkdir(exist_ok=True)
    
    # Run benchmarks for all models
    all_results = {}
    for model in MODELS:
        output_dir = run_genai_perf_benchmark(model)
        if output_dir:
            results = parse_genai_perf_results(output_dir)
            all_results[model['key']] = results
    
    # Save combined results
    with open("results/benchmark_results.json", 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Generate and print summary
    summary = generate_summary(all_results)
    print(summary)
    
    # Save summary
    with open("results/benchmark_summary.txt", 'w') as f:
        f.write(summary)
    
    print(f"\nBenchmarking complete!")
    print(f"Results saved to: ./results/")
    print(f"Summary: ./results/benchmark_summary.txt")
    print(f"Data: ./results/benchmark_results.json")
    
    # Step 3: Automatically generate LLM summary
    generate_llm_summary()
    
    # Step 4: Inform user about web dashboard
    print("\n" + "="*60)
    print("VIEW RESULTS IN WEB DASHBOARD")
    print("="*60)
    print("\nTo view your benchmark results in an interactive dashboard:")
    print("\n  1. Run: bash start_web_dashboard.sh")
    print("     or:  python web_app.py")
    print("\n  2. Open your browser to: http://localhost:3000")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()

