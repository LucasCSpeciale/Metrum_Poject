#!/usr/bin/env python3
"""
LLM-Generated Summary of Benchmark Results
Uses Claude via OpenRouter to generate a human-readable analysis
"""

import json
import csv
import requests
import os
from pathlib import Path
from datetime import datetime

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
if not OPENROUTER_API_KEY:
    print("ERROR: OPENROUTER_API_KEY environment variable not set!")
    print("Please set it with: export OPENROUTER_API_KEY='your-key-here'")
    exit(1)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
CLAUDE_MODEL = "anthropic/claude-3.5-sonnet"  # Using Claude 3.5 Sonnet for high-quality analysis

def read_csv_metrics(csv_path):
    """Read GenAI-Perf CSV results and extract metrics"""
    metrics = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Metric' in row and 'avg' in row:
                # This is a metric with statistics
                metric_name = row['Metric']
                metrics[metric_name] = {
                    'avg': row.get('avg', 'N/A'),
                    'min': row.get('min', 'N/A'),
                    'max': row.get('max', 'N/A'),
                    'p99': row.get('p99', 'N/A'),
                    'p90': row.get('p90', 'N/A'),
                    'p75': row.get('p75', 'N/A'),
                }
            elif 'Metric' in row and 'Value' in row:
                # This is a single-value metric
                metric_name = row['Metric']
                metrics[metric_name] = row.get('Value', 'N/A')
    
    return metrics

def collect_benchmark_data():
    """Collect all benchmark results from the results directory"""
    results_dir = Path("results")
    
    models = {
        "GPT-4o Mini": "gpt-4o-mini",
        "Claude 3 Haiku": "claude-3-haiku",
        "Llama 3.1 8B": "llama-3.1-8b"
    }
    
    benchmark_data = {}
    
    for model_name, model_key in models.items():
        csv_path = results_dir / model_key / "profile_export_genai_perf.csv"
        if csv_path.exists():
            metrics = read_csv_metrics(csv_path)
            benchmark_data[model_name] = metrics
        else:
            print(f"Warning: Results not found for {model_name}")
    
    return benchmark_data

def format_data_for_llm(benchmark_data):
    """Format benchmark data into a clear structure for the LLM"""
    formatted_text = "# LLM Benchmark Results\n\n"
    formatted_text += f"**Benchmark Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
    formatted_text += "**Tool:** NVIDIA GenAI-Perf via OpenRouter\n"
    formatted_text += "**Test Configuration:** 60-second measurement window, ~50 token inputs\n\n"
    
    for model_name, metrics in benchmark_data.items():
        formatted_text += f"## {model_name}\n\n"
        
        # Format the metrics
        for metric_name, metric_value in metrics.items():
            if isinstance(metric_value, dict):
                formatted_text += f"**{metric_name}:**\n"
                for stat, value in metric_value.items():
                    formatted_text += f"  - {stat}: {value}\n"
            else:
                formatted_text += f"**{metric_name}:** {metric_value}\n"
        
        formatted_text += "\n"
    
    return formatted_text

def call_claude_for_summary(benchmark_data_text):
    """Call Claude via OpenRouter to generate a human-readable summary"""
    
    prompt = f"""You are an expert in LLM performance analysis. I've benchmarked three different LLM models using NVIDIA GenAI-Perf through OpenRouter. Please analyze the following performance data and provide a comprehensive, human-readable summary.

{benchmark_data_text}

Please provide:
1. An executive summary highlighting the key findings
2. A performance comparison ranking the models
3. Specific use-case recommendations for each model
4. Notable insights about latency, throughput, and output characteristics
5. A conclusion with actionable recommendations

Make the summary accessible to both technical and non-technical stakeholders. Use clear language and highlight the most important metrics."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "LLM Benchmark Summary Generator"
    }
    
    payload = {
        "model": CLAUDE_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.3  # Lower temperature for more factual analysis
    }
    
    print(f"Calling Claude ({CLAUDE_MODEL}) to generate summary...")
    print(f"Input size: {len(prompt)} characters")
    
    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content']
            
            # Extract usage info
            usage = result.get('usage', {})
            print(f"Summary generated successfully!")
            print(f"   Input tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"   Output tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"   Total tokens: {usage.get('total_tokens', 'N/A')}")
            
            return summary
        else:
            print(f"Error: API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception while calling Claude: {e}")
        return None

def save_summary(summary, benchmark_data):
    """Save the LLM-generated summary to a file"""
    
    # Save as Markdown
    output_file = Path("LLM_GENERATED_SUMMARY.md")
    
    with open(output_file, 'w') as f:
        f.write("# LLM-Generated Benchmark Summary\n\n")
        f.write(f"**Generated by:** Claude 3.5 Sonnet via OpenRouter\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Models Analyzed:** {', '.join(benchmark_data.keys())}\n\n")
        f.write("---\n\n")
        f.write(summary)
        f.write("\n\n---\n\n")
        f.write("*This summary was automatically generated using Claude 3.5 Sonnet analyzing GenAI-Perf benchmark results.*\n")
    
    print(f"\nSummary saved to: {output_file}")
    
    # Also save raw data as JSON for reference
    data_file = Path("benchmark_data_summary.json")
    with open(data_file, 'w') as f:
        json.dump(benchmark_data, f, indent=2)
    
    print(f"Raw data saved to: {data_file}")

def main():
    """Main execution flow"""
    print("="*60)
    print("LLM-Generated Benchmark Summary")
    print("Using Claude 3.5 Sonnet via OpenRouter")
    print("="*60)
    print()
    
    # Step 1: Collect benchmark data
    print("Step 1: Collecting benchmark results...")
    benchmark_data = collect_benchmark_data()
    
    if not benchmark_data:
        print("No benchmark data found. Please run benchmarks first.")
        return
    
    print(f"Collected data for {len(benchmark_data)} models")
    print()
    
    # Step 2: Format data for LLM
    print("Step 2: Formatting data for Claude...")
    formatted_data = format_data_for_llm(benchmark_data)
    print(f"Data formatted ({len(formatted_data)} characters)")
    print()
    
    # Step 3: Call Claude to generate summary
    print("Step 3: Generating summary with Claude...")
    summary = call_claude_for_summary(formatted_data)
    
    if summary:
        print()
        print("="*60)
        print("GENERATED SUMMARY")
        print("="*60)
        print()
        print(summary)
        print()
        print("="*60)
        
        # Step 4: Save the summary
        print()
        print("Step 4: Saving summary...")
        save_summary(summary, benchmark_data)
        
        print()
        print("Summary generation complete!")
        print(f"Read the full summary: LLM_GENERATED_SUMMARY.md")
    else:
        print("Failed to generate summary")

if __name__ == "__main__":
    main()

