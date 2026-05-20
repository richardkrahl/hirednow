#!/usr/bin/env python3
"""
JARVIS Stealth Job Scraper
Uses invisible_playwright to bypass bot detection
"""

try:
    from invisible_playwright import InvisiblePlaywright
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("⚠️  invisible_playwright not installed")
    print("   Run: pip install git+https://github.com/feder-cr/invisible_playwright.git")
    print("   Then: python -m invisible_playwright fetch")

import json
from bs4 import BeautifulSoup
import time

class StealthJobScraper:
    """
    Job scraper using stealth Firefox
    Bypasses Indeed, LinkedIn bot detection
    """
    
    def __init__(self):
        self.jobs = []
    
    def scrape_indeed(self, query, location, max_results=50):
        """
        Scrape Indeed using stealth browser
        """
        if not STEALTH_AVAILABLE:
            print("❌ Stealth mode not available")
            return []
        
        url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
        
        print(f"🕵️  Stealth scraping Indeed...")
        
        with InvisiblePlaywright() as browser:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            
            # Wait for job cards to load
            page.wait_for_selector(".jobsearch-SerpJobCard", timeout=10000)
            
            # Get page content
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Parse jobs
            job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard')[:max_results]
            
            for card in job_cards:
                try:
                    job = {
                        'title': card.find('h2', class_='jobTitle').get_text(strip=True) if card.find('h2', class_='jobTitle') else '',
                        'company': card.find('span', class_='companyName').get_text(strip=True) if card.find('span', class_name='companyName') else '',
                        'location': card.find('div', class_='companyLocation').get_text(strip=True) if card.find('div', class_='companyLocation') else '',
                        'summary': card.find('div', class_='job-snippet').get_text(strip=True) if card.find('div', class_='job-snippet') else '',
                        'source': 'Indeed',
                        'scraped_at': time.strftime('%Y-%m-%dT%H:%M:%S')
                    }
                    
                    # Get URL from link
                    link = card.find('a', class_='jcs-JobTitle')
                    if link:
                        job['url'] = 'https://www.indeed.com' + link.get('href', '')
                    
                    if job['title'] and job['company']:
                        self.jobs.append(job)
                        
                except Exception as e:
                    continue
        
        print(f"✅ Found {len(self.jobs)} jobs from Indeed")
        return self.jobs
    
    def auto_fill_greenhouse(self, url, profile_data):
        """
        Auto-fill Greenhouse application form
        """
        if not STEALTH_AVAILABLE:
            return False
        
        print(f"🕵️  Auto-filling {url}...")
        
        with InvisiblePlaywright() as browser:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            
            # Fill common Greenhouse fields
            fields = {
                'first_name': profile_data.get('firstName'),
                'last_name': profile_data.get('lastName'),
                'email': profile_data.get('email'),
                'phone': profile_data.get('phone'),
                'linkedin': profile_data.get('linkedin'),
                'website': profile_data.get('website'),
            }
            
            filled = 0
            for field_name, value in fields.items():
                if value:
                    try:
                        # Try different selectors
                        selectors = [
                            f"input[name='{field_name}']",
                            f"input[id*='{field_name}']",
                            f"input[placeholder*='{field_name.replace('_', ' ')}']",
                        ]
                        
                        for selector in selectors:
                            try:
                                page.fill(selector, value)
                                filled += 1
                                break
                            except:
                                continue
                    except:
                        pass
            
            print(f"✅ Filled {filled} fields")
            
            # Take screenshot for verification
            screenshot_path = f"/tmp/greenhouse_{int(time.time())}.png"
            page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            
            return filled > 0
    
    def auto_fill_lever(self, url, profile_data):
        """
        Auto-fill Lever application form
        """
        if not STEALTH_AVAILABLE:
            return False
        
        print(f"🕵️  Auto-filling Lever: {url}...")
        
        with InvisiblePlaywright() as browser:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            
            # Lever uses different field names
            fields = {
                'name': f"{profile_data.get('firstName', '')} {profile_data.get('lastName', '')}".strip(),
                'email': profile_data.get('email'),
                'phone': profile_data.get('phone'),
                'org': profile_data.get('currentCompany'),
                'linkedin': profile_data.get('linkedin'),
                'urls[Portfolio]': profile_data.get('website'),
            }
            
            filled = 0
            for field_name, value in fields.items():
                if value:
                    try:
                        page.fill(f"input[name='{field_name}']", value)
                        filled += 1
                    except:
                        pass
            
            print(f"✅ Filled {filled} fields")
            return filled > 0


if __name__ == "__main__":
    import sys
    
    if not STEALTH_AVAILABLE:
        print("\n" + "="*60)
        print("INSTALL INSTRUCTIONS")
        print("="*60)
        print("1. pip install git+https://github.com/feder-cr/invisible_playwright.git")
        print("2. python -m invisible_playwright fetch")
        print("3. Run this script again")
        sys.exit(1)
    
    scraper = StealthJobScraper()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "indeed" and len(sys.argv) > 3:
            query = sys.argv[2]
            location = sys.argv[3]
            jobs = scraper.scrape_indeed(query, location)
            print(f"\nFound {len(jobs)} jobs")
            for i, job in enumerate(jobs[:5], 1):
                print(f"{i}. {job['title']} at {job['company']}")
        
        elif command == "fill" and len(sys.argv) > 2:
            url = sys.argv[2]
            # Load profile
            import json
            profile_path = "~/.openclaw/workspace/projects/job-hunter/data/profile.json"
            try:
                with open(profile_path) as f:
                    profile = json.load(f)
                scraper.auto_fill_greenhouse(url, profile.get('personal', {}))
            except FileNotFoundError:
                print(f"❌ Profile not found. Create: {profile_path}")
        
        else:
            print("Usage:")
            print("  python stealth_scraper.py indeed 'Product Manager' 'Nashville, TN'")
            print("  python stealth_scraper.py fill 'https://boards.greenhouse.io/...'")
    else:
        print("Stealth Job Scraper - Ready")
        print("Install invisible_playwright to enable")
