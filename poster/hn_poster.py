#!/usr/bin/env python3
"""
HiredNow Hacker News Poster - API-Free Browser Automation
Uses Playwright to post to HN without API keys
"""

import json
import os
from playwright.sync_api import sync_playwright
from datetime import datetime

class HNPoster:
    def __init__(self):
        self.data_dir = os.path.expanduser("~/.openclaw/workspace/projects/job-hunter/data")
        self.config_file = f"{self.data_dir}/hn_config.json"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def load_config(self):
        """Load saved credentials if they exist"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self, config):
        """Save credentials for future use"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        print(f"✅ Credentials saved to {self.config_file}")
    
    def get_credentials(self):
        """Get HN credentials - interactive or from config"""
        config = self.load_config()
        
        if config.get('username') and config.get('password'):
            use_saved = input(f"Use saved credentials for {config['username']}? (y/n): ").lower()
            if use_saved == 'y':
                return config['username'], config['password']
        
        print("\n🔐 Hacker News Login")
        print("(Your credentials will be saved locally for future use)")
        username = input("Username: ")
        password = input("Password: ")
        
        save = input("Save credentials for next time? (y/n): ").lower()
        if save == 'y':
            self.save_config({'username': username, 'password': password})
        
        return username, password
    
    def post_to_hn(self, title, url, text=None):
        """
        Post to Hacker News using browser automation
        """
        print(f"\n📝 Preparing HN Post")
        print(f"Title: {title}")
        print(f"URL: {url}")
        if text:
            print(f"Text: {text[:100]}...")
        
        # Confirm before posting
        confirm = input("\nReady to post? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Post cancelled")
            return False
        
        username, password = self.get_credentials()
        
        print("\n🚀 Launching browser...")
        
        with sync_playwright() as p:
            # Launch with stealth settings
            browser = p.firefox.launch(
                headless=False,  # Visible so you can see it work
                slow_mo=100
            )
            
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            
            page = context.new_page()
            
            try:
                # Login
                print("🔐 Logging in to HN...")
                page.goto("https://news.ycombinator.com/login")
                page.fill('input[name="acct"]', username)
                page.fill('input[name="pw"]', password)
                page.click('input[value="login"]')
                page.wait_for_load_state("networkidle")
                
                # Navigate to submit
                print("➕ Navigating to submit page...")
                page.goto("https://news.ycombinator.com/submit")
                page.wait_for_load_state("networkidle")
                
                # Fill form
                print("✍️  Filling submission form...")
                page.fill('input[name="title"]', title)
                page.fill('input[name="url"]', url)
                
                if text:
                    # HN doesn't support text + URL, use text instead
                    page.click('a:has-text("or create an Ask HN")')  # Switch to text mode
                    page.fill('textarea[name="text"]', text)
                
                # Submit
                print("📤 Submitting...")
                page.click('input[type="submit"]')
                page.wait_for_load_state("networkidle")
                
                # Success check
                if "news.ycombinator.com/newest" in page.url or "item?id=" in page.url:
                    print("✅ Posted successfully!")
                    print(f"🔗 {page.url}")
                    
                    # Save to log
                    self.log_post("Hacker News", title, url, page.url)
                    
                    browser.close()
                    return True
                else:
                    print("⚠️  Check browser - may need manual verification")
                    input("Press Enter when done...")
                    browser.close()
                    return False
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                browser.close()
                return False
    
    def log_post(self, platform, title, url, result_url):
        """Log the post for tracking"""
        log_file = f"{self.data_dir}/posts_log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "title": title,
            "url": url,
            "result_url": result_url
        }
        
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"📝 Logged to {log_file}")


def main():
    """CLI interface"""
    poster = HNPoster()
    
    # HiredNow launch post
    title = "Show HN: HiredNow - $79 one-time job application automation (100% local)"
    url = "https://hirednow.app"
    
    print("=" * 60)
    print("HIRED NOW - Hacker News Poster")
    print("=" * 60)
    print("\nThis will post to Hacker News using browser automation.")
    print("No API keys needed. 100% local.")
    print()
    
    # Post
    success = poster.post_to_hn(title, url)
    
    if success:
        print("\n🎉 HN post successful!")
    else:
        print("\n⚠️  Post may have failed. Check browser.")


if __name__ == "__main__":
    main()
