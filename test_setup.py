#!/usr/bin/env python3
"""
Test script for the Resume Customizer Tool
"""

import os
import sys
from pathlib import Path

def test_setup():
    """Test if everything is set up correctly."""
    print("🧪 Testing Resume Customizer Setup...")
    print("=" * 40)
    
    # Check if files exist
    base_dir = Path(__file__).parent
    
    files_to_check = [
        "resume_customizer.py",
        "job_description.txt",
        "templates/resume.tex",
        "templates/resume.cls"
    ]
    
    print("📁 Checking required files...")
    all_files_exist = True
    for file_path in files_to_check:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_files_exist = False
    
    # Check API key
    print("\n🔑 Checking API key...")
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ GEMINI_API_KEY environment variable is set")
    else:
        print("❌ GEMINI_API_KEY environment variable is NOT set")
        print("💡 Set it with: export GEMINI_API_KEY='your_api_key_here'")
        all_files_exist = False
    
    # Check LaTeX installation
    print("\n📊 Checking LaTeX installation...")
    import subprocess
    try:
        result = subprocess.run(['pdflatex', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ pdflatex is installed")
        else:
            print("❌ pdflatex not working properly")
    except FileNotFoundError:
        print("❌ pdflatex is not installed")
        print("💡 Install with: sudo apt-get install texlive-latex-base texlive-latex-extra")
        all_files_exist = False
    
    print("\n" + "=" * 40)
    if all_files_exist:
        print("🎉 All checks passed! Ready to test the tool.")
        print("\n🚀 Test command:")
        print("python resume_customizer.py --job-file job_description.txt --job-title 'ExxonMobil Software Engineer'")
    else:
        print("❌ Some requirements are missing. Please fix the issues above.")
    
    return all_files_exist

if __name__ == "__main__":
    test_setup()
