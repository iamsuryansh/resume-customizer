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
from typing import Optional, Tuple

from config_manager import ConfigManager


class ResumeCustomizer:
    def __init__(self, api_key: str, config: ConfigManager = None):
        """Initialize the Resume Customizer with Gemini API key and configuration."""
        genai.configure(api_key=api_key)
        
        # Use provided config or create default
        self.config = config if config else ConfigManager()
        
        # Initialize AI model
        self.model = genai.GenerativeModel(self.config.get_ai_model())
        
        # Set up directories
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.config.get_templates_dir()
        self.output_dir = self.config.get_output_dir()
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
    
    def read_resume_template(self) -> str:
        """Read the original resume.tex file."""
        # Try configured paths
        resume_filename = self.config.get_resume_template_name()
        resume_paths = [
            self.templates_dir / resume_filename,
            self.base_dir / resume_filename,
            self.templates_dir / "resume.tex",  # fallback
            self.base_dir / "resume.tex"        # fallback
        ]
        
        for resume_path in resume_paths:
            if resume_path.exists():
                with open(resume_path, 'r', encoding='utf-8') as file:
                    return file.read()
        
        raise FileNotFoundError(f"Resume template not found in {[str(p) for p in resume_paths]}")
    
    def get_cls_file_path(self) -> Path:
        """Get the path to the resume.cls file."""
        # Try configured paths
        cls_filename = self.config.get_resume_class_name()
        cls_paths = [
            self.templates_dir / cls_filename,
            self.base_dir / cls_filename,
            self.templates_dir / "resume.cls",  # fallback
            self.base_dir / "resume.cls"        # fallback
        ]
        
        for cls_path in cls_paths:
            if cls_path.exists():
                return cls_path
        
        raise FileNotFoundError(f"Resume class file not found in {[str(p) for p in cls_paths]}")
    
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
        # Build prompt using configuration
        prompt = self.config.build_ai_prompt(resume_content, job_description)
        
        max_retries = self.config.get_max_retries()
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                result = response.text.strip()
                
                # Remove any code block markers if present
                if result.startswith('```'):
                    # Find the end of the opening code block marker
                    first_newline = result.find('\n')
                    if first_newline != -1:
                        result = result[first_newline + 1:]
                
                if result.endswith('```'):
                    result = result[:-3].rstrip()
                
                return result
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Attempt {attempt + 1} failed, retrying... ({str(e)})")
                    continue
                else:
                    raise Exception(f"Error communicating with Gemini after {max_retries} attempts: {str(e)}")
    
    def save_customized_resume(self, content: str, job_title: str = None) -> Path:
        """Save the customized resume content to a new .tex file."""
        # Generate filename based on configuration
        filename_parts = ["resume"]
        
        if job_title:
            # Clean job title for filename
            max_length = self.config.get_max_job_title_length()
            clean_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_title = clean_title.replace(' ', '_')[:max_length]
            filename_parts.append(clean_title)
        else:
            filename_parts.append("customized")
        
        if self.config.should_include_timestamp():
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_parts.append(timestamp)
        
        filename = "_".join(filename_parts) + ".tex"
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return output_path
    
    def compile_pdf(self, tex_file_path: Path) -> Path:
        """Compile the .tex file to PDF using pdflatex."""
        # Copy the .cls file to output directory if it exists
        try:
            cls_source = self.get_cls_file_path()
            cls_dest = self.output_dir / cls_source.name
            import shutil
            shutil.copy2(cls_source, cls_dest)
        except FileNotFoundError as e:
            print(f"⚠️  Warning: {e}")
            print("Proceeding without class file...")
        
        # Change to output directory for compilation
        original_cwd = os.getcwd()
        os.chdir(self.output_dir)
        
        try:
            # Get compilation settings from config
            compiler = self.config.get_latex_compiler()
            passes = self.config.get_compilation_passes()
            options = self.config.get_compiler_options()
            
            # Run LaTeX compilation
            for i in range(passes):
                print(f"📊 Running {compiler} (pass {i+1}/{passes})...")
                
                cmd = [compiler] + options + [tex_file_path.name]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    error_msg = f"LaTeX compilation failed on pass {i+1}:\n"
                    error_msg += f"Command: {' '.join(cmd)}\n"
                    error_msg += f"STDOUT:\n{result.stdout}\n"
                    error_msg += f"STDERR:\n{result.stderr}"
                    raise Exception(error_msg)
            
            pdf_path = tex_file_path.with_suffix('.pdf')
            if not pdf_path.exists():
                raise Exception("PDF file was not generated successfully")
            
            return pdf_path
            
        finally:
            os.chdir(original_cwd)
    
    def cleanup_latex_files(self, tex_file_path: Path):
        """Clean up auxiliary LaTeX files (.aux, .log, etc.)."""
        if not self.config.should_cleanup_aux_files():
            print("🔧 Skipping cleanup (disabled in config)")
            return
        
        aux_extensions = self.config.get_aux_extensions()
        cleaned_count = 0
        
        for ext in aux_extensions:
            aux_file = tex_file_path.with_suffix(ext)
            if aux_file.exists():
                aux_file.unlink()
                cleaned_count += 1
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned up {cleaned_count} auxiliary files")
    
    def process_resume(self, job_input: str, is_file: bool = False, job_title: str = None) -> Tuple[Path, Path]:
        """Main method to process resume customization."""
        print("📄 Reading resume template...")
        resume_content = self.read_resume_template()
        print(f"   📏 Resume content: {len(resume_content)} characters")
        
        print("💼 Reading job description...")
        job_description = self.read_job_description(job_input, is_file)
        print(f"   📏 Job description: {len(job_description)} characters")
        
        print(f"🤖 Customizing resume with {self.config.get_ai_model()}...")
        customized_content = self.customize_resume_with_gemini(resume_content, job_description)
        print(f"   📏 Customized content: {len(customized_content)} characters")
        
        print("💾 Saving customized resume...")
        tex_path = self.save_customized_resume(customized_content, job_title)
        
        print("📊 Compiling PDF...")
        pdf_path = self.compile_pdf(tex_path)
        
        print("🧹 Managing auxiliary files...")
        self.cleanup_latex_files(tex_path)
        
        return tex_path, pdf_path


def main():
    parser = argparse.ArgumentParser(description="Customize resume for specific job using Gemini AI")
    
    # Job description input (mutually exclusive)
    job_group = parser.add_mutually_exclusive_group(required=False)
    job_group.add_argument('--job-description', '-d', 
                          help="Job description as text")
    job_group.add_argument('--job-file', '-f', 
                          help="Path to text file containing job description")
    
    # Optional parameters
    parser.add_argument('--job-title', '-t', 
                       help="Job title for better file naming")
    parser.add_argument('--api-key', '-k', 
                       help="Gemini API key (or set GEMINI_API_KEY environment variable)")
    parser.add_argument('--config-dir', '-c',
                       help="Directory containing config files (default: current directory)")
    parser.add_argument('--show-config', action='store_true',
                       help="Show current configuration and exit")
    parser.add_argument('--model', '-m',
                       help="Override AI model to use (e.g., gemini-1.5-pro)")
    
    args = parser.parse_args()
    
    try:
        # Initialize configuration
        config_dir = Path(args.config_dir) if args.config_dir else None
        config = ConfigManager(config_dir)
        
        # Override model if specified
        if args.model:
            config.update_config('ai', 'model', args.model)
        
        # Show configuration if requested
        if args.show_config:
            print("📋 Current Configuration:")
            print("-" * 40)
            for key, value in config.get_config_summary().items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
            return
        
        # Check if job description is provided for customization
        if not args.job_description and not args.job_file:
            parser.error("Job description is required for resume customization. Use --job-description or --job-file, or --show-config to view configuration.")
        
        # Get API key
        api_key = args.api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ Error: Please provide Gemini API key via --api-key or GEMINI_API_KEY environment variable")
            sys.exit(1)
        
        # Initialize customizer with configuration
        customizer = ResumeCustomizer(api_key, config)
        
        # Show configuration summary
        print(f"🔧 Using model: {config.get_ai_model()}")
        print(f"📁 Templates directory: {config.get_templates_dir()}")
        print(f"📂 Output directory: {config.get_output_dir()}")
        print()
        
        # Determine input type and process
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
        
        # Show results
        tex_size = tex_path.stat().st_size
        pdf_size = pdf_path.stat().st_size
        
        print("\n✅ Resume customization completed successfully!")
        print(f"📄 LaTeX file: {tex_path}")
        print(f"📋 PDF file: {pdf_path}")
        print(f"📊 File sizes: LaTeX={tex_size:,} bytes, PDF={pdf_size:,} bytes")
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
