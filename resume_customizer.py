#!/usr/bin/env python3
"""
Resume Customizer Tool

This tool takes a job description (via text input or file) and your resume content,
sends both to Gemini AI to customize the resume for the specific job, then generates
a PDF using LaTeX.

Usage:
    python resume_customizer.py --job-description "Your job description here"
    python resume_customizer.py --job-file path/to/job_description.txt
"""

import os
import sys
import argparse
import subprocess
import datetime
from pathlib import Path
import google.generativeai as genai
from typing import Optional


class ResumeCustomizer:
    def __init__(self, api_key: str):
        """Initialize the Resume Customizer with Gemini API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir / "output"
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
    
    def read_resume_template(self) -> str:
        """Read the original resume.tex file."""
        # Try templates directory first, then root directory
        resume_paths = [
            self.templates_dir / "resume.tex",
            self.base_dir / "resume.tex"
        ]
        
        for resume_path in resume_paths:
            if resume_path.exists():
                with open(resume_path, 'r', encoding='utf-8') as file:
                    return file.read()
        
        raise FileNotFoundError(f"Resume template not found in {resume_paths}")
    
    def get_cls_file_path(self) -> Path:
        """Get the path to the resume.cls file."""
        # Try templates directory first, then root directory
        cls_paths = [
            self.templates_dir / "resume.cls",
            self.base_dir / "resume.cls"
        ]
        
        for cls_path in cls_paths:
            if cls_path.exists():
                return cls_path
        
        raise FileNotFoundError(f"Resume class file not found in {cls_paths}")
    
    def read_job_description(self, job_input: str, is_file: bool = False) -> str:
        """Read job description from text or file."""
        if is_file:
            job_path = Path(job_input)
            if not job_path.exists():
                raise FileNotFoundError(f"Job description file not found at {job_path}")
            
            with open(job_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        else:
            return job_input.strip()
    
    def customize_resume_with_gemini(self, resume_content: str, job_description: str) -> str:
        """Send resume and job description to Gemini for customization."""
        prompt = f"""
You are an expert resume writer. I will provide you with:
1. My current resume in LaTeX format
2. A job description for a position I'm applying to

Please customize my resume to better match the job requirements while keeping the same LaTeX structure and formatting. Focus on:
- Highlighting relevant skills and experiences that match the job requirements
- Adjusting the summary/objective to align with the role
- Reordering or emphasizing experiences that are most relevant
- Using keywords from the job description where appropriate
- Maintaining professional tone and accuracy

IMPORTANT: 
- Return ONLY the modified LaTeX content, no explanations or markdown formatting
- Keep the same document structure and LaTeX commands
- Don't add any content that isn't true or verifiable
- Preserve all LaTeX formatting and commands exactly

Here's my current resume:
{resume_content}

Here's the job description:
{job_description}

Please provide the customized resume in LaTeX format:
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Error communicating with Gemini: {str(e)}")
    
    def save_customized_resume(self, content: str, job_title: str = None) -> Path:
        """Save the customized resume content to a new .tex file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if job_title:
            # Clean job title for filename
            clean_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_title = clean_title.replace(' ', '_')[:50]  # Limit length
            filename = f"resume_{clean_title}_{timestamp}.tex"
        else:
            filename = f"resume_customized_{timestamp}.tex"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return output_path
    
    def compile_pdf(self, tex_file_path: Path) -> Path:
        """Compile the .tex file to PDF using pdflatex."""
        # Copy the .cls file to output directory if it exists
        try:
            cls_source = self.get_cls_file_path()
            cls_dest = self.output_dir / "resume.cls"
            import shutil
            shutil.copy2(cls_source, cls_dest)
        except FileNotFoundError as e:
            print(f"⚠️  Warning: {e}")
            print("Proceeding without class file...")
        
        # Change to output directory for compilation
        original_cwd = os.getcwd()
        os.chdir(self.output_dir)
        
        try:
            # Run pdflatex twice (standard for LaTeX compilation)
            for i in range(2):
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    tex_file_path.name
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise Exception(f"LaTeX compilation failed:\n{result.stdout}\n{result.stderr}")
            
            pdf_path = tex_file_path.with_suffix('.pdf')
            if not pdf_path.exists():
                raise Exception("PDF file was not generated successfully")
            
            return pdf_path
            
        finally:
            os.chdir(original_cwd)
    
    def cleanup_latex_files(self, tex_file_path: Path):
        """Clean up auxiliary LaTeX files (.aux, .log, etc.)."""
        aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
        for ext in aux_extensions:
            aux_file = tex_file_path.with_suffix(ext)
            if aux_file.exists():
                aux_file.unlink()
    
    def process_resume(self, job_input: str, is_file: bool = False, job_title: str = None) -> tuple[Path, Path]:
        """Main method to process resume customization."""
        print("📄 Reading resume template...")
        resume_content = self.read_resume_template()
        
        print("💼 Reading job description...")
        job_description = self.read_job_description(job_input, is_file)
        
        print("🤖 Customizing resume with Gemini AI...")
        customized_content = self.customize_resume_with_gemini(resume_content, job_description)
        
        print("💾 Saving customized resume...")
        tex_path = self.save_customized_resume(customized_content, job_title)
        
        print("📊 Compiling PDF...")
        pdf_path = self.compile_pdf(tex_path)
        
        print("🧹 Cleaning up auxiliary files...")
        self.cleanup_latex_files(tex_path)
        
        return tex_path, pdf_path


def main():
    parser = argparse.ArgumentParser(description="Customize resume for specific job using Gemini AI")
    
    # Job description input (mutually exclusive)
    job_group = parser.add_mutually_exclusive_group(required=True)
    job_group.add_argument('--job-description', '-d', 
                          help="Job description as text")
    job_group.add_argument('--job-file', '-f', 
                          help="Path to text file containing job description")
    
    # Optional parameters
    parser.add_argument('--job-title', '-t', 
                       help="Job title for better file naming")
    parser.add_argument('--api-key', '-k', 
                       help="Gemini API key (or set GEMINI_API_KEY environment variable)")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: Please provide Gemini API key via --api-key or GEMINI_API_KEY environment variable")
        sys.exit(1)
    
    try:
        # Initialize customizer
        customizer = ResumeCustomizer(api_key)
        
        # Determine input type
        if args.job_file:
            tex_path, pdf_path = customizer.process_resume(
                args.job_file, 
                is_file=True, 
                job_title=args.job_title
            )
        else:
            tex_path, pdf_path = customizer.process_resume(
                args.job_description, 
                is_file=False, 
                job_title=args.job_title
            )
        
        print("\n✅ Resume customization completed successfully!")
        print(f"📄 LaTeX file: {tex_path}")
        print(f"📋 PDF file: {pdf_path}")
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
