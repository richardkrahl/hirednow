#!/usr/bin/env python3
"""
JARVIS Job Hunter - Alternative Stealth Mode
Uses Playwright with stealth patches (no invisible_playwright required)
"""

from playwright.sync_api import sync_playwright
import time
import random

def stealth_scrape_indeed(query, location):
    """
    Scrape Indeed using Playwright with stealth techniques
    """
    print(f"🕵️  Stealth scraping Indeed for: {query} in {location}")
    
    with sync_playwright() as p:
        # Launch with stealth settings
        browser = p.firefox.launch(
            headless=False,  # Visible browser (less suspicious)
            slow_mo=100,     # Slow down actions
        )
        
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        # Navigate with human-like delays
        url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
        page.goto(url, wait_until="networkidle")
        
        # Wait for content
        time.sleep(random.uniform(2, 4))
        
        # Scroll like human
        for _ in range(3):
            page.mouse.wheel(0, random.randint(300, 700))
            time.sleep(random.uniform(0.5, 1.5))
        
        # Extract jobs
        jobs = page.evaluate("""() => {
            const cards = document.querySelectorAll('[data-testid="job-title"], .jobTitle, h2.jobTitle');
            return Array.from(cards).slice(0, 25).map(card => {
                const parent = card.closest('[data-testid="job-slide"], .job_seen_beacon, .slider_container') || card.parentElement;
                return {
                    title: card.textContent?.trim() || '',
                    company: parent.querySelector('[data-testid="company-name"], .companyName')?.textContent?.trim() || '',
                    location: parent.querySelector('[data-testid="job-location"], .companyLocation')?.textContent?.trim() || '',
                    url: card.closest('a')?.href || ''
                };
            });
        }""")
        
        browser.close()
        
        # Filter valid jobs
        valid_jobs = [j for j in jobs if j.get('title') and j.get('company')]
        
        print(f"✅ Found {len(valid_jobs)} jobs")
        return valid_jobs


def simple_scrape_indeed(query, location):
    """
    Fallback: Simple requests-based scraper with rotation
    """
    import requests
    from bs4 import BeautifulSoup
    
    print(f"📡 Simple scrape Indeed: {query} in {location}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    
    url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            jobs = []
            cards = soup.find_all(['div', 'td'], class_=lambda x: x and ('job' in x.lower() if x else False))[:25]
            
            for card in cards:
                title_elem = card.find(['h2', 'a'], class_=lambda x: x and ('title' in x.lower() if x else False))
                if title_elem:
                    jobs.append({
                        'title': title_elem.get_text(strip=True),
                        'company': 'Unknown',
                        'location': location,
                        'url': url
                    })
            
            print(f"✅ Found {len(jobs)} jobs")
            return jobs
        else:
            print(f"⚠️  Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        query = sys.argv[1]
        location = sys.argv[2]
        
        # Try Playwright first
        try:
            jobs = stealth_scrape_indeed(query, location)
            if jobs:
                for i, job in enumerate(jobs[:5], 1):
                    print(f"{i}. {job['title']} at {job['company']}")
        except Exception as e:
            print(f"Playwright failed: {e}")
            print("Trying simple scraper...")
            jobs = simple_scrape_indeed(query, location)
    else:
        print("Usage: python alt_stealth.py 'Product Manager' 'Nashville, TN'")
