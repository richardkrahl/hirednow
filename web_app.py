#!/usr/bin/env python3
"""
HiredNow Simple Web GUI
Flask-based visual interface
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import subprocess

app = Flask(__name__)
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/projects/job-hunter/data")

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Load data
    jobs = []
    if os.path.exists(f"{DATA_DIR}/jobs.json"):
        with open(f"{DATA_DIR}/jobs.json") as f:
            jobs = json.load(f)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HiredNow Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; }}
            .card {{ margin-bottom: 1rem; }}
        </style>
    </head>
    <body>
        <div class="hero text-center">
            <h1>🎯 HiredNow</h1>
            <p class="lead">Apply to jobs automatically</p>
        </div>
        
        <div class="container mt-4">
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5>🔍 Search Jobs</h5>
                            <form action="/search" method="POST">
                                <input type="text" name="title" class="form-control mb-2" placeholder="Job Title">
                                <input type="text" name="location" class="form-control mb-2" placeholder="Location">
                                <button type="submit" class="btn btn-primary w-100">Search</button>
                            </form>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-8">
                    <h3>Found {len(jobs)} Jobs</h3>
                    {"".join([f"""
                    <div class="card">
                        <div class="card-body">
                            <h5>{job.get('title', 'Unknown')}</h5>
                            <p>{job.get('company', 'Unknown')} • {job.get('location', 'Unknown')}</p>
                            <a href="{job.get('url', '#')}" target="_blank" class="btn btn-sm btn-outline-primary">View</a>
                        </div>
                    </div>
                    """ for job in jobs[:10]])}
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/search', methods=['POST'])
def search():
    """Search for jobs"""
    title = request.form.get('title', '')
    location = request.form.get('location', '')
    
    # Run scraper
    subprocess.run([
        'python3', 'scraper/job_scraper.py',
        title, location
    ], cwd=os.path.dirname(__file__))
    
    return f"""
    <script>window.location = '/';</script>
    <p>Searching for {title} in {location}...</p>
    """

if __name__ == '__main__':
    print("🚀 Starting HiredNow web app...")
    print("📍 Open: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
