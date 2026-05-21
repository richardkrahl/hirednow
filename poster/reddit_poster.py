#!/usr/bin/env python3
"""
HiredNow Reddit Poster - API-Free Browser Automation
Uses Playwright to post to Reddit without API keys
"""

import json
import os
import time
from playwright.sync_api import sync_playwright
from datetime import datetime

class RedditPoster:
    def __init__(self):
        self.data_dir = os.path.expanduser("~/.openclaw/workspace/projects/job-hunter/data")
        self.config_file = f"{self.data_dir}/reddit_config.json"
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
        """Get Reddit credentials - interactive or from config"""
        config = self.load_config()
        
        if config.get('username') and config.get('password'):
            use_saved = input(f"Use saved credentials for {config['username']}? (y/n): ").lower()
            if use_saved == 'y':
                return config['username'], config['password']
        
        print("\n🔐 Reddit Login")
        print("(Your credentials will be saved locally for future use)")
        username = input("Username: ")
        password = input("Password: ")
        
        save = input("Save credentials for next time? (y/n): ").lower()
        if save == 'y':
            self.save_config({'username': username, 'password': password})
        
        return username, password
    
    def post_to_subreddit(self, subreddit, title, text):
        """
        Post to a subreddit using browser automation
        """
        print(f"\n📝 Preparing Reddit Post")
        print(f"Subreddit: r/{subreddit}")
        print(f"Title: {title}")
        print(f"Text: {text[:100]}...")
        
        # Confirm before posting
        confirm = input("\nReady to post? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Post cancelled")
            return False
        
        username, password = self.get_credentials()
        
        print("\n🚀 Launching browser...")
        
        with sync_playwright() as p:
            browser = p.firefox.launch(
                headless=False,
                slow_mo=100
            )
            
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            
            page = context.new_page()
            
            try:
                # Login
                print("🔐 Logging in to Reddit...")
                page.goto("https://www.reddit.com/login/")
                time.sleep(2)
                
                # Reddit uses iframes for login sometimes
                page.fill('input[name="username"]', username)
                page.fill('input[name="password"]', password)
                page.click('button[type="submit"]')
                time.sleep(3)
                
                # Navigate to subreddit submit
                print(f"➕ Navigating to r/{subreddit}...")
                page.goto(f"https://www.reddit.com/r/{subreddit}/submit")
                time.sleep(2)
                
                # Fill form
                print("✍️  Filling submission form...")
                page.fill('textarea[placeholder*="Title"]', title)
                page.fill('div[contenteditable="true"]', text)
                
                # Submit
                print("📤 Submitting...")
                page.click('button[type="submit"]')
                time.sleep(3)
                
                # Check if successful
                if "/comments/" in page.url:
                    print("✅ Posted successfully!")
                    print(f"🔗 {page.url}")
                    
                    self.log_post("Reddit", subreddit, title, page.url)
                    
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
    
    def log_post(self, platform, subreddit, title, result_url):
        """Log the post for tracking"""
        log_file = f"{self.data_dir}/posts_log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": f"{platform} (r/{subreddit})",
            "title": title,
            "url": result_url
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
    """CLI interface with pre-built posts"""
    poster = RedditPoster()
    
    # Pre-built posts for different subreddits
    posts = [
        {
            "subreddit": "webdev",
            "title": "Built a job application automation tool - 100% local, no cloud, $79 one-time",
            "text": """I got tired of paying $600+/year for job application tools that store my resume in the cloud. So I built HiredNow.

It's a Python-based job application automation tool that:
- Scrapes LinkedIn & Indeed with Playwright
- Uses local AI (Ollama) to tailor resumes - no API costs
- Auto-fills job forms via Chrome extension
- Tracks applications in a local dashboard

The kicker: Everything runs locally. Your resume never touches the cloud. No subscriptions. $79 one-time.

Tech stack:
- Python 3.11+
- Playwright for browser automation
- Ollama for local AI
- Chrome Extension for form filling
- JSON Resume format

Open source, MIT license.

Site: https://hirednow.app
GitHub: https://github.com/richardkrahl/hirednow

Happy to answer questions about the architecture or local AI setup."""
        },
        {
            "subreddit": "antiwork",
            "title": "Stop renting your job search tools - I built something better",
            "text": """I was paying $600+/year just to auto-apply to jobs. That's insane for a tool.

So I built HiredNow.

The anti-subscription job application tool:
- $79 one-time (not $600+/year)
- 100% local - your data never leaves your machine
- No cloud lock-in
- You own it forever
- Open source (MIT)

It does everything the expensive tools do:
✅ Auto-finds jobs on LinkedIn/Indeed
✅ AI optimizes your resume per job
✅ Auto-fills application forms
✅ Tracks your pipeline

But here's the thing - you own it. No monthly fees. No "cancel anytime" nonsense. Just a tool that works.

Built with Python + local AI (Ollama). No API keys needed. Runs on your machine.

https://hirednow.app
https://github.com/richardkrahl/hirednow

Stop renting. Start owning."""
        },
        {
            "subreddit": "python",
            "title": "Built a job application automation tool with Python + Playwright + Local AI",
            "text": """Hey Python devs,

I built HiredNow - a job application automation tool using:
- Python 3.11+ for core automation
- Playwright for browser scraping
- Ollama for local AI (no OpenAI API costs)
- Chrome Extension for form auto-fill
- JSON Resume for standardization

Features:
- Scrapes LinkedIn & Indeed automatically
- AI tailors resume per job using local LLM
- Auto-fills Greenhouse/Lever job forms
- Tracks applications with SQLite
- Generates cover letters

The cool part: Everything is local. No cloud. No subscriptions. Your resume never leaves your machine.

Pricing: $79 one-time (vs $600+/year for competitors)

GitHub: https://github.com/richardkrahl/hirednow
Site: https://hirednow.app

Looking for feedback on the architecture and happy to discuss the local AI implementation."""
        }
    ]
    
    print("=" * 60)
    print("HIRED NOW - Reddit Poster")
    print("=" * 60)
    print("\nPre-built posts ready:")
    
    for i, post in enumerate(posts, 1):
        print(f"\n{i}. r/{post['subreddit']}")
        print(f"   Title: {post['title'][:60]}...")
    
    print("\nOptions:")
    print("- Enter number (1-3) to post that one")
    print("- Enter 'all' to post to all three")
    print("- Enter 'custom' for manual entry")
    
    choice = input("\nChoice: ").strip().lower()
    
    if choice == 'all':
        for post in posts:
            poster.post_to_subreddit(post['subreddit'], post['title'], post['text'])
            time.sleep(60)  # Rate limiting
    elif choice.isdigit() and 1 <= int(choice) <= len(posts):
        post = posts[int(choice) - 1]
        poster.post_to_subreddit(post['subreddit'], post['title'], post['text'])
    else:
        print("\nCustom post:")
        subreddit = input("Subreddit (without r/): ")
        title = input("Title: ")
        text = input("Text (press Enter twice when done):\n")
        poster.post_to_subreddit(subreddit, title, text)


if __name__ == "__main__":
    main()
