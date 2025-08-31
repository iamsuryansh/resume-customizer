#!/usr/bin/env python3
"""
Configuration Manager for Resume Customizer Tool

This module handles loading and managing configuration from config files.
"""

import configparser
import os
from pathlib import Path
from typing import Dict, List, Any


class ConfigManager:
    """Manages configuration settings for the Resume Customizer Tool."""
    
    def __init__(self, config_dir: Path = None):
        """Initialize the configuration manager."""
        if config_dir is None:
            config_dir = Path(__file__).parent
        
        self.config_dir = config_dir
        self.config_file = config_dir / "config.ini"
        self.prompts_file = config_dir / "prompts.ini"
        
        # Load configurations
        self.config = configparser.ConfigParser()
        self.prompts = configparser.ConfigParser()
        
        self.load_configurations()
    
    def load_configurations(self):
        """Load configuration files."""
        # Load main config
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            self._create_default_config()
        
        # Load prompts config
        if self.prompts_file.exists():
            self.prompts.read(self.prompts_file)
        else:
            self._create_default_prompts()
    
    def _create_default_config(self):
        """Create default configuration if file doesn't exist."""
        self.config['ai'] = {
            'model': 'gemini-1.5-flash'
        }
        self.config['paths'] = {
            'templates_dir': 'templates',
            'output_dir': 'output',
            'job_descriptions_dir': 'job_descriptions'
        }
        self.config['files'] = {
            'resume_template': 'resume.tex',
            'resume_class': 'resume.cls'
        }
        self.config['output'] = {
            'max_job_title_length': '50',
            'include_timestamp': 'true',
            'cleanup_aux_files': 'true'
        }
        self.config['latex'] = {
            'compiler': 'pdflatex',
            'compilation_passes': '2',
            'compiler_options': '-interaction=nonstopmode',
            'aux_extensions': '.aux,.log,.out,.fdb_latexmk,.fls,.synctex.gz'
        }
        self.config['customization'] = {
            'focus_areas': 'skills,experience,summary,keywords',
            'add_explanations': 'false',
            'preserve_formatting': 'true',
            'max_retries': '3'
        }
        
        # Save default config
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def _create_default_prompts(self):
        """Create default prompts if file doesn't exist."""
        self.prompts['main_prompt'] = {
            'system_role': 'You are an expert resume writer and career consultant.',
            'instruction': 'Customize the resume to match job requirements while preserving LaTeX structure.'
        }
        
        # Save default prompts
        with open(self.prompts_file, 'w') as f:
            self.prompts.write(f)
    
    def get_ai_model(self) -> str:
        """Get the AI model to use."""
        return self.config.get('ai', 'model', fallback='gemini-1.5-flash')
    
    def get_templates_dir(self) -> Path:
        """Get the templates directory path."""
        return self.config_dir / self.config.get('paths', 'templates_dir', fallback='templates')
    
    def get_output_dir(self) -> Path:
        """Get the output directory path."""
        return self.config_dir / self.config.get('paths', 'output_dir', fallback='output')
    
    def get_job_descriptions_dir(self) -> Path:
        """Get the job descriptions directory path."""
        return self.config_dir / self.config.get('paths', 'job_descriptions_dir', fallback='job_descriptions')
    
    def get_resume_template_name(self) -> str:
        """Get the resume template filename."""
        return self.config.get('files', 'resume_template', fallback='resume.tex')
    
    def get_resume_class_name(self) -> str:
        """Get the resume class filename."""
        return self.config.get('files', 'resume_class', fallback='resume.cls')
    
    def get_max_job_title_length(self) -> int:
        """Get maximum job title length for filenames."""
        return self.config.getint('output', 'max_job_title_length', fallback=50)
    
    def should_include_timestamp(self) -> bool:
        """Check if timestamp should be included in filenames."""
        return self.config.getboolean('output', 'include_timestamp', fallback=True)
    
    def should_cleanup_aux_files(self) -> bool:
        """Check if auxiliary files should be cleaned up."""
        return self.config.getboolean('output', 'cleanup_aux_files', fallback=True)
    
    def get_latex_compiler(self) -> str:
        """Get LaTeX compiler command."""
        return self.config.get('latex', 'compiler', fallback='pdflatex')
    
    def get_compilation_passes(self) -> int:
        """Get number of LaTeX compilation passes."""
        return self.config.getint('latex', 'compilation_passes', fallback=2)
    
    def get_compiler_options(self) -> List[str]:
        """Get LaTeX compiler options as a list."""
        options = self.config.get('latex', 'compiler_options', fallback='-interaction=nonstopmode')
        return [opt.strip() for opt in options.split() if opt.strip()]
    
    def get_aux_extensions(self) -> List[str]:
        """Get list of auxiliary file extensions to clean up."""
        extensions = self.config.get('latex', 'aux_extensions', fallback='.aux,.log,.out')
        return [ext.strip() for ext in extensions.split(',') if ext.strip()]
    
    def get_focus_areas(self) -> List[str]:
        """Get list of focus areas for customization."""
        areas = self.config.get('customization', 'focus_areas', fallback='skills,experience,summary')
        return [area.strip() for area in areas.split(',') if area.strip()]
    
    def should_add_explanations(self) -> bool:
        """Check if explanatory comments should be added."""
        return self.config.getboolean('customization', 'add_explanations', fallback=False)
    
    def should_preserve_formatting(self) -> bool:
        """Check if original formatting should be strictly preserved."""
        return self.config.getboolean('customization', 'preserve_formatting', fallback=True)
    
    def get_max_retries(self) -> int:
        """Get maximum number of retry attempts for AI calls."""
        return self.config.getint('customization', 'max_retries', fallback=3)
    
    def build_ai_prompt(self, resume_content: str, job_description: str) -> str:
        """Build the complete AI prompt from configuration."""
        # Get prompt components
        role = self.prompts.get('system', 'role', fallback='You are an expert resume writer.')
        context = self.prompts.get('instructions', 'context', fallback='Customize the resume for the job.')
        focus_areas = self.prompts.get('customization', 'focus_areas', fallback='skills, experience')
        format_req = self.prompts.get('output', 'format_requirements', fallback='Return only LaTeX code.')
        quality = self.prompts.get('output', 'quality_guidelines', fallback='Ensure proper LaTeX syntax.')
        approach = self.prompts.get('style', 'approach', fallback='Maintain professional tone.')
        
        # Build the complete prompt
        prompt = f"""{role}

{context}

Focus on: {focus_areas}

IMPORTANT REQUIREMENTS:
- {format_req}
- {quality}
- {approach}

OUTPUT FORMAT:
Please return ONLY the complete customized LaTeX resume content. Do not include any explanations, markdown formatting, or additional text outside the LaTeX code.

Here's my current resume:
{resume_content}

Here's the job description:
{job_description}

Please provide the customized resume in LaTeX format:"""
        
        return prompt
    
    def update_config(self, section: str, key: str, value: str):
        """Update a configuration value."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, key, value)
        
        # Save to file
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def update_prompt(self, section: str, key: str, value: str):
        """Update a prompt configuration value."""
        if not self.prompts.has_section(section):
            self.prompts.add_section(section)
        
        self.prompts.set(section, key, value)
        
        # Save to file
        with open(self.prompts_file, 'w') as f:
            self.prompts.write(f)
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration."""
        return {
            'ai_model': self.get_ai_model(),
            'templates_dir': str(self.get_templates_dir()),
            'output_dir': str(self.get_output_dir()),
            'latex_compiler': self.get_latex_compiler(),
            'compilation_passes': self.get_compilation_passes(),
            'focus_areas': self.get_focus_areas(),
            'max_retries': self.get_max_retries(),
            'include_timestamp': self.should_include_timestamp(),
            'cleanup_aux_files': self.should_cleanup_aux_files(),
            'preserve_formatting': self.should_preserve_formatting(),
            'add_explanations': self.should_add_explanations()
        }


# Convenience function for getting default config manager
def get_config() -> ConfigManager:
    """Get the default configuration manager instance."""
    return ConfigManager()


if __name__ == "__main__":
    # Test the configuration manager
    config = get_config()
    print("Configuration Summary:")
    for key, value in config.get_config_summary().items():
        print(f"  {key}: {value}")
