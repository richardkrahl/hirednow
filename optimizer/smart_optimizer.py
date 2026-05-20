#!/usr/bin/env python3
"""
JARVIS Smart Resume Optimizer
Analyzes resume against job description and suggests improvements
"""

import json
import re
import subprocess
import os
from typing import Dict, List, Tuple

class SmartResumeOptimizer:
    """
    AI-powered resume optimization for specific job applications
    """
    
    def __init__(self, resume_path: str, model: str = "hoangquan456/qwen3-nothink:8b"):
        self.resume_path = resume_path
        self.model = model
        self.resume_text = self._load_resume()
    
    def _load_resume(self) -> str:
        """Load resume from file"""
        with open(os.path.expanduser(self.resume_path), 'r') as f:
            return f.read()
    
    def extract_job_keywords(self, job_description: str) -> List[str]:
        """Extract key skills/requirements from job description"""
        prompt = f"""Extract the top 15 most important keywords, skills, and requirements from this job description.
Return ONLY a comma-separated list, nothing else.

Job Description:
{job_description[:3000]}"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            keywords = result.stdout.strip()
            # Clean and split
            keywords = [k.strip().lower() for k in keywords.replace('\n', ',').split(',') if k.strip()]
            return keywords[:15]
        
        except Exception as e:
            print(f"Keyword extraction error: {e}")
            return []
    
    def calculate_match_score(self, job_description: str) -> Dict:
        """Calculate ATS match score between resume and job"""
        keywords = self.extract_job_keywords(job_description)
        resume_lower = self.resume_text.lower()
        
        matches = []
        missing = []
        
        for keyword in keywords:
            # Check for keyword or synonyms
            if keyword in resume_lower:
                matches.append(keyword)
            else:
                missing.append(keyword)
        
        score = (len(matches) / len(keywords)) * 100 if keywords else 0
        
        return {
            'score': round(score, 1),
            'keywords': keywords,
            'matched': matches,
            'missing': missing,
            'recommendation': 'strong' if score >= 80 else 'moderate' if score >= 60 else 'weak'
        }
    
    def generate_tailored_resume(self, job_title: str, company: str, job_description: str) -> str:
        """Generate tailored resume for specific job"""
        match_data = self.calculate_match_score(job_description)
        
        prompt = f"""You are an expert resume writer. Rewrite this resume to better match the job description.

JOB:
Title: {job_title}
Company: {company}

ORIGINAL RESUME:
{self.resume_text[:2000]}

JOB DESCRIPTION KEYWORDS (MUST INCLUDE):
{', '.join(match_data['missing'][:8])}

Instructions:
1. Keep the same basic structure
2. Incorporate the missing keywords naturally
3. Emphasize relevant experience
4. Keep it under 400 words
5. Make it ATS-friendly

TAILORED RESUME:"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.stdout.strip()
        
        except Exception as e:
            return f"Error generating tailored resume: {e}"
    
    def generate_bullet_improvements(self, job_description: str) -> List[str]:
        """Suggest improved bullet points"""
        prompt = f"""Given this resume and job description, suggest 3 improved bullet points
for the work experience section that better match the job requirements.

RESUME:
{self.resume_text[:2000]}

JOB REQUIREMENTS:
{job_description[:1500]}

Suggest 3 improved bullets (keep them concise, results-oriented):"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.stdout.strip().split('\n')[:3]
        
        except Exception as e:
            return [f"Error: {e}"]
    
    def create_cover_letter(self, job_title: str, company: str, job_description: str) -> str:
        """Generate personalized cover letter"""
        prompt = f"""Write a compelling cover letter for this job application.

Job: {job_title} at {company}

Resume Highlights:
{self.resume_text[:1500]}

Job Description:
{job_description[:1500]}

Write a professional cover letter (300-400 words) that:
1. Shows enthusiasm for the role
2. Matches experience to requirements
3. Demonstrates knowledge of the company
4. Has a strong call to action

Cover Letter:"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.stdout.strip()
        
        except Exception as e:
            return f"Error generating cover letter: {e}"
    
    def full_optimization_report(self, job_title: str, company: str, job_description: str) -> Dict:
        """Generate complete optimization report"""
        print(f"🤖 Analyzing resume for {job_title} at {company}...")
        
        match_score = self.calculate_match_score(job_description)
        
        print(f"   Match score: {match_score['score']}%")
        print(f"   Recommendation: {match_score['recommendation'].upper()}")
        
        report = {
            'job_title': job_title,
            'company': company,
            'match_score': match_score,
            'bullet_suggestions': self.generate_bullet_improvements(job_description),
            'tailored_resume': self.generate_tailored_resume(job_title, company, job_description),
            'cover_letter': self.create_cover_letter(job_title, company, job_description)
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print formatted optimization report"""
        print("\n" + "="*60)
        print(f"📄 RESUME OPTIMIZATION REPORT")
        print("="*60)
        
        print(f"\n🎯 JOB: {report['job_title']} at {report['company']}")
        
        score = report['match_score']
        print(f"\n📊 ATS MATCH SCORE: {score['score']}%")
        print(f"   Recommendation: {score['recommendation'].upper()}")
        
        if score['matched']:
            print(f"\n✅ MATCHED KEYWORDS ({len(score['matched'])}):")
            print(f"   {', '.join(score['matched'][:8])}")
        
        if score['missing']:
            print(f"\n⚠️  MISSING KEYWORDS ({len(score['missing'])}):")
            print(f"   {', '.join(score['missing'][:8])}")
        
        if report['bullet_suggestions']:
            print(f"\n💡 SUGGESTED BULLETS:")
            for i, bullet in enumerate(report['bullet_suggestions'], 1):
                print(f"   {i}. {bullet}")
        
        print(f"\n📝 TAILORED RESUME:")
        print("-"*60)
        print(report['tailored_resume'])
        
        print(f"\n✉️  COVER LETTER:")
        print("-"*60)
        print(report['cover_letter'])
        
        print("\n" + "="*60)


# CLI interface
if __name__ == "__main__":
    import sys
    
    resume_path = "~/.openclaw/workspace/projects/job-hunter/data/resume_text.txt"
    
    if len(sys.argv) < 4:
        print("Usage: python smart_optimizer.py 'Job Title' 'Company' 'path/to/job_description.txt'")
        print("\nExample:")
        print("  python smart_optimizer.py 'Product Manager' 'Google' job_desc.txt")
        sys.exit(1)
    
    job_title = sys.argv[1]
    company = sys.argv[2]
    job_desc_path = sys.argv[3]
    
    # Load job description
    try:
        with open(job_desc_path, 'r') as f:
            job_description = f.read()
    except FileNotFoundError:
        print(f"❌ Job description not found: {job_desc_path}")
        sys.exit(1)
    
    # Run optimization
    optimizer = SmartResumeOptimizer(resume_path)
    report = optimizer.full_optimization_report(job_title, company, job_description)
    optimizer.print_report(report)
    
    # Save outputs
    output_dir = "~/.openclaw/workspace/projects/job-hunter/outputs"
    os.makedirs(os.path.expanduser(output_dir), exist_ok=True)
    
    base_name = f"{company.lower().replace(' ', '_')}_{job_title.lower().replace(' ', '_')}"
    
    # Save tailored resume
    resume_path = os.path.expanduser(f"{output_dir}/{base_name}_resume.txt")
    with open(resume_path, 'w') as f:
        f.write(report['tailored_resume'])
    print(f"\n💾 Saved tailored resume to: {resume_path}")
    
    # Save cover letter
    cover_path = os.path.expanduser(f"{output_dir}/{base_name}_cover_letter.txt")
    with open(cover_path, 'w') as f:
        f.write(report['cover_letter'])
    print(f"💾 Saved cover letter to: {cover_path}")
