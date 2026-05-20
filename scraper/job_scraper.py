#!/usr/bin/env python3
"""
JARVIS Job Scraper
Free job search automation - No API keys needed
Sources: LinkedIn, Indeed, company career pages via RSS/HTML
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote
import feedparser

class JobScraper:
    """
    Multi-source job scraper
    Privacy-first: No accounts, no tracking, local only
    """
    
    def __init__(self, cache_dir="~/.openclaw/workspace/projects/job-hunter/data"):
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        
        # Job board RSS feeds (where available)
        self.rss_sources = {
            'stackoverflow': 'https://stackoverflow.com/jobs/feed',
            'github': 'https://jobs.github.com/positions.atom',
        }
        
        # Search URLs
        self.search_urls = {
            'indeed': 'https://www.indeed.com/jobs',
            'linkedin': 'https://www.linkedin.com/jobs/search',
        }
    
    def search_indeed(self, query, location="", max_results=50):
        """
        Search Indeed for jobs
        """
        jobs = []
        
        params = {
            'q': query,
            'l': location,
            'start': 0,
        }
        
        try:
            response = self.session.get(
                self.search_urls['indeed'],
                params=params,
                timeout=15
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Indeed job cards
            job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard')[:max_results]
            
            for card in job_cards:
                try:
                    job = {
                        'title': '',
                        'company': '',
                        'location': '',
                        'summary': '',
                        'url': '',
                        'posted': '',
                        'source': 'Indeed',
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    # Title
                    title_elem = card.find('h2', class_='jobTitle')
                    if title_elem:
                        job['title'] = title_elem.get_text(strip=True)
                        link = title_elem.find('a')
                        if link:
                            job['url'] = urljoin('https://www.indeed.com', link.get('href', ''))
                    
                    # Company
                    company_elem = card.find('span', class_='companyName')
                    if company_elem:
                        job['company'] = company_elem.get_text(strip=True)
                    
                    # Location
                    location_elem = card.find('div', class_='companyLocation')
                    if location_elem:
                        job['location'] = location_elem.get_text(strip=True)
                    
                    # Summary
                    summary_elem = card.find('div', class_='job-snippet')
                    if summary_elem:
                        job['summary'] = summary_elem.get_text(strip=True)
                    
                    # Posted date
                    date_elem = card.find('span', class_='date')
                    if date_elem:
                        job['posted'] = date_elem.get_text(strip=True)
                    
                    if job['title'] and job['company']:
                        jobs.append(job)
                        
                except Exception as e:
                    continue
            
            time.sleep(random.uniform(2, 4))  # Be polite
            
        except Exception as e:
            print(f"❌ Indeed search error: {e}")
        
        return jobs
    
    def search_linkedin(self, query, location="", max_results=50):
        """
        Search LinkedIn Jobs (public listings)
        """
        jobs = []
        
        # LinkedIn public job search URL
        params = {
            'keywords': query,
            'location': location,
            'trk': 'public_jobs_jobs-search-bar_search-submit',
        }
        
        try:
            response = self.session.get(
                self.search_urls['linkedin'],
                params=params,
                timeout=15
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # LinkedIn job cards
            job_cards = soup.find_all('div', class_='base-card')[:max_results]
            
            for card in job_cards:
                try:
                    job = {
                        'title': '',
                        'company': '',
                        'location': '',
                        'summary': '',
                        'url': '',
                        'posted': '',
                        'source': 'LinkedIn',
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    # Title
                    title_elem = card.find('h3', class_='base-search-card__title')
                    if title_elem:
                        job['title'] = title_elem.get_text(strip=True)
                    
                    # Company
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    if company_elem:
                        job['company'] = company_elem.get_text(strip=True)
                    
                    # Location
                    location_elem = card.find('span', class_='job-search-card__location')
                    if location_elem:
                        job['location'] = location_elem.get_text(strip=True)
                    
                    # URL
                    link = card.find('a', class_='base-card__full-link')
                    if link:
                        job['url'] = link.get('href', '')
                    
                    # Metadata
                    meta_elem = card.find('time')
                    if meta_elem:
                        job['posted'] = meta_elem.get_text(strip=True)
                    
                    if job['title'] and job['company']:
                        jobs.append(job)
                        
                except Exception as e:
                    continue
            
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"❌ LinkedIn search error: {e}")
        
        return jobs
    
    def search_company_career_page(self, company_url, keywords=None):
        """
        Scrape a specific company's career page
        """
        jobs = []
        
        try:
            response = self.session.get(company_url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for job listings (common patterns)
            job_patterns = [
                soup.find_all('div', class_=re.compile('job', re.I)),
                soup.find_all('li', class_=re.compile('job', re.I)),
                soup.find_all('a', href=re.compile('career|job|position', re.I)),
            ]
            
            for pattern in job_patterns:
                for elem in pattern[:20]:
                    try:
                        job = {
                            'title': elem.get_text(strip=True),
                            'company': 'Unknown',
                            'url': urljoin(company_url, elem.get('href', '')),
                            'source': 'Company Website',
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        if job['title'] and len(job['title']) < 100:
                            jobs.append(job)
                    except:
                        continue
            
        except Exception as e:
            print(f"❌ Company page error: {e}")
        
        return jobs
    
    def calculate_match_score(self, job, resume_keywords):
        """
        Calculate match score between job and resume
        Returns score 0-100
        """
        score = 0
        text = f"{job.get('title', '')} {job.get('summary', '')}".lower()
        
        # Keyword matching
        matches = 0
        for keyword in resume_keywords:
            if keyword.lower() in text:
                matches += 1
        
        if resume_keywords:
            score = (matches / len(resume_keywords)) * 100
        
        return round(score, 1)
    
    def save_jobs(self, jobs, filename="jobs.json"):
        """
        Save jobs to JSON file
        """
        import os
        filepath = os.path.expanduser(f"{self.cache_dir}/{filename}")
        
        with open(filepath, 'w') as f:
            json.dump(jobs, f, indent=2)
        
        print(f"💾 Saved {len(jobs)} jobs to {filepath}")
    
    def load_jobs(self, filename="jobs.json"):
        """
        Load jobs from JSON file
        """
        import os
        filepath = os.path.expanduser(f"{self.cache_dir}/{filename}")
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return []


# CLI interface
if __name__ == "__main__":
    import sys
    
    scraper = JobScraper()
    
    if len(sys.argv) > 1:
        query = sys.argv[1]
        location = sys.argv[2] if len(sys.argv) > 2 else ""
        
        print(f"🔍 Searching for: {query}")
        if location:
            print(f"📍 Location: {location}")
        print()
        
        # Search Indeed
        print("Searching Indeed...")
        indeed_jobs = scraper.search_indeed(query, location, max_results=25)
        print(f"  Found {len(indeed_jobs)} jobs")
        
        # Search LinkedIn
        print("Searching LinkedIn...")
        linkedin_jobs = scraper.search_linkedin(query, location, max_results=25)
        print(f"  Found {len(linkedin_jobs)} jobs")
        
        # Combine and save
        all_jobs = indeed_jobs + linkedin_jobs
        scraper.save_jobs(all_jobs)
        
        print(f"\n✅ Total: {len(all_jobs)} jobs found")
        print("\nTop 5 results:")
        for i, job in enumerate(all_jobs[:5], 1):
            print(f"{i}. {job['title']} at {job['company']}")
            print(f"   {job['location']} | {job['source']}")
            print()
    else:
        print("Usage: python job_scraper.py 'job title' [location]")
        print("Example: python job_scraper.py 'Product Manager' 'Nashville, TN'")
