#!/usr/bin/env python3
"""
Simple script to create a job description file interactively.
"""

import os
from pathlib import Path

def create_job_description_file():
    """Interactive script to create job description files."""
    print("📝 Job Description File Creator")
    print("=" * 40)
    
    # Get job title
    job_title = input("Enter the job title: ").strip()
    if not job_title:
        print("❌ Job title is required!")
        return
    
    # Clean filename
    clean_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = clean_title.replace(' ', '_').lower() + '.txt'
    
    # Get job description
    print(f"\nEnter the job description (press Ctrl+D when finished):")
    print("-" * 50)
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    job_description = '\n'.join(lines).strip()
    
    if not job_description:
        print("❌ Job description cannot be empty!")
        return
    
    # Save file
    job_descriptions_dir = Path(__file__).parent / "job_descriptions"
    job_descriptions_dir.mkdir(exist_ok=True)
    
    file_path = job_descriptions_dir / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(job_description)
    
    print(f"\n✅ Job description saved to: {file_path}")
    print(f"\nYou can now run:")
    print(f"python resume_customizer.py --job-file {file_path} --job-title \"{job_title}\"")

if __name__ == "__main__":
    create_job_description_file()
