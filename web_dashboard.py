
#!/usr/bin/env python3
"""
HiredNow Bootstrap Web Dashboard
Simple Flask app with Bootstrap UI
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/projects/job-hunter/data")
JOBS_FILE = f"{DATA_DIR}/jobs.json"
PROFILE_FILE = f"{DATA_DIR}/profile.json"

def load_jobs():
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE) as f:
            return json.load(f)
    return []

def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE) as f:
            return json.load(f)
    return {}

@app.route('/')
def dashboard():
    jobs = load_jobs()
    profile = load_profile()
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HiredNow Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; }}
        .stat-card {{ background: white; border-radius: 10px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .job-card {{ background: white; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .btn-primary {{ background-color: #667eea; border-color: #667eea; }}
        .btn-primary:hover {{ background-color: #764ba2; border-color: #764ba2; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-dark" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <span class="navbar-brand mb-0 h1">⚡ HiredNow</span>
            <span class="navbar-text text-white">Job Application Automation</span>
        </div>
    </nav>

    <div class="hero">
        <div class="container text-center">
            <h1 class="display-4">Apply to Jobs Automatically</h1>
            <p class="lead">Find jobs. Optimize resume. Auto-apply. Track everything.</p>
            <a href="#search" class="btn btn-light btn-lg">Start Job Search</a>
        </div>
    </div>

    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="stat-card text-center">
                    <h2 class="text-primary">{len(jobs)}</h2>
                    <p class="text-muted">Jobs Found</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card text-center">
                    <h2 class="text-success">0</h2>
                    <p class="text-muted">Applications Sent</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card text-center">
                    <h2 class="text-warning">0</h2>
                    <p class="text-muted">Interviews</p>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">🔍 Search Jobs</h5>
                    </div>
                    <div class="card-body">
                        <form id="searchForm">
                            <div class="mb-3">
                                <label class="form-label">Job Title</label>
                                <input type="text" id="jobTitle" class="form-control" placeholder="e.g., Hospitality Manager">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Location</label>
                                <input type="text" id="jobLocation" class="form-control" placeholder="e.g., Nashville, TN">
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Search Jobs</button>
                        </form>
                        <div id="searchStatus" class="mt-3"></div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">⚡ Quick Actions</h5>
                    </div>
                    <div class="card-body">
                        <a href="https://hirednow.app" target="_blank" class="btn btn-outline-primary w-100 mb-2">View Website</a>
                        <a href="https://github.com/richardkrahl/hirednow" target="_blank" class="btn btn-outline-dark w-100 mb-2">View on GitHub</a>
                        <button class="btn btn-outline-success w-100" onclick="window.open('chrome://extensions', '_blank')">Open Chrome Extension</button>
                    </div>
                </div>
            </div>

            <div class="col-md-8">
                <div class="card">
                    <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">📋 Job Listings</h5>
                        <span class="badge bg-primary">{len(jobs)} found</span>
                    </div>
                    <div class="card-body">
                        {''.join([f"""
                        <div class="job-card">
                            <div class="d-flex justify-content-between">
                                <h6 class="mb-1">{job.get('title', 'Unknown')}</h6>
                                <span class="badge bg-info">{job.get('source', 'Unknown')}</span>
                            </div>
                            <p class="mb-1 text-muted">{job.get('company', 'Unknown')} • {job.get('location', 'Unknown')}</p>
                            <div class="d-flex gap-2 mt-2">
                                <a href="{job.get('url', '#')}" target="_blank" class="btn btn-sm btn-outline-primary">View Job</a>
                                <button class="btn btn-sm btn-outline-success" onclick="optimizeResume('{job.get('title', '').replace("'", "\\'")}')">Optimize Resume</button>
                            </div>
                        </div>
                        """ for job in jobs[:10]]) if jobs else '<p class="text-muted text-center">No jobs found yet. Use the search form to find jobs.</p>'}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p class="mb-0">HiredNow © 2026 • Built with ❤️ in Nashville</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('searchForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const title = document.getElementById('jobTitle').value;
            const location = document.getElementById('jobLocation').value;
            const status = document.getElementById('searchStatus');
            
            status.innerHTML = '<div class="alert alert-info">Searching...</div>';
            
            try {{
                const response = await fetch('/api/search', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{title, location}})
                }});
                const result = await response.json();
                status.innerHTML = '<div class="alert alert-success">Found ' + result.count + ' jobs!</div>';
                setTimeout(() => location.reload(), 2000);
            }} catch (error) {{
                status.innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
            }}
        }});

        function optimizeResume(jobTitle) {{
            alert('Resume optimization for: ' + jobTitle + '\\nRun: python3 optimizer/smart_optimizer.py in terminal');
        }}
    </script>
</body>
</html>
    """

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.json
    title = data.get('title', '')
    location = data.get('location', '')
    
    # Run scraper in background
    try:
        result = subprocess.run(
            ['python3', 'scraper/job_scraper.py', title, location],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        jobs = load_jobs()
        return jsonify({"success": True, "count": len(jobs)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/jobs')
def api_jobs():
    return jsonify(load_jobs())

if __name__ == '__main__':
    print("🚀 HiredNow Dashboard starting...")
    print("📍 Open: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
