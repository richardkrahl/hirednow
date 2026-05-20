#!/usr/bin/env python3
"""
JARVIS Resume Optimizer
AI-powered resume and cover letter optimization
Uses local Ollama for privacy
"""

import subprocess
import json
import re
from datetime import datetime

class ResumeOptimizer:
    """
    Optimize resumes and generate cover letters using local AI
    No data sent to cloud - 100% private
    """
    
    def __init__(self, model="hoangquan456/qwen3-nothink:8b"):
        self.model = model
    
    def extract_keywords(self, job_description):
        """
        Extract key skills/requirements from job description
        """
        prompt = f"""Extract the top 10 most important keywords/skills from this job description.
Return only a comma-separated list, nothing else.

Job Description:
{job_description[:2000]}"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            keywords = result.stdout.strip()
            # Clean up and split
            keywords = [k.strip() for k in keywords.replace('\n', ',').split(',') if k.strip()]
            return keywords[:10]
        
        except Exception as e:
            print(f"❌ Keyword extraction error: {e}")
            return []
    
    def calculate_ats_score(self, resume_text, job_description):
        """
        Calculate ATS (Applicant Tracking System) match score
        """
        job_keywords = self.extract_keywords(job_description)
        resume_lower = resume_text.lower()
        
        matches = 0
        matched_keywords = []
        
        for keyword in job_keywords:
            if keyword.lower() in resume_lower:
                matches += 1
                matched_keywords.append(keyword)
        
        score = (matches / len(job_keywords)) * 100 if job_keywords else 0
        
        return {
            'score': round(score, 1),
            'total_keywords': len(job_keywords),
            'matched': matches,
            'missing': [k for k in job_keywords if k.lower() not in resume_lower],
            'matched_keywords': matched_keywords
        }
    
    def suggest_improvements(self, resume_text, job_description):
        """
        Get AI suggestions for resume improvements
        """
        prompt = f"""You are an expert resume writer and ATS optimizer.

Analyze this resume against the job description and suggest specific improvements.
Focus on:
1. Missing keywords to add
2. Skills to emphasize
3. Experience to highlight
4. Format improvements

Job Description:
{job_description[:1500]}

Current Resume:
{resume_text[:2000]}

Provide 5-7 specific, actionable suggestions:"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.stdout.strip()
        
        except Exception as e:
            return f"Error generating suggestions: {e}"
    
    def generate_cover_letter(self, resume_text, job_title, company, job_description, tone="professional"):
        """
        Generate personalized cover letter
        """
        prompt = f"""Write a {tone} cover letter for this job application.

Job Title: {job_title}
Company: {company}

Job Description:
{job_description[:1500]}

Candidate Resume Highlights:
{resume_text[:1500]}

Write a compelling cover letter (300-400 words) that:
1. Shows enthusiasm for the role
2. Matches candidate experience to job requirements
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
    
    def tailor_resume(self, resume_text, job_description):
        """
        Create tailored resume bullet points for specific job
        """
        prompt = f"""Given this resume and job description, rewrite 3-5 bullet points
from the resume to better match the job requirements.

Job Description:
{job_description[:1500]}

Current Resume:
{resume_text[:1500]}

Provide improved bullet points:"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.stdout.strip()
        
        except Exception as e:
            return f"Error tailoring resume: {e}"
    
    def analyze_resume(self, resume_text):
        """
        General resume analysis and feedback
        """
        prompt = f"""Analyze this resume and provide feedback on:
1. Overall strengths
2. Areas for improvement
3. Missing sections (if any)
4. Format suggestions
5. Impact of bullet points

Resume:
{resume_text[:2000]}

Analysis:"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.stdout.strip()
        
        except Exception as e:
            return f"Error analyzing resume: {e}"


# CLI interface
if __name__ == "__main__":
    import sys
    import os
    
    optimizer = ResumeOptimizer()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python resume_optimizer.py analyze <resume_file>")
        print("  python resume_optimizer.py score <resume_file> <job_description>")
        print("  python resume_optimizer.py cover <resume_file> <job_title> <company> <job_description>")
        print("  python resume_optimizer.py improve <resume_file> <job_description>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "analyze" and len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            resume = f.read()
        print(optimizer.analyze_resume(resume))
    
    elif command == "score" and len(sys.argv) > 3:
        with open(sys.argv[2], 'r') as f:
            resume = f.read()
        with open(sys.argv[3], 'r') as f:
            job = f.read()
        
        score_data = optimizer.calculate_ats_score(resume, job)
        print(f"\n📊 ATS Match Score: {score_data['score']}%")
        print(f"   Matched {score_data['matched']} of {score_data['total_keywords']} keywords")
        print(f"\n✅ Matched: {', '.join(score_data['matched_keywords'])}")
        print(f"\n❌ Missing: {', '.join(score_data['missing'])}")
    
    elif command == "cover" and len(sys.argv) > 5:
        with open(sys.argv[2], 'r') as f:
            resume = f.read()
        job_title = sys.argv[3]
        company = sys.argv[4]
        with open(sys.argv[5], 'r') as f:
            job_desc = f.read()
        
        print(optimizer.generate_cover_letter(resume, job_title, company, job_desc))
    
    elif command == "improve" and len(sys.argv) > 3:
        with open(sys.argv[2], 'r') as f:
            resume = f.read()
        with open(sys.argv[3], 'r') as f:
            job = f.read()
        
        print(optimizer.suggest_improvements(resume, job))
    
    else:
        print("Invalid command. Use --help for usage.")
