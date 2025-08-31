#!/usr/bin/env python3
"""
Demo script to test the Resume Customizer with your actual job description
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from resume_customizer import ResumeCustomizer

def demo():
    """Demo the resume customizer with your job description."""
    print("🎯 Resume Customizer Demo")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not set. Run ./setup_api_key.sh first")
        return False
    
    try:
        # Initialize customizer
        print("🤖 Initializing Gemini AI...")
        customizer = ResumeCustomizer(api_key)
        
        # Use your actual job description file
        job_file = "job_description.txt"
        job_title = "ExxonMobil Software Engineer"
        
        print(f"📋 Processing job: {job_title}")
        print(f"📄 Using job description from: {job_file}")
        
        # Process the resume
        tex_path, pdf_path = customizer.process_resume(
            job_file, 
            is_file=True, 
            job_title=job_title
        )
        
        print("\n🎉 Success! Files generated:")
        print(f"📄 LaTeX: {tex_path}")
        print(f"📋 PDF: {pdf_path}")
        
        # Show file sizes
        tex_size = tex_path.stat().st_size
        pdf_size = pdf_path.stat().st_size
        print(f"\n📊 File sizes:")
        print(f"   LaTeX: {tex_size:,} bytes")
        print(f"   PDF: {pdf_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = demo()
    if success:
        print("\n✨ Demo completed successfully!")
        print("💡 You can now create more customized resumes using:")
        print("   python resume_customizer.py --job-file your_job.txt --job-title 'Job Title'")
    else:
        print("\n❌ Demo failed. Please check the error messages above.")
