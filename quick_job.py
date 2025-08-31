#!/usr/bin/env python3
"""
Quick Job Description File Creator
"""

import os
from pathlib import Path

def main():
    print("📝 Quick Job Description Creator")
    print("=" * 35)
    
    # Get job title
    job_title = input("Job title: ").strip()
    if not job_title:
        print("❌ Job title required!")
        return
    
    # Create filename
    clean_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = clean_title.replace(' ', '_').lower() + '.txt'
    
    print(f"\n📋 Paste the job description below (Ctrl+D when done):")
    print("-" * 50)
    
    # Read job description
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass
    
    content = '\n'.join(content_lines).strip()
    if not content:
        print("❌ Job description cannot be empty!")
        return
    
    # Save file
    job_dir = Path("job_descriptions")
    job_dir.mkdir(exist_ok=True)
    
    file_path = job_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Saved: {file_path}")
    print(f"\n🚀 Run customizer with:")
    print(f"python resume_customizer.py --job-file {file_path} --job-title \"{job_title}\"")

if __name__ == "__main__":
    main()
