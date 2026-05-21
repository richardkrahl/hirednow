#!/usr/bin/env python3
"""
HiredNow X/Twitter Poster - API-Free Browser Automation
Uses Playwright to post to X without API keys
"""

import json
import os
import time
from playwright.sync_api import sync_playwright
from datetime import datetime

class XPoster:
    def __init__(self):
        self.data_dir = os.path.expanduser("~/.openclaw/workspace/projects/job-hunter/data")
        self.config_file = f"{self.data_dir}/x_config.json"
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
        """Get X credentials - interactive or from config"""
        config = self.load_config()
        
        if config.get('username') and config.get('password'):
            use_saved = input(f"Use saved credentials for {config['username']}? (y/n): ").lower()
            if use_saved == 'y':
                return config['username'], config['password']
        
        print("\n🔐 X/Twitter Login")
        print("(Your credentials will be saved locally for future use)")
        username = input("Username/Email: ")
        password = input("Password: ")
        
        save = input("Save credentials for next time? (y/n): ").lower()
        if save == 'y':
            self.save_config({'username': username, 'password': password})
        
        return username, password
    
    def post_thread(self, tweets):
        """
        Post a thread to X using browser automation
        tweets: list of tweet texts
        """
        if len(tweets) == 1:
            print(f"\n📝 Preparing X Post")
            print(f"Tweet: {tweets[0][:100]}...")
        else:
            print(f"\n📝 Preparing X Thread ({len(tweets)} tweets)")
            for i, tweet in enumerate(tweets, 1):
                print(f"{i}. {tweet[:80]}...")
        
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
                slow_mo=150
            )
            
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            
            page = context.new_page()
            
            try:
                # Login
                print("🔐 Logging in to X...")
                page.goto("https://twitter.com/i/flow/login")
                time.sleep(3)
                
                # Fill login
                page.fill('input[name="text"]', username)
                page.click('//span[contains(text(), "Next")]')
                time.sleep(2)
                
                page.fill('input[name="password"]', password)
                page.click('//span[contains(text(), "Log in")]')
                time.sleep(3)
                
                # Check for 2FA
                if "enter your verification code" in page.content().lower():
                    print("⚠️  2FA required!")
                    code = input("Enter 2FA code: ")
                    page.fill('input[name="text"]', code)
                    page.click('//span[contains(text(), "Next")]')
                    time.sleep(2)
                
                # Post tweets
                tweet_urls = []
                reply_to = None
                
                for i, tweet in enumerate(tweets, 1):
                    print(f"✍️  Posting tweet {i}/{len(tweets)}...")
                    
                    # Click compose
                    page.click('a[href="/compose/tweet"]')
                    time.sleep(1)
                    
                    # Fill tweet
                    page.fill('div[data-testid="tweetTextarea_0"]', tweet)
                    time.sleep(1)
                    
                    # Post
                    page.click('button[data-testid="tweetButton"]')
                    time.sleep(2)
                    
                    # Get URL
                    current_url = page.url
                    if "/status/" in current_url:
                        tweet_urls.append(current_url)
                        print(f"✅ Posted: {current_url}")
                    
                    time.sleep(2)
                
                print(f"\n🎉 Thread posted successfully!")
                for url in tweet_urls:
                    print(f"🔗 {url}")
                
                # Log
                self.log_post("X/Twitter", "Thread", tweets[0], tweet_urls[0] if tweet_urls else "")
                
                browser.close()
                return True
                
            except Exception as e:
                print(f"❌ Error: {e}")
                browser.close()
                return False
    
    def log_post(self, platform, type_, content, result_url):
        """Log the post for tracking"""
        log_file = f"{self.data_dir}/posts_log.json"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "type": type_,
            "content": content[:100],
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
    """CLI interface with pre-built thread"""
    poster = XPoster()
    
    # Pre-built thread for HiredNow launch
    thread = [
        """I was paying $600+/year for job application tools that stored my resume in the cloud.

So I built my own.

Introducing HiredNow - $79 once, not $600+/year.

🧵👇""",
        
        """What it does:

🔍 Auto-finds jobs on LinkedIn & Indeed
✨ AI optimizes your resume per job
🤖 Browser extension auto-fills forms  
📊 Tracks your application pipeline

Everything runs locally. No cloud. No subscriptions.""",
        
        """Why local matters:

❌ Your resume never leaves your machine
❌ No API costs (uses Ollama)
❌ No data mining
❌ No "we updated our privacy policy"

Just you, your data, and Python.""",
        
        """The price comparison:

Others: $600+/year
HiredNow: $79 one-time

Savings year 1: $500+
Savings year 2: $600+
Savings year 3: $600+

Own your tools. Stop renting them.""",
        
        """Open source. MIT license.

Built with Python + Playwright + Ollama.

🌐 https://hirednow.app
⭐ https://github.com/richardkrahl/hirednow

RT if you're tired of subscription software."""
    ]
    
    print("=" * 60)
    print("HIRED NOW - X/Twitter Thread Poster")
    print("=" * 60)
    print("\nPre-built thread ready:")
    print(f"({len(thread)} tweets)")
    for i, tweet in enumerate(thread, 1):
        print(f"\n{i}. {tweet[:80]}...")
    
    print("\nOptions:")
    print("- 'thread' - post full thread")
    print("- 'single' - post just first tweet")
    print("- 'custom' - enter your own")
    
    choice = input("\nChoice: ").strip().lower()
    
    if choice == 'thread':
        poster.post_thread(thread)
    elif choice == 'single':
        poster.post_thread([thread[0]])
    else:
        print("\nCustom post:")
        tweets = []
        while True:
            tweet = input(f"Tweet {len(tweets)+1} (blank to finish):\n")
            if not tweet:
                break
            tweets.append(tweet)
        
        if tweets:
            poster.post_thread(tweets)


if __name__ == "__main__":
    main()
