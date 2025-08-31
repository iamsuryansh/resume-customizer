#!/usr/bin/env python3
"""
Test mode for Resume Customizer - simulates AI response to test LaTeX compilation
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path
import shutil

class TestResumeCustomizer:
    def __init__(self):
        """Initialize test mode."""
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)
    
    def read_resume_template(self) -> str:
        """Read the original resume.tex file."""
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
        cls_paths = [
            self.templates_dir / "resume.cls",
            self.base_dir / "resume.cls"
        ]
        
        for cls_path in cls_paths:
            if cls_path.exists():
                return cls_path
        
        raise FileNotFoundError(f"Resume class file not found in {cls_paths}")
    
    def read_job_description(self, job_file: str) -> str:
        """Read job description from file."""
        job_path = Path(job_file)
        if not job_path.exists():
            raise FileNotFoundError(f"Job description file not found at {job_path}")
        
        with open(job_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    
    def simulate_customization(self, resume_content: str, job_description: str) -> str:
        """Simulate AI customization by making small targeted changes."""
        print("🔄 Simulating AI customization...")
        
        # For testing, we'll make some targeted changes based on the ExxonMobil job
        customized = resume_content
        
        # Update summary to mention Azure and microservices
        if "Software Engineer with 4 years of experience" in customized:
            customized = customized.replace(
                "Software Engineer with 4 years of experience building scalable \\textbf{Python APIs} and backend systems within \\textbf{microservice} architectures.",
                "Software Engineer with 4 years of experience building scalable \\textbf{Python APIs} and backend systems within \\textbf{microservice} architectures. Experienced with \\textbf{Azure} cloud technologies and \\textbf{REST APIs}."
            )
        
        # Add a comment to show this is test-customized
        customized = "% Test-customized resume for ExxonMobil Software Engineer position\n" + customized
        
        return customized
    
    def save_customized_resume(self, content: str, job_title: str = None) -> Path:
        """Save the customized resume content to a new .tex file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if job_title:
            clean_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_title = clean_title.replace(' ', '_')[:50]
            filename = f"resume_{clean_title}_{timestamp}.tex"
        else:
            filename = f"resume_test_{timestamp}.tex"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return output_path
    
    def compile_pdf(self, tex_file_path: Path) -> Path:
        """Compile the .tex file to PDF using pdflatex."""
        # Copy the .cls file to output directory
        try:
            cls_source = self.get_cls_file_path()
            cls_dest = self.output_dir / "resume.cls"
            shutil.copy2(cls_source, cls_dest)
        except FileNotFoundError as e:
            print(f"⚠️  Warning: {e}")
        
        # Change to output directory for compilation
        original_cwd = os.getcwd()
        os.chdir(self.output_dir)
        
        try:
            # Run pdflatex twice
            for i in range(2):
                print(f"📊 Running pdflatex (pass {i+1}/2)...")
                result = subprocess.run([
                    'pdflatex', 
                    '-interaction=nonstopmode',
                    tex_file_path.name
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print("LaTeX Output:")
                    print(result.stdout)
                    print("LaTeX Errors:")
                    print(result.stderr)
                    raise Exception(f"LaTeX compilation failed on pass {i+1}")
            
            pdf_path = tex_file_path.with_suffix('.pdf')
            if not pdf_path.exists():
                raise Exception("PDF file was not generated")
            
            return pdf_path
            
        finally:
            os.chdir(original_cwd)
    
    def cleanup_latex_files(self, tex_file_path: Path):
        """Clean up auxiliary LaTeX files."""
        aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
        for ext in aux_extensions:
            aux_file = tex_file_path.with_suffix(ext)
            if aux_file.exists():
                aux_file.unlink()
    
    def test_process(self) -> bool:
        """Test the complete process."""
        try:
            print("📄 Reading resume template...")
            resume_content = self.read_resume_template()
            print(f"   Resume length: {len(resume_content)} characters")
            
            print("💼 Reading job description...")
            job_description = self.read_job_description("job_description.txt")
            print(f"   Job description length: {len(job_description)} characters")
            
            print("🤖 Simulating AI customization...")
            customized_content = self.simulate_customization(resume_content, job_description)
            
            print("💾 Saving test resume...")
            tex_path = self.save_customized_resume(customized_content, "ExxonMobil_Test")
            
            print("📊 Compiling PDF...")
            pdf_path = self.compile_pdf(tex_path)
            
            print("🧹 Cleaning up auxiliary files...")
            self.cleanup_latex_files(tex_path)
            
            print(f"\n✅ Test completed successfully!")
            print(f"📄 LaTeX file: {tex_path}")
            print(f"📋 PDF file: {pdf_path}")
            
            # Show file sizes
            tex_size = tex_path.stat().st_size
            pdf_size = pdf_path.stat().st_size
            print(f"\n📊 Generated files:")
            print(f"   LaTeX: {tex_size:,} bytes")
            print(f"   PDF: {pdf_size:,} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

def main():
    print("🧪 Resume Customizer - Test Mode")
    print("=" * 40)
    print("This will test LaTeX compilation without calling Gemini AI")
    print("")
    
    tester = TestResumeCustomizer()
    success = tester.test_process()
    
    if success:
        print("\n🎉 LaTeX compilation test passed!")
        print("💡 The tool is ready. Get your Gemini API key to enable AI customization.")
    else:
        print("\n❌ Test failed. Check the error messages above.")

if __name__ == "__main__":
    main()
