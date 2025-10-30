#!/usr/bin/env python3
"""
LLM Benchmark Web Dashboard
Flask web interface for running benchmarks and viewing results
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import csv
import subprocess
import os
from pathlib import Path
from datetime import datetime
import threading

app = Flask(__name__)

# Global state for benchmark status
benchmark_status = {
    'running': False,
    'current_model': None,
    'progress': 0,
    'logs': []
}

def read_csv_metrics(csv_path):
    """Read GenAI-Perf CSV results"""
    metrics = {}
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Parse first section (metrics with statistics)
            i = 0
            if i < len(rows):
                headers = rows[i]  # ['Metric', 'avg', 'min', 'max', ...]
                i += 1
                
                # Read rows until we hit empty line or next section
                while i < len(rows) and len(rows[i]) > 0 and rows[i][0] != 'Metric':
                    row = rows[i]
                    if len(row) >= 2:
                        metric_name = row[0]
                        # Create dict with all percentile values
                        metrics[metric_name] = {}
                        for j, header in enumerate(headers[1:], start=1):
                            if j < len(row):
                                # Remove quotes and store value
                                value = row[j].strip('"').strip()
                                metrics[metric_name][header] = value if value else 'N/A'
                            else:
                                metrics[metric_name][header] = 'N/A'
                    i += 1
                
                # Skip empty rows
                while i < len(rows) and (len(rows[i]) == 0 or not any(rows[i])):
                    i += 1
                
                # Parse second section (single value metrics)
                if i < len(rows) and rows[i][0] == 'Metric' and len(rows[i]) > 1 and rows[i][1] == 'Value':
                    i += 1
                    while i < len(rows) and len(rows[i]) >= 2:
                        metric_name = rows[i][0]
                        value = rows[i][1].strip('"').strip()
                        metrics[metric_name] = value if value else 'N/A'
                        i += 1
                        
    except Exception as e:
        print(f"Error reading CSV {csv_path}: {e}")
        import traceback
        traceback.print_exc()
    return metrics

def get_benchmark_results():
    """Collect all benchmark results"""
    results_dir = Path("results")
    
    models = {
        "GPT-4o Mini": "gpt-4o-mini",
        "Claude 3 Haiku": "claude-3-haiku",
        "Llama 3.1 8B": "llama-3.1-8b"
    }
    
    results = {}
    
    for model_name, model_key in models.items():
        csv_path = results_dir / model_key / "profile_export_genai_perf.csv"
        json_path = results_dir / model_key / "profile_export_genai_perf.json"
        
        if csv_path.exists():
            metrics = read_csv_metrics(csv_path)
            
            # Try to get TTFT from JSON if available
            if json_path.exists():
                try:
                    with open(json_path, 'r') as f:
                        json_data = json.load(f)
                        # GenAI-Perf JSON structure - TTFT is at root level
                        if 'time_to_first_token' in json_data:
                            ttft_data = json_data['time_to_first_token']
                            metrics['Time to First Token (ms)'] = {
                                'avg': f"{ttft_data.get('avg', 'N/A'):.2f}" if isinstance(ttft_data.get('avg'), (int, float)) else 'N/A',
                                'min': f"{ttft_data.get('min', 'N/A'):.2f}" if isinstance(ttft_data.get('min'), (int, float)) else 'N/A',
                                'max': f"{ttft_data.get('max', 'N/A'):.2f}" if isinstance(ttft_data.get('max'), (int, float)) else 'N/A',
                                'p99': f"{ttft_data.get('p99', 'N/A'):.2f}" if isinstance(ttft_data.get('p99'), (int, float)) else 'N/A',
                                'p95': f"{ttft_data.get('p95', 'N/A'):.2f}" if isinstance(ttft_data.get('p95'), (int, float)) else 'N/A',
                                'p90': f"{ttft_data.get('p90', 'N/A'):.2f}" if isinstance(ttft_data.get('p90'), (int, float)) else 'N/A',
                                'p75': f"{ttft_data.get('p75', 'N/A'):.2f}" if isinstance(ttft_data.get('p75'), (int, float)) else 'N/A',
                                'p50': f"{ttft_data.get('p50', 'N/A'):.2f}" if isinstance(ttft_data.get('p50'), (int, float)) else 'N/A',
                                'p25': f"{ttft_data.get('p25', 'N/A'):.2f}" if isinstance(ttft_data.get('p25'), (int, float)) else 'N/A',
                            }
                except Exception as e:
                    print(f"Error reading JSON for {model_name}: {e}")
            
            results[model_name] = {
                'metrics': metrics,
                'exists': True,
                'key': model_key
            }
        else:
            results[model_name] = {
                'metrics': {},
                'exists': False,
                'key': model_key
            }
    
    return results

def get_ai_summary():
    """Read the AI-generated summary"""
    summary_path = Path("LLM_GENERATED_SUMMARY.md")
    if summary_path.exists():
        with open(summary_path, 'r') as f:
            return f.read()
    return None

def run_benchmark_async():
    """Run benchmark in background thread"""
    global benchmark_status
    
    benchmark_status['running'] = True
    benchmark_status['progress'] = 0
    benchmark_status['logs'] = ['Starting benchmark...']
    
    try:
        # Activate venv and run benchmark
        result = subprocess.run(
            ['bash', '-c', 'source venv/bin/activate && python benchmark.py'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            benchmark_status['logs'].append('Benchmarks completed successfully!')
            benchmark_status['progress'] = 100
        else:
            benchmark_status['logs'].append(f'Benchmark failed: {result.stderr}')
            
    except Exception as e:
        benchmark_status['logs'].append(f'Error: {str(e)}')
    finally:
        benchmark_status['running'] = False
        benchmark_status['current_model'] = None

@app.route('/')
def index():
    """Main dashboard"""
    results = get_benchmark_results()
    has_results = any(r['exists'] for r in results.values())
    
    return render_template('index.html', 
                         results=results, 
                         has_results=has_results,
                         benchmark_status=benchmark_status)

@app.route('/api/chart-data')
def chart_data():
    """API endpoint for chart data"""
    results = get_benchmark_results()
    
    # Prepare throughput data
    throughput_labels = []
    throughput_data = []
    
    # Prepare latency data
    latency_datasets = []
    
    for model_name, data in results.items():
        if data['exists']:
            # Throughput data
            throughput_labels.append(model_name)
            throughput = data['metrics'].get('Output Token Throughput (per sec)', '0')
            try:
                throughput_data.append(float(throughput))
            except (ValueError, TypeError):
                throughput_data.append(0)
            
            # Latency data
            if 'Request Latency (ms)' in data['metrics']:
                latency_metrics = data['metrics']['Request Latency (ms)']
                
                def parse_metric(value):
                    """Parse metric value, removing commas"""
                    if isinstance(value, str):
                        return float(value.replace(',', ''))
                    return float(value) if value else 0
                
                latency_datasets.append({
                    'label': model_name,
                    'data': [
                        parse_metric(latency_metrics.get('min', '0')),
                        parse_metric(latency_metrics.get('p75', '0')),
                        parse_metric(latency_metrics.get('avg', '0')),
                        parse_metric(latency_metrics.get('p90', '0')),
                        parse_metric(latency_metrics.get('p99', '0')),
                        parse_metric(latency_metrics.get('max', '0'))
                    ],
                    'borderWidth': 3,
                    'fill': False,
                    'tension': 0.4
                })
    
    return jsonify({
        'throughput': {
            'labels': throughput_labels,
            'data': throughput_data
        },
        'latency': {
            'labels': ['Min', 'p75', 'Avg', 'p90', 'p99', 'Max'],
            'datasets': latency_datasets
        }
    })

@app.route('/api/results')
def api_results():
    """API endpoint for results data"""
    return jsonify(get_benchmark_results())

@app.route('/api/benchmark/start', methods=['POST'])
def start_benchmark():
    """Start benchmark process"""
    global benchmark_status
    
    if benchmark_status['running']:
        return jsonify({'error': 'Benchmark already running'}), 400
    
    # Start benchmark in background thread
    thread = threading.Thread(target=run_benchmark_async)
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/api/benchmark/status')
def benchmark_status_api():
    """Get current benchmark status"""
    return jsonify(benchmark_status)

@app.route('/summary')
def summary():
    """View AI-generated summary"""
    ai_summary = get_ai_summary()
    return render_template('summary.html', summary=ai_summary)

@app.route('/comparison')
def comparison():
    """Side-by-side comparison view"""
    results = get_benchmark_results()
    return render_template('comparison.html', results=results)

@app.route('/model/<model_key>')
def model_detail(model_key):
    """Detailed view for a specific model"""
    results = get_benchmark_results()
    
    # Find model by key
    model_data = None
    model_name = None
    for name, data in results.items():
        if data['key'] == model_key:
            model_data = data
            model_name = name
            break
    
    if not model_data:
        return "Model not found", 404
    
    return render_template('model_detail.html', 
                         model_name=model_name, 
                         model_data=model_data)

if __name__ == '__main__':
    print("="*60)
    print("LLM Benchmark Web Dashboard")
    print("="*60)
    print("Starting server on http://localhost:3000")
    print("Open your browser and navigate to the URL above")
    print("="*60)
    print()
    
    app.run(host='0.0.0.0', port=3000, debug=True)


