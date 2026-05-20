#!/usr/bin/env python3
"""
JARVIS Auto-Applier
Browser automation for job applications
Uses Selenium/Playwright to auto-fill forms
"""

import json
import time
import random
from datetime import datetime
from urllib.parse import urlparse

class AutoApplier:
    """
    Automated job application filler
    Supports: LinkedIn Easy Apply, Indeed, company career portals
    """
    
    def __init__(self, profile_data=None):
        self.profile = profile_data or self._load_profile()
        self.application_log = []
    
    def _load_profile(self):
        """Load user profile from JSON"""
        import os
        profile_path = os.path.expanduser(
            "~/.openclaw/workspace/projects/job-hunter/data/profile.json"
        )
        
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                return json.load(f)
        
        return {}
    
    def save_profile(self, profile_data):
        """Save user profile"""
        import os
        profile_path = os.path.expanduser(
            "~/.openclaw/workspace/projects/job-hunter/data/profile.json"
        )
        
        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        print(f"💾 Profile saved to {profile_path}")
    
    def create_profile_template(self):
        """Create empty profile template"""
        template = {
            "personal": {
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": "",
                "address": "",
                "city": "",
                "state": "",
                "zip": "",
                "linkedin": "",
                "website": "",
                "github": ""
            },
            "work_authorization": {
                "authorized_us": True,
                "require_sponsorship": False,
                "clearance": None
            },
            "preferences": {
                "desired_salary_min": 0,
                "willing_relocate": False,
                "remote_only": False,
                "work_type": "full-time"  # full-time, part-time, contract
            },
            "experience": [
                {
                    "title": "",
                    "company": "",
                    "start_date": "",
                    "end_date": "",
                    "description": ""
                }
            ],
            "education": [
                {
                    "degree": "",
                    "school": "",
                    "graduation_year": ""
                }
            ],
            "skills": [],
            "resume_path": "",
            "cover_letter_template": ""
        }
        
        return template
    
    def log_application(self, job_data, status="pending"):
        """Log job application"""
        application = {
            "job_title": job_data.get("title"),
            "company": job_data.get("company"),
            "url": job_data.get("url"),
            "date": datetime.now().isoformat(),
            "status": status,  # pending, applied, rejected, interview
            "notes": ""
        }
        
        self.application_log.append(application)
        self._save_log()
    
    def _save_log(self):
        """Save application log"""
        import os
        log_path = os.path.expanduser(
            "~/.openclaw/workspace/projects/job-hunter/data/applications.json"
        )
        
        with open(log_path, 'w') as f:
            json.dump(self.application_log, f, indent=2)
    
    def load_log(self):
        """Load application log"""
        import os
        log_path = os.path.expanduser(
            "~/.openclaw/workspace/projects/job-hunter/data/applications.json"
        )
        
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                self.application_log = json.load(f)
        
        return self.application_log
    
    def generate_application_form_data(self, job_data):
        """
        Generate form data for job application
        Returns dict of field values
        """
        if not self.profile:
            print("❌ No profile found. Create one first.")
            return None
        
        form_data = {
            # Personal info
            "firstName": self.profile.get("personal", {}).get("first_name"),
            "lastName": self.profile.get("personal", {}).get("last_name"),
            "email": self.profile.get("personal", {}).get("email"),
            "phone": self.profile.get("personal", {}).get("phone"),
            "address": self.profile.get("personal", {}).get("address"),
            "city": self.profile.get("personal", {}).get("city"),
            "state": self.profile.get("personal", {}).get("state"),
            "zip": self.profile.get("personal", {}).get("zip"),
            
            # Links
            "linkedin": self.profile.get("personal", {}).get("linkedin"),
            "website": self.profile.get("personal", {}).get("website"),
            "github": self.profile.get("personal", {}).get("github"),
            
            # Work auth
            "authorized": self.profile.get("work_authorization", {}).get("authorized_us"),
            "sponsorship": self.profile.get("work_authorization", {}).get("require_sponsorship"),
            
            # Preferences
            "salary": self.profile.get("preferences", {}).get("desired_salary_min"),
            "relocate": self.profile.get("preferences", {}).get("willing_relocate"),
            "remote": self.profile.get("preferences", {}).get("remote_only"),
            
            # Resume path
            "resume": self.profile.get("resume_path"),
        }
        
        return form_data
    
    def check_already_applied(self, job_url):
        """Check if already applied to this job"""
        for app in self.application_log:
            if app.get("url") == job_url:
                return True
        return False
    
    def get_application_stats(self):
        """Get statistics on applications"""
        if not self.application_log:
            self.load_log()
        
        stats = {
            "total": len(self.application_log),
            "pending": 0,
            "applied": 0,
            "rejected": 0,
            "interview": 0,
            "by_company": {},
            "by_date": {}
        }
        
        for app in self.application_log:
            status = app.get("status", "pending")
            stats[status] += 1
            
            company = app.get("company", "Unknown")
            stats["by_company"][company] = stats["by_company"].get(company, 0) + 1
            
            date = app.get("date", "")[:10]  # YYYY-MM-DD
            stats["by_date"][date] = stats["by_date"].get(date, 0) + 1
        
        return stats
    
    def print_stats(self):
        """Print application statistics"""
        stats = self.get_application_stats()
        
        print("\n" + "="*60)
        print("📊 APPLICATION STATISTICS")
        print("="*60)
        print(f"\nTotal Applications: {stats['total']}")
        print(f"  ✅ Applied: {stats['applied']}")
        print(f"  ⏳ Pending: {stats['pending']}")
        print(f"  ❌ Rejected: {stats['rejected']}")
        print(f"  🎯 Interview: {stats['interview']}")
        
        if stats['by_company']:
            print(f"\nTop Companies:")
            sorted_companies = sorted(
                stats['by_company'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
            for company, count in sorted_companies:
                print(f"  {company}: {count}")


# Browser automation (placeholder for Selenium/Playwright)
class BrowserAutomator:
    """
    Browser automation for form filling
    Requires: pip install selenium webdriver-manager
    """
    
    def __init__(self):
        self.driver = None
    
    def init_driver(self):
        """Initialize browser driver"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            options.add_argument("--headless")  # Run in background
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            
            return True
        except Exception as e:
            print(f"❌ Browser init error: {e}")
            return False
    
    def fill_form(self, url, form_data):
        """Fill job application form"""
        if not self.driver:
            if not self.init_driver():
                return False
        
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for load
            
            # Find and fill form fields
            # This is a simplified version - real implementation would:
            # - Detect field types
            # - Handle different form structures
            # - Upload resume
            # - Submit form
            
            print(f"🌐 Loaded: {url}")
            print("⚠️  Form automation requires site-specific implementation")
            
            return True
            
        except Exception as e:
            print(f"❌ Form fill error: {e}")
            return False
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()


# CLI interface
if __name__ == "__main__":
    import sys
    
    applier = AutoApplier()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python auto_applier.py create-profile")
        print("  python auto_applier.py stats")
        print("  python auto_applier.py log <job_url> [status]")
        print("  python auto_applier.py check <job_url>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create-profile":
        template = applier.create_profile_template()
        applier.save_profile(template)
        print("✅ Profile template created!")
        print("Edit: ~/.openclaw/workspace/projects/job-hunter/data/profile.json")
    
    elif command == "stats":
        applier.print_stats()
    
    elif command == "log" and len(sys.argv) > 2:
        job = {"url": sys.argv[2], "title": "Unknown", "company": "Unknown"}
        status = sys.argv[3] if len(sys.argv) > 3 else "pending"
        applier.log_application(job, status)
        print(f"✅ Logged application: {status}")
    
    elif command == "check" and len(sys.argv) > 2:
        if applier.check_already_applied(sys.argv[2]):
            print("⚠️  Already applied to this job")
        else:
            print("✅ Not yet applied")
    
    else:
        print("Invalid command")
