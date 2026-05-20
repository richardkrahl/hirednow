#!/usr/bin/env python3
"""
JARVIS Application Tracker
Track job applications, interviews, follow-ups
Excel/CSV export, reminders, analytics
"""

import json
import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict

class ApplicationTracker:
    """
    Track job applications from search to hire
    """
    
    def __init__(self, data_dir="~/.openclaw/workspace/projects/job-hunter/data"):
        self.data_dir = os.path.expanduser(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        self.db_file = os.path.join(self.data_dir, "applications_db.json")
        self.load_database()
    
    def load_database(self):
        """Load application database"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.database = json.load(f)
        else:
            self.database = {
                "applications": [],
                "companies": {},
                "contacts": [],
                "notes": []
            }
    
    def save_database(self):
        """Save application database"""
        with open(self.db_file, 'w') as f:
            json.dump(self.database, f, indent=2)
    
    def add_application(self, job_data, status="discovered"):
        """
        Add new job application to track
        """
        application = {
            "id": len(self.database["applications"]) + 1,
            "title": job_data.get("title", ""),
            "company": job_data.get("company", ""),
            "location": job_data.get("location", ""),
            "url": job_data.get("url", ""),
            "salary_range": job_data.get("salary", ""),
            "description": job_data.get("summary", ""),
            "source": job_data.get("source", ""),
            
            # Tracking
            "status": status,  # discovered, applied, phone_screen, interview, offer, rejected, ghosted
            "date_discovered": datetime.now().isoformat(),
            "date_applied": None,
            "date_last_contact": None,
            
            # Documents
            "resume_used": "",
            "cover_letter_used": "",
            
            # Scores
            "match_score": job_data.get("match_score", 0),
            "interest_level": 3,  # 1-5
            
            # Notes
            "notes": "",
            "follow_up_date": None,
            
            # Contact info
            "recruiter_name": "",
            "recruiter_email": "",
            "recruiter_phone": "",
        }
        
        # Check if already exists
        for existing in self.database["applications"]:
            if existing["url"] == application["url"]:
                print(f"⚠️  Already tracking: {application['title']} at {application['company']}")
                return existing
        
        self.database["applications"].append(application)
        self.save_database()
        
        print(f"✅ Added: {application['title']} at {application['company']}")
        return application
    
    def update_status(self, app_id, new_status, notes=""):
        """Update application status"""
        for app in self.database["applications"]:
            if app["id"] == app_id:
                old_status = app["status"]
                app["status"] = new_status
                
                if new_status == "applied" and not app["date_applied"]:
                    app["date_applied"] = datetime.now().isoformat()
                
                app["date_last_contact"] = datetime.now().isoformat()
                
                if notes:
                    app["notes"] += f"\n[{datetime.now().strftime('%Y-%m-%d')}] {notes}"
                
                self.save_database()
                print(f"✅ Updated: {app['title']} - {old_status} → {new_status}")
                return app
        
        print(f"❌ Application {app_id} not found")
        return None
    
    def set_follow_up(self, app_id, days_from_now=7):
        """Set follow-up reminder"""
        follow_up_date = datetime.now() + timedelta(days=days_from_now)
        
        for app in self.database["applications"]:
            if app["id"] == app_id:
                app["follow_up_date"] = follow_up_date.isoformat()
                self.save_database()
                print(f"📅 Follow-up set for {follow_up_date.strftime('%Y-%m-%d')}")
                return app
        
        return None
    
    def get_pipeline(self):
        """Get applications organized by status"""
        pipeline = defaultdict(list)
        
        for app in self.database["applications"]:
            pipeline[app["status"]].append(app)
        
        return dict(pipeline)
    
    def get_follow_ups(self):
        """Get applications needing follow-up"""
        today = datetime.now()
        follow_ups = []
        
        for app in self.database["applications"]:
            if app.get("follow_up_date"):
                follow_up = datetime.fromisoformat(app["follow_up_date"])
                if follow_up.date() <= today.date():
                    days_overdue = (today - follow_up).days
                    follow_ups.append({
                        **app,
                        "days_overdue": days_overdue
                    })
        
        return sorted(follow_ups, key=lambda x: x["days_overdue"], reverse=True)
    
    def get_statistics(self):
        """Get comprehensive statistics"""
        apps = self.database["applications"]
        
        if not apps:
            return {"error": "No applications tracked"}
        
        stats = {
            "total_applications": len(apps),
            "by_status": defaultdict(int),
            "by_company": defaultdict(int),
            "by_source": defaultdict(int),
            "by_week": defaultdict(int),
            "avg_match_score": 0,
            "response_rate": 0,
            "interview_rate": 0,
            "offer_rate": 0,
        }
        
        total_score = 0
        responses = 0
        interviews = 0
        offers = 0
        
        for app in apps:
            # Status counts
            stats["by_status"][app["status"]] += 1
            
            # Company counts
            stats["by_company"][app["company"]] += 1
            
            # Source counts
            stats["by_source"][app["source"]] += 1
            
            # Weekly counts
            week = app["date_discovered"][:7]  # YYYY-MM
            stats["by_week"][week] += 1
            
            # Match scores
            if app.get("match_score"):
                total_score += app["match_score"]
            
            # Response tracking
            if app["status"] in ["applied", "phone_screen", "interview", "offer"]:
                responses += 1
            if app["status"] in ["interview", "offer"]:
                interviews += 1
            if app["status"] == "offer":
                offers += 1
        
        stats["avg_match_score"] = round(total_score / len(apps), 1) if apps else 0
        stats["response_rate"] = round((responses / len(apps)) * 100, 1) if apps else 0
        stats["interview_rate"] = round((interviews / len(apps)) * 100, 1) if apps else 0
        stats["offer_rate"] = round((offers / len(apps)) * 100, 1) if apps else 0
        
        return stats
    
    def export_csv(self, filename="applications.csv"):
        """Export to CSV for Excel"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not self.database["applications"]:
            print("❌ No applications to export")
            return
        
        keys = self.database["applications"][0].keys()
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.database["applications"])
        
        print(f"💾 Exported to {filepath}")
    
    def print_dashboard(self):
        """Print dashboard view"""
        print("\n" + "="*70)
        print("📊 JOB HUNT DASHBOARD")
        print("="*70)
        
        stats = self.get_statistics()
        
        if "error" in stats:
            print(f"\n{stats['error']}")
            return
        
        print(f"\n📈 OVERVIEW")
        print(f"   Total Applications: {stats['total_applications']}")
        print(f"   Avg Match Score: {stats['avg_match_score']}%")
        print(f"   Response Rate: {stats['response_rate']}%")
        print(f"   Interview Rate: {stats['interview_rate']}%")
        print(f"   Offer Rate: {stats['offer_rate']}%")
        
        print(f"\n📋 PIPELINE")
        for status, count in sorted(stats['by_status'].items()):
            emoji = {
                "discovered": "🔍",
                "applied": "📤",
                "phone_screen": "📞",
                "interview": "🎯",
                "offer": "💰",
                "rejected": "❌",
                "ghosted": "👻"
            }.get(status, "📄")
            print(f"   {emoji} {status}: {count}")
        
        # Follow-ups needed
        follow_ups = self.get_follow_ups()
        if follow_ups:
            print(f"\n⏰ FOLLOW-UPS NEEDED ({len(follow_ups)})")
            for app in follow_ups[:5]:
                overdue = f"({app['days_overdue']} days overdue)" if app['days_overdue'] > 0 else "(today)"
                print(f"   • {app['company']} - {app['title']} {overdue}")
        
        print(f"\n🏢 TOP COMPANIES")
        sorted_companies = sorted(
            stats['by_company'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for company, count in sorted_companies:
            print(f"   {company}: {count} applications")


# CLI interface
if __name__ == "__main__":
    import sys
    
    tracker = ApplicationTracker()
    
    if len(sys.argv) < 2:
        tracker.print_dashboard()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) > 2:
        # Quick add from job URL
        job = {"url": sys.argv[2], "title": "Unknown", "company": "Unknown"}
        if len(sys.argv) > 3:
            job["title"] = sys.argv[3]
        if len(sys.argv) > 4:
            job["company"] = sys.argv[4]
        tracker.add_application(job)
    
    elif command == "update" and len(sys.argv) > 3:
        app_id = int(sys.argv[2])
        status = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        tracker.update_status(app_id, status, notes)
    
    elif command == "follow-up" and len(sys.argv) > 2:
        app_id = int(sys.argv[2])
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        tracker.set_follow_up(app_id, days)
    
    elif command == "export":
        tracker.export_csv()
    
    elif command == "dashboard":
        tracker.print_dashboard()
    
    else:
        print("Usage:")
        print("  python application_tracker.py [dashboard]")
        print("  python application_tracker.py add <url> [title] [company]")
        print("  python application_tracker.py update <app_id> <status> [notes]")
        print("  python application_tracker.py follow-up <app_id> [days]")
        print("  python application_tracker.py export")
