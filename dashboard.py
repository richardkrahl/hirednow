#!/usr/bin/env python3
"""
HiredNow Web Dashboard - Professional Bootstrap UI
Production-ready Flask application
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return []

@app.route('/')
def dashboard():
    jobs = load_data('jobs.json')
    profile = load_data('profile.json')
    
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HiredNow - Job Application Automation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
        }
        .hero {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 4rem 0;
        }
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .job-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid var(--primary);
        }
        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border: none;
        }
        .btn-primary:hover {
            opacity: 0.9;
        }
        .feature-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand" href="#"><i class="bi bi-lightning-fill"></i> HiredNow</a>
            <span class="navbar-text text-white">Apply to jobs automatically</span>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
        <div class="container text-center">
            <h1 class="display-4 fw-bold mb-3">Find Jobs Faster</h1>
            <p class="lead mb-4">Auto-search LinkedIn & Indeed. AI-optimize resumes. Track applications.</p>
            <div class="d-flex justify-content-center gap-3">
                <a href="#dashboard" class="btn btn-light btn-lg"><i class="bi bi-search"></i> Find Jobs</a>
                <a href="https://github.com/richardkrahl/hirednow" class="btn btn-outline-light btn-lg"><i class="bi bi-github"></i> View Code</a>
            </div>
            <p class="mt-3 opacity-75"><i class="bi bi-shield-check"></i> 100% Local • No Cloud • $79 One-Time</p>
        </div>
    </section>

    <!-- Stats -->
    <section class="py-5" id="dashboard">
        <div class="container">
            <div class="row g-4 mb-5">
                <div class="col-md-4">
                    <div class="stat-card">
                        <i class="bi bi-briefcase-fill text-primary" style="font-size: 3rem;"></i>
                        <h2 class="mt-3 text-primary">""" + str(len(jobs)) + """</h2>
                        <p class="text-muted">Jobs Found</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stat-card">
                        <i class="bi bi-send-fill text-success" style="font-size: 3rem;"></i>
                        <h2 class="mt-3 text-success">0</h2>
                        <p class="text-muted">Applications</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="stat-card">
                        <i class="bi bi-calendar-check-fill text-warning" style="font-size: 3rem;"></i>
                        <h2 class="mt-3 text-warning">0</h2>
                        <p class="text-muted">Interviews</p>
                    </div>
                </div>
            </div>

            <div class="row">
                <!-- Search Panel -->
                <div class="col-lg-4 mb-4">
                    <div class="card shadow-sm">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0"><i class="bi bi-search"></i> Search Jobs</h5>
                        </div>
                        <div class="card-body">
                            <form id="searchForm">
                                <div class="mb-3">
                                    <label class="form-label">Job Title</label>
                                    <input type="text" id="jobTitle" class="form-control" placeholder="e.g., Product Manager" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Location</label>
                                    <input type="text" id="jobLocation" class="form-control" placeholder="e.g., San Francisco, CA">
                                </div>
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="bi bi-search"></i> Search
                                </button>
                            </form>
                            <div id="searchStatus" class="mt-3"></div>
                        </div>
                    </div>

                    <div class="card shadow-sm mt-4">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0"><i class="bi bi-tools"></i> Actions</h5>
                        </div>
                        <div class="card-body">
                            <a href="https://hirednow.app" target="_blank" class="btn btn-outline-primary w-100 mb-2">
                                <i class="bi bi-globe"></i> Website
                            </a>
                            <a href="https://github.com/richardkrahl/hirednow" target="_blank" class="btn btn-outline-dark w-100">
                                <i class="bi bi-github"></i> GitHub
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Job Listings -->
                <div class="col-lg-8">
                    <div class="card shadow-sm">
                        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="bi bi-list-ul"></i> Job Listings</h5>
                            <span class="badge bg-primary">""" + str(len(jobs)) + """ jobs</span>
                        </div>
                        <div class="card-body">
                            """ + (''.join([f"""
                            <div class="job-card">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div>
                                        <h5 class="mb-1">{job.get('title', 'Unknown')}</h5>
                                        <p class="text-muted mb-1">
                                            <i class="bi bi-building"></i> {job.get('company', 'Unknown')} 
                                            <span class="mx-2">•</span>
                                            <i class="bi bi-geo-alt"></i> {job.get('location', 'Unknown')}
                                        </p>
                                    </div>
                                    <span class="badge bg-info">{job.get('source', 'LinkedIn')}</span>
                                </div>
                                <div class="mt-3">
                                    <a href="{job.get('url', '#')}" target="_blank" class="btn btn-sm btn-outline-primary">
                                        <i class="bi bi-box-arrow-up-right"></i> View Job
                                    </a>
                                </div>
                            </div>
                            """ for job in jobs[:10]]) if jobs else '<p class="text-muted text-center py-5">No jobs found yet. Use the search form to find jobs.</p>') + """
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features -->
            <div class="row mt-5">
                <div class="col-12 text-center mb-4">
                    <h2>How It Works</h2>
                </div>
                <div class="col-md-4 text-center mb-4">
                    <div class="feature-icon mx-auto"><i class="bi bi-search"></i></div>
                    <h5>Find Jobs</h5>
                    <p class="text-muted">Automatically search LinkedIn & Indeed for relevant positions.</p>
                </div>
                <div class="col-md-4 text-center mb-4">
                    <div class="feature-icon mx-auto"><i class="bi bi-magic"></i></div>
                    <h5>Optimize Resume</h5>
                    <p class="text-muted">AI tailors your resume for each job using local Ollama.</p>
                </div>
                <div class="col-md-4 text-center mb-4">
                    <div class="feature-icon mx-auto"><i class="bi bi-send"></i></div>
                    <h5>Auto-Apply</h5>
                    <p class="text-muted">Browser extension auto-fills applications with one click.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-4 mt-5">
        <div class="container">
            <p class="mb-0">HiredNow © 2026 • Built with <i class="bi bi-heart-fill text-danger"></i> in Nashville, TN</p>
            <p class="mb-0 mt-2 small">100% Local • No Cloud • Open Source (MIT)</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('searchForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = e.target.querySelector('button');
            const status = document.getElementById('searchStatus');
            
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Searching...';
            status.innerHTML = '<div class="alert alert-info">Searching LinkedIn & Indeed...</div>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        title: document.getElementById('jobTitle').value,
                        location: document.getElementById('jobLocation').value
                    })
                });
                const result = await response.json();
                status.innerHTML = '<div class="alert alert-success">Found ' + result.count + ' jobs!</div>';
                setTimeout(() => location.reload(), 1500);
            } catch (error) {
                status.innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-search"></i> Search';
            }
        });
    </script>
</body>
</html>
    """
    return html

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    try:
        subprocess.run([
            'python3', 'scraper/job_scraper.py',
            data.get('title', ''),
            data.get('location', '')
        ], cwd=BASE_DIR, timeout=120)
        jobs = load_data('jobs.json')
        return jsonify({'success': True, 'count': len(jobs)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 HiredNow Dashboard")
    print("📍 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
